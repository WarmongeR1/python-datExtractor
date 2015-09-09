# -*- encoding: utf-8 -*-
import unittest
import os
import datetime

from datextractor.utils import load_pickle, get_data_from_page


class GetDataFromPageTest(unittest.TestCase):
    def setUp(self):

        _filepath = os.path.join(os.path.dirname(__file__), 'data',
                                 'active_texts_raw.pkl')
        print(_filepath)
        self._texts = load_pickle(_filepath)

    def testEqual(self):
        _result_equal_test = [
            '2015-05-18 00:00:00',
            '2014-10-29 00:00:00',
            '2015-04-22 20:15:00',
            None,
            '2013-11-30 00:00:00',
        ]
        for i, x in enumerate(_result_equal_test):
            _ = get_data_from_page(self._texts[i])
            if x is not None:
                self.assertTrue(isinstance(_, datetime.datetime))
                self.assertEqual(str(_), x)
            else:
                self.assertEqual(_, x)
