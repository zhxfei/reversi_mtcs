#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   player.py
   author      :   zhouhualin22@mails.ucas.ac.cn
   Date：      :   2022-09-20
   Description :

"""
import time
import random
import pygame

from board import Board
from mtcs import uct_search, State


class StepIllegalError(Exception):
    pass


class Player(object):
    def __init__(self, board, game_center):
        assert isinstance(board, Board)
        self.board = board
        self.gc = game_center

    def _move(self, step, piece_color):
        """

        :param step: 走棋的位置
        :param piece_color: 走棋方
        :return:
        """
        if self.gc is not None:
            self.gc.ui.delete_put_remind_piece(self.board.get_next_valid_step(self.board.cur_player))

        # put piece, cur_player same as the piece's color
        self.board.board[step[0]][step[1]] = piece_color
        # revers pieces
        reversed_lst = self.board.reverse_pieces(step)

        if self.gc is not None:
            # update ui
            self.gc.ui.put_piece(step, piece_color)
            pygame.display.update()
            time.sleep(self.gc.reverse_wait)
            for piece in reversed_lst:
                self.gc.ui.put_piece(piece, piece_color)

        # print to debug
        # print("user:{} step:{} reverse:{} valid_step:{}".format(
        #     piece_color, step, reversed_lst,
        #     self.board.next_valid_steps)
        # )
        # self.board.print_board()

    def move(self, *args, **kwargs):
        raise NotImplementedError


class HumanPlayer(Player):
    def move(self, *args, **kwargs):
        """
        选手走棋, 从ui获取输入，更新棋盘
        :param clock:
        :return:
        """
        clock = args[0]
        step = self.gc.ui.get_mouse_input(clock)
        # check step valid
        print("step:{} valid_step: {}".format(step, self.board.next_valid_steps))
        if step not in self.board.next_valid_steps:
            raise StepIllegalError
        self._move(step, self.board.cur_player)
        return step


class RandomPlayer(Player):
    def move(self, *args, **kwargs):
        """
        随机走棋
        :param step:
        :return:
        """
        piece_color = self.board.cur_player
        step = random.choice(self.board.next_valid_steps)
        self._move(step, piece_color)
        return step


class MCTSPlayer(Player):

    def move(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        t = time.time()
        piece_color = self.board.cur_player
        state = State(board=self.board)
        step = uct_search(state)
        ret = round(time.time() - t, 2)
        self._move(step, piece_color)
        return ret


class GreedyPlayer(Player):

    def move(self, *args, **kwargs):
        """
        贪心走棋，每一次都找能翻转最多的棋子
        :param args:
        :param kwargs:
        :return:
        """
        piece_color = self.board.cur_player
        step = self.board.get_greedy_step()
        self._move(step, piece_color)
        return step
