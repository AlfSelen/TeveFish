import tesserocr
import pyautogui
import keyboard
import time
from os import environ
from PIL import ImageOps
USERNAME = environ.get('USERNAME')

up_match_cases = ["up", "urei", "arro", "lol", "lot, op ", "ot an", "lei", "loin", "pank"]
down_match_cases = ["yom", "dio", "iby", "byo", "bio", "down", "dy", "wn arr", "bl on", "blond", "blom", "blowing", "oi bt", "oita", "dbi", "vwwn", "ido", "idl", "by", "iyo"]
inventory_space_match_cases = ["must", "have"]

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

def im_to_text(img):
    # tess_path = "C:/Users/alf/anaconda3/envs/fishing/share/tessdata/"
    tess_path = "C:/Users/" + USERNAME + "/anaconda3/envs/teve/share/tessdata/"

    gray = ImageOps.grayscale(img)
    text = tesserocr.image_to_text(gray, psm=7, path=tess_path).rstrip()
    return text


def capture_instruction_from_text(text: str) -> int:
    low_case = text.lower()
#    if "up" in low_case or "urei" in low_case or "arro" in low_case or "lol" in low_case or "lot" in low_case \
#            or "op " in low_case or "ot an" in low_case or "lei" in low_case:
    if any(match in low_case for match in up_match_cases):
        pyautogui.press("up")
        return 1
#    elif "yom" in low_case or "dio" in low_case or "iby" in low_case or "byo" in low_case or "bio" in low_case \
#            or "down" in low_case or "dy" in low_case or "wn arr" in low_case or "bl on" in low_case or "blond" in \
#            low_case or "blom" in low_case or "blowin" in low_case or "oi bt" in low_case or "oita" in low_case:
    elif any(match in low_case for match in down_match_cases):
        pyautogui.press("down")
        return 1
    #elif "mustaave" in low_case or "musthiave" in low_case or "musthave" in low_case or "must" in low_case or "have" \
    #        in low_case:
    elif any(match in low_case for match in inventory_space_match_cases):
        return -1
    else:
        return 0


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


def capture_hero(img) -> bool:
    extrema = img.convert("L").getextrema()
    if extrema[0] == extrema[1]:
        return True
    else:
        return False
