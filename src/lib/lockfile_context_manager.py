"""Context Managers for m3's lockfile and state on disk."""

from typing import Optional

from src.config.config import Config
from src.config.loader import load_config_and_lockfile
from src.config.lockfile import Lockfile


class M3ContextManager():
    """Context manager for m3's state on disk."""

    def __init__(self, config: Config, lockfile: Lockfile):
        self.config = config
        self.lockfile = lockfile

    @staticmethod
    # pylint: disable-next=missing-function-docstring
    def create():
        config, lockfile = load_config_and_lockfile()
        return M3ContextManager(config, lockfile)

    def __enter__(self) -> tuple[Optional[Config], Optional[Lockfile]]:
        return (self.config, self.lockfile)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.config.write()
        self.lockfile.write()
