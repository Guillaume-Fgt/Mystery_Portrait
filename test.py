# import itertools


# def lines_coord():
#     vertical_lines = itertools.product(range(0, 300, 20), (0, 440))
#     horizontal_lines = itertools.product((0, 300), range(0, 440, 20))

#     args_vert = [iter(vertical_lines)] * 2
#     args_hor = [iter(horizontal_lines)] * 2
#     return zip(*args_vert)


# for element in lines_coord():
#     print(element)

# import re

# string_test = "0_9.jpg"
# number = re.search(r"(\d+)_(\d+)", string_test).group(2)
# print(number + "OK")

# from PIL import Image, ImageDraw
# import os
# from grid import draw_number
# from main import folder_exists_or_clean
# import PIL.ImageOps

# # for root, _, files in os.walk("shapes"):
# #     for name in files:
# #         im = Image.open(os.path.join(root, name))
# #         draw_number(im, 20, 2)
# #         im.show()


# def generate_shape(width: int, height: int) -> None:
#     original_im = Image.new(
#         "L",
#         (width, height),
#     )
#     folder = folder_exists_or_clean("shape")
#     im = original_im.copy()
#     im.save(f"{folder}/9.jpg")
#     inverted_image = PIL.ImageOps.invert(im)
#     inverted_image.save(f"{folder}/0.jpg")
#     draw = ImageDraw.Draw(im)
#     draw.rectangle([(0, 0), (width, int(height / 2) - 1)], fill="white")
#     im.save(f"{folder}/1.jpg")
#     inverted_image = PIL.ImageOps.invert(im)
#     inverted_image.save(f"{folder}/3.jpg")
#     rotated = im.rotate(90)
#     rotated.save(f"{folder}/2.jpg")
#     inverted_image = PIL.ImageOps.invert(rotated)
#     inverted_image.save(f"{folder}/4.jpg")
#     im = original_im.copy()
#     draw = ImageDraw.Draw(im)
#     draw.polygon([(0, 0), (width - 1, 0), (0, height - 1)], fill="white")
#     im.save(f"{folder}/5.jpg")
#     inverted_image = PIL.ImageOps.invert(im)
#     inverted_image.save(f"{folder}/7.jpg")
#     rotated = inverted_image.rotate(90)
#     rotated.save(f"{folder}/8.jpg")
#     inverted_image = PIL.ImageOps.invert(rotated)
#     inverted_image.save(f"{folder}/6.jpg")


# generate_shape(20, 20)

# from main import closest_modulo_zero

# print(closest_modulo_zero(2481, 60))
# print(closest_modulo_zero(3507, 60))

from grid import draw_grid
from PIL import Image
from main import closest_modulo_zero, crop_image


img = Image.new("RGB", (3480, 2460))
# A4 format at 300 DPI (a bit lower to have dims modulo 60 = 0)
# draw_grid(img, 60, 3480, 2460, "grey")
# img.save("test.jpg", dpi=(300, 300))
print(img.info)


def get_aspect_ratio(image: Image):
    width, height = image.size
    return width / height


def create_canvas(aspect_ratio: float) -> Image:
    if aspect_ratio < 1:
        img = Image.new("RGB", (2460, 3480))
    else:
        img = Image.new("RGB", (3480, 2460))
    return img


aspect = get_aspect_ratio(Image.open("Eastwood.jpg"))
image = create_canvas(aspect)
print(image.size)
