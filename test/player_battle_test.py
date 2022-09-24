#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   player_battle_test.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-22
   Description :

"""
import time
import math
import config
import argparse

from player import RandomPlayer, MCTSPlayer, GreedyPlayer
from board import Board

CNT = 1000
CP = 1 / math.sqrt(2)


def random_vs_random():
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

        print("{} {}, gets results: {} : {}, no winner cnt:{}".format(
            "black vs white total", cnt, black_win_cnt, white_win_cnt, no_winner_cnt))


def random_vs_mtcs():
    start_time = time.time()
    no_winner_cnt, black_win_cnt, white_win_cnt, cnt = 0, 0, 0, 0
    while cnt < CNT:
        cnt += 1
        board = Board(game_center=None)
        player_black = RandomPlayer(board, game_center=None)
        player_white = MCTSPlayer(board, game_center=None)
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


def random_vs_greedy():
    no_winner_cnt, black_win_cnt, white_win_cnt, cnt = 0, 0, 0, 0
    while cnt < CNT:
        start_time = time.time()
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


def random_vs_mtcs_with_ui():
    from reversi import GameCenter
    args = prepare_args()
    args.max_iterate = 100
    gc = GameCenter(args)
    gc.player_black = RandomPlayer(gc.board, gc)
    gc.mode = "random_player"
    gc.start_loop(battle_wait=0)


# random_vs_random()
random_vs_mtcs_with_ui()

# random_vs_greedy()
