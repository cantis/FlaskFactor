''' Enums used in the application '''

from enum import Enum


class ItemType(Enum):
    ''' Enum for item types '''
    MELEE = 0
    RANGED = 1
    ARMOUR = 2
    AMMUNITION = 3
    EQUIPMENT = 4
    POTION = 5
    WAND = 6
    MISC_MAGIC = 7
    TREASURE = 8
    RING = 9
    SCROLL = 10
    CONSUMABLE = 11
