from dataclasses import dataclass
from typing import Optional
from typing import Union


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


@dataclass
class CFDataResponse:
    '''
    Data object for CurseForge API calls.

    The payload contains the data from the API call.
    The statusCode optionally contains the HTTP status code.
    The status optionally contains either an explanation of the status code corresponding to response.reason
    or an explanation of a non-HTTP error that occurred.
    '''
    payload: CFGetModResponse
    statusCode: Optional[int]
    status: Optional[str]
