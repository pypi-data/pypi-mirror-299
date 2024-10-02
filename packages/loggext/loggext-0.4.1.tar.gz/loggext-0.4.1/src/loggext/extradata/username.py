# -*- coding=utf-8 -*-
r"""

"""
from functools import cache
from ._cls import DataProvider


__all__ = ['UsernameField']


class UsernameField(DataProvider):
    r"""
    Finds the username and adds it to the LogRecord as `username`

    !!! example
        ```pycon
        >>> import logging
        >>> UsernameField().install()
        ```

    !!! info
        On UNIX systems this uses the :mod:`pwd` module which means ``root`` will
        be reported when :man:`sudo` is used (as it should). If this fails (for
        example on Windows) then :func:`getpass.getuser()` is used as a fallback.
    """

    @cache
    def _username(self) -> str:
        try:
            import pwd, os
            uid = os.getuid()
            return pwd.getpwuid(uid).pw_name
        except (ImportError, KeyError):
            import getpass
            return getpass.getuser()

    def add_data(self, record):
        record.username = self._username()
