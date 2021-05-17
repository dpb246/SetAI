#small script used to create all the images for the dataset
from PIL import ImageGrab
from PIL import Image

import numpy as np
import os

def crop(im, rows, cols):
    imgwidth, imgheight = im.size
    height = np.int(imgheight/rows)
    width = np.int(imgwidth/cols)

    for i in range(rows):
        for j in range(cols):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

top_left_corner = (985, 130)
bot_right_corner = (1575, 620+122)

image_count = 1
dir_path = r"C:\Users\dpb24\OneDrive - University of Waterloo\SideProjects\SetGame\Images"

rows = 5
cols = 3

if __name__== '__main__':
    while input("q to quit, enter to take photos")!="q":
        im = ImageGrab.grab([*top_left_corner, *bot_right_corner])

        path = os.path.join(dir_path, "Test.png")
        im.save(path)

        imgwidth, imgheight = im.size
        height = np.int(imgheight/rows)
        width = np.int(imgwidth/cols)
        print(f"height {height}, width {width}")

        for k, piece in enumerate(crop(im, rows, cols)):
            img = Image.new('RGB', (width, height), 255)

            img.paste(piece)
            img.thumbnail((50, 50))
            path = os.path.join(dir_path, f"Set_{image_count}.png")
            image_count += 1
            img.save(path)


