import pygame
from pygame.locals import *

from src.duel.duel_gui import load_images
from src.etc import gui_components
from src.entities import shadows

"""
duel.py

This deals with the game mechanics and GUI of duelling
"""


class DuelController:

    def __init__(self, master, player, enemy):

        self.master = master

        self.player = player.meta
        self.enemy = enemy.meta

        self.images = load_images()

        self.background = self.images["background"]

        self.attack_main_button = gui_components.Button(self.images["attack_main_button"], 508, 584)
        self.attack_alt_button = gui_components.Button(self.images["attack_alt_button"], 730, 584)
        self.item_button = gui_components.Button(self.images["item_button"], 508, 645)
        self.retreat_button = gui_components.Button(self.images["retreat_button"], 730, 645)

        self.buttons = [
            self.attack_main_button,
            self.attack_alt_button,
            self.item_button,
            self.retreat_button
        ]

        self.player_image = pygame.transform.scale(self.player.images["R"], (300, 300))
        self.enemy_image = pygame.transform.scale(self.enemy.images["L"], (230, 230))

        class PlayerShadow:
            rect = self.player_image.get_rect()
            rect.topleft = (75, 368)
            tile_code = "duel_player"

        class EnemyShadow:
            rect = self.enemy_image.get_rect()
            rect.topleft = (640, 53)
            tile_code = "duel_enemy"

        self.player_shadow = shadows.Shadow(PlayerShadow())
        self.enemy_shadow = shadows.Shadow(EnemyShadow())

    def update(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.master.game_exit = True

        [button.update() for button in self.buttons]

    def draw(self, display):

        display.blit(self.background, (0, 0))

        self.player_shadow.draw(display)
        self.enemy_shadow.draw(display)

        display.blit(self.player_image, (75, 368))
        display.blit(self.enemy_image, (640, 53))

        [button.draw(display) for button in self.buttons]