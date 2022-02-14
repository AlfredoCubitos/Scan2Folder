import re
from wand.image import Image
import pytesseract
from pytesseract import Output
import numpy as np

## pagesize definitions
## ANSI: https://pixelsconverter.com/us-paper-sizes-to-pixels
## DIN:  https://www.a4-size.com/a4-size-in-pixels
##             dpi:(width,height)

pagesize = {
        "A4":{
            "Portrait":{
                72:(586,842),
                96:(794,1123),
                150:(1240,1754),
                300:(2480,3508),
                600:(4961,7016)
                },
            "Landscape":{}
            }
    }

#print(pagesize['A4']['Portrait'][300])


def check_orientation(file):
    with Image(filename=file) as image:
        img = np.array(image)
        osd = pytesseract.image_to_osd(img)
        angle = re.search('(?<=Rotate: )\d+', osd).group(0)
        #script = re.search('(?<=Script: )\w+', osd).group(0)

        if int(angle) > 0:
            with image.clone() as rotated:
                rotated.rotate((int(angle)*-1))
                rotated.save(filename=file)

def deskew(file):
    with Image(filename=file) as image:
        with image.clone() as skewed:
            skewed.deskew(0.4)
            skewed.reset_coords()
            skewed.save(filename=file)

def crop(file, left=0, top=0, width=None, height=None):
    with Image(filename=file) as image:
        with image.clone() as croped:
            croped.crop(left,top,width+left,height)
            croped.save(filename=file)
###
# file: image File
# size: page Size e.g. "A4"
# ori:  page orintation
# dpi:  scan resolution e.g. 300
###
def crop_resize(file, left=0, top=0, width=None, height=None, size="A4", ori="Portrait" , dpi=300):

    wi, hei = pagesize[size][ori][dpi]
    print(width, " " , height)
    with Image(filename=file) as image:
        w, h = image.size
        image.transform(crop=f"{width}x{height}+{left}+{top}",resize=f"{wi}x{hei}")
        image.save(filename=file)

def enhance_image(file):

            #   r,  g, b
    matrix = [[0.98, 0, 0], #red
              [0, 0.99, 0], #green
              [0, 0, 1]]    #blue

    with Image(filename=file) as image:

        with image.clone() as enhance:
            enhance.color_matrix(matrix)
            enhance.normalize()
            enhance.level(0.1,0.9)
            enhance.sharpen(1)
            enhance.save(filename=file)

def create_pdf(file,name):
    pdf = pytesseract.image_to_pdf_or_hocr(file,lang='deu', extension='pdf')
    with open(name+'.pdf', 'w+b') as f:
        f.write(pdf)

