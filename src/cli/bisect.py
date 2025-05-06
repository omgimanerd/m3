"""bisect subcommand module"""

import click

from src.util.click_helpers import CONTEXT_SETTINGS


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Bisect:

    @click.group()
    @staticmethod
    def bisect():
        """Command subgroup for bisect subcommands"""

    @click.command(context_settings=CONTEXT_SETTINGS)
    @click.option('no-disable', help="""List of mods to not disable during this
                   bisect operation.""")
    @staticmethod
    def start():
        """Binary searches your currently installed mods, disabling half of
        them at a time until you find a culprit mod that is causing problems."""

    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def good():
        """Marks this half of the binary search as good."""

    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def bad():
        """Marks this half of the binary search as bad."""

    @click.command(context_settings=CONTEXT_SETTINGS)
    @staticmethod
    def reset():
        """Re-enables all mods and stops the binary search."""

    bisect.add_command(start)
    bisect.add_command(good)
    bisect.add_command(bad)
    bisect.add_command(reset)
