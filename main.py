from PIL import Image, ImageDraw
from split import split
from hash import img_shapes, compare_image_hash
import os
import shutil
import re
from typing import Iterator
import logging


def convert_to_BW(image_path: str, threshold: int) -> Image:
    with Image.open(image_path) as portrait:
        portrait_gray = portrait.convert("L")
        portrait_threshold = portrait_gray.point(
            lambda x: 255 if x > threshold else 0
        )  # noqa: E501
        return portrait_threshold


def closest_modulo_zero(num1: int, num2: int) -> int:
    while num1 % num2 != 0:
        num1 -= 1
    return num1


def crop_image(image: Image, crop_width: int, crop_height: int) -> Image:
    crop_left = (crop_width - crop_width) / 2
    crop_right = crop_left + crop_width
    crop_upper = (crop_height - crop_height) / 2
    crop_lower = crop_upper + crop_height
    portrait_crop = image.crop((crop_left, crop_upper, crop_right, crop_lower))
    return portrait_crop


def folder_exists_or_clean(name: str) -> str:
    """creates a folder if not exists else delete and recreates. Returns path"""
    current_directory = os.getcwd()
    if not os.path.exists(name):
        os.makedirs(name)
    else:
        shutil.rmtree(name)
        os.makedirs(name)
    return f"{current_directory}/{name}"


def get_list_files(folder: str) -> list[str]:
    list_files = []
    for root, _, files in os.walk(folder):
        files.sort(key=lambda f: int(re.sub("\D", "", f)))
        for name in files:
            list_files.append(os.path.join(root, name))
    return list_files


def iterator_PIL(image_width: int, image_height: int, pixel_iter: int) -> Iterator:
    for height in range(0, image_height, pixel_iter):
        for width in range(0, image_width, pixel_iter):
            yield (width, height)


def main(grid_size_pixel: int, image_name: str) -> None:
    logging.basicConfig(level=logging.INFO)

    logging.info("Process started")
    portrait = convert_to_BW(image_name, 113)
    portrait_width, portrait_height = portrait.size
    crop_width = closest_modulo_zero(portrait_width, grid_size_pixel)
    crop_height = closest_modulo_zero(portrait_height, grid_size_pixel)
    portrait_crop = crop_image(portrait, crop_width, crop_height)

    logging.info("Split started")
    split(
        portrait_crop,
        crop_width // grid_size_pixel,
        crop_height // grid_size_pixel,
        "split",
    )
    forms_folder = folder_exists_or_clean("forms")

    # find the closest shape for each splitted part
    logging.info("Searching for closest shape")
    for root, _, files in os.walk("split"):
        for name in files:
            compare_dict = {}
            name_img = Image.open(os.path.join(root, name))
            for img_shape in img_shapes():
                img = Image.open(img_shape)
                compare_dict[img_shape] = compare_image_hash(name_img, img)
            file_to_copy = min(compare_dict, key=compare_dict.get)
            shutil.copyfile(file_to_copy, f"{forms_folder}/{name}")

    # creation of the mystery image:
    logging.info("Creation of the mystery image")
    mystery_image = Image.new("L", (crop_width, crop_height))
    img_matrice = iterator_PIL(crop_width, crop_height, grid_size_pixel)
    list_files = get_list_files("forms")
    for index, value in enumerate(img_matrice):
        form_image = Image.open(list_files[index])
        # draw_img = ImageDraw.Draw(form_image)
        # draw_img.text((5, 5), f"{index}", fill=(255, 0, 0), align="center")
        mystery_image.paste(
            form_image,
            box=value,
        )
    mystery_image.save(f"Mystery_Portrait_{image_name}")
    mystery_image.show()


if __name__ == "__main__":
    main(5, "Clooney.jpg")
