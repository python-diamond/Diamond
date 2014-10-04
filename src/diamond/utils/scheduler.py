# coding=utf-8

import time
import multiprocessing
import sys
import signal

try:
    from setproctitle import getproctitle, setproctitle
except ImportError:
    setproctitle = None


class CollectorTimeoutException(Exception):
    pass


def collector_timeout(signum, frame):
    """
    Called by the timeout alarm during the collector run time
    """
    raise CollectorTimeoutException()


def collector_process(collector, metric_queue, log):
    """
    """
    proc = multiprocessing.current_process()
    if setproctitle:
        setproctitle('%s - %s' % (getproctitle(), proc.name))

    signal.signal(signal.SIGALRM, collector_timeout)

    interval = float(collector.config['interval'])
    max_time = int(interval * 0.9)

    log.debug(
        'Starting %s. Interval: %s seconds. Max collection time: %s seconds.',
        proc.name,
        interval,
        max_time
        )

    # Validate the interval
    if interval <= 0:
        log.critical('interval of %s is not valid!', interval)
        sys.exit(1)

    # When should we wake up again?
    next_collection = time.time() + interval

    while(True):
        try:
            try:
                # Ensure collector run times fit into the collection window
                signal.alarm(max_time)

                # Collect!
                collector._run()

                # Success! Disable the alarm
                signal.alarm(0)

            except CollectorTimeoutException, e:
                log.critical('Took too long to run! Killed!')

            # TODO: Catch other signals and log correctly

            # Any exception? Kill the thread
            except Exception, e:
                log.error(e)
                break
        finally:
            # If the collector took too long to run, skip ahead to the next
            # valid collection interval

            while next_collection < time.time():
                next_collection += interval

            # Sleep until next collection time

            time.sleep(next_collection - time.time())


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
