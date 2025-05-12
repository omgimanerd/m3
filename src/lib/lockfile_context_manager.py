"""File Context Manager for m3 lockfile."""


class LockfileContextManager():
    """Context manager for m3 lockfile."""

    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()
