import pygame

from src.etc import constants
from src.terrain import tile_data
from src.terrain.generators import map_generator

import os, json, operator

"""
dec_generator.py

This file translates external decoration
maps into JSON format. The decoration
maps are not included in source to save
storage space, so this should never be ran
in runtime.
"""


def generate_decs(map_dir):

    files = os.listdir(map_dir)

    pix_arrays = [pygame.PixelArray(pygame.image.load(map_dir + "/" + file)) for file in files]

    for layer in pix_arrays:

        chunks_wide = tuple(map(operator.floordiv, layer.shape,
                                (constants.chunk_w, constants.chunk_h)))
        num_chunks = chunks_wide[0] * chunks_wide[1]

        chunks = []
        chunk_x, chunk_y = 0, 0
        for n in range(num_chunks):

            chunks += [[[layer[x + (chunk_x * constants.chunk_w)][y + (chunk_y * constants.chunk_h)]
                         for x in range(constants.chunk_w)]
                        for y in range(constants.chunk_h)]]

            chunk_x += 1
            if chunk_x % chunks_wide[0] == 0:
                chunk_x = 0
                chunk_y += 1

        chunks = [sum(chunk, []) for chunk in chunks]

        dec_data = {}
        chunk_x, chunk_y = 0, 0

        for chunk in chunks:

            if False in [x == 16777215 for x in chunk]:
                chunk_idx, chunk_idy = chunk_x, chunk_y
                while len(str(chunk_idx)) < 2:
                    chunk_idx = "0" + str(chunk_idx)

                while len(str(chunk_idy)) < 2:
                    chunk_idy = "0" + str(chunk_idy)

                chunk_id = chunk_idx + chunk_idy

                dec_data[chunk_id] = []

                x, y = 0, 0
                for dec in chunk:

                    if dec != 16777215:
                        print("hello", chunk_id)
                        tile_posx, tile_posy = x, y

                        while len(str(tile_posx)) < 2:
                            tile_posx = "0" + str(tile_posx)

                        while len(str(tile_posy)) < 2:
                            tile_posy = "0" + str(tile_posy)

                        pos = tile_posx + tile_posy

                        dec_data[chunk_id] += [{"pos": pos, "tileid": tile_data.tile_colors[dec]}]

                        x += 1
                        if x % 20 == 0:
                            x = 0
                            y += 1
            chunk_x += 1
            if chunk_x % chunks_wide[0] == 0:
                chunk_x = 0
                chunk_y += 1

        with open("src/saves/decs.json", "w") as outfile:
            json.dump(dec_data, outfile)
            outfile.close()


if __name__ == "__main__":

    pygame.init()

    generate_decs("D:/bean_rpg etc/decmaps")
    map_generator.generate_map("src/resources/map.png")
