#!/usr/local/bin/python3.10

import warnings
warnings.simplefilter('ignore', category=UserWarning)

from easynmt import EasyNMT
from functools import partial
import logging
import nltk
from pandas import concat, read_csv
from pathlib import Path
import re
from typing import List, Union

# translation model map
models = {"small": 'opus-mt', "large": 'm2m_100_1.2B'}


'''
>>> from pandas import read_csv, concat
>>> from pathlib import Path
>>> a = read_csv('/tmp/1.csv')
>>> b = read_csv('/tmp/2.csv')
>>> c = concat([a, b], ignore_index=True).fillna('')
>>> c
      en        zh      ja
0    FDA  食品和药物管理局  食品医薬品局
1  COVID      新冠病毒    コビッド
2    DOJ       司法部
3    CIA     中央情报局
>>>

 r = re.compile(r'zzz(\d+)zzz')

 r.sub('hello', 'This is the zzz1zzz reporting system and how many deaths were reported to zzz1zzz by year.')
def func(matchobj):
...     print(matchobj.group(1))
...     return f'@{matchobj.group(1)}@'

r.sub(func, 'This is the zzz1zzz reporting system and how many deaths were reported to zzz2zzz by year.')
'''

class NMT:

    # magics of source language
    MAGICS = {'en': 'zzz{loc}zzz', 'zh': '@{loc}@'}
    MAGIC_REX = {'en': re.compile(r'zzz(\d+)zzz'), 'zh': re.compile(r'@(\d+)@')}
    NONE_REX = re.compile(r'$^')

    def __init__(self,
                 model_name: str = 'small',
                 model_dir: Path = Path('/models/easynmt'),
                 glossaries: Union[Path, List[Path]] = None,
    ):
        self._model_name = model_name
        logging.info(f'Loading neural machine translation model {model_name}')
        self._model = EasyNMT(model_name=models[model_name], cache_folder=str(model_dir))
        if glossaries is not None:
            if isinstance(glossaries, Path):
                glossaries = [glossaries]
            self._glossary = concat([read_csv(f) for f in glossaries], ignore_index=True).fillna('')
        else:
            self._glossary = None
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', download_dir=str(model_dir/'nltk_data'))


    def translate(self, documents: Union[str, List[str]], target_lang: str):
        if isinstance(documents, str):
            documents = [documents]
        encoded = self._encode_glossary(documents, target_lang=target_lang)
        translated = self._model.translate(documents=[text for _, text in encoded],
                                           target_lang=target_lang,
                                           show_progress_bar=True)
        translated = list(zip([lang for lang, _ in encoded], translated))
        documents = self._decode_glossary(translated, target_lang=target_lang)
        return documents


    def _encode_glossary(self, documents: List[str], target_lang: str):
        encoded_documents = []
        # if self._glossary is None or target_lang not in self._glossary.columns:
        #     return documents
        logging.info(f'encoding glossary, target_lang: {target_lang}')
        for text in documents:
            source_lang = self._model.language_detection(text)
            if self._glossary is not None \
               and source_lang != target_lang \
               and source_lang in self._glossary.columns \
               and source_lang in self.MAGICS.keys() \
               and target_lang in self._glossary.columns:
                for i, term in enumerate(self._glossary[source_lang]):
                    # embed magics to text
                    text = text.replace(term, self.MAGICS[source_lang].format(loc=i))
                logging.debug(f'golossary embeded text: {text}')
            encoded_documents.append((source_lang, text))
        return encoded_documents


    def _decode_glossary(self, documents: list, target_lang: str):
        decoded_documents = []
        # if self._glossary is None or target_lang not in self._glossary.columns:
        #     return documents
        logging.info(f'decoding glossary, target_lang: {target_lang}')
        for source_lang, text in documents:
            if self._glossary is not None and target_lang in self._glossary.columns:
                rex = self.MAGIC_REX.get(source_lang, self.NONE_REX)
                text = rex.sub(partial(self._rex_replace, target_lang), text)
                logging.debug(f'glossary decoded text: {text}')
            decoded_documents.append(text)
        return decoded_documents


    def _rex_replace(self, target_lang: str, match):
        return self._glossary[target_lang][int(match.group(1))]


if __name__ == "__main__":
    """
    example:
    nmt.py -m large -g glossary.csv "This is the VAERS reporting system and how many deaths were reported to VAERS by year."
    """

    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Translate text by Neural machine translation.")
    parser.add_argument("text", metavar="text",
                        help="the text to translate")
    parser.add_argument("-m", "--model", nargs="?",
                        choices=list(models.keys()),
                        default=list(models.keys())[0],
                        help="the model name of Neural machine translation")
    parser.add_argument("-md", "--model_dir", nargs="?",
                        type=Path,
                        default=Path('/models'),
                        help="A dir to save nmt models")
    parser.add_argument("-g", "--glossary", nargs="?",
                        type=lambda l : [Path(p) for p in l.split(',')],
                        default=None,
                        help="the glossary file list seperated by comma")
    parser.add_argument("-t", "--target_lang", nargs="?",
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
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-vv", "--verbose_more", action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose_more:
        logging.getLogger().setLevel(logging.DEBUG)

    nmt = NMT(model_name=args.model,
              model_dir=args.model_dir/'easynmt',
              glossaries=args.glossary)
    documents = nmt.translate(documents=args.text, target_lang=args.target_lang)
    for doc in documents:
        print(doc)
    sys.exit()
