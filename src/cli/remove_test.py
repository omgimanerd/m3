"""Integration and function testing for remove.py"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from src.cli.remove import Remove
from src.util.enum import AssetType

ASSET_ID_TO_REMOVE = 'a-jar'
INVALID_ASSET_ID = 'not-an-asset123'


@patch('src.config.lockfile.LOCKFILE_FILENAME', "test_m3.lock.json")
@patch('src.config.config.CONFIG_FILENAME', "test_m3.json")
class RemoveTest:
    def test_remove(
            self, current_dir, config_from_path, tmp_path,
            copy_test_data_directory, setup_asset_dir, create_tmpdir):
        """Tests that the remove command uninstalls the given asset from the
        project."""
        ref_path = current_dir / 'testdata/'
        runner = CliRunner()

        mock_config = config_from_path(ref_path / 'test_m3.json')
        asset_paths = mock_config.paths.get()

        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            copy_test_data_directory(
                ref_path, Path(td))
            setup_asset_dir(mock_config, Path(td))

            # Expected filepath of the removed asset in the real filesystem
            removed_filepath = Path(td) / asset_paths[AssetType.MOD] / 'a.jar'
            tmp_dir_path = Path(td) / 'temp'
            create_tmpdir(tmp_dir_path)

            # Patch creation of the temp filesystem to make the root of the
            # temp filesystem predictable and match the path we expect
            with patch('tempfile.TemporaryDirectory') as mock_tmpdir:
                mock_tmpdir_context = MagicMock()
                mock_tmpdir_context.__enter__.return_value = tmp_dir_path
                mock_tmpdir.return_value = mock_tmpdir_context

                result = runner.invoke(Remove.remove, [ASSET_ID_TO_REMOVE])
                assert not removed_filepath.is_file()
                assert result.exit_code == 0  # Prevents silent failures of test

    @patch('src.cli.remove.uninstall_asset')
    def test_remove_invalid_id(
        self, mock_uninstall_asset, current_dir,
            tmp_path, copy_test_data_directory, load_dir):
        """Tests that the remove command gracefully handles invalid asset
        IDs."""
        ref_path = current_dir / 'testdata/'
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            copy_test_data_directory(
                ref_path, Path(td)
            )
            original_dir_contents = load_dir(Path(td))
            result = runner.invoke(Remove.remove, [INVALID_ASSET_ID])
            new_dir_contents = load_dir(Path(td))
            assert original_dir_contents == new_dir_contents
            mock_uninstall_asset.assert_not_called()
            assert result.exit_code == 0  # Prevents silent failures of test
