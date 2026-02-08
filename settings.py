POSITION = 4
LOCATIONS = {
    "2560x1440": [
        [(614, 1408), 17],
        [(533, 1313), 36],
        [(545, 1288), 30],
        [(467, 1176), 22],
        [(390, 1395), 40, (406, 1341)]
    ]
}

SCAN_AREA = (664 - 30 - 45 + 11, 813 + 12, 889 - 664 - 50, 867 - 829)

SCAN_PIXEL_LOCATION = (609, 836)
pixel_red = (603, 841)
inventory_full = (5, 20, 55)
INVENTORY_SLOT_EMPTY = ""

HERO_PORTRAIT = (854, 1229, 951 - 854, 1296 - 1229)
ITEM_SLOTS = (1590, 1205), (1691, 1204), (1603, 1289), (1702, 1296), (1589, 1389), (1700, 1389)
FISHING_ROD = ITEM_SLOTS[0]
DROP_INVENTORY_INTERVAL = 45  # Minutes for how often hero will drop inventory
STUCK_INTERVAL = 5  # Minutes for how often hero should do -suicide if stuck and not fishing
ACTIVATE_BADFISH = False # Set to True if you have problem with problem getting killed by flying fish
BADFISH_CHANCE = 30 # Default one in 40 of presses will be wrong to stop the flying fish from spawing, only active if ACTIVATE_BADFISH is set to True 
