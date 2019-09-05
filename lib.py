from PIL import Image


def resize_by_multiples(image, char_limit=80, multiple=9):
    max_val = multiple*char_limit
    h = image.height
    w = image.width

    if w > max_val:
        w_final = max_val
        h_cut = w-max_val
        h_diff = multiple * (h_cut % multiple)

    else:
        w_diff = w % multiple
        h_diff = h % multiple
        w_final = w-w_diff if w_diff != 0 else w

    h_final = h - h_diff if h_diff != 0 else h

    if h_final != h or w_final != w:
        return image.resize((w_final, h_final), Image.NEAREST)
    else:
        return image
