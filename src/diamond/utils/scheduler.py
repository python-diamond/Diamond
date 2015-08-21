# coding=utf-8

import time
import math
import multiprocessing
import os
import random
import sys
import signal

try:
    from setproctitle import getproctitle, setproctitle
except ImportError:
    setproctitle = None

from diamond.utils.signals import signal_to_exception
from diamond.utils.signals import SIGALRMException
from diamond.utils.signals import SIGHUPException


def collector_process(collector, metric_queue, log):
    """
    """
    proc = multiprocessing.current_process()
    if setproctitle:
        setproctitle('%s - %s' % (getproctitle(), proc.name))

    signal.signal(signal.SIGALRM, signal_to_exception)
    signal.signal(signal.SIGHUP, signal_to_exception)
    signal.signal(signal.SIGUSR2, signal_to_exception)

    interval = float(collector.config['interval'])

    log.debug('Starting')
    log.debug('Interval: %s seconds', interval)

    # Validate the interval
    if interval <= 0:
        log.critical('interval of %s is not valid!', interval)
        sys.exit(1)

    # Start the next execution at the next window plus some stagger delay to
    # avoid having all collectors running at the same time
    next_window = math.floor(time.time() / interval) * interval
    stagger_offset = random.uniform(0, interval - 1)

    # Allocate time till the end of the window for the collector to run. With a
    # minimum of 1 second
    max_time = int(max(interval - stagger_offset, 1))
    log.debug('Max collection time: %s seconds', max_time)

    # Setup stderr/stdout as /dev/null so random print statements in thrid
    # party libs do not fail and prevent collectors from running.
    # https://github.com/BrightcoveOS/Diamond/issues/722
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    while(True):
        try:
            time_to_sleep = (next_window + stagger_offset) - time.time()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            elif time_to_sleep < 0:
                # clock has jumped, lets skip missed intervals
                next_window = time.time()

            next_window += interval

            # Ensure collector run times fit into the collection window
            signal.alarm(max_time)

            # Collect!
            collector._run()

            # Success! Disable the alarm
            signal.alarm(0)

        except SIGALRMException:
            log.error('Took too long to run! Killed!')

            # Adjust  the stagger_offset to allow for more time to run the
            # collector
            stagger_offset = stagger_offset * 0.9

            max_time = int(max(interval - stagger_offset, 1))
            log.debug('Max collection time: %s seconds', max_time)

        except SIGHUPException:
            # Reload the config if requested
            # We must first disable the alarm as we don't want it to interrupt
            # us and end up with half a loaded config
            signal.alarm(0)

            log.info('Reloading config reload due to HUP')
            collector.load_config()
            log.info('Config reloaded')

        except Exception:
            log.exception('Collector failed!')
            break


def handler_process(handlers, metric_queue, log):
    proc = multiprocessing.current_process()
    if setproctitle:
        setproctitle('%s - %s' % (getproctitle(), proc.name))

    log.debug('Starting process %s', proc.name)

    while(True):
        metric = metric_queue.get(block=True, timeout=None)
        for handler in handlers:
            if metric is not None:
                handler._process(metric)
            else:
                handler._flush()
