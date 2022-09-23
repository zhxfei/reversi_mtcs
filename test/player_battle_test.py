#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   player_battle_test.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-22
   Description :

"""
import config
import time

from player import RandomPlayer, MCTSPlayer, GreedyPlayer
from board import Board

CNT = 1000


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


def random_vs_mtcs_with_ui():
    from reversi import GameCenter
    gc = GameCenter()
    gc.player_black = RandomPlayer(gc.board, gc)
    gc.mode = "random_player"
    gc.start_loop(battle_wait=2)


# random_vs_random()
random_vs_mtcs_with_ui()

# random_vs_greedy()
