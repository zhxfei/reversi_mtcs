#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   ui.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-17
   Description :

"""
import os
import time
import logging

import config

import pygame
import pygame_gui



class GameExitError(Exception):
    pass


class UI:
    def __init__(self, game_center=None):
        self.broad = None
        self.gc = game_center
        self.window_surface = None
        self.ui_conf = {
            "windows_size": (640, 480),
            "caption": "ui caption",

        }

        # colors
        self.BLACK = (0, 0, 0)
        self.BACKGROUND = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (128, 128, 0)

        # display
        self.SCREEN_SIZE = (640, 480)
        self.BOARD_POS = (100, 20)
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # messages
        # self.BLACK_LAB_POS = (5, self.SCREEN_SIZE[1] / 4)
        # self.WHITE_LAB_POS = (560, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)
        self.scoreFont = pygame.font.SysFont("Serif", 58)

        # image files
        self.board_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "board.bmp")).convert()
        self.black_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "preta.bmp")).convert()
        self.white_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "branca.bmp")).convert()

        self.tip_img = pygame.image.load(os.path.join(config.IMAGES_DIR,
                                                      "tip.bmp")).convert()
        # self.clear_img = pygame.image.load(os.path.join(config.IMAGES_DIR,
        #                                                 "nada.bmp")).convert()

        self.manager = pygame_gui.UIManager(self.ui_conf['windows_size'])
        self.window_surface = pygame.display.set_mode(self.ui_conf['windows_size'])

        self.prepare()

    def prepare(self):
        """
        设置背景，页面布局（分数、当前player），加载图片材料
        :return:
        """
        pygame.display.set_caption(self.ui_conf['caption'])

        # background = pygame.Surface(self.ui_conf['windows_size'])
        # background.fill(pygame.Color('#B7B7B7'))
        self.window_surface.fill(pygame.Color("#B7B7B7"))
        board_img = pygame.image.load(os.path.join(
            "./resources/images", "board.bmp"
        )).convert_alpha()

        self.window_surface.blit(board_img, self.BOARD_POS)
        self.put_piece((3, 3), config.WHITE)
        self.put_piece((4, 4), config.WHITE)
        self.put_piece((3, 4), config.BLACK)
        self.put_piece((4, 3), config.BLACK)

    def put_piece(self, pos, color):
        """ draws piece with given position and color """
        if pos == None:
            return

        # flip orientation (because xy screen orientation)
        pos = (pos[1], pos[0])

        if color == config.BLACK:
            img = self.black_img
        elif color == config.WHITE:
            img = self.white_img
        else:
            img = self.tip_img

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        pygame.display.flip()

    def get_mouse_input(self, clock):
        """ Get place clicked by mouse
        """
        while True:
            time_delta = clock.tick(config.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # click was out of board, ignores
                    if mouse_x > self.BOARD_SIZE + self.BOARD[0] or \
                            mouse_x < self.BOARD[0] or \
                            mouse_y > self.BOARD_SIZE + self.BOARD[1] or \
                            mouse_y < self.BOARD[1]:
                        continue

                    # find place
                    position = ((mouse_x - self.BOARD[0]) // self.SQUARE_SIZE), \
                               ((mouse_y - self.BOARD[1]) // self.SQUARE_SIZE)
                    # flip orientation
                    position = (position[1], position[0])
                    logging.debug("user input position:{}".format(position))
                    return position

                elif event.type == pygame.QUIT:
                    raise GameExitError
            pygame.display.update()
            time.sleep(.05)
