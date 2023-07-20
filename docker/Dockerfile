FROM python:3.10-slim

ENV TIKTOKEN_CACHE_DIR='/models'
WORKDIR /app

# install wisper
RUN apt-get -qy update && apt-get install -qy git ffmpeg && \
    pip install -U openai-whisper


# install moviepy
RUN apt install -qy imagemagick fonts-liberation locales ttf-wqy-microhei && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8 && \
    ln -s /etc/fonts/conf.avail/69-language-selector-zh-cn.conf /etc/fonts/conf.d/

ENV LC_ALL C.UTF-8

# RUN pip install matplotlib

# modify ImageMagick policy file so that Textclips work correctly.
RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml 
