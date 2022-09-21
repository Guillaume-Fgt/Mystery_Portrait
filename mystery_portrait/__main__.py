from PIL import Image
import shutil
import logging
from pathlib import Path
from mystery_portrait.config import load_config
from mystery_portrait.shapes import generate_shape, generate_dict_shapes, save_image
from mystery_portrait.image import (
    convert_to_BW,
    split,
    find_closest_shape,
    create_mystery,
    draw_grid,
    add_border,
)
from mystery_portrait.utils import (
    mm_dpi_to_px,
    closest_modulo_zero,
    folder_exists_or_clean,
)


def main() -> None:

    logging.basicConfig(level=logging.INFO)

    config = load_config("./config.json")
    logging.info("Finding pX dimensions")
    # dimensions in px for the desired dpi and dimensions in mm
    width_px = mm_dpi_to_px(config.dpi, config.width_mm)
    height_px = mm_dpi_to_px(config.dpi, config.height_mm)
    grid_size_px = mm_dpi_to_px(config.dpi, config.grid_size_mm)

    # dimensions to have entire grid tile on x and y axis
    resize_width = closest_modulo_zero(width_px, grid_size_px)
    resize_height = closest_modulo_zero(height_px, grid_size_px)

    logging.info("Generate shapes")
    shape_folder = folder_exists_or_clean("shapes")
    dict_shapes = generate_dict_shapes(grid_size_px, grid_size_px)
    generator_shape = generate_shape(dict_shapes)
    for shape, filename in generator_shape:
        save_image(shape_folder, shape, filename)

    # resize image accordingly
    with Image.open(config.image_path) as image:
        im = image.resize((resize_width, resize_height))
        im_bw = convert_to_BW(im, config.bw_threshold)

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

    mystery_im = create_mystery(
        resize_width,
        resize_height,
        grid_size_px,
        config.num_color,
        config.solution,
        forms_folder,
    )
    draw_grid(mystery_im, grid_size_px, resize_width, resize_height, config.grid_color)
    bordered_im = add_border(mystery_im, config.border_color, config.border_thickness)

    # saving the final image to original folder
    path = Path(config.image_path)
    if config.solution:
        portrait_path = path.parent / f"mystery_image_solution_{path.name}"
    else:
        portrait_path = path.parent / f"mystery_image_{path.name}"
    bordered_im.save(portrait_path, dpi=(300, 300))

    # removing working folders
    shutil.rmtree(shape_folder)
    shutil.rmtree(forms_folder)
    shutil.rmtree(split_folder)


if __name__ == "__main__":
    main()
