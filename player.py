#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   player.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-20
   Description :

"""
import random

from board import Board


class StepIllegalError(Exception):
    pass


class Player(object):
    def __init__(self, board, game_center):
        assert isinstance(board, Board)
        self.board = board
        self.gc = game_center

    def move(self, *args, **kwargs):
        raise NotImplementedError


class HumanPlayer(Player):
    def move(self, clock):
        """
        选手走棋, 从ui获取输入，更新棋盘
        :param clock:
        :return:
        """
        step = self.gc.ui.get_mouse_input(clock)
        # check step valid
        print("step:{} valid_step: {}".format(step, self.board.next_valid_steps))
        if step not in self.board.next_valid_steps:
            raise StepIllegalError

        # put piece, cur_player same as the piece's color
        self.board.board[step[0]][step[1]] = self.board.cur_player
        self.gc.ui.put_piece(step, self.board.cur_player)

        # revers pieces
        reversed_lst = self.board.reverse_pieces(step)
        for piece in reversed_lst:
            self.gc.ui.put_piece(piece, self.board.cur_player)

        print("user:{} step:{} reverse:{} valid_step:{}".format(self.board.cur_player, step, reversed_lst,
                                                                self.board.next_valid_steps))
        self.board.print_board()
        return step


class RandomPlayer(Player):
    def move(self):
        """
        随机move
        :param step:
        :return:
        """
        piece_color = self.board.cur_player
        step = random.choice(self.board.next_valid_steps)
        self.board.board[step[0]][step[1]] = piece_color
        self.gc.ui.put_piece(step, piece_color)
        reversed_lst = self.board.reverse_pieces(step)
        for piece in reversed_lst:
            self.gc.ui.put_piece(piece, self.board.cur_player)
        print("user:{} step:{} reverse:{} valid_step:{}".format(self.board.cur_player, step, reversed_lst,
                                                                self.board.next_valid_steps))
        self.board.print_board()
        return step
