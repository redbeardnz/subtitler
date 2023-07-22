#!/bin/bash

ROOT_DIR=$(dirname $(dirname $(realpath -LP ${0})))
SCRIPT_NAME=$(basename ${0})

function show_usage {
    echo "Usage: ${SCRIPT_NAME} [-h] show this help info."
    echo "       ${SCRIPT_NAME} [-v] video [style options]"
    echo "${SCRIPT_NAME} add subtitle to video. The subtitle text"
    echo "is retrieved from a srt file with a suffix '.srt' appended"
    echo "to the name of input video"
    echo
    echo "  input:"
    echo "  video     Local file path to video."
    echo
    echo "  output:"
    echo "  video     Output video saved in the same folder as input video with a"
    echo "            name equaling to video name's stem + .sub + video suffix."
    echo
    echo "  options:"
    echo "  -h        Show this help info."
    echo "  -v        Show more verbose log."
    echo
    echo "  style options:"
    echo "  -fs, --font_size <size>     Size of font. Default 16."
    echo "  -fc, --font_color <color>   RGB Color of font. Default FFFFFF (white)."
    echo "  -ft, --font_transparency <transparency>"
    echo "                              Transparency of font (0 ~ 100). Default 0."
    echo "  -ow, --outline_width <width>"
    echo "                              Width of font outline, in pixels. Default 1."
    echo "                              In box border_style, it's the width of box."
    echo "  -oc, --outline_color <color>"
    echo "                              RGB Color of font outline. Default 000000 (black)."
    echo "  -ot, --outline_transparency <transparency>"
    echo "                              Transparency of font outline (0 ~ 100). Default 0."
    echo "  -sd, --shadow_depth <depth> Depth of the font shadow, in pixels. Default 1."
    echo "  -sc, --shadow_color <color> RGB Color of font shadow. Default 000000 (black)."
    echo "  -st, --shadow_transparency <transparency>"
    echo "                              Transparency of font shadow (0 ~ 100). Default 0."
    echo "  -bl, --bold                 Enable bold font."
    echo "  -il, --italic               Enable italic font."
    echo "  -ul, --underline            Enable font underline."
    echo "  -so, --strikeout            Enable font strikeout."
    echo "  -bs, --border_style <border_style>"
    echo "                              border_style: shadow, box, rectangle. Default shadow."
    echo "                              shadow: font with shadow."
    echo "                              box: each subtitle line is embedded in one box."
    echo "                              rectangle: subtitle lines are embedded in a rectangle."
    echo "  -al, --alignment <align>    align: 'bottom_left', 'bottom_center', 'bottom_right'"
    echo "                                     'center_left', 'center_center', 'center_right'"
    echo "                                     'top_left',    'top_center',    'top_right'"
    echo "                              Default 'bottom_center'"
    echo "  -ag, --angle <angle>        Angle (float) of the subtitle, in degree. Default 0.0."
    echo "  -sp, --spacing <spacing>    Extra space (in pixels) between characters. Default 0."
    echo "  -ml, --margin_left <margin> Margin from subtitle to video left border. Default 0."
    echo "  -mr, --margin_right <margin>"
    echo "                              Margin from subtitle to video right border. Default 0."
    echo "  -mv, --margin_vertical <margin>"
    echo "                              Margin from subtitle to video top/bottom border."
    echo "                              Default 0."
    echo "  -sx, --scalex <scale>       Modifies the width of the font by scale (float)."
    echo "                              Default 1.0."
    echo "  -sy, --scaley <scale>       Modifies the height of the font by scale (float)."
    echo "                              Default 1.0."
    echo "  -qa, --quality <quality>    quality: ultrahigh, high, standard, fast, ultrafast"
    echo "                              The quality of output video."
    echo "                              Default standard."
    echo
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
#while getopts "hvc:s:t:w:" opt; do
while getopts "hv" opt; do
    case ${opt} in
        h ) # process option h
            show_usage
            exit 0
            ;;
        v ) # process option v
            OPTIONS="-v"
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
shift
OPTIONS="${OPTIONS} ${@}"

VIDEO_NAME=$(basename ${VIDEO})
VIDEO_NAME_STEM="${VIDEO_NAME%.*}"
VIDEO_NAME_SUFF="${VIDEO_NAME##*.}"
VIDEO_DIR=$(dirname ${VIDEO})
OUTPUT_VIDEO_NAME=${VIDEO_NAME_STEM}.sub.${VIDEO_NAME_SUFF}
OUTPUT_VIDEO=${VIDEO_DIR}/${OUTPUT_VIDEO_NAME}
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
docker-compose -f docker/docker-compose.yml run --rm -v ${VIDEO}:/video/${VIDEO_NAME}:ro -v ${OUTPUT_VIDEO}:/video/${OUTPUT_VIDEO_NAME} -v ${SRT_FILE}:/subtitle/${SRT_FILE_NAME}:ro subtitler /app/add_subtitle.py ${OPTIONS} -s /subtitle/${SRT_FILE_NAME} /video/${VIDEO_NAME} /video/${OUTPUT_VIDEO_NAME}
cd ${CWD}
