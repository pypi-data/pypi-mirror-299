from __future__ import annotations

import collections
import collections.abc
import typing

from momotor.bundles.elements.base import Element
from momotor.bundles.utils.filters import FilterableTuple

T = typing.TypeVar('T', bound=Element)


def group_by_attr(items: collections.abc.Iterable[T], *attrs: str) \
        -> dict[str, FilterableTuple[T]] | dict[tuple[str, str], FilterableTuple[T]]:
    """ Group a list of elements by the value of one or more attributes

    :param items: list of elements to group
    :param attrs: name(s) of the attribute to group on
    :return: a dictionary of lists of elements
    """
    by_key: dict[typing.Any, typing.Deque[T]] = collections.defaultdict(collections.deque)

    if len(attrs) == 1:
        make_key = lambda i: getattr(i, attrs[0], None)  # noqa
    else:
        make_key = lambda i: tuple(getattr(i, attr, None) for attr in attrs)  # noqa

    for item in items:
        by_key[make_key(item)].append(item)

    return dict(
        (key, FilterableTuple(values))
        for key, values in by_key.items()
    )
