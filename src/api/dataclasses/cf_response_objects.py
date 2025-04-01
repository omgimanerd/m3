from dataclasses import dataclass


@dataclass
class CFGetModData:
    """
    Metadata for CurseForge Mod
    """
    id: int
    gameId: int
    name: str
    slug: str
    links: dict
    summary: str
    status: int
    downloadCount: int
    primaryCategoryId: int
    classId: int
    authors: list[dict]
    mainFileId: int
    latestFiles: list[dict]
    latestFileIndexes: list[dict]
    latestEarlyAccessFilesIndexes: list[dict]
    dateCreated: str
    dateModified: str
    allowModDistribution: bool
    isAvailable: bool


@dataclass
class CFGetModResponse:
    """
    Format for CurseForge "Get Mod" response
    """
    data: list[CFGetModData]
