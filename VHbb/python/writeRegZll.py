#!/usr/bin/env python
#from samplesclass import sample
#from printcolor import printc
import pickle
import sys
import os
import ROOT 
import math
import shutil
from ROOT import TFile
from ROOT import TXNetFile
import ROOT
from array import array
import warnings
from optparse import OptionParser
#from BetterConfigParser import BetterConfigParser
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
argv = sys.argv
ROOT.gROOT.SetBatch(True)
parser = OptionParser()

parser.add_option("-S", "--samples", dest="names", default="",
                                        help="samples you want to run on")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                                        help="configuration defining the plots to make")
(opts, args) = parser.parse_args(argv)
if opts.config =="":
    opts.config = "config"

from myutils import BetterConfigParser, ParseInfo

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

pathIN = config.get('Directories','SYSin')
pathOUT = config.get('Directories','SYSout')
tmpDir = os.environ["TMPDIR"]

name = config.get('TrainRegression', 'name')

namelist=opts.names.split(',')

#load info
info = ParseInfo(samplesinfo,pathIN)

sample = namelist[0]

print '\n\n\t\t ======= Applying Regression weights to sample: ', sample,'========\n\n'



def deltaPhi(phi1, phi2): 
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result

do = True



def resolutionBias(eta):
    if(eta< 0.5): return 0.052
    if(eta< 1.1): return 0.057
    if(eta< 1.7): return 0.096
    if(eta< 2.3): return 0.134
    if(eta< 5): return 0.28
    return 0

def corrPt(pt,eta,mcPt):
    return (pt+resolutionBias(math.fabs(eta))*(pt-mcPt))/pt

def addAdditionalJets(H, tree):
    for i in range(tree.nhjidxaddJetsdR08):
        idx = tree.hjidxaddJetsdR08[i]
        if (idx == tree.hJCidx[0]) or (idx == tree.hJCidx[1]): continue
        addjet = ROOT.TLorentzVector()
        addjet.SetPtEtaPhiM(tree.Jet_pt[idx],tree.Jet_eta[idx],tree.Jet_phi[idx],tree.Jet_mass[idx])
        H = H + addjet
    return H

ROOT.gROOT.ProcessLine(
        "struct H {\
        int         HiggsFlag;\
        float         mass;\
	float 	      masswithFSR;\
        float         pt;\
        float         eta;\
        float         phi;\
        float         dR;\
        float         dPhi;\
        float         dEta;\
        } ;"
    )


