# -*- coding=utf-8 -*-
r"""

"""


__all__ = ['MESSAGE', 'LEVEL_MESSAGE', 'MINIMAL', 'THREADED', 'PROCESSING', 'ASYNC', 'DEBUGGING']


MESSAGE = "{message}"
r""" minimalistic design with only the logged information """

LEVEL_MESSAGE = "{levelname:.3} | {message}"
r""" minimalistic design with the logged information and the severity """

MINIMAL = "{asctime} | {levelname:.3} | {name:>15} | {message}"
r""" this is a simple format which includes the time, level, logger-name and message """

THREADED = "{asctime} | {levelname:.3} | {thread:>3} | {message}"
r""" useful when doing multi-threading """

PROCESSING = "{asctime} | {levelname:.3} | {process:>5} | {message}"
r""" useful when doing multi-processing """

ASYNC = "{asctime} | {levelname:.3} | {taskName:>10} | {message}"
r""" useful when doing asnyc-code """

DEBUGGING = "{asctime} | {levelname:.3} | {name:>15} | {funcName:>12} | {lineno:>3} | {message}"
r""" format with all the information you need to find where the error comes from """
