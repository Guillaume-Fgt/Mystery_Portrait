import os
import shutil
from pathlib import Path
from typing import Generator


def folder_exists_or_clean(name: str) -> Path:
    """create an empty folder 'name' and return its absolute path"""
    if not os.path.exists(name):
        os.makedirs(name)
    else:
        shutil.rmtree(name)
        os.makedirs(name)
    return Path(name)


def closest_modulo_zero(num1: int, num2: int) -> int:
    if num2 == 0:
        raise ValueError("The grid's square size cannot be equal to zero")
    while num1 % num2 != 0:
        num1 -= 1
    return num1


def mm_dpi_to_px(dpi: int, dim_mm: float) -> int:
    """take a dpi and dimension in mm and return dimension needed in pixel"""
    dim_px = (dpi * dim_mm) // 25.4  # 1inch=25.4mm, DPI:Dot Per Inch
    return int(dim_px)


def list_files_from_dir(dir: Path) -> Generator[Path, None, None]:
    return dir.iterdir()
