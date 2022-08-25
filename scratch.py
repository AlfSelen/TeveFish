
from PIL import Image, ImageGrab
import pyautogui
from imagehash import average_hash
from custom_func import  change_resolution_coord
from settings import *






#from settings import *


res_width, res_height = pyautogui.size()
RESOLUTION = "x".join(map(str, [res_width, res_height]))


items = []
for item in ITEM_SLOTS:
    items.append(change_resolution_coord(item, tuple(map(int,RESOLUTION.split("x")))))
ITEM_SLOTS = tuple(items)

hash1 = average_hash(pyautogui.screenshot(region=ITEM_SLOTS[-2]))
hash2 = average_hash(pyautogui.screenshot(region=ITEM_SLOTS[-1]))

print(f"Inventory 5: {hash1}\nInventory 6: {hash2}")
