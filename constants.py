import os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 50

# Colors
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



IMG_DIR = "./img/"
#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 600
TILE_SIZE = 50
DEFAULT_SPEED = 3

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
        "image": os.path.join(IMG_DIR, "herb", "dreamplume.png"),
        "description": [
            "Habitat: Hidden within dusty caves.",
            "Appearance: Wispy purple petals glowing softly.",
            "Effect: Eases stress, calms Titan-induced anxiety.",
            "Use: Brew calming elixirs or sleep boosters."
        ]
    },
    {
        "name": "Bacteria",
        "image": os.path.join(IMG_DIR, "bacteria.png"),
        "description": [
            "Habitat: Clings to methane ice or cave walls.",
            "Appearance: Blue cellular blob with antennae.",
            "Effect: Digests nitrogen, produces trace oxygen.",
            "Use: Power bio-reactors or terraforming tech."
        ]
    }
]
