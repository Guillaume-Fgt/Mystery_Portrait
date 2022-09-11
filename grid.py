from PIL import Image, ImageDraw, ImageFont


def draw_grid(image: Image, step_size: int, height: int, width: int) -> None:

    draw = ImageDraw.Draw(image)

    y_start = 0
    y_end = height

    for x in range(0, width, step_size):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=128)

    x_start = 0
    x_end = width

    for y in range(0, height, step_size):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=128)


def draw_number(image: Image, grid_size_pixel: int, num: int) -> None:
    draw = ImageDraw.Draw(image)
    myfont = ImageFont.truetype("Ubuntu-Regular.ttf", grid_size_pixel - 1)
    msg = f"{num}"
    draw.text(
        (grid_size_pixel / 2, grid_size_pixel / 2),
        msg,
        fill="black",
        anchor="mm",
        font=myfont,
    )
