import argparse

from PIL import Image, ImageFilter, ImageOps
from lib import resize_by_multiples
from collections import Counter
from colr import Colr as c

parser = argparse.ArgumentParser()
parser.add_argument('path', help="path to image file")
parser.add_argument('--kernel', dest='kernel', metavar='K', type=int, default=3, help="size of the kernel")
parser.add_argument('--no-color', dest='no-color', help="Print without coloration", action='store_true')
args = vars(parser.parse_args())

KERN = args['kernel']

assert(args.get('path', 0)), "A file path was not provided!"

ascii_fillers = ["*", "&", "#", "@", "0", "%", "^", "S", "=", "~", ":" ",", "!"]

orig = resize_by_multiples(Image.open(args['path']), KERN)
mode_filter = ImageFilter.ModeFilter(size=KERN)

color_img = orig.filter(mode_filter).filter(ImageFilter.EDGE_ENHANCE_MORE)
color_img = ImageOps.posterize(color_img, 3)

grey_img = color_img.convert("L")

orig = orig.filter(ImageFilter.GaussianBlur)
grey_pxl = grey_img.load()
color_pxl = orig.load()

min_grey_value = 254//(len(ascii_fillers)-1)
w, h = grey_img.size

for y_step in range(0, h, KERN*KERN):
    line = []  # [(char, color), ...]
    for x_step in range(0, w, KERN*KERN):
        grey_kern = Counter([grey_pxl[x_step+x, y_step+y] for y in range(KERN) for x in range(KERN)]).most_common()
        color_kern = Counter([color_pxl[x_step+x, y_step+y] for y in range(KERN) for x in range(KERN)]).most_common()
        char = ascii_fillers[grey_kern[0][0]//min_grey_value]
        color = color_kern[0][0]
        line.append((char, color))

    if args.get('no-color', 0):
        print(*[char for char, color in line])
    else:
        print(*[c().rgb(*color, char) for char, color in line])
