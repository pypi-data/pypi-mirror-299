# -*- coding=utf-8 -*-
r"""

"""
import abc
import logging
import typing as t


__all__ = ['DataProvider', 'Combiner']


class DataProvider(logging.Filter):
    # noinspection PyMissingConstructor
    def __init__(self): ...

    def install(self, logger: logging.Logger = logging.root) -> None:
        r""" installs this field """
        for handler in logger.handlers:
            handler.addFilter(self)

    def filter(self, record: logging.LogRecord):
        self.add_data(record)
        return True

    @abc.abstractmethod
    def add_data(self, record: logging.LogRecord): ...

    def __rand__(self, other):
        return Combiner(self, other)

    def __and__(self, other):
        return Combiner(self, other)

    def __ror__(self, other):
        return Combiner(self, other)

    def __or__(self, other):
        return Combiner(self, other)



class Combiner(DataProvider):
    _filters: t.List[DataProvider]

    def __init__(self, *filters: DataProvider):
        super().__init__()
        self._filters = []
        for fltr in filters:
            if isinstance(fltr, Combiner):
                self._filters.extend(fltr._filters)
            else:
                self._filters.append(fltr)

    def filter(self, record):
        for fltr in self._filters:
            fltr.filter(record)
