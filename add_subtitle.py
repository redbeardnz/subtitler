#!/usr/local/bin/python3.10

import argparse
import logging
import os
from pathlib import Path
import tempfile
from time import perf_counter

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip

# log color
GREEN = '\33[32m'
RESET = '\33[0m'

parser = argparse.ArgumentParser(description="Add subtitle from srt file to video.")
parser.add_argument("video", metavar="video",
                    type=Path,
                    help="the video from which subtitle is retrieved")
parser.add_argument("-o", "--output", nargs="?",
                    type=Path, required=True,
                    help="path for output video")
parser.add_argument("-s", "--subtitle_file", nargs="?",
                    type=Path, required=True,
                    help="path for subtitle srt file")
parser.add_argument("-fs", "--font_size", nargs="?",
                    type=int, default=100,
                    help="font size of subtitle")
parser.add_argument("-fc", "--font_color", nargs="?",
                    type=str, default='FloralWhite',
                    help="font size of subtitle")
parser.add_argument("-sc", "--stroke_color", nargs="?",
                    type=str, default='black',
                    help="stroke color of subtitle")
parser.add_argument("-sw", "--stroke_width", nargs="?",
                    type=float, default=0.1,
                    help="stroke width of subtitle")
parser.add_argument("-v", "--verbose", action="store_true", default=False)
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)


start = perf_counter()
with tempfile.TemporaryDirectory() as tmp_dir:
    os.chdir(tmp_dir)
    clip = VideoFileClip(str(args.video))
    generator = lambda txt: TextClip(txt,
                                     font='WenQuanYi-Micro-Hei',
                                     fontsize=args.font_size,
                                     color=args.font_color,
                                     stroke_color=args.stroke_color,
                                     stroke_width=args.stroke_width,
                                     method='caption',
                                     size=clip.size,
                                     align='South')
    sub = SubtitlesClip(str(args.subtitle_file), generator)
    out_video = CompositeVideoClip([clip, sub])
    out_video_name = args.video.parent / f'{args.video.stem}.sub{args.video.suffix}'
    out_video.write_videofile(str(out_video_name), audio_codec='aac', fps=clip.fps)
end = perf_counter()

logging.info("video is saved to %s, total cost %s seconds",
             GREEN+f'{out_video_name.name}'+RESET,
             GREEN+f'{end-start:.2f}'+RESET)
