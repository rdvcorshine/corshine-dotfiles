#!/usr/bin/env python

import os

# Please write your screenshot dir with full path. Later, I'll improve this.
screenshot_dir    = "/home/corshine/Arch-Corshine/Screenshots"
os.chdir(screenshot_dir)
ss_dir           = os.getcwd()
list_file        = os.popen("ls -p | grep -v /").read().split("\n")[:-1]
original_file    = list_file[-1]
target           = list(original_file)
target.insert(-4, 'X')
target_file      = ''.join(target)
color_profile    = "/usr/share/color/icc/colord/sRGB.icc"
color_fg         = "#ffffff"
color_bg         = "#666666"
border_size      = "7"
background_color = "#282a36"
background_size  = "10"
shadow_size      = "50x20+0+20"
font             = "JetBrains-Mono-Medium"
font_size        = "11"
color_fg         = "#ffffff"
color_bg         = "#666666"
author_position  = ["NorthEast", "+90+16"]
author           = "Author: @" + \
                   os.popen("echo $USER").read().rstrip("\n")

os.system(f"""
convert {original_file} -bordercolor '{color_bg}' -border {border_size} \
{target_file}

convert {target_file} \\( +clone -background black \
-shadow {shadow_size} \\) +swap -background none \
-layers merge +repage {target_file}; \

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

convert {target_file} -profile {color_profile} {target_file}
""")

if os.system("which optipng > /dev/null 2>&1"):
    os.system(f"optipng {target_file}")
    print("OPTIPNG DONE!")

print(f"""SS_DIR: {ss_dir}
SOURCE: {original_file}
TARGET: {target_file}
FRAMING SUCCESS!""")
