from __future__ import annotations

import collections.abc
import typing

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

__all__ = ['KeyedTuple']


IT = typing.TypeVar('IT')

KeyType: TypeAlias = typing.Union[str, int, IT]
ItemsType: TypeAlias = typing.Union["KeyedTuple[IT]", collections.abc.Mapping[str, IT], collections.abc.Iterable[IT]]


class KeyedTuple(typing.Generic[IT], collections.abc.Sequence[IT], collections.abc.Mapping[KeyType, IT]):
    """ A tuple of objects with an indexable attribute that acts as both an immutable sequence and a mapping.
    Elements can be accessed by their numeric index or the key attribute.

    :param items: the initial items for the tuple. can be an iterable, mapping, another :py:class:`KeyedTuple`, or None
    :param key_attr: the attribute to index the items on. defaults to 'id'

    If `items` is another :py:class:`KeyedTuple`, `key_attr` must either be the same as the `key_attr` of `items`,
    or not provided.
    """
    __dict: dict | None = None
    __key_attr: str | None = None

    def __init__(self, items: ItemsType | None = None, *, key_attr: str | None = None):
        if key_attr is None:
            key_attr = items.__key_attr if isinstance(items, KeyedTuple) else 'id'

        self.__key_attr = key_attr
        self.__dict = dict()
        if items is not None:
            self.__extend(items)

    def __extend(self, items: ItemsType) -> None:
        """ Extend sequence by appending elements

        :param items: the items to add to the sequence. Can be a :py:class:`KeyedTuple`, sequence or mapping

        If `items` is a :py:class:`KeyedTuple`, it must be compatible, ie. have the same `key_attr` value
        """
        key_attr = self.__key_attr
        if isinstance(items, KeyedTuple) and items.__key_attr != key_attr:
            raise ValueError(f"items.key_attr '{items.__key_attr}' is not '{key_attr}'")

        # Validate all items before adding
        def iter_items():
            if isinstance(items, KeyedTuple):
                # a KeyedList validated all key-value pairs already
                yield from items.items()

            elif hasattr(items, 'items'):
                # Mapping -- need to validate the keys with the items
                for k, v in items.items():
                    try:
                        iik = getattr(v, key_attr)
                    except AttributeError:
                        raise ValueError(f"item {v} does not have key attribute '{key_attr}'")

                    if iik != k:
                        raise KeyError(f"key '{k}' does not match the item {v} key '{iik}'")

                    yield k, v

            else:
                # Iterable -- generate items
                for v in items:
                    try:
                        yield getattr(v, key_attr), v
                    except AttributeError:
                        raise ValueError(f"item {v} does not have key attribute '{key_attr}'")

        for key, value in iter_items():
            if key in self.__dict:
                raise ValueError(f"item with key '{key}' already exists")

            self.__dict[key] = value

    def __get_key(self, key_or_index: KeyType) -> str:
        if isinstance(key_or_index, slice):
            raise IndexError("slicing of a KeyedTuple is not supported")

        if hasattr(key_or_index, self.__key_attr):
            key = str(getattr(key_or_index, self.__key_attr))
            if key not in self.__dict or self.__dict[key] != key_or_index:
                raise KeyError(key_or_index)

            return key

        if not isinstance(key_or_index, (str, int)):
            raise ValueError(f"access items by index (as int) or id (as str), not {type(key_or_index)}")

        if isinstance(key_or_index, int):
            return list(self.__dict.keys())[key_or_index]

        return key_or_index

    def __getitem__(self, key_or_index: KeyType) -> IT:
        return self.__dict[self.__get_key(key_or_index)]

    def get(self, key_or_index: KeyType, default=None):
        """ Get an item from the sequence by index, key or item

        :param key_or_index: index, key or item
        :param default: the value to return if item does not exist
        :return: the item or `default`
        """
        try:
            key = self.__get_key(key_or_index)
        except KeyError:
            return default
        else:
            return self.__dict.get(key, default)

    def keys(self) -> collections.abc.KeysView[str]:
        """ A set-like object providing a view on the keys """
        return self.__dict.keys()

    def values(self) -> collections.abc.ValuesView[IT]:
        """ A set-like object providing a view on the values """
        return self.__dict.values()

    def items(self) -> collections.abc.ItemsView[str, IT]:
        """ A set-like object providing a view on the items """
        return self.__dict.items()

    def __iter__(self):
        for item in self.values():
            yield item

    def copy(self) -> Self:
        """ Create a shallow copy """
        return self.__class__(self)

    __copy__ = copy

    def __contains__(self, key_or_index: KeyType) -> bool:
        if isinstance(key_or_index, int):
            return 0 <= key_or_index < len(self.__dict)

        try:
            key = getattr(key_or_index, self.__key_attr)
        except AttributeError:
            return key_or_index in self.__dict
        else:
            return self.__dict.get(key) == key_or_index

    def __len__(self) -> int:
        return len(self.__dict)

    def __eq__(self, other) -> bool:
        if isinstance(other, KeyedTuple):
            return other.__key_attr == self.__key_attr and other.__dict == self.__dict
        elif isinstance(other, list):
            return other == list(self)
        else:
            return other == self.__dict

    def count(self, value: IT) -> int:
        """ Return number of occurrences of value

        :param value: the item to count
        :return: the number of occurrences
        """
        try:
            key = getattr(value, self.__key_attr)
        except AttributeError:
            return 0
        else:
            return 1 if self.__dict.get(key) == value else 0

    def index(self, value: IT, start=0, stop=None) -> int:
        """ Return first index of value

        :param value: the item to find
        :param start: the index to start searching from
        :param stop: the index to stop searching at
        :return: the index of the first occurrence
        """
        if start is not None and start < 0:
            start = max(len(self) + start, 0)
        if stop is not None and stop < 0:
            stop += len(self)

        i, it = 0, self.__iter__()
        while stop is None or i < stop:
            try:
                v = next(it)
            except StopIteration:
                break

            if i >= start and (v is value or v == value):
                return i

            i += 1

        raise ValueError
