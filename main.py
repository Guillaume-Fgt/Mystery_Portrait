from PIL import Image, ImageDraw
from split import split
from hash import img_shapes, compare_image_hash
import os
import shutil
import re
from typing import Iterator
import logging
from grid import draw_grid, draw_number
import PIL.ImageOps


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


def generate_shape(width: int, height: int) -> None:
    original_im = Image.new(
        "L",
        (width, height),
    )
    folder = folder_exists_or_clean("shapes")
    im = original_im.copy()
    im.save(f"{folder}/9.jpg")
    inverted_image = PIL.ImageOps.invert(im)
    inverted_image.save(f"{folder}/0.jpg")
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 0), (width, int(height / 2) - 1)], fill="white")
    im.save(f"{folder}/1.jpg")
    inverted_image = PIL.ImageOps.invert(im)
    inverted_image.save(f"{folder}/3.jpg")
    rotated = im.rotate(90)
    rotated.save(f"{folder}/2.jpg")
    inverted_image = PIL.ImageOps.invert(rotated)
    inverted_image.save(f"{folder}/4.jpg")
    im = original_im.copy()
    draw = ImageDraw.Draw(im)
    draw.polygon([(0, 0), (width - 1, 0), (0, height - 1)], fill="white")
    im.save(f"{folder}/5.jpg")
    inverted_image = PIL.ImageOps.invert(im)
    inverted_image.save(f"{folder}/7.jpg")
    rotated = inverted_image.rotate(90)
    rotated.save(f"{folder}/8.jpg")
    inverted_image = PIL.ImageOps.invert(rotated)
    inverted_image.save(f"{folder}/6.jpg")


def main(grid_size_pixel: int, image_name: str) -> None:
    logging.basicConfig(level=logging.INFO)

    logging.info("Generate shapes")
    generate_shape(grid_size_pixel, grid_size_pixel)
    logging.info("Process started")
    portrait = convert_to_BW(image_name, 105)
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
            num_shape = re.search(r"(\d+)", file_to_copy).group(0)
            new_name = re.search(r"(\d+)", name).group(0)
            shutil.copyfile(file_to_copy, f"{forms_folder}/{new_name}_{num_shape}.jpg")

    # creation of the mystery image:
    logging.info("Creation of the mystery image")
    mystery_image = Image.new("L", (crop_width, crop_height))
    img_matrice = iterator_PIL(crop_width, crop_height, grid_size_pixel)
    list_files = get_list_files("forms")
    for index, value in enumerate(img_matrice):
        form_image = Image.open(list_files[index])
        # form_image = Image.open("shapes/0.jpg") #without shapes
        number = re.search(r"(\d+)_(\d+)", list_files[index]).group(2)
        draw_number(form_image, grid_size_pixel, number)
        mystery_image.paste(
            form_image,
            box=value,
        )
    draw_grid(mystery_image, grid_size_pixel, crop_height, crop_width)
    mystery_image.save(f"Mystery_Portrait_{image_name}")


if __name__ == "__main__":
    main(30, "ND.jpg")
