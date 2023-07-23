#! /bin/bash

ROOT_DIR=$(dirname $(realpath ${0}))

mkdir -p ~/bin && \
    ln -s ${ROOT_DIR}/scripts/asr.sh ~/bin/ && \
    ln -s ${ROOT_DIR}/scripts/batch_asr.sh ~/bin/ && \
    ln -s ${ROOT_DIR}/scripts/subtitle.sh ~/bin/ && \
    ln -s ${ROOT_DIR}/scripts/batch_subtitle.sh ~/bin/ && \
    echo 'PATH=$PATH:~/bin' >> ~/.bashrc
