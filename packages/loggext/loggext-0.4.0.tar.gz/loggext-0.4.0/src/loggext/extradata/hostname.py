# -*- coding=utf-8 -*-
r"""

"""
from functools import cache
from ._cls import DataProvider


__all__ = ['HostnameField']


class HostnameField(DataProvider):
    r"""
    Finds the hostname and adds it to the LogRecord as `hostname`

    !!! example
        ```pycon
        >>> import logging
        >>> HostnameField().install()
        ```
    """

    @cache
    def _hostname(self) -> str:
        import socket
        return socket.gethostname()

    def add_data(self, record):
        record.hostname = self._hostname()
