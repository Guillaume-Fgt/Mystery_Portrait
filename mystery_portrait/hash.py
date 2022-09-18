from PIL import Image
import imagehash
import os


def hash_shapes() -> dict[str, str]:
    hash_dict = {}
    for root, _, files in os.walk("shapes"):
        for name in files:
            with Image.open(os.path.join(root, name)) as image:
                hash = imagehash.phash(image)
                hash_dict[name] = str(hash)
    return hash_dict


def img_shapes():
    list_image = []
    for root, _, files in os.walk("shapes"):
        for name in files:
            list_image.append(os.path.join(root, name))
    return list_image


def compare_image_hash(image1: Image.Image, image2: Image.Image) -> int:
    """compare hash of 2 images. Returns hamming distance"""
    hash1 = imagehash.phash(image1)
    hash2 = imagehash.phash(image2)
    return hash1 - hash2
