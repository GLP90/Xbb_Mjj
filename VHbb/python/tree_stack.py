#!/usr/bin/env python

import pickle
import ROOT 
from collections import Counter
from array import array
import sys, os
from optparse import OptionParser
from copy import copy,deepcopy
from math import sqrt
ROOT.gROOT.SetBatch(True)
import numpy as np
from multiprocessing import Process, Lock
from time import sleep

# Punzi Significance Function

def punzi(signal, bkg):

	return signal / (1.5 + sqrt(bkg) + 0.2*bkg) 


def sampling_error(signal, bkg):

	return sqrt( (signal/(signal+bkg))*(1-(signal/(signal+bkg))) / (signal+bkg))

def counting_error(num):

	return np.sqrt(1/num)


#CONFIGURE
argv = sys.argv
parser = OptionParser()
parser.add_option("-R", "--region", dest="region", default="",
                      help="region to plot")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")

parser.add_option("-B", "--batch", dest="batch", default="False",
		  help="Batch Mode")

(opts, args) = parser.parse_args(argv)
if opts.config =="":
        opts.config = "config"

        
from myutils import BetterConfigParser, printc, ParseInfo, mvainfo, StackMaker, HistoMaker


#opts.config.append('13TeVconfig/vhbbPlotDef.ini')
#print 'Plot Config List: ',opts.config

config = BetterConfigParser()
config.read(opts.config)

#path = opts.path
region = opts.region

batch = opts.batch
print batch
# additional blinding cut:
addBlindingCut = None
if config.has_option('Plot_general','addBlindingCut'):
    addBlindingCut = config.get('Plot_general','addBlindingCut')
    print 'adding add. blinding cut'

#get locations:
Wdir=config.get('Directories','Wdir')

# the samples_nosplit.cfg file in 13TeV
samplesinfo=config.get('Directories','samplesinfo')

# which directory to take the samples from(sys_out currently)
path = config.get('Directories','plottingSamples')


# Add external macros
# For batch jobs lock the compliation
#lock = Lock()
#sleep(np.random.rand(1,1)*120) 
#lock.acquire()
#ROOT.gSystem.CompileMacro("../plugins/PU.C")
#lock.release()


#if os.path.exists("../interface/VHbbNameSpace_h.so"):
#print 'ROOT.gROOT.LoadMacro("../interface/VHbbNameSpace_h.so")'
#ROOT.gROOT.LoadMacro("../interface/VHbbNameSpace_h.so")

section='Plot:%s'%region

info = ParseInfo(samplesinfo, path)

print '----> Making Plots: ', region, ' from directory: ', path	



#----------Histo from trees------------
def doPlot():

	vars = (config.get(section, 'vars')).split(',')
	data = config.get(section,'Datas')
	mc = eval(config.get('Plot_general','samples'))
	
	print '  with Vars:', vars
	print '  Using MC samples: ', mc
	print '  and Data samples: ', data

	# Is set in plots.  Can be the mass of ZH/ggZH.
	SignalRegion = False
	if config.has_option(section,'Signal'):
		mc.append(config.get(section,'Signal'))
		SignalRegion = True

	#print '\n\n\t\t=====SignalRegion:', SignalRegion	
            
	datasamples = info.get_samples(data)
	mcsamples = info.get_samples(mc)

	GroupDict = eval(config.get('Plot_general','Group'))
	
        #GETALL AT ONCE
	options = []
	Stacks  = []
	for i in range(len(vars)):
		Stacks.append(StackMaker(config, vars[i], region, SignalRegion))
		options.append(Stacks[i].options)

        # Init the HistoMaker class
	Plotter = HistoMaker(mcsamples+datasamples, path, config, options, GroupDict)

        #print '\nProducing Plot of %s\n'%vars[v]
	Lhistos = [[] for _ in range(0,len(vars))]
	Ltyps = [[] for _ in range(0,len(vars))]
	Ldatas = [[] for _ in range(0,len(vars))]
	Ldatatyps = [[] for _ in range(0,len(vars))]
	Ldatanames = [[] for _ in range(0,len(vars))]

        #Find out Lumi:
	lumicounter=0.
	lumi=0.
	for job in datasamples:
		lumi+=float(job.lumi)
		lumicounter+=1.

	if lumicounter > 0:
		lumi=lumi/lumicounter

	print '\n\t\t Luminosity Auto Calculation: ', lumi	

	# temp hack	
	#lumi = 3000.	
	Plotter.lumi=lumi
	mass = Stacks[0].mass
	

	# Define the counters for statistics counting
	mass_count = Counter()
	bdt_count  = Counter() 


	for job in mcsamples:

		# hDictList returns list of TH1Fs of the specified vars to plot
		if addBlindingCut:
			hDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
		else:
			hDictList = Plotter.get_histos_from_tree(job)

		#print '\n\n\t\tJob name: ', job.name	
		if job.name == 'ZH125':
        		#or job.name == 'ggZH125':
			Overlaylist = deepcopy([hDictList[v].values()[0] for v in range(0,len(vars))])
			
		for v in range(0,len(vars)):
			Lhistos[v].append(hDictList[v].values()[0])
			Ltyps[v].append(hDictList[v].keys()[0])
			hist = hDictList[v].values()[0]
			
		# end variable loop	
	# end MC sample loop	

	# Loop over data 	
	for job in datasamples:
		
		# temp hack to turn off data
		#break
		
		#hTemp, typ = Plotter.get_histos_from_tree(job)
		if addBlindingCut:
			dDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
		else:
			dDictList = Plotter.get_histos_from_tree(job)
			
		for v in range(0,len(vars)):
			Ldatas[v].append(dDictList[v].values()[0])
			Ldatatyps[v].append(dDictList[v].keys()[0])
			Ldatanames[v].append(job.name)

        # produce the final plots and save		
	for v in range(0,len(vars)):

		histos = Lhistos[v]
		typs = Ltyps[v]
		Stacks[v].histos = Lhistos[v]
		Stacks[v].typs = Ltyps[v]
		Stacks[v].datas = Ldatas[v]
		Stacks[v].datatyps = Ldatatyps[v]
		Stacks[v].datanames= Ldatanames[v]
		if SignalRegion:
			Stacks[v].overlay = Overlaylist[v]
		Stacks[v].lumi = lumi
		
		
		Stacks[v].doPlot()

		Stacks[v].overlay = []
		Stacks[v].histos = Lhistos[v]
		Stacks[v].typs = Ltyps[v]
		Stacks[v].datas = Ldatas[v]
		Stacks[v].datatyps = Ldatatyps[v]
		Stacks[v].datanames= Ldatanames[v]
		Stacks[v].normalize = True
		Stacks[v].options['pdfName'] = Stacks[v].options['pdfName'].replace('.pdf','_norm.pdf')
		#Stacks[v].doPlot()
		print 'i am done!\n'
#----------------------------------------------------
doPlot()
sys.exit(0)
