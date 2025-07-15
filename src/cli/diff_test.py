"""Integration and functional testing for diff.py"""

from unittest.mock import patch

from click.testing import CliRunner

from src.cli.diff import Diff, DiffOutputBuilder


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
    output_builder = DiffOutputBuilder()
    expected_output = output_builder.build_diff_output(
        ['c.zip'], [td + '/assets/mods/b.jar']) + '\n'
    assert result.output == expected_output
