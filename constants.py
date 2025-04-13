
import pygame

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 700
TILE_SIZE = 40

# Colors
LIGHT_GREEN=(180, 255, 180)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLUE_LIGHT=(0,255,255)
BLACK=(0,0,0)
YELLOW=(255,255,0)
ORANGE=(255,140,0)
WHITE=(255,255,255)
BROWN = (188, 143, 112)
PINK=(255,0,255)
GREY=(128,128,128)
GRAY = (169, 169, 169)
DEFAULT_SPEED = 3


IMG_DIR = "./img/"
BACKGROUND_DIR = "./img/background/"
HERB_DIR = "./img/herb/"


HERB_DATA = {
    "Glowvine":  {
        "image": f"{HERB_DIR}Glowvine.png",
        "description": [
            "Habitat: Grows near methane lakes in darkness.",
            "Appearance: Bioluminescent cyan tendrils with soft cyan glow.",
            "Effect: Restores visibility in Titan's long night.",
            "Use: Craft light patches to reveal or attract life."
        ]
    },
    "Dreamplume": {
       "image": f"{HERB_DIR}DreamPlume.png",
        "description": [
            "Habitat: Hidden within dusty caves.",
            "Appearance: Wispy purple petals glowing softly.",
            "Effect: Eases stress, calms Titan-induced anxiety.",
            "Use: Brew calming elixirs or sleep boosters."
        ]
    },
    "Iceburst Fern": {
        "image": f"{HERB_DIR}IceburstFern.png",
        "description": [
            "Habitat: Windswept dune fields.",
            "Appearance: Spiky leaves that freeze on contact with air.",
            "Effect: Temporarily reduces body temperature in volcanic zones.",
            "Use: Ingredient for 'coolant paste', useful near cryovolcanoes."
        ]
    },
    "Nitrobloom": {
        "image": f"{HERB_DIR}Nitrobloom.png",
        "description": [
            "Habitat: Fertile rocky ridges, nitrogen-rich ground.",
            "Appearance: Puffy, bright-orange flowers that pulse faintly.",
            "Effect: Slight stamina boost, slows hunger.",
            "Use: Add to meals or craft biostimulants."
        ]
    },
    "Resonant Moss": {
        "image": f"{HERB_DIR}ResonantMoss.png",
        "description": [
            "Habitat: Ice cave walls and shaded valleys.",
            "Appearance: Velvet-like moss that vibrates faintly.",
            "Effect: Stores kinetic energy.",
            "Use: Essential for crafting battery packs or sonar tools."
        ]
    }
}
