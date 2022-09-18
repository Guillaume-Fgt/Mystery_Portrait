from PIL import Image
import shutil
import logging
from pathlib import Path
from mystery_portrait.image import (
    generate_shape,
    convert_to_BW,
    split,
    find_closest_shape,
    create_mystery,
)
from mystery_portrait.utils import (
    mm_dpi_to_px,
    closest_modulo_zero,
    folder_exists_or_clean,
)


def main(
    width_mm: float,
    height_mm: float,
    dpi: int,
    image_path: str,
    grid_size_mm: float,
    grid_color: str,
    bw_threshold: int,
    border_color: str,
    border_thickness: int,
):

    logging.basicConfig(level=logging.INFO)

    logging.info("Finding pX dimensions")
    # dimensions in px for the desired dpi and dimensions in mm
    width_px = mm_dpi_to_px(dpi, width_mm)
    height_px = mm_dpi_to_px(dpi, height_mm)
    grid_size_px = mm_dpi_to_px(dpi, grid_size_mm)

    # dimensions to have entire grid tile on x and y axis
    resize_width = closest_modulo_zero(width_px, grid_size_px)
    resize_height = closest_modulo_zero(height_px, grid_size_px)

    logging.info("Generate shapes")
    shape_folder = folder_exists_or_clean("shapes")
    generate_shape(shape_folder, grid_size_px, grid_size_px)

    # resize image accordingly
    with Image.open(image_path) as image:
        im = image.resize((resize_width, resize_height))
        im_bw = convert_to_BW(im, bw_threshold)

    logging.info("Split started")
    split_folder = folder_exists_or_clean("split")
    split(
        im_bw,
        resize_width // grid_size_px,
        resize_height // grid_size_px,
        split_folder,
    )

    # find the closest shape for each splitted part
    forms_folder = folder_exists_or_clean("forms")
    logging.info("Searching for closest shape")
    find_closest_shape(split_folder, shape_folder, forms_folder)

    # creation of the mystery image:
    logging.info("Creation of the mystery image")

    bordered_image = create_mystery(
        resize_width,
        resize_height,
        grid_size_px,
        grid_color,
        border_color,
        border_thickness,
    )

    # saving the final image to original folder
    path = Path(image_path)
    portrait_path = path.parent / f"mystery_portrait_{path.name}"
    bordered_image.save(portrait_path, dpi=(300, 300))

    # removing working folders
    shutil.rmtree(shape_folder)
    shutil.rmtree(forms_folder)
    shutil.rmtree(split_folder)


if __name__ == "__main__":
    main(
        190, 277, 300, "C:/Users/guill/Downloads/Keanu.jpg", 4, "grey", 105, "black", 3
    )
