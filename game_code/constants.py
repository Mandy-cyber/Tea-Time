from pygame.math import Vector2
from random import randint

# GENERAL
#----------------------
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800
TILESIZE = 64
IMG_SIZE = (64,64)
DROP_SIZE = (32, 32)



# AFFIRMATIONS
#----------------------
AFFIRMATIONS = [
    'affirmation one',
    'affirmation two',
    'affirmation three'
]



# SPEEDS
#----------------------
DAY_SPEED = 2
TRANSITION_SPEED = 0.5
PLAYER_SPEED = 250


# INVENTORY
#----------------------
# sidebar inventory
ITEM_PADDING = 30
x_pos = SCREEN_WIDTH - 60

SIDEBAR_POSITIONS = {
    'player_tool': (x_pos, 50),
    'glass_bottle': (x_pos, 50 + ITEM_PADDING),
    'journal': (x_pos, 50 + (ITEM_PADDING * 2)),

    'hibiscus': (x_pos, 50 + (ITEM_PADDING * 3)),
    'lavender': (x_pos, 50 + (ITEM_PADDING * 4)),
    'chamomile': (x_pos, 50 + (ITEM_PADDING * 5)),
    'basil': (x_pos, 50 + (ITEM_PADDING * 6))
}


# OFFSETS
#----------------------
ITEM_AMOUNT_OFFSET = Vector2(20, 30)

TOOL_OFFSET = {
    'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}


# OVERLAY
#----------------------
overlay_x = SCREEN_WIDTH - 25
OVERLAY_IMG_SIZE = (64, 64)
OVERLAYS = {
    'tool': (overlay_x - 30, 90),
    'herb': (overlay_x - 30, 165),
    'item': (overlay_x - 30, 250)
}


# LAYERS
#----------------------
LAYERS = {
    'water': 0,
    'earth': 1,
    'soil': 2,
    'water_patch': 3,
    'ground_rain': 4,
    'herb_plant': 5,
    'player': 6,
    'buildings': 7,
    'bush_herbs': 8,
    'rain_drops': 9 
}


# HERBS
#----------------------
GROW_SPEED = {
    'hibiscus': 0.6,
    'lavender': 0.7,
    'chamomile': 0.8,
    'basil': 1,
}

HERB_PRICES = {
    'hibiscus': 75,
    'lavender': 40,
    'chamomile': 50,
    'basil': 20,
}

# options for how many drops a herb can give
HERB_DROPS = {
    'hibiscus':  [1, 2],
    'lavender':  [1, 2, 3, 4],
    'chamomile': [1, 2, 3, 4, 5],
    'basil':     [1, 2, 3, 4, 5, 6]
}

# how much health the wild herb plants have
WILD_HERBS = {
    'HibiscusTree': 3,
    'ChamomileBush': 4,
    'LavenderBush': 4,
    'BasilBush': 5,
}

# where herbs can be placed on their plant
WILD_HERBS_POS = {
    'HibiscusTree': [(50, 30), (30, 20), (20, 10), (40, 30)],
    'ChamomileBush': [(30, 0), (30, 0), (50, 0)],
    'LavenderBush': [(10, 1), (30, 9), (50, 5)]
}



# SHOP ITEMS
#----------------------
# things you can buy from the shop
SHOP_PRICES = {
    'hibiscus': 50,
    'lavender': 30,
    'chamomile': 40,
    'basil': 20,

    'glass_bottle': 50,
    'journal': 200
}