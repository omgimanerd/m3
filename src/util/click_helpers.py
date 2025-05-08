"""Helpers for click to declare command aliases."""

import click


class AliasCommand(click.Command):
    """Custom subclass of click.Command that supports an extra aliases kwargs
    to be stored as an acceptable alias for executing the command."""

    # pylint: disable-next=dangerous-default-value
    def __init__(self, *args, aliases=[], **kwargs):
        self.aliases = set(aliases)
        super().__init__(*args, **kwargs)

    def format_help(self, ctx, formatter):
        """Overrides the format_help function to write the accepted aliases into
        the help text."""
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        if len(self.aliases) > 0:
            with formatter.section('Aliases'):
                formatter.write_text(', '.join(self.aliases))
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)


def command_with_aliases(*args, **kwargs):
    """Returns a decorator that wraps the click.command decorator, forwarding
    *args as aliases to the AliasCommand subclass and **kwargs to the
    underlying click.command decorator itself."""
    def decorator(func):
        return click.command(cls=AliasCommand, aliases=args, **kwargs)(func)
    return decorator


class AliasGroup(click.Group):
    """Custom subclass of click.Group that allows for command aliasing using
    the decorator above."""

    def get_command(self, ctx: click.Context, cmd_name: str):
        """Overload of click.Group's get_command method to search through the
        a command's registered aliases if they exist.

        Args:
           ctx: The click context
           cmd_name: The command name provided on the actual command line
        """
        # Attempt to look up the base command first.
        default_command = click.Group.get_command(self, ctx, cmd_name)
        if default_command is not None:
            return default_command
        for command_name in self.list_commands(ctx):
            # Get the actual command object corresponding to the command name
            command = self.get_command(ctx, command_name)
            if isinstance(command, AliasCommand):
                if cmd_name in command.aliases:
                    return command
        return None

    def resolve_command(self, ctx: click.Context, args: list[any]):
        """Overload of click.Group's resolve_command method to always return the
        full command name."""
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args
