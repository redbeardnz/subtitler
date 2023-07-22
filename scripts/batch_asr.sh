#!/bin/bash

ROOT_DIR=$(dirname $(dirname $(realpath -LP ${0})))
SCRIPT_NAME=$(basename ${0})

function show_usage {
    echo
    echo "Usage: ${SCRIPT_NAME} -h   show this help info."
    echo "       ${SCRIPT_NAME} [asr options] video_list_file"
    echo "${SCRIPT_NAME} is a wrapper of asr.sh to process videos in a batch."
    echo "The input video_list_file contains one or more videos' paths saved"
    echo "as one path per-line. asr.sh is called one by one against these paths."
    echo "All options of ${SCRIPT_NAME} are sent transparently to asr.sh."
    echo
    echo "  input:"
    echo "  video_list_file   A text file list multiple videos' pathes, one path per line."
    echo
}

OPTIONS=""
# Reset in case getopts has been used previously in the shell.
OPTIND=1
while getopts "hvm:d:" opt; do
    case ${opt} in
        h ) # process option h
            show_usage
            exit 0
            ;;
        * ) # save all options
            OPTIONS="${OPTIONS} -${opt} ${OPTARG}"
            ;;
    esac
done
shift $((OPTIND-1))

####################
####    main    ####
####################
INPUT_FILE=$(realpath -LP ${1})
INPUT_FILE_DIR=$(dirname ${INPUT_FILE})
CWD=$(pwd)


START=$(date +%s)
VIDEO_PATHS=""
while read -r path;
do
    VIDEO_PATHS="${VIDEO_PATHS} ${path}"
done < ${INPUT_FILE}

cd ${INPUT_FILE_DIR}
for path in ${VIDEO_PATHS};
do
    asr.sh ${OPTIONS} ${path}
done
cd ${CWD}
END=$(date +%s)
COST=$((${END}-${START}))

GREEN='\033[0;32m'
RESET='\033[0m'
printf "${SCRIPT_NAME} cost:  ${GREEN}$((${COST} / 3600))${RESET}hrs ${GREEN}$(((${COST} / 60) % 60))${RESET}min ${GREEN}$((${COST} % 60))${RESET}sec"
