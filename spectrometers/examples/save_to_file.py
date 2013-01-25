import spectrometers

if __name__ == '__main__':
	if len(sys.argv)>1:
		spectrometer=Biowave_II()
		fileName = 'feExperiment'+datetime.datetime.now().strftime("%d_%m_%y__%H_%M_%S")
		while(1):
			try:
				sampleID=""
				while (enterSampleIds==True and sampleID==""):
					print 'enter sample ID'
					sampleID = raw_input().strip()
					spectrum = spectrometer.read()
				f=open(fileName,'a')
				f.write(yaml.dump(spectrum))
				f.close()
			except KeyboardInterrupt:
				print 'Done taking samples'
		spectrometer.close()