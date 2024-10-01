from __future__ import annotations

import collections.abc
import copy
import typing

import momotor.bundles
from momotor.bundles.binding import ResourceComplexType, ResourcesComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentBasicElement
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.assertion import assert_elements_bundle
from momotor.bundles.utils.filters import FilterableTuple
from momotor.bundles.utils.grouping import group_by_attr
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['Resource', 'ResourcesType', 'ResourcesMixin']


class Resource(ContentBasicElement[ResourceComplexType, ResourcesComplexType]):
    # noinspection PyUnresolvedReferences
    """ A Resource element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.ResourceComplexType`
    """
    @staticmethod
    def get_node_type() -> type[ResourceComplexType]:
        return ResourceComplexType

    @staticmethod
    def _get_parent_type() -> type[ResourcesComplexType]:
        return ResourcesComplexType

    def create(self, *, name: str, value: str | None = None) -> Self:
        self._create_content(name=name, value=value)
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", *, name: str | None = None) -> "Resource":
        """ Recreate this :py:class:`Resource` in a target bundle, optionally changing the `name`.
        All other attributes are copied unchanged.

        :param target_bundle: The target bundle
        :param name: New name for the option
        :return: The recreated :py:class:`Resource`
        """
        return Resource(target_bundle).create(
            name=name or self.name,
            value=self.value
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ResourceComplexType,
                          direct_parent: ResourcesComplexType,
                          ref_parent: ResourcesComplexType | None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(direct_parent)
        self._check_parent_type(ref_parent, True)

        self._create_content_from_node(node, direct_parent, ref_parent, args=args)

        return self

    def _construct_node(self, *, args: BundleConstructionArguments) -> ResourceComplexType:
        return (
            self._construct_content(
                ResourceComplexType(),
                args=args
            )
        )


if Resource.__doc__ and Element.__doc__:
    Resource.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


ResourcesType: TypeAlias = FilterableTuple[Resource]


# noinspection PyProtectedMember
class ResourcesMixin:
    __unset: typing.ClassVar = object()
    _resources: ResourcesType = __unset
    _resources_by_name: dict[str, ResourcesType] | None = None

    @typing.final
    @property
    def resources(self) -> ResourcesType:
        """ `resources` attribute """
        assert self._resources is not self.__unset, "Uninitialized attribute `resources`"
        return self._resources

    @resources.setter
    def resources(self: ElementMixinProtocol | Self, resources: collections.abc.Iterable[Resource] | None):
        assert self._resources is self.__unset, "Immutable attribute `resources`"
        if resources is not None:
            self._resources = assert_elements_bundle(FilterableTuple(resources), self.bundle)
        else:
            self._resources = ResourcesType()

        self._resources_updated()

    def _resources_updated(self):
        self._resources_by_name = None

    def _collect_resources(self: ElementMixinProtocol, parent: object, *,
                           args: BundleFactoryArguments) -> collections.abc.Generator[Resource, None, None]:
        resources_node: ResourcesComplexType | None = None
        for tag_name, node in get_nested_complex_nodes(parent, 'resources', 'resource'):
            if tag_name == 'resources':
                resources_node = typing.cast(ResourcesComplexType, node)
            else:
                resource_node = typing.cast(ResourceComplexType, node)
                yield Resource(self.bundle)._create_from_node(resource_node, resources_node, None, args=args)

    # noinspection PyMethodMayBeStatic
    def _construct_resources_nodes(self, *, args: BundleConstructionArguments) \
            -> collections.abc.Generator[ResourcesComplexType, None, None]:
        resources = self.resources
        if resources:
            yield ResourcesComplexType(resource=[
                resource._construct_node(args=args)
                for resource in resources
            ])

    def _get_resources(self) -> dict[str, ResourcesType]:
        if self._resources_by_name is None:
            self._resources_by_name = group_by_attr(self.resources, 'name')

        return self._resources_by_name

    def get_resources(self) -> dict[str, ResourcesType]:
        """ Get the resources as a dictionary name -> Resource """
        return copy.copy(self._get_resources())
