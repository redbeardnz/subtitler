FROM python:3.10-slim

WORKDIR /app
COPY ./requirements.txt ./

# install wisper, easynmt
RUN apt-get -qy update && apt-get install -qy git ffmpeg g++ && \
    pip install -U -r requirements.txt && \
    rm requirements.txt

# whisper tiktok cache
ENV TIKTOKEN_CACHE_DIR=/models/whisper/tiktoken
# EasyNMT cache
ENV TRANSFORMERS_CACHE=/models/transformers
ENV TORCH_CACHE=/models/torch
ENV NLTK_DATA=/models/easynmt/nltk_data

# install moviepy
RUN apt install -qy fonts-liberation locales ttf-wqy-microhei && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8 && \
    ln -s /etc/fonts/conf.avail/69-language-selector-zh-cn.conf /etc/fonts/conf.d/

ENV LC_ALL C.UTF-8
