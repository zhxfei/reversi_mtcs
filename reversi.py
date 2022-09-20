#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   reversi.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-14
   Description :

"""
import time

import config
from ui import UI
from board import Board
from player import RandomPlayer, HumanPlayer, StepIllegalError

import pygame


class GameOverException(Exception):
    pass


class GameCenter:
    def __init__(self):
        pygame.init()
        self.ui = UI(game_center=self)
        self.board = Board(game_center=self)

        # 初始化玩家
        self.player_black = HumanPlayer(self.board, self)
        self.player_white = RandomPlayer(self.board, self)
        self.mode = "human_player"

        self.gm_is_running = True
        self.board.cur_player = config.BLACK

    def start_loop(self):
        """

        :return:
        """
        clock = pygame.time.Clock()
        winner = None
        while self.gm_is_running and not self.board.game_ended():
            clock.tick(config.FPS)
            time.sleep(0.05)
            if len(self.board.next_valid_steps) == 0:
                self.board.switch_player()
            try:
                if self.board.cur_player == config.BLACK:
                    # if self.mode == "human_player":
                    self.player_black.move(clock)
                    self.board.switch_player()
                else:
                    self.player_white.move()
                    self.board.switch_player()
            except StepIllegalError:
                print("illegal step")
                # todo: 调试
                # break

            # 更新黑白棋统计
            whites, blacks, _ = self.board.count_pieces()
            self.ui.update_score(whites, blacks)

        # game is not running...
        if self.board.game_ended():
            whites, blacks, empty = self.board.count_pieces()
            if whites > blacks:
                winner = config.WHITE
            elif blacks > whites:
                winner = config.BLACK
            self.ui.show_winner(winner)
        # restarting game
        print("game is over, and it will restart in 5 seconds...")
        time.sleep(5)
        self.restart_game()

    def restart_game(self):
        """
        重新开始游戏
        :return:
        """
        self.board.init_broad()
        self.ui.prepare()
        return self.start_loop()


if __name__ == '__main__':
    gc = GameCenter()
    gc.start_loop()
