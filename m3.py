#!/usr/bin/env python3
"""CLI entry point."""

import click

from src.cli.add import Add
from src.cli.apply import Apply
from src.cli.auth import Auth
from src.cli.diff import Diff
from src.cli.export import Export
from src.cli.freeze import Freeze
from src.cli.init import Init
from src.cli.list import List
from src.cli.prune import Prune
from src.cli.remove import Remove
from src.util.click_helpers import CONTEXT_SETTINGS, command_aliases


@click.group(context_settings=CONTEXT_SETTINGS, cls=command_aliases({
    'add': {'a', 'install'},
    'remove': {'rm', 'uninstall'},
    'diff': {'d'},
    'list': {'l'},
}))
def m3():
    """Click command group for all m3 commands."""


m3.add_command(Init.init)
m3.add_command(Add.add)
m3.add_command(Remove.remove)
m3.add_command(Diff.diff)
m3.add_command(List.list)
m3.add_command(Apply.apply)

m3.add_command(Freeze.freeze)
m3.add_command(Prune.prune)

m3.add_command(Export.export)

m3.add_command(Auth.auth)


if __name__ == '__main__':
    m3()
