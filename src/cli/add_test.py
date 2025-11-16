"""Integration and function testing for add.py"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from src.api.wrappers.cf_wrapper import CurseForgeWrapper
from src.cli.add import Add
from src.config.lockfile_entry import LockfileEntry
from src.lib.asset import CurseForgeAsset
from src.util.enum import AssetType, Platform, Side

FILE_ID_FOR_TEST = 17
MOD_ID_FOR_TEST = 71


@patch('src.config.lockfile.LOCKFILE_FILENAME', "test_m3.lock.json")
@patch('src.config.config.CONFIG_FILENAME', "test_m3.json")
class AddTest:
    @patch.object(LockfileEntry, 'create_lockfile_entry_from_resp_obj')
    @patch.object(CurseForgeWrapper, 'get_mod')
    @patch.object(CurseForgeWrapper, 'get_asset_files')
    @patch('src.util.asset_management.download_file')
    def test_add(
            self, mock_download_file, mock_get_asset_files, mock_get_mod,
            mock_create_lockfile_entry_from_resp_obj, copy_test_data_directory,
            current_dir, tmp_path, create_file, read_json_file):
        """Tests that the add command installs the given asset to the project."""
        ref_path = current_dir / 'testdata/'
        runner = CliRunner()

        mock_get_asset_return = MagicMock()
        mock_asset_data = MagicMock()
        mock_asset_data.modId = MOD_ID_FOR_TEST
        mock_get_asset_return.__getitem__.return_value = mock_asset_data
        mock_get_asset_files.return_value.data = mock_get_asset_return

        mock_get_mod.return_value.data = {'id': MOD_ID_FOR_TEST}
        mock_asset_hashes = read_json_file(
            current_dir / 'testdata/test_add_file_hashes.json')
        mock_asset = CurseForgeAsset(
            name="d.jar", display_name="d.jar", platform=Platform.CURSEFORGE,
            asset_type=AssetType.MOD, side=Side.BOTH, cdn_link="test-cdn-link",
            dependencies=[],
            project_id=MOD_ID_FOR_TEST, file_id=FILE_ID_FOR_TEST)
        mock_create_lockfile_entry_from_resp_obj.return_value = LockfileEntry(
            name=mock_asset.name, display_name=mock_asset.display_name,
            hash=mock_asset_hashes, platform=mock_asset.platform,
            asset_type=mock_asset.asset_type, asset=mock_asset)

        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            copy_test_data_directory(ref_path, td)
            expected_filepath = Path(td) / 'assets/mods/d.jar'

            def _mock_download_file(*args, **kwargs):
                create_file(expected_filepath, 'Test file d.jar')
            mock_download_file.side_effect = _mock_download_file
            runner.invoke(Add.add, [str(FILE_ID_FOR_TEST)])
            mock_download_file.assert_called_once()
            assert expected_filepath.is_file()

    @patch('src.util.asset_management.download_file')
    def test_add_invalid_file_id_format(
            self, mock_download_file, copy_test_data_directory, current_dir,
            tmp_path, load_dir):
        """Tests that the add command displays an error message to the user when
        provided with a non-numerical file ID."""
        ref_path = current_dir / 'testdata/'
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            copy_test_data_directory(ref_path, td)
            original_dir_contents = load_dir(Path(td))
            runner.invoke(Add.add, ['abc'])
            new_dir_contents = load_dir(Path(td))
            assert original_dir_contents == new_dir_contents
            mock_download_file.assert_not_called()
