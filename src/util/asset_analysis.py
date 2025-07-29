"""Helper functions used to analyze data on assets."""

from packaging.version import InvalidVersion, Version


def is_older_than_version(
        supported: list[str],
        target_version: Version) -> bool:
    """Determines if an asset that supports a list of versions is older than a
    given target version.

    Args:
        supported: The list of versions an asset supports
        target_version: The version to compare the supported versions to

    Returns:
        True if all supported versions are older than the target version, False
        otherwise.
    """
    for v in supported:
        try:
            version = Version(v)
            if version >= target_version:
                return False
        except InvalidVersion:
            continue
    return True


def keyword_in_category_url(categories: list[dict], keyword: str) -> bool:
    """Determines if a keyword exists in the path of at least one of the
    category URLs for the given list of categories.

    Args:
        categories: The list of categories to parse the URLs of
        keyword: The keyword to look for

    Returns:
        True if the keyword is found in at least one of the category URLs, False
        otherwise.
    """
    for category in categories:
        if keyword in category['url']:
            return True
    return False


def keyword_in_modules(modules: list[dict], keyword: str) -> bool:
    """Determines if a keyword exists in the name of at least one of the given
    modules.

    Args:
        modules: The list of modules to parse the names of
        keyword: The keyword to look for

    Returns:
        True if the keyword is found in the name of at least one of the modules,
        False otherwise
    """
    for module in modules:
        if keyword in module['name']:
            return True
    return False
