from typing import Generator
from mystery_portrait import utils
import pytest
from PIL import Image
import os
import shutil


def test_closest_modulo_zero() -> None:
    assert utils.closest_modulo_zero(5, 3) == 3


def test_closest_modulo_zero_zero() -> None:
    with pytest.raises(
        ValueError, match="The grid's square size cannot be equal to zero"
    ):
        utils.closest_modulo_zero(3, 0)


def test_mm_dpi_to_px() -> None:
    assert utils.mm_dpi_to_px(300, 210) == 2480


@pytest.fixture
def folder_with_files() -> Generator:
    current_directory = os.getcwd()
    os.makedirs("test_utils")
    for i in range(3):
        new_image = Image.new("RGB", (200, 200))
        new_image.save(f"{current_directory}/test_utils/{i}_0.jpg")
    yield f"{current_directory}/test_utils"
    shutil.rmtree(f"{current_directory}/test_utils")


def test_folder_exists_or_clean_not_existing(folder_with_files) -> None:
    shutil.rmtree(folder_with_files)
    utils.folder_exists_or_clean("test_utils")
    assert os.path.exists("test_utils")
