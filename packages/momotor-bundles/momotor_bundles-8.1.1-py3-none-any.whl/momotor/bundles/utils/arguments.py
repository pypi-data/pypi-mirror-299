from __future__ import annotations

from dataclasses import dataclass, field

import collections.abc
import pathlib
from zipfile import ZIP_DEFLATED

__all__ = [
    "BundleFactoryArguments",
    "FileConstructionArguments",
    "DirectoryConstructionArguments",
]


@dataclass(frozen=True)
class BundleFactoryArguments:
    #: XML file name if not the default (for directory and zip paths)
    xml_name: str | None = field(default=None)

    #: force (``True``) or prevent (``False``) use of `lxml`_ library.
    #: If ``None``, uses `lxml`_ when installed.
    use_lxml: bool | None = field(default=None)

    #: enable (``True``) or disable (``False``) XML validation.
    #: If ``None``, uses default setting, which is to enable validation
    validate_xml: bool | None = field(default=None)

    #: location used in error messages
    location_base: str | pathlib.Path = field(default=None)

    #: validate <file> node signatures
    validate_signature: bool = field(default=True)

    #: accept XML produced with legacy generator (the `momotor-common` package)
    legacy: bool = field(default=False)


@dataclass(frozen=True)
class BundleConstructionArguments:
    #: force (``True``) or prevent (``False``) use of `lxml`_ library.
    #: If ``None``, auto-detects `lxml`_ availability
    use_lxml: bool | None = field(default=None)

    #: generate a better readable XML document
    pretty_xml: bool = field(default=False)

    #: encoding of the XML document
    encoding: str = field(default='utf-8')

    #: name of the xml document. If not provided uses the default name for the bundle
    #: (eg. `recipe.xml`, `config.xml`, `product.xml` or `result.xml`)
    xml_name: str = field(default=None)

    #: sign the <file> nodes. This calculates a hash of the attachments and adds it as an attribute in the XML
    sign_files: bool = field(default=True)

    #: hashing algorithms to use when :py:attr:`sign_files` is set to ``True``. Default ``['sha1']``
    hashers: collections.abc.Sequence[str] = field(default_factory=lambda: tuple(['sha1']))

    #: write XML compatible with legacy parser (the `momotor-common` package)
    legacy: bool = field(default=False)

    #: create optimized bundle
    optimize: bool = field(default=True)

    #: add a generator meta node. If ``True``, uses this package's name and version number. If ``False`` does not add
    #: a generator node. If a string is provided, uses that as the generator name, and adds the package name.
    #: Default ``True``
    generator_name: bool | str = field(default=True)


@dataclass(frozen=True)
class FileConstructionArguments(BundleConstructionArguments):
    #: force zip format output
    zip: bool = False

    #: compression mode, see :py:class:`zipfile.ZipFile` for possible values.
    #: (Defaults to :py:data:`~zipfile.ZIP_DEFLATED`, only used when generating a zipped bundle)
    compression: int = field(default=ZIP_DEFLATED)

    #: compression level, see :py:class:`zipfile.ZipFile` for possible values.
    #: (Only used when generating a zipped bundle)
    compresslevel: int | None = field(default=None)


@dataclass(frozen=True)
class DirectoryConstructionArguments(BundleConstructionArguments):
    #: the mode bits (defaults to `0o700`, making the directory only accessible to the current user)
    dir_mode: int = field(default=0o700)
