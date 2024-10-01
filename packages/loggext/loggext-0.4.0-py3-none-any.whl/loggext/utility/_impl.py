# -*- coding=utf-8 -*-
r"""

"""
import os
import sys
import logging


__all__ = [
    'logging_is_configured', 'is_running_as_service', 'is_running_in_shell',
    'no_thread_info', 'no_process_info', 'no_multiprocess_info',
]


def logging_is_configured() -> bool:
    r"""
    :return: if :func:`logging.basicConfig` was already called. (if the root-logger has handlers)
    """
    return len(logging.root.handlers) > 0


def is_running_as_service() -> bool:
    r"""
    :return: if the current script is running as a service (or not)
    """
    return os.getenv('TERM') is None and os.isatty(sys.stdin.fileno())


def is_running_in_shell() -> bool:
    r"""
    :return: if the current script is running in a shell (or not)
    """
    return os.isatty(sys.stdin.fileno())


def no_thread_info():
    r""" disabled threading-information in the LogRecord for slight performance boost """
    logging.logThreads = False


def no_process_info():
    r""" disabled process-information in the LogRecord for slight performance boost """
    logging.logProcess = False


def no_multiprocess_info():
    r""" disabled multiprocessing-information in the LogRecord for slight performance boost """
    logging.logMultiprocessing = False
