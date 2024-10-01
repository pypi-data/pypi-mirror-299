# -*- coding=utf-8 -*-
r"""

"""


__all__ = ['MESSAGE', 'LEVEL_MESSAGE', 'MINIMAL', 'THREADED', 'PROCESSING', 'ASYNC', 'DEBUGGING']


MESSAGE = "{message}"
LEVEL_MESSAGE = "{levelname:.3} | {message}"
MINIMAL = "{asctime} | {levelname:.3} | {name:>15} | {message}"
THREADED = "{asctime} | {levelname:.3} | {thread:>3} | {message}"
PROCESSING = "{asctime} | {levelname:.3} | {process:>5} | {message}"
ASYNC = "{asctime} | {levelname:.3} | {taskName:>10} | {message}"
DEBUGGING = "{asctime} | {levelname:.3} | {name:>15} | {funcName:>12} | {lineno:>3} | {message}"
