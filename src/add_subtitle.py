#!/usr/local/bin/python3.10

import argparse
import json
import logging
# from matplotlib import colors
import os
from pathlib import Path
import subprocess
import tempfile
from time import perf_counter

# from moviepy.editor import *
# from moviepy.video.tools.subtitles import SubtitlesClip
# from moviepy.video.io.VideoFileClip import VideoFileClip

# log color
GREEN = '\33[32m'
RESET = '\33[0m'

class Subtitle:
    # ffprobe command
    _FFPROBE = 'ffprobe' \
        ' -select_streams v:0' \
        ' -show_entries stream=codec_name,pix_fmt,color_transfer,color_primaries' \
        ' -of default=noprint_wrappers=1' \
        ' -print_format json' \
        ' {video}'

    # refer to http://www.tcax.org/docs/ass-specs.htm
    _SUBTITLE_ASS_STYLE = 'Fontname={font_name}' \
        ',Fontsize={font_size}' \
        ',PrimaryColour=&H{font_transparency:02X}{font_color}&' \
        ',Outline={outline_width}' \
        ',OutlineColour=&H{outline_transparency:02X}{outline_color}&' \
        ',Shadow={shadow_depth}' \
        ',BackColour=&H{shadow_transparency:02X}{shadow_color}&' \
        ',BorderStyle={border_style}' \
        ',Bold={bold}' \
        ',Italic={italic}' \
        ',Underline={underline}' \
        ',Strikeout={strikeout}' \
        ',Alignment={alignment}' \
        ',Angle={angle}' \
        ',Spacing={spacing}' \
        ',MarginL={margin_left}' \
        ',MarginR={margin_right}' \
        ',MarginV={margin_vertical}' \
        ',ScaleX={scalex}' \
        ',ScaleY={scaley}'

    # quality is ffmpeg crf. 0 lossless ~ 51 wrost
    _FFMPEG_QUALITY = {"standard": 23, "ultrahigh": 0, "high": 16, "fast": 31, "ultrafast": 51}
    _FFMPEG_SDR = 'ffmpeg -y' \
        ' -i {input_video_path}' \
        ' -vf "subtitles={srt_path}:force_style=\'{ass_style}\'"' \
        ' -crf {quality}' \
        ' {output_video_path}'
    # the tag hvc1 comes from
    # https://discussions.apple.com/thread/253813055?answerId=257147397022#257147397022
    _FFMPEG_HDR = 'ffmpeg -y' \
        ' -i {input_video_path}' \
        ' -vf "subtitles={srt_path}:force_style=\'{ass_style}\'"' \
        ' -crf {quality}' \
        ' -vcodec hevc -tag:v hvc1' \
        ' {output_video_path}'

    ALIGNMENT = {"bottom_left": 0b0001, "bottom_center": 0b0010, "bottom_right": 0b0011,
                 "top_left":    0b0101, "top_center":    0b0110, "top_right":    0b0111,
                 "center_left": 0b1001, "center_center": 0b1010, "center_right": 0b1011,
    }

    # border_style: 4 is added by
    # https://github.com/libass/libass/blob/d1f0f20bfa98864cd2aaf931f144909d319545aa/Changelog#L142
    BORDER_STYLE = {"shadow": 1, "box": 3, "rectangle": 4}

    # default style values
    DEFAULT_STYLE = {
        "font_size": 16, "font_color": 'FFFFFF', "font_transparency": 0,
        "outline_width": 1, "outline_color": '000000', "outline_transparency": 0,
        "shadow_depth": 1, "shadow_color": '000000', "shadow_transparency": 0,
        "bold": False, "italic": False, "underline": False, "strikeout": False,
        "border_style": "shadow", "alignment": "bottom_center", "angle": 0.0, "spacing": 0,
        "margin_left": 0, "margin_right": 0, "margin_vertical": 0, "scalex": 1, "scaley": 1,
    }

    def __init__(self, video: Path, srt: Path, **kwargs):
        """
        kwargs parameters:
        font_name: str
            The subtitle font as identified by operating systems.
        font_size: int
            The point size of the font.
            Default to 16
        font_color: str
            The font color. See README.md appendix for full color name list.
            Default to white
        font_transparency: int
            The transparency of the font. Its value range from 0 to 100.
            Default to 0
        outline_width: int
            The width of the text outline, in pixels. In box border_style, it's the width of box.
            Default to 1
        outline_color: str
            The color used to outline the font, or if border_style=="box" or
            border_style=="rectangle", it's the color of the opaque box). See README.md
            appendix for full color name list.
            Default to black
        outline_transparency: int
            The transparency of the text outline. Its value range from 0 to 100.
            Default to 0
        shadow_depth: int
            The depth of the text shadow, in pixels.
            Default to 1
        shadow_color: str
            The color of the subtitle shadow or if border_style=="box" or
            border_style=="rectangle", it's the color of the opaque box). See README.md
            appendix for full color name list.
            Default to black
        shadow_transparency: int
            The transparency of the text shadow. Its value range from 0 to 100.
            Default to 0
        bold: bool
            True: enalbe bold font, False: disable bold font
            Default to False
        italic: bool
            True: enalbe italic font, False: disable italic font
            Default to False
        underline: bool
            True: enable font underline, False: disable font underline
            Default to False
        strikeout: bool
            True: enable font strikeout, False: disable font strikeout
            Default to False
        border_style: str
            shadow (default), box, or rectangle
        alignment: str
            The position and alignment of subtitle.
            Accepted values: "bottom_left", "bottom_center", "bottom_right",
                             "center_left", "center_center", "center_right",
                             "top_left",    "top_center",    "top_right".
            Default to "bottom_center"
        angle: float
            The angle of subtitle in degree.
            Default to 0.0 degree
        spacing: int
            Extra space (in pixels) between characters.
            Default to 0
        margin_left: int
            The margin between subtitle and video left border.
            Default to 0
        margin_right: int
            The margin between subtitle and video right border.
            Default to 0
        margin_vertical: int
            The margin between subtitle and video top or bottom border.
            Default to 0
        scalex: float
            Modifies the width of the font.
            Default to 1
        scaley: float
            Modifies the height of the font.
            Default to 1
        """

        if kwargs.get("border_style", "shadow") not in self.BORDER_STYLE:
            raise ValueError(f'border_style [{kwargs.get("border_style", "shadow")}] is not supported')
        if kwargs.get("alignment", "bottom_center") not in self.ALIGNMENT:
            raise ValueError(f'alignment [{kwargs.get("alignment", "bottom_center")}] is not supported')

        self.style = self.DEFAULT_STYLE
        self.style.update(kwargs)
        self.style["font_color"] = self._rgb_to_bgr(self.style["font_color"])
        self.style["font_transparency"] = self._transparency(self.style["font_transparency"])
        self.style["outline_color"] = self._rgb_to_bgr(self.style["outline_color"])
        self.style["outline_transparency"] = self._transparency(self.style["outline_transparency"])
        self.style["shadow_color"] = self._rgb_to_bgr(self.style["shadow_color"])
        self.style["shadow_transparency"] = self._transparency(self.style["shadow_transparency"])
        self.style["border_style"] = self.BORDER_STYLE[self.style["border_style"]]
        self.style["alignment"] = self.ALIGNMENT[self.style["alignment"]]
        self.style["bold"] = -1 if self.style["bold"] else 0
        self.style["italic"] = -1 if self.style["italic"] else 0
        self.style["underline"] = -1 if self.style["underline"] else 0
        self.style["strikeout"] = -1 if self.style["strikeout"] else 0

        self.video_info = self._prob_video_info(video)
        self._video_quality = self._FFMPEG_QUALITY[kwargs.get("quality", "standard")]
        self._video = video
        self._srt = srt


    def write_to_file(self, file_path: Path):
        ass_style = self._SUBTITLE_ASS_STYLE.format(**self.style)
        if self.video_info["codec_name"].lower() in ['hevc', 'h265']:
            # for hdr, another solution:
            # codec='libx264',
            # '-color_trc', video_info["color_transfer"],
            # '-color_primaries', video_info["color_primaries"],
            # '-pix_fmt', video_info["pix_fmt"]],
            cmd_pattern = self._FFMPEG_HDR
        else:
            cmd_pattern = self._FFMPEG_SDR
        cmd = cmd_pattern.format(input_video_path=self._video,
                                 srt_path=self._srt,
                                 ass_style=ass_style,
                                 quality=self._video_quality,
                                 output_video_path=file_path)
        logging.debug(cmd)
        try:
            p = subprocess.run(cmd, shell=True, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            msg = e.stderr.decode("utf-8").strip()
            logging.error(f"ffmpeg returns {e.returncode}, console [{msg}]")
            return False
        except Exception as e:
            logging.error(f"exception in ffmpeg. e={repr(e)}")
            return False


    def _rgb_to_bgr(self, rgb: str):
        # rgb_hex -> bgr_hex
        # example: 'xkcd:pink' -> 'FF81C0' -> 'C081FF'
        #          'pink'      -> 'FFC0CB' -> 'CBC0FF
        rgb = rgb.upper()
        return f'{rgb[4:6]}{rgb[2:4]}{rgb[0:2]}'


    def _transparency(self, transparency: int):
        # map transparency to 0 ~ 255
        if transparency < 0:
            transparency = 0
        elif transparency > 100:
            transparency = 100
        return int(transparency * 255 / 100)


    def _prob_video_info(self, video: Path):
        cmd = self._FFPROBE.format(video=video)
        try:
            p = subprocess.run(cmd, shell=True, capture_output=True, check=True)
            ffprobe_ret = json.loads(p.stdout.decode("utf-8").strip())
            return ffprobe_ret["streams"][0]
        except subprocess.CalledProcessError as e:
            msg = e.stderr.decode("utf-8").strip()
            logging.error(f"ffprobe returns {e.returncode}, console [{msg}]")
            return None
        except Exception as e:
            logging.error(f"exception in ffprobe. e={repr(e)}")
            return None



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Add subtitle from srt file to video.")
    parser.add_argument("video", metavar="video",
                        type=Path,
                        help="the original video")
    parser.add_argument("output", metavar="output",
                        type=Path,
                        help="path of generated video")
    parser.add_argument("-s", "--srt", nargs="?",
                        type=Path, required=True,
                        help="path for subtitle srt file")

    parser.add_argument("-fs", "--font_size", nargs="?",
                        type=int, default=16,
                        help="size of font")
    parser.add_argument("-fc", "--font_color", nargs="?",
                        type=str, default='FFFFFF',
                        help="RGB color hex of font")
    parser.add_argument("-ft", "--font_transparency", nargs="?",
                        type=int, default=0,
                        help="transparency of font")

    parser.add_argument("-ow", "--outline_width", nargs="?",
                        type=int, default=1,
                        help="width of font outline, in pixels. In box border_style, it's the width of box.")
    parser.add_argument("-oc", "--outline_color", nargs="?",
                        type=str, default='000000',
                        help="RGB color hex of font outline")
    parser.add_argument("-ot", "--outline_transparency", nargs="?",
                        type=int, default=0,
                        help="transparency of font outline")

    parser.add_argument("-sd", "--shadow_depth", nargs="?",
                        type=int, default=1,
                        help="depth of the font shadow, in pixels")
    parser.add_argument("-sc", "--shadow_color", nargs="?",
                        type=str, default='000000',
                        help="RGB color hex of font shadow")
    parser.add_argument("-st", "--shadow_transparency", nargs="?",
                        type=int, default=0,
                        help="transparency of font shadow")

    parser.add_argument("-bl", "--bold", action="store_true", default=False)
    parser.add_argument("-il", "--italic", action="store_true", default=False)
    parser.add_argument("-ul", "--underline", action="store_true", default=False)
    parser.add_argument("-so", "--strikeout", action="store_true", default=False)

    parser.add_argument("-bs", "--border_style", nargs="?",
                        choices=list(Subtitle.BORDER_STYLE.keys()),
                        help="border style of subtitle")
    parser.add_argument("-al", "--alignment", nargs="?",
                        choices=list(Subtitle.ALIGNMENT.keys()),
                        default="bottom_center",
                        help="Alignment of subtitle")
    parser.add_argument("-ag", "--angle", nargs="?",
                        type=float, default=0,
                        help="angle (in degree) of subtitle")
    parser.add_argument("-sp", "--spacing", nargs="?",
                        type=int, default=0,
                        help="Extra space (in pixels) between characters")
    parser.add_argument("-ml", "--margin_left", nargs="?",
                        type=int, default=0,
                        help="margin between subtitle and video left border")
    parser.add_argument("-mr", "--margin_right", nargs="?",
                        type=int, default=0,
                        help="margin between subtitle and video right border")
    parser.add_argument("-mv", "--margin_vertical", nargs="?",
                        type=int, default=0,
                        help="margin between subtitle and video top/bottom border")
    parser.add_argument("-sx", "--scalex", nargs="?",
                        type=float, default=1,
                        help="Modifies the width of the font")
    parser.add_argument("-sy", "--scaley", nargs="?",
                        type=float, default=1,
                        help="Modifies the height of the font")
    parser.add_argument("-qa", "--quality", nargs="?",
                        choices=list(Subtitle._FFMPEG_QUALITY.keys()),
                        default=list(Subtitle._FFMPEG_QUALITY.keys())[0],
                        help="The quality of output video")

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


    start = perf_counter()
    sub = Subtitle(font_name='WenQuanYi-Micro-Hei', **dict(args._get_kwargs()))
    sub.write_to_file(args.output)
    end = perf_counter()

    logging.info("video is saved to %s, total cost %s seconds",
                 GREEN+f'{args.output}'+RESET,
                 GREEN+f'{end-start:.2f}'+RESET)
