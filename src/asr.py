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

import nmt


# log color
GREEN = '\33[32m'
RESET = '\33[0m'


if __name__ == "__main__":
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
                        type=Path,
                        default=Path('/models'),
                        help="A dir to save whisper ASR models")
    parser.add_argument("-mt", "--model_translation", nargs="?",
                        choices=list(nmt.models.keys()),
                        default=list(nmt.models.keys())[0],
                        help="model of translation")
    parser.add_argument("-t", "--translate", nargs="?",
                        choices=[
                            "aav", "aed", "af", "alv", "am", "ar", "art", "ase", "az", "bat",
                            "bcl", "be", "bem", "ber", "bg", "bi", "bn", "bnt", "bzs", "ca",
                            "cau", "ccs", "ceb", "cel", "chk", "cpf", "crs", "cs", "csg", "csn",
                            "cus", "cy", "da", "de", "dra", "ee", "efi", "el", "en", "eo", "es",
                            "et", "eu", "euq", "fi", "fj", "fr", "fse", "ga", "gaa", "gil", "gl",
                            "grk", "guw", "gv", "ha", "he", "hi", "hil", "ho", "hr", "ht", "hu",
                            "hy", "id", "ig", "ilo", "is", "iso", "it", "ja", "jap", "ka", "kab",
                            "kg", "kj", "kl", "ko", "kqn", "kwn", "kwy", "lg", "ln", "loz", "lt",
                            "lu", "lua", "lue", "lun", "luo", "lus", "lv", "map", "mfe", "mfs",
                            "mg", "mh", "mk", "mkh", "ml", "mos", "mr", "ms", "mt", "mul", "ng",
                            "nic", "niu", "nl", "no", "nso", "ny", "nyk", "om", "pa", "pag",
                            "pap", "phi", "pis", "pl", "pon", "poz", "pqe", "pqw", "prl", "pt",
                            "rn", "rnd", "ro", "roa", "ru", "run", "rw", "sal", "sg", "sh", "sit",
                            "sk", "sl", "sm", "sn", "sq", "srn", "ss", "ssp", "st", "sv", "sw",
                            "swc", "taw", "tdt", "th", "ti", "tiv", "tl", "tll", "tn", "to",
                            "toi", "tpi", "tr", "trk", "ts", "tum", "tut", "tvl", "tw", "ty",
                            "tzo", "uk", "umb", "ur", "ve", "vi", "vsl", "wa", "wal", "war",
                            "wls", "xh", "yap", "yo", "yua", "zai", "zh", "zne"],
                        default=None,
                        help="the target language of translation")
    parser.add_argument("-ks", "--keep_source", action="store_true", default=False,
                        help="subtitle contain both original language and tranlated language")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    start = perf_counter()
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(name=args.model,
                               download_root=str(args.model_dir.resolve()/'whisper'),
                               device=DEVICE)

    logging.debug(f"transcribing {args.video} ...")
    transcription = model.transcribe(audio=args.video, fp16=False)

    if args.translate is not None:
        transcription = nmt.translation(transcription=transcription,
                                        model_translation=args.model_translation,
                                        model_dir=args.model_dir.resolve()/'easynmt',
                                        target_lang=args.translate,
                                        keep_source=args.keep_source)

    srt_file = args.video + '.srt'
    logging.debug(f"generating {Path(srt_file).name} ...")
    writer = WriteSRT(args.srt_dir)
    writer(transcription, srt_file)

    end = perf_counter()
    logging.info("subtitle is saved to %s, total cost %s seconds",
                 GREEN+f'{Path(srt_file).name}'+RESET,
                 GREEN+f'{end-start:.2f}'+RESET)

    sys.exit()
