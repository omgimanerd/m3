"""Testing for packer.py"""

from src.config.config import Config
from src.lib.packer import copy_files


def test_copy_pack_files(current_dir, tmp_path):
    """Tests different permutations of inclusion and exclusion patterns."""
    c = Config(
        name="test_copy_pack_files_config",
        client_includes=[
            "config",
            "kubejs"
        ],
        client_excludes=[
            "*file_to_ignore",
        ],
        server_includes=[
            "config",
            "kubejs",
        ],
        server_excludes=[
            "kubejs/assets/*"
            "*file_to_ignore",
        ]
    )
    testdata_dir = current_dir / "testdata" / "test_copy_pack_files"
    copy_files(testdata_dir, tmp_path, [
        "config",
        "kubejs",
        'important_*'
    ], [
        "*file_to_ignore",
        "*jsconfig.json"
    ])
