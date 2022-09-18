from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from mystery_portrait.hash import compare_image_hash
from typing import Iterator
import re
import shutil


def draw_grid(
    image: Image.Image, step_size: int, width: int, height: int, color: str
) -> None:

    draw = ImageDraw.Draw(image)

    y_start = 0
    y_end = height

    for x in range(step_size, width + step_size, step_size):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=color)

    x_start = 0
    x_end = width

    for y in range(step_size, height + step_size, step_size):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=color)


def draw_number(image: Image.Image, grid_size_pixel: int, num: int, color: str) -> None:
    draw = ImageDraw.Draw(image)
    myfont = ImageFont.truetype(
        "mystery_portrait/ressources/Ubuntu-Regular.ttf", grid_size_pixel - 1
    )
    msg = f"{num}"
    draw.text(
        (grid_size_pixel / 2, grid_size_pixel / 2),
        msg,
        fill=color,
        anchor="mm",
        font=myfont,
    )


def add_border(image: Image.Image, border_color: str, border_width: int) -> Image.Image:
    border_color = border_color
    image = ImageOps.expand(image, border=(border_width,) * 4, fill=border_color)
    return image


def convert_to_BW(image: Image.Image, threshold: int) -> Image.Image:
    image_gray = image.convert("L")
    image_threshold = image_gray.point(lambda x: 255 if x > threshold else 0)
    return image_threshold


def get_aspect_ratio(image: Image.Image):
    width, height = image.size
    return width / height


def iterator_PIL(image_width: int, image_height: int, pixel_iter: int) -> Iterator:
    for height in range(0, image_height, pixel_iter):
        for width in range(0, image_width, pixel_iter):
            yield (width, height)


def generate_shape(folder: Path, width: int, height: int) -> None:
    original_im = Image.new(
        "RGB",
        (width, height),
    )
    im = original_im.copy()
    im.save(f"{folder}/9.jpg")
    inverted_image = ImageOps.invert(im)
    inverted_image.save(f"{folder}/0.jpg")
    draw = ImageDraw.Draw(im)
    draw.rectangle(((0, 0), (width, int(height / 2) - 1)), fill="white")
    im.save(f"{folder}/1.jpg")
    inverted_image = ImageOps.invert(im)
    inverted_image.save(f"{folder}/3.jpg")
    rotated = im.rotate(90)
    rotated.save(f"{folder}/2.jpg")
    inverted_image = ImageOps.invert(rotated)
    inverted_image.save(f"{folder}/4.jpg")
    im = original_im.copy()
    draw = ImageDraw.Draw(im)
    draw.polygon([(0, 0), (width - 1, 0), (0, height - 1)], fill="white")
    im.save(f"{folder}/5.jpg")
    inverted_image = ImageOps.invert(im)
    inverted_image.save(f"{folder}/7.jpg")
    rotated = inverted_image.rotate(90)
    rotated.save(f"{folder}/8.jpg")
    inverted_image = ImageOps.invert(rotated)
    inverted_image.save(f"{folder}/6.jpg")


def split(im: Image.Image, rows: int, cols: int, split_dir: Path):
    im_width, im_height = im.size
    row_width = int(im_width / rows)
    row_height = int(im_height / cols)
    n = 0
    for i in range(0, cols):
        for j in range(0, rows):
            box = (
                j * row_width,
                i * row_height,
                j * row_width + row_width,
                i * row_height + row_height,
            )
            outp = im.crop(box)
            outp_path = split_dir / f"{n:04}.jpg"
            outp.save(outp_path)
            n += 1


def find_closest_shape(split_dir: Path, shape_dir: Path, form_dir: Path) -> None:
    for name in split_dir.iterdir():
        compare_dict = {}
        name_img = Image.open(name)
        for img_shape in shape_dir.iterdir():
            img = Image.open(img_shape)
            compare_dict[img_shape.name] = compare_image_hash(name_img, img)
        file_to_copy = min(compare_dict, key=lambda x: compare_dict.get(x, 10))
        num_shape_re = re.search(r"(\d+)", file_to_copy)
        if num_shape_re:
            num_shape = num_shape_re.group(0)
        else:
            raise ValueError(f"Unable to find num of shape file {file_to_copy}")
        new_name_re = re.search(r"(\d+)", name.name)
        if new_name_re:
            new_name = new_name_re.group(0)
        else:
            raise ValueError(f"Unable to find num of split file {name.name}")
        shutil.copyfile(
            shape_dir / f"{file_to_copy}", form_dir / f"{new_name}_{num_shape}.jpg"
        )


def create_mystery(
    width: int,
    height: int,
    grid_size: int,
    grid_color: str,
    border_color: str,
    border_thickness: int,
) -> Image.Image:
    mystery_image = Image.new("RGB", (width, height))
    img_matrice = iterator_PIL(width, height, grid_size)
    list_files = [files.name for files in Path("forms").iterdir()]
    for index, value in enumerate(img_matrice):
        form_image = Image.open(Path("forms") / list_files[index])
        # form_image = Image.open("shapes/0.jpg")  # without shapes
        re_number = re.search(r"(\d+)_(\d+)", list_files[index])
        if re_number:
            number = re_number.group(2)
        else:
            raise ValueError(f"Number for {list_files[index]} not found!")
        draw_number(form_image, grid_size, int(number), grid_color)
        mystery_image.paste(
            form_image,
            box=value,
        )
    draw_grid(mystery_image, grid_size, width, height, "grey")
    return add_border(mystery_image, border_color, border_thickness)
