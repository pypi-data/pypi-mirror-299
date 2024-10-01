from __future__ import annotations

import collections.abc
import dataclasses

from momotor.bundles.base import Bundle
from momotor.bundles.binding import Config as ConfigRootType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.meta import MetaMixin, Meta
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.mixins.id import IdMixin
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['ConfigBundle']


class ConfigBundle(Bundle[ConfigRootType], IdMixin, MetaMixin, OptionsMixin, FilesMixin):
    """ A config bundle. This implements the interface to create and access Momotor configuration files
    """
    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str | None = None,
               meta: Meta | None = None,
               options: collections.abc.Iterable[Option] | None = None,
               files: collections.abc.Iterable[File] | None = None) -> Self:
        """ Set all attributes for this :py:class:`~momotor.bundles.ConfigBundle`

        Usage:

        .. code-block:: python

           config = ConfigBundle(...).create(id=..., meta=..., options=..., files=...)

        :param id: `id` of the bundle (optional)
        :param meta: `meta` of the bundle (optional)
        :param options: list of options (optional)
        :param files: list of files (optional)
        :return: self
        """
        self.id = id
        self.meta = meta
        self.options = options
        self.files = files
        return self

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ConfigRootType, *, args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)

        return self.create(
            id=node.id,
            meta=self._collect_meta(node, args=args),
            options=self._collect_options(node, [], args=args),
            files=self._collect_files(node, [], args=args)
        )

    def _construct_node(self, *, args: BundleConstructionArguments) -> ConfigRootType:
        child_args = dataclasses.replace(args, generator_name=False)
        return ConfigRootType(
            id=self.id,
            meta=list(self._construct_meta_node(args=args)),
            options=list(self._construct_options_nodes(args=child_args)),
            files=list(self._construct_files_nodes(args=child_args)),
        )

    @staticmethod
    def get_node_type() -> type[ConfigRootType]:
        return ConfigRootType

    @staticmethod
    def get_default_xml_name() -> str:
        """ Get the default XML file name

        :return: 'config.xml'
        """
        return 'config.xml'

    @staticmethod
    def get_category() -> BundleCategory:
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.CONFIG`
        """
        return BundleCategory.CONFIG


# Extend the docstring with the generic documentation of Bundle
if ConfigBundle.__doc__ and Bundle.__doc__:
    ConfigBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
