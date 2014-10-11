# coding=utf-8

import time
import multiprocessing
import sys
import signal
import traceback

try:
    from setproctitle import getproctitle, setproctitle
except ImportError:
    setproctitle = None

from diamond.utils.signals import signal_to_exception
from diamond.utils.signals import SIGALRMException
from diamond.utils.signals import SIGUSR1Exception
from diamond.utils.signals import SIGUSR2Exception


def collector_process(collector, metric_queue, log):
    """
    """
    proc = multiprocessing.current_process()
    if setproctitle:
        setproctitle('%s - %s' % (getproctitle(), proc.name))

    signal.signal(signal.SIGALRM, signal_to_exception)
    signal.signal(signal.SIGUSR1, signal_to_exception)
    signal.signal(signal.SIGUSR2, signal_to_exception)

    interval = float(collector.config['interval'])
    max_time = int(interval * 0.9)

    log.debug('Starting')
    log.debug('Interval: %s seconds', interval)
    log.debug('Max collection time: %s seconds', max_time)

    # Validate the interval
    if interval <= 0:
        log.critical('interval of %s is not valid!', interval)
        sys.exit(1)

    next_collection = time.time()

    while(True):
        try:
            time.sleep(next_collection - time.time())

            next_collection += interval

            # Ensure collector run times fit into the collection window
            signal.alarm(max_time)

            # Collect!
            collector._run()

            # Success! Disable the alarm
            signal.alarm(0)

        except SIGALRMException, e:
            log.error('Took too long to run! Killed!')
            continue

        except SIGUSR1Exception:
            log.debug('Received USR1')
            pass

        except SIGUSR2Exception:
            log.debug('Received USR2')
            pass

        # Any other exception? Kill the thread
        except Exception, e:
            traceback.print_stack()
            log.error('%s(%s)', e, e.args)
            raise e
            break


def handler_process(handlers, metric_queue, log):
    proc = multiprocessing.current_process()
    if setproctitle:
        setproctitle('%s - %s' % (getproctitle(), proc.name))

    log.debug('Starting process %s', proc.name)

    while(True):
        metrics = metric_queue.get(block=True, timeout=None)
        for metric in metrics:
            for handler in handlers:
                handler._process(metric)
        for handler in handlers:
            handler._flush()
