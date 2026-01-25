# Made by GoriMeri

import pyautogui
from mss import mss
import numpy as np
from settings import (
    POSITION,
    LOCATIONS,
    SCAN_AREA,
    SCAN_PIXEL_LOCATION,
    HERO_PORTRAIT,
    STUCK_INTERVAL,
    DROP_INVENTORY_INTERVAL,
    ITEM_SLOTS,
)
from time import sleep, time
from datetime import datetime
from pynput import keyboard
from threading import Lock
from custom_func import (
    capture_hero,
    empty_inventory,
    change_resolution_coord,
    change_resolution_region,
    color_np,
    color_press,
    full_inventory,
    move_inventory,
)
import logging

running = True
paused = False


def on_press(key):
    global running
    global paused

    try:
        # check if Shift is held and a character key is pressed
        if key.char.lower() == "q" and keyboard.Key.shift in current_keys:
            running = False
            paused = False
            print("Shift + Q pressed → exiting program")

        if key.char.lower() == "p" and keyboard.Key.shift in current_keys:
            paused = not paused
            print(f"Shift + P pressed → running set to {paused}")

    except AttributeError:
        pass


def on_release(key):
    # remove key from the set when released
    current_keys.discard(key)


def on_press_wrapper(key):
    current_keys.add(key)
    on_press(key)


