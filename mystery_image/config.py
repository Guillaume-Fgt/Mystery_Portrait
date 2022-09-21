from dataclasses import dataclass
import json


@dataclass
class ImageConfig:
    width_mm: float
    height_mm: float
    dpi: int
    image_path: str
    grid_size_mm: float
    grid_color: str
    num_color: str
    bw_threshold: int
    border_color: str
    border_thickness: int
    solution: bool


def load_config(config_file: str) -> ImageConfig:
    with open(config_file, "r") as f:
        data = json.load(f)
        return ImageConfig(**data)
