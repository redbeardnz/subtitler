#!/bin/bash

ROOT_DIR=$(dirname $(dirname $(realpath ${0})))
SCRIPT_NAME=$(basename ${0})

function show_usage {
    echo "Usage: ${SCRIPT_NAME} -h"
    echo "       ${SCRIPT_NAME} [-i] [-g glossary_file] ... video [asr options]"
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
    echo "  -g <glossary_file>"
    echo "               Specify glossary file for translation."
    echo "               Use this option multiple times to specify multiple glossary files"
    echo "  -i           Enable network. By default network is disabled."
    echo "               '-i' must be specified when you need download AI model."
    echo "  -h           Show this help info."
    echo
    echo "  asr options:"
    echo "  -m, --model <asr_model>"
    echo "               asr_model is the whisper model to use. The full whisper model list is"
    echo "               [tiny.en tiny base.en base small.en small medium.en medium"
    echo "                large-v1 large-v2 large]."
    echo "               Default to small."
    echo "  -mt, --model_translation <model_translation>"
    echo "               model_translation specify neural translation model to use."
    echo "               The full model list is [small, large]"
    echo "               Default to small."
    echo "  -t, --translate <language_code>"
    echo "               language_code specify the target language to translate."
    echo "               The full language code list is:"
    echo "               [aav, aed, af, alv, am, ar, art, ase, az, bat, bcl, be, bem, ber, bg,"
    echo "                bi, bn, bnt, bzs, ca, cau, ccs, ceb, cel, chk, cpf, crs, cs, csg, csn,"
    echo "                cus, cy, da, de, dra, ee, efi, el, en, eo, es, et, eu, euq, fi, fj,"
    echo "                fr, fse, ga, gaa, gil, gl, grk, guw, gv, ha, he, hi, hil, ho, hr, ht,"
    echo "                hu, hy, id, ig, ilo, is, iso, it, ja, jap, ka, kab, kg, kj, kl, ko,"
    echo "                kqn, kwn, kwy, lg, ln, loz, lt, lu, lua, lue, lun, luo, lus, lv, map,"
    echo "                mfe, mfs, mg, mh, mk, mkh, ml, mos, mr, ms, mt, mul, ng, nic, niu, nl,"
    echo "                no, nso, ny, nyk, om, pa, pag, pap, phi, pis, pl, pon, poz, pqe, pqw,"
    echo "                prl, pt, rn, rnd, ro, roa, ru, run, rw, sal, sg, sh, sit, sk, sl, sm,"
    echo "                sn, sq, srn, ss, ssp, st, sv, sw, swc, taw, tdt, th, ti, tiv, tl, tll,"
    echo "                tn, to, toi, tpi, tr, trk, ts, tum, tut, tvl, tw, ty, tzo, uk, umb,"
    echo "                ur, ve, vi, vsl, wa, wal, war, wls, xh, yap, yo, yua, zai, zh, zne]"
    echo "               See project Appendix for mapping from language name to language code."
    echo "               Default: no translation."
    echo "  -ks, --keep_source"
    echo "               if this option is specified, srt contains both original and translated"
    echo "               lanugages. if not specified, srt contains only the translated language."
    echo "  -v, --verbose"
    echo "               Show detailed log."
    echo "  -vv, --verbose_more"
    echo "               Show more detailed log."
    echo
}


# ### main ###
# show usage by default
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

MODEL_DIR=${ROOT_DIR}/models
NET_ENABLED=false
GLOSSARIES_DOCKER_MOUNT=''
GLOSSARIES_OPT=''

# Reset in case getopts has been used previously in the shell.
OPTIND=1
while getopts "g:hi" opt; do
    case ${opt} in
        g ) # process option g
            GLOSSARY_PATH=$(realpath ${OPTARG})
            GLOSSARY_FILENAME=$(basename ${GLOSSARY_PATH})
            GLOSSARIES_DOCKER_MOUNT="${GLOSSARIES_DOCKER_MOUNT} -v ${GLOSSARY_PATH}:/glossary/${GLOSSARY_FILENAME}:ro"
            if [ -z "${GLOSSARIES_OPT}" ]; then
                GLOSSARIES_OPT="-g /glossary/${GLOSSARY_FILENAME}"
            else
                GLOSSARIES_OPT="${GLOSSARIES_OPT},/glossary/${GLOSSARY_FILENAME}"
            fi
            ;;
        h ) # process option h
            show_usage
            exit 0
            ;;
        i ) # process option i
            NET_ENABLED=true
            ;;
        \? ) # invalid option
            echo
            show_usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

VIDEO=$(realpath ${1})
shift
OPTIONS=${@}

VIDEO_NAME=$(basename ${VIDEO})
VIDEO_DIR=$(dirname ${VIDEO})
SRT_FILE=${VIDEO}.srt
SRT_FILE_NAME=$(basename ${SRT_FILE})
DOCER_SERVICE=subtitler
CWD=$(pwd)

# create an empty srt file to be mounted by docker
if ! touch ${SRT_FILE}; then
    exit 1
fi

if ${NET_ENABLED}; then
    DOCER_SERVICE=${DOCER_SERVICE}-with-net
fi

cd ${ROOT_DIR}
docker-compose -f docker/docker-compose.yml run --rm -v ${VIDEO}:/video/${VIDEO_NAME}:ro -v ${SRT_FILE}:/output/${SRT_FILE_NAME} -v ${MODEL_DIR}:/models ${GLOSSARIES_DOCKER_MOUNT} ${DOCER_SERVICE} /app/asr.py ${OPTIONS} ${GLOSSARIES_OPT} /video/${VIDEO_NAME} /output
cd ${CWD}
