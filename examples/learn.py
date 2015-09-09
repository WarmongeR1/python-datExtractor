# -*- encoding: utf-8 -*-

from os.path import join
import os

from datextractor.utils import get_texts_info, \
    get_data_from_page, \
    check_page_without_date, \
    validate_page

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


def main():
    active_folder = ACTIVE_PAGES_DIR

    _path_active_texts_raw = join(LEARN_FOLDER, 'active_texts_raw.pkl')

    # ////////////////////////////
    # Load data
    # ////////////////////////////
    active_texts = get_texts_info(_path_active_texts_raw, active_folder)

    print(len(active_texts))

    not_processing_list = [
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

    cnt = 0
    for i, x in enumerate(active_texts[cnt:5]):
        print("Parse %s of %s" % (i + cnt, len(active_texts)))

        if x not in not_processing_list and validate_page(x):
            date = get_data_from_page(x)

            if date is None and check_page_without_date(x):
                continue
            elif date is None:
                with open('/tmp/test.html', 'w') as fio:
                    fio.write(x)
                break
            else:
                pass
                # print(date)
    else:
        print("All ok")


if __name__ == '__main__':
    main()
