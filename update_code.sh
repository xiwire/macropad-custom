#!/bin/sh
# Script for installing a given code to the MacroPad
# Usage:
# ./update.sh <code_name> [<mount_point>]

RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BOLD="\033[1m"
RESET="\033[0m"

logInfo () {
    echo -e "${GREEN}${@}${RESET}"
}
logWarning () {
    echo -e "${YELLOW}${BOLD}${@}${RESET}"
}
logError () {
    echo -e "${RED}${BOLD}${@}${RESET}"
}

if [ -z $1 ]; then
    logError "No code specified. Please specify a code to upload."
    logInfo "Available codes:"
    echo "$(ls codes)"
    exit 1
fi

if [ -z $2 ]; then
    MOUNTED_PATH=$(lsblk -l -o MOUNTPOINTS | grep CIRCUITPY)
else
    MOUNTED_PATH=$2
fi

if [ -z $MOUNTED_PATH ]; then
    log 'No CIRCUITPY drives are mounted'
    exit 1
fi

if [ $(wc -l <<< MOUNTED_PATH) -gt 1 ]; then
    log 'More than one CIRCUITPY drive mounted, please specify one.'
    exit 1
fi

logInfo "Installing ${1} to ${MOUNTED_PATH}"
cp "codes/${1}/code.py" "${MOUNTED_PATH}/code.py"

logInfo "Installed! :D"
