# Based on
# https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/

import time
import sys

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

import numpy as np
from life_board import LifeBoard
from boundary_conditions import BoundaryConditions
np.set_printoptions(threshold=sys.maxsize, linewidth=300)

# Define the simple rotor
rotor = [
    (16,16),(17,16),(18,16)
    ]

glider = [
    (10,10),(11,10),(12,10),(12,11),(11,12)
    ]

simkin_gun = [
    "OO.....OO........................",
    "OO.....OO........................",
    ".................................",
    "....OO...........................",
    "....OO...........................",
    ".................................",
    ".................................",
    ".................................",
    ".................................",
    "......................OO.OO......",
    ".....................O.....O.....",
    ".....................O......O..OO",
    ".....................OOO...O...OO",
    "..........................O......",
    ".................................",
    ".................................",
    ".................................",
    "....................OO...........",
    "....................O............",
    ".....................OOO.........",
    ".......................O........."
]


def convert_to_tuples(array_of_strings, offset_x, offset_y):
    lengths = [len(s) for s in array_of_strings]
    assert np.all(np.asarray(lengths)==lengths[0])
    tuples=[]
    for j in range(len(array_of_strings)):
        for i in range(lengths[0]):
            if array_of_strings[j][i]=='O':
                tuples.append((i+offset_x, j+offset_y))
    return tuples


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)


board = LifeBoard(disp.width, disp.height, BoundaryConditions.WRAP, BoundaryConditions.WRAP)

board.set_cells(convert_to_tuples(simkin_gun, 30, 10))
print(board.board)
print("\n-------\n")

while True:
    board.update()

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    for iy in range(height):
        for ix in range(width):
            image.putpixel((ix,iy), board.board[iy,ix])
    disp.image(image)
    disp.show()

    # time.sleep(0.01)
