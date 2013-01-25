# -*- coding: utf-8 -*-

from spectrometers import Spectrometer
from spectrometers.devices import Nanodrop
from spectrometers.devices import Biowave2

import json
import unittest

class TestSpectrometer(unittest.TestCase):
    def test_initialization(self):
        # TODO find the not raises helper on self
        self.spectrometer = Spectrometer()

if __name__ == "__main__":
    unittest.main()
