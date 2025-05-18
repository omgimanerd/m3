#!/usr/bin/env python3
"""CLI entry point."""

import click

from src.cli.add import Add
from src.cli.apply import Apply
from src.cli.auth import Auth
from src.cli.export import Export
from src.cli.freeze import Freeze
from src.cli.init import Init
from src.cli.list import List
from src.cli.prune import Prune
from src.cli.remove import Remove
from src.cli.status import Status
from src.util.click import AliasGroup


@click.group(context_settings={
    'help_option_names': ['-h', '--help']
}, cls=AliasGroup)
# pylint: disable-next=missing-function-docstring
def m3():
    pass


m3.add_command(Init.init)
m3.add_command(Add.add)
m3.add_command(Remove.remove)
m3.add_command(Status.status)
m3.add_command(List.list)
m3.add_command(Apply.apply)

m3.add_command(Freeze.freeze)
m3.add_command(Prune.prune)

m3.add_command(Export.export)

m3.add_command(Auth.auth)


if __name__ == '__main__':
    m3()
