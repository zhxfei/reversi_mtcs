#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   mtcs.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-21
   Description :

"""
import os
import copy
import math
import random
import pickle

import config
from board import Board

CACHE_ON = 1
MAX_VISIT_COUNT = 100


class Node:
    node_cache = dict()
    cache_battle_layer = 10

    def __init__(self, *args, **kwargs):
        """
        蒙特卡洛树节点
        :param args:
        :param kwargs:
                state: 每个节点都对应一个棋盘，都有一个状态
        """
        # self.actions = kwargs['actions']
        self.state = kwargs['state']
        self.reward = 0.0
        self.visit_cnt = 0.0
        self.parent = None
        self.children = set()
        self.child_expand_num = 0
        self.valid_actions = self.state.board.get_next_valid_step()

    def set_child(self, node):
        """
        设置孩子节点
        :param node:
        :return:
        """
        self.children.add(node)
        node.parent = self

    def all_children_expand(self):
        """
        判断是否所有的孩子都被扩展了
        :return:
        """
        return len(self.valid_actions) == 0

    @classmethod
    def init_cache_map(cls):
        if not cls.node_cache and os.path.exists(config.CACHE_FILE_PATH):
            # every time when game start up, should init cache map
            cls.node_cache = cls.loads(config.CACHE_FILE_PATH)

    @classmethod
    def save_cache_map(cls):
        if not cls.node_cache:
            # node cache is empty
            return

        with open(config.CACHE_FILE_PATH, 'wb') as f:
            pickle.dump(cls.node_cache, f)

    @classmethod
    def from_cache(cls, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return: return a tuple, instance and whether the item come from the cache
        """
        state = kwargs['state']
        battle_num = state.board.count_level()
        if battle_num > cls.cache_battle_layer or not CACHE_ON:
            # 当玩家走棋次数超过一定数量就不做缓存，当对局到后面做蒙特卡洛树实时构建的深度也不是很高
            # 对局次数越少，越有共性，对局次数越多，构建越快
            return cls(*args, **kwargs), False

        item_key = hash(state.board)
        if item_key in cls.node_cache:
            # key is exists in cache map, return old instance
            # print("key exists!")
            # state.board.print_board()
            return cls.node_cache[item_key], True

        # new instance
        ins = cls(*args, **kwargs)
        cls.node_cache[item_key] = ins
        return ins, False

    @staticmethod
    def loads(file_path):
        with open(file_path, 'rb') as f:
            ret = pickle.load(f)
        return ret


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
        """
        更新棋盘是否结束的标识
        :return:
        """
        self.is_terminate = self.board.game_ended()
        self.winner = self.board.get_winner() if self.is_terminate else None


def uct_search(state, max_iter, cp):
    """
    :param state: 当前的状态
    :param max_iter: 最大迭代次数
    :param cp: 常数因子，超参数
    :return: 玩家MAX行动下，当前最优动作a*
    """
    cnt = 0
    # 根据当前的state创建一个root node
    rn, _ = Node.from_cache(state=state)

    while cnt < max_iter:
        if rn.visit_cnt > MAX_VISIT_COUNT:
            # 当采样超过一定的数量后就不再采样
            break
        vl = select_policy(rn, cp)
        ts = simulate_policy(vl.state)
        back_propagate(vl, ts)
        cnt += 1

    best_node = ucb_calculate(rn, 0)
    return best_node.state.step


def select_policy(root_node, cp):
    """

    :param root_node:
    :param cp: 超参数
    :return: node
    """
    ret_node = root_node
    while not ret_node.state.is_terminate:
        if not ret_node.all_children_expand():
            return expand(ret_node)
        else:
            r = ucb_calculate(ret_node, cp)
            if r == ret_node:
                # 当前的棋盘无棋可走的时候
                break
            ret_node = r
    return ret_node


def expand(v):
    """

    :param v: 节点v
    :return: 未被扩展的后继节点child_node
    """
    step = random.choice(v.valid_actions)
    v.valid_actions.remove(step)

    ns = generate_new_state(v.state, step)
    child_node = Node(state=ns)
    v.set_child(child_node)
    return child_node


def ucb_calculate(node, c):
    """
    根据ucb算法计算最优的节点
    :param node: 节点v
    :param c: 超参数c, default: 1/math.sqrt(2)
    :return:
    """
    max_v = -1 * config.INFINITY
    ret_v = node

    for child in node.children:
        v = child.reward / child.visit_cnt + c * math.sqrt(
            2 * math.log(node.visit_cnt) / child.visit_cnt
        )
        if v >= max_v:
            max_v = v
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
    while not ts.is_terminate:
        if not ts.board.next_valid_steps:
            ts.board.switch_player()

        step = random.choice(ts.board.next_valid_steps)
        ts.board.board[step[0]][step[1]] = ts.board.cur_player
        _ = ts.board.reverse_pieces(step)
        ts.board.switch_player()
        ts.update_terminate_status()
    return ts


def back_propagate(v, ts):
    """
    反向传播更新reward和visit count
    :param v: 反向传播更新的起始节点
    :param ts: 终局的状态，根据其判断输赢方的分数
    :return:
    """
    winner = ts.board.get_winner()
    # 价值500W的公式
    delta = -1 if winner == v.state.board.cur_player else 1

    while v is not None:
        v.visit_cnt += 1
        v.reward += delta

        delta = -1 * delta
        v = v.parent


def copy_board(ob):
    """
    拷贝棋盘，用新棋盘模拟
    :param ob:
    :return:
    """
    return Board(
        game_center=None,
        board=copy.deepcopy(ob.board),
        init_board=False,
        cur_player=ob.cur_player,
        next_valid_steps=ob.next_valid_steps
    )
