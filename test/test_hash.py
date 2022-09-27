#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   test_hash.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-24
   Description :

"""
from mcts import Node, State
from board import Board

b1 = Board()
b2 = Board()
s1 = State(board=b1)
s2 = State(board=b2)
n1, _ = Node.from_cache(state=s1)
n2, _ = Node.from_cache(state=s2)


print(id(n2), "----", id(n2))
