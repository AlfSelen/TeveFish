# Made by GoriMeri

import pyautogui
from settings import *
from time import sleep, time
from datetime import datetime
import keyboard
from custom_func import im_to_text, capture_instruction_from_text, capture_hero, empty_inventory, change_resolution_coord, change_resolution_region, color, color_press
import logging
from sys import exit
import PIL


def goto_fishing_spot():
    print("Detected dead hero: Will wait for 15 and go back")
    sleep(15)
    keyboard.press("1")
    sleep(0.2)
    if POSITION == 4:
        pyautogui.moveTo((LOCATIONS[RESOLUTION][POSITION][2]))
        sleep(0.05)
        pyautogui.click()
        sleep(0.05)
        pyautogui.click(button='right')
        keyboard.press('shift')
        sleep(0.05)
    pyautogui.moveTo((LOCATIONS[RESOLUTION][POSITION][0]))
    sleep(0.05)
    pyautogui.click()
    sleep(0.1)
    pyautogui.click(button='right')
    sleep(0.1)
    keyboard.release('shift')
    sleep(LOCATIONS[RESOLUTION][POSITION][1])


def click_fish():
    pyautogui.moveTo(ITEM_SLOTS[0])
    pyautogui.click()


def capture_instruction(x=0):
    # try:
    im = pyautogui.screenshot(region=SCAN_AREA)
    # im.save(str(x) + '.png')
    # img = np.array(im)
    text = im_to_text(im)

    # color_values = img_color_text_anly(img)
    down, up = 0, 0
    for i, color in enumerate(color_values):
        if UP[i][0] <= color <= UP[i][1]:
            up += 1
        if DOWN[i][0] <= color <= DOWN[i][1]:
            down += 1
    if up == 3:
        pyautogui.press("up")
        return True
    elif down == 3:
        pyautogui.press("down")
        return True
    else:
        return False


def img_color_text_anly(img):
    # img = cv2.imread(path)  # Read input image

    h_red = cv2.calcHist([img], [2], None, [256], [0, 256])
    h_green = cv2.calcHist([img], [1], None, [256], [0, 256])
    h_blue = cv2.calcHist([img], [0], None, [256], [0, 256])

    # h_red.sum() must be img.shape[0]*img.shape[1]

    # Remove background pixels from the histograms.
    # Set histogram bins above 230 with zero
    # assume all text has lower values of red, green and blue.
    h_red[230:] = 0
    h_green[230:] = 0
    h_blue[230:] = 0

    # Compute number of elements in histogram, after removing background
    count_red = h_red.sum()
    count_green = h_green.sum()
    count_blue = h_blue.sum()

    # Compute the sum of pixels in the original image according to histogram.
    # Example:
    # If h[100] = 10
    # Then there are 10 pixels with value 100 in the image.
    # The sum of the 10 pixels is 100*10.
    # The sum of an pixels in the original image is: h[0]*0 + h[1]*1 + h[2]*2...
    sum_red = np.sum(h_red * np.c_[0:256])
    sum_green = np.sum(h_green * np.c_[0:256])
    sum_blue = np.sum(h_blue * np.c_[0:256])

    # Compute the average - divide sum by count.
    avg_red = sum_red / count_red
    avg_green = sum_green / count_green
    avg_blue = sum_blue / count_blue
    return avg_red, avg_green, avg_blue
    # print('Text RGB average is about: {}, {}, {}'.format(avg_red, avg_green, avg_blue))


def send_chat(text: str):
    keyboard.send("enter")
    sleep(0.02)
    keyboard.write(text)
    sleep(0.02)
    keyboard.send("enter")
    sleep(0.02)


