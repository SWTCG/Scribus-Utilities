#!/usr/bin/env python

"""
This is scribalbum_letter.py. This script will load the images from a
directory, creating a new document of US Letter size.

USAGE: It is probably better not to already have any document in Scribus,
since memory usage can become intense when a large number of images is
used.
You are first presented with a dialog to choose either 4 or 6 images per page.
Next select a directory where your images are located. Finally, select the
types of image files, using the code you see in the last dialog.
NOTE: If you choose PDF, only the first page will be imported, and the PDF
will be rasterized.

AUTHOR: Gregory Pittman Original version: 2005.02.13, this version: 2008.07.23

LICENSE: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your option) any
later version.

"""

import scribus
import os

filetype = []
dicttype = {'j': '.jpg', 'p': '.png', 't': '.tif', 'g': '.gif', 'P': '.pdf'}
Dicttype = {'j': '.JPG', 'p': '.PNG', 't': '.TIF', 'g': '.GIF', 'P': '.PDF'}
nrimages = '0'
while (nrimages != '4') and (nrimages != '6'):
    nrimages = scribus.valueDialog('Pictures',
                                   '- US Letter Paper -\n Four or Six Images per Page?\nChange to 6 as desired', '4')
imagedir = scribus.fileDialog('Select Image Directory', 'Directories', isdir=True)
imagetype = scribus.valueDialog('Image Types',
                                'Enter the Image Types, where\n j=jpg,p=png,t=tif,g=gif,P=pdf\n "jptgP" selects all',
                                'jptgP')
for t in imagetype[0:]:
    filetype.append(dicttype[t])
    filetype.append(Dicttype[t])
d = os.listdir(imagedir)
D = []
for file in d:
    for format in filetype:
        if file.endswith(format):
            D.append(file)
D.sort()
labelFont = "DejaVu Sans Book"

# When 4 pics per page, coords are: (15, 42),(310, 187), (15, 388), (310, 533)
# When 6 pics per page: (15, 42),(310, 42), (15, 290), (310, 290),(15,533),(310,533)
# if nrimages == '4':
#     xpos = [15, 310, 15, 310]
#     ypos = [42, 187, 388, 533]
# if nrimages == '6':
#     xpos = [15, 310, 15, 310, 15, 310]
#     ypos = [42, 42, 290, 290, 533, 533]
# This proportion is right for photographs from my digital camera
pwidth = 69.35
pheight = 94.35
imagecount = 0
# framecount = 0
if len(D) > 0:
    if scribus.newDocument((69.35, 94.35), (0, 0, 0, 0), scribus.PORTRAIT, 1, scribus.UNIT_MM, scribus.PAGE_1, 0, 1):
        while imagecount < len(D):
            if imagecount > 0:
                scribus.newPage(-1)
                framecount = 0
            # L is the frame at the top of each page showing the directory name
            # L = scribus.createText(15, 20, 200, 20)
            # scribus.setText("Dir: " + imagedir, L)
            # scribus.setTextAlignment(scribus.ALIGN_LEFT, L)
            # scribus.setFont(labelFont, L)
            # scribus.setFontSize(10, L)
            # Here is where we're loading images into the page, four at a time, then go back up for a newPage
            if imagecount < len(D):
                f = scribus.createImage(0, 0, pwidth, pheight)
                scribus.loadImage(imagedir + '/' + D[imagecount], f)
                scribus.setScaleImageToFrame(scaletoframe=1, proportional=0, name=f)
                lenfilename = len(D[imagecount])
                Lpiclen = int(5.3 * lenfilename)
                # Lpic is the label for each picture, with position and length adjusted
                # according to the text length, so if you change the font or its size,
                # you may need to adjust this only approximate calculation.
                # Lpic = scribus.createText(x, y + 193, Lpiclen, 15)
                # scribus.setText(D[imagecount], Lpic)
                # scribus.setTextAlignment(scribus.ALIGN_RIGHT, Lpic)
                # scribus.setFont(labelFont, Lpic)
                # scribus.setFontSize(8, Lpic)
                # scribus.setFillColor("White", Lpic)
                imagecount += 1

    scribus.setRedraw(1)
    scribus.redrawAll()

else:
    result = scribus.messageBox('Not Found', 'No Images found with\n this search selection', scribus.BUTTON_OK)