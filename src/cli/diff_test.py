"""Integration and functional testing for diff.py"""

from unittest.mock import patch

from click.testing import CliRunner

from src.cli.diff import Diff
from src.util.formatter import CustomOutputFormatter


@patch('src.config.lockfile.LOCKFILE_FILENAME', 'test_m3.lock.json')
@patch('src.config.config.CONFIG_FILENAME', 'test_m3.json')
def test_diff(copy_test_data_directory, current_dir, tmp_path):
    """Tests that the diff command shows the diff between the lockfile's state
    and the project assets."""
    ref_path = current_dir / 'testdata/'
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        copy_test_data_directory(ref_path, td)
        result = runner.invoke(Diff.diff)
    formatter = CustomOutputFormatter()
    expected_output = formatter.format(
        '{diff_title:title}', diff_title='Asset Diff')
    expected_output += '\n' + formatter.format(
        '{missing:header}', missing='Lockfile assets missing')
    expected_output += '\n' + formatter.format(
        '{missing_asset:diff_minus}', missing_asset='c.zip')
    expected_output += '\n' + formatter.format(
        '{separator:separator}', separator='')
    expected_output += '\n' + formatter.format(
        '{new_assets:header}', new_assets='New assets found')
    new_asset_path = td + '/assets/mods/b.jar'
    expected_output += '\n' + formatter.format(
        '{new_asset:diff_plus}', new_asset=new_asset_path
    ) + '\n'
    assert result.output == expected_output