for iter in range(0,1):
    
    regWeight = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/myMacros/regression/forDavid/weights_ZH_genJet_boost/TMVARegression_BDTG.weights.xml'
     
    input  = TFile.Open('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v14_11_2015_ggZH125.root', 'read')
    
    output = TFile.Open('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/dec_zll_genJet_boost/v14_11_2015_ggZH125.root', 'recreate')
    
    
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
    H = ROOT.H()
    HNoReg = ROOT.H()
    HwithM = ROOT.H()	
    tree.SetBranchStatus('H',0)
    output.cd()
    newtree = tree.CloneTree(0)        
    regDict = {"Jet_pt":"Jet_pt[0]",
               "Jet_corr":"Jet_corr[0]"  ,
               "rho":"rho[0]",
               "Jet_eta":"Jet_eta[0]",
               "Jet_mt":"Jet_mt[0]",
               "Jet_leadTrackPt":"Jet_leadTrackPt[0]",
               "Jet_leptonPtRel":"Jet_leptonPtRel[0]",
               "Jet_leptonPt":"Jet_leptonPt[0]",
               "Jet_leptonDeltaR":"Jet_leptonDeltaR[0]",
               "Jet_neHEF":"Jet_neHEF[0]",
               "Jet_neEmEF":"Jet_neEmEF[0]",
               "Jet_chMult":"Jet_chMult[0]" ,
               "Jet_vtxPt":"Jet_vtxPt[0]",
               "Jet_vtxMass":"Jet_vtxMass[0]",
               "Jet_vtx3dL":"Jet_vtx3dL[0]",
               "Jet_vtxNtrk":"Jet_vtxNtrk[0]",
               "Jet_vtx3deL":"Jet_vtx3deL[0]"}

    regVars = ["Jet_pt",
               "Jet_corr"  ,
               "rho",
               "Jet_eta",
               "Jet_mt",
               "Jet_leadTrackPt",
               "Jet_leptonPtRel",
               "Jet_leptonPt",
               "Jet_leptonDeltaR",
               "Jet_neHEF",
               "Jet_neEmEF",
               "Jet_chMult" ,
               "Jet_vtxPt",
               "Jet_vtxMass",
               "Jet_vtx3dL",
               "Jet_vtxNtrk",
               "Jet_vtx3deL"]      	
		

    #Regression branches
    applyRegression = True
    newtree.Branch( 'H', H , 'HiggsFlag/I:mass/F:masswithFSR/F:pt/F:eta/F:phi/F:dR/F:dPhi/F:dEta/F' )
    newtree.Branch( 'HNoReg', HNoReg , 'HiggsFlag/I:mass/F:masswithFSR/F:pt/F:eta/F:phi/F:dR/F:dPhi/F:dEta/F' )
    newtree.Branch( 'HwithM', HwithM , 'HiggsFlag/I:mass/F:masswithFSR/F:pt/F:eta/F:phi/F:dR/F:dPhi/F:dEta/F' )	
    Event = array('f',[0])
    rho25 = array('f',[0])
    HVMass_Reg = array('f',[0])
    newtree.Branch('HVMass_Reg',HVMass_Reg,'HVMass_Reg/F')
    fRho25 = ROOT.TTreeFormula("rho",'rho',tree)
    Jet_regWeight = array('f',[0]*2)
    Jet_MET_dPhiArray = [array('f',[0]),array('f',[0])]
    Jet_rawPtArray = [array('f',[0]),array('f',[0])]
    newtree.Branch('Jet_regWeight',Jet_regWeight,'Jet_regWeight[2]/F')
    readerJet0 = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet1 = ROOT.TMVA.Reader("!Color:!Silent" )
        
    hJ0 = ROOT.TLorentzVector()
    hJ1 = ROOT.TLorentzVector()

     	


    theForms = {}
    theVars0 = {}
    theVars1 = {}
    
    def addVarsToReader(reader,theVars,theForms,i):
        for key in regVars:
	    print key	
            var = regDict[key]
            theVars[key] = array( 'f', [ 0 ] )
            reader.AddVariable(key,theVars[key])
            formula = regDict[key].replace("[0]","[%.0f]" %i)
            print 'Adding var: %s with %s to readerJet%.0f' %(key,formula,i)
            theForms['form_reg_%s_%.0f'%(key,i)] = formula #ROOT.TTreeFormula("form_reg_%s_%.0f"%(key,i),'%s' %(formula),tree)
        return

    addVarsToReader(readerJet0,theVars0,theForms,0)
    addVarsToReader(readerJet1,theVars1,theForms,1)
    readerJet0.BookMVA( "jet0Regression", regWeight )
    readerJet1.BookMVA( "jet1Regression", regWeight )
    #print theForms	 


    for entry in range(0,nEntries):
            tree.GetEntry(entry)
	    Event[0]=tree.evt

            if entry % 10000 is 0: print '---> Event # ', entry 


	    Jet_pt_0 = tree.Jet_pt[tree.hJCidx[0]]
            Jet_pt_1 = tree.Jet_pt[tree.hJCidx[1]]
            Jet_eta_0 = tree.Jet_eta[tree.hJCidx[0]]
            Jet_eta_1 = tree.Jet_eta[tree.hJCidx[1]]
            Jet_m_0 = tree.Jet_mass[tree.hJCidx[0]]
            Jet_m_1 = tree.Jet_mass[tree.hJCidx[1]]
            Jet_phi_0 = tree.Jet_phi[tree.hJCidx[0]]
            Jet_phi_1 = tree.Jet_phi[tree.hJCidx[1]]
            hJ0.SetPtEtaPhiM(Jet_pt_0,Jet_eta_0,Jet_phi_0,Jet_m_0)
            hJ1.SetPtEtaPhiM(Jet_pt_1,Jet_eta_1,Jet_phi_1,Jet_m_1)
            Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()
            Jet_met_dPhi_0 =   deltaPhi(tree.met_phi,Jet_phi_0)
            Jet_met_dPhi_1 =   deltaPhi(tree.met_phi,Jet_phi_1)
            met_pt_0 = tree.met_pt
            met_pt_1 = tree.met_pt
            Jet_vtxPt_0 = tree.Jet_vtxPt[tree.hJCidx[0]]
            Jet_vtxPt_1 = tree.Jet_vtxPt[tree.hJCidx[1]]
            Jet_vtx3dL_0= tree.Jet_vtx3DVal[tree.hJCidx[0]]
            Jet_vtx3dL_1= tree.Jet_vtx3DVal[tree.hJCidx[1]]
            Jet_vtx3deL_0= tree.Jet_vtx3DSig[tree.hJCidx[0]]
            Jet_vtx3deL_1= tree.Jet_vtx3DSig[tree.hJCidx[1]]
            Jet_vtxMass_0= tree.Jet_vtxMass[tree.hJCidx[0]]
            Jet_vtxMass_1= tree.Jet_vtxMass[tree.hJCidx[1]]
            Jet_vtxNtrk_0= tree.Jet_vtxNtracks[tree.hJCidx[0]]
            Jet_vtxNtrk_1= tree.Jet_vtxNtracks[tree.hJCidx[1]]
            Jet_chEmEF_0=tree.Jet_chEmEF[tree.hJCidx[0]]
            Jet_chEmEF_1=tree.Jet_chEmEF[tree.hJCidx[1]]
            Jet_chHEF_0=tree.Jet_chHEF[tree.hJCidx[0]]
            Jet_chHEF_1=tree.Jet_chHEF[tree.hJCidx[1]]
            Jet_neHEF_0=tree.Jet_neHEF[tree.hJCidx[0]]
            Jet_neHEF_1=tree.Jet_neHEF[tree.hJCidx[1]]
            Jet_neEmEF_0=tree.Jet_neEmEF[tree.hJCidx[0]]
            Jet_neEmEF_1=tree.Jet_neEmEF[tree.hJCidx[1]]
            #Jet_mcPt_0 = tree.Jet_mcPt[tree.hJCidx[0]]
            #Jet_mcPt_1 = tree.Jet_mcPt[tree.hJCidx[1]]
            Jet_rawPt_0 = tree.Jet_rawPt[tree.hJCidx[0]]
            Jet_rawPt_1 = tree.Jet_rawPt[tree.hJCidx[1]]

            if sample == 'Zuu' or sample == 'Zee':
                 Jet_corr_0 = Jet_pt_0/Jet_rawPt_0
                 Jet_corr_1 = Jet_pt_1/Jet_rawPt_1
                
            else:    
                Jet_corr_0 = tree.Jet_corr[tree.hJCidx[0]]
                Jet_corr_1 = tree.Jet_corr[tree.hJCidx[1]]
            

            #Jet_JECUnc_0 = tree.Jet_JECUnc[tree.hJCidx[0]]
            #Jet_JECUnc_1 = tree.Jet_JECUnc[tree.hJCidx[1]]
            Jet_chMult_0 = tree.Jet_chMult[tree.hJCidx[0]]
            Jet_chMult_1 = tree.Jet_chMult[tree.hJCidx[1]]
            Jet_leadTrackPt_0 = tree.Jet_leadTrackPt[tree.hJCidx[0]]
            Jet_leadTrackPt_1 = tree.Jet_leadTrackPt[tree.hJCidx[1]]
            Jet_leptonPtRel_0 = tree.Jet_leptonPtRel[tree.hJCidx[0]]
            Jet_leptonPtRel_1= tree.Jet_leptonPtRel[tree.hJCidx[1]]
            Jet_leptonDeltaR_0 = tree.Jet_leptonDeltaR[tree.hJCidx[0]]
            Jet_leptonDeltaR_1 = tree.Jet_leptonDeltaR[tree.hJCidx[0]]
            Jet_leptonPt_0 = tree.Jet_leptonPt[tree.hJCidx[0]]
            Jet_leptonPt_1= tree.Jet_leptonPt[tree.hJCidx[1]]
            rho_0=tree.rho
            rho_1=tree.rho
 
            #corrRes0 = corrPt(Jet_pt_0,Jet_eta_0,Jet_mcPt_0)
            #corrRes1 = corrPt(Jet_pt_1,Jet_eta_1,Jet_mcPt_1)
            #Jet_rawPt_0 *= corrRes0
            #Jet_rawPt_1 *= corrRes1
            # Jet_rawPtArray[0][0] = Jet_rawPt_0
            #Jet_rawPtArray[1][0] = Jet_rawPt_1
            
	
	    for key in regVars:
                #print key	
                    theVars0[key][0] = eval("%s_0" %(key)) #theForms["form_reg_%s_0" %(key)].EvalInstance()
                    theVars1[key][0] =  eval("%s_1" %(key)) #theForms["form_reg_%s_1" %(key)].EvalInstance()
                    
	    if applyRegression:
                HNoReg.HiggsFlag = 1
                HNoReg.mass = (hJ0+hJ1).M()
                HNoReg.pt = (hJ0+hJ1).Pt()
                HNoReg.eta = (hJ0+hJ1).Eta()
                HNoReg.phi = (hJ0+hJ1).Phi()
                HNoReg.dR = hJ0.DeltaR(hJ1)
                HNoReg.dPhi = hJ0.DeltaPhi(hJ1)
                HNoReg.dEta = abs(hJ0.Eta()-hJ1.Eta())
	        HNoRegwithFSR = ROOT.TLorentzVector()
                HNoRegwithFSR.SetPtEtaPhiM(HNoReg.pt,HNoReg.eta,HNoReg.phi,HNoReg.mass)
                
                HNoRegwithFSR = addAdditionalJets(HNoRegwithFSR,tree)
		HNoReg.masswithFSR = HNoRegwithFSR.M()
                rPt0 = max(0.0001,readerJet0.EvaluateRegression( "jet0Regression" )[0])
                rPt1 = max(0.0001,readerJet1.EvaluateRegression( "jet1Regression" )[0])
                Jet_regWeight[0] = rPt0/Jet_pt_0
                Jet_regWeight[1] = rPt1/Jet_pt_1
                hJ0.SetPtEtaPhiM(rPt0,Jet_eta_0,Jet_phi_0,0.)#tree.Jet_mass[0])
                hJ1.SetPtEtaPhiM(rPt1,Jet_eta_1,Jet_phi_1,0.)#tree.Jet_mass[1])
                tree.Jet_pt[0] = rPt0
                tree.Jet_pt[1] = rPt1
                H.HiggsFlag = 1
                H.mass = (hJ0+hJ1).M()
                H.pt = (hJ0+hJ1).Pt()
                H.eta = (hJ0+hJ1).Eta()
                H.phi = (hJ0+hJ1).Phi()
                H.dR = hJ0.DeltaR(hJ1)
                H.dPhi = hJ0.DeltaPhi(hJ1)
                H.dEta = abs(hJ0.Eta()-hJ1.Eta())
		hJ0.SetPtEtaPhiM(rPt0,Jet_eta_0,Jet_phi_0,4.8)#tree.Jet_mass[0])
                hJ1.SetPtEtaPhiM(rPt1,Jet_eta_1,Jet_phi_1,4.8)#tree.Jet_mass[1])
		HRegwithFSR = ROOT.TLorentzVector()
                HRegwithFSR.SetPtEtaPhiM(H.pt,H.eta,H.phi,H.mass)

                HRegwithFSR = addAdditionalJets(HRegwithFSR,tree)
		H.masswithFSR = HRegwithFSR.M()
		HwithM.mass = (hJ0+hJ1).M()
		#print HwithM.mass
                HwithM.pt = (hJ0+hJ1).Pt()
                HwithM.eta = (hJ0+hJ1).Eta()
                HwithM.phi = (hJ0+hJ1).Phi()
                HwithM.dR = hJ0.DeltaR(hJ1)
                HwithM.dPhi = hJ0.DeltaPhi(hJ1)
                HwithM.dEta = abs(hJ0.Eta()-hJ1.Eta())
		HRegwithMwithFSR = ROOT.TLorentzVector()
                HRegwithMwithFSR.SetPtEtaPhiM(HwithM.pt,HwithM.eta,HwithM.phi,HwithM.mass)

                HRegwithMwithFSR = addAdditionalJets(HRegwithMwithFSR,tree)
		HwithM.masswithFSR = HRegwithMwithFSR.M()

                if (Jet_regWeight[0] > 5. or Jet_regWeight[1] > 5. ) :
                    print 'Event %.0f' %(Event[0])
                    print 'corr 0 %.2f' %(Jet_regWeight[0])
                    print 'corr 1 %.2f' %(Jet_regWeight[1])
                    print 'rPt0 %.2f' %(rPt0)
                    print 'rPt1 %.2f' %(rPt1)
                    print 'rE0 %.2f' %(rE0)
                    print 'rE1 %.2f' %(rE1)
                    print 'Mass %.2f' %(H.mass)

            
            newtree.Fill()
        
    newtree.AutoSave()
    output.Close()
        
