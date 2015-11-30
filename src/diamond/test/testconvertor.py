from diamond.convertor import time

import unittest


class TestConvertor(unittest.TestCase):

    def test_basic(self):
        self.assertEquals(time.convert(60, 's', 's'), 60.0)
        self.assertEquals(time.convert(60, 's', 'm'), 1.0)
        self.assertEquals(time.convert(60000, 'ms', 'm'), 1.0)
        self.assertEquals(time.convert(60000, 'MS', 'minutes'), 1.0)

        self.assertEquals(time.convert(3600 * 1000 * 1.4, 'ms', 'h'), 1.4)
        self.assertEquals(time.convert(86400 * 1000 * 2.5, 'ms', 'd'), 2.5)
        self.assertEquals(time.convert(86400 * 1000 * 365 * 0.7, 'ms', 'y'),
                          0.7)
        self.assertEquals(time.convert(1000, 'ms', 'us'), 1000000)
        self.assertEquals(time.convert(1000, 'ms', 'ns'), 1000000000)

        self.assertEquals(time.convert(1.5, 'y', 'ns'),
                          1.5 * 365 * 24 * 3600 * 1000 * 1000 * 1000)

    def test_unrecognised_unit(self):
        self.assertRaises(NotImplementedError, time.convert, 60, 's', 'months')
