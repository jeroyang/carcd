#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""
test_carcd
----------------------------------

Tests for `carcd` module.
"""

import unittest
from collections import OrderedDict

from carcd import name


class TestCarcd(unittest.TestCase):

    def setUp(self):
        pass

    def test_beautify(self):
        data = '我是1個  大呆 !!'
        result = name.beautify(data)
        wanted = '我是 1 個 大呆!!'

    def test_asciilize(self):
        result = name.asciilize('12 34 何大一！')
        wanted = '12 34 He Da Yi!'
        self.assertEqual(result, wanted)

    def test_name_split(self):
        title = '12-2 ABC 大大一.mp3'
        result = name.name_split(title)
        wanted = OrderedDict([
                    ('number', '12-2'),
                    ('space', ' '),
                    ('title', 'ABC 大大一'),
                    ('ext', '.mp3')
                 ])
        self.assertEqual(result, wanted)

    def test_name_join(self):
        items = [
                    ('12-2', 'number'),
                    (None, 'space'),
                    ('ABC 大大一', 'title'),
                    ('.mp3', 'ext')
                 ]
        wanted = '12-2ABC 大大一.mp3'

    def test_number_format(self):
        result = name.number_format('2', fill=2)
        wanted = '02'
        self.assertEqual(result, wanted)
        result = name.number_format('2-2', fill=2)
        wanted = '02-02'
        self.assertEqual(result, wanted)

    def test_name_handle(self):
        title = '12-2 何大一.mp3'
        result = name.name_handle(title)
        wanted = '12-02 He Da Yi 何大一.mp3'
        self.assertEqual(result, wanted)

    def test_is_pinyined(self):
        data = 'He Da Yi 何大一'
        self.assertTrue(name.is_pinyined(data))
        data = 'ABC 何大一'
        self.assertFalse(name.is_pinyined(data))

    def tearDown(self):
        pass
