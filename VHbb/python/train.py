#!/usr/bin/env python
from optparse import OptionParser
import sys, re, os
import pickle
import ROOT 
ROOT.gROOT.SetBatch(True)
from array import array
#warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
#usage: ./train run gui



######## Turn of Eval #######
isEval = False
isEval = True

#CONFIGURE
argv = sys.argv
parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                          help="Verbose mode.")
parser.add_option("-T", "--training", dest="training", default="",
                      help="Training")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
parser.add_option("-S","--setting", dest="MVAsettings", default='',
                      help="Parameter setting string")
parser.add_option("-N","--name", dest="set_name", default='',
                      help="Parameter setting name. Output files will have this name")
parser.add_option("-L","--local",dest="local", default=True,
                      help="True to run it locally. False to run on batch system using config")

(opts, args) = parser.parse_args(argv)
if opts.config =="":
        opts.config = "config"

#Import after configure to get help message
from myutils import BetterConfigParser, mvainfo, ParseInfo, TreeCache

#load config
config = BetterConfigParser()
config.read(opts.config)
anaTag = config.get("Analysis","tag")
run = opts.training
gui = opts.verbose

print '-----> Input Training Sample(s): ', run

#GLOABAL rescale from Train/Test Spliiting:
global_rescale=2.

#get locations:
MVAdir      = config.get('Directories','vhbbpath')+'/data/'
samplesinfo = config.get('Directories','samplesinfo')

#systematics
systematics = config.get('systematics','systematics')
systematics = systematics.split(' ')

print '\n----> with Systematics:', systematics

weightF = config.get('Weights','weightF_bdt')
#weightF = config.get('Weights','weightF')

VHbbNameSpace = config.get('VHbbNameSpace','library')
ROOT.gSystem.Load(VHbbNameSpace)

#CONFIG
#factory
factoryname = config.get('factory','factoryname')
factorysettings = config.get('factory','factorysettings')

print 'factorysettings:', factorysettings

#MVA
MVAtype = config.get(run,'MVAtype')

#MVA name and settings. From local running or batch running different option
#print opts.local
if(eval(opts.local)):
	#print 'Local run'
	MVAname = run
	MVAsettings = config.get(run,'MVAsettings')

elif(opts.set_name!='' and opts.MVAsettings!=''):
	print 'Batch run'
	MVAname = opts.set_name
	MVAsettings = opts.MVAsettings
else :
	print 'Problem in configuration. Missing or inconsitent information Check input options'
	sys.exit()	
#print '@DEBUG: MVAname'
#print 'input : ' + opts.set_name
#print 'used : ' + MVAname

fnameOutput = MVAdir+factoryname+'_'+MVAname+'.root'
print '-----> Output File: ', fnameOutput

#locations
path = config.get('Directories','MVAin')

# Cuts
TCutname = config.get(run, 'treeCut')
TCut     = config.get('Cuts',TCutname)

#signals
signals = config.get(run,'signals')
signals = eval(signals)
print '\n -----> Training Signals: ', signals 

#backgrounds
backgrounds = config.get(run,'backgrounds')
backgrounds = eval(backgrounds)
print '\n -----> Training Backgrounds: ', backgrounds



treeVarSet  = config.get(run,'treeVarSet')
#print '\n -----> Training Features: ', treeVarSet
        
#variables
#TreeVar Array
MVA_Vars={}
MVA_Vars['Nominal']=config.get(treeVarSet,'Nominal')
MVA_Vars['Nominal']=MVA_Vars['Nominal'].split(' ')    

#Infofile
info = ParseInfo(samplesinfo,path)

#Workdir
workdir=ROOT.gDirectory.GetPath()

# Test and Train event cuts
TrainCut= TCut +' & evt%2==0'
EvalCut = TCut +' & evt%2!=0'

#TrainCut= TCut +' & !((evt%2)==0)'
#EvalCut = TCut +' & (evt%2)==0'

cuts = [TrainCut,EvalCut]  

print '\n ------> with Train Cuts: ', TrainCut
print '                Test Cuts : ', EvalCut

samples = []
samples = info.get_samples(signals+backgrounds)
tc = TreeCache(cuts,samples,path,config)

output = ROOT.TFile.Open(fnameOutput, "RECREATE")

print '\n\t>>> READING EVENTS <<<\n'

signal_samples = info.get_samples(signals)
background_samples = info.get_samples(backgrounds)

#TRAIN trees
Tbackgrounds = []
TbScales = []
Tsignals = []
TsScales = []
#EVAL trees
Ebackgrounds = []
EbScales = []
Esignals = []
EsScales = []

#load trees
for job in signal_samples:
    	
    print '\tREADING IN %s AS SIG'%job.name
    
    Tsignal = tc.get_tree(job,TrainCut)
    ROOT.gDirectory.Cd(workdir)
    TsScale = tc.get_scale(job,config)*global_rescale
    Tsignals.append(Tsignal)
    TsScales.append(TsScale)
    if isEval: 
	    Esignal = tc.get_tree(job,EvalCut)
	    Esignals.append(Esignal)
	    EsScales.append(TsScale)
	    print '\t\t\tEval %s events'%Esignal.GetEntries()
    print '\t\t\tTraining %s events'%Tsignal.GetEntries()
    

for job in background_samples:

    print '\tREADING IN %s AS BKG'%job.name
    
    Tbackground = tc.get_tree(job,TrainCut)
    ROOT.gDirectory.Cd(workdir)
    TbScale = tc.get_scale(job,config)*global_rescale
    Tbackgrounds.append(Tbackground)
    TbScales.append(TbScale)
    if isEval:
	    Ebackground = tc.get_tree(job,EvalCut)
	    Ebackgrounds.append(Ebackground)
	    EbScales.append(TbScale)
	    print '\t\t\tEval %s events'%Ebackground.GetEntries()
    ROOT.gDirectory.Cd(workdir)
    print '\t\t\tTraining %s events'%Tbackground.GetEntries()
    
            

