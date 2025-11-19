"""list subcommand module"""

from typing import Tuple

import click

from src.config.loader import load_config_and_lockfile
from src.lib.multikey_dict import MultiKeyDict
from src.util.click import command_with_aliases
from src.util.enum import AssetType
from src.util.formatter import CustomOutputFormatter

INVALID_ASSET_TYPE_MSG = 'Not a valid asset type. See --help for valid asset types.'
LIST_HEADERS_ALL = ['NAME', 'TYPE', 'SOURCE']
LIST_HEADERS_BY_TYPE = ['NAME', 'SOURCE']


def process_asset_data(
        asset_multikey_dict: MultiKeyDict,
        headers: list[str]) -> Tuple[list[tuple], list[int]]:
    """Given a MultiKeyDict containing asset data, extract the asset name, type,
    and source for each asset, depending on the headers indicated. Return this
    information stored in a tuple for each asset, along with the max length
    found for each field.
    
    Args:
        asset_multikey_dict: A MultiKeyDict containing asset data to process
        headers: A list of header names indicating which data fields to extract

    Returns:
        A list of tuples containing the extracted data for each asset and a list
        of ints containing the max length found for each field.
    """
    asset_data = []
    max_len = [len(field) for field in headers]
    for asset in asset_multikey_dict.get_values():
        entry = []
        for i, field in enumerate(headers):
            if field == 'NAME':
                entry.append(asset.name)
                max_len[i] = max(max_len[i], len(asset.name))
            elif field == 'TYPE':
                entry.append(asset.asset_type.value)
                max_len[i] = max(max_len[i], len(asset.asset_type.value))
            else:
                entry.append(asset.platform.value)
                max_len[i] = max(max_len[i], len(asset.platform.value))
        asset_data.append(tuple(entry))
    return asset_data, max_len


def update_max_len(max_len: list[int], curr_max: list[int]) -> list[int]:
    """Given a list of max lengths of each field so far, update and return the
    list based on max lengths recorded for another batch of data.
    
    Args:
        max_len: The max lengths recorded so far for each field
        curr_max: The new max lengths recorded for a new batch of data

    Returns:
        A list containing the max lengths of each field across both previously
        and newly processed data.
    """

    return [max(a, b) for a, b in zip(max_len, curr_max)]


class ListOutputBuilder:
    """Builds the output for the list command in a predefined format to
    display."""

    def build_list_output(
            self, assets: list[tuple], col_widths: list[int], 
            header_titles: list[str], asset_type: AssetType=None) -> str:
        """Given a list of tuples containing the relevant asset
        data, builds the output for the list command and adjust the width of
        each field according to the minimum width required specified in
        col_widths. Sorts the asset data output in alphabetical order by asset
        name.

        Args:
            assets: The relevant asset data to print col_widths: The minimum
            required width for each column of data header_titles: The titles of
            each column to put in the header asset_type: optional arg to specify
            asset type in title of output

        Returns:
            The output for the list command as a string.
        """
        formatter = CustomOutputFormatter()
        output = ''
        if asset_type:
            output += formatter.format('{list_title:title}', 
                                       list_title=f'{asset_type.name} Asset List')
        else:
            output += formatter.format('{list_title:title}',
                                   list_title='Asset List')
        if len(assets) == 0:
            output += '\n' + formatter.format(
                '{no_assets:header}', no_assets='No assets found'
            )
            return output
        
        header = ''
        for i, header_name in enumerate(header_titles):
            header += formatter.format(f'{header_name:<{max(len(header_name), col_widths[i]) + 2}}')
        output += '\n' + header
        for asset in sorted(assets):
            entry = ''
            for i, asset_data in enumerate(asset):
                entry += formatter.format(f'{asset_data:<{max(len(header_titles[i]), col_widths[i]) + 2}}')
            output += '\n' + entry
            
        return output



# pylint: disable-next=missing-class-docstring
class List:
    @command_with_aliases('l', 'ls')
    @click.option('-t', '--type', 'type_',
                  help="""Filters the output by asset type.""")
    @staticmethod
    def list(type_):
        """Lists the assets present in the project lockfile configuration.

        Use `m3 diff` to diff it against the project directory contents.

        Valid asset types: mod, resource_pack, shader_pack, texture_pack
        """
        config, lockfile = load_config_and_lockfile()

        if config is None or lockfile is None:
            raise click.ClickException('Not an m3 project')

        if type_:
            if type_ not in AssetType:
                click.echo(INVALID_ASSET_TYPE_MSG)

            lockfile_assets_multikey_dict = lockfile.get_assets_by_type(
                AssetType(
                    type_))

            # Build output here and return
            asset_data, max_len = process_asset_data(lockfile_assets_multikey_dict, LIST_HEADERS_BY_TYPE)
            output_builder = ListOutputBuilder()
            output = output_builder.build_list_output(asset_data, max_len, LIST_HEADERS_BY_TYPE)
            click.echo(output)
            return

        output = ''
        output_builder = ListOutputBuilder()
        asset_datas = {}
        max_len = [len(field) for field in LIST_HEADERS_ALL]
        for asset_type in AssetType:
            lockfile_assets_multikey_dict = lockfile.get_assets_by_type(
                asset_type)
            # Build output here and return
            asset_data, curr_max = process_asset_data(lockfile_assets_multikey_dict, LIST_HEADERS_ALL)
            asset_datas[asset_type] = asset_data
            max_len = update_max_len(max_len, curr_max)
        for asset_type, data in asset_datas.items():
            asset_output = output_builder.build_list_output(data, max_len, LIST_HEADERS_ALL, asset_type)
            output += '\n' + asset_output + '\n'
        click.echo(output)
