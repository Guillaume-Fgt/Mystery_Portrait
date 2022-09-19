from PIL import Image, ImageDraw
from pathlib import Path


def draw_polygon(
    width: int, height: int, coordinates: list[tuple], color: str, filename: str
) -> None:
    new_im = Image.new("L", (width, height))
    draw = ImageDraw.Draw(new_im)
    draw.polygon(coordinates, fill=color)
    new_im.save(f"{filename}")


def generate_shapes(folder: Path, width: int, height: int) -> None:
    """generate the 10 basics shapes used to create a mystery image"""
    all_shapes = {
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

    for key, value in all_shapes.items():
        draw_polygon(width, height, value, "white", f"{folder}/{key}.jpg")
