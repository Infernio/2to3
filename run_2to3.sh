#!/bin/bash

# Check if stdout is a tty and supports color
# If not, they will be undefined and hence resolve to empty strings
if test -t 1
then
    ncolors=$(tput colors)
    if test -n "$ncolors" && test "$ncolors" -ge 8
    then
        C_RED='\033[1;31m'
        C_GREEN='\033[1;32m'
        C_BLUE='\033[1;34m'
        C_YELLOW='\033[1;33m'
        C_NC='\033[0m'
    fi
fi

# Function to check if a list (string of space-separated words)
# contains a string
function contains() {
    local haystack="$1"
    local needle="$2"
    if [[ $haystack =~ (^|[[:space:]])"$needle"($|[[:space:]]) ]]
    then
        res=0
    else
        res=1
    fi
    return $res
}

# Fixers that we want to skip, e.g. because they just break things
SKIPPED_FIXERS="funcattrs idioms unicode_literals ws_comma"

# The working directory that the script was run in
WORKING_DIR="$(pwd)"

# The directory that we want to run 2to3 on
TARGET_DIR="$(readlink -fn ../wrye-bash)"

cd "$TARGET_DIR"
# Check that the user won't have existing changes added into our commits
if [ ! -z "$(git status --porcelain)" ]
then
    echo -e "${C_RED}Error:${C_NC} $TARGET_DIR has uncommited changes."
    echo "Commit or stash them before running this script."
    exit 1
fi

# Disable commit signing temporarily to avoid the 50+ popups
git config --local commit.gpgSign false
cd "$WORKING_DIR"

fixers="$(python3 -m lib2to3 -l | tail -n +2)"
echo -e "${C_BLUE}::${C_NC} Running $(echo $fixers | wc -w) fixers"
while IFS= read -r fixer
do
    # Skip this fixer if it's in SKIPPED_FIXERS
    if $(contains "$SKIPPED_FIXERS" "$fixer")
    then
        echo -e "${C_YELLOW}::${C_NC} Skipping fixer '$fixer'"
        continue
    fi
    echo -e "${C_YELLOW}::${C_NC} Running fixer '$fixer'"
    # Silently run the fixer, then commit the result
    python3 -m lib2to3 -f "$fixer" -w -n --no-diff "$TARGET_DIR"
    cd "$TARGET_DIR"
    git commit -a -m "2to3: Run fixer '$fixer'"
    cd "$WORKING_DIR"
    echo -e "${C_GREEN}::${C_NC} Finished running fixer '$fixer'"
done <<< "$fixers"

# Unset the gpgSign config option again
cd "$TARGET_DIR"
git config --local --unset commit.gpgSign
cd "$WORKING_DIR"

echo -e "${C_BLUE}::${C_NC} Done running all fixers"
