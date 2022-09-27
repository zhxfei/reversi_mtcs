#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   player_battle_test.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-22
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
from player import RandomPlayer, StepIllegalError, MCTSPlayer, GreedyPlayer
from mtcs import Node

CNT = 1000
CP = 1 / math.sqrt(2)
EXIT_CODE = 2
restart_wait = 0.1
no_winner_cnt, black_win_cnt, white_win_cnt, cnt = 0, 0, 0, 0
MAX_COUNT = 1000


def random_vs_random():
    from mtcs import Node
    Node.init_cache_map()
    start_time = time.time()
    no_winner_cnt, black_win_cnt, white_win_cnt, cnt = 0, 0, 0, 0
    while cnt < CNT:
        cnt += 1
        board = Board(game_center=None)
        player_black = RandomPlayer(board, game_center=None)
        player_white = RandomPlayer(board, game_center=None)
        while not board.game_ended():
            if len(board.next_valid_steps) == 0:
                board.switch_player()
            if board.cur_player == config.BLACK:
                player_black.move()
                board.switch_player()
            else:
                player_white.move()
                board.switch_player()
        if board.get_winner() == config.BLACK:
            black_win_cnt += 1
        elif board.get_winner() == config.WHITE:
            white_win_cnt += 1
        else:
            no_winner_cnt += 1

        print("{} {}, gets results: {} : {}, no winner cnt:{}, cost time:{}".format(
            "black vs white total", cnt, black_win_cnt, white_win_cnt, no_winner_cnt, time.time() - start_time))


#
# def random_vs_mtcs():
#     from mtcs import Node
#     Node.init_cache_map()
#
#     args = prepare_args()
#     gc = GameCenter(args)
#
#     start_time = time.time()
#     no_winner_cnt, black_win_cnt, white_win_cnt, cnt = 0, 0, 0, 0
#     while cnt < CNT:
#         cnt += 1
#         board = Board(game_center=gc)
#         player_black = RandomPlayer(board, game_center=gc)
#         player_white = MCTSPlayer(board, game_center=gc)
#         while not board.game_ended():
#             if len(board.next_valid_steps) == 0:
#                 board.switch_player()
#             if board.cur_player == config.BLACK:
#                 player_black.move()
#                 board.switch_player()
#             else:
#                 player_white.move()
#                 board.switch_player()
#         if board.get_winner() == config.BLACK:
#             black_win_cnt += 1
#         elif board.get_winner() == config.WHITE:
#             white_win_cnt += 1
#         else:
#             no_winner_cnt += 1
#         print("{} {}, gets results: {} : {}, no winner cnt:{}, cost time:{}".format(
#             "black vs white total", cnt, black_win_cnt, white_win_cnt, no_winner_cnt, time.time() - start_time))


def random_vs_greedy():
    start_time = time.time()
    no_winner_cnt, black_win_cnt, white_win_cnt, cnt = 0, 0, 0, 0
    while cnt < CNT:
        cnt += 1
        board = Board(game_center=None)
        player_black = RandomPlayer(board, game_center=None)
        player_white = GreedyPlayer(board, game_center=None)
        while not board.game_ended():
            if len(board.next_valid_steps) == 0:
                board.switch_player()
            if board.cur_player == config.BLACK:
                player_black.move()
                board.switch_player()
            else:
                player_white.move()
                board.switch_player()
        if board.get_winner() == config.BLACK:
            black_win_cnt += 1
        elif board.get_winner() == config.WHITE:
            white_win_cnt += 1
        else:
            no_winner_cnt += 1

        print("{} {}, gets results: {} : {}, no winner cnt:{}, cost time:{}".format(
            "black vs white total", cnt, black_win_cnt, white_win_cnt, no_winner_cnt, time.time() - start_time))


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


class TestGameCenter:
    def __init__(self, args):
        pygame.init()
        pygame.mixer.init()

        self.ui = UI(game_center=self)
        self.board = Board(game_center=self)

        # 初始化玩家
        self.player_black = RandomPlayer(self.board, self)
        self.player_white = MCTSPlayer(self.board, self)
        self.mode = "human_player"

        self.gm_is_running = True
        self.board.cur_player = config.BLACK
        self.battle_wait = 0.001
        self.reverse_wait = 0.001
        self.args = args

    def start_loop(self, battle_wait=0.01):
        """

        :return:
        """
        Node.init_cache_map()
        global cnt, black_win_cnt, no_winner_cnt, white_win_cnt
        cnt += 1
        if cnt > MAX_COUNT: return
        cost_time = 0
        total_cost_time = 0
        self.ui.show_MCTS_time(cost_time, total_cost_time)
        start_time = time.time()

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
                    # self.ui.music.play()
                else:
                    cost_time = self.player_white.move()
                    total_cost_time += cost_time
                    total_cost_time = round(total_cost_time, 2)
                    self.board.switch_player()
                    # self.ui.music.play()
            except StepIllegalError as e:
                traceback.print_exc()
                # todo: 调试

            except GameExitError:
                # Node.save_cache_map()
                print("save cache map success! game will exit")
                sys.exit(EXIT_CODE)

            # 更新黑白棋统计
            whites, blacks, _ = self.board.count_pieces()
            self.ui.update_score(whites, blacks)
            self.ui.show_MCTS_time(cost_time, total_cost_time)

        # game is not running...
        if self.board.game_ended():
            winner = self.board.get_winner()
            # self.ui.show_winner(winner)
            if winner == config.BLACK:
                black_win_cnt += 1
            elif winner == config.WHITE:
                white_win_cnt += 1
            else:
                no_winner_cnt += 1
            print("{} {}, gets results: {} : {}, no winner cnt:{}, cost time:{}".format(
                "black vs white total", cnt, black_win_cnt, white_win_cnt, no_winner_cnt, time.time() - start_time))

        # restarting game
        print("game is over, and it will restart in 5 seconds...")
        Node.save_cache_map()
        time.sleep(restart_wait)
        return self.restart_game(battle_wait)

    def restart_game(self, battle_wait):
        """
        重新开始游戏
        :return:
        """
        self.board.init_broad()
        self.ui.prepare()
        return self.start_loop(battle_wait)


def random_vs_mtcs_with_ui_main():
    args = prepare_args()
    gc = TestGameCenter(args)
    gc.start_loop()


if __name__ == '__main__':
    random_vs_greedy()
    # random_vs_mtcs_with_ui_main()

    # random_vs_greedy()
