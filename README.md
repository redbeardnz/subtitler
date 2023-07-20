
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

|${\color{#acc2d9}cloudy blue}$ 'ACC2D9'|${\color{#56ae57}dark pastel green}$ '56AE57'|${\color{#b2996e}dust}$ 'B2996E'|
|--|--|--|
|${\color{#a8ff04}electric lime}$ 'A8FF04'|${\color{#69d84f}fresh green}$ '69D84F'|${\color{#894585}light eggplant}$ '894585'|
|--|--|--|
|${\color{#70b23f}nasty green}$ '70B23F'|${\color{#d4ffff}really light blue}$ 'D4FFFF'|${\color{#65ab7c}tea}$ '65AB7C'|
|--|--|--|
|${\color{#952e8f}warm purple}$ '952E8F'|${\color{#fcfc81}yellowish tan}$ 'FCFC81'|${\color{#a5a391}cement}$ 'A5A391'|
|--|--|--|
|${\color{#388004}dark grass green}$ '388004'|${\color{#4c9085}dusty teal}$ '4C9085'|${\color{#5e9b8a}grey teal}$ '5E9B8A'|
|--|--|--|
|${\color{#efb435}macaroni and cheese}$ 'EFB435'|${\color{#d99b82}pinkish tan}$ 'D99B82'|${\color{#0a5f38}spruce}$ '0A5F38'|
|--|--|--|
|${\color{#0c06f7}strong blue}$ '0C06F7'|${\color{#61de2a}toxic green}$ '61DE2A'|${\color{#3778bf}windows blue}$ '3778BF'|
|--|--|--|
|${\color{#2242c7}blue blue}$ '2242C7'|${\color{#533cc6}blue with a hint of purple}$ '533CC6'|${\color{#9bb53c}booger}$ '9BB53C'|
|--|--|--|
|${\color{#05ffa6}bright sea green}$ '05FFA6'|${\color{#1f6357}dark green blue}$ '1F6357'|${\color{#017374}deep turquoise}$ '017374'|
|--|--|--|
|${\color{#0cb577}green teal}$ '0CB577'|${\color{#ff0789}strong pink}$ 'FF0789'|${\color{#afa88b}bland}$ 'AFA88B'|
|--|--|--|
|${\color{#08787f}deep aqua}$ '08787F'|${\color{#dd85d7}lavender pink}$ 'DD85D7'|${\color{#a6c875}light moss green}$ 'A6C875'|
|--|--|--|
|${\color{#a7ffb5}light seafoam green}$ 'A7FFB5'|${\color{#c2b709}olive yellow}$ 'C2B709'|${\color{#e78ea5}pig pink}$ 'E78EA5'|
|--|--|--|
|${\color{#966ebd}deep lilac}$ '966EBD'|${\color{#ccad60}desert}$ 'CCAD60'|${\color{#ac86a8}dusty lavender}$ 'AC86A8'|
|--|--|--|
|${\color{#947e94}purpley grey}$ '947E94'|${\color{#983fb2}purply}$ '983FB2'|${\color{#ff63e9}candy pink}$ 'FF63E9'|
|--|--|--|
|${\color{#b2fba5}light pastel green}$ 'B2FBA5'|${\color{#63b365}boring green}$ '63B365'|${\color{#8ee53f}kiwi green}$ '8EE53F'|
|--|--|--|
|${\color{#b7e1a1}light grey green}$ 'B7E1A1'|${\color{#ff6f52}orange pink}$ 'FF6F52'|${\color{#bdf8a3}tea green}$ 'BDF8A3'|
|--|--|--|
|${\color{#d3b683}very light brown}$ 'D3B683'|${\color{#fffcc4}egg shell}$ 'FFFCC4'|${\color{#430541}eggplant purple}$ '430541'|
|--|--|--|
|${\color{#ffb2d0}powder pink}$ 'FFB2D0'|${\color{#997570}reddish grey}$ '997570'|${\color{#ad900d}baby shit brown}$ 'AD900D'|
|--|--|--|
|${\color{#c48efd}liliac}$ 'C48EFD'|${\color{#507b9c}stormy blue}$ '507B9C'|${\color{#7d7103}ugly brown}$ '7D7103'|
|--|--|--|
|${\color{#fffd78}custard}$ 'FFFD78'|${\color{#da467d}darkish pink}$ 'DA467D'|${\color{#410200}deep brown}$ '410200'|
|--|--|--|
|${\color{#c9d179}greenish beige}$ 'C9D179'|${\color{#fffa86}manilla}$ 'FFFA86'|${\color{#5684ae}off blue}$ '5684AE'|
|--|--|--|
|${\color{#6b7c85}battleship grey}$ '6B7C85'|${\color{#6f6c0a}browny green}$ '6F6C0A'|${\color{#7e4071}bruise}$ '7E4071'|
|--|--|--|
|${\color{#009337}kelley green}$ '009337'|${\color{#d0e429}sickly yellow}$ 'D0E429'|${\color{#fff917}sunny yellow}$ 'FFF917'|
|--|--|--|
|${\color{#1d5dec}azul}$ '1D5DEC'|${\color{#054907}darkgreen}$ '054907'|${\color{#b5ce08}green/yellow}$ 'B5CE08'|
|--|--|--|
|${\color{#8fb67b}lichen}$ '8FB67B'|${\color{#c8ffb0}light light green}$ 'C8FFB0'|${\color{#fdde6c}pale gold}$ 'FDDE6C'|
|--|--|--|
|${\color{#ffdf22}sun yellow}$ 'FFDF22'|${\color{#a9be70}tan green}$ 'A9BE70'|${\color{#6832e3}burple}$ '6832E3'|
|--|--|--|
|${\color{#fdb147}butterscotch}$ 'FDB147'|${\color{#c7ac7d}toupe}$ 'C7AC7D'|${\color{#fff39a}dark cream}$ 'FFF39A'|
|--|--|--|
|${\color{#850e04}indian red}$ '850E04'|${\color{#efc0fe}light lavendar}$ 'EFC0FE'|${\color{#40fd14}poison green}$ '40FD14'|
|--|--|--|
|${\color{#b6c406}baby puke green}$ 'B6C406'|${\color{#9dff00}bright yellow green}$ '9DFF00'|${\color{#3c4142}charcoal grey}$ '3C4142'|
|--|--|--|
|${\color{#f2ab15}squash}$ 'F2AB15'|${\color{#ac4f06}cinnamon}$ 'AC4F06'|${\color{#c4fe82}light pea green}$ 'C4FE82'|
|--|--|--|
|${\color{#2cfa1f}radioactive green}$ '2CFA1F'|${\color{#9a6200}raw sienna}$ '9A6200'|${\color{#ca9bf7}baby purple}$ 'CA9BF7'|
|--|--|--|
|${\color{#875f42}cocoa}$ '875F42'|${\color{#3a2efe}light royal blue}$ '3A2EFE'|${\color{#fd8d49}orangeish}$ 'FD8D49'|
|--|--|--|
|${\color{#8b3103}rust brown}$ '8B3103'|${\color{#cba560}sand brown}$ 'CBA560'|${\color{#698339}swamp}$ '698339'|
|--|--|--|
|${\color{#0cdc73}tealish green}$ '0CDC73'|${\color{#b75203}burnt siena}$ 'B75203'|${\color{#7f8f4e}camo}$ '7F8F4E'|
|--|--|--|
|${\color{#26538d}dusk blue}$ '26538D'|${\color{#63a950}fern}$ '63A950'|${\color{#c87f89}old rose}$ 'C87F89'|
|--|--|--|
|${\color{#b1fc99}pale light green}$ 'B1FC99'|${\color{#ff9a8a}peachy pink}$ 'FF9A8A'|${\color{#f6688e}rosy pink}$ 'F6688E'|
|--|--|--|
|${\color{#76fda8}light bluish green}$ '76FDA8'|${\color{#53fe5c}light bright green}$ '53FE5C'|${\color{#4efd54}light neon green}$ '4EFD54'|
|--|--|--|
|${\color{#a0febf}light seafoam}$ 'A0FEBF'|${\color{#7bf2da}tiffany blue}$ '7BF2DA'|${\color{#bcf5a6}washed out green}$ 'BCF5A6'|
|--|--|--|
|${\color{#ca6b02}browny orange}$ 'CA6B02'|${\color{#107ab0}nice blue}$ '107AB0'|${\color{#2138ab}sapphire}$ '2138AB'|
|--|--|--|
|${\color{#719f91}greyish teal}$ '719F91'|${\color{#fdb915}orangey yellow}$ 'FDB915'|${\color{#fefcaf}parchment}$ 'FEFCAF'|
|--|--|--|
|${\color{#fcf679}straw}$ 'FCF679'|${\color{#1d0200}very dark brown}$ '1D0200'|${\color{#cb6843}terracota}$ 'CB6843'|
|--|--|--|
|${\color{#31668a}ugly blue}$ '31668A'|${\color{#247afd}clear blue}$ '247AFD'|${\color{#ffffb6}creme}$ 'FFFFB6'|
|--|--|--|
|${\color{#90fda9}foam green}$ '90FDA9'|${\color{#86a17d}grey/green}$ '86A17D'|${\color{#fddc5c}light gold}$ 'FDDC5C'|
|--|--|--|
|${\color{#78d1b6}seafoam blue}$ '78D1B6'|${\color{#13bbaf}topaz}$ '13BBAF'|${\color{#fb5ffc}violet pink}$ 'FB5FFC'|
|--|--|--|
|${\color{#20f986}wintergreen}$ '20F986'|${\color{#ffe36e}yellow tan}$ 'FFE36E'|${\color{#9d0759}dark fuchsia}$ '9D0759'|
|--|--|--|
|${\color{#3a18b1}indigo blue}$ '3A18B1'|${\color{#c2ff89}light yellowish green}$ 'C2FF89'|${\color{#d767ad}pale magenta}$ 'D767AD'|
|--|--|--|
|${\color{#720058}rich purple}$ '720058'|${\color{#ffda03}sunflower yellow}$ 'FFDA03'|${\color{#01c08d}green/blue}$ '01C08D'|
|--|--|--|
|${\color{#ac7434}leather}$ 'AC7434'|${\color{#014600}racing green}$ '014600'|${\color{#9900fa}vivid purple}$ '9900FA'|
|--|--|--|
|${\color{#02066f}dark royal blue}$ '02066F'|${\color{#8e7618}hazel}$ '8E7618'|${\color{#d1768f}muted pink}$ 'D1768F'|
|--|--|--|
|${\color{#96b403}booger green}$ '96B403'|${\color{#fdff63}canary}$ 'FDFF63'|${\color{#95a3a6}cool grey}$ '95A3A6'|
|--|--|--|
|${\color{#7f684e}dark taupe}$ '7F684E'|${\color{#751973}darkish purple}$ '751973'|${\color{#089404}true green}$ '089404'|
|--|--|--|
|${\color{#ff6163}coral pink}$ 'FF6163'|${\color{#598556}dark sage}$ '598556'|${\color{#214761}dark slate blue}$ '214761'|
|--|--|--|
|${\color{#3c73a8}flat blue}$ '3C73A8'|${\color{#ba9e88}mushroom}$ 'BA9E88'|${\color{#021bf9}rich blue}$ '021BF9'|
|--|--|--|
|${\color{#734a65}dirty purple}$ '734A65'|${\color{#23c48b}greenblue}$ '23C48B'|${\color{#8fae22}icky green}$ '8FAE22'|
|--|--|--|
|${\color{#e6f2a2}light khaki}$ 'E6F2A2'|${\color{#4b57db}warm blue}$ '4B57DB'|${\color{#d90166}dark hot pink}$ 'D90166'|
|--|--|--|
|${\color{#015482}deep sea blue}$ '015482'|${\color{#9d0216}carmine}$ '9D0216'|${\color{#728f02}dark yellow green}$ '728F02'|
|--|--|--|
|${\color{#ffe5ad}pale peach}$ 'FFE5AD'|${\color{#4e0550}plum purple}$ '4E0550'|${\color{#f9bc08}golden rod}$ 'F9BC08'|
|--|--|--|
|${\color{#ff073a}neon red}$ 'FF073A'|${\color{#c77986}old pink}$ 'C77986'|${\color{#d6fffe}very pale blue}$ 'D6FFFE'|
|--|--|--|
|${\color{#fe4b03}blood orange}$ 'FE4B03'|${\color{#fd5956}grapefruit}$ 'FD5956'|${\color{#fce166}sand yellow}$ 'FCE166'|
|--|--|--|
|${\color{#b2713d}clay brown}$ 'B2713D'|${\color{#1f3b4d}dark blue grey}$ '1F3B4D'|${\color{#699d4c}flat green}$ '699D4C'|
|--|--|--|
|${\color{#56fca2}light green blue}$ '56FCA2'|${\color{#fb5581}warm pink}$ 'FB5581'|${\color{#3e82fc}dodger blue}$ '3E82FC'|
|--|--|--|
|${\color{#a0bf16}gross green}$ 'A0BF16'|${\color{#d6fffa}ice}$ 'D6FFFA'|${\color{#4f738e}metallic blue}$ '4F738E'|
|--|--|--|
|${\color{#ffb19a}pale salmon}$ 'FFB19A'|${\color{#5c8b15}sap green}$ '5C8B15'|${\color{#54ac68}algae}$ '54AC68'|
|--|--|--|
|${\color{#89a0b0}bluey grey}$ '89A0B0'|${\color{#7ea07a}greeny grey}$ '7EA07A'|${\color{#1bfc06}highlighter green}$ '1BFC06'|
|--|--|--|
|${\color{#cafffb}light light blue}$ 'CAFFFB'|${\color{#b6ffbb}light mint}$ 'B6FFBB'|${\color{#a75e09}raw umber}$ 'A75E09'|
|--|--|--|
|${\color{#152eff}vivid blue}$ '152EFF'|${\color{#8d5eb7}deep lavender}$ '8D5EB7'|${\color{#5f9e8f}dull teal}$ '5F9E8F'|
|--|--|--|
|${\color{#63f7b4}light greenish blue}$ '63F7B4'|${\color{#606602}mud green}$ '606602'|${\color{#fc86aa}pinky}$ 'FC86AA'|
|--|--|--|
|${\color{#8c0034}red wine}$ '8C0034'|${\color{#758000}shit green}$ '758000'|${\color{#ab7e4c}tan brown}$ 'AB7E4C'|
|--|--|--|
|${\color{#030764}darkblue}$ '030764'|${\color{#fe86a4}rosa}$ 'FE86A4'|${\color{#d5174e}lipstick}$ 'D5174E'|
|--|--|--|
|${\color{#fed0fc}pale mauve}$ 'FED0FC'|${\color{#680018}claret}$ '680018'|${\color{#fedf08}dandelion}$ 'FEDF08'|
|--|--|--|
|${\color{#fe420f}orangered}$ 'FE420F'|${\color{#6f7c00}poop green}$ '6F7C00'|${\color{#ca0147}ruby}$ 'CA0147'|
|--|--|--|
|${\color{#1b2431}dark}$ '1B2431'|${\color{#00fbb0}greenish turquoise}$ '00FBB0'|${\color{#db5856}pastel red}$ 'DB5856'|
|--|--|--|
|${\color{#ddd618}piss yellow}$ 'DDD618'|${\color{#41fdfe}bright cyan}$ '41FDFE'|${\color{#cf524e}dark coral}$ 'CF524E'|
|--|--|--|
|${\color{#21c36f}algae green}$ '21C36F'|${\color{#a90308}darkish red}$ 'A90308'|${\color{#6e1005}reddy brown}$ '6E1005'|
|--|--|--|
|${\color{#fe828c}blush pink}$ 'FE828C'|${\color{#4b6113}camouflage green}$ '4B6113'|${\color{#4da409}lawn green}$ '4DA409'|
|--|--|--|
|${\color{#beae8a}putty}$ 'BEAE8A'|${\color{#0339f8}vibrant blue}$ '0339F8'|${\color{#a88f59}dark sand}$ 'A88F59'|
|--|--|--|
|${\color{#5d21d0}purple/blue}$ '5D21D0'|${\color{#feb209}saffron}$ 'FEB209'|${\color{#4e518b}twilight}$ '4E518B'|
|--|--|--|
|${\color{#964e02}warm brown}$ '964E02'|${\color{#85a3b2}bluegrey}$ '85A3B2'|${\color{#ff69af}bubble gum pink}$ 'FF69AF'|
|--|--|--|
|${\color{#c3fbf4}duck egg blue}$ 'C3FBF4'|${\color{#2afeb7}greenish cyan}$ '2AFEB7'|${\color{#005f6a}petrol}$ '005F6A'|
|--|--|--|
|${\color{#0c1793}royal}$ '0C1793'|${\color{#ffff81}butter}$ 'FFFF81'|${\color{#f0833a}dusty orange}$ 'F0833A'|
|--|--|--|
|${\color{#f1f33f}off yellow}$ 'F1F33F'|${\color{#b1d27b}pale olive green}$ 'B1D27B'|${\color{#fc824a}orangish}$ 'FC824A'|
|--|--|--|
|${\color{#71aa34}leaf}$ '71AA34'|${\color{#b7c9e2}light blue grey}$ 'B7C9E2'|${\color{#4b0101}dried blood}$ '4B0101'|
|--|--|--|
|${\color{#a552e6}lightish purple}$ 'A552E6'|${\color{#af2f0d}rusty red}$ 'AF2F0D'|${\color{#8b88f8}lavender blue}$ '8B88F8'|
|--|--|--|
|${\color{#9af764}light grass green}$ '9AF764'|${\color{#a6fbb2}light mint green}$ 'A6FBB2'|${\color{#ffc512}sunflower}$ 'FFC512'|
|--|--|--|
|${\color{#750851}velvet}$ '750851'|${\color{#c14a09}brick orange}$ 'C14A09'|${\color{#fe2f4a}lightish red}$ 'FE2F4A'|
|--|--|--|
|${\color{#0203e2}pure blue}$ '0203E2'|${\color{#0a437a}twilight blue}$ '0A437A'|${\color{#a50055}violet red}$ 'A50055'|
|--|--|--|
|${\color{#ae8b0c}yellowy brown}$ 'AE8B0C'|${\color{#fd798f}carnation}$ 'FD798F'|${\color{#bfac05}muddy yellow}$ 'BFAC05'|
|--|--|--|
|${\color{#3eaf76}dark seafoam green}$ '3EAF76'|${\color{#c74767}deep rose}$ 'C74767'|${\color{#b9484e}dusty red}$ 'B9484E'|
|--|--|--|
|${\color{#647d8e}grey/blue}$ '647D8E'|${\color{#bffe28}lemon lime}$ 'BFFE28'|${\color{#d725de}purple/pink}$ 'D725DE'|
|--|--|--|
|${\color{#b29705}brown yellow}$ 'B29705'|${\color{#673a3f}purple brown}$ '673A3F'|${\color{#a87dc2}wisteria}$ 'A87DC2'|
|--|--|--|
|${\color{#fafe4b}banana yellow}$ 'FAFE4B'|${\color{#c0022f}lipstick red}$ 'C0022F'|${\color{#0e87cc}water blue}$ '0E87CC'|
|--|--|--|
|${\color{#8d8468}brown grey}$ '8D8468'|${\color{#ad03de}vibrant purple}$ 'AD03DE'|${\color{#8cff9e}baby green}$ '8CFF9E'|
|--|--|--|
|${\color{#94ac02}barf green}$ '94AC02'|${\color{#c4fff7}eggshell blue}$ 'C4FFF7'|${\color{#fdee73}sandy yellow}$ 'FDEE73'|
|--|--|--|
|${\color{#33b864}cool green}$ '33B864'|${\color{#fff9d0}pale}$ 'FFF9D0'|${\color{#758da3}blue/grey}$ '758DA3'|
|--|--|--|
|${\color{#f504c9}hot magenta}$ 'F504C9'|${\color{#77a1b5}greyblue}$ '77A1B5'|${\color{#8756e4}purpley}$ '8756E4'|
|--|--|--|
|${\color{#889717}baby shit green}$ '889717'|${\color{#c27e79}brownish pink}$ 'C27E79'|${\color{#017371}dark aquamarine}$ '017371'|
|--|--|--|
|${\color{#9f8303}diarrhea}$ '9F8303'|${\color{#f7d560}light mustard}$ 'F7D560'|${\color{#bdf6fe}pale sky blue}$ 'BDF6FE'|
|--|--|--|
|${\color{#75b84f}turtle green}$ '75B84F'|${\color{#9cbb04}bright olive}$ '9CBB04'|${\color{#29465b}dark grey blue}$ '29465B'|
|--|--|--|
|${\color{#696006}greeny brown}$ '696006'|${\color{#adf802}lemon green}$ 'ADF802'|${\color{#c1c6fc}light periwinkle}$ 'C1C6FC'|
|--|--|--|
|${\color{#35ad6b}seaweed green}$ '35AD6B'|${\color{#fffd37}sunshine yellow}$ 'FFFD37'|${\color{#a442a0}ugly purple}$ 'A442A0'|
|--|--|--|
|${\color{#f36196}medium pink}$ 'F36196'|${\color{#947706}puke brown}$ '947706'|${\color{#fff4f2}very light pink}$ 'FFF4F2'|
|--|--|--|
|${\color{#1e9167}viridian}$ '1E9167'|${\color{#b5c306}bile}$ 'B5C306'|${\color{#feff7f}faded yellow}$ 'FEFF7F'|
|--|--|--|
|${\color{#cffdbc}very pale green}$ 'CFFDBC'|${\color{#0add08}vibrant green}$ '0ADD08'|${\color{#87fd05}bright lime}$ '87FD05'|
|--|--|--|
|${\color{#1ef876}spearmint}$ '1EF876'|${\color{#7bfdc7}light aquamarine}$ '7BFDC7'|${\color{#bcecac}light sage}$ 'BCECAC'|
|--|--|--|
|${\color{#bbf90f}yellowgreen}$ 'BBF90F'|${\color{#ab9004}baby poo}$ 'AB9004'|${\color{#1fb57a}dark seafoam}$ '1FB57A'|
|--|--|--|
|${\color{#00555a}deep teal}$ '00555A'|${\color{#a484ac}heather}$ 'A484AC'|${\color{#c45508}rust orange}$ 'C45508'|
|--|--|--|
|${\color{#3f829d}dirty blue}$ '3F829D'|${\color{#548d44}fern green}$ '548D44'|${\color{#c95efb}bright lilac}$ 'C95EFB'|
|--|--|--|
|${\color{#3ae57f}weird green}$ '3AE57F'|${\color{#016795}peacock blue}$ '016795'|${\color{#87a922}avocado green}$ '87A922'|
|--|--|--|
|${\color{#f0944d}faded orange}$ 'F0944D'|${\color{#5d1451}grape purple}$ '5D1451'|${\color{#25ff29}hot green}$ '25FF29'|
|--|--|--|
|${\color{#d0fe1d}lime yellow}$ 'D0FE1D'|${\color{#ffa62b}mango}$ 'FFA62B'|${\color{#01b44c}shamrock}$ '01B44C'|
|--|--|--|
|${\color{#ff6cb5}bubblegum}$ 'FF6CB5'|${\color{#6b4247}purplish brown}$ '6B4247'|${\color{#c7c10c}vomit yellow}$ 'C7C10C'|
|--|--|--|
|${\color{#b7fffa}pale cyan}$ 'B7FFFA'|${\color{#aeff6e}key lime}$ 'AEFF6E'|${\color{#ec2d01}tomato red}$ 'EC2D01'|
|--|--|--|
|${\color{#76ff7b}lightgreen}$ '76FF7B'|${\color{#730039}merlot}$ '730039'|${\color{#040348}night blue}$ '040348'|
|--|--|--|
|${\color{#df4ec8}purpleish pink}$ 'DF4EC8'|${\color{#6ecb3c}apple}$ '6ECB3C'|${\color{#8f9805}baby poop green}$ '8F9805'|
|--|--|--|
|${\color{#5edc1f}green apple}$ '5EDC1F'|${\color{#d94ff5}heliotrope}$ 'D94FF5'|${\color{#c8fd3d}yellow/green}$ 'C8FD3D'|
|--|--|--|
|${\color{#070d0d}almost black}$ '070D0D'|${\color{#4984b8}cool blue}$ '4984B8'|${\color{#51b73b}leafy green}$ '51B73B'|
|--|--|--|
|${\color{#ac7e04}mustard brown}$ 'AC7E04'|${\color{#4e5481}dusk}$ '4E5481'|${\color{#876e4b}dull brown}$ '876E4B'|
|--|--|--|
|${\color{#58bc08}frog green}$ '58BC08'|${\color{#2fef10}vivid green}$ '2FEF10'|${\color{#2dfe54}bright light green}$ '2DFE54'|
|--|--|--|
|${\color{#0aff02}fluro green}$ '0AFF02'|${\color{#9cef43}kiwi}$ '9CEF43'|${\color{#18d17b}seaweed}$ '18D17B'|
|--|--|--|
|${\color{#35530a}navy green}$ '35530A'|${\color{#1805db}ultramarine blue}$ '1805DB'|${\color{#6258c4}iris}$ '6258C4'|
|--|--|--|
|${\color{#ff964f}pastel orange}$ 'FF964F'|${\color{#ffab0f}yellowish orange}$ 'FFAB0F'|${\color{#8f8ce7}perrywinkle}$ '8F8CE7'|
|--|--|--|
|${\color{#24bca8}tealish}$ '24BCA8'|${\color{#3f012c}dark plum}$ '3F012C'|${\color{#cbf85f}pear}$ 'CBF85F'|
|--|--|--|
|${\color{#ff724c}pinkish orange}$ 'FF724C'|${\color{#280137}midnight purple}$ '280137'|${\color{#b36ff6}light urple}$ 'B36FF6'|
|--|--|--|
|${\color{#48c072}dark mint}$ '48C072'|${\color{#bccb7a}greenish tan}$ 'BCCB7A'|${\color{#a8415b}light burgundy}$ 'A8415B'|
|--|--|--|
|${\color{#06b1c4}turquoise blue}$ '06B1C4'|${\color{#cd7584}ugly pink}$ 'CD7584'|${\color{#f1da7a}sandy}$ 'F1DA7A'|
|--|--|--|
|${\color{#ff0490}electric pink}$ 'FF0490'|${\color{#805b87}muted purple}$ '805B87'|${\color{#50a747}mid green}$ '50A747'|
|--|--|--|
|${\color{#a8a495}greyish}$ 'A8A495'|${\color{#cfff04}neon yellow}$ 'CFFF04'|${\color{#ffff7e}banana}$ 'FFFF7E'|
|--|--|--|
|${\color{#ff7fa7}carnation pink}$ 'FF7FA7'|${\color{#ef4026}tomato}$ 'EF4026'|${\color{#3c9992}sea}$ '3C9992'|
|--|--|--|
|${\color{#886806}muddy brown}$ '886806'|${\color{#04f489}turquoise green}$ '04F489'|${\color{#fef69e}buff}$ 'FEF69E'|
|--|--|--|
|${\color{#cfaf7b}fawn}$ 'CFAF7B'|${\color{#3b719f}muted blue}$ '3B719F'|${\color{#fdc1c5}pale rose}$ 'FDC1C5'|
|--|--|--|
|${\color{#20c073}dark mint green}$ '20C073'|${\color{#9b5fc0}amethyst}$ '9B5FC0'|${\color{#0f9b8e}blue/green}$ '0F9B8E'|
|--|--|--|
|${\color{#742802}chestnut}$ '742802'|${\color{#9db92c}sick green}$ '9DB92C'|${\color{#a4bf20}pea}$ 'A4BF20'|
|--|--|--|
|${\color{#cd5909}rusty orange}$ 'CD5909'|${\color{#ada587}stone}$ 'ADA587'|${\color{#be013c}rose red}$ 'BE013C'|
|--|--|--|
|${\color{#b8ffeb}pale aqua}$ 'B8FFEB'|${\color{#dc4d01}deep orange}$ 'DC4D01'|${\color{#a2653e}earth}$ 'A2653E'|
|--|--|--|
|${\color{#638b27}mossy green}$ '638B27'|${\color{#419c03}grassy green}$ '419C03'|${\color{#b1ff65}pale lime green}$ 'B1FF65'|
|--|--|--|
|${\color{#9dbcd4}light grey blue}$ '9DBCD4'|${\color{#fdfdfe}pale grey}$ 'FDFDFE'|${\color{#77ab56}asparagus}$ '77AB56'|
|--|--|--|
|${\color{#464196}blueberry}$ '464196'|${\color{#990147}purple red}$ '990147'|${\color{#befd73}pale lime}$ 'BEFD73'|
|--|--|--|
|${\color{#32bf84}greenish teal}$ '32BF84'|${\color{#af6f09}caramel}$ 'AF6F09'|${\color{#a0025c}deep magenta}$ 'A0025C'|
|--|--|--|
|${\color{#ffd8b1}light peach}$ 'FFD8B1'|${\color{#7f4e1e}milk chocolate}$ '7F4E1E'|${\color{#bf9b0c}ocher}$ 'BF9B0C'|
|--|--|--|
|${\color{#6ba353}off green}$ '6BA353'|${\color{#f075e6}purply pink}$ 'F075E6'|${\color{#7bc8f6}lightblue}$ '7BC8F6'|
|--|--|--|
|${\color{#475f94}dusky blue}$ '475F94'|${\color{#f5bf03}golden}$ 'F5BF03'|${\color{#fffeb6}light beige}$ 'FFFEB6'|
|--|--|--|
|${\color{#fffd74}butter yellow}$ 'FFFD74'|${\color{#895b7b}dusky purple}$ '895B7B'|${\color{#436bad}french blue}$ '436BAD'|
|--|--|--|
|${\color{#d0c101}ugly yellow}$ 'D0C101'|${\color{#c6f808}greeny yellow}$ 'C6F808'|${\color{#f43605}orangish red}$ 'F43605'|
|--|--|--|
|${\color{#02c14d}shamrock green}$ '02C14D'|${\color{#b25f03}orangish brown}$ 'B25F03'|${\color{#2a7e19}tree green}$ '2A7E19'|
|--|--|--|
|${\color{#490648}deep violet}$ '490648'|${\color{#536267}gunmetal}$ '536267'|${\color{#5a06ef}blue/purple}$ '5A06EF'|
|--|--|--|
|${\color{#cf0234}cherry}$ 'CF0234'|${\color{#c4a661}sandy brown}$ 'C4A661'|${\color{#978a84}warm grey}$ '978A84'|
|--|--|--|
|${\color{#1f0954}dark indigo}$ '1F0954'|${\color{#03012d}midnight}$ '03012D'|${\color{#2bb179}bluey green}$ '2BB179'|
|--|--|--|
|${\color{#c3909b}grey pink}$ 'C3909B'|${\color{#a66fb5}soft purple}$ 'A66FB5'|${\color{#770001}blood}$ '770001'|
|--|--|--|
|${\color{#922b05}brown red}$ '922B05'|${\color{#7d7f7c}medium grey}$ '7D7F7C'|${\color{#990f4b}berry}$ '990F4B'|
|--|--|--|
|${\color{#8f7303}poo}$ '8F7303'|${\color{#c83cb9}purpley pink}$ 'C83CB9'|${\color{#fea993}light salmon}$ 'FEA993'|
|--|--|--|
|${\color{#acbb0d}snot}$ 'ACBB0D'|${\color{#c071fe}easter purple}$ 'C071FE'|${\color{#ccfd7f}light yellow green}$ 'CCFD7F'|
|--|--|--|
|${\color{#00022e}dark navy blue}$ '00022E'|${\color{#828344}drab}$ '828344'|${\color{#ffc5cb}light rose}$ 'FFC5CB'|
|--|--|--|
|${\color{#ab1239}rouge}$ 'AB1239'|${\color{#b0054b}purplish red}$ 'B0054B'|${\color{#99cc04}slime green}$ '99CC04'|
|--|--|--|
|${\color{#937c00}baby poop}$ '937C00'|${\color{#019529}irish green}$ '019529'|${\color{#ef1de7}pink/purple}$ 'EF1DE7'|
|--|--|--|
|${\color{#000435}dark navy}$ '000435'|${\color{#42b395}greeny blue}$ '42B395'|${\color{#9d5783}light plum}$ '9D5783'|
|--|--|--|
|${\color{#c8aca9}pinkish grey}$ 'C8ACA9'|${\color{#c87606}dirty orange}$ 'C87606'|${\color{#aa2704}rust red}$ 'AA2704'|
|--|--|--|
|${\color{#e4cbff}pale lilac}$ 'E4CBFF'|${\color{#fa4224}orangey red}$ 'FA4224'|${\color{#0804f9}primary blue}$ '0804F9'|
|--|--|--|
|${\color{#5cb200}kermit green}$ '5CB200'|${\color{#76424e}brownish purple}$ '76424E'|${\color{#6c7a0e}murky green}$ '6C7A0E'|
|--|--|--|
|${\color{#fbdd7e}wheat}$ 'FBDD7E'|${\color{#2a0134}very dark purple}$ '2A0134'|${\color{#044a05}bottle green}$ '044A05'|
|--|--|--|
|${\color{#fd4659}watermelon}$ 'FD4659'|${\color{#0d75f8}deep sky blue}$ '0D75F8'|${\color{#fe0002}fire engine red}$ 'FE0002'|
|--|--|--|
|${\color{#cb9d06}yellow ochre}$ 'CB9D06'|${\color{#fb7d07}pumpkin orange}$ 'FB7D07'|${\color{#b9cc81}pale olive}$ 'B9CC81'|
|--|--|--|
|${\color{#edc8ff}light lilac}$ 'EDC8FF'|${\color{#61e160}lightish green}$ '61E160'|${\color{#8ab8fe}carolina blue}$ '8AB8FE'|
|--|--|--|
|${\color{#920a4e}mulberry}$ '920A4E'|${\color{#fe02a2}shocking pink}$ 'FE02A2'|${\color{#9a3001}auburn}$ '9A3001'|
|--|--|--|
|${\color{#65fe08}bright lime green}$ '65FE08'|${\color{#befdb7}celadon}$ 'BEFDB7'|${\color{#b17261}pinkish brown}$ 'B17261'|
|--|--|--|
|${\color{#885f01}poo brown}$ '885F01'|${\color{#02ccfe}bright sky blue}$ '02CCFE'|${\color{#c1fd95}celery}$ 'C1FD95'|
|--|--|--|
|${\color{#836539}dirt brown}$ '836539'|${\color{#fb2943}strawberry}$ 'FB2943'|${\color{#84b701}dark lime}$ '84B701'|
|--|--|--|
|${\color{#b66325}copper}$ 'B66325'|${\color{#7f5112}medium brown}$ '7F5112'|${\color{#5fa052}muted green}$ '5FA052'|
|--|--|--|
|${\color{#6dedfd}robin's egg}$ '6DEDFD'|${\color{#0bf9ea}bright aqua}$ '0BF9EA'|${\color{#c760ff}bright lavender}$ 'C760FF'|
|--|--|--|
|${\color{#ffffcb}ivory}$ 'FFFFCB'|${\color{#f6cefc}very light purple}$ 'F6CEFC'|${\color{#155084}light navy}$ '155084'|
|--|--|--|
|${\color{#f5054f}pink red}$ 'F5054F'|${\color{#645403}olive brown}$ '645403'|${\color{#7a5901}poop brown}$ '7A5901'|
|--|--|--|
|${\color{#a8b504}mustard green}$ 'A8B504'|${\color{#3d9973}ocean green}$ '3D9973'|${\color{#000133}very dark blue}$ '000133'|
|--|--|--|
|${\color{#76a973}dusty green}$ '76A973'|${\color{#2e5a88}light navy blue}$ '2E5A88'|${\color{#0bf77d}minty green}$ '0BF77D'|
|--|--|--|
|${\color{#bd6c48}adobe}$ 'BD6C48'|${\color{#ac1db8}barney}$ 'AC1DB8'|${\color{#2baf6a}jade green}$ '2BAF6A'|
|--|--|--|
|${\color{#26f7fd}bright light blue}$ '26F7FD'|${\color{#aefd6c}light lime}$ 'AEFD6C'|${\color{#9b8f55}dark khaki}$ '9B8F55'|
|--|--|--|
|${\color{#ffad01}orange yellow}$ 'FFAD01'|${\color{#c69c04}ocre}$ 'C69C04'|${\color{#f4d054}maize}$ 'F4D054'|
|--|--|--|
|${\color{#de9dac}faded pink}$ 'DE9DAC'|${\color{#05480d}british racing green}$ '05480D'|${\color{#c9ae74}sandstone}$ 'C9AE74'|
|--|--|--|
|${\color{#60460f}mud brown}$ '60460F'|${\color{#98f6b0}light sea green}$ '98F6B0'|${\color{#8af1fe}robin egg blue}$ '8AF1FE'|
|--|--|--|
|${\color{#2ee8bb}aqua marine}$ '2EE8BB'|${\color{#11875d}dark sea green}$ '11875D'|${\color{#fdb0c0}soft pink}$ 'FDB0C0'|
|--|--|--|
|${\color{#b16002}orangey brown}$ 'B16002'|${\color{#f7022a}cherry red}$ 'F7022A'|${\color{#d5ab09}burnt yellow}$ 'D5AB09'|
|--|--|--|
|${\color{#86775f}brownish grey}$ '86775F'|${\color{#c69f59}camel}$ 'C69F59'|${\color{#7a687f}purplish grey}$ '7A687F'|
|--|--|--|
|${\color{#042e60}marine}$ '042E60'|${\color{#c88d94}greyish pink}$ 'C88D94'|${\color{#a5fbd5}pale turquoise}$ 'A5FBD5'|
|--|--|--|
|${\color{#fffe71}pastel yellow}$ 'FFFE71'|${\color{#6241c7}bluey purple}$ '6241C7'|${\color{#fffe40}canary yellow}$ 'FFFE40'|
|--|--|--|
|${\color{#d3494e}faded red}$ 'D3494E'|${\color{#985e2b}sepia}$ '985E2B'|${\color{#a6814c}coffee}$ 'A6814C'|
|--|--|--|
|${\color{#ff08e8}bright magenta}$ 'FF08E8'|${\color{#9d7651}mocha}$ '9D7651'|${\color{#feffca}ecru}$ 'FEFFCA'|
|--|--|--|
|${\color{#98568d}purpleish}$ '98568D'|${\color{#9e003a}cranberry}$ '9E003A'|${\color{#287c37}darkish green}$ '287C37'|
|--|--|--|
|${\color{#b96902}brown orange}$ 'B96902'|${\color{#ba6873}dusky rose}$ 'BA6873'|${\color{#ff7855}melon}$ 'FF7855'|
|--|--|--|
|${\color{#94b21c}sickly green}$ '94B21C'|${\color{#c5c9c7}silver}$ 'C5C9C7'|${\color{#661aee}purply blue}$ '661AEE'|
|--|--|--|
|${\color{#6140ef}purpleish blue}$ '6140EF'|${\color{#9be5aa}hospital green}$ '9BE5AA'|${\color{#7b5804}shit brown}$ '7B5804'|
|--|--|--|
|${\color{#276ab3}mid blue}$ '276AB3'|${\color{#feb308}amber}$ 'FEB308'|${\color{#8cfd7e}easter green}$ '8CFD7E'|
|--|--|--|
|${\color{#6488ea}soft blue}$ '6488EA'|${\color{#056eee}cerulean blue}$ '056EEE'|${\color{#b27a01}golden brown}$ 'B27A01'|
|--|--|--|
|${\color{#0ffef9}bright turquoise}$ '0FFEF9'|${\color{#fa2a55}red pink}$ 'FA2A55'|${\color{#820747}red purple}$ '820747'|
|--|--|--|
|${\color{#7a6a4f}greyish brown}$ '7A6A4F'|${\color{#f4320c}vermillion}$ 'F4320C'|${\color{#a13905}russet}$ 'A13905'|
|--|--|--|
|${\color{#6f828a}steel grey}$ '6F828A'|${\color{#a55af4}lighter purple}$ 'A55AF4'|${\color{#ad0afd}bright violet}$ 'AD0AFD'|
|--|--|--|
|${\color{#004577}prussian blue}$ '004577'|${\color{#658d6d}slate green}$ '658D6D'|${\color{#ca7b80}dirty pink}$ 'CA7B80'|
|--|--|--|
|${\color{#005249}dark blue green}$ '005249'|${\color{#2b5d34}pine}$ '2B5D34'|${\color{#bff128}yellowy green}$ 'BFF128'|
|--|--|--|
|${\color{#b59410}dark gold}$ 'B59410'|${\color{#2976bb}bluish}$ '2976BB'|${\color{#014182}darkish blue}$ '014182'|
|--|--|--|
|${\color{#bb3f3f}dull red}$ 'BB3F3F'|${\color{#fc2647}pinky red}$ 'FC2647'|${\color{#a87900}bronze}$ 'A87900'|
|--|--|--|
|${\color{#82cbb2}pale teal}$ '82CBB2'|${\color{#667c3e}military green}$ '667C3E'|${\color{#fe46a5}barbie pink}$ 'FE46A5'|
|--|--|--|
|${\color{#fe83cc}bubblegum pink}$ 'FE83CC'|${\color{#94a617}pea soup green}$ '94A617'|${\color{#a88905}dark mustard}$ 'A88905'|
|--|--|--|
|${\color{#7f5f00}shit}$ '7F5F00'|${\color{#9e43a2}medium purple}$ '9E43A2'|${\color{#062e03}very dark green}$ '062E03'|
|--|--|--|
|${\color{#8a6e45}dirt}$ '8A6E45'|${\color{#cc7a8b}dusky pink}$ 'CC7A8B'|${\color{#9e0168}red violet}$ '9E0168'|
|--|--|--|
|${\color{#fdff38}lemon yellow}$ 'FDFF38'|${\color{#c0fa8b}pistachio}$ 'C0FA8B'|${\color{#eedc5b}dull yellow}$ 'EEDC5B'|
|--|--|--|
|${\color{#7ebd01}dark lime green}$ '7EBD01'|${\color{#3b5b92}denim blue}$ '3B5B92'|${\color{#01889f}teal blue}$ '01889F'|
|--|--|--|
|${\color{#3d7afd}lightish blue}$ '3D7AFD'|${\color{#5f34e7}purpley blue}$ '5F34E7'|${\color{#6d5acf}light indigo}$ '6D5ACF'|
|--|--|--|
|${\color{#748500}swamp green}$ '748500'|${\color{#706c11}brown green}$ '706C11'|${\color{#3c0008}dark maroon}$ '3C0008'|
|--|--|--|
|${\color{#cb00f5}hot purple}$ 'CB00F5'|${\color{#002d04}dark forest green}$ '002D04'|${\color{#658cbb}faded blue}$ '658CBB'|
|--|--|--|
|${\color{#749551}drab green}$ '749551'|${\color{#b9ff66}light lime green}$ 'B9FF66'|${\color{#9dc100}snot green}$ '9DC100'|
|--|--|--|
|${\color{#faee66}yellowish}$ 'FAEE66'|${\color{#7efbb3}light blue green}$ '7EFBB3'|${\color{#7b002c}bordeaux}$ '7B002C'|
|--|--|--|
|${\color{#c292a1}light mauve}$ 'C292A1'|${\color{#017b92}ocean}$ '017B92'|${\color{#fcc006}marigold}$ 'FCC006'|
|--|--|--|
|${\color{#657432}muddy green}$ '657432'|${\color{#d8863b}dull orange}$ 'D8863B'|${\color{#738595}steel}$ '738595'|
|--|--|--|
|${\color{#aa23ff}electric purple}$ 'AA23FF'|${\color{#08ff08}fluorescent green}$ '08FF08'|${\color{#9b7a01}yellowish brown}$ '9B7A01'|
|--|--|--|
|${\color{#f29e8e}blush}$ 'F29E8E'|${\color{#6fc276}soft green}$ '6FC276'|${\color{#ff5b00}bright orange}$ 'FF5B00'|
|--|--|--|
|${\color{#fdff52}lemon}$ 'FDFF52'|${\color{#866f85}purple grey}$ '866F85'|${\color{#8ffe09}acid green}$ '8FFE09'|
|--|--|--|
|${\color{#eecffe}pale lavender}$ 'EECFFE'|${\color{#510ac9}violet blue}$ '510AC9'|${\color{#4f9153}light forest green}$ '4F9153'|
|--|--|--|
|${\color{#9f2305}burnt red}$ '9F2305'|${\color{#728639}khaki green}$ '728639'|${\color{#de0c62}cerise}$ 'DE0C62'|
|--|--|--|
|${\color{#916e99}faded purple}$ '916E99'|${\color{#ffb16d}apricot}$ 'FFB16D'|${\color{#3c4d03}dark olive green}$ '3C4D03'|
|--|--|--|
|${\color{#7f7053}grey brown}$ '7F7053'|${\color{#77926f}green grey}$ '77926F'|${\color{#010fcc}true blue}$ '010FCC'|
|--|--|--|
|${\color{#ceaefa}pale violet}$ 'CEAEFA'|${\color{#8f99fb}periwinkle blue}$ '8F99FB'|${\color{#c6fcff}light sky blue}$ 'C6FCFF'|
|--|--|--|
|${\color{#5539cc}blurple}$ '5539CC'|${\color{#544e03}green brown}$ '544E03'|${\color{#017a79}bluegreen}$ '017A79'|
|--|--|--|
|${\color{#01f9c6}bright teal}$ '01F9C6'|${\color{#c9b003}brownish yellow}$ 'C9B003'|${\color{#929901}pea soup}$ '929901'|
|--|--|--|
|${\color{#0b5509}forest}$ '0B5509'|${\color{#a00498}barney purple}$ 'A00498'|${\color{#2000b1}ultramarine}$ '2000B1'|
|--|--|--|
|${\color{#94568c}purplish}$ '94568C'|${\color{#c2be0e}puke yellow}$ 'C2BE0E'|${\color{#748b97}bluish grey}$ '748B97'|
|--|--|--|
|${\color{#665fd1}dark periwinkle}$ '665FD1'|${\color{#9c6da5}dark lilac}$ '9C6DA5'|${\color{#c44240}reddish}$ 'C44240'|
|--|--|--|
|${\color{#a24857}light maroon}$ 'A24857'|${\color{#825f87}dusty purple}$ '825F87'|${\color{#c9643b}terra cotta}$ 'C9643B'|
|--|--|--|
|${\color{#90b134}avocado}$ '90B134'|${\color{#01386a}marine blue}$ '01386A'|${\color{#25a36f}teal green}$ '25A36F'|
|--|--|--|
|${\color{#59656d}slate grey}$ '59656D'|${\color{#75fd63}lighter green}$ '75FD63'|${\color{#21fc0d}electric green}$ '21FC0D'|
|--|--|--|
|${\color{#5a86ad}dusty blue}$ '5A86AD'|${\color{#fec615}golden yellow}$ 'FEC615'|${\color{#fffd01}bright yellow}$ 'FFFD01'|
|--|--|--|
|${\color{#dfc5fe}light lavender}$ 'DFC5FE'|${\color{#b26400}umber}$ 'B26400'|${\color{#7f5e00}poop}$ '7F5E00'|
|--|--|--|
|${\color{#de7e5d}dark peach}$ 'DE7E5D'|${\color{#048243}jungle green}$ '048243'|${\color{#ffffd4}eggshell}$ 'FFFFD4'|
|--|--|--|
|${\color{#3b638c}denim}$ '3B638C'|${\color{#b79400}yellow brown}$ 'B79400'|${\color{#84597e}dull purple}$ '84597E'|
|--|--|--|
|${\color{#411900}chocolate brown}$ '411900'|${\color{#7b0323}wine red}$ '7B0323'|${\color{#04d9ff}neon blue}$ '04D9FF'|
|--|--|--|
|${\color{#667e2c}dirty green}$ '667E2C'|${\color{#fbeeac}light tan}$ 'FBEEAC'|${\color{#d7fffe}ice blue}$ 'D7FFFE'|
|--|--|--|
|${\color{#4e7496}cadet blue}$ '4E7496'|${\color{#874c62}dark mauve}$ '874C62'|${\color{#d5ffff}very light blue}$ 'D5FFFF'|
|--|--|--|
|${\color{#826d8c}grey purple}$ '826D8C'|${\color{#ffbacd}pastel pink}$ 'FFBACD'|${\color{#d1ffbd}very light green}$ 'D1FFBD'|
|--|--|--|
|${\color{#448ee4}dark sky blue}$ '448EE4'|${\color{#05472a}evergreen}$ '05472A'|${\color{#d5869d}dull pink}$ 'D5869D'|
|--|--|--|
|${\color{#3d0734}aubergine}$ '3D0734'|${\color{#4a0100}mahogany}$ '4A0100'|${\color{#f8481c}reddish orange}$ 'F8481C'|
|--|--|--|
|${\color{#02590f}deep green}$ '02590F'|${\color{#89a203}vomit green}$ '89A203'|${\color{#e03fd8}purple pink}$ 'E03FD8'|
|--|--|--|
|${\color{#d58a94}dusty pink}$ 'D58A94'|${\color{#7bb274}faded green}$ '7BB274'|${\color{#526525}camo green}$ '526525'|
|--|--|--|
|${\color{#c94cbe}pinky purple}$ 'C94CBE'|${\color{#db4bda}pink purple}$ 'DB4BDA'|${\color{#9e3623}brownish red}$ '9E3623'|
|--|--|--|
|${\color{#b5485d}dark rose}$ 'B5485D'|${\color{#735c12}mud}$ '735C12'|${\color{#9c6d57}brownish}$ '9C6D57'|
|--|--|--|
|${\color{#028f1e}emerald green}$ '028F1E'|${\color{#b1916e}pale brown}$ 'B1916E'|${\color{#49759c}dull blue}$ '49759C'|
|--|--|--|
|${\color{#a0450e}burnt umber}$ 'A0450E'|${\color{#39ad48}medium green}$ '39AD48'|${\color{#b66a50}clay}$ 'B66A50'|
|--|--|--|
|${\color{#8cffdb}light aqua}$ '8CFFDB'|${\color{#a4be5c}light olive green}$ 'A4BE5C'|${\color{#cb7723}brownish orange}$ 'CB7723'|
|--|--|--|
|${\color{#05696b}dark aqua}$ '05696B'|${\color{#ce5dae}purplish pink}$ 'CE5DAE'|${\color{#c85a53}dark salmon}$ 'C85A53'|
|--|--|--|
|${\color{#96ae8d}greenish grey}$ '96AE8D'|${\color{#1fa774}jade}$ '1FA774'|${\color{#7a9703}ugly green}$ '7A9703'|
|--|--|--|
|${\color{#ac9362}dark beige}$ 'AC9362'|${\color{#01a049}emerald}$ '01A049'|${\color{#d9544d}pale red}$ 'D9544D'|
|--|--|--|
|${\color{#fa5ff7}light magenta}$ 'FA5FF7'|${\color{#82cafc}sky}$ '82CAFC'|${\color{#acfffc}light cyan}$ 'ACFFFC'|
|--|--|--|
|${\color{#fcb001}yellow orange}$ 'FCB001'|${\color{#910951}reddish purple}$ '910951'|${\color{#fe2c54}reddish pink}$ 'FE2C54'|
|--|--|--|
|${\color{#c875c4}orchid}$ 'C875C4'|${\color{#cdc50a}dirty yellow}$ 'CDC50A'|${\color{#fd411e}orange red}$ 'FD411E'|
|--|--|--|
|${\color{#9a0200}deep red}$ '9A0200'|${\color{#be6400}orange brown}$ 'BE6400'|${\color{#030aa7}cobalt blue}$ '030AA7'|
|--|--|--|
|${\color{#fe019a}neon pink}$ 'FE019A'|${\color{#f7879a}rose pink}$ 'F7879A'|${\color{#887191}greyish purple}$ '887191'|
|--|--|--|
|${\color{#b00149}raspberry}$ 'B00149'|${\color{#12e193}aqua green}$ '12E193'|${\color{#fe7b7c}salmon pink}$ 'FE7B7C'|
|--|--|--|
|${\color{#ff9408}tangerine}$ 'FF9408'|${\color{#6a6e09}brownish green}$ '6A6E09'|${\color{#8b2e16}red brown}$ '8B2E16'|
|--|--|--|
|${\color{#696112}greenish brown}$ '696112'|${\color{#e17701}pumpkin}$ 'E17701'|${\color{#0a481e}pine green}$ '0A481E'|
|--|--|--|
|${\color{#343837}charcoal}$ '343837'|${\color{#ffb7ce}baby pink}$ 'FFB7CE'|${\color{#6a79f7}cornflower}$ '6A79F7'|
|--|--|--|
|${\color{#5d06e9}blue violet}$ '5D06E9'|${\color{#3d1c02}chocolate}$ '3D1C02'|${\color{#82a67d}greyish green}$ '82A67D'|
|--|--|--|
|${\color{#be0119}scarlet}$ 'BE0119'|${\color{#c9ff27}green yellow}$ 'C9FF27'|${\color{#373e02}dark olive}$ '373E02'|
|--|--|--|
|${\color{#a9561e}sienna}$ 'A9561E'|${\color{#caa0ff}pastel purple}$ 'CAA0FF'|${\color{#ca6641}terracotta}$ 'CA6641'|
|--|--|--|
|${\color{#02d8e9}aqua blue}$ '02D8E9'|${\color{#88b378}sage green}$ '88B378'|${\color{#980002}blood red}$ '980002'|
|--|--|--|
|${\color{#cb0162}deep pink}$ 'CB0162'|${\color{#5cac2d}grass}$ '5CAC2D'|${\color{#769958}moss}$ '769958'|
|--|--|--|
|${\color{#a2bffe}pastel blue}$ 'A2BFFE'|${\color{#10a674}bluish green}$ '10A674'|${\color{#06b48b}green blue}$ '06B48B'|
|--|--|--|
|${\color{#af884a}dark tan}$ 'AF884A'|${\color{#0b8b87}greenish blue}$ '0B8B87'|${\color{#ffa756}pale orange}$ 'FFA756'|
|--|--|--|
|${\color{#a2a415}vomit}$ 'A2A415'|${\color{#154406}forrest green}$ '154406'|${\color{#856798}dark lavender}$ '856798'|
|--|--|--|
|${\color{#34013f}dark violet}$ '34013F'|${\color{#632de9}purple blue}$ '632DE9'|${\color{#0a888a}dark cyan}$ '0A888A'|
|--|--|--|
|${\color{#6f7632}olive drab}$ '6F7632'|${\color{#d46a7e}pinkish}$ 'D46A7E'|${\color{#1e488f}cobalt}$ '1E488F'|
|--|--|--|
|${\color{#bc13fe}neon purple}$ 'BC13FE'|${\color{#7ef4cc}light turquoise}$ '7EF4CC'|${\color{#76cd26}apple green}$ '76CD26'|
|--|--|--|
|${\color{#74a662}dull green}$ '74A662'|${\color{#80013f}wine}$ '80013F'|${\color{#b1d1fc}powder blue}$ 'B1D1FC'|
|--|--|--|
|${\color{#ffffe4}off white}$ 'FFFFE4'|${\color{#0652ff}electric blue}$ '0652FF'|${\color{#045c5a}dark turquoise}$ '045C5A'|
|--|--|--|
|${\color{#5729ce}blue purple}$ '5729CE'|${\color{#069af3}azure}$ '069AF3'|${\color{#ff000d}bright red}$ 'FF000D'|
|--|--|--|
|${\color{#f10c45}pinkish red}$ 'F10C45'|${\color{#5170d7}cornflower blue}$ '5170D7'|${\color{#acbf69}light olive}$ 'ACBF69'|
|--|--|--|
|${\color{#6c3461}grape}$ '6C3461'|${\color{#5e819d}greyish blue}$ '5E819D'|${\color{#601ef9}purplish blue}$ '601EF9'|
|--|--|--|
|${\color{#b0dd16}yellowish green}$ 'B0DD16'|${\color{#cdfd02}greenish yellow}$ 'CDFD02'|${\color{#2c6fbb}medium blue}$ '2C6FBB'|
|--|--|--|
|${\color{#c0737a}dusty rose}$ 'C0737A'|${\color{#d6b4fc}light violet}$ 'D6B4FC'|${\color{#020035}midnight blue}$ '020035'|
|--|--|--|
|${\color{#703be7}bluish purple}$ '703BE7'|${\color{#fd3c06}red orange}$ 'FD3C06'|${\color{#960056}dark magenta}$ '960056'|
|--|--|--|
|${\color{#40a368}greenish}$ '40A368'|${\color{#03719c}ocean blue}$ '03719C'|${\color{#fc5a50}coral}$ 'FC5A50'|
|--|--|--|
|${\color{#ffffc2}cream}$ 'FFFFC2'|${\color{#7f2b0a}reddish brown}$ '7F2B0A'|${\color{#b04e0f}burnt sienna}$ 'B04E0F'|
|--|--|--|
|${\color{#a03623}brick}$ 'A03623'|${\color{#87ae73}sage}$ '87AE73'|${\color{#789b73}grey green}$ '789B73'|
|--|--|--|
|${\color{#ffffff}white}$ 'FFFFFF'|${\color{#98eff9}robin's egg blue}$ '98EFF9'|${\color{#658b38}moss green}$ '658B38'|
|--|--|--|
|${\color{#5a7d9a}steel blue}$ '5A7D9A'|${\color{#380835}eggplant}$ '380835'|${\color{#fffe7a}light yellow}$ 'FFFE7A'|
|--|--|--|
|${\color{#5ca904}leaf green}$ '5CA904'|${\color{#d8dcd6}light grey}$ 'D8DCD6'|${\color{#a5a502}puke}$ 'A5A502'|
|--|--|--|
|${\color{#d648d7}pinkish purple}$ 'D648D7'|${\color{#047495}sea blue}$ '047495'|${\color{#b790d4}pale purple}$ 'B790D4'|
|--|--|--|
|${\color{#5b7c99}slate blue}$ '5B7C99'|${\color{#607c8e}blue grey}$ '607C8E'|${\color{#0b4008}hunter green}$ '0B4008'|
|--|--|--|
|${\color{#ed0dd9}fuchsia}$ 'ED0DD9'|${\color{#8c000f}crimson}$ '8C000F'|${\color{#ffff84}pale yellow}$ 'FFFF84'|
|--|--|--|
|${\color{#bf9005}ochre}$ 'BF9005'|${\color{#d2bd0a}mustard yellow}$ 'D2BD0A'|${\color{#ff474c}light red}$ 'FF474C'|
|--|--|--|
|${\color{#0485d1}cerulean}$ '0485D1'|${\color{#ffcfdc}pale pink}$ 'FFCFDC'|${\color{#040273}deep blue}$ '040273'|
|--|--|--|
|${\color{#a83c09}rust}$ 'A83C09'|${\color{#90e4c1}light teal}$ '90E4C1'|${\color{#516572}slate}$ '516572'|
|--|--|--|
|${\color{#fac205}goldenrod}$ 'FAC205'|${\color{#d5b60a}dark yellow}$ 'D5B60A'|${\color{#363737}dark grey}$ '363737'|
|--|--|--|
|${\color{#4b5d16}army green}$ '4B5D16'|${\color{#6b8ba4}grey blue}$ '6B8BA4'|${\color{#80f9ad}seafoam}$ '80F9AD'|
|--|--|--|
|${\color{#a57e52}puce}$ 'A57E52'|${\color{#a9f971}spring green}$ 'A9F971'|${\color{#c65102}dark orange}$ 'C65102'|
|--|--|--|
|${\color{#e2ca76}sand}$ 'E2CA76'|${\color{#b0ff9d}pastel green}$ 'B0FF9D'|${\color{#9ffeb0}mint}$ '9FFEB0'|
|--|--|--|
|${\color{#fdaa48}light orange}$ 'FDAA48'|${\color{#fe01b1}bright pink}$ 'FE01B1'|${\color{#c1f80a}chartreuse}$ 'C1F80A'|
|--|--|--|
|${\color{#36013f}deep purple}$ '36013F'|${\color{#341c02}dark brown}$ '341C02'|${\color{#b9a281}taupe}$ 'B9A281'|
|--|--|--|
|${\color{#8eab12}pea green}$ '8EAB12'|${\color{#9aae07}puke green}$ '9AAE07'|${\color{#02ab2e}kelly green}$ '02AB2E'|
|--|--|--|
|${\color{#7af9ab}seafoam green}$ '7AF9AB'|${\color{#137e6d}blue green}$ '137E6D'|${\color{#aaa662}khaki}$ 'AAA662'|
|--|--|--|
|${\color{#610023}burgundy}$ '610023'|${\color{#014d4e}dark teal}$ '014D4E'|${\color{#8f1402}brick red}$ '8F1402'|
|--|--|--|
|${\color{#4b006e}royal purple}$ '4B006E'|${\color{#580f41}plum}$ '580F41'|${\color{#8fff9f}mint green}$ '8FFF9F'|
|--|--|--|
|${\color{#dbb40c}gold}$ 'DBB40C'|${\color{#a2cffe}baby blue}$ 'A2CFFE'|${\color{#c0fb2d}yellow green}$ 'C0FB2D'|
|--|--|--|
|${\color{#be03fd}bright purple}$ 'BE03FD'|${\color{#840000}dark red}$ '840000'|${\color{#d0fefe}pale blue}$ 'D0FEFE'|
|--|--|--|
|${\color{#3f9b0b}grass green}$ '3F9B0B'|${\color{#01153e}navy}$ '01153E'|${\color{#04d8b2}aquamarine}$ '04D8B2'|
|--|--|--|
|${\color{#c04e01}burnt orange}$ 'C04E01'|${\color{#0cff0c}neon green}$ '0CFF0C'|${\color{#0165fc}bright blue}$ '0165FC'|
|--|--|--|
|${\color{#cf6275}rose}$ 'CF6275'|${\color{#ffd1df}light pink}$ 'FFD1DF'|${\color{#ceb301}mustard}$ 'CEB301'|
|--|--|--|
|${\color{#380282}indigo}$ '380282'|${\color{#aaff32}lime}$ 'AAFF32'|${\color{#53fca1}sea green}$ '53FCA1'|
|--|--|--|
|${\color{#8e82fe}periwinkle}$ '8E82FE'|${\color{#cb416b}dark pink}$ 'CB416B'|${\color{#677a04}olive green}$ '677A04'|
|--|--|--|
|${\color{#ffb07c}peach}$ 'FFB07C'|${\color{#c7fdb5}pale green}$ 'C7FDB5'|${\color{#ad8150}light brown}$ 'AD8150'|
|--|--|--|
|${\color{#ff028d}hot pink}$ 'FF028D'|${\color{#000000}black}$ '000000'|${\color{#cea2fd}lilac}$ 'CEA2FD'|
|--|--|--|
|${\color{#001146}navy blue}$ '001146'|${\color{#0504aa}royal blue}$ '0504AA'|${\color{#e6daa6}beige}$ 'E6DAA6'|
|--|--|--|
|${\color{#ff796c}salmon}$ 'FF796C'|${\color{#6e750e}olive}$ '6E750E'|${\color{#650021}maroon}$ '650021'|
|--|--|--|
|${\color{#01ff07}bright green}$ '01FF07'|${\color{#35063e}dark purple}$ '35063E'|${\color{#ae7181}mauve}$ 'AE7181'|
|--|--|--|
|${\color{#06470c}forest green}$ '06470C'|${\color{#13eac9}aqua}$ '13EAC9'|${\color{#00ffff}cyan}$ '00FFFF'|
|--|--|--|
|${\color{#d1b26f}tan}$ 'D1B26F'|${\color{#00035b}dark blue}$ '00035B'|${\color{#c79fef}lavender}$ 'C79FEF'|
|--|--|--|
|${\color{#06c2ac}turquoise}$ '06C2AC'|${\color{#033500}dark green}$ '033500'|${\color{#9a0eea}violet}$ '9A0EEA'|
|--|--|--|
|${\color{#bf77f6}light purple}$ 'BF77F6'|${\color{#89fe05}lime green}$ '89FE05'|${\color{#929591}grey}$ '929591'|
|--|--|--|
|${\color{#75bbfd}sky blue}$ '75BBFD'|${\color{#ffff14}yellow}$ 'FFFF14'|${\color{#c20078}magenta}$ 'C20078'|
|--|--|--|
|${\color{#96f97b}light green}$ '96F97B'|${\color{#f97306}orange}$ 'F97306'|${\color{#029386}teal}$ '029386'|
|--|--|--|
|${\color{#95d0fc}light blue}$ '95D0FC'|${\color{#e50000}red}$ 'E50000'|${\color{#653700}brown}$ '653700'|
|--|--|--|
|${\color{#ff81c0}pink}$ 'FF81C0'|${\color{#0343df}blue}$ '0343DF'|${\color{#15b01a}green}$ '15B01A'|
|--|--|--|
|${\color{#7e1e9c}purple}$ '7E1E9C'


# License
Whisper's AI model weights are released under the MIT License.