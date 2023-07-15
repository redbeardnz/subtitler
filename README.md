
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

## Uninstall Source Code (it needs your Mac's Password to run rm as root user)
- sudo rm -rf ~/software/subtitler

# Run
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

    Usage: subtitle.sh -h   show this help info.
           subtitle.sh [-v] video
    subtitle.sh add subtitle to video. The subtitle text
    is retrieved from a srt file with a suffix '.srt' appended
    to the name of input video
    
      input:
      video          Local file path to video.
    
      output:
      video          Output video saved in the same folder as input video with a
                     name equaling to video name's stem + .sub + video suffix.
    
      options:
      -c font_color   Specify font color of subtitle. The full color list is avaiable
                      in README.md.
                      Default to FloralWhite.
      -s font_size    Specify font size of subtitle. The valie range from 1 to 100
                      Default to 100.
      -t stroke_color Specify stroke color of subtitle. The full color list is avaiable
                      in README.md.
                      Default to black.
      -w stroke_width Specify stroke width of subtitle. The valie is float
                      Default to 0.1.

Videos with subtitle are generated in the same folder as input videos. The name of generated video has a `.sub` added in the name of input videos.

#### Examples:

 - `subtitle.sh ~/subtitle/demo.mp4` generate subtitled video at `~/subtitle/demo.sub.mp4` with default font size/color stroke width/color
 - `subtitle.sh -c yellow -s 90 -t blue -w 0.2 ~/subtitle/demo.mp4` generate the same `~/subtitle/demo.sub.mp4`, but with yellow color font in size 90, and with blue stroke color in width 0.2.


# Appendix

 - The full color list:
