from typing import Generator
from mystery_portrait import image
from PIL import Image
import pytest
from mystery_portrait.utils import folder_exists_or_clean
import shutil
from pathlib import Path
import imagehash


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


def test_draw_grid(create_image) -> None:
    hash1 = imagehash.phash(create_image)
    image.draw_grid(create_image, 1, 2, 2, "white")
    hash2 = imagehash.phash(create_image)
    assert hash1 != hash2


def test_draw_number(create_image) -> None:
    hash1 = imagehash.phash(create_image)
    image.draw_number(create_image, 1, 2, "white")
    hash2 = imagehash.phash(create_image)
    assert hash1 != hash2


@pytest.fixture
def folder_split() -> Generator[Path, None, None]:
    folder = folder_exists_or_clean("split")
    for i, j in ((0, "white"), (1, "black")):
        new_image = Image.new("RGB", (2, 2), j)
        new_image.save(f"{folder}/{i}.jpg")
    yield folder
    shutil.rmtree(folder)


@pytest.fixture
def folder_split_wrong_name() -> Generator[Path, None, None]:
    folder = folder_exists_or_clean("split")
    for i, j in (("zero", "black"), ("one", "white")):
        new_image = Image.new("RGB", (2, 2), j)
        new_image.save(f"{folder}/{i}.jpg")
    yield folder
    shutil.rmtree(folder)


@pytest.fixture
def folder_shape() -> Generator[Path, None, None]:
    folder = folder_exists_or_clean("shape")
    for i, j in ((0, "black"), (1, "white")):
        new_image = Image.new("RGB", (2, 2), j)
        new_image.save(f"{folder}/{i}.jpg")
    yield folder
    shutil.rmtree(folder)


@pytest.fixture
def folder_shape_wrong_name() -> Generator[Path, None, None]:
    folder = folder_exists_or_clean("shape")
    for i, j in (("zero", "black"), ("one", "white")):
        new_image = Image.new("RGB", (2, 2), j)
        new_image.save(f"{folder}/{i}.jpg")
    yield folder
    shutil.rmtree(folder)


def test_find_closest_shape(folder_split, folder_shape, create_folder) -> None:
    image.find_closest_shape(folder_split, folder_shape, create_folder)
    list_files = []
    for element in create_folder.iterdir():
        list_files.append(element.name)
    assert list_files == ["0_1.jpg", "1_0.jpg"]


def test_find_closest_shape_value_error_num_shape(
    folder_split, folder_shape_wrong_name, create_folder
) -> None:
    with pytest.raises(ValueError, match="Unable to find num of shape file one.jpg"):
        image.find_closest_shape(folder_split, folder_shape_wrong_name, create_folder)


def test_find_closest_split_value_error_num_shape(
    folder_split_wrong_name, folder_shape, create_folder
) -> None:
    with pytest.raises(ValueError, match="Unable to find num of split file one.jpg"):
        image.find_closest_shape(folder_split_wrong_name, folder_shape, create_folder)


@pytest.fixture
def folder_mystery() -> Generator:
    folder = folder_exists_or_clean("forms")
    for i in range(3):
        new_image = Image.new("RGB", (5, 5))
        new_image.save(f"{folder}/{i}_0.jpg")
    yield folder
    shutil.rmtree(folder)


def test_create_mystery(folder_mystery) -> None:
    im = image.create_mystery(10, 5, 5, "black", True, folder_mystery)
    width, height = im.size
    assert width, height == (10, 5)
