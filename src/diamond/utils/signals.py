# coding=utf-8

import signal


def signal_to_exception(signum, frame):
    """
    Called by the timeout alarm during the collector run time
    """
    if signum == signal.SIGALRM:
        raise SIGALRMException()
    if signum == signal.SIGUSR1:
        raise SIGUSR1Exception()
    if signum == signal.SIGUSR2:
        raise SIGUSR2Exception()
    raise SignalException(signum)


class SignalException(Exception):
    pass


class SIGALRMException(SignalException):
    pass


class SIGUSR1Exception(SignalException):
    pass


class SIGUSR2Exception(SignalException):
    pass
