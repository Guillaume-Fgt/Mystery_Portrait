from PIL import Image, ImageDraw
from pathlib import Path


def generate_dict_shapes(width: int, height: int) -> dict:
    """return a dict with coordinates to create polygon shapes"""
    all_shapes = {
        "dim": (width, height),
        0: [(0, 0), (0, height), (width, height), (width, 0)],
        1: [(0, 0), (0, (height / 2) - 1), (width, (height / 2) - 1), (width, 0)],
        2: [(0, 0), (0, height), ((width / 2) - 1, height), ((width / 2) - 1, 0)],
        3: [(0, height / 2), (0, height), (width, height), (width, height / 2)],
        4: [(width / 2, 0), (width / 2, height), (width, height), (width, 0)],
        5: [(0, 0), (0, height - 1), (width - 1, 0)],
        6: [(0, 0), (0, height - 1), (width - 1, height - 1)],
        7: [(0, height - 1), (width, height - 1), (width - 1, 0)],
        8: [(0, 0), (width - 1, height - 1), (width - 1, 0)],
        9: [(-1, -1), (-1, -1)],
    }
    return all_shapes


def generate_shape(folder: Path, dict_shapes: dict) -> None:
    """read a dict of shapes and ask to draw them"""
    width, height = dict_shapes.pop("dim")
    for key, value in dict_shapes.items():
        new_im = Image.new("RGB", (width, height))
        draw_polygon(new_im, value, "white")
        new_im.save(f"{folder}/{key}.jpg")


def draw_polygon(im: Image.Image, coordinates: list[tuple], color: str) -> None:
    """draw a polygon over an image"""
    draw = ImageDraw.Draw(im)
    draw.polygon(coordinates, fill=color)
