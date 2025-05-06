#!/usr/bin/env python3
"""CLI entry point."""

import click

from src.cli.add import Add
from src.cli.apply import Apply
from src.cli.auth import Auth
from src.cli.init import Init
from src.cli.list import List
from src.config.config import Config


def test():
    c = Config.get_config()
    print(c)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def m3():
    """Click command group for all m3 commands."""


m3.add_command(Init.init)
m3.add_command(Add.add)
m3.add_command(Auth.auth)
m3.add_command(List.list)
m3.add_command(Apply.apply)


if __name__ == '__main__':
    m3()
