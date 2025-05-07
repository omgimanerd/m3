"""bisect subcommand module"""

import click


# pylint: disable-next=too-few-public-methods, missing-class-docstring
class Bisect:

    @click.group()
    @staticmethod
    def bisect():
        """Command subgroup for bisect subcommands"""

    @click.command()
    @click.option('no-disable', help="""List of mods to not disable during this
                   bisect operation.""")
    @staticmethod
    def start():
        """Binary searches your currently installed mods, disabling half of
        them at a time until you find a culprit mod that is causing problems."""

    @click.command()
    @staticmethod
    def good():
        """Marks this half of the binary search as good."""

    @click.command()
    @staticmethod
    def bad():
        """Marks this half of the binary search as bad."""

    @click.command()
    @staticmethod
    def reset():
        """Re-enables all mods and stops the binary search."""

    bisect.add_command(start)
    bisect.add_command(good)
    bisect.add_command(bad)
    bisect.add_command(reset)
