# -*- coding: utf-8 -*-

from spectrometers import Spectrometer

class Biowave_II(Spectrometer):
	def __init__():
		self.instrumentName='Biowave II'
	def connect(self, port=None):
		if port==None:
			for i in enumerate_serial_ports():
				self.ser=serial.Serial(port=i, baudrate=115200, rtscts=True, dsrdtr=True, timeout=5)
				if self.detect():
					return True
		else:
			self.ser=serial.Serial(port=port, baudrate=115200, rtscts=True, dsrdtr=True, timeout=5)	
	def disconnect(self):
		self.ser.close()
		self.ser=None
	def detect():
		print 'Press the \'Take Reading\' button on the spectrometer\nWaiting 5 seconds'
		end_time=time.time()+5
		while(time.time()<end_time):
			if self.instrumentName in self.ser.readline():
				return True
		return False
	def read(self):
		print 'Starting to look for data'
		startWavelength=None; endWavelength=None; datapoints=[]; datapointsReady=False; lastLine=''
		while(1):
			line=self.ser.readline()
			print 'got a line of data: ' + line
			if "$PAX" in line:
				startWavelength, endWavelength = [int(x) for x in line.split()[4:6]]
				minAbs, maxAbs = [float(x) for x in line.split()[9:11]]
				lastLine=line
			elif "$PPY" in line and len(line.split())>7:
				datapoints= ' '.join(line.split()[5:])
				lastLine=line
			elif "$PPY" in line and len(line.split())==7:
				datapointsReady=True
				datapoints=re.sub('[\n\r]', '', datapoints)
				datapoints=re.sub(r'([0-9])0\.([0-9])', r'\1 0.\2', datapoints)
				datapoints=[float(x) for x in datapoints.split()]
				lastLine=''
			elif "$PPY" in lastLine:
				datapoints+=line
			if datapointsReady==True:
				datapoints =  OrderedDict([(wavelengths[index], ad_voltages[index]) for index in 
										range(0, min([len(ad_voltages), len(wavelengths)]))])
				return OrderedDict([("openSpectrometer data file" , "version 0"), ("sample ID", sampleID),	("startWavelength" , startWavelength), 
									("endWavelength" , endWavelength), ("minAbsorbanceDataValue" , minAbs), 
									("maxAbsorbanceDataValue" , maxAbs), ("datapoints" , datapoints)])
	def write(self):
		raise NotImplementedError("This section isn't developed yet.")