AliceBlue, AntiqueWhite, AntiqueWhite1, AntiqueWhite2, AntiqueWhite3, AntiqueWhite4, aqua, aquamarine, aquamarine1, aquamarine2, aquamarine3, aquamarine4, azure, azure1, azure2, azure3, azure4, beige, bisque, bisque1, bisque2, bisque3, bisque4, black, BlanchedAlmond, blue, blue1, blue2, blue3, blue4, BlueViolet, brown, brown1, brown2, brown3, brown4, burlywood, burlywood1, burlywood2, burlywood3, burlywood4, CadetBlue, CadetBlue1, CadetBlue2, CadetBlue3, CadetBlue4, chartreuse, chartreuse1, chartreuse2, chartreuse3, chartreuse4, chocolate, chocolate1, chocolate2, chocolate3, chocolate4, coral, coral1, coral2, coral3, coral4, CornflowerBlue, cornsilk, cornsilk1, cornsilk2, cornsilk3, cornsilk4, crimson, cyan, cyan1, cyan2, cyan3, cyan4, DarkBlue, DarkCyan, DarkGoldenrod, DarkGoldenrod1, DarkGoldenrod2, DarkGoldenrod3, DarkGoldenrod4, DarkGray, DarkGreen, DarkGrey, DarkKhaki, DarkMagenta, DarkOliveGreen, DarkOliveGreen1, DarkOliveGreen2, DarkOliveGreen3, DarkOliveGreen4, DarkOrange, DarkOrange1, DarkOrange2, DarkOrange3, DarkOrange4, DarkOrchid, DarkOrchid1, DarkOrchid2, DarkOrchid3, DarkOrchid4, DarkRed, DarkSalmon, DarkSeaGreen, DarkSeaGreen1, DarkSeaGreen2, DarkSeaGreen3, DarkSeaGreen4, DarkSlateBlue, DarkSlateGray, DarkSlateGray1, DarkSlateGray2, DarkSlateGray3, DarkSlateGray4, DarkSlateGrey, DarkTurquoise, DarkViolet, DeepPink, DeepPink1, DeepPink2, DeepPink3, DeepPink4, DeepSkyBlue, DeepSkyBlue1, DeepSkyBlue2, DeepSkyBlue3, DeepSkyBlue4, DimGray, DimGrey, DodgerBlue, DodgerBlue1, DodgerBlue2, DodgerBlue3, DodgerBlue4, firebrick, firebrick1, firebrick2, firebrick3, firebrick4, FloralWhite, ForestGreen, fractal, freeze, fuchsia, gainsboro, GhostWhite, gold, gold1, gold2, gold3, gold4, goldenrod, goldenrod1, goldenrod2, goldenrod3, goldenrod4, gray, gray, gray0, gray1, gray10, gray100, gray100, gray11, gray12, gray13, gray14, gray15, gray16, gray17, gray18, gray19, gray2, gray20, gray21, gray22, gray23, gray24, gray25, gray26, gray27, gray28, gray29, gray3, gray30, gray31, gray32, gray33, gray34, gray35, gray36, gray37, gray38, gray39, gray4, gray40, gray41, gray42, gray43, gray44, gray45, gray46, gray47, gray48, gray49, gray5, gray50, gray51, gray52, gray53, gray54, gray55, gray56, gray57, gray58, gray59, gray6, gray60, gray61, gray62, gray63, gray64, gray65, gray66, gray67, gray68, gray69, gray7, gray70, gray71, gray72, gray73, gray74, gray75, gray76, gray77, gray78, gray79, gray8, gray80, gray81, gray82, gray83, gray84, gray85, gray86, gray87, gray88, gray89, gray9, gray90, gray91, gray92, gray93, gray94, gray95, gray96, gray97, gray98, gray99, green, green, green1, green2, green3, green4, GreenYellow, grey, grey0, grey1, grey10, grey100, grey11, grey12, grey13, grey14, grey15, grey16, grey17, grey18, grey19, grey2, grey20, grey21, grey22, grey23, grey24, grey25, grey26, grey27, grey28, grey29, grey3, grey30, grey31, grey32, grey33, grey34, grey35, grey36, grey37, grey38, grey39, grey4, grey40, grey41, grey42, grey43, grey44, grey45, grey46, grey47, grey48, grey49, grey5, grey50, grey51, grey52, grey53, grey54, grey55, grey56, grey57, grey58, grey59, grey6, grey60, grey61, grey62, grey63, grey64, grey65, grey66, grey67, grey68, grey69, grey7, grey70, grey71, grey72, grey73, grey74, grey75, grey76, grey77, grey78, grey79, grey8, grey80, grey81, grey82, grey83, grey84, grey85, grey86, grey87, grey88, grey89, grey9, grey90, grey91, grey92, grey93, grey94, grey95, grey96, grey97, grey98, grey99, honeydew, honeydew1, honeydew2, honeydew3, honeydew4, HotPink, HotPink1, HotPink2, HotPink3, HotPink4, IndianRed, IndianRed1, IndianRed2, IndianRed3, IndianRed4, indigo, ivory, ivory1, ivory2, ivory3, ivory4, khaki, khaki1, khaki2, khaki3, khaki4, lavender, LavenderBlush, LavenderBlush1, LavenderBlush2, LavenderBlush3, LavenderBlush4, LawnGreen, LemonChiffon, LemonChiffon1, LemonChiffon2, LemonChiffon3, LemonChiffon4, LightBlue, LightBlue1, LightBlue2, LightBlue3, LightBlue4, LightCoral, LightCyan, LightCyan1, LightCyan2, LightCyan3, LightCyan4, LightGoldenrod, LightGoldenrod1, LightGoldenrod2, LightGoldenrod3, LightGoldenrod4, LightGoldenrodYellow, LightGray, LightGreen, LightGrey, LightPink, LightPink1, LightPink2, LightPink3, LightPink4, LightSalmon, LightSalmon1, LightSalmon2, LightSalmon3, LightSalmon4, LightSeaGreen, LightSkyBlue, LightSkyBlue1, LightSkyBlue2, LightSkyBlue3, LightSkyBlue4, LightSlateBlue, LightSlateGray, LightSlateGrey, LightSteelBlue, LightSteelBlue1, LightSteelBlue2, LightSteelBlue3, LightSteelBlue4, LightYellow, LightYellow1, LightYellow2, LightYellow3, LightYellow4, lime, LimeGreen, linen, magenta, magenta1, magenta2, magenta3, magenta4, maroon, maroon, maroon1, maroon2, maroon3, maroon4, matte, MediumAquamarine, MediumBlue, MediumForestGreen, MediumGoldenRod, MediumOrchid, MediumOrchid1, MediumOrchid2, MediumOrchid3, MediumOrchid4, MediumPurple, MediumPurple1, MediumPurple2, MediumPurple3, MediumPurple4, MediumSeaGreen, MediumSlateBlue, MediumSpringGreen, MediumTurquoise, MediumVioletRed, MidnightBlue, MintCream, MistyRose, MistyRose1, MistyRose2, MistyRose3, MistyRose4, moccasin, NavajoWhite, NavajoWhite1, NavajoWhite2, NavajoWhite3, NavajoWhite4, navy, NavyBlue, none, OldLace, olive, OliveDra, OliveDrab1, OliveDrab2, OliveDrab3, OliveDrab4, opaque, orange, orange1, orange2, orange3, orange4, OrangeRed, OrangeRed1, OrangeRed2, OrangeRed3, OrangeRed4, orchid, orchid1, orchid2, orchid3, orchid4, PaleGoldenrod, PaleGreen, PaleGreen1, PaleGreen2, PaleGreen3, PaleGreen4, PaleTurquoise, PaleTurquoise1, PaleTurquoise2, PaleTurquoise3, PaleTurquoise4, PaleVioletRed, PaleVioletRed1, PaleVioletRed2, PaleVioletRed3, PaleVioletRed4, PapayaWhip, PeachPuff, PeachPuff1, PeachPuff2, PeachPuff3, PeachPuff4, peru, pink, pink1, pink2, pink3, pink4, plum, plum1, plum2, plum3, plum4, PowderBlue, purple, purple, purple1, purple2, purple3, purple4, red, red1, red2, red3, red4, RosyBrown, RosyBrown1, RosyBrown2, RosyBrown3, RosyBrown4, RoyalBlue, RoyalBlue1, RoyalBlue2, RoyalBlue3, RoyalBlue4, SaddleBrown, salmon, salmon1, salmon2, salmon3, salmon4, SandyBrown, SeaGreen, SeaGreen1, SeaGreen2, SeaGreen3, SeaGreen4, seashell, seashell1, seashell2, seashell3, seashell4, sienna, sienna1, sienna2, sienna3, sienna4, silver, SkyBlue, SkyBlue1, SkyBlue2, SkyBlue3, SkyBlue4, SlateBlue, SlateBlue1, SlateBlue2, SlateBlue3, SlateBlue4, SlateGray, SlateGray1, SlateGray2, SlateGray3, SlateGray4, SlateGrey, snow, snow1, snow2, snow3, snow4, SpringGreen, SpringGreen1, SpringGreen2, SpringGreen3, SpringGreen4, SteelBlue, SteelBlue1, SteelBlue2, SteelBlue3, SteelBlue4, tan, tan1, tan2, tan3, tan4, teal, thistle, thistle1, thistle2, thistle3, thistle4, tomato, tomato1, tomato2, tomato3, tomato4, transparent, turquoise, turquoise1, turquoise2, turquoise3, turquoise4, violet, VioletRed, VioletRed1, VioletRed2, VioletRed3, VioletRed4, wheat, wheat1, wheat2, wheat3, wheat4, white, WhiteSmoke, yellow, yellow1, yellow2, yellow3, yellow4, YellowGreen

# License
Whisper's AI model weights are released under the MIT License.