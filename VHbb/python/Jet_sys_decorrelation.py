import sys
import os,subprocess
import ROOT 
import math
import shutil
import numpy as np
from array import array
from collections import Counter
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
ROOT.gROOT.SetBatch(True)
from optparse import OptionParser
from myutils import BetterConfigParser, ParseInfo
from myutils.btag_reweight import BTagWeightCalculator, Jet
from myutils.leptonSF import *


################################################################

# sample prefix
prefix = 'v24_9_15_'

inpath = '/exports/uftrig01a/dcurry/heppy/files/prep_out/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/jec_out/'

#inpath = 'root://eoscms//eos/cms/store/user/dcurry/heppy/files/sys_out/'
#outpath = 'root://eoscms//eos/cms/store/user/dcurry/heppy/files/sys_out_btag/'

# List of files to add btag weights to
bkg_list = ['DY_inclusive', 'ttbar', 'ZZ_2L2Q', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list =['ZH125', 'ggZH125']

DY_list = ['DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600toInf', 'DY_Bjets', 'DY_BgenFilter',
           'DY_inclusive_nlo', 'DY_Pt100to250', 'DY_Pt250to400','DY_Pt400to650','DY_Pt650toInf'
           ]

ST_list = ['ST_s', 'ST_tW_top', 'ST_tW_antitop']


#file_list = bkg_list + data_list + signal_list + DY_list + ST_list
file_list = ['ZH125']


for file in file_list:
#def osSystem(file):


    print '\n Adding btag weights to sample:', inpath+prefix+file+'.root'
    print '\n Output File                  :', outpath+prefix+file+'.root'

    ifile = ROOT.TFile.Open(inpath+prefix+file+'.root', 'read')
    ofile = ROOT.TFile(outpath+prefix+file+'.root', 'recreate')

    ifile.cd()
    
    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        ifile.cd()
        obj = key.ReadObj()
        if obj.GetName() == 'tree':
            continue
        ofile.cd()
        obj.Write(key.GetName())

    ifile.cd()
    tree = ifile.Get('tree')

    ofile.cd()

    otree = tree.CloneTree(0)
    
    #Do loop here to define all the variables
    VarList = ['HCSV_reg_corrSYSUD_mass_CAT','HCSV_reg_corrSYSUD_pt_CAT', 'HCSV_reg_corrSYSUD_phi_CAT', 'HCSV_reg_corrSYSUD_eta_CAT','Jet_pt_reg_corrSYSUD_CAT']
    SysList = ['JER','JEC']
    UDList = ['Up','Down']
    CatList = ['lowCentral','highCentral','lowForward','highForward']
    SysDicList = []
    
    ConditionDic = {'lowCentral':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[0]]<100. or tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[1]]<100.)',
                    'highCentral':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[0]]>100. or tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[1]]>100.)',
                    'lowForward':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (abs(tree.Jet_eta[tree.hJCidx[0]])<1.4 or abs(tree.Jet_eta[tree.hJCidx[1]])<1.4)',
                    'highForward':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (abs(tree.Jet_eta[tree.hJCidx[0]])>1.4 or abs(tree.Jet_eta[tree.hJCidx[1]])>1.4)'
                    }

    JetConditionDic = {'lowCentral' :'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]<100. && abs(tree.Jet_eta[tree.hJCidx[INDEX]])<1.4',
                       'highCentral':'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]>100. && abs(tree.Jet_eta[tree.hJCidx[INDEX]])<1.4',
                       'lowForward' :'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]<100. && abs(tree.Jet_eta[tree.hJCidx[INDEX]])>1.4',
                       'highForward':'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]>100. && abs(tree.Jet_eta[tree.hJCidx[INDEX]])>1.4'
                       }
    
    
    DefaultVar = {'HCSV_reg_corrSYSUD_mass_CAT':'tree.HCSV_reg_mass','HCSV_reg_corrSYSUD_pt_CAT':'tree.HCSV_reg_pt','HCSV_reg_corrSYSUD_phi_CAT':'tree.HCSV_reg_phi','HCSV_reg_corrSYSUD_eta_CAT':'tree.HCSV_reg_eta','Jet_pt_reg_corrSYSUD_CAT':'tree.Jet_pt_reg[tree.hJCidx[INDEX]]'}
    
    SYSVar = {'HCSV_reg_corrSYSUD_mass_CAT':'tree.HCSV_reg_mass*(HJet_sys.M()/HJet.M())','HCSV_reg_corrSYSUD_pt_CAT':'tree.HCSV_reg_pt*(HJet_sys.Pt()/HJet.Pt())','HCSV_reg_corrSYSUD_phi_CAT':'tree.HCSV_reg_phi*(HJet_sys.Phi()/HJet.Phi())','HCSV_reg_corrSYSUD_eta_CAT':'tree.HCSV_reg_eta*(HJet_sys.Eta()/HJet.Eta())','Jet_pt_reg_corrSYSUD_CAT':'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]'}

    SysBranchDic = {}
    
    #Make a dic corresponding to each sys and create the variables
    for var in VarList:
        for syst in SysList:
            for cat in CatList:
                for ud in UDList:
                    
                    SysDic = {}
                    SysDic['var'] = var
                    SysDic['sys'] = syst
                    SysDic['UD'] = ud
                    SysDic['cat'] = cat
                    SysDic['varname'] = var.replace('SYS',syst).replace('UD',ud).replace('CAT',cat)

                    #Define var
                    if var == 'Jet_pt_reg_corrSYSUD_CAT':
                        #print 'yeah man'
                        #SysDic['varptr'] = array('f',2*[0])
                        temp_name = var.replace('SYS',syst).replace('UD',ud).replace('CAT',cat)
                        SysBranchDic[temp_name] = array('f',2*[0])
                        otree.Branch(SysDic['varname'], SysBranchDic[temp_name], SysDic['varname']+'[2]/F')
                        SysDicList.append(SysDic)
                        
                    else:
                        #SysDic['varptr'] = array('f',[0])
                        temp_name = var.replace('SYS',syst).replace('UD',ud).replace('CAT',cat)
                        SysBranchDic[temp_name] = array('f',1*[0])
                        otree.Branch(SysDic['varname'], SysBranchDic[temp_name], SysDic['varname']+'/F')
                        SysDicList.append(SysDic)

                        
                        
            # Jet flag for low/high central/forward region
            hJet_low     = array('f',[0]*2)
            hJet_high    = array('f',[0]*2)
            hJet_central = array('f',[0]*2)
            hJet_forward = array('f',[0]*2)

            otree.Branch('hJet_low', hJet_low, 'hJet_low[2]/F')
            otree.Branch('hJet_high',hJet_high, 'hJet_high[2]/F')
            otree.Branch('hJet_central', hJet_central, 'hJet_central[2]/F')
            otree.Branch('hJet_forward', hJet_forward, 'hJet_forward[2]/F')


    # Loop over events
    nentries = tree.GetEntries()
    print "nentries = ",nentries
    for entry in range(nentries):

        if (entry%10000 == 0): print "processing entry: %i" % entry
        
        if entry > 10000: continue

        tree.GetEntry(entry)
        
        #####  Fill Jet branches Here ####
        
        # set the higgs jets in the event
        Jet1 = ROOT.TLorentzVector()
        Jet2 = ROOT.TLorentzVector()
        Jet1_sys = ROOT.TLorentzVector()
        Jet2_sys = ROOT.TLorentzVector()
        Jet1.SetPtEtaPhiM(tree.Jet_pt_reg[tree.hJCidx[0]],tree.Jet_eta[tree.hJCidx[0]],tree.Jet_phi[tree.hJCidx[0]],tree.Jet_mass[tree.hJCidx[0]])
        Jet2.SetPtEtaPhiM(tree.Jet_pt_reg[tree.hJCidx[1]],tree.Jet_eta[tree.hJCidx[1]],tree.Jet_phi[tree.hJCidx[1]],tree.Jet_mass[tree.hJCidx[1]])

        ## JER_lowCentral ##
        # Up
        if tree.Jet_pt_reg[tree.hJCidx[0]] < 100. and tree.Jet_eta[tree.hJCidx[0]] < 1.4: 
            Jet1_sys.SetPtEtaPhiM(tree.Jet_pt_reg_corrJERUp[tree.hJCidx[0]],tree.Jet_eta[tree.hJCidx[0]],tree.Jet_phi[tree.hJCidx[0]],tree.Jet_mass[tree.hJCidx[0]])
        else: Jet1_sys = Jet1
        
        if tree.Jet_pt_reg[tree.hJCidx[1]] < 100. and tree.Jet_eta[tree.hJCidx[1]] < 1.4:
                Jet2_sys.SetPtEtaPhiM(tree.Jet_pt_reg_corrJERUp[tree.hJCidx[1]],tree.Jet_eta[tree.hJCidx[1]],tree.Jet_phi[tree.hJCidx[1]],tree.Jet_mass[tree.hJCidx[1]])
        else: Jet2_sys = Jet2
        
        HJet = Jet1+Jet2
        HJet_sys = Jet1_sys+Jet2_sys
                
        SysBranchDic['HCSV_reg_corrJERUp_mass_lowCentral'][0] = tree.HCSV_reg_mass*(HJet_sys.M()/HJet.M())
        SysBranchDic['HCSV_reg_corrJERUp_pt_lowCentral'][0]   = tree.HCSV_reg_pt*(HJet_sys.Pt()/HJet.Pt())
        SysBranchDic['HCSV_reg_corrJERUp_phi_lowCentral'][0]  = tree.HCSV_reg_phi*(HJet_sys.Phi()/HJet.Phi())
        SysBranchDic['HCSV_reg_corrJERUp_eta_lowCentral'][0]  = tree.HCSV_reg_eta*(HJet_sys.Eta()/HJet.Eta())
        SysBranchDic['Jet_pt_reg_corrJERUp_lowCentral'][0] = Jet1_sys.Pt()
        SysBranchDic['Jet_pt_reg_corrJERUp_lowCentral'][1] = Jet2_sys.Pt()
        
           
        
        
        otree.Fill()

    
    #ofile.cd()
    otree.Write()
    otree.AutoSave()
    ofile.Close()
    ifile.Close()
    print 'Finished...'

# Done
#p = multiprocessing.Pool()
#results = p.imap(osSystem, file_list)
#p.close()
#p.join()
