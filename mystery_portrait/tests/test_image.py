from mystery_portrait import image
from PIL import Image
import pytest


@pytest.fixture
def create_image() -> Image.Image:
    return Image.new("RGB", (2, 2))


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
