
#!/usr/bin/env python

from ROOT import *
from optparse import OptionParser
import sys
import numpy as np
import os
import multiprocessing
from myutils import BetterConfigParser, TdrStyles, getRatio
import ConfigParser
import ROOT
from ROOT import gROOT


## Usage: python addSOverBWeight.py [inputntuple] [outputntuple]
## Adds a branch, "sb_weight", with the per-event S/S+B weight for
## the events corresponding bin in the SR BDT Score distribution
## To be applied to all MC and data.

#ROOT.gSystem.SetBatch(True)


# ========================================
argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
config = BetterConfigParser()
config.read(opts.config)

outpath = '/afs/cern.ch/user/d/dcurry/www/TEST/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath

os.system(temp_string2)
os.system(temp_string3)

ROOT.gSystem.Load('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/interface/VHbbNameSpace_h.so')

# =========================================

# sample prefix
prefix = 'v25_'

inpath = '/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/SoverB_out/'

config = BetterConfigParser()
config.read('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/python/13TeVconfig/general')
config.read('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/python/13TeVconfig/cuts')

#signal_region_cut =  eval(config.get('Cuts','bdt_high_Zpt'))
signal_region_cut = '(Vtype_new==1 | Vtype_new==0) & Vtype_new > -1 & Vtype_new < 2 & Jet_btagCMVAV2[hJCMVAV2idx[0]] > -0.5884 & Jet_btagCMVAV2[hJCMVAV2idx[1]] > -0.5884 & V_mass>75. & V_mass < 105. & V_pt < 2000. & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt > 150.& H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt < 2000. & Jet_puId[hJCMVAV2idx[0]] >= 4 & Jet_puId[hJCMVAV2idx[1]] >= 4 & (((Vtype_new==1) & vLeptons_relIso03[0] < 0.15 & vLeptons_relIso03[1] < 0.15 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.0) || ((Vtype_new==0) & vLeptons_relIso04[0] < 0.25 & vLeptons_relIso04[1] < 0.25 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.)) & V_pt > -25.0 & HCMVAV2_reg_mass < 150. & HCMVAV2_reg_mass > 90. & Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20.'

#event_weight = eval(config.get('Weights','weightF_bdt'))
event_weight ='sign(genWeight)*puWeight*bTagWeightCMVAv2_Moriond[0]*((Vtype_new == 1)*eId90SFWeight[0]*eTrackerSFWeight[0]*eTrigSFWeight_doubleEle80x[0] + (Vtype_new == 0)*mIdSFWeight[0]*mIsoSFWeight[0]*mTrackerSFWeight[0]*mTrigSFWeight_doubleMu80x[0])'

#print 'Signal Region:', signal_region_cut
#print 'event weight:', event_weight

var = "gg_plus_ZH125_highZpt.Nominal" # variable to use to categorize by S/B
xmin = -1.0
xmax = 1.0


# print '\nCreating TChains...'
# # input for calculating S / S+B weight.  I have merged DY into one file. ZH and ttbar are as is.
# tree_weight_BKG = TChain("tree")
# tree_weight_BKG.Add(inpath+prefix+'DY_inclusive.root')
# tree_weight_BKG.Add(inpath+prefix+'DY_100to200.root')
# tree_weight_BKG.Add(inpath+prefix+'DY_200to400.root')
# tree_weight_BKG.Add(inpath+prefix+'DY_400to600.root')
# tree_weight_BKG.Add(inpath+prefix+'DY_600to800_ext1.root')
# #tree_weight_BKG.Add(inpath+prefix+'DY_Bjets.root')
# #tree_weight_BKG.Add(inpath+prefix+'DY_BgenFilter.root')
# tree_weight_BKG.Add(inpath+prefix+'ttbar.root')
# tree_weight_BKG.Add(inpath+prefix+'ZZ_2L2Q_ext1.root')
# tree_weight_BKG.Add(inpath+prefix+'ST_s.root')
# tree_weight_BKG.Add(inpath+prefix+'ST_tW_antitop.root')
# tree_weight_BKG.Add(inpath+prefix+'WZ.root')

# tree_weight_SIG = TChain("tree")
# tree_weight_SIG.Add(inpath+prefix+'ZH125.root')
# tree_weight_SIG.Add(inpath+prefix+'ggZH125.root')

# #binedges = [-1.,    -0.886, -0.746, -0.606, -0.466, -0.326, -0.186, -0.046,  0.094,  0.234,  0.374,  0.514,  0.654,  0.794,  0.934,  1.   ] 
# #binedge_array = numpy.zeros(len(binedges),dtype=float)
# #for i in range(len(binedges)):
# #    binedge_array[i] = binedges[i]

# hSig = TH1F("hSig","hSig", 15, -1, 1)
# hBkg = TH1F("hBkg","hBkg", 15, -1, 1)

