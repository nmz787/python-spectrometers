# -*- coding: utf-8 -*-

from spectrometers import Spectrometer

class Nanodrop(Spectrometer):
    """
    Basic API for nanodrops.
    """

    def capture(self):
        """
        Returns a list of wavelengths that were captured in this session.
        """
        raise NotImplementedError

