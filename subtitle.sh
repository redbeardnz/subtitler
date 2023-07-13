#!/bin/bash


ROOT_DIR=$(dirname $(realpath -LP ${0}))
SCRIPT_NAME=$(basename ${0})

function show_usage {
    echo "Usage: ${SCRIPT_NAME} -h   show this help info."
    echo "       ${SCRIPT_NAME} [-v] video"
    echo "${SCRIPT_NAME} add subtitle to video. The subtitle text"
    echo "is retrieved from a srt file with a suffix '.srt' appended"
    echo "to the name of input video"
    echo
    echo "  input:"
    echo "  video          Local file path to video."
    echo
    echo "  output:"
    echo "  video          Output video saved in the same folder as input video with a"
    echo "                 name equaling to video name's stem + .sub + video suffix."
    echo
    echo "  options:"
    echo "  -c font_color   Specify font color of subtitle. The full color list is avaiable"
    echo "                  in github README.md."
    echo "                  Default to FloralWhite."
    echo "  -s font_size    Specify font size of subtitle. The valie range from 1 to 100"
    echo "                  Default to 100."
    echo "  -t stroke_color Specify stroke color of subtitle. The full color list is avaiable"
    echo "                  in github README.md."
    echo "                  Default to black."
    echo "  -w stroke_width Specify stroke width of subtitle. The valie is float"
    echo "                  Default to 0.1."
}


# ### main ###
# show usage by default
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

OPTIONS=''

# Reset in case getopts has been used previously in the shell.
OPTIND=1
while getopts "hvc:s:t:w:" opt; do
    case ${opt} in
        h ) # process option h
            show_usage
            exit 0
            ;;
        v ) # process option v
            OPTIONS="${OPTIONS} -v"
            ;;
        c ) # process option c
            OPTIONS="${OPTIONS} --font_color ${OPTARG}"
            ;;
        s ) # process option s
            OPTIONS="${OPTIONS} --font_size ${OPTARG}"
            ;;
        t ) # process option t
            OPTIONS="${OPTIONS} --stroke_color ${OPTARG}"
            ;;
        w ) # process option w
            OPTIONS="${OPTIONS} --stroke_width ${OPTARG}"
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
VIDEO_NAME_STEM="${VIDEO_NAME%.*}"
VIDEO_NAME_SUFF="${VIDEO_NAME##*.}"
VIDEO_DIR=$(dirname ${VIDEO})
OUTPUT_VIDEO=${VIDEO_DIR}/${VIDEO_NAME_STEM}.sub.${VIDEO_NAME_SUFF}
OUTPUT_VIDEO_NAME=$(basename ${OUTPUT_VIDEO})
SRT_FILE=${VIDEO}.srt
SRT_FILE_NAME=$(basename ${SRT_FILE})
CWD=$(pwd)

# make sure srt file exists
if ! [ -f ${SRT_FILE} ]; then
    echo "${SRT_FILE} does not exist"
    echo "Run asr.sh ${VIDEO} to generate it"
    exit 1
fi

# create an empty output video to be mounted by docker
if ! touch ${OUTPUT_VIDEO}; then
    exit 1
fi

cd ${ROOT_DIR}
docker-compose run --rm -v ${VIDEO}:/video/${VIDEO_NAME}:ro -v ${OUTPUT_VIDEO}:/video/${OUTPUT_VIDEO_NAME} -v ${SRT_FILE}:/subtitle/${SRT_FILE_NAME}:ro subtitler /app/add_subtitle.py ${OPTIONS} -s /subtitle/${SRT_FILE_NAME} -o /output/${OUTPUT_VIDEO_NAME} /video/${VIDEO_NAME}
cd ${CWD}