factory = ROOT.TMVA.Factory(factoryname, output, factorysettings)

print 'factorysettings: ', factorysettings

#set input trees
for i in range(len(Tsignals)):
	factory.AddSignalTree(Tsignals[i], TsScales[i], ROOT.TMVA.Types.kTraining)
	if isEval: factory.AddSignalTree(Esignals[i], EsScales[i], ROOT.TMVA.Types.kTesting)


for i in range(len(Tbackgrounds)):
    if (Tbackgrounds[i].GetEntries()>0):
	    factory.AddBackgroundTree(Tbackgrounds[i], TbScales[i], ROOT.TMVA.Types.kTraining)

    if isEval:
	    if (Ebackgrounds[i].GetEntries()>0):
		    factory.AddBackgroundTree(Ebackgrounds[i], EbScales[i], ROOT.TMVA.Types.kTesting)
        
for var in MVA_Vars['Nominal']:
	factory.AddVariable(var,'D') # add the variables

# Execute TMVA
#weightF = '1'


factory.SetSignalWeightExpression(weightF)
factory.SetBackgroundWeightExpression(weightF)

print '-----> Booking TMVA: '
print '          Type: ', MVAtype
print '          Name: ', MVAname
print '          Settings: ', MVAsettings

factory.BookMethod(MVAtype, MVAname, MVAsettings)
factory.TrainAllMethods()
factory.TestAllMethods()

if isEval: 
	factory.EvaluateAllMethods()

#output.Write()
output.Close()


# #Execute TMVA
# print 'Execute TMVA: SetSignalWeightExpression'
# factory.SetSignalWeightExpression(weightF)
# print 'Execute TMVA: SetBackgroundWeightExpression'
# factory.SetBackgroundWeightExpression(weightF)
# factory.Verbose()
# print 'Execute TMVA: factory.BookMethod'
# my_methodBase_bdt = factory.BookMethod(MVAtype,MVAname,MVAsettings)
# print 'Execute TMVA: TrainMethod'
# my_methodBase_bdt.TrainMethod()
# #factory.TrainAllMethods()
# print 'Execute TMVA: TestAllMethods'
# factory.TestAllMethods()
# print 'Execute TMVA: EvaluateAllMethods'
# factory.EvaluateAllMethods()
# print 'Execute TMVA: output.Write'
# output.Write()

# output.cd('Method_%s'%MVAtype)
# #ROOT.gDirectory.ls()
# ROOT.gDirectory.cd(MVAname)

# rocIntegral_default=my_methodBase_bdt.GetROCIntegral()
# roc_integral_test = my_methodBase_bdt.GetROCIntegral(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_B'))
# roc_integral_train = my_methodBase_bdt.GetROCIntegral(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_B'))

# #significance = my_methodBase_bdt.GetSignificance()
# #separation_test = my_methodBase_bdt.GetSeparation(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_B'))
# #separation_train = my_methodBase_bdt.GetSeparation(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_B'))
# #ks_signal = (ROOT.gDirectory.Get(my_methodBase_bdtname+'_'+MVAname+'_S')).KolmogorovTest(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_S'))
# #ks_bkg= (ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_B')).KolmogorovTest(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_B'))


# print '@DEBUG: ROC TEST Integral   :', roc_integral_test
# print '@DEBUG: ROC TRAIN Integral  :', roc_integral_train

# #myROC = my_methodBase_bdt.GetIntegral(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_rejBvsS'))

# #print '@DEBUG: ROC TEst NEW:', myROC

# # Now save this ROC into a text file
# f = open('roc_temp.txt', 'a')	
# f.write("%s\n" % roc_integral_test)
# f.close()




#print '@LOG: ROC integral using signal and background'
#print roc_integral_test
#print '@LOG: ROC integral using train signal and background'
#print roc_integral_train
#print '@LOG: ROC integral ratio (Test/Train)'
#print roc_integral_test/roc_integral_train
#print '@LOG: Significance'
#print significance
#print '@LOG: Separation for test sample'
#print separation_test
#print '@LOG: Separation for test train'
#print separation_train
#print '@LOG: Kolmogorov test on signal'
#print ks_signal
#print '@LOG: Kolmogorov test on background'
#print ks_bkg



#WRITE INFOFILE
infofile = open(MVAdir+factoryname+'_'+MVAname+'.info','w')
print '@DEBUG: output infofile name'
print infofile

info=mvainfo(MVAname)
info.factoryname=factoryname
info.factorysettings=factorysettings
info.MVAtype=MVAtype
info.MVAsettings=MVAsettings
info.weightfilepath=MVAdir
info.path=path
info.varset=treeVarSet
info.vars=MVA_Vars['Nominal']
pickle.dump(info,infofile)
infofile.close()

print '\n-----> Output File: ', fnameOutput





# Open the GUi
#temp_string = 'root -l ../src/TMVAGui.C\(\"test.root\"\)'
#print 'Test:',temp_string
#os.system('root -l ../src/TMVAGui.C\(\"test.root\"\)')
	  
#gui = True
if gui == True: 
	
    ROOT.gROOT.ProcessLine( ".L ../src/TMVAGui.C")
    ROOT.gROOT.ProcessLine( "TMVAGui(\"%s\")" % fnameOutput )
    ROOT.gApplication.Run() 
    







#  LocalWords:  MVAname
