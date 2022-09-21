from PIL import Image
import imagehash


def compare_image_hash(image1: Image.Image, image2: Image.Image) -> int:
    """compare hash of 2 images. Returns hamming distance"""
    hash1 = imagehash.phash(image1)
    hash2 = imagehash.phash(image2)
    return hash1 - hash2
