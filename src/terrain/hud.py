import pygame
from pygame.locals import *

from src.etc import gui_components, constants
from src.entities import icons

"""
hud.py

This file manages the
games heads-up display
"""


class HUD:

    def __init__(self, player, master):

        self.player = player
        self.master = master

        self.health_display = HealthDisplay(self.player, self.master)
        self.bean_select = BeanSelectPopup(self.player, self.master, 297, 452)

        self.components = [
            self.health_display
        ]

    def update(self):

        [component.update() for component in self.components]

    def open_widget(self, widget):

        self.components.append(widget)

    def close_widget(self, widget):

        self.components.remove(widget)

    def draw(self, display):

        [component.draw(display) for component in self.components]


class HealthDisplay:

    def __init__(self, player, master, x=0, y=0):

        self.player = player
        self.master = master

        self.active_bean_stat = 0

        self.x = x
        self.y = y

        self.background = gui_components.Fill(self.x, self.y, 200, 209, constants.GUI_BACKING)

        self.bean_stats = [gui_components.Fill(self.x+5, self.y+5+35*n, 190, 30, constants.GUI_FILL)
                           for n in range(len(self.player.beans))]
        self.health_bars = [gui_components.ProgressBar(self.x+9, self.y+27+36*n, 182, 5,
                                                       (constants.HEALTH_BAR_RED, constants.HEALTH_BAR_GREEN))
                            for n in range(len(self.player.beans))]
        self.bean_labels = [gui_components.Label(self.x+9, self.y+3+40*n, "{}{} Bean".format(
            self.player.beans[n].bean[0].upper(), self.player.beans[n].bean[1:]),
                                                 False, 20, constants.BLACK)
                            for n in range(len(self.player.beans))]

        self.xp_bar = gui_components.ProgressBar(self.x+9, self.y+37+34*self.active_bean_stat, 182, 5,
                                                 (constants.XP_BAR_BLUE, constants.XP_BAR_CYAN))

        self.level_label = gui_components.Label(self.x, self.y+41+35*self.active_bean_stat, "Level {}".format(
            self.player.beans[self.active_bean_stat].meta.level), False, 20, constants.BLACK)

        self.components = [self.background] + self.bean_stats + self.health_bars + self.bean_labels +\
                          [self.xp_bar, self.level_label]

    def update(self):

        for panel in self.bean_stats:
            if panel.rect.collidepoint(pygame.mouse.get_pos()):
                self.active_bean_stat = self.bean_stats.index(panel)

        self.update_components()
        self.fix_positions()

    def update_components(self):

        bean_no = 0
        for bar in self.health_bars:
            bar.update(self.player.beans[bean_no].meta.hp/self.player.beans[bean_no].meta.max_hp)

            bean_no += 1

        self.xp_bar.update(
            self.player.beans[self.active_bean_stat].meta.xp/int((constants.level_up_base *
                                                                 (constants.level_up_multiplier **
                                                                  self.player.beans[self.active_bean_stat].meta.level)))
        )

        self.level_label.update("Level {}".format(self.player.beans[self.active_bean_stat].meta.level))

    def fix_positions(self):

        panel_idx = 0
        for stat_panel in self.bean_stats:

            if panel_idx == self.active_bean_stat:
                if not stat_panel.rect.height == 60:
                    stat_panel.resize(stat_panel.rect.width, 60)

            else:
                if not stat_panel.rect.height == 30:
                    stat_panel.resize(stat_panel.rect.width, 30)
            if panel_idx == 0:
                stat_panel.rect.top = self.x+5
                self.health_bars[panel_idx].rect.top = self.x+27
                self.bean_labels[panel_idx].rect.top = self.x+3
            else:
                stat_panel.rect.top = self.bean_stats[panel_idx-1].rect.bottom + 5
                self.health_bars[panel_idx].rect.top = self.bean_stats[panel_idx-1].rect.bottom + 27
                self.bean_labels[panel_idx].rect.top = self.bean_stats[panel_idx - 1].rect.bottom + 3

            self.xp_bar.rect.top = self.y+34 + 35 * self.active_bean_stat

            self.level_label.rect.top = self.y+41 + 35 * self.active_bean_stat
            self.level_label.rect.right = self.background.rect.right - 7

            panel_idx += 1

    def draw(self, display):

        [component.draw(display) for component in self.components]


class BeanSelectPopup:

    def __init__(self, player, master, x, y):

        self.player = player
        self.master = master

        self.x = x
        self.y = y

        self.selected_option = 0

        self.background = gui_components.Fill(self.x, self.y, 366, 176, constants.GUI_BACKING)
        self.background_fill = gui_components.Fill(self.x+5, self.y+5, 356, 166, constants.GUI_FILL)

        self.title = [
            gui_components.Label(self.x+9, self.y+3, "You have been challenged to fight!", False, 20, constants.BLACK),
            gui_components.Label(self.x+9, self.y+21, "Which bean accepts the challenge?", False, 20, constants.BLACK)
        ]

        self.options = [gui_components.Label(self.x+35, self.y+39+18*n, "{}{} Bean".format(
            self.player.beans[n].bean[0].upper(), self.player.beans[n].bean[1:]),
                                             False, 20, constants.BLACK) for n in range(len(self.player.beans))]
        self.options.append(gui_components.Label(self.x+35, self.y+39+18*len(self.options), "I decline the challenge",
                                                 False, 20, constants.BLACK))

        self.space_label = gui_components.Label(self.background.rect.centerx, self.y+159, "<Space to Select>",
                                                True, 20, (79, 80, 68))

        self.arrow = icons.ArrowPointer(self.x+23, self.y+44+18*self.selected_option)

        self.components = [
            self.background,
            self.background_fill,
            self.space_label,
            self.arrow
        ] + self.title + self.options

    def update(self):

        self.arrow.realign(self.x+23, self.y+44+18*self.selected_option)

    def handle_event(self, e):

        if e.type == KEYUP:

            if e.key in (K_UP, K_w):
                self.selected_option = (self.selected_option-1) % 6

            elif e.key in (K_DOWN, K_s):
                self.selected_option = (self.selected_option+1) % 6

    def draw(self, display):

        [component.draw(display) for component in self.components]
