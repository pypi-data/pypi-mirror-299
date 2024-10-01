# -*- coding=utf-8 -*-
r"""

"""
import typing as t


__all__ = ['LoggingFormatBuilder']


class LoggingFormatBuilder:
    r"""
    ```pycon

    >>> logging_format: str = LoggingFormatBuilder(separator=" | ") \
    ...     .add_asctime() \
    ...     .add_levelname(".3") \
    ...     .add_module("<10") \
    ...     .add_lineno(">3") \
    ...     .add_message() \
    ...     .build()

    ```
    """

    _separator: str
    _parts: t.List[str]

    def __init__(self, *, separator: str = ":"):
        self._separator = separator
        self._parts = []

    def build(self) -> str:
        r""" create the final logging-format """
        return self._separator.join(self._parts)

    def add_field(self, name: str, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" adds a custom field """
        if fmt is None:
            self._parts.append(f"{{{name}}}")
        else:
            self._parts.append(f"{{{name}:{fmt}}}")
        return self

    def add_literal(self, literal: str) -> 'LoggingFormatBuilder':
        r""" adds a literal string as given """
        self._parts.append(literal)
        return self

    def add_asctime(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r"""
        Human-readable time when the LogRecord was created.
        By default, this is of the form ‘2003-07-08 16:49:45,896’
        (the numbers after the comma are millisecond portion of the time).
        """
        return self.add_field('asctime', fmt)

    def add_created(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Time when the LogRecord was created (as returned by time.time()). """
        return self.add_field('created', fmt)

    def add_filename(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Filename portion of pathname. """
        return self.add_field('filename', fmt)

    def add_funcname(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Name of function containing the logging call. """
        return self.add_field('funcName', fmt)

    def add_levelname(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL). """
        return self.add_field('levelname', fmt)

    def add_levelno(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL). """
        return self.add_field('levelno', fmt)

    def add_lineno(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Source line number where the logging call was issued (if available). """
        return self.add_field('lineno', fmt)

    def add_message(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" The logged message, computed as msg % args. This is set when Formatter.format() is invoked. """
        return self.add_field('message', fmt)

    def add_module(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Module (name portion of filename). """
        return self.add_field('module', fmt)

    def add_msecs(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Millisecond portion of the time when the LogRecord was created. """
        return self.add_field('msecs', fmt)

    def add_name(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Name of the logger used to log the call. """
        return self.add_field('name', fmt)

    def add_pathname(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Full pathname of the source file where the logging call was issued (if available). """
        return self.add_field('pathname', fmt)

    def add_process(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Process ID (if available) """
        return self.add_field('process', fmt)

    def add_processname(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Process name (if available) """
        return self.add_field('processName', fmt)

    def add_relativecreated(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded."""
        return self.add_field('relativeCreated', fmt)

    def add_thread(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Thread ID (if available) """
        return self.add_field('thread', fmt)

    def add_threadname(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" Thread name (if available) """
        return self.add_field('threadName', fmt)

    def add_taskname(self, fmt: str = None) -> 'LoggingFormatBuilder':
        r""" asyncio.Task name (if available) """
        return self.add_field('taskName', fmt)
