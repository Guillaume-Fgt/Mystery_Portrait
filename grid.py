from PIL import Image, ImageDraw, ImageFont, ImageOps


def draw_grid(
    image: Image, step_size: int, width: int, height: int, color: str
) -> None:

    draw = ImageDraw.Draw(image)

    y_start = 0
    y_end = height

    for x in range(step_size, width + step_size, step_size):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=color)

    x_start = 0
    x_end = width

    for y in range(step_size, height + step_size, step_size):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=color)


def draw_number(image: Image, grid_size_pixel: int, num: int, color: str) -> None:
    draw = ImageDraw.Draw(image)
    myfont = ImageFont.truetype("Ubuntu-Regular.ttf", grid_size_pixel - 1)
    msg = f"{num}"
    draw.text(
        (grid_size_pixel / 2, grid_size_pixel / 2),
        msg,
        fill=color,
        anchor="mm",
        font=myfont,
    )


def add_border(image: Image, border_color: str, border_width: int) -> Image:
    border_color = border_color
    # top, right, bottom, left
    border_width = (border_width,) * 4
    image = ImageOps.expand(image, border=border_width, fill=border_color)
    return image


def dpi_mm_toPx(dpi: int, dim_grid_mm: int) -> float:
    dim_grid_inPx = (dpi * dim_grid_mm) / 25.4
    return dim_grid_inPx
