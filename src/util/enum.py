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
