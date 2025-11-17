"""Integration and functional testing for apply.py"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from src.cli.apply import Apply
from src.util.enum import AssetType


@patch('src.config.lockfile.LOCKFILE_FILENAME', 'test_m3.lock.json')
@patch('src.config.config.CONFIG_FILENAME', 'test_m3.json')
class ApplyTest:
    @patch('src.util.asset_management.download_file')
    def test_apply(self, mock_download_file, copy_test_data_directory,
                   setup_asset_dir, current_dir, tmp_path, config_from_path,
                   create_tmpdir, create_file):
        """Tests that the apply command applies the lockfile's state to the project
        assets."""
        ref_path = current_dir / 'testdata/'
        runner = CliRunner()

        mock_config = config_from_path(ref_path / 'test_m3.json')
        asset_paths = mock_config.paths.get()

        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            copy_test_data_directory(ref_path, td)
            setup_asset_dir(mock_config, Path(td))

            # Expected filepath of the asset in the real filesystem
            expected_filepath = Path(
                td) / asset_paths[AssetType.TEXTURE_PACK] / 'c.zip'
            tmp_dir_path = Path(td) / 'temp'
            # Expected filepath of the asset in the temp filesystem
            tmp_expected_filepath = tmp_dir_path / \
                asset_paths[AssetType.TEXTURE_PACK] / 'c.zip'
            create_tmpdir(tmp_dir_path)

            # Patch creation of the temp filesystem to make the root of the
            # temp filesystem predictable and match the path we expect
            with patch('tempfile.TemporaryDirectory') as mock_tmpdir:
                mock_tmpdir_context = MagicMock()
                mock_tmpdir_context.__enter__.return_value = tmp_dir_path
                mock_tmpdir.return_value = mock_tmpdir_context

                # side_effect requires a callable but we need to set the args
                # of this side_effect here in the test.
                # Use wrapper function to construct a callable with the args.
                def _mock_download_file(*args, **kwargs):
                    create_file(
                        tmp_expected_filepath, 'Test file c.zip')
                mock_download_file.side_effect = _mock_download_file
                result = runner.invoke(Apply.apply)
        mock_download_file.assert_called_once()
        assert expected_filepath.is_file()
        assert result.exit_code == 0  # Prevents silent failures of test

    @patch('src.util.asset_management.download_file')
    def test_apply_with_remove(
            self, mock_download_file, copy_test_data_directory, current_dir,
            config_from_path, setup_asset_dir, create_tmpdir, tmp_path,
            create_file):
        """Tests that the apply command applies the lockfile's state to the project
        assets and removes assets that are not in the lockfile."""
        ref_path = current_dir / 'testdata/'
        runner = CliRunner(echo_stdin=True)

        mock_config = config_from_path(ref_path / 'test_m3.json')
        asset_paths = mock_config.paths.get()

        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            copy_test_data_directory(ref_path, td)
            setup_asset_dir(mock_config, Path(td))

            # Expected filepath of the asset in the real filesystem
            expected_filepath = Path(
                td) / asset_paths[AssetType.TEXTURE_PACK] / 'c.zip'
            tmp_dir_path = Path(td) / 'temp'
            # Expected filepath of the asset in the temp filesystem
            tmp_expected_filepath = tmp_dir_path / \
                asset_paths[AssetType.TEXTURE_PACK] / 'c.zip'
            create_tmpdir(tmp_dir_path)

            # Patch creation of the temp filesystem to make the root of the
            # temp filesystem predictable and match the path we expect
            with patch('tempfile.TemporaryDirectory') as mock_tmpdir:
                mock_tmpdir_context = MagicMock()
                mock_tmpdir_context.__enter__.return_value = tmp_dir_path
                mock_tmpdir.return_value = mock_tmpdir_context

                # side_effect requires a callable but we need to set the args
                # of this side_effect here in the test.
                # Use wrapper function to construct a callable with the args.
                def _mock_download_file(*args, **kwargs):
                    create_file(
                        tmp_expected_filepath, 'Test file c.zip')
                mock_download_file.side_effect = _mock_download_file
                result = runner.invoke(Apply.apply, ['-r'])
        mock_download_file.assert_called_once()
        uninstalled_filepath = tmp_path / '/assets/mods/b.jar'
        assert not os.path.exists(uninstalled_filepath)
        assert expected_filepath.is_file()
        assert not uninstalled_filepath.is_file()
        assert result.exit_code == 0  # Prevents silent failures of test
