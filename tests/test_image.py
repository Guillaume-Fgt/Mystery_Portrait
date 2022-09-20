from typing import Generator
from mystery_portrait import image
from PIL import Image
import pytest
from mystery_portrait.utils import folder_exists_or_clean
import shutil
from pathlib import Path


@pytest.fixture
def create_image() -> Image.Image:
    return Image.new("RGB", (2, 2))


@pytest.fixture
def create_folder() -> Generator[Path, None, None]:
    folder = folder_exists_or_clean("test_folder")
    yield folder
    shutil.rmtree("test_folder")


def test_get_aspect_ratio(create_image) -> None:
    assert image.get_aspect_ratio(create_image) == 1


def test_convert_to_BW(create_image) -> None:
    im_bw = image.convert_to_BW(create_image, 100)
    assert im_bw.mode == "L"


def test_add_border(create_image) -> None:
    bordered = image.add_border(create_image, "black", 2)
    or_width, or_height = create_image.size
    width, height = bordered.size
    assert width, height == (or_width + 2, or_height + 2)


def test_iterator_PIL() -> None:
    iterator = image.iterator_PIL(10, 5, 5)
    assert list(iterator) == [(0, 0), (5, 0)]


def test_split(create_image, create_folder) -> None:
    image.split(create_image, 2, 2, create_folder)
    list_files = list(create_folder.iterdir())
    assert len(list_files) == 4
