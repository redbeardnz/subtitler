#!/usr/local/bin/python3.10

import argparse
import logging
from pathlib import Path
import torch
import whisper
from whisper.utils import WriteSRT


parser = argparse.ArgumentParser(description="Generate subtitle srt file from video.")
parser.add_argument("video", metavar="video",
                    help="the video from which subtitle is retrieved")
parser.add_argument("-v", "--verbose", action="store_true", default=False)
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model(name="small", device=DEVICE)

logging.debug(f"transcribing {args.video} ...")
transcription = model.transcribe(audio=args.video, fp16=False)

writer = WriteSRT(Path.cwd())
writer(transcription, args.video)
logging.debug(f"subtitle is saved to {Path.cwd()}/{Path(args.video).stem}.srt")
