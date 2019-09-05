from PIL import Image


def grey_highpass(limit: int, pixel_value: int, hard=False) -> int:
    if hard:
        val = 255 if pixel_value >= limit else 0
    else:
        val = pixel_value if pixel_value >= limit else 0
    return val


def binary_highpass(pixel_value, limit):
    return pixel_value >= limit


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


class GreyCharacter:

    def __init__(self, char_representation, bool_kernel):
        self.char_representation = char_representation
        self.bool_kernel = bool_kernel

    def similarity_score(self, ext_bool_kernel):
        assert(len(ext_bool_kernel) == len(self.bool_kernel)), "kernel sizes are not the same!"
        score = 0
        for pix1, pix2 in zip(self.bool_kernel, ext_bool_kernel):
            if pix1 == pix2:
                score += 1
