from __future__ import annotations

import collections.abc
import typing
from dataclasses import dataclass, field
from pathlib import PurePosixPath, PurePath

import momotor.bundles
from momotor.bundles.binding import CheckletComplexType, CheckletsComplexType, LinkComplexType
from momotor.bundles.elements.base import NestedElement, Element
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.resources import Resource, ResourcesMixin
from momotor.bundles.mixins.attachments import SrcAttachmentMixin, AttachmentSrc
from momotor.bundles.mixins.name import NameStrMixin
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.assertion import assert_sequence_instanceof
from momotor.bundles.utils.filters import FilterableTuple

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['Checklet', 'CheckletMixin']

CT = typing.TypeVar('CT', bound=object)


@dataclass(frozen=True)
class Link:
    """ An immutable `dataclass` for a reference to a link
    """
    #: The src of the link
    src: str = field()


@dataclass(frozen=True)
class PackageVersion:
    """ An immutable `dataclass` for a reference to a package with version
    """
    #: The name of the package
    name: str = field()
    #: The version qualifier for the package
    version: str = field()


class Repository(SrcAttachmentMixin, Element[CheckletComplexType.Repository]):
    __unset: typing.ClassVar = object()
    _type: str = __unset
    _revision: str | None = __unset

    @typing.final
    @property
    def type_(self) -> str:
        assert self._type is not self.__unset, "Uninitialized attribute `type`"
        return self._type

    @type_.setter
    def type_(self, type_: str):
        assert self._type is self.__unset, "Immutable attribute `type`"
        assert isinstance(type_, str), "Invalid type for attribute `type`"
        self._type = type_

    @typing.final
    @property
    def revision(self) -> str:
        assert self._revision is not self.__unset, "Uninitialized attribute `revision`"
        return self._revision

    @revision.setter
    def revision(self, revision: str | None):
        assert self._revision is self.__unset, "Immutable attribute `revision`"
        assert revision is None or isinstance(revision, str), "Invalid type for attribute `revision`"
        self._revision = revision

    def create(self,
               src: PurePath | AttachmentSrc | None,
               type_: str,
               revision: str | None = None) -> Self:

        # If `src` is an AttachmentSrc, it refers to an attachment of another bundle

        self.src = src
        self.type_ = type_
        self.revision = revision

        return self

    # noinspection PyMethodOverriding
    def recreate(self, target_bundle: "momotor.bundles.Bundle") -> "Repository":
        """ Recreate this :py:class:`Repository` in a target bundle.

        The target bundle will *link* to the same attachment in `src`, the attachment will not be copied.
        No attributes can be changed.

        :param target_bundle: The target bundle
        :return: The recreated :py:class:`Repository`
        """
        return Repository(target_bundle).create(
            src=self._src,
            type_=self.type_,
            revision=self.revision
        )

    def _create_from_node(self, node: CheckletComplexType.Repository, *, args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)

        return self.create(
            src=AttachmentSrc(PurePosixPath(node.src), self.bundle, validate=args.validate_signature),
            type_=node.type_value,
            revision=node.revision
        )

    def _construct_node(self, *, args: BundleConstructionArguments) -> CT:
        return CheckletComplexType.Repository(
            src=str(self._export_path(PurePosixPath('repository', self.src.name))),
            type_value=self.type_,
            revision=self.revision
        )

    @staticmethod
    def get_node_type() -> type[CT]:
        return CheckletComplexType.Repository


