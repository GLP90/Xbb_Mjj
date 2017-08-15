#!/usr/bin/env python
# ===================================================
# Python script to perform Kinematic Fit on Zll Higgs mass
#
#  !!!! Needs to be ran from python directory
#
# 2/15/2015 David Curry
# ===================================================


import sys
import os
import re
import fileinput
import subprocess
import shutil
from array import array
import numpy as np
from decimal import *
from matplotlib import interactive
from ROOT import *
from optparse import OptionParser
import math
from myutils import BetterConfigParser, ParseInfo


ROOT.gROOT.SetBatch(True)

# Import heppy configurations
argv = sys.argv
parser = OptionParser()
parser.add_option("-S", "--samples", dest="names", default="",
                                        help="samples you want to run on")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                                        help="configuration defining the plots to make")
(opts, args) = parser.parse_args(argv)
if opts.config =="":
            opts.config = "config"

config = BetterConfigParser()
config.read(opts.config)

samplesinfo = config.get('Directories','samplesinfo')

tmpDir = os.environ["TMPDIR"]

pathIN = config.get('Directories','SYSout')
pathOUT = config.get('Directories','SYSout')

name = config.get('TrainRegression', 'name') 

namelist = opts.names.split(',')

info = ParseInfo(samplesinfo,pathIN)

# Now load kinFit modules/namspaces
ROOT.gSystem.Load("libPhysicsToolsKinFitter.so")

KinFitNameSpace = ('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/interface/kinFitZll_h.so')
  
ROOT.gSystem.Load(KinFitNameSpace)

from ROOT import HZll

# Loop over files in sample path and apply kinfit to selcted file(name)
for job in info:
    if not job.name in namelist: continue
    
    print '\n----> Performing Kin Fit on Sample: ', job
    
    # make the input/output files
    #input  = TFile.Open(pathIN+'/'+job.prefix+job.identifier+name+'.root','read')
    #output = TFile.Open(pathOUT+'/'+job.prefix+job.identifier+name+'_kinFit.root','recreate')
    input  = TFile.Open('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET.root', 'read')
    output = TFile.Open('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_kinFit.root', 'recreate')
    
    print '\n----> Input : ' , input
    print '----> Output: ', output
    
    # Set the tree address
    input.cd()
    tree = input.Get(job.tree)
    nEntries = tree.GetEntries()
    print '----> tree  : ', tree
    
    # Keep the old pre kinFit mass
    output.cd()
    newtree = tree.CloneTree(0)
    
    H_mass_kf      = array('f',[0]*1)
    newtree.Branch('H_mass_kf', H_mass_kf, 'H_mass_kf[1]/F')
    

    print '\n\n======== Filling New Branches / Applying Kinematic Fit ========'

    for entry in range(0,nEntries):
        
        tree.GetEntry(entry)
        
        if entry % 10000 is 0: print 'Event #', entry

        # Init the kinFit Mass
        H_mass_kf[0] = -999
        
        # ==== Cuts =====
        if tree.nvLeptons < 2: continue
                                
        if tree.nJet < 2 : continue

        #if tree.Jet_pt[tree.hJCidx[0]] < 20 or tree.Jet_pt[tree.hJCidx[1]] < 20: continue
        
        
        # ==============
            
        #print '\n\n====== Event # ', entry,'======'
        #print ' vLeptons_pt[0] = ', tree.vLeptons_pt[0]
        #print ' vLeptons_pt[1] = ', tree.vLeptons_pt[1]
        #print ' hJets_pt[0]    = ', tree.hJets_pt[0]
        #print ' hJets_pt[1]    = ', tree.hJets_pt[1]
        #print ' hJets_eta[0]   = ', tree.hJets_eta[0]
        #print ' hJets_eta[1]   = ', tree.hJets_eta[1]
        #print ' hJets_phi[0]   = ', tree.hJets_phi[0]
        #print ' hJets_phi[1]   = ', tree.hJets_phi[1]
        #print ' hJets_mass[0]  = ', tree.hJets_mass[0]
        #print ' hJets_mass[1]  = ', tree.hJets_mass[1]
        
        
        # Init the TLorentz vectors.  Two Jets, Two Leptons
        hj0 = TLorentzVector()
        hj1 = TLorentzVector()
        hj0.SetPtEtaPhiM(tree.Jet_pt_reg[0],tree.Jet_eta[tree.hJCidx[0]],tree.Jet_phi[tree.hJCidx[0]],tree.Jet_mass_reg[0])
        hj1.SetPtEtaPhiM(tree.Jet_pt_reg[1],tree.Jet_eta[tree.hJCidx[1]],tree.Jet_phi[tree.hJCidx[1]],tree.Jet_mass_reg[1])
        
        
        hl0 = TLorentzVector()
        hl1 = TLorentzVector()
        hl0.SetPtEtaPhiM(tree.vLeptons_pt[0],tree.vLeptons_eta[0],tree.vLeptons_phi[0],tree.vLeptons_mass[0])
        hl1.SetPtEtaPhiM(tree.vLeptons_pt[1],tree.vLeptons_eta[1],tree.vLeptons_phi[1],tree.vLeptons_mass[1])
        
        # total transverse momentum
        Px = hj0.Px() + hl0.Px() + hj1.Px() + hl1.Px() + tree.met_pt*math.cos(tree.met_phi)
        Py = hj0.Py() + hl0.Py() + hj1.Py() + hl1.Py() + tree.met_pt*math.sin(tree.met_phi)
        
        # Send to the kinFitter
        Higgs = HZll.Xchi2(hl0, hl1, hj0, hj1, Px, Py)
        
        # get the Higgs mass
        H_mass_kf[0] = abs(Higgs.M())
        
        # test higgs mass
        #h_mass_test = HZll.chi2(hj0, hj1)

        '''
        print '\n======= KinFit Results ========'
        print 'Higgs Mass  : ', tree.H_mass
        print 'KinFit Mass : ', H_mass_kf
        print 'KF Test Mass: ', h_mass_test
        '''
        
        # fill the tree
        newtree.Fill()
        
    # end event loop

    newtree.AutoSave()
    output.Close()

# end sample loop


print '\n\n-----> Kinematic Fit has finished...'




