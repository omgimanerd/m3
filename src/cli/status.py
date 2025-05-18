"""diff subcommand"""

from src.util.click import command_with_aliases


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Status:
    @command_with_aliases('s', 'st')
    @staticmethod
    def status():
        """Diffs the lockfile against the project asset directories."""
