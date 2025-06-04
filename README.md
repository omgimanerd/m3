# m3 - Minecraft Modpack Manager

A CLI tool for Minecraft modpack development to aid in mod version management
and modpack export.

## Authors

-   omgimanerd
-   Ceiran

# Usage

Usage: m3.py [OPTIONS] COMMAND [ARGS]...

Options:
-h, --help Show this message and exit.

Commands:
```
add Installs assets into the project.
apply Applies the lockfile's state to the project assets.
auth Set or get the CurseForge API key.
export Builds the modpack for export.
freeze Saves the state of the project's assets into the lockfile.
init Initializes an m3 managed project in the current directory.
list Lists the assets present in the project lockfile configuration.
prune Removes project assets that are not in the lockfile.
remove Removes the specified asset from your file system and lockfile.
status Diffs the lockfile against the project asset directories.
```