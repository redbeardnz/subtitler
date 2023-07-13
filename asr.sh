#!/bin/bash


ROOT_DIR=$(dirname $(realpath -LP ${0}))
SCRIPT_NAME=$(basename ${0})

function show_usage {
    echo "Usage: ${SCRIPT_NAME} -h   show this help info."
    echo "       ${SCRIPT_NAME} [-v] [-m model] [-d model_dir] video"
    echo "${SCRIPT_NAME} converts the speech of a video to text."
    echo "The text is saved in a srt file with a suffix '.srt'"
    echo "appended to the name of input video"
    echo
    echo "  input:"
    echo "  video        Local file path to video."
    echo
    echo "  output:"
    echo "  {video}.srt  Output srt file is saved in the same folder as the input"
    echo "               video with a name equaling to video's name + .srt suffix."
    echo
    echo "  options:"
    echo "  -m model     Specify whisper asr model to use. The full model list is"
    echo "               [tiny.en tiny base.en base small.en small medium.en medium"
    echo "                large-v1 large-v2 large]."
    echo "               Default to small."
    echo "  -d model_dir Specify the location to store whisper models."
    echo "               Default to ${ROOT_DIR}/models."
}


# ### main ###
# show usage by default
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

VERBOSE=''
MODEL=small
MODEL_DIR=${ROOT_DIR}/models

# Reset in case getopts has been used previously in the shell.
OPTIND=1
while getopts "hvm:d:" opt; do
    case ${opt} in
        h ) # process option h
            show_usage
            exit 0
            ;;
        d ) # process option d
            MODEL_DIR=$(realpath -LP ${OPTARG})
            ;;
        m ) # process option m
            MODEL=${OPTARG}
            ;;
        v ) # process option v
            VERBOSE='-v'
            ;;
        \? ) # invalid option
            echo
            show_usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

VIDEO=$(realpath -LP ${1})
VIDEO_NAME=$(basename ${VIDEO})
VIDEO_DIR=$(dirname ${VIDEO})
SRT_FILE=${VIDEO}.srt
SRT_FILE_NAME=$(basename ${SRT_FILE})
CWD=$(pwd)

# create an empty srt file to be mounted by docker
if ! touch ${SRT_FILE}; then
    exit 1
fi

cd ${ROOT_DIR}
docker-compose run --rm -v ${VIDEO}:/video/${VIDEO_NAME}:ro -v ${SRT_FILE}:/output/${SRT_FILE_NAME} -v ${MODEL_DIR}:/models subtitler /app/retrieve.py ${VERBOSE} -m ${MODEL} -md /models /video/${VIDEO_NAME} /output
cd ${CWD}
