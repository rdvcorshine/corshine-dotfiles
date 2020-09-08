#!/usr/bin/env python

import os
from datetime import datetime

screenshot_dir    = "/home/corshine/Arch-Corshine/Screenshots"
os.chdir(screenshot_dir)
original_file     = datetime.now().strftime("Screenshot_%Y-%m-%d_%H-%M-%S.png")
target            = list(original_file)
target.insert(-4, 'X')
target_file       = ''.join(target)
color_profile     = "/usr/share/color/icc/colord/sRGB.icc"
border_size       = "7"
background_color  = "white" # "none" for transparent
background_size   = "15"
shadow_size       = "50x20+0+20"
font              = "JetBrains-Mono-Medium"
font_size         = "15"
color_fg          = "#ffffff"
color_bg          = "#666666"
author_position   = ["NorthEast", "+80+16"]
author            = "Author: "+ \
                    os.popen("echo $USER").read().rstrip("\n")

os.system(f"""
flameshot gui --raw > {original_file}

convert {original_file} -bordercolor '{color_bg}' -border {border_size} \
{target_file}

convert {target_file} \
     \( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,5 5,0 fill white circle 5,5 5,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
     \) -alpha off -compose CopyOpacity -composite {target_file} \

convert {target_file} \\( +clone -background black \
-shadow {shadow_size} \\) +swap -background none \
-layers merge +repage {target_file}

convert {target_file} -bordercolor {background_color} \
-border {background_size} {target_file}

echo -n " {author} " | convert {target_file} \
-gravity {author_position[0]} -pointsize {font_size} -fill '{color_fg}' \
-undercolor '{color_bg}' -font {font} \
-annotate {author_position[1]} @- {target_file}

convert {target_file} -gravity South -chop 0x{int(background_size)/2} \
{target_file}

convert {target_file} -gravity North -background {background_color} \
-splice 0x{int(background_size)/2} {target_file}

convert {target_file} -profile {color_profile} {target_file} \

xclip -selection clipboard -i {target_file} -t image/png \

""")

if os.system("which optipng > /dev/null 2>&1"):
    os.system(f"optipng {target_file}")

list_file = os.popen("ls -p | grep -v /").read().split("\n")[:-1]
last_file = list_file[-1]
#os.system(f"rm -rf {original_file}")
