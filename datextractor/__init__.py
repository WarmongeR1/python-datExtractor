# -*- encoding: utf-8 -*-

import os

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
RES_FOLDER = os.path.join(BASE_DIR, 'resources')
LEARN_FOLDER = os.path.join(RES_FOLDER, 'learn')

OUT_RES_FOLDER = '/home/warmonger/Develop/Groups/PythonDigest/resources/'
ACTIVE_PAGES_DIR = os.path.join(OUT_RES_FOLDER, 'active', 'pages')
NOT_ACTIVE_PAGES_DIR = os.path.join(OUT_RES_FOLDER, 'not_active', 'pages')
TAGS_PATH = os.path.join(RES_FOLDER, 'tags.yaml')

def create_folder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)


create_folder(RES_FOLDER)
create_folder(LEARN_FOLDER)

from .extractor import *
