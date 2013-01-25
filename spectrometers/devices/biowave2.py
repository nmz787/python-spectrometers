# -*- coding: utf-8 -*-

from spectrometers import Spectrometer

class Biowave2(Spectrometer):
    """
    Basic API for Bio-Wave II.
    """

    def capture(self):
        """
        Returns a list of wavelengths that were captured in this session.
        """
        raise NotImplementedError

