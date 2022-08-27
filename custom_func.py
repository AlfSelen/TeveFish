import pyautogui
import keyboard
import time
from os import environ

USERNAME = environ.get('USERNAME')


def change_resolution_coord(coord, to_resolution=(1920, 1080)):
    # Standard resolution "2560x1440"
    standard_res = (2560, 1440)
    out_cord = (int(coord[0] * to_resolution[0] / standard_res[0]), int(coord[1] * to_resolution[1] / standard_res[1]))
    return out_cord


def change_resolution_region(region, to_resolution=(1920, 1080)):
    standard_res = (2560, 1440)
    out_xy_from = (int(region[0] * to_resolution[0] / standard_res[0]), int(region[2] * to_resolution[1] / standard_res[1]))
    out_xy_to = (int(region[1] * to_resolution[0] / standard_res[0]), int(region[3] * to_resolution[1] / standard_res[1]))
    out_region = (out_xy_from[0], out_xy_to[0], out_xy_from[1], out_xy_to[1])
    return out_region


def color(compare_pixel) -> str:
    """
    Returns color of pixel (Green/Yellow/"")
    :param compare_pixel:
    :return:
    """
    if compare_pixel[0] > 179 and 140 < compare_pixel[1] < 210 and compare_pixel[2] < 50:
        return "Yellow"
    elif compare_pixel[0] < 25 and 199 < compare_pixel[1] and compare_pixel[2] < 25:
        return "Green"
    else:
        return ""


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
        time.sleep(0.03)
        pyautogui.click(button='right')
        time.sleep(0.03)
        pyautogui.moveTo(drop_off)
        time.sleep(0.03)
        pyautogui.click()
        time.sleep(0.03)


def move_inventory(from_slots, to_slots):
    for from_slot, to_slot in zip(from_slots, to_slots):
        pyautogui.moveTo(from_slot)
        time.sleep(0.08)
        pyautogui.click(button='right')
        time.sleep(0.08)
        pyautogui.moveTo(to_slot)
        time.sleep(0.08)
        pyautogui.click()
        time.sleep(0.08)


def full_inventory(slots, compares):
    threshold = 15
    for slot, compare in zip(slots, compares):
        im = pyautogui.screenshot(region=(slot[0], slot[1], 1, 1))
        for pixel, check_px in zip(im.getpixel((0, 0)), compare):
            if abs(pixel - check_px) > threshold:
                return True
    return False


def capture_hero(img) -> bool:
    extrema = img.convert("L").getextrema()
    if extrema[0] == extrema[1]:
        return True
    else:
        return False
