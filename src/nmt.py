import warnings
warnings.simplefilter('ignore', category=UserWarning)

from easynmt import EasyNMT
import nltk
from pathlib import Path

# translation model map
models = {"small": 'opus-mt', "large": 'm2m_100_1.2B'}


def translation(transcription: dict,
                model_translation: str,
                model_dir: Path,
                target_lang: str,
                keep_source: bool):
    if transcription["language"] == target_lang:
        return transcription
    # download nltk punkt
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', download_dir=str(model_dir/'nltk_data'))
    # load nmt model
    nmt = EasyNMT(model_name=models[model_translation], cache_folder=str(model_dir))
    texts = [seg["text"] for seg in transcription["segments"]]
    texts = nmt.translate(documents=texts, target_lang=target_lang)
    for seg in transcription["segments"]:
        original_text = seg["text"].strip()
        translated_text = texts[seg["id"]].strip()
        if keep_source:
            seg["text"] = f'{translated_text}\n{original_text}'
        else:
            seg["text"] = translated_text
    return transcription
