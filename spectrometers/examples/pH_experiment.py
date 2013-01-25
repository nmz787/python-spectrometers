import spectrometers

if __name__ == '__main__':
	if len(sys.argv)!=2:
		print 'the only argument should be config file path'
		quit()
	spectrometer.calculate_pH(sys.argv[1])