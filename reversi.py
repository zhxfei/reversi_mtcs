#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   reversi.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-14
   Description :

"""
import os
import time
import random

import config
from collections import namedtuple

from ui import UI

import pygame

FPS = 60

Position = namedtuple('Position', ['x', 'y'])


class StepIllegal(Exception):
    pass


class Broad:
    def __init__(self, game_center=None):
        self.board = None
        self.gc = game_center
        self.cur_player = config.BLACK
        self.init_broad()
        self.next_valid_steps = self.get_next_valid_step()

    def init_broad(self):
        self.board = [[config.EMPTY] * 8 for _ in range(8)]
        self.board[3][3] = config.WHITE
        self.board[4][4] = config.WHITE
        self.board[3][4] = config.BLACK
        self.board[4][3] = config.BLACK

    def check_direction(self, row, column, row_add, column_add, next_player, other_color):
        """
        检查某个位置的某个方向是否可以落子
        :param row:
        :param column:
        :param row_add:
        :param column_add:
        :param next_player:
        :param other_color:
        :return:
        """

        i = row + row_add
        j = column + column_add
        if 0 <= i <= 7 and 0 <= j <= 7 and self.board[i][j] == other_color:
            i += row_add
            j += column_add
            while 0 <= i <= 7 and 0 <= j <= 7 and self.board[i][j] == other_color:
                i += row_add
                j += column_add
            if 0 <= i <= 7 and 0 <= j <= 7 and self.board[i][j] == next_player:
                return row, column

    def get_next_valid_step(self, next_player=None):
        """
        获取下一步可能得步骤
        :param next_player: 下一步谁走
        :return:
        """
        if next_player is None:
            next_player = self.cur_player
        other = self.get_counter(next_player)
        res = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != config.EMPTY:
                    continue
                for (inc_x, inc_y) in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
                    pos = self.check_direction(row, col, inc_x, inc_y, next_player, other)
                    if pos:
                        res.append(pos)
        return res

    def reverse_piece(self, step):
        row, col = step
        if self.board[row][col] != config.EMPTY:
            self.board[row][col] = config.BLACK if self.board[row][col] == config.WHITE else config.WHITE

    def reverse_pieces(self, step, cur_player=None):
        cur_player = cur_player or self.cur_player
        other = self.get_counter(cur_player)
        ops_pieces = []
        row, col = step
        for (inc_x, inc_y) in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            pos = self.check_direction(row, col, inc_x, inc_y, cur_player, other)
            if pos:
                i = row + inc_x
                j = col + inc_y
                while self.board[i][j] != self.cur_player:
                    self.reverse_piece((i, j))
                    ops_pieces.append((i, j))
                    i = i + inc_x
                    j = j + inc_y
        return ops_pieces

    def get_counter(self, next_player):
        next_player = next_player or self.cur_player
        if next_player == config.BLACK:
            return config.WHITE
        else:
            return config.BLACK

    def move(self, step):
        """
        update broad, reverse
        :param step:
        :return:
        """
        # check step valid
        if step not in self.next_valid_steps:
            raise StepIllegal

        # put piece, cur_player same as the piece's color
        self.board[step[0]][step[1]] = self.cur_player
        self.gc.ui.put_piece(step, self.cur_player)

        # revers pieces
        reversed_lst = self.reverse_pieces(step)
        for piece in reversed_lst:
            self.gc.ui.put_piece(piece, self.cur_player)

        print("user:{} step:{} reverse:{} valid_step:{}".format(self.cur_player, step, reversed_lst,
                                                                self.next_valid_steps))
        self.print_board()

        # get next_valid_step, update player
        self.cur_player = self.get_counter(self.cur_player)
        self.next_valid_steps = self.get_next_valid_step()
        if len(self.next_valid_steps) == 0:
            self.cur_player = self.get_counter(self.cur_player)
            self.next_valid_steps = self.get_next_valid_step()

        if self.cur_player == config.BLACK:
            # return ui loop
            return
        else:
            # next_step = self.mtcs.get_next_step(self)
            # return self.move(self., next_step)
            next_step = random.choice(self.next_valid_steps)
            return self.move(next_step)

    def __getitem__(self, i, j):
        return self.board[i][j]

    def game_ended(self):
        """ Is the game ended? """
        # board full or wipeout
        whites, blacks, empty = self.count_pieces()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        if self.get_next_valid_step(config.BLACK) == [] and \
                self.get_next_valid_step(config.WHITE) == []:
            return True

        return False

    def count_pieces(self):
        """ Returns the number of white pieces, black pieces and empty squares, in
        this order.
        """
        whites = 0
        blacks = 0
        empty = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == config.WHITE:
                    whites += 1
                elif self.board[i][j] == config.BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

    def print_board(self):
        for i in range(8):
            print(i, ' |', end=' ')
            for j in range(8):
                if self.board[i][j] == config.BLACK:
                    print('B', end=' ')
                elif self.board[i][j] == config.WHITE:
                    print('W', end=' ')
                else:
                    print(' ', end=' ')
                print('|', end=' ')
            print()


class GameCenter:
    def __init__(self):
        pygame.init()
        self.ui = UI(game_center=self)
        self.board = Broad(game_center=self)

        self.gm_is_running = True

    def start_loop(self):
        """

        :return:
        """
        clock = pygame.time.Clock()

        winner = None

        while self.gm_is_running:
            clock.tick(config.FPS)
            #pygame.display.flip()
            time.sleep(0.05)
            # if self.board.game_ended():
            #     whites, blacks, empty = self.board.count_pieces()
            #     if whites > blacks:
            #         winner = config.WHITE
            #     elif blacks > whites:
            #         winner = config.BLACK
            #     break
            if self.board.cur_player == config.BLACK:
                step = self.ui.get_mouse_input(clock)
                try:
                    self.board.move(step)
                except StepIllegal:
                    print("illegal step {}".format(step))


if __name__ == '__main__':
    gc = GameCenter()
    gc.start_loop()
