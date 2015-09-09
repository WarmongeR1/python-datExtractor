# -*- encoding: utf-8 -*-

from os.path import join
import os

from datextractor.utils import get_texts_info, \
    get_data_from_page, \
    validate_page, read_csv

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
RES_FOLDER = os.path.join(BASE_DIR, 'resources')
LEARN_FOLDER = os.path.join(RES_FOLDER, 'learn')

OUT_RES_FOLDER = '/home/warmonger/Develop/Groups/PythonDigest/resources/'
ACTIVE_PAGES_DIR = os.path.join(OUT_RES_FOLDER, 'active', 'pages')
NOT_ACTIVE_PAGES_DIR = os.path.join(OUT_RES_FOLDER, 'not_active', 'pages')


def create_folder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)


create_folder(RES_FOLDER)
create_folder(LEARN_FOLDER)


def get_not_valid_cnts():
    return [
        193,
        259,
        306,
        357,
        396,
        405,
        419,
        421,
        475,
        512,
        527,
        542,
        579,
        685,
        782,
        788,
        814,
        826,
        840,
        849,
        858,
        875,
        913,
        932,
        964
    ]


def main():
    active_folder = ACTIVE_PAGES_DIR

    _path_markup_csv = join(RES_FOLDER, 'markup.csv')

    cnt_tests = 52
    test_data = read_csv(_path_markup_csv)[1:cnt_tests]

    _path_active_texts_raw = join(LEARN_FOLDER, 'active_texts_raw.pkl')
    texts = get_texts_info(_path_active_texts_raw, active_folder)

    not_processing_list = get_not_valid_cnts()

    for page_str, _, date in test_data:
        page = int(page_str)
        page_text = texts[page]
        if page not in not_processing_list and validate_page(page_text):
            page_date = get_data_from_page(page_text)
            if date != page_date:
                print("Error: excepted '%s', got '%s'" % (date, page_date))
                break

if __name__ == '__main__':
    main()
