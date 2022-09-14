# 1inch=25.4mm


def mm_dpi_to_px(dpi: int, dim_mm: float) -> int:
    """take a dpi and dimension in mm and return dimension needed in pixel"""
    dim_px = (dpi * dim_mm) // 25.4
    return int(dim_px)
