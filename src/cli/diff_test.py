"""Integration and functional testing for diff.py"""

from src.cli.diff import evaluate_diff


def test_diff(config_from_path, lockfile_from_path, current_dir):
    """Tests that the diff command shows the diff between the lockfile's state
    and the project assets."""
    config = config_from_path('testdata/test_m3.json')
    lockfile = lockfile_from_path('testdata/test_m3.lock.json')
    missing_assets, new_assets = evaluate_diff(config, lockfile)
    assert missing_assets == ['c.zip']
    assert new_assets == [current_dir / 'testdata/assets/mods/b.jar']
