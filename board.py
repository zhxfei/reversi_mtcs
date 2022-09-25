#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   board.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-20
   Description :

"""
from functools import reduce

import config


class Board:
    direction_lst = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    def __init__(self, *args, **kwargs):
        """
        通过gc来联系各个组件
        :param game_center:
        """
        self.board = kwargs.get('board', None)
        self.gc = kwargs.get('game_center', None)
        self.next_valid_steps = kwargs.get('next_valid_steps', None)
        # 即将落子的player
        self.cur_player = kwargs.get('cur_player', None)
        if kwargs.get('init_board', True):
            self.init_broad()

    def init_broad(self):
        # 初始化棋盘
        self.board = [[config.EMPTY] * 8 for _ in range(8)]
        self.board[3][3] = config.WHITE
        self.board[4][4] = config.WHITE
        self.board[3][4] = config.BLACK
        self.board[4][3] = config.BLACK
        # 黑棋先手
        self.cur_player = config.BLACK
        self.next_valid_steps = self.get_next_valid_step(config.BLACK)

    def check_direction(self, row, column, row_add, column_add, next_player, other_color):
        """
        检查某个位置的某个方向是否可以落子
        :param row:  行
        :param column: 列
        :param row_add: 行增量
        :param column_add: 列增量
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
                for (inc_x, inc_y) in self.direction_lst:
                    pos = self.check_direction(row, col, inc_x, inc_y, next_player, other)
                    if pos:
                        res.append(pos)
        return list(set(res))

    def update_next_valid_step(self):
        """
        每次选手走棋都需要更新
        :return:
        """
        self.next_valid_steps = self.get_next_valid_step()

    def reverse_piece(self, step):
        """翻转一颗棋子"""
        row, col = step
        if self.board[row][col] != config.EMPTY:
            self.board[row][col] = config.BLACK if self.board[row][col] == config.WHITE else config.WHITE

    def reverse_pieces(self, step, cur_player=None, do_reverse=True):
        """走棋时，找出所有的需要翻转的棋子"""
        cur_player = cur_player or self.cur_player
        other = self.get_counter(cur_player)
        ops_pieces = []
        row, col = step
        for (inc_x, inc_y) in self.direction_lst:
            pos = self.check_direction(row, col, inc_x, inc_y, cur_player, other)
            if pos:
                i = row + inc_x
                j = col + inc_y
                while self.board[i][j] != self.cur_player:
                    if do_reverse:
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

    def game_ended(self):
        """检测棋盘是否结束"""
        whites, blacks, empty = self.count_pieces()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        if self.get_next_valid_step(config.BLACK) == [] and \
                self.get_next_valid_step(config.WHITE) == []:
            return True

        return False

    def count_pieces(self):
        """ 统计棋盘中棋子的数量 """
        # print("count start....")
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
        # print("count over: {} {} {}".format(whites, blacks, empty))
        return whites, blacks, empty

    def print_board(self):
        """
        打印棋盘
        :return:
        """
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

    def switch_player(self):
        self.cur_player = self.get_counter(self.cur_player)
        self.update_next_valid_step()

    def get_winner(self):
        """
        获得棋盘的winner
        :return:
        """
        whites, blacks, empty = self.count_pieces()
        if whites > blacks:
            winner = config.WHITE
        elif blacks > whites:
            winner = config.BLACK
        else:
            winner = None
        return winner

    def get_greedy_step(self):
        max_num = -999
        ret_step = None
        for step in self.get_next_valid_step():
            ops_pieces = list(set(self.reverse_pieces(step, do_reverse=False)))
            if len(ops_pieces) >= max_num:
                ret_step = step
        return ret_step

    def count_level(self):
        """
        统计从开始游戏到现在共经历的多少步
        :return:
        """
        whites, blacks, _ = self.count_pieces()
        return whites + blacks - 4

    def __getitem__(self, i, j):
        return self.board[i][j]

    def generate_map_key(self):
        """
        生成 cache map key
        :return:
        """
        s = reduce(lambda x, y: x + y, [str(item) for row in self.board for item in row])
        s += str(self.cur_player)
        return s
