#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   mtcs.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-21
   Description :

"""
import copy
import math
import random

from board import Board

max_iter = 5
CP = 0.1


class Node:
    def __init__(self, *args, **kwargs):
        """
        :param kwargs:
        """
        # self.actions = kwargs['actions']
        self.state = kwargs['state']
        self.reward = 0.0
        self.visit_cnt = 0.0
        self.parent = None
        self.children = set()
        self.child_expand_num = 0

    def set_child(self, node):
        """

        :param node:
        :return:
        """
        self.children.add(node)
        node.parent = self

    def all_children_expand(self):
        """
        所有的孩子都被扩展了
        :return:
        """
        return len(self.state.board.get_next_valid_step()) - self.child_expand_num == 0


class State:
    def __init__(self, board, step=None):
        """
        棋盘的状态，传入棋盘和到达这个状态需要的action
        :param board: Board
        """
        self.board = copy_board(board)
        self.step = step or None
        self.is_terminate = self.board.game_ended()
        self.winner = self.board.get_winner() if self.is_terminate else None

    def update_terminate_status(self):
        self.is_terminate = self.board.game_ended()


def uct_search(state):
    """
    :param state: 当前的状态
    :return: 玩家MAX行动下，当前最优动作a*
    """
    cnt = 0
    # 根据当前的state创建一个root node
    rn = Node(state=state)
    while cnt < max_iter:
        vl = select_policy(rn)
        if vl.state.is_terminate:
            # direct select a leaf node with terminated status
            break
        ts = simulate_policy(vl.state)
        back_propagate(vl, ts)
        cnt += 1
    best_node = ucb_calculate(rn, 0)
    return best_node.state.step


def select_policy(rn):
    """

    :param rn: root node
    :return: node
    """
    v = rn
    while not v.state.is_terminate:
        if not v.all_children_expand():
            return expand(v)
        else:
            v = ucb_calculate(v, CP)
    return v


def back_propagate(v, ts):
    """

    :param v: 反向传播更新的起始节点
    :param ts: 终局的状态，根据其判断输赢方的分数
    :return:
    """
    winner = ts.board.get_winner()
    while v is not None:
        v.visit_cnt += 1
        i = 1 if winner != ts.board.cur_player else -1
        v.reward += i
        v = v.parent


def expand(v):
    """

    :param v: 节点v
    :return: 未被扩展的后继节点v'
    """
    step = random.choice(v.state.board.next_valid_steps)
    ns = generate_new_state(v.state, step)
    child_node = Node(state=ns)
    v.set_child(child_node)
    return child_node


def ucb_calculate(node, c):
    """
    计算ucb
    :param node: 节点v
    :param c: 超参数c
    :return:
    """
    max_v = -999999999
    ret_v = None

    for child in node.children:
        v = child.reward / child.visit_cnt + c * math.sqrt(
            2 * math.log(node.visit_cnt) / child.visit_cnt
        )
        if v >= max_v:
            ret_v = child

    return ret_v


def generate_new_state(state, step):
    """
    状态转移
    :param state:
    :param step:
    :return:
    """
    nb = copy.deepcopy(state.board)

    nb.board[step[0]][step[1]] = nb.cur_player
    _ = nb.reverse_pieces(step)
    nb.switch_player()

    ns = State(board=nb, step=step)
    return ns


def simulate_policy(s):
    """

    :param s: state 状态
    :return: st: state terminate，模拟的终止状态
    """
    ts = copy.deepcopy(s)
    print("start simulate...")
    while not ts.is_terminate:
        if not ts.board.next_valid_steps:
            ts.board.switch_player()

        step = random.choice(ts.board.next_valid_steps)
        ts.board.board[step[0]][step[1]] = ts.board.cur_player
        _ = ts.board.reverse_pieces(step)
        ts.board.switch_player()
        ts.update_terminate_status()
    return ts


def copy_board(ob):
    """

    :param ob:
    :return:
    """

    return Board(
        game_center=None,
        board=copy.copy(ob.board),
        init_board=False,
        cur_player=ob.cur_player,
        next_valid_steps=ob.next_valid_steps
    )
