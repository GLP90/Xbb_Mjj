###############################################
#  Copy data_obs to mlfit.root
#
#
#
###############################################

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
import multiprocessing
import logging
from matplotlib import interactive
import ROOT

indir = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/limits/v24_ICHEP_VH_11_9_withRP_ICHEPweights/'

datacard_list = ['vhbb_TH_BDT_Zuu_LowPt.root', 'vhbb_TH_BDT_Zuu_HighPt.root', 'vhbb_TH_BDT_Zee_LowPt.root', 'vhbb_TH_BDT_Zee_HighPt.root']

#datacard_list = ['vhbb_TH_BDT_Zuu_HighPt.root']
#datacard_list = ['vhbb_TH_BDT_Zuu_LowPt.root']
#datacard_list = ['vhbb_TH_BDT_Zee_HighPt.root']
#datacard_list = ['vhbb_TH_BDT_Zee_LowPt.root']

fout = ROOT.TFile(indir+"mlfit.root","UPDATE")

print '\nOut File:', fout

for datacard in datacard_list:    

    infile = ROOT.TFile(indir+datacard,"READ")

    print '\nIn File:', infile

    if 'Zee_High' in datacard:
        hSR_data = infile.Get("ZeeHighPt_13TeV/data_obs")
    if 'Zuu_High' in datacard:
        hSR_data = infile.Get("ZuuHighPt_13TeV/data_obs")
    if 'Zuu_Low' in datacard:
        hSR_data = infile.Get("ZuuLowPt_13TeV/data_obs")
    if 'Zee_Low' in datacard:
        hSR_data = infile.Get("ZeeLowPt_13TeV/data_obs")
    
    #hSR_data = infile.Get("data_obs")
  
    print 'Data Obs:', hSR_data

    fit_list = ['prefit', 'fit_b', 'fit_s']
    
    if len(datacard_list) > 2:
        for fit in fit_list:
            if 'Zee_High' in datacard:
                fout.cd('shapes_'+fit+'/ch4_Zee_SIG_high')
                hSR_data.Write()
            if 'Zuu_High' in datacard:
                fout.cd('shapes_'+fit+'/ch3_Zmm_SIG_high')
                hSR_data.Write()
            if 'Zuu_Low' in datacard:
                fout.cd('shapes_'+fit+'/ch1_Zmm_SIG_low')
                hSR_data.Write()
            if 'Zee_Low' in datacard:
                fout.cd('shapes_'+fit+'/ch2_Zee_SIG_low')
                hSR_data.Write()

    else:
        for fit in fit_list:
            if 'Zee_High' in datacard:
                fout.cd('shapes_'+fit+'/Zee_SIG_high')
                hSR_data.Write()
            if 'Zuu_High' in datacard:
                fout.cd('shapes_'+fit+'/Zmm_SIG_high')
                hSR_data.Write()
            if 'Zuu_Low' in datacard:
                fout.cd('shapes_'+fit+'/Zmm_SIG_low')
                hSR_data.Write()
            if 'Zee_Low' in datacard:
                fout.cd('shapes_'+fit+'/Zee_SIG_low')
                hSR_data.Write()
            

    infile.Close()


fout.Close()
  

