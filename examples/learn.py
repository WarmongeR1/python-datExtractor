# -*- encoding: utf-8 -*-
import csv

from os.path import join
import os
import json

import gspread
from oauth2client.client import SignedJwtAssertionCredentials

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

def get_test_table():
    scope = ["https://spreadsheets.google.com/feeds"]
    secrets_file = os.path.join(RES_FOLDER, 'google_json.json')
    spreadsheet = "markup"
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
    # Load in the secret JSON key (must be a service account)
    json_key = json.load(open(secrets_file))
    # Authenticate using the signed key
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)

    gc = gspread.authorize(credentials)
    return gc.open(spreadsheet).sheet1



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

    cnt_tests = 52
    test_data = table[1:cnt_tests]

    _path_active_texts_raw = join(LEARN_FOLDER, 'active_texts_raw.pkl')
    texts = get_texts_info(_path_active_texts_raw, active_folder)

    not_processing_list = get_not_valid_cnts()

    start_cnt = 32
    verbose = True
    test_data = test_data[start_cnt:]

    russian_page = [
        18,
        26,
        42,
        44,
        46,
        50,
    ]

    for page_str, _, date in test_data:
        page = int(page_str)
        print("Processing %s of %s" % (page_str, cnt_tests))

        if page in russian_page:
            print(
                "This is Russian page, parsedatetime does not support this language"
            )
            continue

        page_text = texts[page]
        if page not in not_processing_list and validate_page(page_text):
            page_date = get_data_from_page(page_text, verbose=verbose)
            page_date_str = page_date.strftime("%d.%m.%Y %H:%M:%S") \
                if page_date is not None  else 'None'
            if date != page_date_str:
                print("Error: excepted '%s', got '%s'" % (date, page_date_str))
                with open('/tmp/test.html', 'w') as fio:
                    fio.write(page_text)
                break


if __name__ == '__main__':
    main()


