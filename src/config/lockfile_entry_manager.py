"""Class for managing the lockfile data."""

import os
from pathlib import Path

from click import ClickException

from src.config.config import Config
from src.config.lockfile import Lockfile, LockfileEntries
from src.lib.dataclasses import get_field_names
from src.lib.multikey_dict import MultiKeyDict
from src.util.hash import hash_jar_dir_multi_hash
from src.util.web_util import download_file

# Order of HASH_ALGS must match order of algs in key_set for MultiKeyDict
HASH_ALGS = ['sha1', 'sha512', 'md5']
DEFAULT_ALG = 'sha512'


class LockfileEntryManager:
    """Wrapper class for managing and modifying lockfile entries."""

    def __init__(self, lockfile: Lockfile, config: Config):
        self.config = Config.get_config()
        self.lockfile = lockfile
        self.lockfile_entries = lockfile.lockfile_entries
        self.asset_paths = config.resolve_asset_paths()
        self.entry_hash_map = {}
        self.curr_asset_hash_map = {asset: {}
                                    for asset in get_field_names(LockfileEntries)}

    def _rm_asset_file(self, asset: str, asset_hash: str):
        """Removes an asset file given the asset type and its file hash.

        Args:
            asset: The asset type to look under
            asset_hash: The hash of the asset file to delete
        """
        asset_path = self.asset_paths[asset]
        curr_asset = self.curr_asset_hash_map[asset].get(asset_hash)
        if curr_asset is not None:
            file_name = curr_asset['file_name']
            file_path = asset_path / file_name

            if os.path.exists(file_path):
                os.remove(file_path)

    def config_entry_hash_map(self):
        """Configures a hash map that maps asset entries to their hashes and
        asset names using multikey dicts.

        Creates a separate hash map entry for each asset to encapsulate each
        multikey dict.
        """
        for asset in get_field_names(LockfileEntries):
            asset_entries = getattr(self.lockfile_entries, asset)
            # Extra count for indexing by human-readable name
            num_of_keys = len(HASH_ALGS) + 1
            self.entry_hash_map[asset] = MultiKeyDict(num_of_keys)
            for name, entry in asset_entries.items():
                key_set = (entry.hash.sha1,
                           entry.hash.sha512, entry.hash.md5, name)
                self.entry_hash_map[asset].add(key_set, entry)

    def hash_current_asset_files(self):
        """Hashes the .jar files in each asset path defined by the m3 config and
        returns a dict containing the hashes for each .jar file.

        Sets this as the hash map to reference for the current state of the
        assets.

        For each .jar file, generates hashes with all algorithms listed in
        `HASH_ALGS` and uses the algorithm defined by `DEFAULT_ALG` to index the
        sub-dict containing these hashes. Note that the `DEFAULT_ALG` should be 
        an algorithm in `HASH_ALGS`.
        """
        if DEFAULT_ALG not in HASH_ALGS:
            # Is this the right exception type?
            raise ClickException('Specified default hashing algorithm ' +
                                 f'{DEFAULT_ALG} not in ' +
                                 f'hash algorithms to use: {HASH_ALGS}')
        for asset in get_field_names(LockfileEntries):
            path = self.asset_paths[asset]
            if not path.is_file() and (any(path.iterdir())):
                asset_hashes = hash_jar_dir_multi_hash(
                    path, HASH_ALGS, DEFAULT_ALG)
                self.curr_asset_hash_map[asset] = asset_hashes

    def config_hash_maps(self):
        """Configures all hash maps required to compare lockfile state and the 
        current assets state."""
        self.config_entry_hash_map()
        self.hash_current_asset_files()

    def _get_asset_entry_from_hash(self, asset: str, asset_sha: str):
        """Returns the lockfile entry for the given hashed asset. If the asset 
        map is empty or the asset is not found, returns None.

        Args:
            asset: The asset type to look under
            asset_sha: The hash of the file of this asset

        Returns:
            The associated lockfile asset entry if it exists, else returns None.
        """
        if len(self.entry_hash_map[asset]) == 0:
            return None
        return self.entry_hash_map[asset].get(asset_sha)

    def _get_nth_key_from_multikey(self, multikeydict: MultiKeyDict, index: int
                                   ) -> list:
        """Returns the nth key in the multikey for all multikeys in the dict.

        Args:
            multikeydict: The multikeydict to get all nth keys for
            index: The nth key to get, where n is equal to index

        Returns:
            A list containing the nth key for all multikeys in the dict.
        """
        return [multikey[index] for multikey in multikeydict.get_multikeys()]

    def _get_diff_of_lockfile_and_curr_assets(self, asset: str):
        """Returns a set containing the asset hashes that exist in the lockfile
        but not in the current assets.

        Args:
            asset: The asset type to compare hashes for

        Returns:
            A set containing the set difference of the lockfile entries and the
            current assets for the given asset type.
        """
        index = HASH_ALGS.index(DEFAULT_ALG)
        lockfile_assets_set = set(self._get_nth_key_from_multikey(
            self.lockfile_entries[asset], index))
        curr_assets_set = set(self.curr_asset_hash_map[asset].keys())
        return lockfile_assets_set.difference(curr_assets_set)

    def _get_diff_of_curr_assets_and_lockfile(self, asset: str):
        """Returns a set containing the asset hashes that exist in the current 
        assets but not in the lockfile.

        Args:
            asset: The asset type to compare hashes for

        Returns:
            A set containing the set difference of the current assets and the 
            lockfile entries for the given asset type.
        """
        index = HASH_ALGS.index(DEFAULT_ALG)
        lockfile_assets_set = set(self._get_nth_key_from_multikey(
            self.lockfile_entries[asset], index))
        curr_assets_set = set(self.curr_asset_hash_map[asset].keys())
        return curr_assets_set.difference(lockfile_assets_set)

    def _get_intersect_of_lockfile_and_curr_assets(self, asset: str):
        """Returns a set containing the asset hashes that exist in both the 
        lockfile and the current assets.

        Args:
            asset: The asset type to compare hashes for

        Returns:
            A set containing the set intersect of the lockfile entries and the 
            current assets for the given asset type.
        """
        index = HASH_ALGS.index(DEFAULT_ALG)
        lockfile_assets_set = set(self._get_nth_key_from_multikey(
            self.lockfile_entries[asset], index))
        curr_assets_set = set(self.curr_asset_hash_map[asset].keys())
        return lockfile_assets_set.intersection(curr_assets_set)

    def apply_lockfile_for_asset(self, asset: str, install_queue: set):
        """Given a set containing hashes of assets in the lockfile but not in 
        the current assets, applies the state of the lockfile by downloading 
        those assets.

        Args:
            asset: The asset type to apply the lockfile state for
            install_queue: The set containing hashes of assets to download
        """
        for asset_sha in install_queue:
            asset = self._get_asset_entry_from_hash(asset, asset_sha)
            cdn_link = asset.file_data.cdn_link
            asset_entry = self.entry_hash_map[asset].get(asset_sha)
            asset_name = asset_entry.file_name
            dest = Path(self.asset_paths[asset]) / asset_name
            download_file(cdn_link, dest)

    def rm_asset_lockfile_diff_from_curr_assets(self, asset: str, rm_queue: set):
        """Given a set containing hashes of assets in the current assets but not 
        in the lockfile, applies the state of the lockfile by removing those 
        assets from the current assets.

        Args:
            asset: The asset type to apply the lockfile state for
            rm_queue: The set containing hashses of assets to remove
        """
        for asset_sha in rm_queue:
            self._rm_asset_file(asset, asset_sha)

    def apply(self):
        """Applies the lockfile state to the current assets by installing any 
        assets that exist in the lockfile but do not exist in the current
        assets.

        Note that it will not remove any assets that are already installed but 
        do not exist in the lockfile.
        """
        for asset in get_field_names(LockfileEntries):
            install_queue = self._get_diff_of_lockfile_and_curr_assets(asset)
            self.apply_lockfile_for_asset(asset, install_queue)

    def prune(self):
        """Removes any assets that are currently installed but are not listed 
        in the lockfile."""
        for asset in get_field_names(LockfileEntries):
            rm_queue = self._get_diff_of_curr_assets_and_lockfile(asset)
            self.rm_asset_lockfile_diff_from_curr_assets(asset, rm_queue)
