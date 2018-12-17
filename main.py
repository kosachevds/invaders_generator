import random
import sys
import os
from collections import namedtuple
import numpy as np

from PIL import Image, ImageDraw

Square = namedtuple("Square", ["top_left_x", "top_left_y", "size"])


def get_color_set(count, count_non_black):
    lower = 50
    upper = 215
    colors = np.random.randint(lower, upper, (count_non_black, 3))
    colors = [tuple(item) for item in colors]
    colors += (count - count_non_black) * [(0, 0, 0)]
    return colors


def draw_cell(square, draw, color):
    border = (
        square.top_left_x,
        square.top_left_y,
        square.top_left_x + square.size,
        square.top_left_y + square.size)
    draw.rectangle(border, color)


def draw_sprite(border, draw, invader_width):
    cell_width = border.size / invader_width
    colors = get_color_set(6, 3)
    color_stack = []
    middle = int(invader_width / 2)
    # cells = []
    # TODO: count black cells and regenerate esli ih mnogo
    for y in range(invader_width):
        for i, x in enumerate(range(invader_width)):
            square = Square(
                x * cell_width + border.top_left_x,
                y * cell_width + border.top_left_y,
                cell_width
            )
            if i <= middle:
                color = random.choice(colors)
                if i != middle:
                    color_stack.append(color)
            else:
                color = color_stack.pop()
            draw_cell(square, draw, color)


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
    main(5, 5, 1900)
    # main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
