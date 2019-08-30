#!/bin/bash

# Script to check all Python scripts for PEP-8 issues

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

IFS=$'\n'

# list of directories with sources to check
directories=$(cat ${SCRIPT_DIR}/directories.txt)

# list of separate files to check
separate_files=$(cat ${SCRIPT_DIR}/files.txt)

pass=0
fail=0

# set up terminal colors
NORMAL=$(tput sgr0)
RED=$(tput bold && tput setaf 1)
GREEN=$(tput bold && tput setaf 2)
YELLOW=$(tput bold && tput setaf 3)

function prepare_venv() {
    # we want tests to run on python3.6
    printf 'checking alias `python3.6` ... ' >&2
    PYTHON=$(which python3.6 2> /dev/null)
    if [ "$?" -ne "0" ]; then
        printf "%sNOT FOUND%s\n" "${YELLOW}" "${NORMAL}" >&2

        printf 'checking alias `python3` ... ' >&2
        PYTHON=$(which python3 2> /dev/null)

        let ec=$?
        [ "$ec" -ne "0" ] && printf "${RED} NOT FOUND ${NORMAL}\n" && return $ec
    fi

    printf "%sOK%s\n" "${GREEN}" "${NORMAL}" >&2

    ${PYTHON} -m venv "venv" && source venv/bin/activate && python -m pip install pyflakes
}

pushd "${SCRIPT_DIR}/.."

# run the pyflakes for all files that are provided in $1
function check_files() {
    for source in $1
    do
        echo "$source"
        python -m pyflakes "$source"
        if [ $? -eq 0 ]
        then
            echo "    Pass"
            let "pass++"
        elif [ $? -eq 2 ]
        then
            echo "    Illegal usage (should not happen)"
            exit 2
        else
            echo "    Fail"
            let "fail++"
        fi
    done
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

echo "----------------------------------------------------"
echo "Checking source files for common errors in following"
echo "directories:"
echo "$directories"
echo "----------------------------------------------------"
echo

# checks for the whole directories
for directory in $directories
do
    files=$(find "$directory" -path "$directory/venv" -prune -o -name '*.py' -print)

    check_files "$files"
done

echo "----------------------------------------------------"
echo "Checking following source files for common errors:"
echo "$separate_files"
echo "----------------------------------------------------"
echo

check_files "$separate_files"

popd

if [ $fail -eq 0 ]
then
    echo "All checks passed for $pass source files"
else
    let total=$pass+$fail
    echo "$fail source files out of $total files needs to be checked and fixed"
    exit 1
fi

