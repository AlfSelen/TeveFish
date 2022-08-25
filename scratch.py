
from PIL import Image, ImageGrab
import pyautogui
from imagehash import dhash, average_hash
from custom_func import change_resolution_coord, capture_position
from settings import *
from time import sleep




sleep(4)
#from settings import *


res_width, res_height = pyautogui.size()
RESOLUTION = "x".join(map(str, [res_width, res_height]))


items = []
for item in ITEM_SLOTS:
    items.append(change_resolution_coord(item, tuple(map(int,RESOLUTION.split("x")))))
ITEM_SLOTS = tuple(items)

def coord_to_region(cord, size):
    return cord[0], cord[1], cord[0] + size, cord[1] + size


hash1 = average_hash(pyautogui.screenshot(region=coord_to_region(ITEM_SLOTS[-2], 40)))
hash2 = average_hash(pyautogui.screenshot(region=coord_to_region(ITEM_SLOTS[-1], 40)))

print(coord_to_region(ITEM_SLOTS[-2], 40))
print(coord_to_region(ITEM_SLOTS[-1], 40))

print(f"Inventory 5: {hash1}\nInventory 6: {hash2}")

capture_position()


# 3000100000000000
# Inventory 6: 6000200000000000
#Inventory 5: 3000000000000000
#Inventory 6: 2000000000000000