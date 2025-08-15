"""Integration and functional testing for apply.py"""

import os
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from src.cli.apply import Apply


@patch('src.config.lockfile.LOCKFILE_FILENAME', 'test_m3.lock.json')
@patch('src.config.config.CONFIG_FILENAME', 'test_m3.json')
@patch('src.util.asset_management.download_file')
def test_apply(mock_download_file,
               copy_test_data_directory, current_dir, tmp_path,
               create_file):
    """Tests that the apply command applies the lockfile's state to the project
    assets."""
    ref_path = current_dir / 'testdata/'
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        copy_test_data_directory(ref_path, td)
        mock_download_file.side_effect = lambda *args, **kwargs: create_file(
            Path(td) / 'assets/texturepacks/c.zip', 'Test file c.zip')
        result = runner.invoke(Apply.apply)
    mock_download_file.assert_called_once()
    assert "Installed c.zip" in result.output


@patch('src.config.lockfile.LOCKFILE_FILENAME', 'test_m3.lock.json')
@patch('src.config.config.CONFIG_FILENAME', 'test_m3.json')
@patch('src.util.asset_management.download_file')
def test_apply_with_remove(
        mock_download_file, copy_test_data_directory, current_dir, tmp_path,
        create_file):
    """Tests that the apply command applies the lockfile's state to the project
    assets and removes assets that are not in the lockfile."""
    ref_path = current_dir / 'testdata/'
    runner = CliRunner(echo_stdin=True)

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        copy_test_data_directory(ref_path, td)
        mock_download_file.side_effect = lambda *args, **kwargs: create_file(
            Path(td) / 'assets/texturepacks/c.zip', 'Test file c.zip')
        result = runner.invoke(Apply.apply, ['-r'])

    mock_download_file.assert_called_once()
    assert not os.path.exists(tmp_path / '/assets/mods/b.jar')
    assert "Installed c.zip" in result.output
    assert "Uninstalled b.jar" in result.output
