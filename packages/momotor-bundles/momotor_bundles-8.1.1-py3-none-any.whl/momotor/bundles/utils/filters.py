from __future__ import annotations

import abc
import collections.abc
import fnmatch
import os
import re
import typing

from .text import smart_split, unescape_string_literal
from .rglob import rglobcase

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

__all__ = ['F', 'Not', 'Any', 'All', 'FilterableList', 'FilterableTuple']


TV = typing.TypeVar('TV')
TC = typing.TypeVar('TC')
TS = typing.TypeVar('TS', bound=collections.abc.Iterable)
TO = typing.TypeVar('TO', bound=object)


Str_or_PathLike: TypeAlias = typing.Union[str, os.PathLike]


def pathlike_to_str(c: TC) -> str | TC:
    if hasattr(c, 'as_posix'):
        return c.as_posix()

    try:
        return os.fspath(c)
    except TypeError:
        return c


class _Filter(abc.ABC):
    """ Base for the filter operators """
    OP: typing.ClassVar[str]

    def __call__(self, obj: object) -> bool:
        raise NotImplementedError


class _All(_Filter):
    """ Default combiner for the :py:class:`F` base filter operator, do not use directly """
    def __init__(self, *fs: _Filter):
        self._fs = fs

    def __call__(self, obj: object) -> bool:
        return all(f(obj) for f in self._fs)


class _Any(_Filter):
    """ Combiner for the :py:class:`Any` filter, do not use directly """
    def __init__(self, *fs: _Filter):
        self._fs = fs

    def __call__(self, obj: object) -> bool:
        return any(f(obj) for f in self._fs)


class _Always(_Filter):
    """ Filter helper that always matches. Used for :py:class:`All` with no arguments """
    def __call__(self, obj: object) -> bool:
        return True

    def __str__(self):
        return 'Always'


class _Never(_Filter):
    """ Filter helper that never matches. Used for :py:class:`All` with no arguments """
    def __call__(self, obj: object) -> bool:
        return False

    def __str__(self):
        return 'Never'


class _FilterOperatorProtocol(typing.Protocol[TC]):
    def _cast(self, c: TC) -> TC:
        ...

    def _check(self, c: TC) -> bool:
        ...


class _FilterOperator(_Filter, typing.Generic[TV, TC], abc.ABC):
    f: typing.Final[str]
    v: typing.Final[TV]

    def __init__(self, field: str, value: TV):
        self.f = field
        self.v = value

    def __call__(self, obj: object) -> bool:
        try:
            c = getattr(obj, self.f)
            c = self._cast(c)
            return self._check(c)
        except (TypeError, AttributeError):
            return False

    # noinspection PyMethodMayBeStatic
    def _cast(self, c: TC) -> TC:
        return pathlike_to_str(c)

    def _check(self, c: TC) -> bool:
        raise NotImplementedError

    def __str__(self):
        return f'{self.f}__{self.OP}={self.v!r}'


class _IFilterOperator(_FilterOperator[TV, TC], typing.Generic[TV, TC], abc.ABC):
    def __init__(self, field: str, value: TV):
        super().__init__(field, self._cast(value))

    def _cast(self, c: TC) -> TC:
        c = pathlike_to_str(c)

        try:
            if isinstance(c, str):
                return c.lower()
            else:
                return type(c)(i.lower() for i in c)
        except (AttributeError, TypeError):
            raise TypeError(f"Expected a string or sequence of strings, got {type(c)}")


class Equal(_FilterOperator[typing.Any, typing.Any]):
    """ Equality filter (case-sensitive).
    """
    OP = 'eq'

    def _check(self, c: typing.Any) -> bool:
        return self.v == c

    def __str__(self):
        return f'{self.f}={self.v!r}'


