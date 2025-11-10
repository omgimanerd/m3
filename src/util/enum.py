"""Enums used by this codebase."""

from enum import Enum


class Platform(Enum):
    """CurseForge or Modrinth, we only support exporting packs to these two
    platforms."""
    CURSEFORGE = 'curseforge'
    MODRINTH = 'modrinth'


class Side(Enum):
    """Mod required on client-side, server-side, or both.

    If required on one side (e.g. client-side), implied that it is optional for 
    the other side.
    """
    CLIENT = 'client'
    SERVER = 'server'
    BOTH = 'both'


class AssetType(Enum):
    """Asset types that m3 manages."""
    MOD = 'mod'
    RESOURCE_PACK = 'resource_pack'
    TEXTURE_PACK = 'texture_pack'
    SHADER_PACK = 'shader_pack'


class HashAlg(Enum):
    """Hash algorithms that m3 supports."""
    SHA1 = 'sha1'
    SHA256 = 'sha256'
    SHA512 = 'sha512'
    MD5 = 'md5'


class AssetStatus(Enum):
    """Asset status indicating its state in the current project."""
    INSTALLED = 'installed'
    ERROR_INSTALL = 'error_install'
