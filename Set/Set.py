#Runs through the game once when enter is pressed in console, until q is submitted
#Currently configured for darkmode 1440p screen, future improvements include testing for other screen resolutions

from PIL import ImageGrab
from PIL import Image

import tensorflow as tf

from Card import Card, COLOUR, SHADING, SHAPE, check_set

import numpy as np
import random

from tensorflow import keras

import win32api, win32con
import time, math

#seperates the screen shot into the 15 images
def crop(im, rows, cols):
    imgwidth, imgheight = im.size
    height = np.int(imgheight/rows)
    width = np.int(imgwidth/cols)

    for i in range(rows):
        for j in range(cols):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

#returns card object from string given by classifier 
def get_card(str):
    if str == 'NoCard': return None

    arr = str.split('-')
    
    colour_lookup = {'green':COLOUR.GREEN, 'orange':COLOUR.ORANGE, 'pink':COLOUR.PINK}
    shape_lookup = {'diamond':SHAPE.DIAMOND, 'squiggle':SHAPE.SQUIGGLE, 'oval':SHAPE.OVAL}
    shading_lookup = {'filled':SHADING.SOLID, 'outline':SHADING.OUTLINED, 'shaded':SHADING.STRIPED}

    return Card(colour_lookup[arr[0]], shape_lookup[arr[2]], shading_lookup[arr[3]], int(arr[1]))

def click(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


img_height = 31
img_width = 50

class_names = ['NoCard', 'green-1-diamond-filled', 'green-1-diamond-outline', 'green-1-diamond-shaded', 'green-1-oval-filled', 'green-1-oval-outline', 'green-1-oval-shaded', 'green-1-squiggle-filled', 'green-1-squiggle-outline', 'green-1-squiggle-shaded', 'green-2-diamond-filled', 'green-2-diamond-outline', 'green-2-diamond-shaded', 'green-2-oval-filled', 'green-2-oval-outline', 'green-2-oval-shaded', 'green-2-squiggle-filled', 'green-2-squiggle-outline', 'green-2-squiggle-shaded', 'green-3-diamond-filled', 'green-3-diamond-outline', 'green-3-diamond-shaded', 'green-3-oval-filled', 'green-3-oval-outline', 'green-3-oval-shaded', 'green-3-squiggle-filled', 'green-3-squiggle-outline', 'green-3-squiggle-shaded', 'orange-1-diamond-filled', 'orange-1-diamond-outline', 'orange-1-diamond-shaded', 'orange-1-oval-filled', 'orange-1-oval-outline', 'orange-1-oval-shaded', 'orange-1-squiggle-filled', 'orange-1-squiggle-outline', 'orange-1-squiggle-shaded', 'orange-2-diamond-filled', 'orange-2-diamond-outline', 'orange-2-diamond-shaded', 'orange-2-oval-filled', 'orange-2-oval-outline', 'orange-2-oval-shaded', 'orange-2-squiggle-filled', 'orange-2-squiggle-outline', 'orange-2-squiggle-shaded', 'orange-3-diamond-filled', 'orange-3-diamond-outline', 'orange-3-diamond-shaded', 'orange-3-oval-filled', 'orange-3-oval-outline', 'orange-3-oval-shaded', 'orange-3-squiggle-filled', 'orange-3-squiggle-outline', 'orange-3-squiggle-shaded', 'pink-1-diamond-filled', 'pink-1-diamond-outline', 'pink-1-diamond-shaded', 'pink-1-oval-filled', 'pink-1-oval-outline', 'pink-1-oval-shaded', 'pink-1-squiggle-filled', 'pink-1-squiggle-outline', 'pink-1-squiggle-shaded', 'pink-2-diamond-filled', 'pink-2-diamond-outline', 'pink-2-diamond-shaded', 'pink-2-oval-filled', 'pink-2-oval-outline', 'pink-2-oval-shaded', 'pink-2-squiggle-filled', 'pink-2-squiggle-outline', 'pink-2-squiggle-shaded', 'pink-3-diamond-filled', 'pink-3-diamond-outline', 'pink-3-diamond-shaded', 'pink-3-oval-filled', 'pink-3-oval-outline', 'pink-3-oval-shaded', 'pink-3-squiggle-filled', 'pink-3-squiggle-outline', 'pink-3-squiggle-shaded']

model = keras.models.load_model('DarkModeSet-1.2')

if __name__ == "__main__":
    top_left_corner = (985, 130)
    bot_right_corner = (1575, 620+122)
    rows = 5
    cols = 3

    while input("q to quit, enter to take photos")!="q":
        im = ImageGrab.grab([*top_left_corner, *bot_right_corner])

        imgwidth, imgheight = im.size
        height = np.int(imgheight/rows)
        width = np.int(imgwidth/cols)
        print(f"height {height}, width {width}")

        #first identify all the sets
        visible_cards = []

        for k, piece in enumerate(crop(im, rows, cols)):
            img = Image.new('RGB', (width, height), 255)

            img.paste(piece)
            img.thumbnail((50, 50))

            img_array = tf.expand_dims(keras.preprocessing.image.img_to_array(img), 0)

            test_res = tf.nn.softmax(model.predict(img_array))
            best_guess = class_names[np.argmax(test_res)]

            print(k, best_guess)

            card = get_card(best_guess)
            if card: visible_cards.append(card)

        #now have list of cards, try to find all the sets
        valid_sets = []

        for i in range(len(visible_cards)):
            for ii in range(i+1, len(visible_cards)):
                for iii in range(ii+1, len(visible_cards)):
                    if check_set(visible_cards[i], visible_cards[ii], visible_cards[iii]):
                        valid_sets.append((i, ii, iii))
        
        print(valid_sets)

        if len(valid_sets) == 0:
            print("bad card or something")
            continue

        selected_set = random.choice(valid_sets)

        print(selected_set)

        #actually click the code
        for key in selected_set:
            pos = [int(top_left_corner[0]+width*(key%cols)+width/2), 
                   int(top_left_corner[1]+height*math.floor(key/cols)+height/2)]

            print(pos, key, key%cols, math.floor(key/cols))
            click(pos)
            time.sleep(0.01)
