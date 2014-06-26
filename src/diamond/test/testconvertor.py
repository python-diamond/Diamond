from diamond.convertor import time

import unittest


class TestConvertor(unittest.TestCase):
    def test_basic(self):
        self.assertEquals(time.convert(60, 's', 's'), 60.0)
        self.assertEquals(time.convert(60, 's', 'm'), 1.0)
        self.assertEquals(time.convert(60000, 'ms', 'm'), 1.0)
        self.assertEquals(time.convert(60000, 'MS', 'minutes'), 1.0)

    def test_unrecognised_unit(self):
        self.assertRaises(NotImplementedError, time.convert, 60, 's', 'hours')
