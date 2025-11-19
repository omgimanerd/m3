"""Integration and functional testing for list.py"""

from src.cli.list import LIST_HEADERS_ALL, process_asset_data
from src.util.enum import AssetType


def test_process_asset_data(lockfile_from_path):
    """Tests that the list command processes asset data in the expected
    structure and format."""
    lockfile = lockfile_from_path('testdata/test_m3.lock.json')
    mod_assets = lockfile.get_assets_by_type(AssetType.MOD)
    texture_assets = lockfile.get_assets_by_type(AssetType.TEXTURE_PACK)
    mod_asset_data, mod_max_len = process_asset_data(
        mod_assets, LIST_HEADERS_ALL)
    texture_asset_data, texture_max_len = process_asset_data(
        texture_assets, LIST_HEADERS_ALL)

    assert mod_asset_data == [
        (asset.name, asset.asset_type.value, asset.platform.value)
        for asset in mod_assets.get_values()]
    assert mod_max_len == [
        max(max(len(asset.name) for asset in mod_assets.get_values()), len(LIST_HEADERS_ALL[0])),
        max(max(len(asset.asset_type.value) for asset in mod_assets.get_values()), len(LIST_HEADERS_ALL[1])),
        max(max(len(asset.platform.value) for asset in mod_assets.get_values()), len(LIST_HEADERS_ALL[2]))
    ]

    assert texture_asset_data == [
        (asset.name, asset.asset_type.value, asset.platform.value)
        for asset in texture_assets.get_values()]
    assert texture_max_len == [
        max(max(len(asset.name) for asset in texture_assets.get_values()), len(LIST_HEADERS_ALL[0])),
        max(max(len(asset.asset_type.value) for asset in texture_assets.get_values()), len(LIST_HEADERS_ALL[1])),
        max(max(len(asset.platform.value) for asset in texture_assets.get_values()), len(LIST_HEADERS_ALL[2]))
    ]
