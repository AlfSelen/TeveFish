# Made by GoriMeri

import pyautogui
from settings import *
from time import sleep, time
from datetime import datetime
import keyboard
from custom_func import capture_hero, empty_inventory, change_resolution_coord, change_resolution_region, color, color_press, full_inventory, move_inventory
import logging
from sys import exit


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
    print("Starting in 3")
    sleep(3)

    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.info("[Started]: " + str(datetime.now()))

    # code for adding other screen resolutions support
    res_width, res_height = pyautogui.size()
    RESOLUTION = "x".join(map(str, [res_width, res_height]))
    # Map locations
    resolution_key = []
    for position in LOCATIONS["2560x1440"][:-1]:
        resolution_key.append([change_resolution_coord(position[0], tuple(map(int, RESOLUTION.split("x")))), position[1]])
    resolution_key.append(
        [change_resolution_coord(LOCATIONS["2560x1440"][-1][0], tuple(map(int, RESOLUTION.split("x")))), LOCATIONS["2560x1440"][-1][1], change_resolution_coord(LOCATIONS["2560x1440"][-1][2], tuple(map(int, RESOLUTION.split("x"))))])
    LOCATIONS[RESOLUTION] = resolution_key
    print(LOCATIONS[RESOLUTION])
    # SCAN_AREA
    SCAN_AREA = change_resolution_region(SCAN_AREA, tuple(map(int, RESOLUTION.split("x"))))
    SCAN_PIXEL_LOCATION = change_resolution_coord(SCAN_PIXEL_LOCATION, tuple(map(int, RESOLUTION.split("x"))))
    print(f"SCAN_PIXEL_LOCATION:{SCAN_PIXEL_LOCATION}")
    # HERO_PORTRAIT
    HERO_PORTRAIT = change_resolution_region(HERO_PORTRAIT, tuple(map(int, RESOLUTION.split("x"))))
    # ITEM_SLOTS
    items = []
    for item in ITEM_SLOTS:
        items.append(change_resolution_coord(item, tuple(map(int, RESOLUTION.split("x")))))
    ITEM_SLOTS = tuple(items)
    # Last 2 items slots for comparison to full inventory
    COMPARES = []
    for slot in ITEM_SLOTS[4:]:
        im = pyautogui.screenshot(region=(slot[0], slot[1], 1, 1))
        pixel = im.getpixel((0, 0))
        COMPARES.append(pixel)
    EMPTY_INVENTORY_FROM = 1
    if POSITION == 4:
        EMPTY_INVENTORY_FROM = 2
    # endregion screen resolution support

    x = 0
    Pause = False
    soft_pause = False
    scanned_text = ""
    last_fish_time = time()
    last_suicide = time()
    last_pause = time()
    inventory_full_check = time()
    inventory_emptying_timer = time()
    empty_inventory_after_fish = False

    empty_inventory(ITEM_SLOTS[EMPTY_INVENTORY_FROM:], HERO_PORTRAIT[:2])
    while True:
        if keyboard.is_pressed("shift+p"):
            Pause = False
            soft_pause = False
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
            if keyboard.is_pressed("ctrl+p"):
                soft_pause = True
            if keyboard.is_pressed("shift+q"):
                print("Quitting")
                logging.info("[Quitting]: " + str(datetime.now()))
                exit()
                break
            im = pyautogui.screenshot(region=(SCAN_PIXEL_LOCATION[0]-6, SCAN_PIXEL_LOCATION[1], 10, 1))
            greens, yellows = 0,0
            for i in range(10):
                pixel_color = color(im.getpixel((i, 0)))
                if  pixel_color == "Green":
                    greens += 1
                elif pixel_color == "Yellow":
                    yellows += 1
            im_color = ""
            if greens > 2:
                im_color = "Green"
            elif yellows > 2:
                im_color = "Yellow"
            if im_color:
                last_fish_time = time()
                color_press(im_color)

            if capture_hero(pyautogui.screenshot(region=(HERO_PORTRAIT[0], HERO_PORTRAIT[1], HERO_PORTRAIT[2], HERO_PORTRAIT[3]))):
                logging.info("Hero died: " + str(datetime.now()))
                goto_fishing_spot()

            if not empty_inventory_after_fish and not soft_pause:
                click_fish()
            elif time() - last_fish_time > 10:
                if empty_inventory_after_fish:

                    inventory_emptying_timer = time()
                    empty_inventory(ITEM_SLOTS[EMPTY_INVENTORY_FROM:4], HERO_PORTRAIT[:2])
                    move_inventory(ITEM_SLOTS[4:], ITEM_SLOTS[EMPTY_INVENTORY_FROM:EMPTY_INVENTORY_FROM + 1])
                    empty_inventory_after_fish = False
                elif soft_pause:
                    Pause = False
                    break

            if time() - inventory_emptying_timer > DROP_INVENTORY_INTERVAL * 60:
                inventory_emptying_timer = time()
                logging.info("[Timed] Clearing inventory: " + str(datetime.now()))
                empty_inventory_after_fish = True

            if time() - inventory_full_check > 30:
                inventory_full_check = time()
                if full_inventory(ITEM_SLOTS[4:], COMPARES):
                    empty_inventory_after_fish = True
                    logging.info("[Inventory Full] Clearing inventory: " + str(datetime.now()))

            if time() - last_fish_time > 60 * STUCK_INTERVAL and time() - last_suicide > 60 * STUCK_INTERVAL:
                logging.info("[Stuck] Trying suicide: " + str(datetime.now()))
                send_chat("-k")
                last_suicide = time()

            sleep(0.1)
