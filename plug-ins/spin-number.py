#!/usr/bin/env python
#
# Copy this in ~/.gimp-2.x/plug-ins/
# and restart gimp

import math
from gimpfu import *

def SpinNumber(height, width, num, fontname, fontsize):
    """
    Create an image with a number in it, then move it up in separate layers
    (frames) until another number is shown.  This is to give the effect of an
    odometer
    
    Params:
      height: height of image in pixels
      width: width of image in pixels
      num: which number to show when animation finished (0-9)
      fontname: font to use for the numbers
      fontsize: size of the font to use.
    """
    img = gimp.Image(height, width, RGB)
    img.disable_undo()

    prev_num = num - 1
    if prev_num < 0:
        prev_num = 9
    txt = '%d\n%d' % (prev_num, num)
    steps = 8
    (txt_w, txt_h, ascent, descent) = pdb.gimp_text_get_extents_fontname( 
        txt, fontsize, PIXELS, fontname) 
    start_y = (txt_h / 2) - height
    print start_y
    for index in range(steps):
        y = start_y - index * (float(height) / (steps - 1))
        OneLayer(img, width, height, fontname, fontsize, txt, index, y)

    img.enable_undo()
    gimp.Display(img)
    gimp.displays_flush()
    fname = "num-%d.gif" % num,
    # pdb.file_gif_save(
    #     1, # Interactive mode
    #     img,
    #     pdb.gimp_image_get_active_drawable(img),
    #     fname,
    #     fname,
    #     0, # interlace
    #     1, # loop
    #     250, # ms
    #     0)

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
    layer = gimp.Layer(img, "layer-%d (200ms)" % index, 
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
                (PF_STRING, "fontname", "Font Name", "FreeSans Bold"),
                (PF_INT, "fontsize", "Font Size", 32),
        ],
        [],
        SpinNumber
        )

main()