# print '\nDrawing Weight Histograms...'
# tree_weight_SIG.Draw("%s>>hSig" %var,"((%s)*(%s))" % (signal_region_cut,event_weight))
# tree_weight_BKG.Draw("%s>>hBkg" %var,"((%s)*(%s))" % (signal_region_cut,event_weight))

# Import BDT outPut distributiuons and create 2 histograms: sum of signal and background
file = TFile.Open('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/ZllHbb_SR_Datacards_ChannelDecorrelatedBtag_5_1/vhbb_TH_BDT_Zuu_HighPt.root', 'read')
file.cd('ZuuHighPt_13TeV')

#BKG
Z2b     = gDirectory.Get('Zj2b')
Z1b     = gDirectory.Get('Zj1b')
Zlight  = gDirectory.Get('Zj0b')
ttbar   = gDirectory.Get('TT')
VVHF    = gDirectory.Get('VVHF')
VVLF    = gDirectory.Get('VVLF')

Z2b.Add(Z1b)
Z2b.Add(Zlight)
Z2b.Add(ttbar)
Z2b.Add(VVHF)
Z2b.Add(VVLF)

#SIG
ZH125   = gDirectory.Get('ZH_hbb')
ggZH125 = gDirectory.Get('ggZH_hbb')
ZH125.Add(ggZH125)

# create arrays of bin content
bkg_BDT = [Z2b.GetBinContent(ibin) for ibin in range(1,16)] 
sig_BDT = [ZH125.GetBinContent(ibin) for ibin in range(1,16)]

bin_list = [x for x in np.linspace(-1,1,15)]

print bin_list
print bkg_BDT
print sig_BDT

# List of files to add btag weights to
bkg_list = ['ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

DY_list = ['DY_600to800_ext1', 'DY_600to800_ext2','DY_600to800_ext3','DY_600to800_ext4','DY_600to800_ext5', 'DY_600to800_ext6',
           'DY_Bjets_Vpt100to200','DY_Bjets_Vpt200toInf',
           ]

ST_list = ['ST_s', 'ST_tW_top', 'ST_tW_antitop', 'ST_t_antitop']

file_list = bkg_list + data_list + signal_list + DY_list + ST_list

file_list1 = ST_list + ['WZ','DY_Bjets','DY_inclusive', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'DY_1200to2500', 'DY_2500toInf',
                        'DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_800to1200_ext1','DY_800to1200_ext2',
                        'DY_Bjets_Vpt100to200_ext2', 'DY_Bjets_Vpt200toInf_ext2']

file_list2 = DY_list + signal_list + ['ttbar']

#for file in file_list:
def osSystem(file):

    print '\nAdding S/S+B weights to sample:', inpath+prefix+file+'.root'
    print 'Output File                  :', outpath+prefix+file+'.root'

    ifile = ROOT.TFile.Open(inpath+prefix+file+'.root', 'read')
    ofile = ROOT.TFile(outpath+prefix+file+'.root', 'recreate')

    ifile.cd()

    tree = ifile.Get('tree')
    
    #tree = ifile.Get('tree/gg_plus_ZH125_highZpt')
    
    print 'Tree:', tree

    #for entry in tree:
    #    print entry.Nominal
        

    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        ifile.cd()
        obj = key.ReadObj()
        if obj.GetName() == 'tree':
            continue
        ofile.cd()
        obj.Write(key.GetName())

    ofile.cd()

    otree = tree.CloneTree(0)

    sb_weight = np.zeros(1,dtype=float)
    otree.Branch("sb_weight",sb_weight,"sb_weight/D")

    tree.SetBranchStatus('gg_plus_ZH125_lowZpt', 0)

    #for entry in tree:
    #    print '\nNew Entry:', entry
    #    print entry.Nominal

        
    
    nentries = tree.GetEntries()
    print "total entries: %i " % nentries
    for ientry in range(nentries):
        
        if (ientry % 10000 == 0): 
            print "processing entry: %i" % ientry
            
        #if ientry > 1000: continue
            
        tree.GetEntry(ientry)
        
        val = otree.Nominal
        
        #print val
        val_bin = min(range(len(bin_list)), key=lambda i: abs(bin_list[i]-val))
        #print '\nBin Number of BDT Score:', val_bin
        
        s = sig_BDT[val_bin]
        b = bkg_BDT[val_bin]
        sb_weight[0] = s / (s+b)
        
        #print s,b
        
        otree.Fill()

    #otree.Write()
    otree.AutoSave()
    ofile.Close()
    ifile.Close()
    print 'Finished...'    



p = multiprocessing.Pool()
results = p.imap(osSystem, file_list1)
p.close()
p.join()

p = multiprocessing.Pool()
results = p.imap(osSystem, file_list2)
p.close()
p.join()


# plot weights for validity checks
# canv = TCanvas("canv","canv")
# hTot = ZH125.Clone()
# hTot.Add(Z2b)
# ZH125.Divide(hTot) # S / S+B
# ZH125.Draw("hist")
# canv.SaveAs("sb_weights.pdf")
# canv.SetLogy(True)
# canv.SaveAs("sb_weights_log.pdf")




