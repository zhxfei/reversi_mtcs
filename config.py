#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   config.py
   author      :   zhuxiaofei22@mails.ucas.ac.cn
   Date：      :   2022-09-16
   Description :

"""
import os

FPS = 60
EMPTY = 0
BLACK = 1
WHITE = 2
INFINITY = 999999999
MAX = 0
MIN = 1
DEFAULT_LEVEL = 2
HUMAN = "human"
COMPUTER = "computer"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = ROOT_DIR + "/test"
IMAGES_DIR = ROOT_DIR + "/resources/images"
SOUND_DIR = ROOT_DIR + "/resources/sounds"
DATA_DIR = ROOT_DIR + "/data/"
CACHE_FILE_NAME = "node_cache"
CACHE_FILE_PATH = DATA_DIR + CACHE_FILE_NAME
