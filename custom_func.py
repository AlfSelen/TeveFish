import pyautogui
import keyboard
import time
from os import environ
# from PIL import ImageOps
USERNAME = environ.get('USERNAME')

def change_resolution_coord(coord, to_resolution=(1920, 1080)):
    # Standard resolution "2560x1440"
    standard_res = (2560, 1440)
    out_cord = (int(coord[0] * to_resolution[0] / standard_res[0]), int(coord[1] * to_resolution[1] / standard_res[1]))
    return out_cord

def change_resolution_region(region, to_resolution=(1920,1080)):
    standard_res = (2560, 1440)
    out_xy_from = (int(region[0] * to_resolution[0] / standard_res[0]), int(region[2] * to_resolution[1] / standard_res[1]))
    out_xy_to   = (int(region[1] * to_resolution[0] / standard_res[0]), int(region[3] * to_resolution[1] / standard_res[1]))
    out_region = (out_xy_from[0],out_xy_to[0],out_xy_from[1],out_xy_to[1])
    return out_region


def color(compare_pixel: (int, int)) -> str:
    """
    Returns color of pixel (Green/Yellow/ None)
    :param compare_pixel:
    :return:
    """

    THRESHOLD_YELLOW_UP = (255, 204, 0, 255)
    THRESHOLD_GREEN_DOWN = (0, 255, 0, 255)
    THRESHOLD = 15
    green, yellow = True, True
    for val, check_yellow, check_green in zip(compare_pixel, THRESHOLD_YELLOW_UP, THRESHOLD_GREEN_DOWN):
        if abs(val - check_yellow) > THRESHOLD:
            yellow = False
        if abs(val - check_green) > THRESHOLD:
            green = False
    if green:
        return "Green"
    if yellow:
        return "Yellow"

def color_press(pixel_color: str):
    """

    :param pixel_color:
    :return:
    """
    if pixel_color == "Yellow":
        pyautogui.press("up")
    elif pixel_color == "Green":
        pyautogui.press("down")
    time.sleep(0.05)

def capture_position():
    while True:
        x, y = pyautogui.position()
        if keyboard.is_pressed("e"):
            print(x, y)
        time.sleep(0.1)
        if keyboard.is_pressed("q"):
            break


def empty_inventory(slots, drop_off):
    for slot in slots:
        pyautogui.moveTo(slot)
        time.sleep(0.01)
        pyautogui.click(button='right')
        time.sleep(0.01)
        pyautogui.moveTo(drop_off)
        time.sleep(0.01)
        pyautogui.click()
        time.sleep(0.01)

def full_inventory(slots):
    threshold = 20
    full_inv = False
    for slot in slots:
        if
    return full_inv

def capture_hero(img) -> bool:
    extrema = img.convert("L").getextrema()
    if extrema[0] == extrema[1]:
        return True
    else:
        return False
