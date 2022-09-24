#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   ui.py
   author      :   zhouhualin22@mails.ucas.ac.cn
   Date：      :   2022-09-17
   Description :

"""
import os
import time
import logging

import pygame

import config


class GameExitError(Exception):
    pass


class UI:
    def __init__(self, game_center=None):
        self.broad = None
        self.gc = game_center
        self.window_surface = None
        self.ui_conf = {
            "windows_size": (800, 480),
            "caption": "ui caption",

        }

        self.WHITE = (255, 255, 255)
        # display
        self.SCREEN_SIZE = (640, 480)
        self.BOARD_POS = (92, 14)
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # messages
        # self.BLACK_LAB_POS = (5, self.SCREEN_SIZE[1] / 4)
        # self.WHITE_LAB_POS = (560, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)
        self.scoreFont = pygame.font.SysFont("Serif", 20)

        # image files
        self.board_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "board233.png")).convert()
        self.black_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "black1.png")).convert()
        self.white_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "white1.png")).convert()
        self.remind_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "remind.png")).convert()
        self.delete_remind_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "cover.png")).convert()
        self.delete_remind_img1 = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "cover3.png")).convert()
        self.tip1 = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "record.jpg")).convert()
        self.tip_img = pygame.image.load(os.path.join(config.IMAGES_DIR,
                                                      "remind.png")).convert()
        # self.clear_img = pygame.image.load(os.path.join(config.IMAGES_DIR,
        #                                                 "nada.bmp")).convert()

        # self.manager = pygame_gui.UIManager(self.ui_conf['windows_size'])
        self.window_surface = pygame.display.set_mode(self.ui_conf['windows_size'])

        # self.font = pygame.font.SysFont("Times New Roman", 22)
        self.score_font = pygame.font.SysFont("Serif", 30)
        self.music = pygame.mixer.Sound(config.SOUND_DIR + "/chess_voice.wav")

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
            config.IMAGES_DIR, "board233.png"
        )).convert_alpha()
        background_img = pygame.image.load(os.path.join(
            config.IMAGES_DIR, "background.png"
        )).convert_alpha()
        IMAGE_SMALL = pygame.transform.scale(background_img, (800, 580))
        self.window_surface.blit(IMAGE_SMALL, (0, 0))
        self.window_surface.blit(board_img, self.BOARD_POS)
        self.put_piece((3, 3), config.WHITE)
        self.put_piece((4, 4), config.WHITE)
        self.put_piece((3, 4), config.BLACK)
        self.put_piece((4, 3), config.BLACK)
        self.show_score(2, 2)

    def put_remind_piece(self, pos):
        if pos is None:
            return
        img = self.remind_img
        for z in pos:
            x = z[1] * self.SQUARE_SIZE + self.BOARD[0]
            y = z[0] * self.SQUARE_SIZE + self.BOARD[1]
            self.screen.blit(img, (x, y), img.get_rect())

    def delete_put_remind_piece(self, pos):
        if pos is None:
            return
        img = self.delete_remind_img
        for z in pos:
            x = z[1] * self.SQUARE_SIZE + self.BOARD[0]
            y = z[0] * self.SQUARE_SIZE + self.BOARD[1]
            self.screen.blit(img, (x, y))

    def put_piece(self, pos, color):
        """ draws piece with given position and color """
        if pos is None:
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

    def show_winner(self, player_color):
        self.screen.fill(pygame.Color(0, 0, 0, 50))
        win_font = pygame.font.SysFont("Courier New", 34)
        restart_font = pygame.font.SysFont("Courier New", 34)
        restart_msg = "Game Over and will restart in 5s!"
        if player_color == config.WHITE:
            show_msg = "White player wins!"
        elif player_color == config.BLACK:
            show_msg = "Black player wins!"
        else:
            show_msg = "No Winner!"
        w_msg = win_font.render(show_msg, True, self.WHITE)
        r_msg = restart_font.render(restart_msg, True, self.WHITE)
        self.screen.blit(
            w_msg, w_msg.get_rect(centerx=self.screen.get_width() / 2, centery=120))
        self.screen.blit(
            r_msg, r_msg.get_rect(centerx=self.screen.get_width() / 2, centery=240))
        pygame.display.flip()

    def show_score(self, white, black):
        black_text = self.score_font.render("".format(black), True, pygame.Color("#B7B7B7"))
        white_text = self.score_font.render("".format(white), True, pygame.Color("#B7B7B7"))
        black_text_rect = black_text.get_rect()
        white_text_rect = white_text.get_rect()
        black_text_rect.topleft = (600, 40)
        white_text_rect.topleft = (600, 80)
        self.window_surface.blit(self.tip1, (565, 12))
        self.window_surface.blit(black_text, black_text_rect)
        self.window_surface.blit(white_text, white_text_rect)

        black_text = self.score_font.render("Black: {}".format(black), True, (0, 0, 0))
        white_text = self.score_font.render("White: {}".format(white), True, (255, 255, 255))
        black_text_rect = black_text.get_rect()
        white_text_rect = white_text.get_rect()
        black_text_rect.topleft = (600, 40)
        white_text_rect.topleft = (600, 80)

        self.window_surface.blit(black_text, black_text_rect)
        self.window_surface.blit(white_text, white_text_rect)

    def update_score(self, white, black):
        # print("update score {} {}".format(white, black))
        self.show_score(white, black)

    def show_MCTS_time(self, ret_time):
        mcts_time = ret_time
        time_text = self.score_font.render("".format(mcts_time), True, pygame.Color("#B7B7B7"))
        time_text_rect = time_text.get_rect()
        time_text_rect.topleft = (605, 180)
        self.window_surface.blit(self.tip1, (565, 150))
        time_text = self.score_font.render("time: {}s".format(mcts_time), True, (0, 0, 0))
        time_text_rect = time_text.get_rect()
        time_text_rect.topleft = (605, 180)
        self.window_surface.blit(time_text, time_text_rect)
        #print(mcts_time)
        #print("a")
