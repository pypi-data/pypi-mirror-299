# -*- coding=utf-8 -*-
r"""

"""
from functools import cache
from ._cls import DataProvider


__all__ = ['ShortNameField']



class ShortNameField(DataProvider):
    r"""
    Shortens the name of the current logger and adds it to the LogRecord as `shortName`.
    This can heavily decrease the size of your log-files in exchange for losing some clarity.

    !!! example
        `project.custom.module` -> `p.c.module`

    !!! example
        ```pycon
        >>> import logging
        >>> ShortNameField().install()
        ```
    """

    @cache
    def _short_name(self, name: str) -> str:
        *head, tail = name.split('.')
        return '.'.join(tuple(p[0] for p in head) + (tail,))

    def add_data(self, record):
        print(f"Adding ShortNameField for {record.name}")
        record.shortName = self._short_name(record.name)
