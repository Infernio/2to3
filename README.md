## Fork of 2to3 with Wrye Bash-specific tweaks
Licensed under the same license as CPython, see [LICENSE](LICENSE) for more information.

### Usage
1. Clone this at the same level as wrye-bash, leaving you with a structure like this:
    ```
       |
       |- 2to3
       |- wrye-bash
    ```
1. In the `2to3` directory, run `./run_2to3.sh`.
   Note that this script has only been tested on Linux.
   It should work on macOS and WSL as well, but pure Windows is untested.
1. Wait until all fixers have run.
