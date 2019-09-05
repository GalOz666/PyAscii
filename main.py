from PIL import Image, ImageFilter, ImageOps
from lib import grey_highpass, resize_by_multiples, GreyCharacter
from collections import Counter

from colr import Colr as c

KERN = 3

ascii_fillers = ["*", "&", "#", "@", "0", "%", "^", "S", "=", "~", ":" ","]
# up = GreyCharacter("|", [[0, 1, 0]*3])
# middle = GreyCharacter("--", [[0, 0, 0], [1, 1, 1], [0, 0, 0]])


color_img = resize_by_multiples(Image.open("ravi.jpeg"), KERN)
mode_filter = ImageFilter.ModeFilter(size=KERN)

color_img = ImageOps.posterize(color_img, 3).filter(mode_filter).filter(ImageFilter.EDGE_ENHANCE_MORE)

grey_img = color_img.convert("L")
# clamp_img = grey_img.point(lambda i: grey_highpass(80, i, hard=True))

# bin_pxl = clamp_img.load()
grey_pxl = grey_img.load()
color_pxl = color_img.load()


min_grey_value = 254//(len(ascii_fillers)-1)
w, h = grey_img.size

for y_step in range(0, h, KERN*KERN):
    line = []  # [(char, color), ...]
    for x_step in range(0, w, KERN*KERN):
        # binary_kern = [bin_pxl[x_step+x, y_step+y] for y in range(KERN) for x in range(KERN)])
        grey_kern = Counter([grey_pxl[x_step+x, y_step+y] for y in range(KERN) for x in range(KERN)]).most_common()
        color_kern = Counter([color_pxl[x_step+x, y_step+y] for y in range(KERN) for x in range(KERN)]).most_common()
        char = ascii_fillers[grey_kern[0][0]//min_grey_value]
        color = color_kern[0][0]
        line.append((char, color))

    # print(*[c().rgb(*color, char) for char, color in line])
    print([(*color, char) for char, color in line])
    print(*color)



#
# grey_img.save('ravipost.jpeg')
# color_img2.save('posterravi.jpeg')
