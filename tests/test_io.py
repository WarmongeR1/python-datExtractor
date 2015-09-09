# -*- encoding: utf-8 -*-
import os
import unittest

from datextractor.utils import read


class IOTest(unittest.TestCase):
    def setUp(self):
        self._data_folder = os.path.join(os.path.dirname(__file__), 'data')

    def test_read(self):
        text = read(os.path.join(self._data_folder, 'read_test1.txt'))
        self.assertEqual(text,
"""fdsfdfgasd
gs
adgs
adg
sadg
sadgksadgksdag
asdgasd
gsadg
sadg
sadgsdagsadgsadgsadgasd



gsadgasdg
gsdagsa
dg
sa'g
t'r;hgep65gh34h345h#45h
h54""")
        self.assertEqual(len(text.split()), 16)
