
# Welcome to Subtitler!

Hello the fellows of **New Federal States of China (NFSC)**.

This project use AI **ASR** ([whisper](https://github.com/openai/whisper)) to generate subtitle file (.srt), and use [moviepy](https://github.com/Zulko/moviepy) to add subtitles to a video. Python is the main programming language. Docker is used to deploy the AI to fellows' PC.


# Setup
## Install Source Code
- mkdir ~/software
- cd ~/software
- git clone https://github.com/redbeardnz/subtitler.git
- cd subtitler
- mkdir ~/bin
- ln -s $(pwd)/*.sh ~/bin/
- echo 'PATH=${PATH}:~/bin' >> ~/.bash_profile

## Uninstall Source Code (it needs your Mac's Password to run rm as root user)
- sudo rm -rf ~/software/subtitler

# Run
## demo videos:
- en.mp4: https://media.gettr.com/group6/getter/2023/07/15/23/5f37125d-5a2a-fadc-3165-1ee49c41422f/out.mp4
- ja.mp4: https://media.gettr.com/group9/getter/2023/07/15/23/3f3bc970-0745-2651-dd05-a49267b7f326/out.mp4
- miles.mp4: https://media.gettr.com/group12/getter/2023/07/15/23/0629d5e3-d17a-dfc6-8762-2de00aa4f8f2/out.mp4

## Retrive subtitle
You can convert the speech of a video into text and save it as a subtitle **SRT** file by [asr.sh](https://github.com/redbeardnz/subtitler/blob/master/asr.sh).
Run `asr.sh -h` to see below usage

    Usage: asr.sh -h   show this help info.
	       asr.sh [-v] [-m model] [-d model_dir] [-i] video
    asr.sh converts the speech of a video to text.
    The text is saved in a srt file with a suffix '.srt'
    appended to the name of input video
    
      input:
      video        Local file path to video.
    
      output:
      {video}.srt  Output srt file is saved in the same folder as the input
                   video with a name equaling to video's name + .srt suffix.
    
      options:
      -d model_dir Specify the location to store whisper models.
                   Default to /Users/knox/work/subtitler/models.
      -m model     Specify whisper asr model to use. The full model list is
                   [tiny.en tiny base.en base small.en small medium.en medium
                    large-v1 large-v2 large].
                   Default to small.
      -i           Enable network. By default network is disabled.
                   '-i' must be specified when you need download AI model.

**SRT** files are generated in the same folder as input videos.
#### Example:
- `asr.sh -v ~/subtitle/demo.mp4` generates SRT file to `~/subtitle/demo.mp4.srt`, using default `small` whisper model and bpe vocab downloaded into folder `models/`.
- `asr.sh -i -m medium -v ~/subtitle/demo.mp4`, generates SRT file using `medium` whisper model downloaded into folder `models/`.
- `asr.sh -i -m medium -d my_models -v ~/subtitle/demo.mp4`, generates SRT file using `medium` whisper model downloaded into folder `my_models/`.

> ***HINT***: When you run [asr.sh](https://github.com/redbeardnz/subtitler/blob/master/asr.sh) at the first time, you need connect your computer to the internet to download whisper models. Once models are well downloaded, internet connection is unnecessary any longer.

#### Uninstall AI models
- sudo rm -rf ~/software/subtitler/models

#### Uninstall Docker image for subtitler
- docker rmi subtitler:latest

## Add subtitle to video
When SRT file `{video}.srt` is available, you can run [subtitle.sh](https://github.com/redbeardnz/subtitler/blob/master/subtitle.sh) to add subtitle into video.
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
      -fc, --font_color <color>   Color of font. Default white.
      -ft, --font_transparency <transparency>
                                  Transparency of font (0 ~ 100). Default 0.
      -ow, --outline_width <width>
                                  Width of font outline, in pixels. Default 1.
                                  In box border_style, it's the width of box
      -oc, --outline_color <color>
                                  Color of font outline. Default black.
      -ot, --outline_transparency <transparency>
                                  Transparency of font outline. Default 0.
      -sd, --shadow_depth <depth> Depth of the font shadow, in pixels. Default 1.
      -sc, --shadow_color <color> Color of font shadow. Default black.
      -st, --shadow_transparency <transparency>
                                  Transparency of font shadow. Default 0.
      -bl, --bold                 Enable bold font.
      -il, --italic               Enable italic font.
      -ul, --underline            Enable font underline.
      -so, --strikeout            Enable font strikeout.
      -bs, --border_style <border_style>
                                  border_style: shadow, box, rectangle. Default shadow.
                                  shadow: font with shadow.
                                  box: each subtitle line is embedded in one box.
                                  rectangle: subtitle lines are embedded in a rectangle.
      -al, --alignment <align>    align: 'bottom left', 'bottom center', 'bottom right'
                                         'center left', 'center center', 'center right'
                                         'top left', 'top center', 'top right'
                                  Default 'bottom center'
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
 - `subtitle.sh ~/subtitle/demo.mp4 -fc yellow -fs 90 -oc blue -ow 2` generate the same `~/subtitle/demo.sub.mp4`, but with yellow color font in size 90, and with blue font outline in 2 pixel width.


# Appendix

 - The full color table:



# License
Whisper's AI model weights are released under the MIT License.