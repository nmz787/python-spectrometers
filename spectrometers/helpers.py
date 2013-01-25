import yaml
import yaml.constructor
 
try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict
 
class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """
 
    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)
 
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)
 
    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)
 
    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)
 
        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping
''' 
if __name__ == '__main__':
    import textwrap
 
    sample = """
    one:
        two: fish
        red: fish
        blue: fish
    two:
        a: yes
        b: no
        c: null
    """
 
    data = yaml.load(textwrap.dedent(sample), OrderedDictYAMLLoader)
 
    assert type(data) is OrderedDict
    print data
'''
import os, datetime, serial, re, yaml, sys, numpy, time, copy
import _winreg as winreg
import itertools
from collections import OrderedDict 
try:
	import gtk
	from matplotlib.figure import Figure
	from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
	from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
except ImportError as exception:
	pass
	

	
def index_min(values):
    return min(xrange(len(values)),key=values.__getitem__)
	
def index_max(values):
    return max(xrange(len(values)),key=values.__getitem__)

def enumerate_serial_ports():
	""" Uses the Win32 registry to return an 
	iterator of serial (COM) ports 
	existing on this computer.
	"""
	#need to learn how to tell if it is windows or not, then branch to do appropriate enumeration
	
	path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
	try:
		key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
	except WindowsError:
		print 'error'
	for i in itertools.count():
		try:
			val = winreg.EnumValue(key, i)
			yield str(val[1])
		except EnvironmentError:
			break
def averageSpectra(listOfSpectra):
	#copy a spectrum so we retain the instrumentName and such in the output
	output=copy.deepcopy(listOfSpectra[0])
	temp=[]
	
	#set all the data in the output to 0
	for wavelength in output['datapoints'].keys():
		temp.append(0)
		output['datapoints'][wavelength]=0
	
	#sum the spectra data
	for spectrum in listOfSpectra:
		for wavelength in output['datapoints'].keys():
			output['datapoints'][wavelength]=output['datapoints'][wavelength]+spectrum['datapoints'][wavelength]
	for wavelength in output['datapoints'].keys():
		output['datapoints'][wavelength]=output['datapoints'][wavelength]/len(listOfSpectra)

	return output
def getLambdaMax(spectrum):
	peakSearchPattern = [1,1,1,-1,-1,-1]

	#this is the list of wavelengths
	xData=numpy.array(spectrum['datapoints'].keys())
	yData=numpy.array(spectrum['datapoints'].values())

	#find peaks on a polyfit
	z=numpy.polyfit(xData, yData,20)
	p = numpy.poly1d(z)
	import matplotlib.pyplot as plt
	import matplotlib
	from matplotlib.widgets import Button
	
	diffData=numpy.diff(p(xData))
	
	i=0
	j=0
	possiblePeaks={}
	for i in range(0,len(diffData)-1):
		if i>=((len(peakSearchPattern)/2)-1) and i<=(len(diffData)-(len(peakSearchPattern)/2)-1):
			j=i-(len(peakSearchPattern)/2)
			counter=0
			for element in peakSearchPattern:
				if element==1 and diffData[j]<0:
					break
				if element==-1 and diffData[j]>0:
					break
				counter+=1
				j+=1
			if counter==len(peakSearchPattern):
				current_wavelength=spectrum['datapoints'].keys()[i]
				possiblePeaks[current_wavelength]=spectrum['datapoints'][current_wavelength]
	
	#make a new plotter window with the dataset
	fig1=spectrum_plotter(xData, yData)
	#plot the original dataset and set it selectable
	fig1.plotSelectable(xData, yData, 'k.', picker=5)
	#plot the fitted curve, just to make sure it was a decent fit #DEBUG this plot could be turned off
	fig1.plot(xData, p(xData), 'w-')
	#plot the possiblePeaks detected using the curve fit to smooth noise
	fig1.plot(possiblePeaks.keys(), possiblePeaks.values(), 'ro', ms=10)
	
	possHiPeak=index_max(possiblePeaks.values())
	fig1.selectPoint(possiblePeaks.keys()[possHiPeak], possiblePeaks.values()[possHiPeak])
	print 'selected peak'
	print fig1.show()

	return possiblePeaks
def calculate_pH(experiment_config_file_path):
	cfgFile=yaml.load(open(experiment_config_file_path), OrderedDictYAMLLoader)
	assert type(cfgFile) is OrderedDict
	
	if cfgFile['openSpectrometer experiment name']!='pH determination':
		print 'config file not for pH experiment'
		quit()
	
	baseLambdaMax=0
	acidLambdaMax=0
	
	baseAvgValueAtBaseLambdaMax=0
	acidAvgValueAtAcidLambdaMax=0
	
	bufferAvgValueAtBaseLambdaMax=0
	bufferAvgValueAtAcidLambdaMax=0
	
	baseData=[]
	acidData=[]
	bufferData=[]

	for fileName in cfgFile['acidFileList'].split(','):
		try:
			acidData.append(yaml.load(open(fileName)))
		except IOError:
			f=os.path.join(os.path.dirname(experiment_config_file_path),fileName)
			print '*****'
			print f
			print '*****'
			acidData.append(yaml.load(open(f)))
	for fileName in cfgFile['baseFileList'].split(','):
		try:
			baseData.append(yaml.load(open(fileName)))
		except IOError:
			baseData.append(yaml.load(open(os.path.join(os.path.dirname(experiment_config_file_path),fileName))))
	for fileName in cfgFile['bufferFileList'].split(','):
		try:
			bufferData.append(yaml.load(open(fileName)))
		except IOError:
			bufferData.append(yaml.load(open(os.path.join(os.path.dirname(experiment_config_file_path),fileName))))	
	return getLambdaMax(averageSpectra(acidData))

class spectrum_plotter:
	def __init__(self, xs, ys):
		self.xs=xs
		self.ys=ys
		
		self.win = gtk.Window()
		self.win.connect("destroy", lambda x: gtk.main_quit())
		self.win.set_default_size(800,600)
		self.win.set_title("openSpectrometer")

		self.vbox = gtk.VBox()
		self.win.add(self.vbox)
		
		self.fig = Figure(figsize=(5,4), dpi=100)
		self.canvas = FigureCanvas(self.fig)  # a gtk.DrawingArea
		
		self.ax = self.fig.add_subplot(111)
		
		self.canvas.mpl_connect('pick_event', self.onpick)
		
		self.vbox.pack_start(self.canvas)
		self.toolbar = NavigationToolbar(self.canvas, self.win)
		self.hbox = gtk.HBox()
		self.button=gtk.Button('Select this point as lambda max')
		self.button.connect("clicked", self.buttonClick)
		self.hbox.pack_start(self.toolbar)
		self.hbox.pack_start(self.button)
		self.vbox.pack_start(self.hbox, False, False)
		
		self.lastind = 0

		self.text = self.ax.text(0.05, 0.95, 'Datapoint index selected: none',
                            transform=self.ax.transAxes, va='top')
	def plot(self, *args, **kwargs):
		self.ax.plot(*args, **kwargs)
	def plotSelectable(self, *args, **kwargs):
		self.line=self.ax.plot(*args, **kwargs)
	def selectPoint(self, x, y):
		self.selected = self.ax.plot([x],[y], 'o', ms=20, alpha=0.4, 
									   color='yellow', visible=False)
	def show(self):
		self.win.show_all()
		gtk.main()
	def buttonClick(self, event):
		return self.lastind
	def onpick(self, event):
		if event.artist!=self.line[0]: return True
		
		N = len(event.ind)
		if not N: return True
		print 'here'

		if N > 1:
			print '%i points found!' % N
		print event.ind

		# the click locations
		x = event.mouseevent.xdata
		y = event.mouseevent.ydata

		dx = numpy.array(x-self.xs[event.ind],dtype=float)
		dy = numpy.array(y-self.ys[event.ind],dtype=float)

		distances = numpy.hypot(dx,dy)
		indmin = distances.argmin()
		dataind = event.ind[indmin]

		self.lastind = dataind
		self.update()

	def update(self):
		if self.lastind is None: return

		dataind = self.lastind
		
		self.selected[0].set_visible(True)
		self.selected[0].set_data(self.xs[dataind], self.ys[dataind])

		# put a user function in here!        
		self.userfunc(dataind)

		self.fig.canvas.draw()

	def userfunc(self,dataind):
		self.text.set_text('datapoint index selected: %d'%dataind)
		print 'No userfunc defined'
		pass
		