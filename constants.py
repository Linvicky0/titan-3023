
import os
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
BROWN = (139, 69, 19)
PINK=(255,0,255)
GREY=(128,128,128)
GRAY = (169, 169, 169)
DEFAULT_SPEED = 3
IMG_DIR = "./img/"

BACKGROUND_DIR = "./img/background/"

HERB_DATA = [
    {
        "name": "Glowvine",
        "image": os.path.join(IMG_DIR, "herb", "Glowvine.png"),
        "description": [
            "Habitat: Grows near methane lakes in darkness.",
            "Appearance: Bioluminescent cyan tendrils.",
            "Effect: Restores visibility in Titan's long night.",
            "Use: Craft light patches to reveal or attract life."
        ]
    },
    {
        "name": "Dreamplume",
        "image": os.path.join(IMG_DIR, "herb", "Dreamplume.png"),
        "description": [
            "Habitat: Hidden within dusty caves.",
            "Appearance: Wispy purple petals glowing softly.",
            "Effect: Eases stress, calms Titan-induced anxiety.",
            "Use: Brew calming elixirs or sleep boosters."
        ]
    },
    {
        "name": "Iceburst Fern",
        "image": os.path.join(IMG_DIR, "herb", "Iceburst_Fern.png"),
        "description": [
            "Habitat: Windswept dune fields.",
            "Appearance: Spiky leaves that freeze on contact with air.",
            "Effect: Temporarily reduces body temperature in volcanic zones.",
            "Use: Ingredient for 'coolant paste', useful near cryovolcanoes."
        ]
    },
    {
        "name": "Nitrobloom",
        "image": os.path.join(IMG_DIR, "herb", "Nitrobloom.png"),
        "description": [
            "Habitat: Fertile rocky ridges, nitrogen-rich ground.",
            "Appearance: Puffy, bright-orange flowers that pulse faintly.",
            "Effect: Slight stamina boost, slows hunger.",
            "Use: Add to meals or craft biostimulants."
        ]
    },
    {
        "name": "Furnace Root",
        "image": os.path.join(IMG_DIR, "herb", "Furnace_Root.png"),
        "description": [
            "Habitat: Around cryovolcano vents.",
            "Appearance: Twisted, glowing root with red sap.",
            "Effect: Generates heat, combats hypothermia.",
            "Use: Craft thermal modules for greenhouses or suits."
        ]
    },
    {
        "name": "Resonant Moss",
        "image": os.path.join(IMG_DIR, "herb", "Resonant_Moss.png"),
        "description": [
            "Habitat: Ice cave walls and shaded valleys.",
            "Appearance: Velvet-like moss that vibrates faintly.",
            "Effect: Stores kinetic energy.",
            "Use: Essential for crafting battery packs or sonar tools."
        ]
    }
]
