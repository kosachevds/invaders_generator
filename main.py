import random
import sys
import os
from collections import namedtuple
import numpy as np

from PIL import Image, ImageDraw

list_sym = []


Square = namedtuple("Square", ["top_left_x", "top_left_y", "size"])


def get_color_set(count, count_non_black):
    lower = 50
    upper = 215
    colors = np.random.randint(lower, upper, (count_non_black, 3))
    colors = [tuple(item) for item in colors]
    colors += (count - count_non_black) * [(0, 0, 0)]
    return colors


def draw_cell(border, draw, color, element, size):
    if element == int(size / 2):
        draw.rectangle(border, color)
    elif len(list_sym) == element + 1:
        draw.rectangle(border, list_sym.pop())
    else:
        list_sym.append(color)
        draw.rectangle(border, color)


def draw_sprite(border, draw, invader_width):
    cell_width = border.size / invader_width
    colors = get_color_set(6, 3)
    i = 1
    for y in range(0, invader_width):
        i *= -1
        element = 0
        for x in range(0, invader_width):
            topLeftX = x * cell_width + border.top_left_x
            topLeftY = y * cell_width + border.top_left_y
            botRightX = topLeftX + cell_width
            botRightY = topLeftY + cell_width
            draw_cell((topLeftX, topLeftY, botRightX, botRightY), draw,
                      random.choice(colors), element, invader_width)
            if element == int(invader_width / 2) or element == 0:
                i *= -1
            element += i


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
