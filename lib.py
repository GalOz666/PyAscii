from PIL import Image


def resize_by_multiples(image, multiple=9, max_val=1720):
    h = image.height
    w = image.width
    if w > max_val:
        h_diff = w-max_val
        w_diff = max_val
    else:
        h_diff = h % multiple
        w_diff = w % multiple

        h_diff = h-h_diff if h_diff != 0 else 0
        w_diff = w-w_diff if h_diff != 0 else 0

    if h_diff or w_diff:
        return image.resize((w_diff, h_diff), Image.NEAREST)
    else:
        return image
