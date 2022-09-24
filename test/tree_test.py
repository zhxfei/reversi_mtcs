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

node_map = Node.loads(config.CACHE_FILE_PATH)

# u.edge('System V.2', 'System V.3')
cnt = 0


def traverse_tree(root, fn, u):
    global cnt
    for child in root.children:
        cnt += 1
        cn = "{}/{}/{}".format(child.reward, child.visit_cnt, cnt)
        u.edge(fn, cn)
        traverse_tree(child, cn, u)


def main():
    for _, node in node_map.items():
        key = hash(node)
        file_pre = config.TEST_DIR + "/{}".format(key)
        file_name = config.TEST_DIR + "/{}.gv".format(key)

        if os.path.exists(file_name):
            os.remove(file_name)

        if os.path.exists(file_pre):
            os.remove(file_pre)

        u = graphviz.Digraph('unix', filename=file_name,
                             node_attr={'color': 'lightblue2', 'style': 'filled'})
        u.attr(size='6,6')

        fn = "{}/{}/{}".format(node.reward, node.visit_cnt, cnt)
        traverse_tree(node, fn, u)
        u.view()


if __name__ == '__main__':
    main()
