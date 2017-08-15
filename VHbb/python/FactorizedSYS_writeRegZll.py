
#!/usr/bin/env python
#from samplesclass import sample
#from printcolor import printc
import pickle
import sys
import os
import ROOT 
import math
import shutil
from collections import Counter
from ROOT import TFile, TMath
from ROOT import TXNetFile
from array import array
import warnings
from optparse import OptionParser
from ROOT import *
import numpy as np
import multiprocessing
ROOT.gROOT.SetBatch(True)


#====================================================

# Group JEC sys or individual
doGroup = False
#doGroup = True

# Print out
isVerbose = False
#isVerbose = True

# Make validation plots
doPlots = False
#doPlots = True

plotpath = '/afs/cern.ch/user/d/dcurry/www/v25_JEC_validation_withMET/'
try: os.system('mkdir '+plotpath)
except:print outpath+' already exists...'
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+plotpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+plotpath
os.system(temp_string2)
os.system(temp_string3)


inpath = '/exports/uftrig01a/dcurry/heppy/files/prep_out/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/jec_out/'

# List of files to add btag weights to
bkg_list = ['ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

DY_list = ['DY_inclusive', 'DY_100to200', 'DY_200to400', 'DY_400to600',
           'DY_Bjets',
           'DY_800to1200_ext1', 'DY_800to1200_ext2',
           'DY_600to800_ext1', 'DY_600to800_ext2','DY_600to800_ext3',
           'DY_Bjets_Vpt100to200', 'DY_Bjets_Vpt200toInf',
           'DY_Bjets_Vpt100to200_ext2', 'DY_Bjets_Vpt200toInf_ext2',
           'DY_1200to2500', 'DY_2500toInf',
           #'DY1J_10to50', 'DY2J_10to50', 'DY3J_10to50'
           ]


DY_parton_list = ['DY0J', 'DY1J']

ST_list = ['ST_s', 'ST_tW_top', 'ST_tW_antitop', 'ST_t_antitop']

prep_list = [
    #'prep_DY_2J', 'prep_DY_2J_NewExt1', 'prep_DY_2J_NewExt2', 'prep_DY_2J_NewExt3',
    #'prep_DY_2J_NewExt4', 'prep_DY_2J_NewExt5', 'prep_DY_2J_NewExt6', 'prep_DY_2J_NewExt7', 'prep_DY_2J_NewExt8']

    'prep_ttbar_ext1', 'prep_ttbar_ext2',
    'prep_ttbar_ext1_NewExt1', 'prep_ttbar_ext2_NewExt1',
    'prep_ttbar_ext1_NewExt2', 'prep_ttbar_ext2_NewExt2',
    'prep_ttbar_ext1_NewExt3', 'prep_ttbar_ext2_NewExt3',
    'prep_ttbar_ext1_NewExt4', 'prep_ttbar_ext2_NewExt4',
    'prep_ttbar_ext1_NewExt5', 'prep_ttbar_ext2_NewExt5',
    'prep_ttbar_ext1_NewExt6','prep_ttbar_ext1_NewExt7','prep_ttbar_ext1_NewExt8','prep_ttbar_ext1_NewExt9'
    ]

temp_list = ['WZ']

file_list  = temp_list

file_list1 = ST_list + ['WZ'] + data_list
file_list2 = signal_list + DY_list + ['ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'ttbar']


def addAdditionalJets(H, tree):
    for i in range(tree.nhjidxaddJetsdR08):
        idx = tree.hjidxaddJetsdR08[i]
        if (idx == tree.hJCidx[0]) or (idx == tree.hJCidx[1]): continue
        addjet = ROOT.TLorentzVector()
        addjet.SetPtEtaPhiM(tree.Jet_pt[idx],tree.Jet_eta[idx],tree.Jet_phi[idx],tree.Jet_mass[idx])
        H = H + addjet
    return H

def deltaPhi(phi1, phi2):
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result


def projectionMETOntoJet(met, metphi, jet, jetphi, onlyPositive=True, threshold = math.pi/4.0):

  deltaphi = deltaPhi(metphi, jetphi)
  met_dot_jet = met * jet * math.cos(deltaphi)
  jetsq = jet * jet
  projection = met_dot_jet / jetsq * jet

  if onlyPositive and abs(deltaphi) >= threshold:
      return 0.0
  else:
      return projection


#for file in file_list:
def osSystem(file):
    
    input  = TFile.Open(inpath+'/v25_'+file+'.root', 'read')
    output = TFile.Open(outpath+'/v25_'+file+'.root', 'recreate')
    
    #input  = TFile.Open(inpath+'/'+file+'.root', 'read')
    #output = TFile.Open(outpath+'/'+file+'.root', 'recreate')
    
    regWeight = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/myMacros/regression/forDavid/gravall-v25.weights.xml'
    #regWeight = '../myMacros/regression/forDavid/weights_zh/TMVARegression_BDTG.weights.xml'

    regVars = ["Jet_pt",
               "nPVs",
               "Jet_eta",
               "Jet_mt",
               "Jet_leadTrackPt",
               "Jet_leptonPtRel",
               "Jet_leptonPt",
               "Jet_leptonDeltaR",
               "Jet_neHEF",
               "Jet_neEmEF",
               "Jet_vtxPt",
               "Jet_vtxMass",
               "Jet_vtx3dL",
               "Jet_vtxNtrk",
               "Jet_vtx3deL"
               #"met_pt",
               #"Jet_met_proj"
               ]      	

    regDict = {"Jet_pt":"Jet_pt[hJCMVAV2idx[0]]",
               #"Jet_corr":"Jet_corr[hJCMVAV2idx[0]]"
               "nPVs":"nPVs",
               "Jet_eta":"Jet_eta[hJCMVAV2idx[0]]",
               "Jet_mt":"Jet_mt[hJCMVAV2idx[0]]",
               "Jet_leadTrackPt": "Jet_leadTrackPt[hJCMVAV2idx[0]]",
               "Jet_leptonPtRel":"Jet_leptonPtRel[hJCMVAV2idx[0]]",
               "Jet_leptonPt":"Jet_leptonPt[hJCMVAV2idx[0]]",
               "Jet_leptonDeltaR":"Jet_leptonDeltaR[hJCMVAV2idx[0]]",
               "Jet_neHEF":"Jet_neHEF[hJCMVAV2idx[0]]",
               "Jet_neEmEF":"Jet_neEmEF[hJCMVAV2idx[0]]",
               "Jet_vtxPt":"Jet_vtxPt[hJCMVAV2idx[0]]",
               "Jet_vtxMass":"Jet_vtxMass[hJCMVAV2idx[0]]",
               "Jet_vtx3dL":"Jet_vtx3dl[hJCMVAV2idx[0]]",
               "Jet_vtxNtrk":"Jet_vtxNtrk[hJCMVAV2idx[0]]",
               "Jet_vtx3deL":"Jet_vtx3deL[hJCMVAV2idx[0]]"
               #"met_pt":"met_pt",
               #"Jet_met_proj":"Jet_met_proj"
               } 

    if doGroup:
        JECsys = [
            "JER",
            "PileUp",
            "Relative",
            "AbsoluteMisc"
            ]

        JECsysGroupDict = {
            "PileUp": ["PileUpDataMC",
                       "PileUpPtRef",
                       "PileUpPtBB",
                       "PileUpPtEC1",
                       "PileUpPtEC2",
                       "PileUpPtHF"],
            "Relative": ["RelativeJEREC1",
                         "RelativeJEREC2",
                         "RelativeJERHF",
                         "RelativeFSR",
                         "RelativeStatFSR",
                         "RelativeStatEC",
                         "RelativeStatHF",
                         "RelativePtBB",
                         "RelativePtEC1",
                         "RelativePtEC2",
                         "RelativePtHF"],
            "AbsoluteMisc": [ "AbsoluteScale",
                              "AbsoluteMPFBias",
                              "AbsoluteStat",
                              "SinglePionECAL",
                              "SinglePionHCAL",
                              "Fragmentation",
                              "TimePtEta",
                              "FlavorQCD"]
            }


    else:
        JECsys = [ 
            "JER",
            
            "PileUpDataMC",
            "PileUpPtRef",
            "PileUpPtBB",
            "PileUpPtEC1",
            #"PileUpPtEC2",
            #"PileUpPtHF",
            
            "RelativeJEREC1",
            #"RelativeJEREC2",
            #"RelativeJERHF",
            "RelativeFSR",
            "RelativeStatFSR",
            "RelativeStatEC",
            #"RelativeStatHF",
            "RelativePtBB",
            "RelativePtEC1",
            #"RelativePtEC2",
            #"RelativePtHF",
            
            "AbsoluteScale",
            "AbsoluteMPFBias",
            "AbsoluteStat",
            "SinglePionECAL",
            "SinglePionHCAL",
            "Fragmentation",
            "TimePtEta",
            "FlavorQCD"
            ]




    ## Set validation plots ##
    if doPlots:
        resolution_hists = {}
        hists = {}
        for var in ['HCMVAV2_reg_mass', 'HCMVAV2_reg_pt']:
            hists['nom_'+var] = TH1F('nom_'+var, 'nom_'+var, 30, 0, 200)
        for syst in JECsys:
            for sdir in ["Up", "Down"]:
                for var in ['HCMVAV2_reg_mass', 'HCMVAV2_reg_pt', 'hJetCMVAV2_pt_reg']:
                    resolution_hists[var+syst+sdir] = TH1F(var+syst+sdir, var+syst+sdir, 30,-0.05,0.05)
                    hists['nom_'+var+syst+sdir] = TH1F('nom_'+var+syst+sdir, 'nom_'+var+syst+sdir, 30, 0, 200)
    
    #print hists    

    print '----> Input : ', input
    print '----> Output: ', output
    
    input.cd()
    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        if obj.GetName() == 'tree':
            continue
        output.cd()
        obj.Write(key.GetName())

    input.cd()
    tree = input.Get('tree')
    nEntries = tree.GetEntries()

    
    output.cd()

    #For new regresssion zero the branches out before cloning new tree
    tree.SetBranchStatus('HCMVAV2_reg_mass',0)
    tree.SetBranchStatus('HCMVAV2_reg_pt',0)
    tree.SetBranchStatus('HCMVAV2_reg_eta',0)
    tree.SetBranchStatus('HCMVAV2_reg_phi',0)
    tree.SetBranchStatus('hJetCMVAV2_pt_reg_0',0)
    tree.SetBranchStatus('hJetCMVAV2_pt_reg_1', 0)
    
    for syst in JECsys:
        for sdir in ["Up", "Down"]:
            tree.SetBranchStatus('HCMVAV2_reg_mass_corr'+syst+sdir, 0)
            tree.SetBranchStatus('HCMVAV2_reg_pt_corr'+syst+sdir, 0)
            tree.SetBranchStatus('HCMVAV2_reg_eta_corr'+syst+sdir, 0)
            tree.SetBranchStatus('HCMVAV2_reg_phi_corr'+syst+sdir, 0)
            tree.SetBranchStatus('hJetCMVAV2_pt_reg_0'+syst+sdir, 0)
            tree.SetBranchStatus('hJetCMVAV2_pt_reg_1'+syst+sdir, 0)

    newtree = tree.CloneTree(0)        

    JEC_systematics = {}

    hJ0 = ROOT.TLorentzVector()
    hJ1 = ROOT.TLorentzVector()
    
    # for the dijet mass/pt
    JEC_systematics['HCMVAV2_reg_mass'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_mass', JEC_systematics['HCMVAV2_reg_mass'], 'HCMVAV2_reg_mass/D')
    
    JEC_systematics['HCMVAV2_reg_pt'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_pt', JEC_systematics['HCMVAV2_reg_pt'], 'HCMVAV2_reg_pt/D')
    
    JEC_systematics['HCMVAV2_reg_eta'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_eta', JEC_systematics['HCMVAV2_reg_eta'], 'HCMVAV2_reg_eta/D')

    JEC_systematics['HCMVAV2_reg_phi'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_phi', JEC_systematics['HCMVAV2_reg_phi'], 'HCMVAV2_reg_phi/D')

    # For the dijet Jets
    JEC_systematics['hJetCMVAV2_pt_reg_0'] = np.zeros(1, dtype=float)
    newtree.Branch('hJetCMVAV2_pt_reg_0', JEC_systematics['hJetCMVAV2_pt_reg_0'], 'hJetCMVAV2_pt_reg_0/D')

    JEC_systematics['hJetCMVAV2_pt_reg_1'] = np.zeros(1, dtype=float)
    newtree.Branch('hJetCMVAV2_pt_reg_1', JEC_systematics['hJetCMVAV2_pt_reg_1'], 'hJetCMVAV2_pt_reg_1/D')

    if 'Zee' not in file and 'Zuu' not in file:
    
        for syst in JECsys:
            for sdir in ["Up", "Down"]:
                JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("HCMVAV2_reg_mass_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir], "HCMVAV2_reg_mass_corr"+syst+sdir+"/D")

                JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("HCMVAV2_reg_pt_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir], "HCMVAV2_reg_pt_corr"+syst+sdir+"/D")

                JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("HCMVAV2_reg_eta_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir], "HCMVAV2_reg_eta_corr"+syst+sdir+"/D")

                JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("HCMVAV2_reg_phi_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir], "HCMVAV2_reg_phi_corr"+syst+sdir+"/D")

                JEC_systematics["hJetCMVAV2_pt_reg_0"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("hJetCMVAV2_pt_reg_0"+syst+sdir, JEC_systematics["hJetCMVAV2_pt_reg_0"+syst+sdir], "hJetCMVAV2_pt_reg_0"+syst+sdir+"/D")

                JEC_systematics["hJetCMVAV2_pt_reg_1"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("hJetCMVAV2_pt_reg_1"+syst+sdir, JEC_systematics["hJetCMVAV2_pt_reg_1"+syst+sdir], "hJetCMVAV2_pt_reg_1"+syst+sdir+"/D")

    # jet reg weights
    JetCMVAV2_regWeight = array('f',[0]*2)
    newtree.Branch('JetCMVAV2_regWeight',JetCMVAV2_regWeight,'JetCMVAV2_regWeight[2]/F')
    
    # define all the readers
    TMVA_reader = {}
    theVars1 = {}
    theVars0 = {}
    
    TMVA_reader['readerJet0'] = ROOT.TMVA.Reader("!Color:!Silent" )
    TMVA_reader['readerJet1'] = ROOT.TMVA.Reader("!Color:!Silent" )
    
    #for syst in JECsys:
    #    for sdir in ["Up", "Down"]:
    #        TMVA_reader['readerJet0_'+syst+sdir] = ROOT.TMVA.Reader("!Color:!Silent" )
    #        TMVA_reader['readerJet1_'+syst+sdir] = ROOT.TMVA.Reader("!Color:!Silent" )

    def addVarsToReader(reader,theVars):
            for key in regVars:
                #print key
                var = regDict[key]
                theVars[key] = array( 'f', [ 0 ] )
                reader.AddVariable(key,theVars[key])
            return

    # Init the TMVA readers
    addVarsToReader(TMVA_reader['readerJet0'],theVars0)
    addVarsToReader(TMVA_reader['readerJet1'],theVars1)
    TMVA_reader['readerJet0'].BookMVA("readerJet0", regWeight)
    TMVA_reader['readerJet1'].BookMVA("readerJet1", regWeight)

    # for syst in JECsys:
    #     for sdir in ["Up", "Down"]:
    #         addVarsToReader(TMVA_reader['readerJet0_'+syst+sdir], theVarsJEC0[syst+sdir])
    #         addVarsToReader(TMVA_reader['readerJet1_'+syst+sdir], theVarsJEC1[syst+sdir])
    #         TMVA_reader['readerJet0_'+syst+sdir].BookMVA("readerJet0_"+syst+sdir, regWeight)
    #         TMVA_reader['readerJet1_'+syst+sdir].BookMVA("readerJet1_"+syst+sdir, regWeight)


    

    print '\n\t ----> Evaluating Regression on sample....'
    
    print tree
    
    for entry in range(0,nEntries):
        
        tree.GetEntry(entry)
        
        if entry % 1000 is 0: print '-----> Event # ', entry
        
        #if entry < 9000: continue
        #if entry > 1000: break
        
        #if tree.nhJCMVAV2idx < 2: continue
        # print entry
        
        if 'ttbar' in file:
            if entry == 9015: continue


        Jet_pt_0 = tree.Jet_pt[tree.hJCMVAV2idx[0]]
        Jet_pt_1 = tree.Jet_pt[tree.hJCMVAV2idx[1]]
        Jet_eta_0 = tree.Jet_eta[tree.hJCMVAV2idx[0]]
        Jet_eta_1 = tree.Jet_eta[tree.hJCMVAV2idx[1]]
        Jet_ptRaw_0 = tree.Jet_rawPt[tree.hJCMVAV2idx[0]]
        Jet_ptRaw_1 = tree.Jet_rawPt[tree.hJCMVAV2idx[1]]
        Jet_m_0 = tree.Jet_mass[tree.hJCMVAV2idx[0]]
        Jet_m_1 = tree.Jet_mass[tree.hJCMVAV2idx[1]]
        Jet_phi_0 = tree.Jet_phi[tree.hJCMVAV2idx[0]]
        Jet_phi_1 = tree.Jet_phi[tree.hJCMVAV2idx[1]]
     
        hJ0.SetPtEtaPhiM(Jet_pt_0, Jet_eta_0, Jet_phi_0, Jet_m_0)
        hJ1.SetPtEtaPhiM(Jet_pt_1, Jet_eta_1, Jet_phi_1, Jet_m_1)
   
        #met_pt_0 = tree.met_pt
        #met_pt_1 = tree.met_pt
        
        #Jet_met_proj_0 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_0, Jet_phi_0)
        #Jet_met_proj_1 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_1, Jet_phi_1)

        Jet_e_0 = hJ0.E()
        Jet_e_1 = hJ1.E()
        Jet_mt_0 = hJ0.Mt()
        Jet_mt_1 = hJ1.Mt()
        
        Jet_vtxPt_0 = max(0.,tree.Jet_vtxPt[tree.hJCMVAV2idx[0]])
        Jet_vtxPt_1 = max(0.,tree.Jet_vtxPt[tree.hJCMVAV2idx[1]])
        Jet_vtx3dL_0= max(0.,tree.Jet_vtx3DVal[tree.hJCMVAV2idx[0]])
        Jet_vtx3dL_1= max(0.,tree.Jet_vtx3DVal[tree.hJCMVAV2idx[1]])
        Jet_vtx3deL_0= max(0.,tree.Jet_vtx3DSig[tree.hJCMVAV2idx[0]])
        Jet_vtx3deL_1= max(0.,tree.Jet_vtx3DSig[tree.hJCMVAV2idx[1]])
        Jet_vtxMass_0= max(0.,tree.Jet_vtxMass[tree.hJCMVAV2idx[0]])
        Jet_vtxMass_1= max(0.,tree.Jet_vtxMass[tree.hJCMVAV2idx[1]])
        Jet_vtxNtrk_0= max(0.,tree.Jet_vtxNtracks[tree.hJCMVAV2idx[0]])
        Jet_vtxNtrk_1= max(0.,tree.Jet_vtxNtracks[tree.hJCMVAV2idx[1]])
        
        Jet_chEmEF_0=tree.Jet_chEmEF[tree.hJCMVAV2idx[0]]
        Jet_chEmEF_1=tree.Jet_chEmEF[tree.hJCMVAV2idx[1]]
        Jet_chHEF_0=tree.Jet_chHEF[tree.hJCMVAV2idx[0]]
        Jet_chHEF_1=tree.Jet_chHEF[tree.hJCMVAV2idx[1]]
        Jet_neHEF_0=tree.Jet_neHEF[tree.hJCMVAV2idx[0]]
        Jet_neHEF_1=tree.Jet_neHEF[tree.hJCMVAV2idx[1]]
        Jet_neEmEF_0=tree.Jet_neEmEF[tree.hJCMVAV2idx[0]]
        Jet_neEmEF_1=tree.Jet_neEmEF[tree.hJCMVAV2idx[1]]
        Jet_rawPt_0 = tree.Jet_rawPt[tree.hJCMVAV2idx[0]]
        Jet_rawPt_1 = tree.Jet_rawPt[tree.hJCMVAV2idx[1]]
        Jet_chMult_0 = tree.Jet_chMult[tree.hJCMVAV2idx[0]]
        Jet_chMult_1 = tree.Jet_chMult[tree.hJCMVAV2idx[1]]
        Jet_leadTrackPt_0 = max(0.,tree.Jet_leadTrackPt[tree.hJCMVAV2idx[0]])
        Jet_leadTrackPt_1 = max(0.,tree.Jet_leadTrackPt[tree.hJCMVAV2idx[1]])
        Jet_leptonPtRel_0 = max(0.,tree.Jet_leptonPtRel[tree.hJCMVAV2idx[0]])
        Jet_leptonPtRel_1= max(0.,tree.Jet_leptonPtRel[tree.hJCMVAV2idx[1]])
        Jet_leptonDeltaR_0 = max(0.,tree.Jet_leptonDeltaR[tree.hJCMVAV2idx[0]])
        Jet_leptonDeltaR_1 = max(0.,tree.Jet_leptonDeltaR[tree.hJCMVAV2idx[1]])
        Jet_leptonPt_0 = max(0.,tree.Jet_leptonPt[tree.hJCMVAV2idx[0]])
        Jet_leptonPt_1= max(0.,tree.Jet_leptonPt[tree.hJCMVAV2idx[1]])
        rho_0=tree.rho
        rho_1=tree.rho
        
        nPVs_0=tree.nPVs
        nPVs_1=tree.nPVs
        
        # JEC factorized branches
        if 'Zee' not in file and 'Zuu' not in file:
            Jet_corr_JER_0 = tree.Jet_corr_JER[tree.hJCMVAV2idx[0]]
            Jet_corr_JER_1 = tree.Jet_corr_JER[tree.hJCMVAV2idx[1]]
            
            Jet_corr_0 = tree.Jet_corr[tree.hJCMVAV2idx[0]]
            Jet_corr_1 = tree.Jet_corr[tree.hJCMVAV2idx[1]]
            
            Jet_corr_JERUp_0 = tree.Jet_corr_JERUp[tree.hJCMVAV2idx[0]]
            Jet_corr_JERUp_1 = tree.Jet_corr_JERUp[tree.hJCMVAV2idx[1]]
            Jet_corr_JERDown_0 = tree.Jet_corr_JERDown[tree.hJCMVAV2idx[0]]
            Jet_corr_JERDown_1 = tree.Jet_corr_JERDown[tree.hJCMVAV2idx[1]]

            Jet_corr_PileUpDataMCUp_0 = tree.Jet_corr_PileUpDataMCUp[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpDataMCUp_1 = tree.Jet_corr_PileUpDataMCUp[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpDataMCDown_0 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpDataMCDown_1 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[1]]

            Jet_corr_PileUpPtRefUp_0 = tree.Jet_corr_PileUpPtRefUp[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtBBUp_0 = tree.Jet_corr_PileUpPtBBUp[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtEC1Up_0 = tree.Jet_corr_PileUpPtEC1Up[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtEC2Up_0 = tree.Jet_corr_PileUpPtEC2Up[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtHFUp_0 = tree.Jet_corr_PileUpPtHFUp[tree.hJCMVAV2idx[0]]

            Jet_corr_RelativeJEREC1Up_0 = tree.Jet_corr_RelativeJEREC1Up[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeJEREC2Up_0 = tree.Jet_corr_RelativeJEREC2Up[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeJERHFUp_0 = tree.Jet_corr_RelativeJERHFUp[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeFSRUp_0 = tree.Jet_corr_RelativeFSRUp[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeStatFSRUp_0 = tree.Jet_corr_RelativeStatFSRUp[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeStatECUp_0 = tree.Jet_corr_RelativeStatECUp[tree.hJCMVAV2idx[0]]
            #Jet_corr_RelativeStatEC2Up_0 = tree.Jet_corr_RelativeStatEC2Up[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeStatHFUp_0 = tree.Jet_corr_RelativeStatHFUp[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtBBUp_0 = tree.Jet_corr_RelativePtBBUp[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtEC1Up_0 = tree.Jet_corr_RelativePtEC1Up[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtEC2Up_0 = tree.Jet_corr_RelativePtEC2Up[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtHFUp_0 = tree.Jet_corr_RelativePtHFUp[tree.hJCMVAV2idx[0]]

            Jet_corr_AbsoluteScaleUp_0 = tree.Jet_corr_AbsoluteScaleUp[tree.hJCMVAV2idx[0]]
            Jet_corr_AbsoluteMPFBiasUp_0 = tree.Jet_corr_AbsoluteMPFBiasUp[tree.hJCMVAV2idx[0]]
            Jet_corr_AbsoluteStatUp_0 = tree.Jet_corr_AbsoluteStatUp[tree.hJCMVAV2idx[0]]
            Jet_corr_SinglePionECALUp_0 = tree.Jet_corr_SinglePionECALUp[tree.hJCMVAV2idx[0]]
            Jet_corr_SinglePionHCALUp_0 = tree.Jet_corr_SinglePionHCALUp[tree.hJCMVAV2idx[0]]
            Jet_corr_FragmentationUp_0 = tree.Jet_corr_FragmentationUp[tree.hJCMVAV2idx[0]]
            Jet_corr_TimePtEtaUp_0 = tree.Jet_corr_TimePtEtaUp[tree.hJCMVAV2idx[0]]
            Jet_corr_FlavorQCDUp_0 = tree.Jet_corr_FlavorQCDUp[tree.hJCMVAV2idx[0]]

            # Jet 2
            Jet_corr_PileUpPtRefUp_1 = tree.Jet_corr_PileUpPtRefUp[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtBBUp_1 = tree.Jet_corr_PileUpPtBBUp[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtEC1Up_1 = tree.Jet_corr_PileUpPtEC1Up[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtEC2Up_1 = tree.Jet_corr_PileUpPtEC2Up[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtHFUp_1 = tree.Jet_corr_PileUpPtHFUp[tree.hJCMVAV2idx[1]]

            Jet_corr_RelativeJEREC1Up_1 = tree.Jet_corr_RelativeJEREC1Up[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeJEREC2Up_1 = tree.Jet_corr_RelativeJEREC2Up[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeJERHFUp_1 = tree.Jet_corr_RelativeJERHFUp[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeFSRUp_1 = tree.Jet_corr_RelativeFSRUp[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeStatFSRUp_1 = tree.Jet_corr_RelativeStatFSRUp[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeStatECUp_1 = tree.Jet_corr_RelativeStatECUp[tree.hJCMVAV2idx[1]]
            #Jet_corr_RelativeStatEC2Up_1 = tree.Jet_corr_RelativeStatEC2Up[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeStatHFUp_1 = tree.Jet_corr_RelativeStatHFUp[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtBBUp_1 = tree.Jet_corr_RelativePtBBUp[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtEC1Up_1 = tree.Jet_corr_RelativePtEC1Up[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtEC2Up_1 = tree.Jet_corr_RelativePtEC2Up[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtHFUp_1 = tree.Jet_corr_RelativePtHFUp[tree.hJCMVAV2idx[1]]

            Jet_corr_AbsoluteScaleUp_1 = tree.Jet_corr_AbsoluteScaleUp[tree.hJCMVAV2idx[1]]
            Jet_corr_AbsoluteMPFBiasUp_1 = tree.Jet_corr_AbsoluteMPFBiasUp[tree.hJCMVAV2idx[1]]
            Jet_corr_AbsoluteStatUp_1 = tree.Jet_corr_AbsoluteStatUp[tree.hJCMVAV2idx[1]]
            Jet_corr_SinglePionECALUp_1 = tree.Jet_corr_SinglePionECALUp[tree.hJCMVAV2idx[1]]
            Jet_corr_SinglePionHCALUp_1 = tree.Jet_corr_SinglePionHCALUp[tree.hJCMVAV2idx[1]]
            Jet_corr_FragmentationUp_1 = tree.Jet_corr_FragmentationUp[tree.hJCMVAV2idx[1]]
            Jet_corr_TimePtEtaUp_1 = tree.Jet_corr_TimePtEtaUp[tree.hJCMVAV2idx[1]]
            Jet_corr_FlavorQCDUp_1 = tree.Jet_corr_FlavorQCDUp[tree.hJCMVAV2idx[1]]

            ## Down ##
            Jet_corr_PileUpDataMCDown_0 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpDataMCDown_1 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpDataMCDown_0 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpDataMCDown_1 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[1]]

            Jet_corr_PileUpPtRefDown_0 = tree.Jet_corr_PileUpPtRefDown[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtBBDown_0 = tree.Jet_corr_PileUpPtBBDown[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtEC1Down_0 = tree.Jet_corr_PileUpPtEC1Down[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtEC2Down_0 = tree.Jet_corr_PileUpPtEC2Down[tree.hJCMVAV2idx[0]]
            Jet_corr_PileUpPtHFDown_0 = tree.Jet_corr_PileUpPtHFDown[tree.hJCMVAV2idx[0]]

            Jet_corr_RelativeJEREC1Down_0 = tree.Jet_corr_RelativeJEREC1Down[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeJEREC2Down_0 = tree.Jet_corr_RelativeJEREC2Down[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeJERHFDown_0 = tree.Jet_corr_RelativeJERHFDown[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeFSRDown_0 = tree.Jet_corr_RelativeFSRDown[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeStatFSRDown_0 = tree.Jet_corr_RelativeStatFSRDown[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeStatECDown_0 = tree.Jet_corr_RelativeStatECDown[tree.hJCMVAV2idx[0]]
            #Jet_corr_RelativeStatEC2Down_0 = tree.Jet_corr_RelativeStatEC2Down[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativeStatHFDown_0 = tree.Jet_corr_RelativeStatHFDown[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtBBDown_0 = tree.Jet_corr_RelativePtBBDown[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtEC1Down_0 = tree.Jet_corr_RelativePtEC1Down[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtEC2Down_0 = tree.Jet_corr_RelativePtEC2Down[tree.hJCMVAV2idx[0]]
            Jet_corr_RelativePtHFDown_0 = tree.Jet_corr_RelativePtHFDown[tree.hJCMVAV2idx[0]]

            Jet_corr_AbsoluteScaleDown_0 = tree.Jet_corr_AbsoluteScaleDown[tree.hJCMVAV2idx[0]]
            Jet_corr_AbsoluteMPFBiasDown_0 = tree.Jet_corr_AbsoluteMPFBiasDown[tree.hJCMVAV2idx[0]]
            Jet_corr_AbsoluteStatDown_0 = tree.Jet_corr_AbsoluteStatDown[tree.hJCMVAV2idx[0]]
            Jet_corr_SinglePionECALDown_0 = tree.Jet_corr_SinglePionECALDown[tree.hJCMVAV2idx[0]]
            Jet_corr_SinglePionHCALDown_0 = tree.Jet_corr_SinglePionHCALDown[tree.hJCMVAV2idx[0]]
            Jet_corr_FragmentationDown_0 = tree.Jet_corr_FragmentationDown[tree.hJCMVAV2idx[0]]
            Jet_corr_TimePtEtaDown_0 = tree.Jet_corr_TimePtEtaDown[tree.hJCMVAV2idx[0]]
            Jet_corr_FlavorQCDDown_0 = tree.Jet_corr_FlavorQCDDown[tree.hJCMVAV2idx[0]]

            # Jet 2
            Jet_corr_PileUpPtRefDown_1 = tree.Jet_corr_PileUpPtRefDown[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtBBDown_1 = tree.Jet_corr_PileUpPtBBDown[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtEC1Down_1 = tree.Jet_corr_PileUpPtEC1Down[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtEC2Down_1 = tree.Jet_corr_PileUpPtEC2Down[tree.hJCMVAV2idx[1]]
            Jet_corr_PileUpPtHFDown_1 = tree.Jet_corr_PileUpPtHFDown[tree.hJCMVAV2idx[1]]

            Jet_corr_RelativeJEREC1Down_1 = tree.Jet_corr_RelativeJEREC1Down[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeJEREC2Down_1 = tree.Jet_corr_RelativeJEREC2Down[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeJERHFDown_1 = tree.Jet_corr_RelativeJERHFDown[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeFSRDown_1 = tree.Jet_corr_RelativeFSRDown[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeStatFSRDown_1 = tree.Jet_corr_RelativeStatFSRDown[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeStatECDown_1 = tree.Jet_corr_RelativeStatECDown[tree.hJCMVAV2idx[1]]
            #Jet_corr_RelativeStatEC2Down_1 = tree.Jet_corr_RelativeStatEC2Down[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativeStatHFDown_1 = tree.Jet_corr_RelativeStatHFDown[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtBBDown_1 = tree.Jet_corr_RelativePtBBDown[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtEC1Down_1 = tree.Jet_corr_RelativePtEC1Down[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtEC2Down_1 = tree.Jet_corr_RelativePtEC2Down[tree.hJCMVAV2idx[1]]
            Jet_corr_RelativePtHFDown_1 = tree.Jet_corr_RelativePtHFDown[tree.hJCMVAV2idx[1]]

            Jet_corr_AbsoluteScaleDown_1 = tree.Jet_corr_AbsoluteScaleDown[tree.hJCMVAV2idx[1]]
            Jet_corr_AbsoluteMPFBiasDown_1 = tree.Jet_corr_AbsoluteMPFBiasDown[tree.hJCMVAV2idx[1]]
            Jet_corr_AbsoluteStatDown_1 = tree.Jet_corr_AbsoluteStatDown[tree.hJCMVAV2idx[1]]
            Jet_corr_SinglePionECALDown_1 = tree.Jet_corr_SinglePionECALDown[tree.hJCMVAV2idx[1]]
            Jet_corr_SinglePionHCALDown_1 = tree.Jet_corr_SinglePionHCALDown[tree.hJCMVAV2idx[1]]
            Jet_corr_FragmentationDown_1 = tree.Jet_corr_FragmentationDown[tree.hJCMVAV2idx[1]]
            Jet_corr_TimePtEtaDown_1 = tree.Jet_corr_TimePtEtaDown[tree.hJCMVAV2idx[1]]
            Jet_corr_FlavorQCDDown_1 = tree.Jet_corr_FlavorQCDDown[tree.hJCMVAV2idx[1]]
        

        for key in regVars:
            #print '\n\tSetting Variable:', key
            theVars0[key][0] = eval("%s_0" %(key))
            theVars1[key][0] = eval("%s_1" %(key))


        # ##### Evaluate the regression #####    
        Pt0 = max(0.0001, TMVA_reader['readerJet0'].EvaluateRegression("readerJet0")[0])
        Pt1 = max(0.0001, TMVA_reader['readerJet1'].EvaluateRegression("readerJet1")[0])
        
        rPt0 = Jet_pt_0*Pt0
        rPt1 = Jet_pt_1*Pt1
        
        JEC_systematics["hJetCMVAV2_pt_reg_0"][0] = Pt0
        JEC_systematics["hJetCMVAV2_pt_reg_1"][0] = Pt1

        JetCMVAV2_regWeight[0] = Pt0/Jet_pt_0
        JetCMVAV2_regWeight[1] = Pt1/Jet_pt_1
        
        hJ0.SetPtEtaPhiM(Pt0, Jet_eta_0, Jet_phi_0, Jet_m_0*(Pt0/Jet_pt_0))
        hJ1.SetPtEtaPhiM(Pt1, Jet_eta_1, Jet_phi_1, Jet_m_1*(Pt1/Jet_pt_1))
            
        JEC_systematics["HCMVAV2_reg_mass"][0] = (hJ0+hJ1).M()
        JEC_systematics["HCMVAV2_reg_pt"][0]   = (hJ0+hJ1).Pt()
        JEC_systematics["HCMVAV2_reg_eta"][0]  = (hJ0+hJ1).Eta()
        JEC_systematics["HCMVAV2_reg_phi"][0]  = (hJ0+hJ1).Phi()

        if isVerbose:
            print '\n\n\nJet1 pt reg:', Pt0, Jet_pt_0
            print 'Jet2 pt reg:', Pt1, Jet_pt_1
            print 'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass"][0], tree.H_reg_mass
        

        if doPlots:
            for var in ['HCMVAV2_reg_mass', 'HCMVAV2_reg_pt']:
                hists['nom_'+var].Fill(JEC_systematics[var][0])


        if 'Zee' in file or 'Zuu' in file: 
            newtree.Fill()
            continue
        
        
        for syst in JECsys:
            for sdir in ["Up", "Down"]:

                theVars0['Jet_pt'][0] = 0
                theVars1['Jet_pt'][0] = 0
                
                if syst == "JER":
                    formula1 = "Jet_rawPt_0*Jet_corr_0*Jet_corr_JER"+sdir+"_0"
                    formula2 = "Jet_rawPt_1*Jet_corr_1*Jet_corr_JER"+sdir+"_1"
                    theVars0['Jet_pt'][0] = eval(formula1)
                    theVars1['Jet_pt'][0] = eval(formula2)

                    if doGroup:
                        pt1 = max(0.0001, TMVA_reader['readerJet0'].EvaluateRegression("readerJet0")[0])
                        pt2 = max(0.0001, TMVA_reader['readerJet1'].EvaluateRegression("readerJet1")[0])
                        
                        rPt0 = Jet_pt_0*pt1
                        rPt1 = Jet_pt_1*pt2
                        
                        JEC_systematics["hJetCMVAV2_pt_reg_0"+syst+sdir][0] = pt1
                        JEC_systematics["hJetCMVAV2_pt_reg_1"+syst+sdir][0] = pt2
                        
                        Jet_regWeight1 = pt1/Jet_pt_0
                        Jet_regWeight2 = pt2/Jet_pt_1
                        
                        hJ0.SetPtEtaPhiM(pt1, Jet_eta_0, Jet_phi_0, Jet_m_0*Jet_regWeight1)
                        hJ1.SetPtEtaPhiM(pt2, Jet_eta_1, Jet_phi_1, Jet_m_1*Jet_regWeight2)
                        
                        JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] = (hJ0+hJ1).M()
                        JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] = (hJ0+hJ1).Pt()
                        JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir][0] = (hJ0+hJ1).Eta()
                        JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir][0] = (hJ0+hJ1).Phi()
                        
                        #print syst+sdir+' Jet1 pt reg:', pt1
                        #print syst+sdir+' Jet2 pt reg:', pt2
                        #print syst+sdir+'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0]
                        
                else:
                    if not doGroup:
                        formula1 = "Jet_rawPt_0*Jet_corr_"+syst+sdir+"_0*Jet_corr_JER_0"
                        formula2 = "Jet_rawPt_1*Jet_corr_"+syst+sdir+"_1*Jet_corr_JER_1"
                        theVars0['Jet_pt'][0] = eval(formula1)
                        theVars1['Jet_pt'][0] = eval(formula2)
            
                    else:
                        for group in JECsys: #["PileUp"], ["Relative"], ["AbsoluteMisc"]:
                            if group == 'JER': continue
                            formula1 = "Jet_rawPt_0*Jet_corr_JER_0"
                            formula2 = "Jet_rawPt_1*Jet_corr_JER_1"
                            #print 'Group SYS:', group
                            for sys in JECsysGroupDict[group]:
                                #print 'Adding group sys to formula:', sys
                                formula1 = formula1 + "*Jet_corr_"+sys+sdir+"_0"
                                formula2 = formula2 + "*Jet_corr_"+sys+sdir+"_1"
                            theVars0['Jet_pt'][0] = eval(formula1)
                            theVars1['Jet_pt'][0] = eval(formula2)

                            #print 'formula1:', formula1
                            #print 'formula2:', formula2
                            pt1 = max(0.0001, TMVA_reader['readerJet0'].EvaluateRegression("readerJet0")[0])
                            pt2 = max(0.0001, TMVA_reader['readerJet1'].EvaluateRegression("readerJet1")[0])

                            rPt0 = Jet_pt_0*pt1
                            rPt1 = Jet_pt_1*pt2
                
                            JEC_systematics["hJetCMVAV2_pt_reg_0"+syst+sdir][0] = pt1
                            JEC_systematics["hJetCMVAV2_pt_reg_1"+syst+sdir][0] = pt2
                
                            Jet_regWeight1 = pt1/Jet_pt_0
                            Jet_regWeight2 = pt2/Jet_pt_1
                
                            hJ0.SetPtEtaPhiM(pt1, Jet_eta_0, Jet_phi_0, Jet_m_0*Jet_regWeight1)
                            hJ1.SetPtEtaPhiM(pt2, Jet_eta_1, Jet_phi_1, Jet_m_1*Jet_regWeight2)
                
                            JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] = (hJ0+hJ1).M()
                            JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] = (hJ0+hJ1).Pt()
                            JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir][0] = (hJ0+hJ1).Eta()
                            JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir][0] = (hJ0+hJ1).Phi()
                
                            print syst+sdir+' Jet1 pt reg:', pt1
                            print syst+sdir+' Jet2 pt reg:', pt2
                            print syst+sdir+'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0]
                            
                            
                            
                if not doGroup:
                    #print 'No grouping...'
                    pt1 = max(0.0001, TMVA_reader['readerJet0'].EvaluateRegression("readerJet0")[0])
                    pt2 = max(0.0001, TMVA_reader['readerJet1'].EvaluateRegression("readerJet1")[0])
                    
                    rPt0 = Jet_pt_0*pt1
                    rPt1 = Jet_pt_1*pt2
                    
                    JEC_systematics["hJetCMVAV2_pt_reg_0"+syst+sdir][0] = pt1
                    JEC_systematics["hJetCMVAV2_pt_reg_1"+syst+sdir][0] = pt2
                    
                    Jet_regWeight1 = pt1/Jet_pt_0
                    Jet_regWeight2 = pt2/Jet_pt_1
                    
                    hJ0.SetPtEtaPhiM(pt1, Jet_eta_0, Jet_phi_0, Jet_m_0*Jet_regWeight1)
                    hJ1.SetPtEtaPhiM(pt2, Jet_eta_1, Jet_phi_1, Jet_m_1*Jet_regWeight2)
                    
                    JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] = (hJ0+hJ1).M()
                    JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] = (hJ0+hJ1).Pt()
                    JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir][0] = (hJ0+hJ1).Eta()
                    JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir][0] = (hJ0+hJ1).Phi()

                    if doPlots:
                        for var in ['HCMVAV2_reg_mass', 'HCMVAV2_reg_pt']:

                            
                            if 'mass' in var:
                                #resolution_hists[var+syst+sdir].Fill((JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] - JEC_systematics["HCMVAV2_reg_mass"][0]))
                                resolution_hists[var+syst+sdir].Fill((JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] - JEC_systematics["HCMVAV2_reg_mass"][0])/JEC_systematics["HCMVAV2_reg_mass"][0])
                                hists['nom_'+var+syst+sdir].Fill(JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0])
                            
                            if 'HCMVAV2_reg_pt' in var:
                                #resolution_hists[var+syst+sdir].Fill((JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] - JEC_systematics["HCMVAV2_reg_pt"][0]))
                                resolution_hists[var+syst+sdir].Fill((JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] - JEC_systematics["HCMVAV2_reg_pt"][0])/JEC_systematics["HCMVAV2_reg_pt"][0])
                                hists['nom_'+var+syst+sdir].Fill(JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0])

                            if 'hJetCMVAV2_pt_reg' in var:
                                #resolution_hists[var+syst+sdir].Fill((JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir][0] - JEC_systematics["hJetCMVAV2_pt_reg"][0]))
                                resolution_hists[var+syst+sdir].Fill((JEC_systematics["hJetCMVAV2_pt_reg_0"+syst+sdir][0] - JEC_systematics["hJetCMVAV2_pt_reg_0"][0])/JEC_systematics["hJetCMVAV2_pt_reg_0"][0])
                                    
                    if isVerbose:
                        print syst+sdir+' Jet1 pt reg:', pt1
                        print syst+sdir+' Jet2 pt reg:', pt2
                        print syst+sdir+'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0]

        # Fill Tree
        newtree.Fill()
                                                                             


    if doPlots:
        PlotDir = plotpath
        for syst in JECsys:
            for var in ['HCMVAV2_reg_mass', 'HCMVAV2_reg_pt']:
                for sdir in ["Up", "Down"]:
                    
                    if sdir is 'Up':
                        c = ROOT.TCanvas(var+syst+sdir,'', 600, 600)
                        c.SetFillStyle(4000)
                        c.SetFrameFillStyle(1000)
                        c.SetFrameFillColor(0)
                        c.SetLogy()
                        name = '%s/%s' %(PlotDir, var+syst+'.pdf')
                        resolution_hists[var+syst+sdir].GetXaxis().SetTitle('(JEC Shifted - Nominal)/Nominal')
                        resolution_hists[var+syst+sdir].SetLineColor(kRed)
                        resolution_hists[var+syst+sdir].SetStats(0)
                        resolution_hists[var+syst+sdir].Draw()
                        
                        leg = TLegend(0.7,0.7,0.9,0.9)
                        leg.SetFillStyle(0)
                        leg.SetBorderSize(0)
                        leg.AddEntry(resolution_hists[var+syst+sdir], 'Up', 'l')

                    else:
                        resolution_hists[var+syst+sdir].Draw('same')
                        leg.AddEntry(resolution_hists[var+syst+sdir], 'Down', 'l')
                        leg.Draw('same')

                        c.Print(name)
                        name2 = name.replace('.pdf', '.png', 2)
                        c.Print(name2)
                        c.Delete()
                        leg.Delete()

                        
                    # Now for normal hists
                    if sdir is 'Up':
                        c1 = ROOT.TCanvas('nom_'+var+syst+sdir,'', 600, 600)
                        c1.SetFillStyle(4000)
                        c1.SetFrameFillStyle(1000)
                        c1.SetFrameFillColor(0)
                    #c.SetLogy()
                        name1 = '%s/%s' %(PlotDir, 'nominal_'+var+syst+'.pdf')
                        hists['nom_'+var+syst+sdir].GetXaxis().SetTitle(var)
                        hists['nom_'+var+syst+sdir].SetLineColor(kRed)
                        hists['nom_'+var].SetLineColor(kBlack)
                        hists['nom_'+var+syst+sdir].SetStats(0)
                        hists['nom_'+var+syst+sdir].Draw()
                        
                        leg1 = TLegend(0.7,0.7,0.9,0.9)
                        leg1.SetFillStyle(0)
                        leg1.SetBorderSize(0)
                        #leg1.AddEntry(hists['nom_'+var+syst+sdir], 'Up', 'l')
                        Utotal = hists['nom_'+var+syst+sdir].GetEntries()
                        leg1.AddEntry(hists['nom_'+var+syst+sdir],'Up(%s)'%round(Utotal,3),'PL')
                    else:
                        hists['nom_'+var+syst+sdir].Draw('same')
                        hists['nom_'+var].Draw('same')
                        #leg1.AddEntry(hists['nom_'+var+syst+sdir], 'Down', 'l')
                        #leg1.AddEntry(hists['nom_'+var], 'Nominal', 'l')
                        
                        
                        Dtotal = hists['nom_'+var+syst+sdir].GetEntries()
                        Ntotal = hists['nom_'+var].GetEntries()

                        leg1.AddEntry(hists['nom_'+var],'Nominal(%s)'%round(Ntotal,3),'PL')
                        leg1.AddEntry(hists['nom_'+var+syst+sdir],'Down(%s)'%round(Dtotal,3),'PL')
                        
                        leg1.Draw('same')
                        
                        c1.Print(name1)
                        name3 = name1.replace('.pdf', '.png', 2)
                        c1.Print(name3)
                        c1.Delete()
                        leg1.Delete()
                        
                                                 
    newtree.AutoSave()
    output.Close()
    input.Close()
    print '\nFile', file, ' finished...'



p = multiprocessing.Pool()
results = p.imap(osSystem, file_list)
p.close()
p.join()

# p = multiprocessing.Pool()
# results = p.imap(osSystem,file_list1)
# p.close()
# p.join()

# p = multiprocessing.Pool()
# results = p.imap(osSystem,file_list2)
# p.close()
# p.join()
