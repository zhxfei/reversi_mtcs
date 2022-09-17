#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   test.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-15
   Description :

"""
# import pygame
# import pygame_gui
#
# FPS = 60
#
# pygame.init()
# windows_size = (800, 600)
# pygame.display.set_caption('Quick Start')
# window_surface = pygame.display.set_mode(windows_size)
#
# background = pygame.Surface(windows_size)
# background.fill(pygame.Color('#000000'))
#
# manager = pygame_gui.UIManager(windows_size)
#
# hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
#                                             text='Start',
#                                             manager=manager)
#
# clock = pygame.time.Clock()
#
# is_running = True
#
# while is_running:
#
#     # 设置执行的最长周期
#     time_delta = clock.tick(FPS) / 1000.0
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             is_running = False
#
#         if event.type == pygame_gui.UI_BUTTON_PRESSED:
#             if event.ui_element == hello_button:
#                 print('Hello World!')
#
#         manager.process_events(event)
#
#     manager.update(time_delta)
#     window_surface.blit(background, (0, 0))
#     manager.draw_ui(window_surface)
#
#     pygame.display.update()


import config

board = [[config.EMPTY] * 8 for _ in range(8)]
board[3][3] = config.WHITE
board[4][4] = config.WHITE
board[3][4] = config.BLACK
board[4][3] = config.BLACK


def counter_color(next_player):
    if next_player == config.BLACK:
        return config.WHITE
    else:
        return config.BLACK


res = []


def get_next_valid(next_player):
    other = counter_color(next_player)
    for i in range(8):
        for j in range(8):
            if board[i][j] != config.EMPTY:
                continue
            if j > 0 and board[i][j - 1] == other:
                k = j - 1
                while (k >= 0 and board[i][k] == other):
                    k -= 1
                if k >= 0 and board[i][k] == next_player:
                    res.append((i, j))
            if j < 7 and board[i][j + 1] == other:
                k = j + 1
                while (k < 7 and board[i][k] == other):
                    k += 1
                if k <= 7 and board[i][k] == next_player:
                    res.append((i, j))
            if i > 0 and board[i - 1][j] == other:
                k = i - 1
                while (k >= 0 and board[k][j] == other):
                    k -= 1
                if k >= 0 and board[k][j] == next_player:
                    res.append((i, j))
            if i < 7 and board[i + 1][j] == other:
                k = i + 1
                while (k < 7 and board[k][j] == other):
                    k += 1
                if (k <= 7 and board[k][j] == next_player):
                    res.append((i, j))
            if (i > 0 and j > 0 and board[i - 1][j - 1] == other):
                m = i - 1
                n = j - 1
                while (m >= 0 and n >= 0 and board[m][n] == other):
                    m -= 1
                    n -= 1
                if (m >= 0 and n >= 0 and board[m][n] == next_player):
                    res.append((i, j))
            if (i < 7 and j < 7 and board[i + 1][j + 1] == other):
                m = i + 1
                n = j + 1
                while (m <= 7 and n <= 7 and board[m][n] == other):
                    m += 1
                    n += 1
                if (m <= 7 and n <= 7 and board[m][n] == next_player):
                    res.append((i, j))


get_next_valid(config.BLACK)
print(res)
