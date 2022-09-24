#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   tree_test.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-23
   Description :

"""
import graphviz
import os
import config
from mtcs import Node

file_pre = config.TEST_DIR + "/unix"
file_name = config.TEST_DIR + "/unix.gv"

if os.path.exists(file_name):
    os.remove(file_name)

if os.path.exists(file_pre):
    os.remove(file_pre)

u = graphviz.Digraph('unix', filename=file_name,
                     node_attr={'color': 'lightblue2', 'style': 'filled'})
u.attr(size='6,6')

r = Node.loads(config.TEST_DIR + '/nodes.pickle')

# u.edge('System V.2', 'System V.3')
cnt = 0


def traverse_tree(root, fn):
    global cnt
    for child in root.children:
        cnt += 1
        cn = "{}/{}/{}".format(child.reward, child.visit_cnt, cnt)
        u.edge(fn, cn)
        traverse_tree(child, cn)


fn = "{}/{}/{}".format(r.reward, r.visit_cnt, cnt)

traverse_tree(r, fn)
u.view()
