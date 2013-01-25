# -*- coding: utf-8 -*-
from collections import OrderedDict
class Spectrometer(object):
    """
    Exposes a simple API for spectrometers/spectrophotometers.
    """
    def __init__(self):
        object.__init__(self)
		raise NotImplementedError("This must be implemented by the subclass.")
	def connect(self):
		raise NotImplementedError("This must be implemented by the subclass.")
	def disconnect(self):
		raise NotImplementedError("This must be implemented by the subclass.")
	def detect(self):
		raise NotImplementedError("This must be implemented by the subclass.")
	def read(self):
		raise NotImplementedError("This must be implemented by the subclass.")
	def write(self):
		raise NotImplementedError("This must be implemented by the subclass.")