#!/usr/bin/env python
from __future__ import print_function
import sys
import os,subprocess
import ROOT 
from array import array
from math import sqrt
from copy import copy
#suppres the EvalInstace conversion warning bug
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
from optparse import OptionParser
import pickle


print ('\n ========== Evaluating BDT Classifier ===========\n')

#CONFIGURE 
ROOT.gROOT.SetBatch(True)
argv = sys.argv
parser = OptionParser()
parser.add_option("-U", "--update", dest="update", default=0,
                      help="update infofile")
parser.add_option("-D", "--discr", dest="discr", default="",
                      help="discriminators to be added")
parser.add_option("-S", "--samples", dest="names", default="",
                      help="samples you want to run on")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)

if opts.config =="":
        opts.config = "config"

#Import after configure to get help message
from myutils import BetterConfigParser, progbar, printc, ParseInfo, MvaEvaluator

config = BetterConfigParser()
config.read(opts.config)
anaTag = config.get("Analysis","tag")

#get locations:
Wdir = config.get('Directories','Wdir')
samplesinfo = config.get('Directories','samplesinfo')

#systematics
INpath  = config.get('Directories','MVAin')
OUTpath = config.get('Directories','MVAout')

#read shape systematics
systematics=config.get('systematics','systematics')

info = ParseInfo(samplesinfo,INpath)

arglist = opts.discr #RTight_blavla,bsbsb

namelistIN = opts.names
namelist   = namelistIN.split(',')
print ('\n-----> SampleList: ', namelist)

MVAlist = arglist.split(',')
print ('-----> MVAList:', MVAlist)

#CONFIG
#factory
factoryname = config.get('factory','factoryname')

# unique training name
name = config.get('MVAGeneral','name') 

#load the namespace
VHbbNameSpace = config.get('VHbbNameSpace','library')
ROOT.gSystem.Load(VHbbNameSpace)

#MVA
MVAinfos = []
MVAdir = config.get('Directories','vhbbpath')+'/python/weights/'
MVAInfodir = config.get('Directories','vhbbpath')+'/data/'
for MVAname in MVAlist: 
    MVAinfofile = open(MVAInfodir+factoryname+'_'+MVAname+'.info','r')
    print ('\n-----> Opening MVA Info file: ', MVAinfofile)
    MVAinfos.append(pickle.load(MVAinfofile))
    MVAinfofile.close()
    
longe = 40
workdir = ROOT.gDirectory.GetPath()

# Acess the weight XML files
theMVAs = []
for mva in MVAinfos:
	theMVAs.append(MvaEvaluator(config, mva))

samples = info.get_samples(namelist)
#tmpDir = os.environ["TMPDIR"]
for job in samples:

    print ('\n-----> Input Sample: ', INpath+'/'+job.prefix+job.identifier+'.root')
    input = ROOT.TFile.Open(INpath+'/'+job.prefix+job.identifier+'.root','read')

    print ('\n-----> Output Sample: ', OUTpath+'/'+job.prefix+job.identifier+'.root')
    outfile = ROOT.TFile.Open(OUTpath+'/'+job.prefix+job.identifier+'.root','recreate')
    
    input.cd()
    obj = ROOT.TObject

    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        if obj.GetName() == job.tree:
		continue
        outfile.cd()
        obj.Write(key.GetName())

    tree = input.Get(job.tree)
    nEntries = tree.GetEntries()
    outfile.cd()
    newtree = tree.CloneTree(0)
            
    #Set branch address for all vars
    for i in range(0,len(theMVAs)):
        theMVAs[i].setVariables(tree,job)

    outfile.cd()

    #Setup Branches
    mvaVals=[]
    for i in range(0,len(theMVAs)):
        if job.type == 'Data':
            mvaVals.append(array('f',[0]))
            newtree.Branch(MVAinfos[i].MVAname,mvaVals[i],'Nominal/F') 
        else:
            mvaVals.append(array('f',[0]*len(systematics.split())))
	    newtree.Branch(theMVAs[i].MVAname,mvaVals[i],':'.join(systematics.split())+'/F')
            #mvaVals.append(array('f',[0]*21))
	    #newtree.Branch(theMVAs[i].MVAname,mvaVals[i],'Nominal:JER_up:JER_down:JES_up:JES_down:JER_up_high:JER_down_high:JER_up_low:JER_down_low:JER_up_central:JER_down_central:JER_up_forward:JER_down_forward:JEC_up_high:JEC_down_high:JEC_up_low:JEC_down_low:JEC_up_central:JEC_down_central:JEC_up_forward:JEC_down_forward/F')
        MVA_formulas_Nominal = []
     
    # Fill event by event:
    for entry in range(0,nEntries):

	if entry%10000 == 0: print ('----> Entry # ', entry)
	    
        tree.GetEntry(entry)
                            
        for i in range(0,len(theMVAs)):
		
		theMVAs[i].evaluate(mvaVals[i],job)

        newtree.Fill()
	
    newtree.AutoSave()
    outfile.Write()
    outfile.Close()
    
    # Save the File
    #targetStorage = OUTpath.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')+'/'+job.prefix+job.identifier+'.root'
    #command = 'lcg-del -b -D srmv2 -l %s' %(targetStorage)
    #print(command)
    #subprocess.call([command], shell=True)
    #command = 'lcg-cp -b -D srmv2 file:///%s %s' %(tmpDir+'/'+job.prefix+job.identifier+'.root',targetStorage)
    #print(command)
    #subprocess.call([command], shell=True)
                

