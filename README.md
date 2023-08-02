
# Welcome to Subtitler!

Hello the fellows of **New Federal States of China (NFSC)**.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/nfsc_flag.jpg)

This project use AI **ASR** ([whisper](https://github.com/openai/whisper)) to generate subtitle file (.srt), and use [ffmpeg](https://www.ffmpeg.org/) to add subtitles to a video. Python is the main programming language. Docker is used to deploy the AI to fellows' PC.


# Other subtitle tools
- [Adobe premiere Pro](https://www.adobe.com/nz/products/premiere/explore/speech.html)
  - Good GUI and subtitle is good as well.
  - Premiere's ASR is not as good as Whisper.
  - Not free.
- [Captions App (require Mac os 13+)](https://apps.apple.com/nz/app/captions-for-talking-videos/id1541407007)
  - Good GUI and subtitle is good as well.
  - Use the same Whisper as ASR.
  - It require Mac os version 13+.

# Setup
## Setup Mac environment
- [Mac 电脑 AI 部署环境搭建 (Part 1) 安装 brew, git, coreutils](https://gettr.com/post/p2mkjtw3b21)
- [Mac 电脑 AI 部署环境搭建 (Part 2) 安装 docker](https://gettr.com/post/p2mkqrr9510)

## Install Source Code
- mkdir ~/Desktop/software
- cd ~/Desktop/software
- git clone https://github.com/redbeardnz/subtitler.git
- cd subtitler
- ./install.sh

## Uninstall Source Code (it needs your Mac's Password to run rm as root user)
- ~/Desktop/software/subtitler/uninstall.sh
- sudo rm -rf ~/Desktop/software/subtitler

# Run
## demo videos:
- en.mp4: https://media.gettr.com/group6/getter/2023/07/15/23/5f37125d-5a2a-fadc-3165-1ee49c41422f/out.mp4
- ja.mp4: https://media.gettr.com/group9/getter/2023/07/15/23/3f3bc970-0745-2651-dd05-a49267b7f326/out.mp4
- miles.mp4: https://media.gettr.com/group12/getter/2023/07/15/23/0629d5e3-d17a-dfc6-8762-2de00aa4f8f2/out.mp4

## Retrive subtitle
You can convert the speech of a video into text and save it as a subtitle **SRT** file by [asr.sh](https://github.com/redbeardnz/subtitler/blob/master/scripts/asr.sh).
Run `asr.sh -h` to see below usage

    Usage: asr.sh -h
           asr.sh [-v] [-i] video [asr options]
    asr.sh converts the speech of a video to text.
    The text is saved in a srt file with a suffix '.srt'
    appended to the name of input video
    
      input:
      video        Local file path to video.
    
      output:
      {video}.srt  Output srt file is saved in the same folder as the input
                   video with a name equaling to video's name + .srt suffix.
    
      options:
      -i           Enable network. By default network is disabled.
                   '-i' must be specified when you need download AI model.
      -v           Show more log.
      -h           Show this help info.
    
      asr options:
      -m, --model <asr_model>
                   asr_model is the whisper model to use. The full whisper model list is
                   [tiny.en tiny base.en base small.en small medium.en medium
                    large-v1 large-v2 large].
                   Default to small.
      -mt, --model_translation <model_translation>
                   model_translation specify neural translation model to use.
                   The full model list is [small, large]
                   Default to small.
      -t, --translate <language_code>
                   language_code specify the target language to translate.
                   The full language code list is:
                   [aav, aed, af, alv, am, ar, art, ase, az, bat, bcl, be, bem, ber, bg,
                    bi, bn, bnt, bzs, ca, cau, ccs, ceb, cel, chk, cpf, crs, cs, csg, csn,
                    cus, cy, da, de, dra, ee, efi, el, en, eo, es, et, eu, euq, fi, fj,
                    fr, fse, ga, gaa, gil, gl, grk, guw, gv, ha, he, hi, hil, ho, hr, ht,
                    hu, hy, id, ig, ilo, is, iso, it, ja, jap, ka, kab, kg, kj, kl, ko,
                    kqn, kwn, kwy, lg, ln, loz, lt, lu, lua, lue, lun, luo, lus, lv, map,
                    mfe, mfs, mg, mh, mk, mkh, ml, mos, mr, ms, mt, mul, ng, nic, niu, nl,
                    no, nso, ny, nyk, om, pa, pag, pap, phi, pis, pl, pon, poz, pqe, pqw,
                    prl, pt, rn, rnd, ro, roa, ru, run, rw, sal, sg, sh, sit, sk, sl, sm,
                    sn, sq, srn, ss, ssp, st, sv, sw, swc, taw, tdt, th, ti, tiv, tl, tll,
                    tn, to, toi, tpi, tr, trk, ts, tum, tut, tvl, tw, ty, tzo, uk, umb,
                    ur, ve, vi, vsl, wa, wal, war, wls, xh, yap, yo, yua, zai, zh, zne]
                   See project Appendix for mapping from language name to language code.
                   Default: no translation.
      -ks, --keep_source
                   if this option is specified, srt contains both original and translated
                   lanugages. if not specified, srt contains only the translated language.

**SRT** files are generated in the same folder as input videos.
#### Example:
- `asr.sh -v ~/subtitle/demo.mp4` generates SRT file to `~/subtitle/demo.mp4.srt`, using default `small` whisper model and bpe vocab downloaded into folder `models/`.
- `asr.sh -i -m medium -v ~/subtitle/demo.mp4`, generates SRT file using `medium` whisper model downloaded into folder `models/`.
- `asr.sh -i -m medium -d my_models -v ~/subtitle/demo.mp4`, generates SRT file using `medium` whisper model downloaded into folder `my_models/`.

> ***HINT***: When you run [asr.sh](https://github.com/redbeardnz/subtitler/blob/master/scripts/asr.sh) at the first time, you need connect your computer to the internet to download whisper models. Once models are well downloaded, internet connection is unnecessary any longer.

#### Uninstall AI models
- sudo rm -rf ~/software/subtitler/models

#### Uninstall Docker image for subtitler
- docker rmi subtitler:latest

## Add subtitle to video
When SRT file `{video}.srt` is available, you can run [subtitle.sh](https://github.com/redbeardnz/subtitler/blob/master/scripts/subtitle.sh) to add subtitle into video.
Run `subtitle.sh -h` to see below usage

    Usage: subtitle.sh [-h] show this help info.
           subtitle.sh [-v] video [style options]
    subtitle.sh add subtitle to video. The subtitle text
    is retrieved from a srt file with a suffix '.srt' appended
    to the name of input video
    
      input:
      video     Local file path to video.
    
      output:
      video     Output video saved in the same folder as input video with a
                name equaling to video name's stem + .sub + video suffix.
    
      options:
      -h        Show this help info.
      -v        Show more verbose log.
    
      style options:
      -fs, --font_size <size>     Size of font. Default 16.
      -fc, --font_color <color>   RGB Color hex of font. Default FFFFFF (white).
      -ft, --font_transparency <transparency>
                                  Transparency of font (0 ~ 100). Default 0.
      -ow, --outline_width <width>
                                  Width of font outline, in pixels. Default 1.
                                  In box border_style, it's the width of box.
      -oc, --outline_color <color>
                                  RGB Color hex of font outline. Default 000000 (black).
      -ot, --outline_transparency <transparency>
                                  Transparency of font outline (0 ~ 100). Default 0.
      -sd, --shadow_depth <depth> Depth of the font shadow, in pixels. Default 1.
      -sc, --shadow_color <color> RGB Color hex of font shadow. Default 000000 (black).
      -st, --shadow_transparency <transparency>
                                  Transparency of font shadow (0 ~ 100). Default 0.
      -bl, --bold                 Enable bold font.
      -il, --italic               Enable italic font.
      -ul, --underline            Enable font underline.
      -so, --strikeout            Enable font strikeout.
      -bs, --border_style <border_style>
                                  border_style: shadow, box, rectangle. Default shadow.
                                  shadow: font with shadow.
                                  box: each subtitle line is embedded in one box.
                                  rectangle: subtitle lines are embedded in a rectangle.
      -al, --alignment <align>    align: 'bottom_left', 'bottom_center', 'bottom_right'
                                         'center_left', 'center_center', 'center_right'
                                         'top_left',    'top_center',    'top_right'
                                  Default 'bottom_center'
      -ag, --angle <angle>        Angle (float) of the subtitle, in degree. Default 0.0.
      -sp, --spacing <spacing>    Extra space (in pixels) between characters. Default 0.
      -ml, --margin_left <margin> Margin from subtitle to video left border. Default 0.
      -mr, --margin_right <margin>
                                  Margin from subtitle to video right border. Default 0.
      -mv, --margin_vertical <margin>
                                  Margin from subtitle to video top/bottom border.
                                  Default 0.
      -sx, --scalex <scale>       Modifies the width of the font by scale (float).
                                  Default 1.0.
      -sy, --scaley <scale>       Modifies the height of the font by scale (float).
                                  Default 1.0.
      -qa, --quality <quality>    quality: ultrahigh, high, standard, fast, ultrafast
                                  The quality of output video.
                                  Default standard.

Videos with subtitle are generated in the same folder as input videos. The name of generated video has a `.sub` added in the name of input videos.

#### Examples:

 - `subtitle.sh ~/subtitle/demo.mp4` generate subtitled video at `~/subtitle/demo.sub.mp4` with default font size/color stroke width/color
 - `subtitle.sh ~/subtitle/demo.mp4 -fc FFFF00 -fs 90 -oc 0000FF -ow 2` generate the same `~/subtitle/demo.sub.mp4`, but with yellow color font in size 90, and with blue font outline in 2 pixel width. See RGB hex in Appendix for yellow color's hex FFFF00 and blue color's hex 0000FF.

> ***HINT***: When you run [subtitle.sh](https://github.com/redbeardnz/subtitler/blob/master/scripts/subtitle.sh) the [style options] must be behind of video path


# Appendix

- RBG colors ${\color{#F7CA5B}hex}$ can be found at [RGB_Color](https://www.rapidtables.com/web/color/RGB_Color.html)

- What are Font, Outline, and Shadow?
![](https://github.com/redbeardnz/subtitler/blob/master/doc/font_outline_shadow.png)

- The border_style modes.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/border_style_modes.png)

- The Outline and Shadow in box and rectangle border style modes.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/outline_shadow_in_box_rectangle_modes.png)

- Transparency.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/transparency.png)

- margins and alignment.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/margins_and_alignment.png)

- The scalex and scaley.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/scalex_scaley.png)

- The angle.
![](https://github.com/redbeardnz/subtitler/blob/master/doc/angle.png)


# License
Whisper's AI model weights are released under the MIT License.
