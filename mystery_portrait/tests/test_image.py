from mystery_portrait import image
from PIL import Image


def test_get_aspect_ratio() -> None:
    im = Image.new("RGB", (2, 2))
    assert image.get_aspect_ratio(im) == 1
