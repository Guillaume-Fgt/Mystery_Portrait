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


def compare_image_hash(image1: Image, image2: Image) -> int:
    """compare hash of 2 images. Returns hamming distance"""
    hash1 = imagehash.phash(image1)
    hash2 = imagehash.phash(image2)
    return hash1 - hash2


# hash = imagehash.phash(Image.open("shapes/0.jpg"))
# otherhash = imagehash.phash(Image.open("shapes/9.jpg"))
# print(hash)

# print(otherhash)

# print(hash == otherhash)

# print(hash - otherhash)  # hamming distance

# >>> original_hash = imagehash.average_hash(Image.open('tests/data/imagehash.png'))
# >>> hash_as_str = str(original_hash)
# >>> print(hash_as_str)
# ffd7918181c9ffff
# >>> restored_hash = imagehash.hex_to_hash(hash_as_str)
# >>> print(restored_hash)
