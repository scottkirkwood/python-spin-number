#!/usr/bin/env python
#
# Copy this in ~/.gimp-2.x/plug-ins/
# and restart gimp

import math
import os
import sys
from gimpfu import *

def SpinNumber(height, width, num, up, fontname, fontsize):
    """
    Create an image with a number in it, then move it up in separate layers
    (frames) until another number is shown.  This is to give the effect of an
    odometer
    
    Params:
      height: height of image in pixels
      width: width of image in pixels
      num: which number to show when animation finished (0-9)
      up: 1 for counting up, 0 for counting down
      fontname: font to use for the numbers
      fontsize: size of the font to use.
    """
    img = gimp.Image(height, width, RGB)
    img.disable_undo()

    if up:
        prev_num = num - 1
        if prev_num < 0:
            prev_num = 9
    else:
        prev_num = num + 1
        if prev_num > 9:
            prev_num = 0
    txt = '%d\n%d' % (prev_num, num)
    steps = 8
    (txt_w, txt_h, ascent, descent) = pdb.gimp_text_get_extents_fontname( 
        txt, fontsize, PIXELS, fontname) 
    start_y = (txt_h / 2) - height
    last_layer = 0
    for index in range(steps):
        y = start_y - index * (float(height) / (steps - 1))
        last_layer = OneLayer(img, width, height, fontname, fontsize, txt, index, y)

    img.enable_undo()
    gimp.Display(img)
    gimp.displays_flush()
    dir = 'up'
    if up == 0:
        dir = 'down'
    SaveImage(os.path.join(os.getcwd(), 'num-%s-%d.gif' % (dir, num)), img)

def SaveImage(fname, img):
    pdb.gimp_image_convert_indexed(
        img,
        2, # 2 FSlow bleed dither
        0, # Make palette
        255, # with 255 colors
        0, # Dither transparency
        1, # Remove unused
        '')
    pdb.gimp_file_save(
        img,
        img.layers[0],
        fname,
        fname)
    print "Saved to '%s'" % fname
    pdb.gimp_image_clean_all(img)

def OneLayer(img, width, height, fontname, fontsize, txt, index, y):
    """
    Create one layer and draw the text and a certain y position, centered on
    the width of the image.

    Params:
      img: image to draw on
      width: width of image in pixels
      height: height of image in pixels
      fontname: name of font used
      txt: text to draw (ex. "0\n1")
      index: index of frame (ex. 0 or 8)
      y: Y position to draw the text, may be negative
    """
    layer = gimp.Layer(img, "layer-%d (120ms)" % index, 
        width, height, RGB_IMAGE, 100, NORMAL_MODE)
    img.add_layer(layer, 0)
    pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
    (txt_w, txt_h, ascent, descent) = pdb.gimp_text_get_extents_fontname( 
        txt, fontsize, PIXELS, fontname) 
    txtfloat = pdb.gimp_text_fontname(img, img.active_layer, 
        width / 2 - txt_w / 2, y, 
        txt, -1, # Border
        True, # AntiAliased
        fontsize, PIXELS, fontname) 

    # Merge with background
    pdb.gimp_floating_sel_anchor(txtfloat)

    pdb.gimp_edit_blend(layer, 
        2, # Tranaparent mode
        2, #BEHIND-MODE,
        0, #GRADIENT_LINEAR,
        50, # Transparency
        0, # Offset,
        0, # Repeat
        0, # Reverse
        0, # Supersample
        1, # Max super sample depth
        0, # Super sample threshold
        1, # Dither
        width // 2, 0, width // 2, height // 2)

    pdb.gimp_edit_blend(layer, 
        2, # Tranaparent mode
        2, #BEHIND-MODE,
        0, #GRADIENT_LINEAR,
        50, # Transparency
        0, # Offset,
        0, # Repeat
        0, # Reverse
        0, # Supersample
        1, # Max super sample depth
        0, # Super sample threshold
        1, # Dither
        width // 2, height, width // 2, height // 2)

    return layer

register(
        "python_fu_spin_number",
        "Tool to make spinning number",
        "Tool for making a spinning number",
        "Scott Kirkwood",
        "Scott Kirkwood",
        "2007",
        "<Toolbox>/Xtns/Python-Fu/Spin Number...",
        "",
        [
                (PF_INT, "height", "Height", 32),
                (PF_INT, "width", "Width", 32),
                (PF_INT, "num", "Number", 1),
                (PF_INT, "up", "1 for couting up, 0 for counting down", 0),
                (PF_STRING, "fontname", "Font Name", "FreeSans Bold"),
                (PF_INT, "fontsize", "Font Size", 32),
        ],
        [],
        SpinNumber
        )

main()