if __name__ == '__main__':
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.info("[Started]: " + str(datetime.now()))
    empty_inventory_countdown = time()

    # code for adding other screen resolutions support
    res_width, res_height = pyautogui.size()
    RESOLUTION = "x".join(map(str,[res_width,res_height]))
    # Map locations
    resolution_key = []
    for position in LOCATIONS["2560x1440"][:-1]:
        resolution_key.append([change_resolution_coord(position[0],tuple(map(int,RESOLUTION.split("x")))), position[1]])
    resolution_key.append(
        [change_resolution_coord(LOCATIONS["2560x1440"][-1][0],tuple(map(int,RESOLUTION.split("x")))), LOCATIONS["2560x1440"][-1][1], change_resolution_coord(LOCATIONS["2560x1440"][-1][2],tuple(map(int,RESOLUTION.split("x"))))])
    LOCATIONS[RESOLUTION] = resolution_key
    print(LOCATIONS[RESOLUTION])
    # SCAN_AREA
    SCAN_AREA = change_resolution_region(SCAN_AREA, tuple(map(int,RESOLUTION.split("x"))))
    SCAN_PIXEL_LOCATION = change_resolution_coord(SCAN_PIXEL_LOCATION, tuple(map(int,RESOLUTION.split("x"))))
    # HERO_PORTRAIT
    HERO_PORTRAIT = change_resolution_region(HERO_PORTRAIT, tuple(map(int,RESOLUTION.split("x"))))
    #ITEM_SLOTS
    items = []
    for item in ITEM_SLOTS:
        items.append(change_resolution_coord(item, tuple(map(int,RESOLUTION.split("x")))))
    ITEM_SLOTS = tuple(items)
    # endregion screen resolution support

    print("Starting in 3")
    sleep(3)
    x = 0
    Pause = False
    scanned_text = ""
    last_fish_time = time()
    last_suicide = time()
    while True:
        if keyboard.is_pressed("shift+p"):
            Pause = False
            last_suicide = time()
            sleep(1)
        elif keyboard.is_pressed("shift+q"):
            break
        else:
            sleep(0.2)
        while not Pause:
            if keyboard.is_pressed("shift+p"):
                Pause = True
                sleep(1)
                break
            if keyboard.is_pressed("shift+q"):
                print("Quitting")
                logging.info("[Quitting]: " + str(datetime.now()))
                exit()
                break
            if time() - empty_inventory_countdown > 1800:
                empty_inventory_countdown = time()
                logging.info("Dropping inventory (because timer): " + str(datetime.now()))
                empty_inventory(ITEM_SLOTS[3:], HERO_PORTRAIT[:2])

            fish_time = time()
            #image = pyautogui.screenshot(region=SCAN_AREA)
            #text = im_to_text(image)
            #is_fishing = capture_instruction_from_text(text)
            im = PIL.ImageGrab.grab(bbox=(SCAN_PIXEL_LOCATION[0], SCAN_PIXEL_LOCATION[1], SCAN_PIXEL_LOCATION[0]+1, SCAN_PIXEL_LOCATION[1]+1))
            im_color = color(im.getpixel((0, 0)))
            is_fishing = 0
            if is_fishing == 1:
                fishing_presses = 0
                print("starting fishing routine")
                last_fish_time = time()
                while time() - fish_time < 5 and fishing_presses < 20 and False:
                    if keyboard.is_pressed("shift+p"):
                        Pause = True
                        sleep(5)
                        break
                    if keyboard.is_pressed("shift+q"):
                        print("Quitting")
                        logging.info("[Quitting]: " + str(datetime.now()))
                        exit()
                        break
                    #image = pyautogui.screenshot(region=SCAN_AREA)
                    #text = im_to_text(image)
                    #fishpress = capture_instruction_from_text(text)
                    #if fishpress == 1:
                    #    fishing_presses += 1
                    #if scanned_text != text:
                    #    print(f"{text}")
                    #    scanned_text = text

            elif is_fishing == 0:
                #image = pyautogui.screenshot(region=SCAN_AREA)
                hero_portrait = pyautogui.screenshot(region=HERO_PORTRAIT)
                #text = im_to_text(image)
                #capture_instruction_from_text(text)
                im = PIL.ImageGrab.grab(bbox=(SCAN_PIXEL_LOCATION[0], SCAN_PIXEL_LOCATION[1], SCAN_PIXEL_LOCATION[0]+1, SCAN_PIXEL_LOCATION[1]+1))
                im_color = color(im.getpixel((0, 0)))
                color_press(im_color)
                if im_color:
                    last_fish_time = time()
                click_fish()

                sleep(0.1)
                if capture_hero(hero_portrait):
                    logging.info("Hero died: " + str(datetime.now()))
                    goto_fishing_spot()
            else:
                logging.info("[Full inventory] Dropping inventory (Inventory full): " + str(datetime.now()))
                empty_inventory(ITEM_SLOTS[3:], HERO_PORTRAIT[:2])
                empty_inventory_countdown = time()
            if Pause:
                break

            #if scanned_text != text:
            #    print(f"{text}")
            #    scanned_text = text

            if time() - empty_inventory_countdown > 60:
                image = pyautogui.screenshot(region=SCAN_AREA)
                text = im_to_text(image)
                if capture_instruction_from_text(text) == -1:
                    empty_inventory(ITEM_SLOTS[3:], HERO_PORTRAIT[:2])
                    empty_inventory_countdown = time()


            if time() - last_fish_time > 60 * 5 and time() - last_suicide > 60 * 5:
                logging.info("[Stuck] Trying suicide: " + str(datetime.now()))
                send_chat("-k")
                last_suicide = time()


