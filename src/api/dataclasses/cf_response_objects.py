"""Dataclasses for the CurseForge API to process response data."""


from typing import Optional, Union

from pydantic.dataclasses import dataclass

CF_HASH_ALG_MAP = {
    1: 'sha1',
    2: 'md5'
}


@dataclass
# pylint: disable=too-many-instance-attributes
class CFFile:
    """Schema of the File object returned by the CurseForge API."""
    # pylint: disable=invalid-name
    id: int
    gameId: int
    modId: int
    isAvailable: bool
    displayName: str
    fileName: str
    releaseType: int  # FileReleaseType is an enum
    fileStatus: int  # FileStatus is an enum
    hashes: list[dict]
    fileDate: str
    fileLength: int
    downloadCount: int
    fileSizeOnDisk: int
    downloadUrl: str
    gameVersions: list[str]
    sortableGameVersions: list[dict]
    dependencies: list[dict]
    exposeAsAlternative: bool
    parentProjectFileId: int
    alternateFileId: int
    isServerPack: bool
    serverPackFileId: int
    isEarlyAccessContent: bool
    earlyAccessEndDate: str
    fileFingerprint: int
    modules: list[dict]
    # pylint: enable=invalid-name


@dataclass
# pylint: disable=too-many-instance-attributes
class CFMod:
    """Schema of the Mod object returned by the CurseForge API."""
    # pylint: disable=invalid-name
    id: int
    gameId: int
    name: str
    slug: str
    links: dict
    summary: str
    status: int
    downloadCount: int
    primaryCategoryId: int
    categories: list[dict]
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
    # pylint: enable=invalid-name


@dataclass
class CFGetModResponse:
    """Format for CurseForge "Get Mod" response.

    See documentation for endpoint here:
    https://docs.curseforge.com/rest-api/?python#get-mod
    """
    data: list[CFMod]


@dataclass
class CFGetFilesResponse:
    """Format for CurseForge "Get Files response.

    See documentation for endpoint here:
    https://docs.curseforge.com/rest-api/?python#get-files
    """
    data: list[CFFile]


@dataclass
class CFDataResponse:
    """Data object for CurseForge API calls.

    The payload contains the data from the API call.
    The statusCode optionally contains the HTTP status code.
    The status optionally contains either an explanation of the status code
    corresponding to response.reason or an explanation of a non-HTTP error that
    occurred.
    """
    payload: Union[CFGetModResponse, CFGetFilesResponse]
    status_code: Optional[int]
    status: Optional[str]
