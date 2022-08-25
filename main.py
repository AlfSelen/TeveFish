# Made by GoriMeri

import pyautogui
from settings import *
from time import sleep, time
from datetime import datetime
import keyboard
from custom_func import im_to_text, capture_hero, empty_inventory, change_resolution_coord, change_resolution_region, color, color_press
import logging
from sys import exit
import PIL
from imagehash import average_hash

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
    last_pause = time()
    while True:
        if keyboard.is_pressed("shift+p"):
            Pause = False
            last_suicide = time()
            last_pause = time()
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
            if time() - empty_inventory_countdown > 1800 and time() - last_pause > 1800:
                empty_inventory_countdown = time()
                logging.info("Dropping inventory (because timer): " + str(datetime.now()))
                empty_inventory(ITEM_SLOTS[3:], HERO_PORTRAIT[:2])

            im = PIL.ImageGrab.grab(bbox=(SCAN_PIXEL_LOCATION[0], SCAN_PIXEL_LOCATION[1], SCAN_PIXEL_LOCATION[0]+1, SCAN_PIXEL_LOCATION[1]+1))
            im_color = color(im.getpixel((0, 0)))
            if im_color:
                last_fish_time = time()
                color_press(im_color)



            if capture_hero(HERO_PORTRAIT):
                logging.info("Hero died: " + str(datetime.now()))
                goto_fishing_spot()
            click_fish()
            sleep(0.1)

            if time() - empty_inventory_countdown > 60:
                image = pyautogui.screenshot(region=SCAN_AREA)
                text = im_to_text(image)
                if capture_instruction_from_text(text) == -1:
                    empty_inventory(ITEM_SLOTS[3:], HERO_PORTRAIT[:2])
                    empty_inventory_countdown = time()

            imagehash.average_hash(Image.open("C:/Users/laptop/PycharmProjects/TeveFish/cap5.png"))

            if time() - last_fish_time > 60 * 5 and time() - last_suicide > 60 * 5:
                logging.info("[Stuck] Trying suicide: " + str(datetime.now()))
                send_chat("-k")
                last_suicide = time()





