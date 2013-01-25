# -*- coding: utf-8 -*-

import json
import unittest

from spectroid import Spectrometer

class TestSpectrometer(unittest.TestCase):
    def test_initialization(self):
        # TODO find the not raises helper on self
        self.spectrometer = Spectrometer()

if __name__ == "__main__":
    unittest.main()
