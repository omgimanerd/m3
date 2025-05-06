"""Helper to set the context settings for CLI commands that accept -h or
--help"""

from typing import Dict

import click

# Context settings used by click command declarations to allow -h or --help as
# help option triggers
CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


def command_aliases(aliases: Dict[str, set[str]]):
    """Returns a subclass of click.Group that handles command aliasing.

    https://click.palletsprojects.com/en/stable/advanced/#command-aliases

    Args:
        aliases: a mapping of commands to their accepted aliases

    Returns:
        the subclass type used by click to resolve commands.
    """
    alias_map = {alias: command for command, _aliases in aliases.items()
                 for alias in _aliases}

    def get_command(self, ctx, cmd_name):
        """Overload of click.Group's get_command method to search through the
        given alias map when getting a command by its alias name."""
        if cmd_name in alias_map:
            return click.Group.get_command(self, ctx, alias_map[cmd_name])
        ctx.fail(f'No such command `{cmd_name}`')
        return None

    def resolve_command(self, ctx, args):
        """Overload of click.Group's resolve_command method to always return the
        full command name."""
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

    # Returns a dynamically created class type that is a subclass of click.Group
    return type('CommandAlias', (click.Group,), {
        'get_command': get_command,
        'resolve_command': resolve_command
    })
