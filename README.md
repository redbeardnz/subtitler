# Welcome to Subtitler!

Hello the fellows of **New Federal States of China (NFSC)**.

This repo shows a demo to use AI **ASR** ([whisper](https://github.com/openai/whisper)) to generate subtitle file (.srt), and use [moviepy](https://github.com/Zulko/moviepy) to add subtitles to a video. This demo uses python as programming language.


# Setup
## Install Source Code
- git clone https://github.com/redbeardnz/subtitler.git
- cd subtitler

## whisper
Please follow [whisper setup](https://github.com/openai/whisper#setup)  to setup

## moviepy

 - pip install moviepy

For Chinese subtitle, please follow the instructions in [Dockerfile](https://github.com/redbeardnz/subtitler/blob/master/Dockerfile) to setup Chinese font set.

## Docker
A Dockerfile base on CPU is provided.

### docker image build
- git clone https://github.com/redbeardnz/subtitler.git
- cd subtitler
- docker build -t subtitler .
### run docker container
- docker run -it --name subtitler -h subtitler -v $(pwd):/app subtitler:latest bash

# Run
## Retrive subtitle
You can convert the audio of a video into text and save it as a subtitle **.srt** file. 
- python retrieve.py *{a/path/to/video}*

A **.srt** file will be generated under your current working dir. For example, `python retrieve.py a.mp4` will generate a srt file with name `a.srt`.

## Add subtitle back to video
Then you can add subtitle back to video
- python add_subtitle.py -s *{a/path/to/srt/file}* -fs 100 *{a/path/to/video}*

