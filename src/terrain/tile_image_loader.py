from src.etc import spritesheet

'''
tile_image_loader.py

This file loads all of the tile images,
so they can be quickly accessed to improve performance.
'''

# Sprite sheet data
# This is where each tile can be found on terrain.png
# Simple 4 item tuples go by the form (x, y, width, height)
# and are for static, generic tiles.
# Tuples of tuples are for animated tiles, that contain all of their frames.
# Dictionaries are for template tiles, where it has the location of the template
# and then the ID of the material

generic_ground = (0, 0, 48, 48)
blue_ground = (48, 0, 48, 48)
path_1 = (0, 48, 48, 48)
path_2 = (48, 48, 48, 48)
path_3 = (96, 48, 48, 48)
path_4 = (144, 48, 48, 48)
path_5 = (192, 48, 48, 48)
path_6 = (240, 48, 48, 48)
path_7 = (288, 48, 48, 48)
path_8 = (336, 48, 48, 48)
path_9 = (0, 96, 48, 48)
path_10 = (48, 96, 48, 48)
path_11 = (96, 96, 48, 48)
path_12 = (144, 96, 48, 48)
path_13 = (192, 96, 48, 48)
path_14 = (240, 96, 48, 48)
path_15 = (288, 96, 48, 48)
dark_ground = (96, 0, 48, 48)
wall_1 = (0, 144, 48, 48)
wall_2 = (0, 192, 48, 48)
wall_3 = (48, 144, 48, 48)
wall_4 = (48, 192, 48, 48)
wall_5 = (96, 144, 48, 48)
wall_6 = (96, 192, 48, 48)
wall_7 = (144, 144, 48, 48)
wall_8 = (144, 192, 48, 48)
wall_9 = (192, 144, 48, 48)
wall_10 = (192, 192, 48, 48)
wall_11 = (240, 144, 48, 48)
wall_12 = (240, 192, 48, 48)
choc_river = (
    (384, 0, 48, 48),
    (384, 48, 48, 48),
    (384, 96, 48, 48),
    (384, 144, 48, 48),
    (432, 0, 48, 48),
    (432, 48, 48, 48),
    (432, 96, 48, 48),
    (432, 144, 48, 48)
)
tree = (288, 144, 96, 192)
shore_1 = {"template": (0, 240, 48, 48),
           "material": 0}
shore_2 = {"template": (48, 240, 48, 48),
           "material": 0}
shore_3 = {"template": (96, 240, 48, 48),
           "material": 0}
shore_4 = {"template": (144, 240, 48, 48),
           "material": 0}
shore_5 = {"template": (0, 288, 48, 48),
           "material": 0}
shore_6 = {"template": (48, 288, 48, 48),
           "material": 0}
shore_7 = {"template": (96, 288, 48, 48),
           "material": 0}
shore_8 = {"template": (144, 288, 48, 48),
           "material": 0}
bush = (384, 192, 96, 48)
grass = (480, 0, 48, 48)
ground_alt = (144, 0, 48, 48)


# Indexing this array by a tiles' ID will
# return its surface.
tiles = [generic_ground, blue_ground, path_1,
         path_2, path_3, path_4, path_5,
         path_6, path_7, path_8, path_9,
         path_10, path_11, path_12,
         path_13, path_14, path_15,
         dark_ground, wall_1, wall_2,
         wall_3, wall_4, wall_5, wall_6,
         wall_7, wall_8, wall_9, wall_10,
         wall_11, wall_12, choc_river,
         tree, shore_1, shore_2,
         shore_3, shore_4, shore_5, shore_6,
         shore_7, shore_8, bush, grass, ground_alt]
images = {}

sprite_sheet = None


# We need to call this after pygame has been initialized
def load_images():

    global sprite_sheet, images

    sprite_sheet = spritesheet.SpriteSheet("src/resources/terrain.png")

    # We need to load template tiles afterwards
    # so we don't reference yet undefined materials
    template_images = []

    for tile in tiles:

        try:
            if type(tile[0]) == int:
                # Only generic tiles have an integer as their first value
                images[tiles.index(tile)] = sprite_sheet.get_image(tile[0],
                                                                   tile[1],
                                                                   tile[2],
                                                                   tile[3])
            else:
                # The other possibility is an animated tile, where we simply repeat the loading process.
                images[tiles.index(tile)] = [sprite_sheet.get_image(frame[0],
                                                                    frame[1],
                                                                    frame[2],
                                                                    frame[3]) for frame in tile]

        # Template tiles won't work at all,
        # so we catch the error and assume it's a template tile
        except KeyError:

            template_images += [tile]

    for tile in template_images:
        # Then we load the template tiles afterwards
        images[tiles.index(tile)] = sprite_sheet.create_template_image(tile["template"],
                                                                       images[tile["material"]])