class IEqual(_IFilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Equality filter (case-insensitive)
    """
    OP = 'ieq'

    def _check(self, c: typing.Any) -> bool:
        return self.v == c


class NotEqual(_FilterOperator[typing.Any, typing.Any]):
    """ Non-equality filter (case-sensitive)
    """
    OP = 'ne'

    def _check(self, c: typing.Any) -> bool:
        return self.v != c


class INotEqual(_IFilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Non-equality filter (case-insensitive)
    """
    OP = 'ine'

    def _check(self, c: Str_or_PathLike) -> bool:
        return self.v != c


class Contains(_FilterOperator[typing.Any, typing.Union[Str_or_PathLike, collections.abc.Collection[typing.Any]]]):
    """ Contains filter (case-sensitive)
    """
    OP = 'contains'

    def _check(self, c: Str_or_PathLike | collections.abc.Collection[typing.Any]) -> bool:
        return self.v in c


class IContains(_IFilterOperator[Str_or_PathLike, typing.Union[Str_or_PathLike, collections.abc.Collection[Str_or_PathLike]]]):
    """ Contains filter (case-insensitive)
    """
    OP = 'icontains'

    def _cast(self, c: Str_or_PathLike | collections.abc.Collection[Str_or_PathLike]) \
            -> Str_or_PathLike | collections.abc.Collection[Str_or_PathLike]:
        c = pathlike_to_str(c)

        if isinstance(c, str):
            return c.lower()
        else:
            return {pathlike_to_str(i) for i in c}

    def _check(self, c: Str_or_PathLike | collections.abc.Collection[Str_or_PathLike]) -> bool:
        return self.v in c


class Contained(_FilterOperator[collections.abc.Collection[typing.Hashable], typing.Any]):
    """ Contained filter (case-sensitive)
    """
    OP = 'in'

    def __init__(self, field: str, value: collections.abc.Collection[typing.Hashable]):
        super().__init__(field, frozenset(value))

    def _check(self, c: TC) -> bool:
        return c in self.v


class IContained(_IFilterOperator[collections.abc.Collection[str], str]):
    """ Contained filter (case-insensitive)
    """
    OP = 'iin'

    def __init__(self, field: str, value: collections.abc.Collection[str]):
        super().__init__(field, frozenset(i.lower() for i in value))

    def _check(self, c: TC) -> bool:
        return c in self.v


class StartsWith(_FilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Starts-with filter (case-sensitive)
    """
    OP = 'startswith'

    def _check(self, c: str) -> bool:
        return c.startswith(self.v)


class IStartsWith(_IFilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Starts-with filter (case-insensitive)
    """
    OP = 'istartswith'

    def _check(self, c: str) -> bool:
        return c.startswith(self.v)


class EndsWith(_FilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Ends-with filter (case-sensitive)
    """
    OP = 'endswith'

    def _check(self, c: str) -> bool:
        return c.endswith(self.v)


class IEndsWith(_IFilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Ends-with filter (case-insensitive)
    """
    OP = 'iendswith'

    def _check(self, c: str) -> bool:
        return c.endswith(self.v)


class _Glob:
    FN: typing.ClassVar[collections.abc.Callable[[str, str], bool]]
    pattern: tuple[str, ...]

    def __init__(self: _FilterOperatorProtocol, field: Str_or_PathLike, value: Str_or_PathLike):
        super().__init__(field, value)
        self.pattern = tuple(
            unescape_string_literal(self._cast(p))
            for p in smart_split(value)
        )

    def _check(self, c: str) -> bool:
        for pattern in self.pattern:
            if self.FN(c, pattern):
                return True

        return False


class Glob(_Glob, _FilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Glob filter (case-sensitive)
    """
    FN = staticmethod(fnmatch.fnmatchcase)
    OP = 'glob'


class IGlob(_Glob, _IFilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ Glob filter (case-insensitive)
    """
    FN = staticmethod(fnmatch.fnmatchcase)
    OP = 'iglob'


class RGlob(_Glob, _FilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ RGlob filter (case-sensitive)
    """
    FN = staticmethod(rglobcase)
    OP = 'rglob'


class IRGlob(_Glob, _IFilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ IRGlob filter (case-insensitive)
    """
    FN = staticmethod(rglobcase)
    OP = 'irglob'


class RegEx(_FilterOperator[Str_or_PathLike, Str_or_PathLike]):
    """ RegEx filter (case-sensitive)
    """
    OP = 're'

    re: re.Pattern

    def __init__(self, field: str, regex: str, flags: int = 0):
        super().__init__(field, regex)
        self.re = re.compile(regex, flags)

    def _check(self, c: str) -> bool:
        return self.re.search(c) is not None


class IRegEx(RegEx):
    """ RegEx filter (case-insensitive)
    """
    OP = 'ire'

    def __init__(self, field: Str_or_PathLike, regex: Str_or_PathLike, flags: int = 0):
        super().__init__(field, regex, flags | re.I)


OPER_MAP: dict[str | None, type[_FilterOperator]] = {
    None: Equal,
    'is': Equal,
    'eq': Equal,
    'ieq': IEqual,
    'iis': IEqual,

    'ne': NotEqual,
    'ine': INotEqual,

    'contains': Contains,
    'icontains': IContains,

    'in': Contained,
    'iin': IContained,

    'startswith': StartsWith,
    'istartswith': IStartsWith,

    'endswith': EndsWith,
    'iendswith': IEndsWith,

    'glob': Glob,
    'iglob': IGlob,
    'rglob': RGlob,
    'irglob': IRGlob,

    're': RegEx,
    'ire': IRegEx,
}


class F(_Filter):
    """ Filter operator

    Base for the other filter operators. Can be used to prevent multiple keywords SyntaxErrors in Python,
    see the :ref:`F object documentation <f object>` for an example.
    """
    COMBINER: typing.ClassVar[_Filter] = _All
    NONE: typing.ClassVar[_Filter] = _Always
    OP = 'F'

    filters: typing.Final[list[_Filter]]
    filter: typing.Final[_Filter]

    def __init__(self, *filters: _Filter, **filter_args):
        filters: list[_Filter] = list(filters)

        for expression, value in filter_args.items():
            if '__' in expression:
                field, oper = expression.rsplit('__', 1)
            else:
                field, oper = expression, None

            fc = OPER_MAP.get(oper)
            if fc is None:
                raise KeyError('Invalid filter operator %r' % oper)

            filters.append(fc(field, value))

        self.filters = filters

        if len(filters) > 1:
            self.filter = self.COMBINER(*filters)
        elif filters:
            self.filter = filters[0]
        else:
            self.filter = self.NONE()

    def __call__(self, obj: object) -> bool:
        return self.filter(obj)

    def __str__(self):
        return self.OP + '(' + ', '.join(str(f) for f in self.filters) + ')'


class Not(F):
    """ "Not" filter operator

    Any item not matching all the lookup arguments will match this filter,
    see the :ref:`Not object documentation <not object>` for an example.
    """
    OP = 'Not'

    def __call__(self, obj: object) -> bool:
        return not self.filter(obj)


class _InvertableF(F):
    def __invert__(self):
        return Not(self)


class All(_InvertableF):
    """ "All" filter operator

    All the lookups in the argument list will need to match for an item to match this filter,
    see the :ref:`All object documentation <all object>` for an example.

    (alias of :py:class:`F`)
    """
    OP = 'All'


class Any(_InvertableF):
    """ "Any" filter operator

    Any of the lookups in the argument list can match for an item to match this filter,
    see the :ref:`Any object documentation <any object>` for an example.
    """
    OP = 'Any'
    COMBINER: typing.ClassVar[_Filter] = _Any
    NONE: typing.ClassVar[_Filter] = _Never


class FilterMixin(typing.Generic[TS, TO], abc.ABC):
    """ Mixin to extend a sequence of objects with filtering functionality
    """
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def filter(self: TS, *args, **kwargs) -> TS:
        """ Returns a filtered version of self that only includes elements that match the provided query

        See :ref:`filtering and excluding`
        """
        return self.__class__(self.ifilter(*args, **kwargs))

    def exclude(self: TS, *args, **kwargs) -> TS:
        """ Returns a filtered version of self that only includes elements that do not match the provided query

        See :ref:`filtering and excluding`
        """
        return self.__class__(self.iexclude(*args, **kwargs))

    def ifilter(self: TS, *args, **kwargs) -> collections.abc.Iterable[TO]:
        """ Iterator version of :py:meth:`filter`
        """
        return filter(F(*args, **kwargs), self)

    def iexclude(self: TS, *args, **kwargs) -> collections.abc.Iterable[TO]:
        """ Iterator version of :py:meth:`exclude`
        """
        return filter(Not(*args, **kwargs), self)

    def filter_with(self: TS, func: collections.abc.Callable[[TO], bool]) -> TS:
        """ Filter the items using a callable function

        :param func: A callable receiving an item and returning a boolean
        """
        return self.__class__(filter(func, self))


class FilterableList(list[TO], FilterMixin[list[TO], TO], typing.Generic[TO]):
    """ A :py:class:`list` with additional functions to filter the objects in the list

    See :ref:`filters` section in the documentation
    """
    pass


class FilterableTuple(tuple[TO, ...], FilterMixin[tuple[TO, ...], TO], typing.Generic[TO]):
    """ A :py:class:`tuple` with additional functions to filter the objects in the tuple

    See :ref:`filters` section in the documentation
    """
    pass
