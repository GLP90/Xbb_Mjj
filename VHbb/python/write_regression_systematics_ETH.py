#!/usr/bin/env python
import sys
import os,subprocess
import ROOT
import math
import shutil
from array import array
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
ROOT.gROOT.SetBatch(True)
from optparse import OptionParser

#usage: ./write_regression_systematic.py path

#os.mkdir(path+'/sys')
argv = sys.argv
parser = OptionParser()
#parser.add_option("-P", "--path", dest="path", default="",
#                      help="path to samples")
parser.add_option("-S", "--samples", dest="names", default="",
                                        help="samples you want to run on")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                                        help="configuration defining the plots to make")
(opts, args) = parser.parse_args(argv)
if opts.config =="":
    opts.config = "config"
    
from myutils import BetterConfigParser, ParseInfo, TreeCache
    
print opts.config
config = BetterConfigParser()
config.read(opts.config)
anaTag = config.get("Analysis","tag")
TrainFlag = eval(config.get('Analysis','TrainFlag'))
btagLibrary = config.get('BTagReshaping','library')
samplesinfo=config.get('Directories','samplesinfo')

VHbbNameSpace=config.get('VHbbNameSpace','library')
ROOT.gSystem.Load(VHbbNameSpace)
AngLikeBkgs=eval(config.get('AngularLike','backgrounds'))
ang_yield=eval(config.get('AngularLike','yields'))

#path=opts.path
pathIN = config.get('Directories','SYSin')
pathOUT = config.get('Directories','SYSout')
tmpDir = os.environ["TMPDIR"]

print 'INput samples:\t%s'%pathIN
print 'OUTput samples:\t%s'%pathOUT


#storagesamples = config.get('Directories','storagesamples')


namelist=opts.names.split(',')

#load info
info = ParseInfo(samplesinfo,pathIN)

def deltaPhi(phi1, phi2):
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result

def addAdditionalJets(H, tree):
    for i in range(tree.nhjidxaddJetsdR08):
        idx = tree.hjidxaddJetsdR08[i]
        if (idx == tree.hJCidx[0]) or (idx == tree.hJCidx[1]): continue
        addjet = ROOT.TLorentzVector()
        addjet.SetPtEtaPhiM(tree.Jet_pt[idx],tree.Jet_eta[idx],tree.Jet_phi[idx],tree.Jet_mass[idx])
        H = H + addjet
        return H
    
def resolutionBias(eta):
    if(eta< 0.5): return 0.052
    if(eta< 1.1): return 0.057
    if(eta< 1.7): return 0.096
    if(eta< 2.3): return 0.134
    if(eta< 5): return 0.28
    return 0

def corrPt(pt,eta,mcPt):
    return 1 ##FIXME
#    return (pt+resolutionBias(math.fabs(eta))*(pt-mcPt))/pt

def corrCSV(btag,  csv, flav):
    if(csv < 0.): return csv
    if(csv > 1.): return csv;
    if(flav == 0): return csv;
    if(math.fabs(flav) == 5): return  btag.ib.Eval(csv)
    if(math.fabs(flav) == 4): return  btag.ic.Eval(csv)
    if(math.fabs(flav) != 4  and math.fabs(flav) != 5): return  btag.il.Eval(csv)
    return -10000


def csvReshape(sh, pt, eta, csv, flav):
    return sh.reshape(float(eta), float(pt), float(csv), int(flav))


for job in info:
    if not job.name in namelist: continue
    ROOT.gROOT.ProcessLine(
        "struct H {\
        int         HiggsFlag;\
        float         mass;\
        float         pt;\
        float         eta;\
        float         phi;\
        float         dR;\
        float         dPhi;\
        float         dEta;\
        } ;"
        )
    if anaTag == '7TeV':
        ROOT.gSystem.Load(btagLibrary)
        from ROOT import BTagShape
        btagNom = BTagShape("../data/csvdiscr.root")
        btagNom.computeFunctions()
        btagUp = BTagShape("../data/csvdiscr.root")
        btagUp.computeFunctions(+1.,0.)
        btagDown = BTagShape("../data/csvdiscr.root")
        btagDown.computeFunctions(-1.,0.)
        btagFUp = BTagShape("../data/csvdiscr.root")
        btagFUp.computeFunctions(0.,+1.)
        btagFDown = BTagShape("../data/csvdiscr.root")
        btagFDown.computeFunctions(0.,-1.)
    else:
        ROOT.gSystem.Load(btagLibrary)
        from ROOT import BTagShapeInterface
        btagNom = BTagShapeInterface("../data/csvdiscr.root",0,0)
        btagUp = BTagShapeInterface("../data/csvdiscr.root",+1,0)
        btagDown = BTagShapeInterface("../data/csvdiscr.root",-1,0)
        btagFUp = BTagShapeInterface("../data/csvdiscr.root",0,+1.)
        btagFDown = BTagShapeInterface("../data/csvdiscr.root",0,-1.)
        
    lhe_weight_map = False if not config.has_option('LHEWeights', 'weights_per_bin') else eval(config.get('LHEWeights', 'weights_per_bin'))
        
        
    print '\t - %s' %(job.name)
    print('opening '+pathIN+'/'+job.prefix+job.identifier+'.root')
    input = ROOT.TFile.Open(pathIN+'/'+job.prefix+job.identifier+'.root','read')
    output = ROOT.TFile.Open(tmpDir+'/'+job.prefix+job.identifier+'.root','recreate')
    print
    print "Writing: ",tmpDir+'/'+job.prefix+job.identifier+'.root'
    print
    
    input.cd()
    
    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        if obj.GetName() == job.tree:
            continue
        output.cd()
        obj.Write(key.GetName())
        
                                                                 input.cd()
                                                                     tree = input.Get(job.tree)
                                                                         nEntries = tree.GetEntries()

                                                                                     H = ROOT.H()
                                                                                         HNoReg = ROOT.H()
                                                                                             HaddJetsdR08 = ROOT.H()
                                                                                                 HaddJetsdR08NoReg = ROOT.H()
    
    


  