class KeyState:
    def __init__(self):
        self.pressed_keys = set()
        self.lock = Lock()
        self.listener = None

    def on_press(self, key):
        with self.lock:
            try:
                if hasattr(key, "char") and key.char:
                    self.pressed_keys.add(key.char)
                else:
                    self.pressed_keys.add(key.name)
            except AttributeError:
                self.pressed_keys.add(str(key))

    def on_release(self, key):
        with self.lock:
            try:
                if hasattr(key, "char") and key.char:
                    self.pressed_keys.discard(key.char)
                else:
                    self.pressed_keys.discard(key.name)
            except AttributeError:
                self.pressed_keys.discard(str(key))

    def is_pressed(self, key_combo):
        with self.lock:
            if "+" in key_combo:
                parts = key_combo.lower().split("+")
                return all(part in self.pressed_keys for part in parts)
            else:
                return key_combo.lower() in self.pressed_keys

    def start_listener(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()


# Initialize key state tracker
# key_state = KeyState()
key_controller = keyboard.Controller()

# track currently pressed keys
current_keys = set()


def get_screen_position(coord, main_display):
    """Transform coordinate to current resolution and monitor position"""
    # scaled = change_resolution_coord(coord, tuple(map(int, widthXheigth.split("x"))))
    # x, y = map(int, widthXheigth.split("x"))
    return (coord[0] + main_display["left"], coord[1] + main_display["top"])


def goto_fishing_spot(main_display):
    print("Detected dead hero: Will wait for 15 and go back")
    sleep(15)
    key_controller.press("1")
    sleep(0.2)
    if POSITION == 4:
        right_click_pos = get_screen_position(
            LOCATIONS[widthXheigth][POSITION][2], main_display
        )
        pyautogui.moveTo(right_click_pos)
        sleep(0.05)
        pyautogui.click()
        sleep(0.05)
        pyautogui.click(button="right")
        key_controller.press(keyboard.Key.shift)
        sleep(0.05)
    main_pos = get_screen_position(LOCATIONS[widthXheigth][POSITION][0], main_display)
    pyautogui.moveTo(main_pos)
    sleep(0.05)
    pyautogui.click()
    sleep(0.1)
    pyautogui.click(button="right")
    sleep(0.1)
    key_controller.release(keyboard.Key.shift)
    sleep(LOCATIONS[widthXheigth][POSITION][1])


def click_fish(main_display):
    fish_slot_pos = get_screen_position(ITEM_SLOTS[0], main_display)
    pyautogui.moveTo(fish_slot_pos)
    pyautogui.click()


def send_chat(text: str):
    key_controller.tap("enter")
    sleep(0.02)
    key_controller.type(text)
    sleep(0.02)
    key_controller.tap("enter")
    sleep(0.02)


def setup_logger():
    logger = logging.getLogger("fishing_bot")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("example.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False
    return logger


def select_monitor(sct) -> dict:
    """returns {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}"""
    print("Available monitors:")
    for i, m in enumerate(sct.monitors[1:], start=1):
        print(f"{i}: {m['width']}x{m['height']} at ({m['left']}, {m['top']})")

    if len(sct.monitors[1:]) > 1:
        monitor_index = int(input("Select monitor (number): "))
    else:
        monitor_index = 1
    monitor = sct.monitors[monitor_index]
    return monitor


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press_wrapper, on_release=on_release)
    listener.start()  # <-- non-blocking
    sct = mss()
    main_display = select_monitor(sct)
    print("Starting in 3")
    sleep(3)

    # logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    # logging.info("[Started]: " + str(datetime.now()))
    logger = setup_logger()

    # code for adding other screen resolutions support
    # res_width, res_height = 1920, 1080
    widthXheigth = f"{main_display['width']}x{main_display['height']}"
    # widthXheigth = "x".join(map(str, [res_width, res_height]))
    # Map locations
    resolution_key = []
    for position in LOCATIONS["2560x1440"][:-1]:
        resolution_key.append(
            [
                change_resolution_coord(
                    position[0], tuple(map(int, widthXheigth.split("x")))
                ),
                position[1],
            ]
        )
    resolution_key.append(
        [
            change_resolution_coord(
                LOCATIONS["2560x1440"][-1][0], tuple(map(int, widthXheigth.split("x")))
            ),
            LOCATIONS["2560x1440"][-1][1],
            change_resolution_coord(
                LOCATIONS["2560x1440"][-1][2], tuple(map(int, widthXheigth.split("x")))
            ),
        ]
    )
    LOCATIONS[widthXheigth] = resolution_key
    # SCAN_AREA
    SCAN_AREA = change_resolution_region(
        SCAN_AREA, tuple(map(int, widthXheigth.split("x")))
    )
    SCAN_PIXEL_LOCATION = change_resolution_coord(
        SCAN_PIXEL_LOCATION, tuple(map(int, widthXheigth.split("x")))
    )
    print(f"SCAN_PIXEL_LOCATION:{SCAN_PIXEL_LOCATION}")
    # HERO_PORTRAIT
    HERO_PORTRAIT = change_resolution_region(
        HERO_PORTRAIT, tuple(map(int, widthXheigth.split("x")))
    )
    # ITEM_SLOTS
    items = []
    for item in ITEM_SLOTS:
        items.append(
            change_resolution_coord(item, tuple(map(int, widthXheigth.split("x"))))
        )
    ITEM_SLOTS = tuple(items)
    # Last 2 items slots for comparison to full inventory
    COMPARES = []
    for slot in ITEM_SLOTS[4:]:
        im = pyautogui.screenshot(
            region=(slot[0] + main_display["left"], slot[1] + main_display["top"], 1, 1)
        )
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

    # Start keyboard listener
    # key_state.start_listener()

    last_fish_time = time()
    # Transform inventory coordinates before calling functions
    transformed_item_slots = [
        get_screen_position(slot, main_display) for slot in ITEM_SLOTS
    ]
    transformed_hero_portrait_pos = get_screen_position(HERO_PORTRAIT[:2], main_display)
    empty_inventory(
        transformed_item_slots[EMPTY_INVENTORY_FROM:], transformed_hero_portrait_pos
    )
    try:
        iteration = time()
        while running:
            while paused:
                sleep(0.5)
            print(
                f"\rFPS: {1 / (max(time() - iteration, 0.000001))}", end="", flush=True
            )
            iteration = time()
            monitor = {
                "left": SCAN_PIXEL_LOCATION[0] - 6 + main_display["left"],
                "top": SCAN_PIXEL_LOCATION[1] + main_display["top"],
                "width": 10,
                "height": 1,
            }
            im = np.array(sct.grab(monitor))
            # im = pyautogui.screenshot(
            #     region=(SCAN_PIXEL_LOCATION[0] - 6, SCAN_PIXEL_LOCATION[1], 10, 1)
            # )
            greens, yellows = 0, 0
            for i in range(10):
                pixel_color = color_np(im[0, i])
                if pixel_color == "Green":
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
                logger.debug(f"Pressing: {im_color}Gr/Yl: {greens}/{yellows}")
                continue

            if time() - last_fish_time > 20 and capture_hero(
                pyautogui.screenshot(
                    region=(
                        HERO_PORTRAIT[0] + main_display["left"],
                        HERO_PORTRAIT[1] + main_display["top"],
                        HERO_PORTRAIT[2],
                        HERO_PORTRAIT[3],
                    )
                )
            ):
                logger.info("Hero died: " + str(datetime.now()))
                goto_fishing_spot(main_display)
                continue

            if not empty_inventory_after_fish and not soft_pause:
                if time() - last_fish_time > 3.5:
                    # Jumpt to fish again
                    click_fish(main_display)
            elif time() - last_fish_time > 10:
                if empty_inventory_after_fish:
                    inventory_emptying_timer = time()
                    # Transform inventory coordinates before calling functions
                    transformed_item_slots = [
                        get_screen_position(slot, main_display) for slot in ITEM_SLOTS
                    ]
                    transformed_hero_portrait_pos = get_screen_position(
                        HERO_PORTRAIT[:2], main_display
                    )
                    empty_inventory(
                        transformed_item_slots[EMPTY_INVENTORY_FROM:4],
                        transformed_hero_portrait_pos,
                    )
                    move_inventory(
                        transformed_item_slots[4:],
                        transformed_item_slots[
                            EMPTY_INVENTORY_FROM : EMPTY_INVENTORY_FROM + 1
                        ],
                    )
                    empty_inventory_after_fish = False
                elif soft_pause:
                    Pause = False
                    break

            if time() - inventory_emptying_timer > DROP_INVENTORY_INTERVAL * 60:
                inventory_emptying_timer = time()
                logger.info("[Timed] Clearing inventory: " + str(datetime.now()))
                empty_inventory_after_fish = True
                continue

            if time() - inventory_full_check > 60:
                inventory_full_check = time()
                if full_inventory(ITEM_SLOTS[4:], COMPARES):
                    empty_inventory_after_fish = True
                    inventory_emptying_timer = time()
                    logger.info(
                        "[Inventory Full] Clearing inventory: " + str(datetime.now())
                    )

            if (
                time() - last_fish_time > 60 * STUCK_INTERVAL
                and time() - last_suicide > 60 * STUCK_INTERVAL
            ):
                logger.info("[Stuck] Trying suicide: " + str(datetime.now()))
                send_chat("-k")
                last_suicide = time()

            sleep(0.1)
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        listener.stop()
