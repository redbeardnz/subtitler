#!/usr/local/bin/python3.10

# suppress numba jit nopython warnings which is caused by whisper function definition
from numba.core.errors import NumbaDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)


import argparse
import logging
from pathlib import Path
import sys
from time import perf_counter
import torch
import whisper
from whisper.utils import WriteSRT

# log color
GREEN = '\33[32m'
RESET = '\33[0m'

parser = argparse.ArgumentParser(description="Generate subtitle srt file from video.")
parser.add_argument("video", metavar="video",
                    help="the video from which subtitle is retrieved")
parser.add_argument("srt_dir", metavar="srt_dir",
                    help="the path of dir to save output subtitle file")
parser.add_argument("-m", "--model", nargs="?",
                    choices=["tiny.en", "tiny", "base.en", "base", "small.en", "small",
                             "medium.en", "medium", "large-v1", "large-v2", "large"],
                    default="small",
                    help="Whisper ASR model")
parser.add_argument("-md", "--model_dir", nargs="?",
                    default=None,
                    help="A dir to save whisper ASR models")
parser.add_argument("-v", "--verbose", action="store_true", default=False)
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

start = perf_counter()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model(name=args.model, download_root=args.model_dir, device=DEVICE)

logging.debug(f"transcribing {args.video} ...")
transcription = model.transcribe(audio=args.video, fp16=False)

srt_file = args.video + '.srt'
logging.debug(f"generating {Path(srt_file).name} ...")
writer = WriteSRT(args.srt_dir)
writer(transcription, srt_file)

end = perf_counter()
logging.info("subtitle is saved to %s, total cost %s seconds",
             GREEN+f'{Path(srt_file).name}'+RESET,
             GREEN+f'{end-start:.2f}'+RESET)

sys.exit()
