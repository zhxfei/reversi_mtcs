#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   test.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-15
   Description :

"""
import pygame
import pygame_gui

FPS = 60

pygame.init()
windows_size = (800, 600)
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(windows_size)

background = pygame.Surface(windows_size)
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager(windows_size)

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Start',
                                            manager=manager)

clock = pygame.time.Clock()

is_running = True

while is_running:

    # 设置执行的最长周期
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
