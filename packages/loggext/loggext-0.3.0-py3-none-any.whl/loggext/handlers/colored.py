# -*- coding=utf-8 -*-
r"""

"""
import sys
import logging
import typing as t
from ..utility import StandardColors


__all__ = ['ColoredConsoleHandler', 'LevelColorConsoleHandler']


ENDCOLOR = "\033[0m"
COLOR_MAP: t.Dict[int, str] = {
    logging.DEBUG: StandardColors.BRIGHT_BLACK.escape_code_fg,
    logging.INFO: StandardColors.BRIGHT_BLUE.escape_code_fg,
    logging.WARN: StandardColors.BRIGHT_YELLOW.escape_code_fg,
    logging.ERROR: StandardColors.BRIGHT_RED.escape_code_fg,
    logging.CRITICAL: StandardColors.BRIGHT_MAGENTA.escape_code_fg,
}
r"""This can be adjusted/extended for custom coloring"""


class ColoredConsoleHandler(logging.StreamHandler):
    r"""
    same as `StreamHandler` but with colored output based on the logging-level of each message
    """
    STDOUT = sys.stdout
    STDERR = sys.stderr

    def format(self, record):
        colorcode = COLOR_MAP.get(record.levelno)
        msg = super().format(record)
        if colorcode is None:
            return msg
        return f"{colorcode}{msg}{ENDCOLOR}"


class LevelColorConsoleHandler(logging.StreamHandler):
    r"""
    similar to `ColoredConsoleHandler` but colors only the levelname
    """
    STDOUT = sys.stdout
    STDERR = sys.stderr

    def emit(self, record):
        colorcode = COLOR_MAP.get(record.levelno)
        if colorcode is not None:
            record = logging.makeLogRecord(record.__dict__)  # copy to not modify for other logging-handlers
            record.levelname = f"{colorcode}{record.levelname}{ENDCOLOR}"
        super().emit(record)
