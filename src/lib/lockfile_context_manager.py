"""Context Managers for m3's lockfile and state on disk."""

from src.config.loader import load_config_and_lockfile


class M3ContextManager():
    """Context manager for m3's state on disk."""

    def __init__(self):
        config, lockfile = load_config_and_lockfile()
        self.config = config
        self.lockfile = lockfile

    def __enter__(self) -> 'M3ContextManager':
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.config.write()
        self.lockfile.write()
