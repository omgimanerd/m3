"""export subcommand module"""


from src.config.config import Config
from src.lib.copy import copy
from src.util.click import command_with_aliases

TMP_DIR = '.tmp'

# pylint: disable-next=too-few-public-methods, missing-class-docstring


class Export:
    @command_with_aliases('ex')
    @staticmethod
    def export():
        """Builds the modpack for export."""


def export(config: Config):
    """Handles exporting the client and server pack to the designated output
    directory as specified by the given config, using the provided inclusion
    and exclusion globs.

    Args:
      config: the m3 configuration to read
    """
    minecraft_dir = config.get_path().parent
    tmp_dir = config.output / TMP_DIR

    # Build and write the client output
    client_dir = tmp_dir / "client"
    copy(minecraft_dir, client_dir,
         config.client_includes, config.client_excludes)

    # Build and write the server output
    server_dir = tmp_dir / "server"
    copy(minecraft_dir, server_dir,
         config.server_includes, config.server_excludes)
