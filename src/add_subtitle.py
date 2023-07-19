#!/usr/local/bin/python3.10

import argparse
import json
import logging
from matplotlib import colors
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

    _FFMPEG_CMD = 'ffmpeg -y' \
        ' -i {input_video_path}' \
        ' -vf "subtitles={srt_path}:force_style=\'{ass_style}\'"' \
        ' {output_video_path}'

    ALIGNMENT = {"bottom left": 0b0001, "bottom center": 0b0010, "bottom right": 0b0011,
                 "top left":    0b0101, "top center":    0b0110, "top right":    0b0111,
                 "center left": 0b1001, "center center": 0b1010, "center right": 0b1011,
    }

    # border_style: 4 is added by
    # https://github.com/libass/libass/blob/d1f0f20bfa98864cd2aaf931f144909d319545aa/Changelog#L142
    BORDER_STYLE = {"shadow": 1, "box": 3, "rectangle": 4}
    COLORS = list(colors.CSS4_COLORS.keys()) + list(colors.XKCD_COLORS.keys())

    # default style values
    DEFAULT_STYLE = {
        "font_size": 16, "font_color": 'white', "font_transparency": 0,
        "outline_width": 1, "outline_color": 'black', "outline_transparency": 0,
        "shadow_depth": 1, "shadow_color": 'black', "shadow_transparency": 0,
        "bold": False, "italic": False, "underline": False, "strikeout": False,
        "border_style": "shadow", "alignment": "bottom center", "angle": 0.0, "spacing": 0,
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
            Accepted values: "bottom left", "bottom center", "bottom right",
                             "center left", "center center", "center right",
                             "top left", "top center", "top right".
            Default to "bottom center"
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

        if kwargs.get("font_color", "white") not in self.COLORS:
            raise ValueError(f'font_color [{kwargs.get("font_color", "white")}] is not found')
        if kwargs.get("outline_color", "black") not in self.COLORS:
            raise ValueError(f'outline_color [{kwargs.get("outline_color", "black")}] is not found')
        if kwargs.get("shadow_color", "black") not in self.COLORS:
            raise ValueError(f'shadow_color [{kwargs.get("shadow_color", "black")}] is not found')
        if kwargs.get("border_style", "shadow") not in self.BORDER_STYLE:
            raise ValueError(f'border_style [{kwargs.get("border_style", "shadow")}] is not supported')
        if kwargs.get("alignment", "bottom center") not in self.ALIGNMENT:
            raise ValueError(f'alignment [{kwargs.get("alignment", "bottom center")}] is not supported')

        self.style = self.DEFAULT_STYLE
        self.style.update(kwargs)
        self.style["font_color"] = self._color_bgr(self.style["font_color"])
        self.style["font_transparency"] = self._transparency(self.style["font_transparency"])
        self.style["outline_color"] = self._color_bgr(self.style["outline_color"])
        self.style["outline_transparency"] = self._transparency(self.style["outline_transparency"])
        self.style["shadow_color"] = self._color_bgr(self.style["shadow_color"])
        self.style["shadow_transparency"] = self._transparency(self.style["shadow_transparency"])
        self.style["border_style"] = self.BORDER_STYLE[self.style["border_style"]]
        self.style["alignment"] = self.ALIGNMENT[self.style["alignment"]]
        self.style["bold"] = -1 if self.style["bold"] else 0
        self.style["italic"] = -1 if self.style["italic"] else 0
        self.style["underline"] = -1 if self.style["underline"] else 0
        self.style["strikeout"] = -1 if self.style["strikeout"] else 0

        self.video_info = self._prob_video_info(video)
        self._video = video
        self._srt = srt


    def write_to_file(self, file_path: Path):
        ass_style = self._SUBTITLE_ASS_STYLE.format(**self.style)
        cmd = self._FFMPEG_CMD.format(input_video_path=self._video,
                                      srt_path=self._srt,
                                      ass_style=ass_style,
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


    def _color_bgr(self, color: str):
        # color -> rgb_hex -> bgr_hex
        # example: 'xkcd:pink' -> '#FF81C0' -> 'C081FF'
        #          'pink'      -> '#FFC0CB' -> 'CBC0FF
        rgb_hex = colors.to_hex(color)[1:].upper()
        return f'{rgb_hex[4:6]}{rgb_hex[2:4]}{rgb_hex[0:2]}'


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
                        type=str, default='white',
                        help="color of font")
    parser.add_argument("-ft", "--font_transparency", nargs="?",
                        type=int, default=0,
                        help="transparency of font")

    parser.add_argument("-ow", "--outline_width", nargs="?",
                        type=int, default=1,
                        help="width of font outline, in pixels. In box border_style, it's the width of box.")
    parser.add_argument("-oc", "--outline_color", nargs="?",
                        type=str, default='black',
                        help="color of font outline")
    parser.add_argument("-ot", "--outline_transparency", nargs="?",
                        type=int, default=0,
                        help="transparency of font outline")

    parser.add_argument("-sd", "--shadow_depth", nargs="?",
                        type=int, default=1,
                        help="depth of the font shadow, in pixels")
    parser.add_argument("-sc", "--shadow_color", nargs="?",
                        type=str, default='black',
                        help="color of font shadow")
    parser.add_argument("-st", "--shadow_transparency", nargs="?",
                        type=int, default=0,
                        help="transparency of font shadow")

    parser.add_argument("-bl", "--bold", action="store_true", default=False)
    parser.add_argument("-il", "--italic", action="store_true", default=False)
    parser.add_argument("-ul", "--underline", action="store_true", default=False)
    parser.add_argument("-so", "--strikeout", action="store_true", default=False)

    parser.add_argument("-bs", "--border_style", nargs="?",
                        choices=["shadow", "box", "rectangle"], default="shadow",
                        help="border style of subtitle")
    parser.add_argument("-al", "--alignment", nargs="?",
                        choices=["bottom left", "bottom center", "bottom right",
                                 "center left", "center center", "center right",
                                 "top left", "top center", "top right"],
                        default="bottom center",
                        help="border style of subtitle")

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

# with tempfile.TemporaryDirectory() as tmp_dir:
#     os.chdir(tmp_dir)
#     add_subtitle_to_video(args.video,
#                           args.subtitle_file,
#                           args.output,
#                           font_name='WenQuanYi-Micro-Hei',
#                           font_size=20,
#                           font_color=color_name('2:pink purple'),
#                           outline_width=1,
#                           border_style='box',
#     )
    # clip = VideoFileClip(str(args.video))
    # generator = lambda txt: TextClip(txt,
    #                                  font='WenQuanYi-Micro-Hei',
    #                                  fontsize=args.font_size,
    #                                  color=args.font_color,
    #                                  stroke_color=args.stroke_color,
    #                                  stroke_width=args.stroke_width,
    #                                  method='caption',
    #                                  size=clip.size,
    #                                  align='South')
    # sub = SubtitlesClip(str(args.subtitle_file), generator)
    # out_video = CompositeVideoClip([clip, sub])
    # out_video_name = args.video.parent / f'{args.video.stem}.sub{args.video.suffix}'

    # if video_info["codec_name"].lower() in ['hevc', 'h265']:
    #     out_video.write_videofile(str(out_video_name),
    #                               audio_codec='aac',
    #                               codec='libx264',
    #                               ffmpeg_params=[
    #                                   '-color_trc', video_info["color_transfer"],
    #                                   '-color_primaries', video_info["color_primaries"],
    #                                   '-pix_fmt', video_info["pix_fmt"]],
    #                               fps=clip.fps,
    #                               threads=os.cpu_count())
    # else:
    #     out_video.write_videofile(str(out_video_name),
    #                               audio_codec='aac',
    #                               fps=clip.fps,
    #                               threads=os.cpu_count())


    logging.info("video is saved to %s, total cost %s seconds",
                 GREEN+f'{args.output}'+RESET,
                 GREEN+f'{end-start:.2f}'+RESET)