class Checklet(
    NestedElement[CheckletComplexType, CheckletsComplexType],
    NameStrMixin,
    ResourcesMixin,
):
    """ A Checklet element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.CheckletComplexType`
    """
    _OLD_DEFAULT_ENTRYPOINT: typing.ClassVar[str] = 'momotor.checklet'

    __unset: typing.ClassVar = object()

    _extras: FilterableTuple[str] | None = __unset
    _version: str | None = __unset
    _entrypoint: str | None = __unset
    _repository: Repository | None = __unset
    _link: Link | None = __unset
    # _indices: tuple[Link, ...] = __unset
    _package_versions: FilterableTuple[PackageVersion] | None = __unset

    @typing.final
    @property
    def extras(self) -> FilterableTuple[str] | None:
        """ `extras` attribute: The Python package extras (eg. "requests") """
        assert self._extras is not self.__unset, "Uninitialized attribute `extras`"
        return self._extras

    @extras.setter
    def extras(self, extras: collections.abc.Iterable[str] | None):
        assert self._extras is self.__unset, "Immutable attribute `extras`"
        if extras is not None:
            assert isinstance(extras, collections.abc.Iterable), "Invalid type for attribute `extras`"
            self._extras = assert_sequence_instanceof(FilterableTuple(extras), str)
        else:
            self._extras = None

    @typing.final
    @property
    def version(self) -> str | None:
        """ `version` attribute: A :pep:`440` Python package version specifier (eg. ">=1.0") """
        assert self._version is not self.__unset, "Uninitialized attribute `version`"
        return self._version

    @version.setter
    def version(self, version: str | None):
        assert self._version is self.__unset, "Immutable attribute `version`"
        assert version is None or isinstance(version, str), "Invalid type for attribute `version`"
        self._version = version

    @typing.final
    @property
    def entrypoint(self) -> typing.Optional[str]:
        """ `entrypoint` attribute: Override the default package entrypoint """
        assert self._entrypoint is not self.__unset, "Uninitialized attribute `entrypoint`"
        return self._entrypoint

    @entrypoint.setter
    def entrypoint(self, entrypoint: str | None):
        assert self._entrypoint is self.__unset, "Immutable attribute `entrypoint`"
        assert entrypoint is None or isinstance(entrypoint, str), "Invalid type for attribute `entrypoint`"
        self._entrypoint = entrypoint

    @typing.final
    @property
    def repository(self) -> Repository | None:
        """ `repository` attribute: where to retrieve the package from """
        assert self._repository is not self.__unset, "Uninitialized attribute `repository`"
        return self._repository

    @repository.setter
    def repository(self, repository: Repository | None):
        assert self._repository is self.__unset, "Immutable attribute `repository`"
        assert repository is None or isinstance(repository, Repository), "Invalid type for attribute `repository`"
        self._repository = repository

    @typing.final
    @property
    def link(self) -> Link | None:
        """ `link` attribute: (unused, untested) """
        assert self._link is not self.__unset, "Uninitialized attribute `link`"
        return self._link

    @link.setter
    def link(self, link: Link | None):
        assert self._link is self.__unset, "Immutable attribute `link`"
        assert link is None or isinstance(link, Link), "Invalid type for attribute `link`"
        self._link = link

    @typing.final
    @property
    def indices(self) -> list[Link | None]:
        """ `indices` attribute: (unused, untested) """
        return None

    @indices.setter
    def indices(self, indices: collections.abc.Iterable[Link] | None):
        if indices is not None:
            raise NotImplementedError

    @typing.final
    @property
    def package_versions(self) -> FilterableTuple[PackageVersion] | None:
        """ `package_versions` attribute: (unused, untested) """
        assert self._package_versions is not self.__unset, "Uninitialized attribute `package_versions`"
        return self._package_versions

    @package_versions.setter
    def package_versions(self, package_versions: collections.abc.Iterable[PackageVersion] | None):
        assert self._package_versions is self.__unset, "Immutable attribute `package_versions`"
        if package_versions is not None:
            assert isinstance(package_versions, collections.abc.Iterable), \
                "Invalid type for attribute `package_versions`"
            self._package_versions = assert_sequence_instanceof(FilterableTuple(package_versions), PackageVersion)
        else:
            self._package_versions = None

    def get_dist_name(self) -> str:
        """ Return a distribution selector (ie. name, extras and version in a single string)

        eg: "name[extra1,extra2]==1.0"

        """
        name = self.name
        extras = self.extras
        version = self.version
        return f"{name}{'[%s]' % (','.join(extras)) if extras else ''}{version or ''}"

    @staticmethod
    def get_node_type() -> type[CheckletComplexType]:
        return CheckletComplexType

    @staticmethod
    def _get_parent_type() -> type[CheckletsComplexType]:
        return CheckletsComplexType

    # noinspection PyAttributeOutsideInit
    def create(self,
               name: str | None = None,
               extras: collections.abc.Iterable[str] | None = None,
               version: str | None = None,
               entrypoint: str | None = None,
               repository: Repository | None = None,
               link: Link | None = None,
               indices: collections.abc.Iterable[Link] | None = None,
               package_versions: collections.abc.Iterable[PackageVersion] | None = None,
               resources: collections.abc.Iterable[Resource] | None = None) -> Self:

        self.name = name
        self.extras = extras
        self.version = version
        self.entrypoint = entrypoint
        self.repository = repository
        self.link = link
        self.indices = indices
        self.package_versions = package_versions
        self.resources = resources
        return self

    # noinspection PyMethodOverriding
    def recreate(self, target_bundle: "momotor.bundles.Bundle") -> "Checklet":
        """ Recreate this :py:class:`Checklet` in a target bundle.
        No attributes can be changed.

        :param target_bundle: The target bundle
        :return: The newly created :py:class:`Checklet`
        """
        return Checklet(target_bundle).create(
            name=self.name,
            extras=self.extras,
            version=self.version,
            entrypoint=self.entrypoint,
            repository=self.repository,
            link=self.link,
            indices=self.indices,
            package_versions=self.package_versions,
            resources=self.resources,
        )

    # noinspection PyMethodOverriding,PyProtectedMember
    def _create_from_node(self, node: CheckletComplexType, parent: CheckletsComplexType | None = None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(parent, True)

        name = []
        if parent and parent.basename:
            name.append(parent.basename)
        if node.name:
            name.append(node.name)

        extras = [extra.strip() for extra in node.extras.split(',')] if node.extras else None

        if node.repository:
            assert len(node.repository) == 1
            repository = Repository(self.bundle)._create_from_node(node.repository[0], args=args)
        else:
            repository = None

        if node.link:
            assert len(node.link) == 1
            # assert not repository
            link = Link(node.link[0].src)
        else:
            link = None

        if node.index:
            assert not repository
            assert not link
            indices = [
                Link(src=index.src) for index in node.index
            ]
        else:
            indices = None

        if node.package_version:
            package_versions = [
                PackageVersion(package_version.name, package_version.version)
                for package_version in node.package_version
            ]
        else:
            package_versions = None

        return self.create(
            name='.'.join(name) if name else None,
            extras=extras,
            version=node.version,
            entrypoint=node.entrypoint,
            repository=repository,
            link=link,
            indices=indices,
            package_versions=package_versions,
            resources=self._collect_resources(node, args=args)
        )

    # noinspection PyProtectedMember
    def _construct_repository_nodes(self, *, args: BundleConstructionArguments) \
            -> collections.abc.Generator[Repository, None, None]:
        if self._repository:
            assert self._repository is not self.__unset, "Uninitialized attribute `repository`"
            yield self._repository._construct_node(args=args)

    def _construct_link_nodes(self, *, args: BundleConstructionArguments) \
            -> collections.abc.Generator[LinkComplexType, None, None]:
        if self._link:
            assert self._link is not self.__unset, "Uninitialized attribute `link`"
            yield LinkComplexType(src=self._link.src)

    # def _construct_index_nodes(self, *, args: BundleConstructionArguments) \
    #        -> collections.abc.Generator[LinkComplexType, None, None]:
    #     if self._indices:
    #         assert self._indices is not self.__unset, "Uninitialized attribute"
    #         for i in self._indices:
    #             yield LinkComplexType(src=i.src)

    def _construct_package_version_nodes(self, *, args: BundleConstructionArguments) \
            -> collections.abc.Generator[CheckletComplexType.PackageVersion, None, None]:
        if self._package_versions:
            assert self._package_versions is not self.__unset, "Uninitialized attribute `package_versions`"
            for pv in self._package_versions:
                yield CheckletComplexType.PackageVersion(name=pv.name, version=pv.version)

    def _construct_node(self, *, args: BundleConstructionArguments) -> CheckletComplexType:
        return CheckletComplexType(
            name=self.name,
            extras=','.join(self.extras) if self.extras else None,
            version=self.version,
            entrypoint=self.entrypoint if self.entrypoint != self._OLD_DEFAULT_ENTRYPOINT else None,
            repository=list(self._construct_repository_nodes(args=args)),
            link=list(self._construct_link_nodes(args=args)),
            index=list(),  # self._construct_index_nodes(args=args),
            package_version=list(self._construct_package_version_nodes(args=args)),
            resources=list(self._construct_resources_nodes(args=args)),
        )


# Extend the docstring with the generic documentation of Element
if Checklet.__doc__ and Element.__doc__:
    Checklet.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


class CheckletMixin(typing.Generic[CT]):
    def _collect_checklet(self: ElementMixinProtocol, node: CT,
                          ref_groups: collections.abc.Iterable[collections.abc.Iterable[object]], *,
                          args: BundleFactoryArguments) \
            -> Checklet | None:

        # TODO use top-level <checklets> node and refs
        if node.checklet:
            if len(node.checklet) > 1:
                raise ValueError("Only one <checklet> node allowed")

            ref_parent, checklet_node = resolve_ref('checklet', node.checklet[0], ref_groups)
            # noinspection PyProtectedMember
            return Checklet(self.bundle)._create_from_node(checklet_node, ref_parent, args=args)

        return None
