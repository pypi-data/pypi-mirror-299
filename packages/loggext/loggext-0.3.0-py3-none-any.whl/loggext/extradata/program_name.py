# -*- coding=utf-8 -*-
r"""

"""
from functools import cache
from ._cls import DataProvider


__all__ = ['ProgramNameField']



class ProgramNameField(DataProvider):
    r"""
    Selects a suitable program-name and adds it to the LogRecord as `programName`

    ```pycon

    >>> import logging
    >>> logging.getLogger().addFilter(ProgramNameField())

    ```
    """

    @cache
    def _program_name(self) -> str:
        import sys
        import os.path as p

        if sys.argv and sys.argv[0] != "-c":
            return p.basename(sys.argv[0])
        main = sys.modules.get('__main__')
        if main and hasattr(main, '__file__'):
            return p.basename(main.__file__)
        if sys.executable:
            return p.basename(sys.executable)
        return "python"

    def filter(self, record):
        record.programName = self._program_name
