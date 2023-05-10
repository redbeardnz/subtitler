#!/usr/local/bin/python3.10

import argparse
import logging
from pathlib import Path

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip


parser = argparse.ArgumentParser(description="Add subtitle from srt file to video.")
parser.add_argument("video", metavar="video",
                    type=Path,
                    help="the video from which subtitle is retrieved")
parser.add_argument("-s", "--subtitle_file", nargs="?",
                    type=Path, required=True,
                    help="path for subtitle srt file")
parser.add_argument("-fs", "--font_size", nargs="?",
                    type=int, default=100,
                    help="font size of subtitle")
parser.add_argument("-v", "--verbose", action="store_true", default=False)
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)


clip = VideoFileClip(str(args.video))
generator = lambda txt: TextClip(txt,
                                 font='WenQuanYi-Micro-Hei',
                                 fontsize=args.font_size,
                                 color='FloralWhite',
                                 method='caption',
                                 size=clip.size,
                                 align='South')
sub = SubtitlesClip(str(args.subtitle_file), generator)
out_video = CompositeVideoClip([clip, sub])
out_video_name = Path.cwd() / f'{args.video.stem}_sub{args.video.suffix}'
out_video.write_videofile(str(out_video_name), audio_codec='aac', fps=clip.fps)
