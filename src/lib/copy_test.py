"""Testing for packer.py"""

from glob import glob
from pathlib import Path

from src.lib.copy import copy


def get_files(root_dir: Path) -> list[str]:
    """Returns a list of all files in all subdirectories from the given root."""
    return sorted(list(filter(
        lambda path: (root_dir / path).is_file(),
        glob('**', root_dir=root_dir, recursive=True,
             include_hidden=True))))


def test_copy(current_dir, tmp_path):
    """Tests different permutations of inclusion and exclusion patterns."""
    testdata_dir = current_dir / "testdata" / "test_copy"
    copy(testdata_dir, tmp_path, [
        "config/**",
        "kubejs/**",
        'important_*'
    ], [
        "**/file_to_ignore",
        "**/jsconfig.json",
        "**/generator_script.py",
    ])
    assert get_files(tmp_path) == sorted([
        'config/config.json',
        'important_file',
        'kubejs/assets/asset1',
        'kubejs/assets/asset2',
        'kubejs/assets/asset3',
        'kubejs/dev_script.js',
        'kubejs/script1.js',
    ])


def test_copy2(current_dir, tmp_path):
    """Tests different permutations of inclusion and exclusion patterns."""
    testdata_dir = current_dir / "testdata" / "test_copy"
    copy(testdata_dir, tmp_path, [
        "config/**",
        "kubejs/**",
        "important_file",
    ], [
        "**/file_to_ignore",
        "kubejs/assets/**",
        "**/dev*"
    ])
    assert get_files(tmp_path) == sorted([
        'config/config.json',
        'important_file',
        'kubejs/jsconfig.json',
        'kubejs/script1.js'
    ])
