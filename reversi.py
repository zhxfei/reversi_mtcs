#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   reversi.py
   author      :   zhouhualin22@mails.ucas.ac.cn
   Date：      :   2022-09-14
   Description :

"""
import sys
import time
import math
import traceback
import argparse

import pygame

import config
from ui import UI, GameExitError
from board import Board
from player import HumanPlayer, StepIllegalError, MCTSPlayer

CP = 1 / math.sqrt(2)
EXIT_CODE = 2


class GameCenter:
    def __init__(self, args):
        pygame.init()
        pygame.mixer.init()

        self.ui = UI(game_center=self)
        self.board = Board(game_center=self)

        # 初始化玩家
        self.player_black = HumanPlayer(self.board, self)
        self.player_white = MCTSPlayer(self.board, self)
        self.mode = "human_player"

        self.gm_is_running = True
        self.board.cur_player = config.BLACK
        self.battle_wait = 0.001
        self.reverse_wait = 0
        self.args = args

    def start_loop(self, battle_wait=0.01):
        """

        :return:
        """
        from mtcs import Node
        Node.init_cache_map()

        ret = 0
        self.ui.show_MCTS_time(ret)
        clock = pygame.time.Clock() if self.mode == "human_player" else None
        while self.gm_is_running and not self.board.game_ended():
            pygame.display.update()
            if clock:  clock.tick(config.FPS)
            time.sleep(battle_wait)
            if len(self.board.next_valid_steps) == 0:
                self.board.switch_player()
            try:
                if self.board.cur_player == config.BLACK:
                    self.ui.put_remind_piece(self.board.get_next_valid_step(self.board.cur_player))
                    self.player_black.move(clock)
                    self.board.switch_player()
                    self.ui.music.play()
                else:
                    ret = self.player_white.move()
                    self.board.switch_player()
                    self.ui.music.play()
            except StepIllegalError as e:
                traceback.print_exc()
                # todo: 调试

            except GameExitError:
                Node.save_cache_map()
                print("save cache map success! game will exit")
                sys.exit(EXIT_CODE)

            # 更新黑白棋统计
            whites, blacks, _ = self.board.count_pieces()
            self.ui.update_score(whites, blacks)
            self.ui.show_MCTS_time(ret)

        # game is not running...
        if self.board.game_ended():
            winner = self.board.get_winner()
            self.ui.show_winner(winner)

        # restarting game
        print("game is over, and it will restart in 5 seconds...")
        Node.save_cache_map()
        time.sleep(4)
        return self.restart_game(battle_wait)

    def restart_game(self, battle_wait):
        """
        重新开始游戏
        :return:
        """
        self.board.init_broad()
        self.ui.prepare()
        return self.start_loop(battle_wait)


def prepare_args():
    description = '''Maximum number of iterations'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-m', '--max_iterate',
                        required=False,
                        default=100,
                        dest='max_iterate',
                        action='store',
                        type=int,
                        help='The larger the number of iterations, the more simulations are performed and the closer the simulated sampling results are to the true distribution, but the longer the time consumed')
    parser.add_argument('-c', '--constant_factor',
                        required=False,
                        default=CP,
                        dest='constant_factor',
                        action='store',
                        type=float,
                        help='hyper parameter, constant factor to balance the experience and future expectation')
    args = parser.parse_args()
    return args


def main():
    args = prepare_args()
    gc = GameCenter(args)
    gc.start_loop()


if __name__ == '__main__':
    main()
