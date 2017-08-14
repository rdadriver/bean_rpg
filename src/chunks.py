import pygame
import json, os

from src import constants, tiles

"""
chunks.py

This file handles the terrain chunks.

Chunks are 20x15 tile areas on the map.
Each chunk has it's unique seed, which is
saved in the save file and assigned to a location.
"""


class ChunkController:

    def __init__(self):

        # The key is a 4 digit string
        # to locate the chunk,
        # and then the value is that
        # chunks seed.
        self.map_seeds = {}
        self.map_tiles = {}
        self.chunk_pos = {}

        self.world_offset_x = 0
        self.world_offset_y = 0

        # temporary - while in dev
        self.create_chunk("0000")

    def create_chunk(self, chunk):

        # Loads a chunk from the save data

        # Open the save file
        with open(os.path.join("saves", "maps.json"), "r") as infile:
            data = json.load(infile)
            infile.close()

        self.map_seeds[chunk] = data[chunk]

        # Creates a group of tile objects
        # from the seed of the given chunk

        seed = self.map_seeds[chunk]
        new_chunk = pygame.sprite.Group()

        # Split the string into each individual tile
        tile_data = [seed[i:i+2] for i in range(0, len(seed), 2)]
        x, y = 0, 0
        for n in tile_data:

            # Create instances of the tiles
            tile = tiles.tiles[int(n)]
            new_chunk.add(tiles.Tile(tile, x, y))

            x += 1
            if x % constants.chunk_w == 0:
                x = 0
                y += 1

        # Add them to the dict of tiles
        self.map_tiles[chunk] = new_chunk

    def draw_chunk(self, chunk, display):

        # Takes a group of tile sprites
        # and draws them to the display

        chunk_to_draw = self.map_tiles[chunk]
        chunk_to_draw.draw(display)
