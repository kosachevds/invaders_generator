import os
import random
import typing

import numpy as np
from PIL import Image, ImageDraw


class Square(typing.NamedTuple):
    top_left_x: float
    top_left_y: float
    size: float


def get_color_set(count: int, count_non_black: int) -> list:
    lower = 50
    upper = 215
    colors = np.random.randint(lower, upper, (count_non_black, 3))
    colors = [tuple(item) for item in colors]
    colors += (count - count_non_black) * [(0, 0, 0)]
    return colors


def draw_cell(square: Square, draw: ImageDraw, color: tuple):
    border = (
        square.top_left_x,
        square.top_left_y,
        square.top_left_x + square.size,
        square.top_left_y + square.size)
    draw.rectangle(border, color)


def generate_sprite_cells(square, invader_width):
    cell_width = square.size / invader_width
    colors = get_color_set(6, 3)
    color_stack = []
    middle = int(invader_width / 2)
    cells = {}
    for y in range(invader_width):
        for i, x in enumerate(range(invader_width)):
            cell = Square(
                x * cell_width + square.top_left_x,
                y * cell_width + square.top_left_y,
                cell_width
            )
            color_from_stack = (i > middle or
                                i == middle and invader_width % 2 == 0)
            if color_from_stack:
                color = color_stack.pop()
            else:
                color = random.choice(colors)
                if not (i == middle):
                    color_stack.append(color)
            cells[cell] = color
    black_cell_count = sum(1 for color in cells.values() if color == (0, 0, 0))
    if black_cell_count < len(cells) / 2:
        return cells
    return generate_sprite_cells(square, invader_width)


def draw_sprite(square, draw, invader_width):
    cells = generate_sprite_cells(square, invader_width)
    for (cell, color) in cells.items():
        draw_cell(cell, draw, color)


def main(invader_width, invader_count, picture_width):
    result_image = Image.new("RGB", (picture_width, picture_width))
    draw = ImageDraw.Draw(result_image)
    invader_size = picture_width / invader_count
    padding = invader_size / invader_width
    for x in range(0, invader_count):
        for y in range(0, invader_count):
            square = Square(
                x * invader_size + padding / 2,
                y * invader_size + padding / 2,
                invader_size - padding
            )
            draw_sprite(square, draw, invader_width)
    if not os.path.exists("./Examples"):
        os.mkdir("./Examples")
    result_image.save("Examples/Example-{0}x{0}-{1}-{2}.jpg".format(
        invader_width, invader_count, picture_width))


if __name__ == "__main__":
    main(7, 5, 1900)
    # main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
