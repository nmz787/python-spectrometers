# -*- coding: utf-8 -*-

from spectrometers import Spectrometer

class openSpectrometer(spectrometer):
	def __init__(self):
		self.instrumentName='openSpectrometer'
		raise NotImplementedError("This section isn't developed yet.")
	def connect(self):
		raise NotImplementedError("This section isn't developed yet.")
	def disconnect(self):
		raise NotImplementedError("This section isn't developed yet.")
	def detect(self):
		raise NotImplementedError("This section isn't developed yet.")
	def read(self):
		raise NotImplementedError("This section isn't developed yet.")
	def write(self):
		raise NotImplementedError("This section isn't developed yet.")