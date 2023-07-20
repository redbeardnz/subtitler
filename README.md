
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

|${\color{#F0F8FF}aliceblue}$ aliceblue|${\color{#FAEBD7}antiquewhite}$ antiquewhite|${\color{#00FFFF}aqua}$ aqua|${\color{#7FFFD4}aquamarine}$ aquamarine|${\color{#F0FFFF}azure}$ azure|${\color{#F5F5DC}beige}$ beige|
|--|--|--|--|--|--|
|${\color{#FFE4C4}bisque}$ bisque|${\color{#000000}black}$ black|${\color{#FFEBCD}blanchedalmond}$ blanchedalmond|${\color{#0000FF}blue}$ blue|${\color{#8A2BE2}blueviolet}$ blueviolet|${\color{#A52A2A}brown}$ brown|
|--|--|--|--|--|--|
|${\color{#DEB887}burlywood}$ burlywood|${\color{#5F9EA0}cadetblue}$ cadetblue|${\color{#7FFF00}chartreuse}$ chartreuse|${\color{#D2691E}chocolate}$ chocolate|${\color{#FF7F50}coral}$ coral|${\color{#6495ED}cornflowerblue}$ cornflowerblue|
|--|--|--|--|--|--|
|${\color{#FFF8DC}cornsilk}$ cornsilk|${\color{#DC143C}crimson}$ crimson|${\color{#00FFFF}cyan}$ cyan|${\color{#00008B}darkblue}$ darkblue|${\color{#008B8B}darkcyan}$ darkcyan|${\color{#B8860B}darkgoldenrod}$ darkgoldenrod|
|--|--|--|--|--|--|
|${\color{#A9A9A9}darkgray}$ darkgray|${\color{#006400}darkgreen}$ darkgreen|${\color{#A9A9A9}darkgrey}$ darkgrey|${\color{#BDB76B}darkkhaki}$ darkkhaki|${\color{#8B008B}darkmagenta}$ darkmagenta|${\color{#556B2F}darkolivegreen}$ darkolivegreen|
|--|--|--|--|--|--|
|${\color{#FF8C00}darkorange}$ darkorange|${\color{#9932CC}darkorchid}$ darkorchid|${\color{#8B0000}darkred}$ darkred|${\color{#E9967A}darksalmon}$ darksalmon|${\color{#8FBC8F}darkseagreen}$ darkseagreen|${\color{#483D8B}darkslateblue}$ darkslateblue|
|--|--|--|--|--|--|
|${\color{#2F4F4F}darkslategray}$ darkslategray|${\color{#2F4F4F}darkslategrey}$ darkslategrey|${\color{#00CED1}darkturquoise}$ darkturquoise|${\color{#9400D3}darkviolet}$ darkviolet|${\color{#FF1493}deeppink}$ deeppink|${\color{#00BFFF}deepskyblue}$ deepskyblue|
|--|--|--|--|--|--|
|${\color{#696969}dimgray}$ dimgray|${\color{#696969}dimgrey}$ dimgrey|${\color{#1E90FF}dodgerblue}$ dodgerblue|${\color{#B22222}firebrick}$ firebrick|${\color{#FFFAF0}floralwhite}$ floralwhite|${\color{#228B22}forestgreen}$ forestgreen|
|--|--|--|--|--|--|
|${\color{#FF00FF}fuchsia}$ fuchsia|${\color{#DCDCDC}gainsboro}$ gainsboro|${\color{#F8F8FF}ghostwhite}$ ghostwhite|${\color{#FFD700}gold}$ gold|${\color{#DAA520}goldenrod}$ goldenrod|${\color{#808080}gray}$ gray|
|--|--|--|--|--|--|
|${\color{#008000}green}$ green|${\color{#ADFF2F}greenyellow}$ greenyellow|${\color{#808080}grey}$ grey|${\color{#F0FFF0}honeydew}$ honeydew|${\color{#FF69B4}hotpink}$ hotpink|${\color{#CD5C5C}indianred}$ indianred|
|--|--|--|--|--|--|
|${\color{#4B0082}indigo}$ indigo|${\color{#FFFFF0}ivory}$ ivory|${\color{#F0E68C}khaki}$ khaki|${\color{#E6E6FA}lavender}$ lavender|${\color{#FFF0F5}lavenderblush}$ lavenderblush|${\color{#7CFC00}lawngreen}$ lawngreen|
|--|--|--|--|--|--|
|${\color{#FFFACD}lemonchiffon}$ lemonchiffon|${\color{#ADD8E6}lightblue}$ lightblue|${\color{#F08080}lightcoral}$ lightcoral|${\color{#E0FFFF}lightcyan}$ lightcyan|${\color{#FAFAD2}lightgoldenrodyellow}$ lightgoldenrodyellow|${\color{#D3D3D3}lightgray}$ lightgray|
|--|--|--|--|--|--|
|${\color{#90EE90}lightgreen}$ lightgreen|${\color{#D3D3D3}lightgrey}$ lightgrey|${\color{#FFB6C1}lightpink}$ lightpink|${\color{#FFA07A}lightsalmon}$ lightsalmon|${\color{#20B2AA}lightseagreen}$ lightseagreen|${\color{#87CEFA}lightskyblue}$ lightskyblue|
|--|--|--|--|--|--|
|${\color{#778899}lightslategray}$ lightslategray|${\color{#778899}lightslategrey}$ lightslategrey|${\color{#B0C4DE}lightsteelblue}$ lightsteelblue|${\color{#FFFFE0}lightyellow}$ lightyellow|${\color{#00FF00}lime}$ lime|${\color{#32CD32}limegreen}$ limegreen|
|--|--|--|--|--|--|
|${\color{#FAF0E6}linen}$ linen|${\color{#FF00FF}magenta}$ magenta|${\color{#800000}maroon}$ maroon|${\color{#66CDAA}mediumaquamarine}$ mediumaquamarine|${\color{#0000CD}mediumblue}$ mediumblue|${\color{#BA55D3}mediumorchid}$ mediumorchid|
|--|--|--|--|--|--|
|${\color{#9370DB}mediumpurple}$ mediumpurple|${\color{#3CB371}mediumseagreen}$ mediumseagreen|${\color{#7B68EE}mediumslateblue}$ mediumslateblue|${\color{#00FA9A}mediumspringgreen}$ mediumspringgreen|${\color{#48D1CC}mediumturquoise}$ mediumturquoise|${\color{#C71585}mediumvioletred}$ mediumvioletred|
|--|--|--|--|--|--|
|${\color{#191970}midnightblue}$ midnightblue|${\color{#F5FFFA}mintcream}$ mintcream|${\color{#FFE4E1}mistyrose}$ mistyrose|${\color{#FFE4B5}moccasin}$ moccasin|${\color{#FFDEAD}navajowhite}$ navajowhite|${\color{#000080}navy}$ navy|
|--|--|--|--|--|--|
|${\color{#FDF5E6}oldlace}$ oldlace|${\color{#808000}olive}$ olive|${\color{#6B8E23}olivedrab}$ olivedrab|${\color{#FFA500}orange}$ orange|${\color{#FF4500}orangered}$ orangered|${\color{#DA70D6}orchid}$ orchid|
|--|--|--|--|--|--|
|${\color{#EEE8AA}palegoldenrod}$ palegoldenrod|${\color{#98FB98}palegreen}$ palegreen|${\color{#AFEEEE}paleturquoise}$ paleturquoise|${\color{#DB7093}palevioletred}$ palevioletred|${\color{#FFEFD5}papayawhip}$ papayawhip|${\color{#FFDAB9}peachpuff}$ peachpuff|
|--|--|--|--|--|--|
|${\color{#CD853F}peru}$ peru|${\color{#FFC0CB}pink}$ pink|${\color{#DDA0DD}plum}$ plum|${\color{#B0E0E6}powderblue}$ powderblue|${\color{#800080}purple}$ purple|${\color{#663399}rebeccapurple}$ rebeccapurple|
|--|--|--|--|--|--|
|${\color{#FF0000}red}$ red|${\color{#BC8F8F}rosybrown}$ rosybrown|${\color{#4169E1}royalblue}$ royalblue|${\color{#8B4513}saddlebrown}$ saddlebrown|${\color{#FA8072}salmon}$ salmon|${\color{#F4A460}sandybrown}$ sandybrown|
|--|--|--|--|--|--|
|${\color{#2E8B57}seagreen}$ seagreen|${\color{#FFF5EE}seashell}$ seashell|${\color{#A0522D}sienna}$ sienna|${\color{#C0C0C0}silver}$ silver|${\color{#87CEEB}skyblue}$ skyblue|${\color{#6A5ACD}slateblue}$ slateblue|
|--|--|--|--|--|--|
|${\color{#708090}slategray}$ slategray|${\color{#708090}slategrey}$ slategrey|${\color{#FFFAFA}snow}$ snow|${\color{#00FF7F}springgreen}$ springgreen|${\color{#4682B4}steelblue}$ steelblue|${\color{#D2B48C}tan}$ tan|
|--|--|--|--|--|--|
|${\color{#008080}teal}$ teal|${\color{#D8BFD8}thistle}$ thistle|${\color{#FF6347}tomato}$ tomato|${\color{#40E0D0}turquoise}$ turquoise|${\color{#EE82EE}violet}$ violet|${\color{#F5DEB3}wheat}$ wheat|
|--|--|--|--|--|--|
|${\color{#FFFFFF}white}$ white|${\color{#F5F5F5}whitesmoke}$ whitesmoke|${\color{#FFFF00}yellow}$ yellow|${\color{#9ACD32}yellowgreen}$ yellowgreen|

|${\color{#acc2d9}cloudy blue}$ 'xkcd:cloudy blue'|${\color{#56ae57}dark pastel green}$ 'xkcd:dark pastel green'|${\color{#b2996e}dust}$ 'xkcd:dust'|
|--|--|--|
|${\color{#a8ff04}electric lime}$ 'xkcd:electric lime'|${\color{#69d84f}fresh green}$ 'xkcd:fresh green'|${\color{#894585}light eggplant}$ 'xkcd:light eggplant'|
|--|--|--|
|${\color{#70b23f}nasty green}$ 'xkcd:nasty green'|${\color{#d4ffff}really light blue}$ 'xkcd:really light blue'|${\color{#65ab7c}tea}$ 'xkcd:tea'|
|--|--|--|
|${\color{#952e8f}warm purple}$ 'xkcd:warm purple'|${\color{#fcfc81}yellowish tan}$ 'xkcd:yellowish tan'|${\color{#a5a391}cement}$ 'xkcd:cement'|
|--|--|--|
|${\color{#388004}dark grass green}$ 'xkcd:dark grass green'|${\color{#4c9085}dusty teal}$ 'xkcd:dusty teal'|${\color{#5e9b8a}grey teal}$ 'xkcd:grey teal'|
|--|--|--|
|${\color{#efb435}macaroni and cheese}$ 'xkcd:macaroni and cheese'|${\color{#d99b82}pinkish tan}$ 'xkcd:pinkish tan'|${\color{#0a5f38}spruce}$ 'xkcd:spruce'|
|--|--|--|
|${\color{#0c06f7}strong blue}$ 'xkcd:strong blue'|${\color{#61de2a}toxic green}$ 'xkcd:toxic green'|${\color{#3778bf}windows blue}$ 'xkcd:windows blue'|
|--|--|--|
|${\color{#2242c7}blue blue}$ 'xkcd:blue blue'|${\color{#533cc6}blue with a hint of purple}$ 'xkcd:blue with a hint of purple'|${\color{#9bb53c}booger}$ 'xkcd:booger'|
|--|--|--|
|${\color{#05ffa6}bright sea green}$ 'xkcd:bright sea green'|${\color{#1f6357}dark green blue}$ 'xkcd:dark green blue'|${\color{#017374}deep turquoise}$ 'xkcd:deep turquoise'|
|--|--|--|
|${\color{#0cb577}green teal}$ 'xkcd:green teal'|${\color{#ff0789}strong pink}$ 'xkcd:strong pink'|${\color{#afa88b}bland}$ 'xkcd:bland'|
|--|--|--|
|${\color{#08787f}deep aqua}$ 'xkcd:deep aqua'|${\color{#dd85d7}lavender pink}$ 'xkcd:lavender pink'|${\color{#a6c875}light moss green}$ 'xkcd:light moss green'|
|--|--|--|
|${\color{#a7ffb5}light seafoam green}$ 'xkcd:light seafoam green'|${\color{#c2b709}olive yellow}$ 'xkcd:olive yellow'|${\color{#e78ea5}pig pink}$ 'xkcd:pig pink'|
|--|--|--|
|${\color{#966ebd}deep lilac}$ 'xkcd:deep lilac'|${\color{#ccad60}desert}$ 'xkcd:desert'|${\color{#ac86a8}dusty lavender}$ 'xkcd:dusty lavender'|
|--|--|--|
|${\color{#947e94}purpley grey}$ 'xkcd:purpley grey'|${\color{#983fb2}purply}$ 'xkcd:purply'|${\color{#ff63e9}candy pink}$ 'xkcd:candy pink'|
|--|--|--|
|${\color{#b2fba5}light pastel green}$ 'xkcd:light pastel green'|${\color{#63b365}boring green}$ 'xkcd:boring green'|${\color{#8ee53f}kiwi green}$ 'xkcd:kiwi green'|
|--|--|--|
|${\color{#b7e1a1}light grey green}$ 'xkcd:light grey green'|${\color{#ff6f52}orange pink}$ 'xkcd:orange pink'|${\color{#bdf8a3}tea green}$ 'xkcd:tea green'|
|--|--|--|
|${\color{#d3b683}very light brown}$ 'xkcd:very light brown'|${\color{#fffcc4}egg shell}$ 'xkcd:egg shell'|${\color{#430541}eggplant purple}$ 'xkcd:eggplant purple'|
|--|--|--|
|${\color{#ffb2d0}powder pink}$ 'xkcd:powder pink'|${\color{#997570}reddish grey}$ 'xkcd:reddish grey'|${\color{#ad900d}baby shit brown}$ 'xkcd:baby shit brown'|
|--|--|--|
|${\color{#c48efd}liliac}$ 'xkcd:liliac'|${\color{#507b9c}stormy blue}$ 'xkcd:stormy blue'|${\color{#7d7103}ugly brown}$ 'xkcd:ugly brown'|
|--|--|--|
|${\color{#fffd78}custard}$ 'xkcd:custard'|${\color{#da467d}darkish pink}$ 'xkcd:darkish pink'|${\color{#410200}deep brown}$ 'xkcd:deep brown'|
|--|--|--|
|${\color{#c9d179}greenish beige}$ 'xkcd:greenish beige'|${\color{#fffa86}manilla}$ 'xkcd:manilla'|${\color{#5684ae}off blue}$ 'xkcd:off blue'|
|--|--|--|
|${\color{#6b7c85}battleship grey}$ 'xkcd:battleship grey'|${\color{#6f6c0a}browny green}$ 'xkcd:browny green'|${\color{#7e4071}bruise}$ 'xkcd:bruise'|
|--|--|--|
|${\color{#009337}kelley green}$ 'xkcd:kelley green'|${\color{#d0e429}sickly yellow}$ 'xkcd:sickly yellow'|${\color{#fff917}sunny yellow}$ 'xkcd:sunny yellow'|
|--|--|--|
|${\color{#1d5dec}azul}$ 'xkcd:azul'|${\color{#054907}darkgreen}$ 'xkcd:darkgreen'|${\color{#b5ce08}green/yellow}$ 'xkcd:green/yellow'|
|--|--|--|
|${\color{#8fb67b}lichen}$ 'xkcd:lichen'|${\color{#c8ffb0}light light green}$ 'xkcd:light light green'|${\color{#fdde6c}pale gold}$ 'xkcd:pale gold'|
|--|--|--|
|${\color{#ffdf22}sun yellow}$ 'xkcd:sun yellow'|${\color{#a9be70}tan green}$ 'xkcd:tan green'|${\color{#6832e3}burple}$ 'xkcd:burple'|
|--|--|--|
|${\color{#fdb147}butterscotch}$ 'xkcd:butterscotch'|${\color{#c7ac7d}toupe}$ 'xkcd:toupe'|${\color{#fff39a}dark cream}$ 'xkcd:dark cream'|
|--|--|--|
|${\color{#850e04}indian red}$ 'xkcd:indian red'|${\color{#efc0fe}light lavendar}$ 'xkcd:light lavendar'|${\color{#40fd14}poison green}$ 'xkcd:poison green'|
|--|--|--|
|${\color{#b6c406}baby puke green}$ 'xkcd:baby puke green'|${\color{#9dff00}bright yellow green}$ 'xkcd:bright yellow green'|${\color{#3c4142}charcoal grey}$ 'xkcd:charcoal grey'|
|--|--|--|
|${\color{#f2ab15}squash}$ 'xkcd:squash'|${\color{#ac4f06}cinnamon}$ 'xkcd:cinnamon'|${\color{#c4fe82}light pea green}$ 'xkcd:light pea green'|
|--|--|--|
|${\color{#2cfa1f}radioactive green}$ 'xkcd:radioactive green'|${\color{#9a6200}raw sienna}$ 'xkcd:raw sienna'|${\color{#ca9bf7}baby purple}$ 'xkcd:baby purple'|
|--|--|--|
|${\color{#875f42}cocoa}$ 'xkcd:cocoa'|${\color{#3a2efe}light royal blue}$ 'xkcd:light royal blue'|${\color{#fd8d49}orangeish}$ 'xkcd:orangeish'|
|--|--|--|
|${\color{#8b3103}rust brown}$ 'xkcd:rust brown'|${\color{#cba560}sand brown}$ 'xkcd:sand brown'|${\color{#698339}swamp}$ 'xkcd:swamp'|
|--|--|--|
|${\color{#0cdc73}tealish green}$ 'xkcd:tealish green'|${\color{#b75203}burnt siena}$ 'xkcd:burnt siena'|${\color{#7f8f4e}camo}$ 'xkcd:camo'|
|--|--|--|
|${\color{#26538d}dusk blue}$ 'xkcd:dusk blue'|${\color{#63a950}fern}$ 'xkcd:fern'|${\color{#c87f89}old rose}$ 'xkcd:old rose'|
|--|--|--|
|${\color{#b1fc99}pale light green}$ 'xkcd:pale light green'|${\color{#ff9a8a}peachy pink}$ 'xkcd:peachy pink'|${\color{#f6688e}rosy pink}$ 'xkcd:rosy pink'|
|--|--|--|
|${\color{#76fda8}light bluish green}$ 'xkcd:light bluish green'|${\color{#53fe5c}light bright green}$ 'xkcd:light bright green'|${\color{#4efd54}light neon green}$ 'xkcd:light neon green'|
|--|--|--|
|${\color{#a0febf}light seafoam}$ 'xkcd:light seafoam'|${\color{#7bf2da}tiffany blue}$ 'xkcd:tiffany blue'|${\color{#bcf5a6}washed out green}$ 'xkcd:washed out green'|
|--|--|--|
|${\color{#ca6b02}browny orange}$ 'xkcd:browny orange'|${\color{#107ab0}nice blue}$ 'xkcd:nice blue'|${\color{#2138ab}sapphire}$ 'xkcd:sapphire'|
|--|--|--|
|${\color{#719f91}greyish teal}$ 'xkcd:greyish teal'|${\color{#fdb915}orangey yellow}$ 'xkcd:orangey yellow'|${\color{#fefcaf}parchment}$ 'xkcd:parchment'|
|--|--|--|
|${\color{#fcf679}straw}$ 'xkcd:straw'|${\color{#1d0200}very dark brown}$ 'xkcd:very dark brown'|${\color{#cb6843}terracota}$ 'xkcd:terracota'|
|--|--|--|
|${\color{#31668a}ugly blue}$ 'xkcd:ugly blue'|${\color{#247afd}clear blue}$ 'xkcd:clear blue'|${\color{#ffffb6}creme}$ 'xkcd:creme'|
|--|--|--|
|${\color{#90fda9}foam green}$ 'xkcd:foam green'|${\color{#86a17d}grey/green}$ 'xkcd:grey/green'|${\color{#fddc5c}light gold}$ 'xkcd:light gold'|
|--|--|--|
|${\color{#78d1b6}seafoam blue}$ 'xkcd:seafoam blue'|${\color{#13bbaf}topaz}$ 'xkcd:topaz'|${\color{#fb5ffc}violet pink}$ 'xkcd:violet pink'|
|--|--|--|
|${\color{#20f986}wintergreen}$ 'xkcd:wintergreen'|${\color{#ffe36e}yellow tan}$ 'xkcd:yellow tan'|${\color{#9d0759}dark fuchsia}$ 'xkcd:dark fuchsia'|
|--|--|--|
|${\color{#3a18b1}indigo blue}$ 'xkcd:indigo blue'|${\color{#c2ff89}light yellowish green}$ 'xkcd:light yellowish green'|${\color{#d767ad}pale magenta}$ 'xkcd:pale magenta'|
|--|--|--|
|${\color{#720058}rich purple}$ 'xkcd:rich purple'|${\color{#ffda03}sunflower yellow}$ 'xkcd:sunflower yellow'|${\color{#01c08d}green/blue}$ 'xkcd:green/blue'|
|--|--|--|
|${\color{#ac7434}leather}$ 'xkcd:leather'|${\color{#014600}racing green}$ 'xkcd:racing green'|${\color{#9900fa}vivid purple}$ 'xkcd:vivid purple'|
|--|--|--|
|${\color{#02066f}dark royal blue}$ 'xkcd:dark royal blue'|${\color{#8e7618}hazel}$ 'xkcd:hazel'|${\color{#d1768f}muted pink}$ 'xkcd:muted pink'|
|--|--|--|
|${\color{#96b403}booger green}$ 'xkcd:booger green'|${\color{#fdff63}canary}$ 'xkcd:canary'|${\color{#95a3a6}cool grey}$ 'xkcd:cool grey'|
|--|--|--|
|${\color{#7f684e}dark taupe}$ 'xkcd:dark taupe'|${\color{#751973}darkish purple}$ 'xkcd:darkish purple'|${\color{#089404}true green}$ 'xkcd:true green'|
|--|--|--|
|${\color{#ff6163}coral pink}$ 'xkcd:coral pink'|${\color{#598556}dark sage}$ 'xkcd:dark sage'|${\color{#214761}dark slate blue}$ 'xkcd:dark slate blue'|
|--|--|--|
|${\color{#3c73a8}flat blue}$ 'xkcd:flat blue'|${\color{#ba9e88}mushroom}$ 'xkcd:mushroom'|${\color{#021bf9}rich blue}$ 'xkcd:rich blue'|
|--|--|--|
|${\color{#734a65}dirty purple}$ 'xkcd:dirty purple'|${\color{#23c48b}greenblue}$ 'xkcd:greenblue'|${\color{#8fae22}icky green}$ 'xkcd:icky green'|
|--|--|--|
|${\color{#e6f2a2}light khaki}$ 'xkcd:light khaki'|${\color{#4b57db}warm blue}$ 'xkcd:warm blue'|${\color{#d90166}dark hot pink}$ 'xkcd:dark hot pink'|
|--|--|--|
|${\color{#015482}deep sea blue}$ 'xkcd:deep sea blue'|${\color{#9d0216}carmine}$ 'xkcd:carmine'|${\color{#728f02}dark yellow green}$ 'xkcd:dark yellow green'|
|--|--|--|
|${\color{#ffe5ad}pale peach}$ 'xkcd:pale peach'|${\color{#4e0550}plum purple}$ 'xkcd:plum purple'|${\color{#f9bc08}golden rod}$ 'xkcd:golden rod'|
|--|--|--|
|${\color{#ff073a}neon red}$ 'xkcd:neon red'|${\color{#c77986}old pink}$ 'xkcd:old pink'|${\color{#d6fffe}very pale blue}$ 'xkcd:very pale blue'|
|--|--|--|
|${\color{#fe4b03}blood orange}$ 'xkcd:blood orange'|${\color{#fd5956}grapefruit}$ 'xkcd:grapefruit'|${\color{#fce166}sand yellow}$ 'xkcd:sand yellow'|
|--|--|--|
|${\color{#b2713d}clay brown}$ 'xkcd:clay brown'|${\color{#1f3b4d}dark blue grey}$ 'xkcd:dark blue grey'|${\color{#699d4c}flat green}$ 'xkcd:flat green'|
|--|--|--|
|${\color{#56fca2}light green blue}$ 'xkcd:light green blue'|${\color{#fb5581}warm pink}$ 'xkcd:warm pink'|${\color{#3e82fc}dodger blue}$ 'xkcd:dodger blue'|
|--|--|--|
|${\color{#a0bf16}gross green}$ 'xkcd:gross green'|${\color{#d6fffa}ice}$ 'xkcd:ice'|${\color{#4f738e}metallic blue}$ 'xkcd:metallic blue'|
|--|--|--|
|${\color{#ffb19a}pale salmon}$ 'xkcd:pale salmon'|${\color{#5c8b15}sap green}$ 'xkcd:sap green'|${\color{#54ac68}algae}$ 'xkcd:algae'|
|--|--|--|
|${\color{#89a0b0}bluey grey}$ 'xkcd:bluey grey'|${\color{#7ea07a}greeny grey}$ 'xkcd:greeny grey'|${\color{#1bfc06}highlighter green}$ 'xkcd:highlighter green'|
|--|--|--|
|${\color{#cafffb}light light blue}$ 'xkcd:light light blue'|${\color{#b6ffbb}light mint}$ 'xkcd:light mint'|${\color{#a75e09}raw umber}$ 'xkcd:raw umber'|
|--|--|--|
|${\color{#152eff}vivid blue}$ 'xkcd:vivid blue'|${\color{#8d5eb7}deep lavender}$ 'xkcd:deep lavender'|${\color{#5f9e8f}dull teal}$ 'xkcd:dull teal'|
|--|--|--|
|${\color{#63f7b4}light greenish blue}$ 'xkcd:light greenish blue'|${\color{#606602}mud green}$ 'xkcd:mud green'|${\color{#fc86aa}pinky}$ 'xkcd:pinky'|
|--|--|--|
|${\color{#8c0034}red wine}$ 'xkcd:red wine'|${\color{#758000}shit green}$ 'xkcd:shit green'|${\color{#ab7e4c}tan brown}$ 'xkcd:tan brown'|
|--|--|--|
|${\color{#030764}darkblue}$ 'xkcd:darkblue'|${\color{#fe86a4}rosa}$ 'xkcd:rosa'|${\color{#d5174e}lipstick}$ 'xkcd:lipstick'|
|--|--|--|
|${\color{#fed0fc}pale mauve}$ 'xkcd:pale mauve'|${\color{#680018}claret}$ 'xkcd:claret'|${\color{#fedf08}dandelion}$ 'xkcd:dandelion'|
|--|--|--|
|${\color{#fe420f}orangered}$ 'xkcd:orangered'|${\color{#6f7c00}poop green}$ 'xkcd:poop green'|${\color{#ca0147}ruby}$ 'xkcd:ruby'|
|--|--|--|
|${\color{#1b2431}dark}$ 'xkcd:dark'|${\color{#00fbb0}greenish turquoise}$ 'xkcd:greenish turquoise'|${\color{#db5856}pastel red}$ 'xkcd:pastel red'|
|--|--|--|
|${\color{#ddd618}piss yellow}$ 'xkcd:piss yellow'|${\color{#41fdfe}bright cyan}$ 'xkcd:bright cyan'|${\color{#cf524e}dark coral}$ 'xkcd:dark coral'|
|--|--|--|
|${\color{#21c36f}algae green}$ 'xkcd:algae green'|${\color{#a90308}darkish red}$ 'xkcd:darkish red'|${\color{#6e1005}reddy brown}$ 'xkcd:reddy brown'|
|--|--|--|
|${\color{#fe828c}blush pink}$ 'xkcd:blush pink'|${\color{#4b6113}camouflage green}$ 'xkcd:camouflage green'|${\color{#4da409}lawn green}$ 'xkcd:lawn green'|
|--|--|--|
|${\color{#beae8a}putty}$ 'xkcd:putty'|${\color{#0339f8}vibrant blue}$ 'xkcd:vibrant blue'|${\color{#a88f59}dark sand}$ 'xkcd:dark sand'|
|--|--|--|
|${\color{#5d21d0}purple/blue}$ 'xkcd:purple/blue'|${\color{#feb209}saffron}$ 'xkcd:saffron'|${\color{#4e518b}twilight}$ 'xkcd:twilight'|
|--|--|--|
|${\color{#964e02}warm brown}$ 'xkcd:warm brown'|${\color{#85a3b2}bluegrey}$ 'xkcd:bluegrey'|${\color{#ff69af}bubble gum pink}$ 'xkcd:bubble gum pink'|
|--|--|--|
|${\color{#c3fbf4}duck egg blue}$ 'xkcd:duck egg blue'|${\color{#2afeb7}greenish cyan}$ 'xkcd:greenish cyan'|${\color{#005f6a}petrol}$ 'xkcd:petrol'|
|--|--|--|
|${\color{#0c1793}royal}$ 'xkcd:royal'|${\color{#ffff81}butter}$ 'xkcd:butter'|${\color{#f0833a}dusty orange}$ 'xkcd:dusty orange'|
|--|--|--|
|${\color{#f1f33f}off yellow}$ 'xkcd:off yellow'|${\color{#b1d27b}pale olive green}$ 'xkcd:pale olive green'|${\color{#fc824a}orangish}$ 'xkcd:orangish'|
|--|--|--|
|${\color{#71aa34}leaf}$ 'xkcd:leaf'|${\color{#b7c9e2}light blue grey}$ 'xkcd:light blue grey'|${\color{#4b0101}dried blood}$ 'xkcd:dried blood'|
|--|--|--|
|${\color{#a552e6}lightish purple}$ 'xkcd:lightish purple'|${\color{#af2f0d}rusty red}$ 'xkcd:rusty red'|${\color{#8b88f8}lavender blue}$ 'xkcd:lavender blue'|
|--|--|--|
|${\color{#9af764}light grass green}$ 'xkcd:light grass green'|${\color{#a6fbb2}light mint green}$ 'xkcd:light mint green'|${\color{#ffc512}sunflower}$ 'xkcd:sunflower'|
|--|--|--|
|${\color{#750851}velvet}$ 'xkcd:velvet'|${\color{#c14a09}brick orange}$ 'xkcd:brick orange'|${\color{#fe2f4a}lightish red}$ 'xkcd:lightish red'|
|--|--|--|
|${\color{#0203e2}pure blue}$ 'xkcd:pure blue'|${\color{#0a437a}twilight blue}$ 'xkcd:twilight blue'|${\color{#a50055}violet red}$ 'xkcd:violet red'|
|--|--|--|
|${\color{#ae8b0c}yellowy brown}$ 'xkcd:yellowy brown'|${\color{#fd798f}carnation}$ 'xkcd:carnation'|${\color{#bfac05}muddy yellow}$ 'xkcd:muddy yellow'|
|--|--|--|
|${\color{#3eaf76}dark seafoam green}$ 'xkcd:dark seafoam green'|${\color{#c74767}deep rose}$ 'xkcd:deep rose'|${\color{#b9484e}dusty red}$ 'xkcd:dusty red'|
|--|--|--|
|${\color{#647d8e}grey/blue}$ 'xkcd:grey/blue'|${\color{#bffe28}lemon lime}$ 'xkcd:lemon lime'|${\color{#d725de}purple/pink}$ 'xkcd:purple/pink'|
|--|--|--|
|${\color{#b29705}brown yellow}$ 'xkcd:brown yellow'|${\color{#673a3f}purple brown}$ 'xkcd:purple brown'|${\color{#a87dc2}wisteria}$ 'xkcd:wisteria'|
|--|--|--|
|${\color{#fafe4b}banana yellow}$ 'xkcd:banana yellow'|${\color{#c0022f}lipstick red}$ 'xkcd:lipstick red'|${\color{#0e87cc}water blue}$ 'xkcd:water blue'|
|--|--|--|
|${\color{#8d8468}brown grey}$ 'xkcd:brown grey'|${\color{#ad03de}vibrant purple}$ 'xkcd:vibrant purple'|${\color{#8cff9e}baby green}$ 'xkcd:baby green'|
|--|--|--|
|${\color{#94ac02}barf green}$ 'xkcd:barf green'|${\color{#c4fff7}eggshell blue}$ 'xkcd:eggshell blue'|${\color{#fdee73}sandy yellow}$ 'xkcd:sandy yellow'|
|--|--|--|
|${\color{#33b864}cool green}$ 'xkcd:cool green'|${\color{#fff9d0}pale}$ 'xkcd:pale'|${\color{#758da3}blue/grey}$ 'xkcd:blue/grey'|
|--|--|--|
|${\color{#f504c9}hot magenta}$ 'xkcd:hot magenta'|${\color{#77a1b5}greyblue}$ 'xkcd:greyblue'|${\color{#8756e4}purpley}$ 'xkcd:purpley'|
|--|--|--|
|${\color{#889717}baby shit green}$ 'xkcd:baby shit green'|${\color{#c27e79}brownish pink}$ 'xkcd:brownish pink'|${\color{#017371}dark aquamarine}$ 'xkcd:dark aquamarine'|
|--|--|--|
|${\color{#9f8303}diarrhea}$ 'xkcd:diarrhea'|${\color{#f7d560}light mustard}$ 'xkcd:light mustard'|${\color{#bdf6fe}pale sky blue}$ 'xkcd:pale sky blue'|
|--|--|--|
|${\color{#75b84f}turtle green}$ 'xkcd:turtle green'|${\color{#9cbb04}bright olive}$ 'xkcd:bright olive'|${\color{#29465b}dark grey blue}$ 'xkcd:dark grey blue'|
|--|--|--|
|${\color{#696006}greeny brown}$ 'xkcd:greeny brown'|${\color{#adf802}lemon green}$ 'xkcd:lemon green'|${\color{#c1c6fc}light periwinkle}$ 'xkcd:light periwinkle'|
|--|--|--|
|${\color{#35ad6b}seaweed green}$ 'xkcd:seaweed green'|${\color{#fffd37}sunshine yellow}$ 'xkcd:sunshine yellow'|${\color{#a442a0}ugly purple}$ 'xkcd:ugly purple'|
|--|--|--|
|${\color{#f36196}medium pink}$ 'xkcd:medium pink'|${\color{#947706}puke brown}$ 'xkcd:puke brown'|${\color{#fff4f2}very light pink}$ 'xkcd:very light pink'|
|--|--|--|
|${\color{#1e9167}viridian}$ 'xkcd:viridian'|${\color{#b5c306}bile}$ 'xkcd:bile'|${\color{#feff7f}faded yellow}$ 'xkcd:faded yellow'|
|--|--|--|
|${\color{#cffdbc}very pale green}$ 'xkcd:very pale green'|${\color{#0add08}vibrant green}$ 'xkcd:vibrant green'|${\color{#87fd05}bright lime}$ 'xkcd:bright lime'|
|--|--|--|
|${\color{#1ef876}spearmint}$ 'xkcd:spearmint'|${\color{#7bfdc7}light aquamarine}$ 'xkcd:light aquamarine'|${\color{#bcecac}light sage}$ 'xkcd:light sage'|
|--|--|--|
|${\color{#bbf90f}yellowgreen}$ 'xkcd:yellowgreen'|${\color{#ab9004}baby poo}$ 'xkcd:baby poo'|${\color{#1fb57a}dark seafoam}$ 'xkcd:dark seafoam'|
|--|--|--|
|${\color{#00555a}deep teal}$ 'xkcd:deep teal'|${\color{#a484ac}heather}$ 'xkcd:heather'|${\color{#c45508}rust orange}$ 'xkcd:rust orange'|
|--|--|--|
|${\color{#3f829d}dirty blue}$ 'xkcd:dirty blue'|${\color{#548d44}fern green}$ 'xkcd:fern green'|${\color{#c95efb}bright lilac}$ 'xkcd:bright lilac'|
|--|--|--|
|${\color{#3ae57f}weird green}$ 'xkcd:weird green'|${\color{#016795}peacock blue}$ 'xkcd:peacock blue'|${\color{#87a922}avocado green}$ 'xkcd:avocado green'|
|--|--|--|
|${\color{#f0944d}faded orange}$ 'xkcd:faded orange'|${\color{#5d1451}grape purple}$ 'xkcd:grape purple'|${\color{#25ff29}hot green}$ 'xkcd:hot green'|
|--|--|--|
|${\color{#d0fe1d}lime yellow}$ 'xkcd:lime yellow'|${\color{#ffa62b}mango}$ 'xkcd:mango'|${\color{#01b44c}shamrock}$ 'xkcd:shamrock'|
|--|--|--|
|${\color{#ff6cb5}bubblegum}$ 'xkcd:bubblegum'|${\color{#6b4247}purplish brown}$ 'xkcd:purplish brown'|${\color{#c7c10c}vomit yellow}$ 'xkcd:vomit yellow'|
|--|--|--|
|${\color{#b7fffa}pale cyan}$ 'xkcd:pale cyan'|${\color{#aeff6e}key lime}$ 'xkcd:key lime'|${\color{#ec2d01}tomato red}$ 'xkcd:tomato red'|
|--|--|--|
|${\color{#76ff7b}lightgreen}$ 'xkcd:lightgreen'|${\color{#730039}merlot}$ 'xkcd:merlot'|${\color{#040348}night blue}$ 'xkcd:night blue'|
|--|--|--|
|${\color{#df4ec8}purpleish pink}$ 'xkcd:purpleish pink'|${\color{#6ecb3c}apple}$ 'xkcd:apple'|${\color{#8f9805}baby poop green}$ 'xkcd:baby poop green'|
|--|--|--|
|${\color{#5edc1f}green apple}$ 'xkcd:green apple'|${\color{#d94ff5}heliotrope}$ 'xkcd:heliotrope'|${\color{#c8fd3d}yellow/green}$ 'xkcd:yellow/green'|
|--|--|--|
|${\color{#070d0d}almost black}$ 'xkcd:almost black'|${\color{#4984b8}cool blue}$ 'xkcd:cool blue'|${\color{#51b73b}leafy green}$ 'xkcd:leafy green'|
|--|--|--|
|${\color{#ac7e04}mustard brown}$ 'xkcd:mustard brown'|${\color{#4e5481}dusk}$ 'xkcd:dusk'|${\color{#876e4b}dull brown}$ 'xkcd:dull brown'|
|--|--|--|
|${\color{#58bc08}frog green}$ 'xkcd:frog green'|${\color{#2fef10}vivid green}$ 'xkcd:vivid green'|${\color{#2dfe54}bright light green}$ 'xkcd:bright light green'|
|--|--|--|
|${\color{#0aff02}fluro green}$ 'xkcd:fluro green'|${\color{#9cef43}kiwi}$ 'xkcd:kiwi'|${\color{#18d17b}seaweed}$ 'xkcd:seaweed'|
|--|--|--|
|${\color{#35530a}navy green}$ 'xkcd:navy green'|${\color{#1805db}ultramarine blue}$ 'xkcd:ultramarine blue'|${\color{#6258c4}iris}$ 'xkcd:iris'|
|--|--|--|
|${\color{#ff964f}pastel orange}$ 'xkcd:pastel orange'|${\color{#ffab0f}yellowish orange}$ 'xkcd:yellowish orange'|${\color{#8f8ce7}perrywinkle}$ 'xkcd:perrywinkle'|
|--|--|--|
|${\color{#24bca8}tealish}$ 'xkcd:tealish'|${\color{#3f012c}dark plum}$ 'xkcd:dark plum'|${\color{#cbf85f}pear}$ 'xkcd:pear'|
|--|--|--|
|${\color{#ff724c}pinkish orange}$ 'xkcd:pinkish orange'|${\color{#280137}midnight purple}$ 'xkcd:midnight purple'|${\color{#b36ff6}light urple}$ 'xkcd:light urple'|
|--|--|--|
|${\color{#48c072}dark mint}$ 'xkcd:dark mint'|${\color{#bccb7a}greenish tan}$ 'xkcd:greenish tan'|${\color{#a8415b}light burgundy}$ 'xkcd:light burgundy'|
|--|--|--|
|${\color{#06b1c4}turquoise blue}$ 'xkcd:turquoise blue'|${\color{#cd7584}ugly pink}$ 'xkcd:ugly pink'|${\color{#f1da7a}sandy}$ 'xkcd:sandy'|
|--|--|--|
|${\color{#ff0490}electric pink}$ 'xkcd:electric pink'|${\color{#805b87}muted purple}$ 'xkcd:muted purple'|${\color{#50a747}mid green}$ 'xkcd:mid green'|
|--|--|--|
|${\color{#a8a495}greyish}$ 'xkcd:greyish'|${\color{#cfff04}neon yellow}$ 'xkcd:neon yellow'|${\color{#ffff7e}banana}$ 'xkcd:banana'|
|--|--|--|
|${\color{#ff7fa7}carnation pink}$ 'xkcd:carnation pink'|${\color{#ef4026}tomato}$ 'xkcd:tomato'|${\color{#3c9992}sea}$ 'xkcd:sea'|
|--|--|--|
|${\color{#886806}muddy brown}$ 'xkcd:muddy brown'|${\color{#04f489}turquoise green}$ 'xkcd:turquoise green'|${\color{#fef69e}buff}$ 'xkcd:buff'|
|--|--|--|
|${\color{#cfaf7b}fawn}$ 'xkcd:fawn'|${\color{#3b719f}muted blue}$ 'xkcd:muted blue'|${\color{#fdc1c5}pale rose}$ 'xkcd:pale rose'|
|--|--|--|
|${\color{#20c073}dark mint green}$ 'xkcd:dark mint green'|${\color{#9b5fc0}amethyst}$ 'xkcd:amethyst'|${\color{#0f9b8e}blue/green}$ 'xkcd:blue/green'|
|--|--|--|
|${\color{#742802}chestnut}$ 'xkcd:chestnut'|${\color{#9db92c}sick green}$ 'xkcd:sick green'|${\color{#a4bf20}pea}$ 'xkcd:pea'|
|--|--|--|
|${\color{#cd5909}rusty orange}$ 'xkcd:rusty orange'|${\color{#ada587}stone}$ 'xkcd:stone'|${\color{#be013c}rose red}$ 'xkcd:rose red'|
|--|--|--|
|${\color{#b8ffeb}pale aqua}$ 'xkcd:pale aqua'|${\color{#dc4d01}deep orange}$ 'xkcd:deep orange'|${\color{#a2653e}earth}$ 'xkcd:earth'|
|--|--|--|
|${\color{#638b27}mossy green}$ 'xkcd:mossy green'|${\color{#419c03}grassy green}$ 'xkcd:grassy green'|${\color{#b1ff65}pale lime green}$ 'xkcd:pale lime green'|
|--|--|--|
|${\color{#9dbcd4}light grey blue}$ 'xkcd:light grey blue'|${\color{#fdfdfe}pale grey}$ 'xkcd:pale grey'|${\color{#77ab56}asparagus}$ 'xkcd:asparagus'|
|--|--|--|
|${\color{#464196}blueberry}$ 'xkcd:blueberry'|${\color{#990147}purple red}$ 'xkcd:purple red'|${\color{#befd73}pale lime}$ 'xkcd:pale lime'|
|--|--|--|
|${\color{#32bf84}greenish teal}$ 'xkcd:greenish teal'|${\color{#af6f09}caramel}$ 'xkcd:caramel'|${\color{#a0025c}deep magenta}$ 'xkcd:deep magenta'|
|--|--|--|
|${\color{#ffd8b1}light peach}$ 'xkcd:light peach'|${\color{#7f4e1e}milk chocolate}$ 'xkcd:milk chocolate'|${\color{#bf9b0c}ocher}$ 'xkcd:ocher'|
|--|--|--|
|${\color{#6ba353}off green}$ 'xkcd:off green'|${\color{#f075e6}purply pink}$ 'xkcd:purply pink'|${\color{#7bc8f6}lightblue}$ 'xkcd:lightblue'|
|--|--|--|
|${\color{#475f94}dusky blue}$ 'xkcd:dusky blue'|${\color{#f5bf03}golden}$ 'xkcd:golden'|${\color{#fffeb6}light beige}$ 'xkcd:light beige'|
|--|--|--|
|${\color{#fffd74}butter yellow}$ 'xkcd:butter yellow'|${\color{#895b7b}dusky purple}$ 'xkcd:dusky purple'|${\color{#436bad}french blue}$ 'xkcd:french blue'|
|--|--|--|
|${\color{#d0c101}ugly yellow}$ 'xkcd:ugly yellow'|${\color{#c6f808}greeny yellow}$ 'xkcd:greeny yellow'|${\color{#f43605}orangish red}$ 'xkcd:orangish red'|
|--|--|--|
|${\color{#02c14d}shamrock green}$ 'xkcd:shamrock green'|${\color{#b25f03}orangish brown}$ 'xkcd:orangish brown'|${\color{#2a7e19}tree green}$ 'xkcd:tree green'|
|--|--|--|
|${\color{#490648}deep violet}$ 'xkcd:deep violet'|${\color{#536267}gunmetal}$ 'xkcd:gunmetal'|${\color{#5a06ef}blue/purple}$ 'xkcd:blue/purple'|
|--|--|--|
|${\color{#cf0234}cherry}$ 'xkcd:cherry'|${\color{#c4a661}sandy brown}$ 'xkcd:sandy brown'|${\color{#978a84}warm grey}$ 'xkcd:warm grey'|
|--|--|--|
|${\color{#1f0954}dark indigo}$ 'xkcd:dark indigo'|${\color{#03012d}midnight}$ 'xkcd:midnight'|${\color{#2bb179}bluey green}$ 'xkcd:bluey green'|
|--|--|--|
|${\color{#c3909b}grey pink}$ 'xkcd:grey pink'|${\color{#a66fb5}soft purple}$ 'xkcd:soft purple'|${\color{#770001}blood}$ 'xkcd:blood'|
|--|--|--|
|${\color{#922b05}brown red}$ 'xkcd:brown red'|${\color{#7d7f7c}medium grey}$ 'xkcd:medium grey'|${\color{#990f4b}berry}$ 'xkcd:berry'|
|--|--|--|
|${\color{#8f7303}poo}$ 'xkcd:poo'|${\color{#c83cb9}purpley pink}$ 'xkcd:purpley pink'|${\color{#fea993}light salmon}$ 'xkcd:light salmon'|
|--|--|--|
|${\color{#acbb0d}snot}$ 'xkcd:snot'|${\color{#c071fe}easter purple}$ 'xkcd:easter purple'|${\color{#ccfd7f}light yellow green}$ 'xkcd:light yellow green'|
|--|--|--|
|${\color{#00022e}dark navy blue}$ 'xkcd:dark navy blue'|${\color{#828344}drab}$ 'xkcd:drab'|${\color{#ffc5cb}light rose}$ 'xkcd:light rose'|
|--|--|--|
|${\color{#ab1239}rouge}$ 'xkcd:rouge'|${\color{#b0054b}purplish red}$ 'xkcd:purplish red'|${\color{#99cc04}slime green}$ 'xkcd:slime green'|
|--|--|--|
|${\color{#937c00}baby poop}$ 'xkcd:baby poop'|${\color{#019529}irish green}$ 'xkcd:irish green'|${\color{#ef1de7}pink/purple}$ 'xkcd:pink/purple'|
|--|--|--|
|${\color{#000435}dark navy}$ 'xkcd:dark navy'|${\color{#42b395}greeny blue}$ 'xkcd:greeny blue'|${\color{#9d5783}light plum}$ 'xkcd:light plum'|
|--|--|--|
|${\color{#c8aca9}pinkish grey}$ 'xkcd:pinkish grey'|${\color{#c87606}dirty orange}$ 'xkcd:dirty orange'|${\color{#aa2704}rust red}$ 'xkcd:rust red'|
|--|--|--|
|${\color{#e4cbff}pale lilac}$ 'xkcd:pale lilac'|${\color{#fa4224}orangey red}$ 'xkcd:orangey red'|${\color{#0804f9}primary blue}$ 'xkcd:primary blue'|
|--|--|--|
|${\color{#5cb200}kermit green}$ 'xkcd:kermit green'|${\color{#76424e}brownish purple}$ 'xkcd:brownish purple'|${\color{#6c7a0e}murky green}$ 'xkcd:murky green'|
|--|--|--|
|${\color{#fbdd7e}wheat}$ 'xkcd:wheat'|${\color{#2a0134}very dark purple}$ 'xkcd:very dark purple'|${\color{#044a05}bottle green}$ 'xkcd:bottle green'|
|--|--|--|
|${\color{#fd4659}watermelon}$ 'xkcd:watermelon'|${\color{#0d75f8}deep sky blue}$ 'xkcd:deep sky blue'|${\color{#fe0002}fire engine red}$ 'xkcd:fire engine red'|
|--|--|--|
|${\color{#cb9d06}yellow ochre}$ 'xkcd:yellow ochre'|${\color{#fb7d07}pumpkin orange}$ 'xkcd:pumpkin orange'|${\color{#b9cc81}pale olive}$ 'xkcd:pale olive'|
|--|--|--|
|${\color{#edc8ff}light lilac}$ 'xkcd:light lilac'|${\color{#61e160}lightish green}$ 'xkcd:lightish green'|${\color{#8ab8fe}carolina blue}$ 'xkcd:carolina blue'|
|--|--|--|
|${\color{#920a4e}mulberry}$ 'xkcd:mulberry'|${\color{#fe02a2}shocking pink}$ 'xkcd:shocking pink'|${\color{#9a3001}auburn}$ 'xkcd:auburn'|
|--|--|--|
|${\color{#65fe08}bright lime green}$ 'xkcd:bright lime green'|${\color{#befdb7}celadon}$ 'xkcd:celadon'|${\color{#b17261}pinkish brown}$ 'xkcd:pinkish brown'|
|--|--|--|
|${\color{#885f01}poo brown}$ 'xkcd:poo brown'|${\color{#02ccfe}bright sky blue}$ 'xkcd:bright sky blue'|${\color{#c1fd95}celery}$ 'xkcd:celery'|
|--|--|--|
|${\color{#836539}dirt brown}$ 'xkcd:dirt brown'|${\color{#fb2943}strawberry}$ 'xkcd:strawberry'|${\color{#84b701}dark lime}$ 'xkcd:dark lime'|
|--|--|--|
|${\color{#b66325}copper}$ 'xkcd:copper'|${\color{#7f5112}medium brown}$ 'xkcd:medium brown'|${\color{#5fa052}muted green}$ 'xkcd:muted green'|
|--|--|--|
|${\color{#6dedfd}robin's egg}$ 'xkcd:robin's egg'|${\color{#0bf9ea}bright aqua}$ 'xkcd:bright aqua'|${\color{#c760ff}bright lavender}$ 'xkcd:bright lavender'|
|--|--|--|
|${\color{#ffffcb}ivory}$ 'xkcd:ivory'|${\color{#f6cefc}very light purple}$ 'xkcd:very light purple'|${\color{#155084}light navy}$ 'xkcd:light navy'|
|--|--|--|
|${\color{#f5054f}pink red}$ 'xkcd:pink red'|${\color{#645403}olive brown}$ 'xkcd:olive brown'|${\color{#7a5901}poop brown}$ 'xkcd:poop brown'|
|--|--|--|
|${\color{#a8b504}mustard green}$ 'xkcd:mustard green'|${\color{#3d9973}ocean green}$ 'xkcd:ocean green'|${\color{#000133}very dark blue}$ 'xkcd:very dark blue'|
|--|--|--|
|${\color{#76a973}dusty green}$ 'xkcd:dusty green'|${\color{#2e5a88}light navy blue}$ 'xkcd:light navy blue'|${\color{#0bf77d}minty green}$ 'xkcd:minty green'|
|--|--|--|
|${\color{#bd6c48}adobe}$ 'xkcd:adobe'|${\color{#ac1db8}barney}$ 'xkcd:barney'|${\color{#2baf6a}jade green}$ 'xkcd:jade green'|
|--|--|--|
|${\color{#26f7fd}bright light blue}$ 'xkcd:bright light blue'|${\color{#aefd6c}light lime}$ 'xkcd:light lime'|${\color{#9b8f55}dark khaki}$ 'xkcd:dark khaki'|
|--|--|--|
|${\color{#ffad01}orange yellow}$ 'xkcd:orange yellow'|${\color{#c69c04}ocre}$ 'xkcd:ocre'|${\color{#f4d054}maize}$ 'xkcd:maize'|
|--|--|--|
|${\color{#de9dac}faded pink}$ 'xkcd:faded pink'|${\color{#05480d}british racing green}$ 'xkcd:british racing green'|${\color{#c9ae74}sandstone}$ 'xkcd:sandstone'|
|--|--|--|
|${\color{#60460f}mud brown}$ 'xkcd:mud brown'|${\color{#98f6b0}light sea green}$ 'xkcd:light sea green'|${\color{#8af1fe}robin egg blue}$ 'xkcd:robin egg blue'|
|--|--|--|
|${\color{#2ee8bb}aqua marine}$ 'xkcd:aqua marine'|${\color{#11875d}dark sea green}$ 'xkcd:dark sea green'|${\color{#fdb0c0}soft pink}$ 'xkcd:soft pink'|
|--|--|--|
|${\color{#b16002}orangey brown}$ 'xkcd:orangey brown'|${\color{#f7022a}cherry red}$ 'xkcd:cherry red'|${\color{#d5ab09}burnt yellow}$ 'xkcd:burnt yellow'|
|--|--|--|
|${\color{#86775f}brownish grey}$ 'xkcd:brownish grey'|${\color{#c69f59}camel}$ 'xkcd:camel'|${\color{#7a687f}purplish grey}$ 'xkcd:purplish grey'|
|--|--|--|
|${\color{#042e60}marine}$ 'xkcd:marine'|${\color{#c88d94}greyish pink}$ 'xkcd:greyish pink'|${\color{#a5fbd5}pale turquoise}$ 'xkcd:pale turquoise'|
|--|--|--|
|${\color{#fffe71}pastel yellow}$ 'xkcd:pastel yellow'|${\color{#6241c7}bluey purple}$ 'xkcd:bluey purple'|${\color{#fffe40}canary yellow}$ 'xkcd:canary yellow'|
|--|--|--|
|${\color{#d3494e}faded red}$ 'xkcd:faded red'|${\color{#985e2b}sepia}$ 'xkcd:sepia'|${\color{#a6814c}coffee}$ 'xkcd:coffee'|
|--|--|--|
|${\color{#ff08e8}bright magenta}$ 'xkcd:bright magenta'|${\color{#9d7651}mocha}$ 'xkcd:mocha'|${\color{#feffca}ecru}$ 'xkcd:ecru'|
|--|--|--|
|${\color{#98568d}purpleish}$ 'xkcd:purpleish'|${\color{#9e003a}cranberry}$ 'xkcd:cranberry'|${\color{#287c37}darkish green}$ 'xkcd:darkish green'|
|--|--|--|
|${\color{#b96902}brown orange}$ 'xkcd:brown orange'|${\color{#ba6873}dusky rose}$ 'xkcd:dusky rose'|${\color{#ff7855}melon}$ 'xkcd:melon'|
|--|--|--|
|${\color{#94b21c}sickly green}$ 'xkcd:sickly green'|${\color{#c5c9c7}silver}$ 'xkcd:silver'|${\color{#661aee}purply blue}$ 'xkcd:purply blue'|
|--|--|--|
|${\color{#6140ef}purpleish blue}$ 'xkcd:purpleish blue'|${\color{#9be5aa}hospital green}$ 'xkcd:hospital green'|${\color{#7b5804}shit brown}$ 'xkcd:shit brown'|
|--|--|--|
|${\color{#276ab3}mid blue}$ 'xkcd:mid blue'|${\color{#feb308}amber}$ 'xkcd:amber'|${\color{#8cfd7e}easter green}$ 'xkcd:easter green'|
|--|--|--|
|${\color{#6488ea}soft blue}$ 'xkcd:soft blue'|${\color{#056eee}cerulean blue}$ 'xkcd:cerulean blue'|${\color{#b27a01}golden brown}$ 'xkcd:golden brown'|
|--|--|--|
|${\color{#0ffef9}bright turquoise}$ 'xkcd:bright turquoise'|${\color{#fa2a55}red pink}$ 'xkcd:red pink'|${\color{#820747}red purple}$ 'xkcd:red purple'|
|--|--|--|
|${\color{#7a6a4f}greyish brown}$ 'xkcd:greyish brown'|${\color{#f4320c}vermillion}$ 'xkcd:vermillion'|${\color{#a13905}russet}$ 'xkcd:russet'|
|--|--|--|
|${\color{#6f828a}steel grey}$ 'xkcd:steel grey'|${\color{#a55af4}lighter purple}$ 'xkcd:lighter purple'|${\color{#ad0afd}bright violet}$ 'xkcd:bright violet'|
|--|--|--|
|${\color{#004577}prussian blue}$ 'xkcd:prussian blue'|${\color{#658d6d}slate green}$ 'xkcd:slate green'|${\color{#ca7b80}dirty pink}$ 'xkcd:dirty pink'|
|--|--|--|
|${\color{#005249}dark blue green}$ 'xkcd:dark blue green'|${\color{#2b5d34}pine}$ 'xkcd:pine'|${\color{#bff128}yellowy green}$ 'xkcd:yellowy green'|
|--|--|--|
|${\color{#b59410}dark gold}$ 'xkcd:dark gold'|${\color{#2976bb}bluish}$ 'xkcd:bluish'|${\color{#014182}darkish blue}$ 'xkcd:darkish blue'|
|--|--|--|
|${\color{#bb3f3f}dull red}$ 'xkcd:dull red'|${\color{#fc2647}pinky red}$ 'xkcd:pinky red'|${\color{#a87900}bronze}$ 'xkcd:bronze'|
|--|--|--|
|${\color{#82cbb2}pale teal}$ 'xkcd:pale teal'|${\color{#667c3e}military green}$ 'xkcd:military green'|${\color{#fe46a5}barbie pink}$ 'xkcd:barbie pink'|
|--|--|--|
|${\color{#fe83cc}bubblegum pink}$ 'xkcd:bubblegum pink'|${\color{#94a617}pea soup green}$ 'xkcd:pea soup green'|${\color{#a88905}dark mustard}$ 'xkcd:dark mustard'|
|--|--|--|
|${\color{#7f5f00}shit}$ 'xkcd:shit'|${\color{#9e43a2}medium purple}$ 'xkcd:medium purple'|${\color{#062e03}very dark green}$ 'xkcd:very dark green'|
|--|--|--|
|${\color{#8a6e45}dirt}$ 'xkcd:dirt'|${\color{#cc7a8b}dusky pink}$ 'xkcd:dusky pink'|${\color{#9e0168}red violet}$ 'xkcd:red violet'|
|--|--|--|
|${\color{#fdff38}lemon yellow}$ 'xkcd:lemon yellow'|${\color{#c0fa8b}pistachio}$ 'xkcd:pistachio'|${\color{#eedc5b}dull yellow}$ 'xkcd:dull yellow'|
|--|--|--|
|${\color{#7ebd01}dark lime green}$ 'xkcd:dark lime green'|${\color{#3b5b92}denim blue}$ 'xkcd:denim blue'|${\color{#01889f}teal blue}$ 'xkcd:teal blue'|
|--|--|--|
|${\color{#3d7afd}lightish blue}$ 'xkcd:lightish blue'|${\color{#5f34e7}purpley blue}$ 'xkcd:purpley blue'|${\color{#6d5acf}light indigo}$ 'xkcd:light indigo'|
|--|--|--|
|${\color{#748500}swamp green}$ 'xkcd:swamp green'|${\color{#706c11}brown green}$ 'xkcd:brown green'|${\color{#3c0008}dark maroon}$ 'xkcd:dark maroon'|
|--|--|--|
|${\color{#cb00f5}hot purple}$ 'xkcd:hot purple'|${\color{#002d04}dark forest green}$ 'xkcd:dark forest green'|${\color{#658cbb}faded blue}$ 'xkcd:faded blue'|
|--|--|--|
|${\color{#749551}drab green}$ 'xkcd:drab green'|${\color{#b9ff66}light lime green}$ 'xkcd:light lime green'|${\color{#9dc100}snot green}$ 'xkcd:snot green'|
|--|--|--|
|${\color{#faee66}yellowish}$ 'xkcd:yellowish'|${\color{#7efbb3}light blue green}$ 'xkcd:light blue green'|${\color{#7b002c}bordeaux}$ 'xkcd:bordeaux'|
|--|--|--|
|${\color{#c292a1}light mauve}$ 'xkcd:light mauve'|${\color{#017b92}ocean}$ 'xkcd:ocean'|${\color{#fcc006}marigold}$ 'xkcd:marigold'|
|--|--|--|
|${\color{#657432}muddy green}$ 'xkcd:muddy green'|${\color{#d8863b}dull orange}$ 'xkcd:dull orange'|${\color{#738595}steel}$ 'xkcd:steel'|
|--|--|--|
|${\color{#aa23ff}electric purple}$ 'xkcd:electric purple'|${\color{#08ff08}fluorescent green}$ 'xkcd:fluorescent green'|${\color{#9b7a01}yellowish brown}$ 'xkcd:yellowish brown'|
|--|--|--|
|${\color{#f29e8e}blush}$ 'xkcd:blush'|${\color{#6fc276}soft green}$ 'xkcd:soft green'|${\color{#ff5b00}bright orange}$ 'xkcd:bright orange'|
|--|--|--|
|${\color{#fdff52}lemon}$ 'xkcd:lemon'|${\color{#866f85}purple grey}$ 'xkcd:purple grey'|${\color{#8ffe09}acid green}$ 'xkcd:acid green'|
|--|--|--|
|${\color{#eecffe}pale lavender}$ 'xkcd:pale lavender'|${\color{#510ac9}violet blue}$ 'xkcd:violet blue'|${\color{#4f9153}light forest green}$ 'xkcd:light forest green'|
|--|--|--|
|${\color{#9f2305}burnt red}$ 'xkcd:burnt red'|${\color{#728639}khaki green}$ 'xkcd:khaki green'|${\color{#de0c62}cerise}$ 'xkcd:cerise'|
|--|--|--|
|${\color{#916e99}faded purple}$ 'xkcd:faded purple'|${\color{#ffb16d}apricot}$ 'xkcd:apricot'|${\color{#3c4d03}dark olive green}$ 'xkcd:dark olive green'|
|--|--|--|
|${\color{#7f7053}grey brown}$ 'xkcd:grey brown'|${\color{#77926f}green grey}$ 'xkcd:green grey'|${\color{#010fcc}true blue}$ 'xkcd:true blue'|
|--|--|--|
|${\color{#ceaefa}pale violet}$ 'xkcd:pale violet'|${\color{#8f99fb}periwinkle blue}$ 'xkcd:periwinkle blue'|${\color{#c6fcff}light sky blue}$ 'xkcd:light sky blue'|
|--|--|--|
|${\color{#5539cc}blurple}$ 'xkcd:blurple'|${\color{#544e03}green brown}$ 'xkcd:green brown'|${\color{#017a79}bluegreen}$ 'xkcd:bluegreen'|
|--|--|--|
|${\color{#01f9c6}bright teal}$ 'xkcd:bright teal'|${\color{#c9b003}brownish yellow}$ 'xkcd:brownish yellow'|${\color{#929901}pea soup}$ 'xkcd:pea soup'|
|--|--|--|
|${\color{#0b5509}forest}$ 'xkcd:forest'|${\color{#a00498}barney purple}$ 'xkcd:barney purple'|${\color{#2000b1}ultramarine}$ 'xkcd:ultramarine'|
|--|--|--|
|${\color{#94568c}purplish}$ 'xkcd:purplish'|${\color{#c2be0e}puke yellow}$ 'xkcd:puke yellow'|${\color{#748b97}bluish grey}$ 'xkcd:bluish grey'|
|--|--|--|
|${\color{#665fd1}dark periwinkle}$ 'xkcd:dark periwinkle'|${\color{#9c6da5}dark lilac}$ 'xkcd:dark lilac'|${\color{#c44240}reddish}$ 'xkcd:reddish'|
|--|--|--|
|${\color{#a24857}light maroon}$ 'xkcd:light maroon'|${\color{#825f87}dusty purple}$ 'xkcd:dusty purple'|${\color{#c9643b}terra cotta}$ 'xkcd:terra cotta'|
|--|--|--|
|${\color{#90b134}avocado}$ 'xkcd:avocado'|${\color{#01386a}marine blue}$ 'xkcd:marine blue'|${\color{#25a36f}teal green}$ 'xkcd:teal green'|
|--|--|--|
|${\color{#59656d}slate grey}$ 'xkcd:slate grey'|${\color{#75fd63}lighter green}$ 'xkcd:lighter green'|${\color{#21fc0d}electric green}$ 'xkcd:electric green'|
|--|--|--|
|${\color{#5a86ad}dusty blue}$ 'xkcd:dusty blue'|${\color{#fec615}golden yellow}$ 'xkcd:golden yellow'|${\color{#fffd01}bright yellow}$ 'xkcd:bright yellow'|
|--|--|--|
|${\color{#dfc5fe}light lavender}$ 'xkcd:light lavender'|${\color{#b26400}umber}$ 'xkcd:umber'|${\color{#7f5e00}poop}$ 'xkcd:poop'|
|--|--|--|
|${\color{#de7e5d}dark peach}$ 'xkcd:dark peach'|${\color{#048243}jungle green}$ 'xkcd:jungle green'|${\color{#ffffd4}eggshell}$ 'xkcd:eggshell'|
|--|--|--|
|${\color{#3b638c}denim}$ 'xkcd:denim'|${\color{#b79400}yellow brown}$ 'xkcd:yellow brown'|${\color{#84597e}dull purple}$ 'xkcd:dull purple'|
|--|--|--|
|${\color{#411900}chocolate brown}$ 'xkcd:chocolate brown'|${\color{#7b0323}wine red}$ 'xkcd:wine red'|${\color{#04d9ff}neon blue}$ 'xkcd:neon blue'|
|--|--|--|
|${\color{#667e2c}dirty green}$ 'xkcd:dirty green'|${\color{#fbeeac}light tan}$ 'xkcd:light tan'|${\color{#d7fffe}ice blue}$ 'xkcd:ice blue'|
|--|--|--|
|${\color{#4e7496}cadet blue}$ 'xkcd:cadet blue'|${\color{#874c62}dark mauve}$ 'xkcd:dark mauve'|${\color{#d5ffff}very light blue}$ 'xkcd:very light blue'|
|--|--|--|
|${\color{#826d8c}grey purple}$ 'xkcd:grey purple'|${\color{#ffbacd}pastel pink}$ 'xkcd:pastel pink'|${\color{#d1ffbd}very light green}$ 'xkcd:very light green'|
|--|--|--|
|${\color{#448ee4}dark sky blue}$ 'xkcd:dark sky blue'|${\color{#05472a}evergreen}$ 'xkcd:evergreen'|${\color{#d5869d}dull pink}$ 'xkcd:dull pink'|
|--|--|--|
|${\color{#3d0734}aubergine}$ 'xkcd:aubergine'|${\color{#4a0100}mahogany}$ 'xkcd:mahogany'|${\color{#f8481c}reddish orange}$ 'xkcd:reddish orange'|
|--|--|--|
|${\color{#02590f}deep green}$ 'xkcd:deep green'|${\color{#89a203}vomit green}$ 'xkcd:vomit green'|${\color{#e03fd8}purple pink}$ 'xkcd:purple pink'|
|--|--|--|
|${\color{#d58a94}dusty pink}$ 'xkcd:dusty pink'|${\color{#7bb274}faded green}$ 'xkcd:faded green'|${\color{#526525}camo green}$ 'xkcd:camo green'|
|--|--|--|
|${\color{#c94cbe}pinky purple}$ 'xkcd:pinky purple'|${\color{#db4bda}pink purple}$ 'xkcd:pink purple'|${\color{#9e3623}brownish red}$ 'xkcd:brownish red'|
|--|--|--|
|${\color{#b5485d}dark rose}$ 'xkcd:dark rose'|${\color{#735c12}mud}$ 'xkcd:mud'|${\color{#9c6d57}brownish}$ 'xkcd:brownish'|
|--|--|--|
|${\color{#028f1e}emerald green}$ 'xkcd:emerald green'|${\color{#b1916e}pale brown}$ 'xkcd:pale brown'|${\color{#49759c}dull blue}$ 'xkcd:dull blue'|
|--|--|--|
|${\color{#a0450e}burnt umber}$ 'xkcd:burnt umber'|${\color{#39ad48}medium green}$ 'xkcd:medium green'|${\color{#b66a50}clay}$ 'xkcd:clay'|
|--|--|--|
|${\color{#8cffdb}light aqua}$ 'xkcd:light aqua'|${\color{#a4be5c}light olive green}$ 'xkcd:light olive green'|${\color{#cb7723}brownish orange}$ 'xkcd:brownish orange'|
|--|--|--|
|${\color{#05696b}dark aqua}$ 'xkcd:dark aqua'|${\color{#ce5dae}purplish pink}$ 'xkcd:purplish pink'|${\color{#c85a53}dark salmon}$ 'xkcd:dark salmon'|
|--|--|--|
|${\color{#96ae8d}greenish grey}$ 'xkcd:greenish grey'|${\color{#1fa774}jade}$ 'xkcd:jade'|${\color{#7a9703}ugly green}$ 'xkcd:ugly green'|
|--|--|--|
|${\color{#ac9362}dark beige}$ 'xkcd:dark beige'|${\color{#01a049}emerald}$ 'xkcd:emerald'|${\color{#d9544d}pale red}$ 'xkcd:pale red'|
|--|--|--|
|${\color{#fa5ff7}light magenta}$ 'xkcd:light magenta'|${\color{#82cafc}sky}$ 'xkcd:sky'|${\color{#acfffc}light cyan}$ 'xkcd:light cyan'|
|--|--|--|
|${\color{#fcb001}yellow orange}$ 'xkcd:yellow orange'|${\color{#910951}reddish purple}$ 'xkcd:reddish purple'|${\color{#fe2c54}reddish pink}$ 'xkcd:reddish pink'|
|--|--|--|
|${\color{#c875c4}orchid}$ 'xkcd:orchid'|${\color{#cdc50a}dirty yellow}$ 'xkcd:dirty yellow'|${\color{#fd411e}orange red}$ 'xkcd:orange red'|
|--|--|--|
|${\color{#9a0200}deep red}$ 'xkcd:deep red'|${\color{#be6400}orange brown}$ 'xkcd:orange brown'|${\color{#030aa7}cobalt blue}$ 'xkcd:cobalt blue'|
|--|--|--|
|${\color{#fe019a}neon pink}$ 'xkcd:neon pink'|${\color{#f7879a}rose pink}$ 'xkcd:rose pink'|${\color{#887191}greyish purple}$ 'xkcd:greyish purple'|
|--|--|--|
|${\color{#b00149}raspberry}$ 'xkcd:raspberry'|${\color{#12e193}aqua green}$ 'xkcd:aqua green'|${\color{#fe7b7c}salmon pink}$ 'xkcd:salmon pink'|
|--|--|--|
|${\color{#ff9408}tangerine}$ 'xkcd:tangerine'|${\color{#6a6e09}brownish green}$ 'xkcd:brownish green'|${\color{#8b2e16}red brown}$ 'xkcd:red brown'|
|--|--|--|
|${\color{#696112}greenish brown}$ 'xkcd:greenish brown'|${\color{#e17701}pumpkin}$ 'xkcd:pumpkin'|${\color{#0a481e}pine green}$ 'xkcd:pine green'|
|--|--|--|
|${\color{#343837}charcoal}$ 'xkcd:charcoal'|${\color{#ffb7ce}baby pink}$ 'xkcd:baby pink'|${\color{#6a79f7}cornflower}$ 'xkcd:cornflower'|
|--|--|--|
|${\color{#5d06e9}blue violet}$ 'xkcd:blue violet'|${\color{#3d1c02}chocolate}$ 'xkcd:chocolate'|${\color{#82a67d}greyish green}$ 'xkcd:greyish green'|
|--|--|--|
|${\color{#be0119}scarlet}$ 'xkcd:scarlet'|${\color{#c9ff27}green yellow}$ 'xkcd:green yellow'|${\color{#373e02}dark olive}$ 'xkcd:dark olive'|
|--|--|--|
|${\color{#a9561e}sienna}$ 'xkcd:sienna'|${\color{#caa0ff}pastel purple}$ 'xkcd:pastel purple'|${\color{#ca6641}terracotta}$ 'xkcd:terracotta'|
|--|--|--|
|${\color{#02d8e9}aqua blue}$ 'xkcd:aqua blue'|${\color{#88b378}sage green}$ 'xkcd:sage green'|${\color{#980002}blood red}$ 'xkcd:blood red'|
|--|--|--|
|${\color{#cb0162}deep pink}$ 'xkcd:deep pink'|${\color{#5cac2d}grass}$ 'xkcd:grass'|${\color{#769958}moss}$ 'xkcd:moss'|
|--|--|--|
|${\color{#a2bffe}pastel blue}$ 'xkcd:pastel blue'|${\color{#10a674}bluish green}$ 'xkcd:bluish green'|${\color{#06b48b}green blue}$ 'xkcd:green blue'|
|--|--|--|
|${\color{#af884a}dark tan}$ 'xkcd:dark tan'|${\color{#0b8b87}greenish blue}$ 'xkcd:greenish blue'|${\color{#ffa756}pale orange}$ 'xkcd:pale orange'|
|--|--|--|
|${\color{#a2a415}vomit}$ 'xkcd:vomit'|${\color{#154406}forrest green}$ 'xkcd:forrest green'|${\color{#856798}dark lavender}$ 'xkcd:dark lavender'|
|--|--|--|
|${\color{#34013f}dark violet}$ 'xkcd:dark violet'|${\color{#632de9}purple blue}$ 'xkcd:purple blue'|${\color{#0a888a}dark cyan}$ 'xkcd:dark cyan'|
|--|--|--|
|${\color{#6f7632}olive drab}$ 'xkcd:olive drab'|${\color{#d46a7e}pinkish}$ 'xkcd:pinkish'|${\color{#1e488f}cobalt}$ 'xkcd:cobalt'|
|--|--|--|
|${\color{#bc13fe}neon purple}$ 'xkcd:neon purple'|${\color{#7ef4cc}light turquoise}$ 'xkcd:light turquoise'|${\color{#76cd26}apple green}$ 'xkcd:apple green'|
|--|--|--|
|${\color{#74a662}dull green}$ 'xkcd:dull green'|${\color{#80013f}wine}$ 'xkcd:wine'|${\color{#b1d1fc}powder blue}$ 'xkcd:powder blue'|
|--|--|--|
|${\color{#ffffe4}off white}$ 'xkcd:off white'|${\color{#0652ff}electric blue}$ 'xkcd:electric blue'|${\color{#045c5a}dark turquoise}$ 'xkcd:dark turquoise'|
|--|--|--|
|${\color{#5729ce}blue purple}$ 'xkcd:blue purple'|${\color{#069af3}azure}$ 'xkcd:azure'|${\color{#ff000d}bright red}$ 'xkcd:bright red'|
|--|--|--|
|${\color{#f10c45}pinkish red}$ 'xkcd:pinkish red'|${\color{#5170d7}cornflower blue}$ 'xkcd:cornflower blue'|${\color{#acbf69}light olive}$ 'xkcd:light olive'|
|--|--|--|
|${\color{#6c3461}grape}$ 'xkcd:grape'|${\color{#5e819d}greyish blue}$ 'xkcd:greyish blue'|${\color{#601ef9}purplish blue}$ 'xkcd:purplish blue'|
|--|--|--|
|${\color{#b0dd16}yellowish green}$ 'xkcd:yellowish green'|${\color{#cdfd02}greenish yellow}$ 'xkcd:greenish yellow'|${\color{#2c6fbb}medium blue}$ 'xkcd:medium blue'|
|--|--|--|
|${\color{#c0737a}dusty rose}$ 'xkcd:dusty rose'|${\color{#d6b4fc}light violet}$ 'xkcd:light violet'|${\color{#020035}midnight blue}$ 'xkcd:midnight blue'|
|--|--|--|
|${\color{#703be7}bluish purple}$ 'xkcd:bluish purple'|${\color{#fd3c06}red orange}$ 'xkcd:red orange'|${\color{#960056}dark magenta}$ 'xkcd:dark magenta'|
|--|--|--|
|${\color{#40a368}greenish}$ 'xkcd:greenish'|${\color{#03719c}ocean blue}$ 'xkcd:ocean blue'|${\color{#fc5a50}coral}$ 'xkcd:coral'|
|--|--|--|
|${\color{#ffffc2}cream}$ 'xkcd:cream'|${\color{#7f2b0a}reddish brown}$ 'xkcd:reddish brown'|${\color{#b04e0f}burnt sienna}$ 'xkcd:burnt sienna'|
|--|--|--|
|${\color{#a03623}brick}$ 'xkcd:brick'|${\color{#87ae73}sage}$ 'xkcd:sage'|${\color{#789b73}grey green}$ 'xkcd:grey green'|
|--|--|--|
|${\color{#ffffff}white}$ 'xkcd:white'|${\color{#98eff9}robin's egg blue}$ 'xkcd:robin's egg blue'|${\color{#658b38}moss green}$ 'xkcd:moss green'|
|--|--|--|
|${\color{#5a7d9a}steel blue}$ 'xkcd:steel blue'|${\color{#380835}eggplant}$ 'xkcd:eggplant'|${\color{#fffe7a}light yellow}$ 'xkcd:light yellow'|
|--|--|--|
|${\color{#5ca904}leaf green}$ 'xkcd:leaf green'|${\color{#d8dcd6}light grey}$ 'xkcd:light grey'|${\color{#a5a502}puke}$ 'xkcd:puke'|
|--|--|--|
|${\color{#d648d7}pinkish purple}$ 'xkcd:pinkish purple'|${\color{#047495}sea blue}$ 'xkcd:sea blue'|${\color{#b790d4}pale purple}$ 'xkcd:pale purple'|
|--|--|--|
|${\color{#5b7c99}slate blue}$ 'xkcd:slate blue'|${\color{#607c8e}blue grey}$ 'xkcd:blue grey'|${\color{#0b4008}hunter green}$ 'xkcd:hunter green'|
|--|--|--|
|${\color{#ed0dd9}fuchsia}$ 'xkcd:fuchsia'|${\color{#8c000f}crimson}$ 'xkcd:crimson'|${\color{#ffff84}pale yellow}$ 'xkcd:pale yellow'|
|--|--|--|
|${\color{#bf9005}ochre}$ 'xkcd:ochre'|${\color{#d2bd0a}mustard yellow}$ 'xkcd:mustard yellow'|${\color{#ff474c}light red}$ 'xkcd:light red'|
|--|--|--|
|${\color{#0485d1}cerulean}$ 'xkcd:cerulean'|${\color{#ffcfdc}pale pink}$ 'xkcd:pale pink'|${\color{#040273}deep blue}$ 'xkcd:deep blue'|
|--|--|--|
|${\color{#a83c09}rust}$ 'xkcd:rust'|${\color{#90e4c1}light teal}$ 'xkcd:light teal'|${\color{#516572}slate}$ 'xkcd:slate'|
|--|--|--|
|${\color{#fac205}goldenrod}$ 'xkcd:goldenrod'|${\color{#d5b60a}dark yellow}$ 'xkcd:dark yellow'|${\color{#363737}dark grey}$ 'xkcd:dark grey'|
|--|--|--|
|${\color{#4b5d16}army green}$ 'xkcd:army green'|${\color{#6b8ba4}grey blue}$ 'xkcd:grey blue'|${\color{#80f9ad}seafoam}$ 'xkcd:seafoam'|
|--|--|--|
|${\color{#a57e52}puce}$ 'xkcd:puce'|${\color{#a9f971}spring green}$ 'xkcd:spring green'|${\color{#c65102}dark orange}$ 'xkcd:dark orange'|
|--|--|--|
|${\color{#e2ca76}sand}$ 'xkcd:sand'|${\color{#b0ff9d}pastel green}$ 'xkcd:pastel green'|${\color{#9ffeb0}mint}$ 'xkcd:mint'|
|--|--|--|
|${\color{#fdaa48}light orange}$ 'xkcd:light orange'|${\color{#fe01b1}bright pink}$ 'xkcd:bright pink'|${\color{#c1f80a}chartreuse}$ 'xkcd:chartreuse'|
|--|--|--|
|${\color{#36013f}deep purple}$ 'xkcd:deep purple'|${\color{#341c02}dark brown}$ 'xkcd:dark brown'|${\color{#b9a281}taupe}$ 'xkcd:taupe'|
|--|--|--|
|${\color{#8eab12}pea green}$ 'xkcd:pea green'|${\color{#9aae07}puke green}$ 'xkcd:puke green'|${\color{#02ab2e}kelly green}$ 'xkcd:kelly green'|
|--|--|--|
|${\color{#7af9ab}seafoam green}$ 'xkcd:seafoam green'|${\color{#137e6d}blue green}$ 'xkcd:blue green'|${\color{#aaa662}khaki}$ 'xkcd:khaki'|
|--|--|--|
|${\color{#610023}burgundy}$ 'xkcd:burgundy'|${\color{#014d4e}dark teal}$ 'xkcd:dark teal'|${\color{#8f1402}brick red}$ 'xkcd:brick red'|
|--|--|--|
|${\color{#4b006e}royal purple}$ 'xkcd:royal purple'|${\color{#580f41}plum}$ 'xkcd:plum'|${\color{#8fff9f}mint green}$ 'xkcd:mint green'|
|--|--|--|
|${\color{#dbb40c}gold}$ 'xkcd:gold'|${\color{#a2cffe}baby blue}$ 'xkcd:baby blue'|${\color{#c0fb2d}yellow green}$ 'xkcd:yellow green'|
|--|--|--|
|${\color{#be03fd}bright purple}$ 'xkcd:bright purple'|${\color{#840000}dark red}$ 'xkcd:dark red'|${\color{#d0fefe}pale blue}$ 'xkcd:pale blue'|
|--|--|--|
|${\color{#3f9b0b}grass green}$ 'xkcd:grass green'|${\color{#01153e}navy}$ 'xkcd:navy'|${\color{#04d8b2}aquamarine}$ 'xkcd:aquamarine'|
|--|--|--|
|${\color{#c04e01}burnt orange}$ 'xkcd:burnt orange'|${\color{#0cff0c}neon green}$ 'xkcd:neon green'|${\color{#0165fc}bright blue}$ 'xkcd:bright blue'|
|--|--|--|
|${\color{#cf6275}rose}$ 'xkcd:rose'|${\color{#ffd1df}light pink}$ 'xkcd:light pink'|${\color{#ceb301}mustard}$ 'xkcd:mustard'|
|--|--|--|
|${\color{#380282}indigo}$ 'xkcd:indigo'|${\color{#aaff32}lime}$ 'xkcd:lime'|${\color{#53fca1}sea green}$ 'xkcd:sea green'|
|--|--|--|
|${\color{#8e82fe}periwinkle}$ 'xkcd:periwinkle'|${\color{#cb416b}dark pink}$ 'xkcd:dark pink'|${\color{#677a04}olive green}$ 'xkcd:olive green'|
|--|--|--|
|${\color{#ffb07c}peach}$ 'xkcd:peach'|${\color{#c7fdb5}pale green}$ 'xkcd:pale green'|${\color{#ad8150}light brown}$ 'xkcd:light brown'|
|--|--|--|
|${\color{#ff028d}hot pink}$ 'xkcd:hot pink'|${\color{#000000}black}$ 'xkcd:black'|${\color{#cea2fd}lilac}$ 'xkcd:lilac'|
|--|--|--|
|${\color{#001146}navy blue}$ 'xkcd:navy blue'|${\color{#0504aa}royal blue}$ 'xkcd:royal blue'|${\color{#e6daa6}beige}$ 'xkcd:beige'|
|--|--|--|
|${\color{#ff796c}salmon}$ 'xkcd:salmon'|${\color{#6e750e}olive}$ 'xkcd:olive'|${\color{#650021}maroon}$ 'xkcd:maroon'|
|--|--|--|
|${\color{#01ff07}bright green}$ 'xkcd:bright green'|${\color{#35063e}dark purple}$ 'xkcd:dark purple'|${\color{#ae7181}mauve}$ 'xkcd:mauve'|
|--|--|--|
|${\color{#06470c}forest green}$ 'xkcd:forest green'|${\color{#13eac9}aqua}$ 'xkcd:aqua'|${\color{#00ffff}cyan}$ 'xkcd:cyan'|
|--|--|--|
|${\color{#d1b26f}tan}$ 'xkcd:tan'|${\color{#00035b}dark blue}$ 'xkcd:dark blue'|${\color{#c79fef}lavender}$ 'xkcd:lavender'|
|--|--|--|
|${\color{#06c2ac}turquoise}$ 'xkcd:turquoise'|${\color{#033500}dark green}$ 'xkcd:dark green'|${\color{#9a0eea}violet}$ 'xkcd:violet'|
|--|--|--|
|${\color{#bf77f6}light purple}$ 'xkcd:light purple'|${\color{#89fe05}lime green}$ 'xkcd:lime green'|${\color{#929591}grey}$ 'xkcd:grey'|
|--|--|--|
|${\color{#75bbfd}sky blue}$ 'xkcd:sky blue'|${\color{#ffff14}yellow}$ 'xkcd:yellow'|${\color{#c20078}magenta}$ 'xkcd:magenta'|
|--|--|--|
|${\color{#96f97b}light green}$ 'xkcd:light green'|${\color{#f97306}orange}$ 'xkcd:orange'|${\color{#029386}teal}$ 'xkcd:teal'|
|--|--|--|
|${\color{#95d0fc}light blue}$ 'xkcd:light blue'|${\color{#e50000}red}$ 'xkcd:red'|${\color{#653700}brown}$ 'xkcd:brown'|
|--|--|--|
|${\color{#ff81c0}pink}$ 'xkcd:pink'|${\color{#0343df}blue}$ 'xkcd:blue'|${\color{#15b01a}green}$ 'xkcd:green'|
|--|--|--|
|${\color{#7e1e9c}purple}$ 'xkcd:purple'|

# License
Whisper's AI model weights are released under the MIT License.