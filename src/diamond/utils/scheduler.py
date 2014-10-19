# coding=utf-8

import time
import multiprocessing
import os
import sys
import signal

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
    reload_config = False
    
    # Setup stderr/stdout as /dev/null so random print statements in thrid
    # party libs do not fail and prevent collectors from running.
    # https://github.com/BrightcoveOS/Diamond/issues/722
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    while(True):
        try:
            time_to_sleep = next_collection - time.time()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

            next_collection += interval

            # Ensure collector run times fit into the collection window
            signal.alarm(max_time)

            # Collect!
            collector._run()

            # Success! Disable the alarm
            signal.alarm(0)

            # Reload the config if requested
            # This is outside of the alarm code as we don't want to interrupt
            # it and end up with half a loaded config
            if reload_config:
                log.debug('Reloading config')
                collector.load_config()
                log.info('Config reloaded')
                reload_config = False

        except SIGALRMException:
            log.error('Took too long to run! Killed!')
            continue

        except SIGUSR1Exception:
            log.info('Scheduling config reload due to USR1')
            reload_config = True
            pass

        except SIGUSR2Exception:
            log.debug('Received USR2')
            pass


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
