# -*- encoding: utf-8 -*-
import csv
from functools import lru_cache
from os.path import join
import os
import json

import gspread

from oauth2client.client import SignedJwtAssertionCredentials

from datextractor import extract, RES_FOLDER, ACTIVE_PAGES_DIR, LEARN_FOLDER
from datextractor.utils import validate_page, get_texts_info, read_csv


@lru_cache(maxsize=10)
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


def get_test_table():
    scope = ["https://spreadsheets.google.com/feeds"]
    secrets_file = os.path.join(RES_FOLDER, 'google_json.json')
    spreadsheet = "markup"
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
    # Load in the secret JSON key (must be a service account)
    json_key = json.load(open(secrets_file))
    # Authenticate using the signed key
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'),
                                                scope)

    gc = gspread.authorize(credentials)
    return gc.open(spreadsheet).sheet1


def test_page(page: int, date: str, texts: list, tests_cnt: int = 10, verbose: bool = False):
    not_processing_list = get_not_valid_cnts()
    page_text = texts[page]
    if page not in not_processing_list and validate_page(page_text):
        for _ in range(tests_cnt):
            page_date = extract(page_text, verbose=verbose)
            page_date_str = page_date.strftime("%d.%m.%Y %H:%M:%S") \
                if page_date is not None  else 'None'
            if date != page_date_str:
                print("!!!!!!! Not equal")


def main():
    active_folder = ACTIVE_PAGES_DIR
    _path_markup_csv = join(RES_FOLDER, 'markup.csv')

    if os.path.exists(_path_markup_csv):
        table = read_csv(_path_markup_csv)
    else:
        table = get_test_table().get_all_values()
        with open(_path_markup_csv, 'w') as fio:
            _ = csv.writer(fio)
            for x in table:
                _.writerow(x)

    cnt_tests = 200
    test_data = table[1:cnt_tests + 2]

    _path_active_texts_raw = join(LEARN_FOLDER, 'active_texts_raw.pkl')
    texts = get_texts_info(_path_active_texts_raw, active_folder)

    not_processing_list = get_not_valid_cnts()

    continue_list = [
        1,
        9,
        18,
        21,
        37,
        42,
        44,
        47,
        59,
        50,
        63,
        60,
        64,
        68,
        76,
        81,
        82,
        89,
        92,
        105,
        106,
        116,
        117,
        118,
        111,
        120,
        129,
        134,
        137,
        141,
        163,
        164,
        174,
        175,
        176,
        178,
        179,
        185,
        181,
        188,
        189,
        198,
        192,
        195,
    ]
    start_cnt = 18
    verbose = False
    # test_data = test_data[0:19]

    test_number = 18

    test_page(test_number, test_data[test_number][2], texts, verbose=verbose)

    #
    #
    # for page_str, _, date in test_data:
    #     page = int(page_str)
    #     print("Processing %s of %s" % (page_str, cnt_tests))
    #     #
    #     # if page in continue_list:
    #     #     print("Random result")
    #     #     continue
    #
    #     if page not in continue_list:
    #         # print("Random result")
    #         continue
    #
    #     page_text = texts[page]
    #     if page not in not_processing_list and validate_page(page_text):
    #         page_date = extract(page_text, verbose=verbose)
    #         page_date_str = page_date.strftime("%d.%m.%Y %H:%M:%S") \
    #             if page_date is not None  else 'None'
    #         if date != page_date_str:
    #             print("Error: excepted '%s', got '%s'" % (date, page_date_str))
    #             with open('/tmp/test.html', 'w') as fio:
    #                 fio.write(page_text)
    #             break


if __name__ == '__main__':
    main()
