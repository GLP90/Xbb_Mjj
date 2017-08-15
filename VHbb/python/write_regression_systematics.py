#! /usr/bin/env python
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


#Usage: ./write_regression_systematic.py path

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
#tmpDir = os.environ["TMPDIR"]

name = config.get('TrainRegression', 'name')

#print 'INput samples:\t%s'%pathIN
#print 'OUTput samples:\t%s'%pathOUT+name

namelist=opts.names.split(',')

#load info
info = ParseInfo(samplesinfo,pathIN)

# counter object
count = Counter()

def computeSF_leg(leg):
    #leg is the leg index, can be 0 or 1
    eff_leg = [1.,0.,0.]
    eff_leg[0] = (weight[leg][0])
    eff_leg[1] = weight[leg][0]-weight[leg][1]
    eff_leg[2] = weight[leg][0]+weight[leg][1]
    return eff_leg

def computeEventSF_fromleg(effleg1, effleg2):
    #returns event efficiency and relative uncertainty
    eff_event = [1.,0.]
    eff_event[0] = ((effleg1[0][0]**2*effleg2[1][0] + effleg1[1][0]**2*effleg2[0][0])/(effleg1[0][0] + effleg1[1][0]))
    #relative uncertainty down
    uncert_down = (abs(((effleg1[0][1]**2*effleg2[1][1] + effleg1[1][1]**2*effleg2[0][1])/(effleg1[0][1] + effleg1[1][1])) - eff_event[0])/eff_event[0])
    #relative uncertainty up
    uncert_up = (abs(((effleg1[0][2]**2*effleg2[1][2] + effleg1[1][2]**2*effleg2[0][2])/(effleg1[0][2] + effleg1[1][2])) - eff_event[0])/eff_event[0])
    eff_event[1]  = (uncert_down+uncert_up)/2.
    return eff_event

def computeEvenSF_DZ(eff):
    eff_event = [1.,0.]
    eff_event[0] = ((eff[0][0]**2 + eff[1][0]**2)/(eff[0][0] + eff[1][0]))
    #relative uncertainty down
    uncert_down = (((eff[0][1]**2 + eff[1][1]**2)/(eff[0][1] + eff[1][1])) - eff_event[0])/eff_event[0]
    #relative uncertainty up
    uncert_up = (((eff[0][2]**2 + eff[1][2]**2)/(eff[0][2] + eff[1][2])) - eff_event[0])/eff_event[0]
    eff_event[1]  = (uncert_down+uncert_up)/2.
    return eff_event

def getLumiAvrgSF(weightLum1, lum1, weightLum2, lum2, weight_SF):
    weight_SF[0] = weightLum1[0]*lum1+weightLum2[0]*lum2
    weight_SF[1] = weightLum1[1]*lum1+weightLum2[1]*lum2
    weight_SF[2] = weightLum1[2]*lum1+weightLum2[2]*lum2

def computeEff(weight_Eff):
    eff1 = []
    eff2 = []
    eff1.append(weight[0][0])
    eff1.append(weight[0][0]-weight[0][1])
    eff1.append(weight[0][0]+weight[0][1])
    eff2.append(weight[1][0])
    eff2.append(weight[1][0]-weight[1][1])
    eff2.append(weight[1][0]+weight[1][1])
    weight_Eff[0] = (eff1[0]*(1-eff2[0])*eff1[0] + eff2[0]*(1-eff1[0])*eff2[0] + eff1[0]*eff1[0]*eff2[0]*eff2[0])
    weight_Eff[1] = (eff1[1]*(1-eff2[1])*eff1[1] + eff2[1]*(1-eff1[1])*eff2[1] + eff1[1]*eff1[1]*eff2[1]*eff2[1])
    weight_Eff[2] = (eff1[2]*(1-eff2[2])*eff1[2] + eff2[2]*(1-eff1[2])*eff2[2] + eff1[2]*eff1[2]*eff2[2]*eff2[2])
    return weight_Eff

def computeWeight(a, b):
    weight = []
    weight.append([])
    weight.append([])
    for i in range(2):
        weight[i].append(a*muTrigEffBfr[i][0] + b*muTrigEffAftr[i][0])
        weight[i].append(math.sqrt((a*muTrigEffBfr[i][1])**2 + (b*muTrigEffAftr[i][1])**2))
    return weight



def deltaPhi(phi1, phi2): 
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result


def deltaR(phi1, eta1, phi2, eta2):
    deta = eta1-eta2
    dphi = deltaPhi(phi1, phi2)
    result = math.sqrt(deta*deta + dphi*dphi)
    return result


def signal_ewk(GenVbosons_pt):
	
	SF = 1.
	#print 'Vpt:', GenVbosons_pt
	EWK = [0.932072955817,
	       0.924376254386,
	       0.916552449249,
	       0.909654343838,
	       0.90479110736,
	       0.902244634267,
	       0.89957486928,
	       0.902899199569,
	       0.899314861082,
	       0.89204902646,
	       0.886663993587,
	       0.878915415638,
	       0.870241565009,
	       0.863239359219,
	       0.85727925851,
	       0.849770804948,
	       0.83762562793,
	       0.829982098864,
	       0.81108451152,
	       0.821942287438,
	       0.79,
	       0.79,
	       0.79,
	       0.79,
	       0.79]
	
	#print EWK[0]
	#print EWK[1]

	if GenVbosons_pt > 0. and GenVbosons_pt < 3000:

		if GenVbosons_pt > 0 and GenVbosons_pt <= 20:
			SF = EWK[0]
		if GenVbosons_pt > 20 and GenVbosons_pt <= 40:
			SF = EWK[1]
		if GenVbosons_pt > 40 and GenVbosons_pt <= 60:
			SF = EWK[2]
		if GenVbosons_pt > 60 and GenVbosons_pt <= 80:
			SF = EWK[3]
		if GenVbosons_pt > 80 and GenVbosons_pt <= 100:
			SF = EWK[4]
		if GenVbosons_pt > 100 and GenVbosons_pt <= 120:
			SF = EWK[5]
		if GenVbosons_pt > 120 and GenVbosons_pt <= 140:
			SF = EWK[6]
		if GenVbosons_pt > 140 and GenVbosons_pt <= 160:
			SF = EWK[7]
		if GenVbosons_pt > 160 and GenVbosons_pt <= 180:
			SF = EWK[8]
		if GenVbosons_pt > 180 and GenVbosons_pt <= 200:
			SF = EWK[9]
		if GenVbosons_pt > 200 and GenVbosons_pt <= 220:
			SF = EWK[10]
		if GenVbosons_pt > 220 and GenVbosons_pt <= 240:
			SF = EWK[11]
		if GenVbosons_pt > 240 and GenVbosons_pt <= 260:
			SF = EWK[12]
		if GenVbosons_pt > 260 and GenVbosons_pt <= 280:
			SF = EWK[13]
		if GenVbosons_pt > 280 and GenVbosons_pt <= 300:
			SF = EWK[14]
		if GenVbosons_pt > 300 and GenVbosons_pt <= 320:
			SF = EWK[15]
		if GenVbosons_pt > 320 and GenVbosons_pt <= 340:
			SF = EWK[16]
		if GenVbosons_pt > 340 and GenVbosons_pt <= 360:
			SF = EWK[17]
		if GenVbosons_pt > 360 and GenVbosons_pt <= 380:
			SF = EWK[18]
		if GenVbosons_pt > 380 and GenVbosons_pt <= 400:
			SF = EWK[19]
		if GenVbosons_pt > 400 and GenVbosons_pt <= 420:
			SF = EWK[20]
		if GenVbosons_pt > 420 and GenVbosons_pt <= 440:
			SF = EWK[21]
		if GenVbosons_pt > 440 and GenVbosons_pt <= 460:
			SF = EWK[22]
		if GenVbosons_pt > 460 and GenVbosons_pt <= 480:
			SF = EWK[23]
		if GenVbosons_pt > 480:
			SF = EWK[24]
		if GenVbosons_pt <= 0:
			SF = 1


	return SF

def signal_ewk_up(GenVbosons_pt):
	
	SF = 1.
	#print 'Vpt:', GenVbosons_pt
	EWK = [0.933479852292,
	       0.925298220882,
	       0.917622981133,
	       0.91102286158,
	       0.90718076681,
	       0.905350232844,
	       0.90336604675,
	       0.903947932682,
	       0.903377015003,
	       0.897282669087,
	       0.892978480734,
	       0.885729935121,
	       0.878913596976,
	       0.872505666469,
	       0.866859512888,
	       0.860942354659,
	       0.850346790893,
	       0.844431351897,
	       0.829520542725,
	       0.837419206895,
	       0.81,
	       0.81,
	       0.81,
	       0.81,
	       0.81
	       ]
	
	if GenVbosons_pt > 0. and GenVbosons_pt < 3000:

		if GenVbosons_pt > 0 and GenVbosons_pt <= 20:
			SF = EWK[0]
		if GenVbosons_pt > 20 and GenVbosons_pt <= 40:
			SF = EWK[1]
		if GenVbosons_pt > 40 and GenVbosons_pt <= 60:
			SF = EWK[2]
		if GenVbosons_pt > 60 and GenVbosons_pt <= 80:
			SF = EWK[3]
		if GenVbosons_pt > 80 and GenVbosons_pt <= 100:
			SF = EWK[4]
		if GenVbosons_pt > 100 and GenVbosons_pt <= 120:
			SF = EWK[5]
		if GenVbosons_pt > 120 and GenVbosons_pt <= 140:
			SF = EWK[6]
		if GenVbosons_pt > 140 and GenVbosons_pt <= 160:
			SF = EWK[7]
		if GenVbosons_pt > 160 and GenVbosons_pt <= 180:
			SF = EWK[8]
		if GenVbosons_pt > 180 and GenVbosons_pt <= 200:
			SF = EWK[9]
		if GenVbosons_pt > 200 and GenVbosons_pt <= 220:
			SF = EWK[10]
		if GenVbosons_pt > 220 and GenVbosons_pt <= 240:
			SF = EWK[11]
		if GenVbosons_pt > 240 and GenVbosons_pt <= 260:
			SF = EWK[12]
		if GenVbosons_pt > 260 and GenVbosons_pt <= 280:
			SF = EWK[13]
		if GenVbosons_pt > 280 and GenVbosons_pt <= 300:
			SF = EWK[14]
		if GenVbosons_pt > 300 and GenVbosons_pt <= 320:
			SF = EWK[15]
		if GenVbosons_pt > 320 and GenVbosons_pt <= 340:
			SF = EWK[16]
		if GenVbosons_pt > 340 and GenVbosons_pt <= 360:
			SF = EWK[17]
		if GenVbosons_pt > 360 and GenVbosons_pt <= 380:
			SF = EWK[18]
		if GenVbosons_pt > 380 and GenVbosons_pt <= 400:
			SF = EWK[19]
		if GenVbosons_pt > 400 and GenVbosons_pt <= 420:
			SF = EWK[20]
		if GenVbosons_pt > 420 and GenVbosons_pt <= 440:
			SF = EWK[21]
		if GenVbosons_pt > 440 and GenVbosons_pt <= 460:
			SF = EWK[22]
		if GenVbosons_pt > 460 and GenVbosons_pt <= 480:
			SF = EWK[23]
		if GenVbosons_pt > 480:
			SF = EWK[24]
		if GenVbosons_pt <= 0:
			SF = 1


	return SF

def signal_ewk_down(GenVbosons_pt):
	
	SF = 1.
	#print 'Vpt:', GenVbosons_pt
	EWK = [0.930666059342,
	       0.923454287889,
	       0.915481917365,
	       0.908285826095,
	       0.90240144791,
	       0.89913903569,
	       0.895783691809,
	       0.895150466456,
	       0.895252707162,
	       0.886815383834,
	       0.88034950644,
	       0.872100896154,
	       0.861569533042,
	       0.853973051969,
	       0.847699004132,
	       0.838599255237,
	       0.824904464966,
	       0.815532845831,
	       0.792648480316,
	       0.806465367982,
	       0.79,
	       0.79,
	       0.79,
	       0.79,
	       0.79
	       ]
	
	if GenVbosons_pt > 0. and GenVbosons_pt < 3000:

		if GenVbosons_pt > 0 and GenVbosons_pt <= 20:
			SF = EWK[0]
		if GenVbosons_pt > 20 and GenVbosons_pt <= 40:
			SF = EWK[1]
		if GenVbosons_pt > 40 and GenVbosons_pt <= 60:
			SF = EWK[2]
		if GenVbosons_pt > 60 and GenVbosons_pt <= 80:
			SF = EWK[3]
		if GenVbosons_pt > 80 and GenVbosons_pt <= 100:
			SF = EWK[4]
		if GenVbosons_pt > 100 and GenVbosons_pt <= 120:
			SF = EWK[5]
		if GenVbosons_pt > 120 and GenVbosons_pt <= 140:
			SF = EWK[6]
		if GenVbosons_pt > 140 and GenVbosons_pt <= 160:
			SF = EWK[7]
		if GenVbosons_pt > 160 and GenVbosons_pt <= 180:
			SF = EWK[8]
		if GenVbosons_pt > 180 and GenVbosons_pt <= 200:
			SF = EWK[9]
		if GenVbosons_pt > 200 and GenVbosons_pt <= 220:
			SF = EWK[10]
		if GenVbosons_pt > 220 and GenVbosons_pt <= 240:
			SF = EWK[11]
		if GenVbosons_pt > 240 and GenVbosons_pt <= 260:
			SF = EWK[12]
		if GenVbosons_pt > 260 and GenVbosons_pt <= 280:
			SF = EWK[13]
		if GenVbosons_pt > 280 and GenVbosons_pt <= 300:
			SF = EWK[14]
		if GenVbosons_pt > 300 and GenVbosons_pt <= 320:
			SF = EWK[15]
		if GenVbosons_pt > 320 and GenVbosons_pt <= 340:
			SF = EWK[16]
		if GenVbosons_pt > 340 and GenVbosons_pt <= 360:
			SF = EWK[17]
		if GenVbosons_pt > 360 and GenVbosons_pt <= 380:
			SF = EWK[18]
		if GenVbosons_pt > 380 and GenVbosons_pt <= 400:
			SF = EWK[19]
		if GenVbosons_pt > 400 and GenVbosons_pt <= 420:
			SF = EWK[20]
		if GenVbosons_pt > 420 and GenVbosons_pt <= 440:
			SF = EWK[21]
		if GenVbosons_pt > 440 and GenVbosons_pt <= 460:
			SF = EWK[22]
		if GenVbosons_pt > 460 and GenVbosons_pt <= 480:
			SF = EWK[23]
		if GenVbosons_pt > 480:
			SF = EWK[24]
		if GenVbosons_pt <= 0:
			SF = 1


	return SF

					

def resolutionBias(eta):
    if(eta< 0.5): return 0.052
    if(eta< 1.1): return 0.057
    if(eta< 1.7): return 0.096
    if(eta< 2.3): return 0.134
    if(eta< 5): return 0.28
    return 0

def corrPt(pt,eta,mcPt):
    return (pt+resolutionBias(math.fabs(eta))*(pt-mcPt))/pt

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


def addAdditionalJets(H, tree):

    for i in range(tree.nhjidxaddJetsdR08):
	    
        idx = tree.hjidxaddJetsdR08[i]
	
	if (idx == tree.hJCidx[0]) or (idx == tree.hJCidx[1]): continue
        
	if tree.Jet_puId[idx] < 4: continue
	
	if tree.Jet_pt_reg[idx] < 15: continue

	if tree.Jet_id[idx] < 3: continue

	addjet = ROOT.TLorentzVector()
	
	addjet.SetPtEtaPhiM(tree.Jet_pt_reg[idx], tree.Jet_eta[idx], tree.Jet_phi[idx], tree.Jet_mass[idx])
	
	H = H + addjet

	#print 'H mass + FSR:', H.M()
	#print 'H PT + FSR  :', H.Pt()

    return H

def projectionMETOntoJet(met, metphi, jet, jetphi, onlyPositive=True, threshold = math.pi/4.0):
  deltaphi = deltaPhi(metphi, jetphi)
  projection = met * math.cos(deltaphi)  
  if onlyPositive and abs(deltaphi) >= threshold:
      return 0.0
  else:
      return projection

def projMetOntoH(ev, tryAlsoWNoLept, recoverAlsoFSR):

  if len(ev.hJCidx)<2:
    return ev.HCSV_mass
  lep0pt = ev.Jet_leptonPt[ev.hJCidx[0]]
  lep1pt = ev.Jet_leptonPt[ev.hJCidx[1]]

  nu = ROOT.TLorentzVector()
  j0 = ROOT.TLorentzVector()
  j1 = ROOT.TLorentzVector()
  j0.SetPtEtaPhiM( ev.Jet_pt_reg[ev.hJCidx[0]],  ev.Jet_eta[ev.hJCidx[0]],  ev.Jet_phi[ev.hJCidx[0]],  ev.Jet_mass[ev.hJCidx[0]])
  j1.SetPtEtaPhiM( ev.Jet_pt_reg[ev.hJCidx[1]],  ev.Jet_eta[ev.hJCidx[1]],  ev.Jet_phi[ev.hJCidx[1]],  ev.Jet_mass[ev.hJCidx[1]])

  proj0 = projectionMETOntoJet(ev.met_pt, ev.met_phi, j0.Pt() , j0.Phi(), False, 999)
  dPhi0= deltaPhi(ev.met_phi,  j0.Phi())    
  proj1 = projectionMETOntoJet(ev.met_pt, ev.met_phi, j1.Pt() ,j1.Phi(), False, 999)
  dPhi1= deltaPhi(ev.met_phi,  j1.Phi())    

  if recoverAlsoFSR:
      FSRjet = ROOT.TLorentzVector()
      idxtoAdd = []
      idxtoAdd =  [x for x in range(ev.nJet)  if ( x not in ev.hJCidx and ev.Jet_pt[x]>15. and abs(ev.Jet_eta[x])<3.0 and  ev.Jet_id[x]>=3 and ev.Jet_puId[x]>=4 and  min( deltaR(ev.Jet_eta[x],ev.Jet_phi[x], j0.Eta(), j0.Phi()), deltaR(ev.Jet_eta[x],ev.Jet_phi[x], j1.Eta(), j1.Phi() ) ) <0.8 )  ] 
      for ad in idxtoAdd:        
            FSRjet.SetPtEtaPhiM( ev.Jet_pt_reg[ad],  ev.Jet_eta[ad],  ev.Jet_phi[ad],  ev.Jet_mass[ad])
            dR0 = deltaR(ev.Jet_eta[ad],ev.Jet_phi[ad], j0.Eta(), j0.Phi() )
            dR1 = deltaR(ev.Jet_eta[ad],ev.Jet_phi[ad], j1.Eta(), j1.Phi() )
            if dR0<dR1:
                   j0 +=FSRjet
            else:
                   j1 +=FSRjet


  if not tryAlsoWNoLept:
      if (lep0pt>0 or lep1pt>0):  
              if ( (abs(dPhi0)<abs(dPhi1)) and lep0pt>0) :
                  nu.SetPtEtaPhiM( proj0,  j0.Eta(),  j0.Phi(), 0)
                  #j0+=nu
              elif ( (abs(dPhi0)>abs(dPhi1))  and lep1pt>0 ):
                  nu.SetPtEtaPhiM( proj1,  j1.Eta(),  j1.Phi(), 0)
                  #j1+=nu

      return (j0+j1).M()
 
  else : 
          if (abs(dPhi0)<abs(dPhi1)) :
                 nu.SetPtEtaPhiM( proj0,  j0.Eta(),  j0.Phi(), 0)
                 #j0+=nu
          else:
                 nu.SetPtEtaPhiM( proj1,  j1.Eta(),  j1.Phi(), 0)
                 #j1+=nu
  
  return (j0+j1).M()


def higgs_semiL_bias(pt, eta, IsSemiLepton):

	'''
	Returns a Higgs mass resolution correction vs pt/et for semi and non semiLeptonic jets
	'''
	
	bias = 1
	
	if IsSemiLepton:
		
            if pt > 50 and pt < 100: 
	        if eta < 0.9:	    
		    bias = abs((0.18-0.14)/0.18)
		if eta > 0.9 and eta < 1.6:
		    bias = abs((0.18-0.14)/0.18)	
		if eta > 1.6 and eta < 2.4:
			bias = abs((0.185-0.142)/0.185)

	    if pt > 100 and pt < 150:
                if eta < 0.9:
                    bias = abs((0.192-0.144)/0.192)
		if eta > 0.9 and eta < 1.6:
                    bias = abs((0.195-0.144)/0.195)
		if eta > 1.6 and eta < 2.4:
                    bias = abs((0.195-0.148)/0.195)
		    
	    if pt > 150:
		    if eta < 0.9:
			    bias = abs((0.157-0.136)/0.57)
		    if eta > 0.9 and eta < 1.6:
			    bias = abs((0.173-0.143)/0.173)
		    if eta > 1.6 and eta < 2.4:
			    bias = abs((0.169-0.146)/0.169)

	else:
		
            if pt > 50 and pt < 100: 
	        if eta < 0.9:	    
		    bias = abs((0.177-0.137)/0.177)
		if eta > 0.9 and eta < 1.6:
		    bias = abs((0.16-0.132)/0.16)	
		if eta > 1.6 and eta < 2.4:
                    bias = abs((0.18-0.136)/0.18)

	    if pt > 100 and pt < 150:
                if eta < 0.9:
                    bias = abs((0.159-0.13)/0.159)
		if eta > 0.9 and eta < 1.6:
                    bias = abs((0.156-0.128)/0.156)
		if eta > 1.6 and eta < 2.4:
                    bias = abs((0.159-0.132)/0.159)
		    
	    if pt > 150:
		    if eta < 0.9:
			    bias = abs((0.136-0.116)/0.136)
		    if eta > 0.9 and eta < 1.6:
			    bias = abs((0.142-0.118)/0.142)
		    if eta > 1.6 and eta < 2.4:
			    bias = abs((0.123-0.123)/0.123)

	return bias


# End Functions
# =============================================================================



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

    
    lhe_weight_map = False if not config.has_option('LHEWeights', 'weights_per_bin') else eval(config.get('LHEWeights', 'weights_per_bin'))
    
    #Set up offline b-weight calculation
    #csvpath = "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/data/csv"
    #csvpath = "./"
    #bweightcalc = BTagWeightCalculator(
	#    csvpath + "/csv_rwt_fit_hf_2015_12_14.root",
	#    csvpath + "/csv_rwt_fit_lf_2015_12_14.root"
	 #   )
    #bweightcalc.btag = "btagCSV"

    
    # make the input/output files    
    input  = ROOT.TFile.Open(pathIN+'/'+job.prefix+job.identifier+'.root','read')
    output = ROOT.TFile.Open(pathOUT+'/'+job.prefix+name+job.identifier+'.root','recreate')
    
    input.cd()

    if lhe_weight_map and 'DY' in job.name:
        inclusiveJob = info.get_sample('DY')
        print inclusiveJob.name
        inclusive = ROOT.TFile.Open(pathIN+inclusiveJob.get_path,'read')
        inclusive.cd()
        obj = ROOT.TObject
        for key in ROOT.gDirectory.GetListOfKeys():
            input.cd()
            obj = key.ReadObj()
            if obj.GetName() == job.tree:
                continue
            output.cd()
            obj.Write(key.GetName())
	inclusive.Close()
    else:
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
    #tree = input.Get('tree')
    nEntries = tree.GetEntries()

    print 'Input: ' , input
    print 'Output: ', output
    print 'job.tree:', job.tree
    print 'tree" ', tree
    print 'nEntries:', nEntries  


    output.cd()

    # For new regresssion zerop the branches out before cloning new tree
    #tree.SetBranchStatus('HCSV_reg_mass',0)
    #tree.SetBranchStatus('HCSV_reg_pt',0)
    #tree.SetBranchStatus('HCSV_reg_mass',0)
    #tree.SetBranchStatus('HCSV_reg_pt',0)

    #if job.type != 'DATA':
    #For new Vtype Zero out the old Vtype and recreat
    #     tree.SetBranchStatus('Vtype',0)
    # 	tree.SetBranchStatus('V_pt',0)
    # 	tree.SetBranchStatus('V_mass',0)
    # 	tree.SetBranchStatus('V_eta',0)
    # 	tree.SetBranchStatus('V_phi',0)
	
    # 	tree.SetBranchStatus('vLeptons_pt',0)
    # 	tree.SetBranchStatus('vLeptons_eta',0)
    # 	tree.SetBranchStatus('vLeptons_phi',0)
    # 	tree.SetBranchStatus('vLeptons_relIso04',0)
    # 	tree.SetBranchStatus('vLeptons_relIso03',0)
	
    
    newtree = tree.CloneTree(0)

    
    # if 'DY_inclusive' in job.name:
    #     Vtype_new = array('f',[0]*1)
    # 	newtree.Branch('Vtype_new', Vtype_new, 'Vtype_new/F')
    
    # 	V_new_pt = array('f',[0]*1)
    # 	newtree.Branch('V_new_pt', V_pt, 'V_new_pt/F')
    
    # 	V_new_eta = array('f',[0]*1)
    # 	newtree.Branch('V_new_eta', V_new_eta, 'V_new_eta/F')
	
    # 	V_new_phi = array('f',[0]*1)
    # 	newtree.Branch('V_new_phi', V_new_phi, 'V_new_phi/F')
    
    # 	V_new_mass = array('f',[0]*1)
    # 	newtree.Branch('V_new_mass', V_new_mass, 'V_new_mass/F')
    
    # 	vLeptons_new_pt = array('f',[0]*2)
    #     newtree.Branch('vLeptons_new_pt', vLeptons_new_pt, 'vLeptons_new_pt[2]/F')

    # 	vLeptons_new_eta = array('f',[0]*2)
    #     newtree.Branch('vLeptons_new_eta', vLeptons_new_eta, 'vLeptons_new_eta[2]/F')

    # 	vLeptons_new_phi = array('f',[0]*2)
    #     newtree.Branch('vLeptons_new_phi', vLeptons_new_phi, 'vLeptons_new_phi[2]/F')

    # 	vLeptons_new_relIso04 = array('f',[0]*2)
    #     newtree.Branch('vLeptons_new_relIso04', vLeptons_new_relIso04, 'vLeptons_new_relIso04[2]/F')
	
    # 	vLeptons_new_relIso03 = array('f',[0]*2)
    #     newtree.Branch('vLeptons_new_relIso03', vLeptons_new_relIso03, 'vLeptons_new_relIso03[2]/F')

    #regWeight = config.get("TrainRegression","regWeight")
    #regDict = eval(config.get("TrainRegression","regDict"))
    #regV_newars = eval(config.get("TrainRegression","regVars"))

    
    # hJ0 = ROOT.TLorentzVector()
    # hJ1 = ROOT.TLorentzVector()
    # hJ2 = ROOT.TLorentzVector()
    # vect = ROOT.TLorentzVector()

    # hJ0_reg = ROOT.TLorentzVector()
    # hJ1_reg = ROOT.TLorentzVector()

    # # for adding 3rd jet
    # hJ0_noReg = ROOT.TLorentzVector()
    # hJ1_noReg = ROOT.TLorentzVector()
    
    
    # #regWeightFilterJets = config.get("Regression","regWeightFilterJets")
    # #regDictFilterJets = eval(config.get("Regression","regDictFilterJets"))
    # #regVarsFilterJets = eval(config.get("Regression","regVarsFilterJets"))

    # # Standard Branches
    # HCSV_dR_reg   = array('f',[0]*1)
    # HCSV_dEta_reg = array('f',[0]*1)
    # HCSV_dPhi_reg = array('f',[0]*1)

    # newtree.Branch('HCSV_dR_reg', HCSV_dR_reg, 'HCSV_dR_reg[1]/F')
    # newtree.Branch('HCSV_dEta_reg', HCSV_dEta_reg, 'HCSV_dEta_reg[1]/F')
    # newtree.Branch('HCSV_dPhi_reg', HCSV_dEta_reg, 'HCSV_dPhi_reg[1]/F')
    
    # HVdPhi_reg = array('f',[0]*1)
    # newtree.Branch('HVdPhi_reg', HVdPhi_reg, 'HVdPhi_reg[1]/F')

    # HCSV_reg_pt_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_pt_FSR', HCSV_reg_pt_FSR, 'HCSV_reg_pt_FSR[1]/F')

    # # Higgs masses
    
    # HCSV_reg_mass_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_FSR', HCSV_reg_mass_FSR, 'HCSV_reg_mass_FSR[1]/F')

    # HCSV_reg_mass_FSR2 = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_FSR2', HCSV_reg_mass_FSR2, 'HCSV_reg_mass_FSR2[1]/F')

    # HCSV_reg_mass_met_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_met_FSR', HCSV_reg_mass_met_FSR, 'HCSV_reg_mass_met_FSR[1]/F')

    # HCSV_reg_mass_met = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_met', HCSV_reg_mass_met, 'HCSV_reg_mass_met[1]/F')

    # # Optional semiLepton decay only
    # HCSV_reg_mass_met_FSR_wSemiL = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_met_FSR_wSemiL', HCSV_reg_mass_met_FSR_wSemiL, 'HCSV_reg_mass_met_FSR_wSemiL[1]/F')

    # HCSV_reg_pt_FSR_wSemiL = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_pt_FSR_wSemiL', HCSV_reg_pt_FSR_wSemiL, 'HCSV_reg_pt_FSR_wSemiL[1]/F')

    # HCSV_reg_pt_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_pt_FSR', HCSV_reg_pt_FSR, 'HCSV_reg_pt_FSR[1]/F')
    
    # Jet_mt = array('f',[0]*2)
    # newtree.Branch('Jet_mt', Jet_mt, 'Jet_mt[2]/F')

    # # For higgs regression resolution
    # HReg_resolution = array('f',[0]*1)
    # newtree.Branch('HReg_resolution', HReg_resolution, 'HReg_resolution[1]/F')

    # # For Higgs semiLepton bias in pt/eta bins
    # Hreg_semiL_bias = array('f',[0]*1)
    # newtree.Branch('Hreg_semiL_bias', Hreg_semiL_bias, 'Hreg_semiL_bias[1]/F')


    # Recerate the jet pt and CMVA in their own branches
    hJetCMVA_pt_0 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_pt_0', hJetCMVA_pt_0, 'hJetCMVA_pt_0/F')
    
    hJetCMVA_pt_1 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_pt_1', hJetCMVA_pt_1, 'hJetCMVA_pt_1/F')

    #hJetCMVAV2_pt_reg_0 = array('f',[0]*1)
    #newtree.Branch('hJetCMVAV2_pt_reg_0', hJetCMVAV2_pt_reg_0, 'hJetCMVAV2_pt_reg_0/F')

    #hJetCMVAV2_pt_reg_1 = array('f',[0]*1)
    #newtree.Branch('hJetCMVAV2_pt_reg_1', hJetCMVAV2_pt_reg_1, 'hJetCMVAV2_pt_reg_1/F')

    hJetCMVA_btag_0 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_btag_0', hJetCMVA_btag_0, 'hJetCMVA_btag_0/F')

    hJetCMVA_btag_1 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_btag_1', hJetCMVA_btag_1, 'hJetCMVA_btag_1/F')

    hJetCMVA_eta_0 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_eta_0', hJetCMVA_eta_0, 'hJetCMVA_eta_0/F')

    hJetCMVA_eta_1 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_eta_1', hJetCMVA_eta_1, 'hJetCMVA_eta_1/F')
    
    hJetCMVA_index_0 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_index_0', hJetCMVA_index_0, 'hJetCMVA_index_0/F')

    hJetCMVA_index_1 = array('f',[0]*1)
    newtree.Branch('hJetCMVA_index_1', hJetCMVA_index_1, 'hJetCMVA_index_1/F')

    hJetCMVAV2_pt_reg = array('f',[0]*21)
    newtree.Branch('hJetCMVAV2_pt_reg', hJetCMVAV2_pt_reg, 'hJetCMVAV2_pt_reg[21]/F')
    
    

    # ========== Lepton SF branches ============

    # per event we have a weight that we fill based on vtype.  It is good for every event
    #lepton_EvtWeight = array('f',[0]*1)
    
    #newtree.Branch('lepton_EvtWeight',lepton_EvtWeight,'lepton_EvtWeight/F')

    vLeptons_SFweight_HLT = array('f',[0]*1)
    vLeptons_SFweight_HLT[0] = 1
    newtree.Branch('vLeptons_SFweight_HLT', vLeptons_SFweight_HLT, 'vLeptons_SFweight_HLT/F')

    eTrigSFWeight = array('f',[0]*1)
    newtree.Branch('eTrigSFWeight', eTrigSFWeight, 'eTrigSFWeight/F')

    eTrigSFWeight_ele23 = array('f',[0]*1)
    eTrigSFWeight_ele23[0] = 1
    newtree.Branch('eTrigSFWeight_ele23', eTrigSFWeight_ele23, 'eTrigSFWeight_ele23/F')

    eTrigSFWeight_ele27 = array('f',[0]*1)
    eTrigSFWeight_ele27[0] = 1
    newtree.Branch('eTrigSFWeight_ele27', eTrigSFWeight_ele27, 'eTrigSFWeight_ele27/F')

    eTrigSFWeight_ele27_BCDEF = array('f',[0]*1)
    newtree.Branch('eTrigSFWeight_ele27_BCDEF', eTrigSFWeight_ele27_BCDEF, 'eTrigSFWeight_ele27_BCDEF/F')

    # New for double ele
    eTrigSFWeight_doubleEle80x = array('f',[0]*1)
    eTrigSFWeight_doubleEle80xUp = array('f',[0]*1)
    eTrigSFWeight_doubleEle80xDown = array('f',[0]*1)
    newtree.Branch('eTrigSFWeight_doubleEle80x', eTrigSFWeight_doubleEle80x, 'eTrigSFWeight_doubleEle80x/F')
    newtree.Branch('eTrigSFWeight_doubleEle80xUp', eTrigSFWeight_doubleEle80xUp, 'eTrigSFWeight_doubleEle80xUp/F')
    newtree.Branch('eTrigSFWeight_doubleEle80xDown', eTrigSFWeight_doubleEle80xDown, 'eTrigSFWeight_doubleEle80xDown/F')

    eTrackerSFWeight = array('f',[0]*1)
    newtree.Branch('eTrackerSFWeight', eTrackerSFWeight, 'eTrackerSFWeight/F')

    eTrackerSFWeightUp = array('f',[0]*1)
    newtree.Branch('eTrackerSFWeightUp', eTrackerSFWeightUp, 'eTrackerSFWeightUp/F')

    eTrackerSFWeightDown = array('f',[0]*1)
    newtree.Branch('eTrackerSFWeightDown', eTrackerSFWeightDown, 'eTrackerSFWeightDown/F')

    eId80SFWeight = array('f',[0]*1)
    newtree.Branch('eId80SFWeight', eId80SFWeight, 'eId80SFWeight/F')

    eId90SFWeight = array('f',[0]*1)
    newtree.Branch('eId90SFWeight', eId90SFWeight, 'eId90SFWeight/F')

    eId90SFWeight_BCDEF = array('f',[0]*1)
    newtree.Branch('eId90SFWeight_BCDEF', eId90SFWeight_BCDEF, 'eId90SFWeight_BCDEF/F')

    mTrigSFWeight = array('f',[0]*1)
    newtree.Branch('mTrigSFWeight', mTrigSFWeight, 'mTrigSFWeight/F')

    mTrigSFWeight_ICHEP = array('f',[0]*1)
    mTrigSFWeight_ICHEP[0] = 1
    newtree.Branch('mTrigSFWeight_ICHEP', mTrigSFWeight_ICHEP, 'mTrigSFWeight_ICHEP/F')

    mTrackerSFWeight = array('f',[0]*1)
    newtree.Branch('mTrackerSFWeight', mTrackerSFWeight, 'mTrackerSFWeight/F')

    mTrackerSFWeightUp = array('f',[0]*1)
    newtree.Branch('mTrackerSFWeightUp', mTrackerSFWeightUp, 'mTrackerSFWeightUp/F')

    mTrackerSFWeightDown = array('f',[0]*1)
    newtree.Branch('mTrackerSFWeightDown', mTrackerSFWeightDown, 'mTrackerSFWeightDown/F')

    mIdSFWeight = array('f',[0]*1)
    newtree.Branch('mIdSFWeight', mIdSFWeight, 'mIdSFWeight/F')

    mIsoSFWeight = array('f',[0]*1)
    newtree.Branch('mIsoSFWeight', mIsoSFWeight, 'mIsoSFWeight/F')

    # New for double ele
    mTrigSFWeight_doubleMu80x = array('f',[0]*1)
    mTrigSFWeight_doubleMu80xUp = array('f',[0]*1)
    mTrigSFWeight_doubleMu80xDown = array('f',[0]*1)
    newtree.Branch('mTrigSFWeight_doubleMu80x', mTrigSFWeight_doubleMu80x, 'mTrigSFWeight_doubleMu80x/F')
    newtree.Branch('mTrigSFWeight_doubleMu80xUp', mTrigSFWeight_doubleMu80xUp, 'mTrigSFWeight_doubleMu80xUp/F')
    newtree.Branch('mTrigSFWeight_doubleMu80xDown', mTrigSFWeight_doubleMu80xDown, 'mTrigSFWeight_doubleMu80xDown/F')

    # # New for trigger string short cut
    # zee_trigger = zee_trigger = array('f',[0]*1)
    # newtree.Branch('zee_trigger',zee_trigger,'zee_trigger/F')
    
    # zuu_trigger = array('f',[0]*1)
    # newtree.Branch('zuu_trigger',zuu_trigger,'zuu_trigger/F')

    # # For DY special Weights
    DY_specialWeight = array('f',[0]*1)
    newtree.Branch('DY_specialWeight',DY_specialWeight,'DY_specialWeight/F')

    # # For LO/NLO Weighting
    NLO_Weight = array('f',[0]*1)
    newtree.Branch('NLO_Weight',NLO_Weight,'NLO_Weight/F')
    
    # for EWK reweighting
    DY_ewkWeight = array('f',[0]*1)
    newtree.Branch('DY_ewkWeight',DY_ewkWeight,'DY_ewkWeight/F')

    if 'DY' in job.name or 'ZZ_2L2Q' in job.name:
	    specialWeight = ROOT.TTreeFormula('specialWeight',job.specialweight, tree)
	    
    # for signal reweighting
    Signal_ewkWeight = array('f',[0]*1)
    newtree.Branch('Signal_ewkWeight',Signal_ewkWeight,'Signal_ewkWeight/F')
    
    Signal_ewkWeight_Up = array('f',[0]*1)
    newtree.Branch('Signal_ewkWeight_Up',Signal_ewkWeight_Up,'Signal_ewkWeight_Up/F')

    Signal_ewkWeight_Down = array('f',[0]*1)
    newtree.Branch('Signal_ewkWeight_Down',Signal_ewkWeight_Down,'Signal_ewkWeight_Down/F')
    
    
    mTrigSFWeightUp   = array('f',[0]*1)
    mTrigSFWeightDown = array('f',[0]*1)
    
    mIdSFWeightUp      = array('f',[0]*1)
    mIdSFWeightDown    = array('f',[0]*1)
    
    mIsoSFWeightUp     = array('f',[0]*1)
    mIsoSFWeightDown   = array('f',[0]*1)
    
    eId90SFWeightUp  = array('f',[0]*1)
    eId90SFWeightDown= array('f',[0]*1)
    
    eTrigSFWeightUp   = array('f',[0]*1)
    eTrigSFWeightDown = array('f',[0]*1)
    
    newtree.Branch('mTrigSFWeightUp',mTrigSFWeightUp,'mTrigSFWeightUp/F')
    newtree.Branch('mTrigSFWeightDown',mTrigSFWeightDown,'mTrigSFWeightDown/F')
    newtree.Branch('mIdSFWeightUp',mIdSFWeightUp,'mIdSFWeightUp/F')
    newtree.Branch('mIdSFWeightDown',mIdSFWeightDown,'mIdSFWeightDown/F')
    newtree.Branch('mIsoSFWeightUp',mIsoSFWeightUp,'mIsoSFWeightUp/F')
    newtree.Branch('mIsoSFWeightDown',mIsoSFWeightDown,'mIsoSFWeightDown/F')
    newtree.Branch('eId90SFWeightUp', eId90SFWeightUp, 'eId90SFWeightUp/F')
    newtree.Branch('eId90SFWeightDown', eId90SFWeightDown, 'eId90SFWeightDown/F')
    newtree.Branch('eTrigSFWeight', eTrigSFWeight, 'eTrigSFWeight/F')
    newtree.Branch('eTrigSFWeightDown', eTrigSFWeightDown, 'eTrigSFWeightDown/F')

    #########################################################################################

    
    print '\n\n======== Filling New Branches/ Applying Regression ========'
        
    for entry in range(0,nEntries):
	    
	    # for testing
	    #if entry > 1000: break
	    	    
            tree.GetEntry(entry)

	    if entry % 10000 is 0: print 'Event #', entry
	    

	    # Set the jet branches
	    hJetCMVA_pt_0[0] = tree.hJetCMVAV2_pt_reg_0
	    hJetCMVA_pt_1[0] = tree.hJetCMVAV2_pt_reg_1
	    
	    hJetCMVA_btag_0[0] = tree.Jet_btagCMVAV2[tree.hJCMVAV2idx[0]]
            hJetCMVA_btag_1[0] = tree.Jet_btagCMVAV2[tree.hJCMVAV2idx[1]]
	    
	    hJetCMVA_eta_0[0] = tree.Jet_eta[tree.hJCMVAV2idx[0]]
            hJetCMVA_eta_1[0] = tree.Jet_eta[tree.hJCMVAV2idx[1]]
	    
	    hJetCMVA_index_0[0] = tree.hJCMVAV2idx[0]
            hJetCMVA_index_1[0] = tree.hJCMVAV2idx[1]

	    for j in xrange(min(tree.nJet,21)):
		    hJetCMVAV2_pt_reg[j] = tree.Jet_pt_reg[j] 
	    
	    
	    #hJetCMVAV2_pt_reg[0] = tree.hJetCMVAV2_pt_reg_0
	    #hJetCMVAV2_pt_reg[1] = tree.hJetCMVAV2_pt_reg_1
	    	    
		    #print ptWeightEWK_Zll(tree.nGenVbosons[0], tree.GenVbosons_pt[0], tree.VtypeSim, tree.nGenTop, tree.nGenHiggsBoson)

	    # if tree.Vtype_new == 0 and (tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v==1 or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v==1 or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v==1 or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v==1):  
	    # 	    zuu_trigger[0] = 1
	    # else:
	    # 	    zuu_trigger[0] = 0


	    # if tree.Vtype_new == 1 and tree.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v == 1:
	    # 	    zee_trigger[0] = 1
            # else:
            #         zee_trigger[0] = 0


			    
	    if job.type != 'DATA':

		    # Set the fixed Vtype
		    # Vtype[0]   = tree.Vtype_new
		    # V_pt[0]    = tree.V_new_pt
		    # V_eta[0]   = tree.V_new_eta
		    # V_phi[0]   = tree.V_new_phi
		    # V_mass[0]  = tree.V_new_eta

		    # vLeptons_pt[0] = tree.vLeptons_new_pt[0]
		    # vLeptons_pt[1] = tree.vLeptons_new_pt[1]

		    # vLeptons_eta[0] = tree.vLeptons_new_eta[0]
                    # vLeptons_eta[1] = tree.vLeptons_new_eta[1]
		    
		    # vLeptons_phi[0] = tree.vLeptons_new_phi[0]
                    # vLeptons_phi[1] = tree.vLeptons_new_phi[1]

		    # vLeptons_relIso03[0] = tree.vLeptons_new_relIso03[0]
                    # vLeptons_relIso03[1] = tree.vLeptons_new_relIso03[1]

		    # vLeptons_relIso04[0] = tree.vLeptons_new_relIso04[0]
                    # vLeptons_relIso04[1] = tree.vLeptons_new_relIso04[1]

		    # Set the special Weight
		    if 'ZZ_2L2Q' in job.name:
			    specialWeight_ = specialWeight.EvalInstance()
			    DY_specialWeight[0] = specialWeight_
			    NLO_Weight[0] = 1		    
			    DY_ewkWeight[0] = 1
			    Signal_ewkWeight[0] = 1
			    Signal_ewkWeight_Up[0] = 1
			    Signal_ewkWeight_Down[0] = 1

		    elif 'DY' in job.name:
			    Signal_ewkWeight[0] = 1
			    Signal_ewkWeight_Up[0] = 1
			    Signal_ewkWeight_Down[0] = 1

			    specialWeight_ = specialWeight.EvalInstance()
			    DY_specialWeight[0] = specialWeight_
			    
			    # NLO weight
			    etabb = abs(tree.Jet_eta[tree.hJCidx[0]] - tree.Jet_eta[tree.hJCidx[1]])
			    if etabb < 5: 
				    NLO_Weight[0] = 1.153*(0.940679 + 0.0306119*etabb -0.0134403*etabb*etabb + 0.0132179*etabb*etabb*etabb -0.00143832*etabb*etabb*etabb*etabb)

			    # EWK weight
			    if len(tree.GenVbosons_pt) > 0 and tree.GenVbosons_pt[0] > 100. and  tree.GenVbosons_pt[0] < 3000:
				    DY_ewkWeight[0] = -0.1808051+6.04146*(pow((tree.GenVbosons_pt[0]+759.098),-0.242556))

		    elif 'ZH' in job.name and not 'ggZH' in job.name:
			    if tree.nGenVbosons > 0:
				     Signal_ewkWeight[0] = signal_ewk(tree.GenVbosons_pt[0])
				     Signal_ewkWeight_Up[0] = signal_ewk_up(tree.GenVbosons_pt[0])
				     Signal_ewkWeight_Down[0] = signal_ewk_down(tree.GenVbosons_pt[0])
			    else:
				    Signal_ewkWeight[0] = 1
				    Signal_ewkWeight_Up[0] = 1
				    Signal_ewkWeight_Down[0] = 1
				    
			    DY_specialWeight[0] = 1
			    NLO_Weight[0] = 1
                            DY_ewkWeight[0] = 1
					    
		    else:		    
			    Signal_ewkWeight[0] = 1
			    Signal_ewkWeight_Up[0] = 1
			    Signal_ewkWeight_Down[0] = 1
			    NLO_Weight[0] = 1
			    DY_ewkWeight[0] = 1
			    DY_specialWeight[0] = 1

			    
		    #print '\nDY Weight:', DY_specialWeight[0]
		    #print 'NLO weight:', NLO_Weight[0]
		    #print 'EWK weight:', DY_ewkWeight[0]
		    #print 'Signal EWK:', Signal_ewkWeight[0]
		    #print signal_ewk(tree.GenVbosons_pt[0])
		    
		    # ================ Lepton Scale Factors =================
		    # For custom made form own JSON files

		    eTrigSFWeight[0]    = 1
		    eId80SFWeight[0]    = 1

		    eId90SFWeight[0]    = 1
		    eId90SFWeightUp[0]    = 1
		    eId90SFWeightDown[0]    = 1

		    eId90SFWeight_BCDEF[0] = 1

		    eTrackerSFWeight[0] = 1
		    eTrackerSFWeightUp[0] = 1
		    eTrackerSFWeightDown[0] = 1

		    eTrigSFWeight_ele27[0] = 1
		    #eTrigSFWeight_ele27Up[0] = 1
		    #eTrigSFWeight_ele27Down[0] = 1
		    
		    eTrigSFWeight_ele27_BCDEF[0] = 1
		    
		    eTrigSFWeight_doubleEle80x[0] = 1
		    eTrigSFWeight_doubleEle80xUp[0] = 1
		    eTrigSFWeight_doubleEle80xDown[0] = 1

		    mIdSFWeight[0]      = 1
		    mIdSFWeightUp[0]      = 1
		    mIdSFWeightDown[0]      = 1

		    mTrackerSFWeight[0] = 1
		    mTrackerSFWeightUp[0] = 1
		    mTrackerSFWeightDown[0] = 1
		    
		    mTrigSFWeight[0]    = 1
		    mTrigSFWeightUp[0]    = 1
		    mTrigSFWeightDown[0]    = 1
		    
		    mIsoSFWeight[0] = 1
		    mIsoSFWeightUp[0] = 1
		    mIsoSFWeightDown[0] = 1
		    
		    mTrigSFWeight_ICHEP[0] = 1

		    mTrigSFWeight_doubleMu80x[0] = 1
		    mTrigSFWeight_doubleMu80xUp[0] = 1
		    mTrigSFWeight_doubleMu80xDown[0] = 1
		    
		    muTrigEffBfr1 = 1
		    muTrigEffBfr2 = 1
		    
		    muTrigEffAftr1 = 1
		    muTrigEffAftr2 = 1


		    muISO_BCDEF = 1
		    muISO_GH = 1
		    
		    muID_BCDEF= 1
		    muID_GH = 1
		    
		    mTrk_BCDEF= 1
                    mTrk_GH = 1
		    
		    eff1 = 1
		    eff2 = 1
		    
		    muID_BCDEF = [1.,0.,0.]
                    muID_GH = [1.,0.,0.]
                    muISO_BCDEF = [1.,0.,0.]
                    muISO_GH = [1.,0.,0.]
                    muTRK_BCDEF= [1.0,0.,0.]
                    muTRK_GH = [1.0,0.,0.]
                    btagSF = [1.,0.,0.]
                    #for muon trigger
                     #Run BCDEFG
                    effDataBCDEFG_leg8 = []
                    effDataBCDEFG_leg17= []
                    effMCBCDEFG_leg8= []
                    effMCBCDEFG_leg17 = []
                     #Run H
                    effDataH_leg8 = []
                    effDataH_leg17 = []
                    effMCH_leg8 = []
                    effMCH_leg17 = []
                     #Run H dZ
                    effDataH_DZ= []
                    effMCH_DZ= []

		    jsons = {
			    #### Muon trigger ISO, and ID ####
			    
			    # # ID
			    'myutils/jsons/80x/muon_ID_BCDEF.json' : ['MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta', 'abseta_pt_ratio'],
			    'myutils/jsons/80x/muon_ID_GH.json'    : ['MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta', 'abseta_pt_ratio'],
			    
			    # ISO
			    'myutils/jsons/80x/muon_ISO_BCDEF.json' : ['LooseISO_LooseID_pt_eta', 'abseta_pt_ratio'],
			    'myutils/jsons/80x/muon_ISO_GH.json'    : ['LooseISO_LooseID_pt_eta', 'abseta_pt_ratio'],

			    # tracker
			    'myutils/jsons/80x/trk_SF_RunBCDEF.json' : ['Graph', 'ratio_eff_eta3_dr030e030_corr'],
			    'myutils/jsons/80x/trk_SF_RunGH.json'    : ['Graph', 'ratio_eff_eta3_dr030e030_corr'],

			    # trigger
			    #BCDEFG
			    'myutils/jsons/80x/Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
			    'myutils/jsons/80x/Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
			    'myutils/jsons/80x/MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
			    'myutils/jsons/80x/MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
                            #H
			    #no DZ
			    'myutils/jsons/80x/Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
			    'myutils/jsons/80x/Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_DATA'],
			    'myutils/jsons/80x/MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg8.json' : ['MC_NUM_hlt_Mu17_Mu8_OR_TkMu8_leg8_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
			    'myutils/jsons/80x/MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg17.json' : ['MC_NUM_hlt_Mu17Mu8_leg17_DEN_LooseIDnISO_PAR_pt_eta', 'abseta_pt_MC'],
			    #with DZ
			    'myutils/jsons/80x/DATA_EfficienciesAndSF_dZ_numH.json' : ['MC_NUM_dZ_DEN_hlt_Mu17_Mu8_OR_TkMu8_loose_PAR_eta1_eta2', 'tag_abseta_abseta_DATA'],
			    'myutils/jsons/80x/MC_EfficienciesAndSF_dZ_numH.json' : ['MC_NUM_dZ_DEN_hlt_Mu17_Mu8_OR_TkMu8_loose_PAR_eta1_eta2', 'tag_abseta_abseta_MC'],


			    #### Electron trigger and ID ####
			    
			    # tracker
			    '../myMacros/scale_factors/80x/ScaleFactor_etracker_80x.json' : ['ScaleFactor_tracker_80x', 'eta_pt_ratio'],
			    
			    # MVAID
			    'myutils/jsons/80x/EIDISO_ZH_out.json' : ['EIDISO_ZH', 'eta_pt_ratio'],
			    
			    # coarse Binning
			    'myutils/jsons/80x/coarse_bin/EIDISO_ZH_out.json' : ['EIDISO_ZH', 'eta_pt_ratio'],
			    
			    # trigger
			    #'myutils/jsons/80x/DiEleLeg1AfterIDISO_out.json' : ['DiEleLeg1AfterIDISO', 'eta_pt_ratio'],
			    #'myutils/jsons/80x/DiEleLeg2AfterIDISO_out.json' : ['DiEleLeg2AfterIDISO', 'eta_pt_ratio']
			    
			    'myutils/jsons/80x/coarse_bin/DiEleLeg1AfterIDISO_out.json' : ['DiEleLeg1AfterIDISO', 'eta_pt_ratio'],
                            'myutils/jsons/80x/coarse_bin/DiEleLeg2AfterIDISO_out.json' : ['DiEleLeg2AfterIDISO', 'eta_pt_ratio']
			    
			    }

		    for j, name in jsons.iteritems():
			    
			    #print '\n New Json Iteration...'
			    #print j
			    #print name[0], name[1]
			    
			    weight = []
			    lepCorr = LeptonSF(j, name[0], name[1])
			    
			    if '_out' in j or 'ScaleFactor_etracker_80x' in j: 
				    #weight.append(lepCorr.get_2D_eta_pt(tree.vLeptons_new_eta[0], tree.vLeptons_new_pt[0]))
                                    #weight.append(lepCorr.get_2D_eta_pt(tree.vLeptons_new_eta[1], tree.vLeptons_new_pt[1]))
				    weight.append(lepCorr.get_2D( tree.vLeptons_new_pt[0], tree.vLeptons_new_eta[0]))
                                    weight.append(lepCorr.get_2D( tree.vLeptons_new_pt[1], tree.vLeptons_new_eta[1]))
				    

			    elif 'trk_SF_Run' not in j and 'EfficienciesAndSF_dZ_numH' not in j:
				    weight.append(lepCorr.get_2D( tree.vLeptons_new_pt[0], tree.vLeptons_new_eta[0]))
				    weight.append(lepCorr.get_2D( tree.vLeptons_new_pt[1], tree.vLeptons_new_eta[1]))

			    elif 'trk_SF_Run' not in j and 'EfficienciesAndSF_dZ_numH' in j:
				    weight.append(lepCorr.get_2D(tree.vLeptons_new_eta[0], tree.vLeptons_new_eta[1]))
				    weight.append(lepCorr.get_2D(tree.vLeptons_new_eta[1], tree.vLeptons_new_eta[0]))

			    elif 'trk_SF_Run' in j:	    
				    weight.append(lepCorr.get_1D(tree.vLeptons_new_eta[0]))
                                    weight.append(lepCorr.get_1D(tree.vLeptons_new_eta[1]))


			    if tree.Vtype_new == 0:
				    
				    if j.find('trk_SF_RunBCDEF') != -1:
					    mTrk_BCDEF     = weight[0][0]*weight[1][0]
					    mTrk_BCDEF_up   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            mTrk_BCDEF_down = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print mTrk_BCDEF

				    elif j.find('trk_SF_RunGH') != -1:
                                            mTrk_GH     = weight[0][0]*weight[1][0]
					    mTrk_GH_up   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            mTrk_GH_down = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print weight[0][0], weight[1][0]

				    elif j.find('muon_ID_BCDEF') != -1:
					    muID_BCDEF = weight[0][0]*weight[1][0]  
					    mIDSFWeightUp_BCDEF   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mIDSFWeightDown_BCDEF = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])

				    elif j.find('muon_ID_GH') != -1:
					    muID_GH = weight[0][0]*weight[1][0]
					    mIDSFWeightUp_GH  = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mIDSFWeightDown_GH = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muID_GH

				    elif j.find('muon_ISO_BCDEF') != -1:
					    muISO_BCDEF = weight[0][0]*weight[1][0]
					    mISOSFWeightUp_BCDEF   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mISOSFWeightDown_BCDEF = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muISO_BCDEF

				    elif j.find('muon_ISO_GH') != -1:
					    muISO_GH = weight[0][0]*weight[1][0]
					    mISOSFWeightUp_GH   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mISOSFWeightDown_GH = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muISO_GH

				    elif j.find('EfficienciesAndSF_doublehlt_perleg') != -1:
					    
					    if j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8') != -1:
						    effDataBCDEFG_leg8.append(computeSF_leg(0))
						    effDataBCDEFG_leg8.append(computeSF_leg(1))
					    elif j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17') != -1:
						    effDataBCDEFG_leg17.append(computeSF_leg(0))
						    effDataBCDEFG_leg17.append(computeSF_leg(1))
					    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg8') != -1:
						    effMCBCDEFG_leg8.append(computeSF_leg(0))
						    effMCBCDEFG_leg8.append(computeSF_leg(1))
					    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunBCDEFG_leg17') != -1:
						    effMCBCDEFG_leg17.append(computeSF_leg(0))
						    effMCBCDEFG_leg17.append(computeSF_leg(1))
					    elif j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg8') != -1:
						    effDataH_leg8.append(computeSF_leg(0))
						    effDataH_leg8.append(computeSF_leg(1))
					    elif j.find('Data_EfficienciesAndSF_doublehlt_perleg_RunH_leg17') != -1:
						    effDataH_leg17.append(computeSF_leg(0))
						    effDataH_leg17.append(computeSF_leg(1))
					    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg8') != -1:
						    effMCH_leg8.append(computeSF_leg(0))
						    effMCH_leg8.append(computeSF_leg(1))
					    elif j.find('MC_EfficienciesAndSF_doublehlt_perleg_RunH_leg17') != -1:
						    effMCH_leg17.append(computeSF_leg(0))
						    effMCH_leg17.append(computeSF_leg(1))
				    elif j.find('DATA_EfficienciesAndSF_dZ_numH') != -1:
					    effDataH_DZ.append(computeSF_leg(0))
					    effDataH_DZ.append(computeSF_leg(1))
				    elif j.find('MC_EfficienciesAndSF_dZ_numH') != -1:
					    effMCH_DZ.append(computeSF_leg(0))
					    effMCH_DZ.append(computeSF_leg(1))
					    

			    elif tree.Vtype_new == 1:
				    				    	    
				    if j.find('EIDISO_ZH_out') != -1:
					    eId90SFWeight[0] = weight[0][0]*weight[1][0]
					    eId90SFWeightUp[0] = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    eId90SFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    
				    elif j.find('DiEleLeg1AfterIDISO_out') != -1:
					    eff1 = weight[0][0]
					    eff1Up = (weight[0][0]+weight[0][1])
					    eff1Down = (weight[0][0]-weight[0][1])

				    elif j.find('DiEleLeg2AfterIDISO_out') != -1:
                                            eff2 = weight[1][0]
                                            eff2Up = (weight[1][0]+weight[1][1])
                                            eff2Down = (weight[1][0]-weight[1][1])

				    elif j.find('ScaleFactor_etracker_80x') != -1:
					    eTrackerSFWeight[0] = weight[0][0]*weight[1][0]
					    eTrackerSFWeightUp[0]   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            eTrackerSFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    
					    
                    # End JSON loop ====================================
					    
		    if tree.Vtype_new == 0:
			    
			    mIdSFWeight[0]     = muID_BCDEF*(20.1/36.4) + muID_GH*(16.3/36.4)
			    mIdSFWeightUp[0]   = mIDSFWeightUp_BCDEF*(20.1/36.4) + mIDSFWeightUp_GH*(16.3/36.4)
			    mIdSFWeightDown[0] = mIDSFWeightDown_BCDEF*(20.1/36.4) + mIDSFWeightDown_GH*(16.3/36.4)
			    
			    mIsoSFWeight[0]     = muISO_BCDEF*(20.1/36.4) + muISO_GH*(16.3/36.4)
                            mIsoSFWeightUp[0]   = mISOSFWeightUp_BCDEF*(20.1/36.4) + mISOSFWeightUp_GH*(16.3/36.4)
                            mIsoSFWeightDown[0] = mISOSFWeightDown_BCDEF*(20.1/36.4) + mISOSFWeightDown_GH*(16.3/36.4)
			    
			    mTrackerSFWeight[0]     = mTrk_BCDEF*(20.1/36.4) + mTrk_GH*(16.3/36.4)
			    mTrackerSFWeightUp[0]   = mTrk_BCDEF_up*(20.1/36.4) + mTrk_GH_up*(16.3/36.4)
			    mTrackerSFWeightDown[0] = mTrk_BCDEF_down*(20.1/36.4) + mTrk_GH_down*(16.3/36.4)
			    
			    EffData_BCDEFG = [1.0,0.]
			    EffMC_BCDEFG = [1.0,0.]
			    SF_BCDEFG = [1.0,0.,0.]
			    EffData_BCDEFG = computeEventSF_fromleg(effDataBCDEFG_leg8,effDataBCDEFG_leg17)
			    EffMC_BCDEFG = computeEventSF_fromleg(effMCBCDEFG_leg8,effMCBCDEFG_leg17)
			    SF_BCDEFG[0] =  (EffData_BCDEFG[0]/EffMC_BCDEFG[0])
			    SF_BCDEFG[1] = (1-math.sqrt(EffData_BCDEFG[1]**2+ EffMC_BCDEFG[1]**2))*SF_BCDEFG[0]
			    SF_BCDEFG[2] = (1+math.sqrt(EffData_BCDEFG[1]**2+ EffMC_BCDEFG[1]**2))*SF_BCDEFG[0]
                            #H no DZ
			    EffData_H = [1.0,0.]
			    EffMC_H = [1.0,0.]
			    SF_H = [1.0,0.,0.]
			    EffData_H = computeEventSF_fromleg(effDataH_leg8,effDataH_leg17)
			    EffMC_H = computeEventSF_fromleg(effMCH_leg8,effMCH_leg17)
			    SF_H[0] =  (EffData_H[0]/EffMC_H[0])
			    SF_H[1] = (1-math.sqrt(EffData_H[1]**2+ EffMC_H[1]**2))*SF_H[0]
			    SF_H[2] = (1+math.sqrt(EffData_H[1]**2+ EffMC_H[1]**2))*SF_H[0]
                            #H DZ SF
			    EffData_DZ = [1.0,0.]
			    EffMC_DZ = [1.0,0.]
			    SF_DZ = [1.0,0.,0.]
			    EffData_DZ = computeEvenSF_DZ(effDataH_DZ)
			    EffMC_DZ = computeEvenSF_DZ(effMCH_DZ)
			    SF_DZ[0] = (EffData_DZ[0]/EffMC_DZ[0])
			    SF_DZ[1] = (1-math.sqrt(EffData_DZ[1]**2+ EffMC_DZ[1]**2))*SF_DZ[0]
			    SF_DZ[2] = (1+math.sqrt(EffData_DZ[1]**2+ EffMC_DZ[1]**2))*SF_DZ[0]
			    
			    mTrigSFWeight_doubleMu80x[0]     = (27.221/35.827)*SF_BCDEFG[0] + (8.606/35.827)*SF_H[0]*SF_DZ[0]
			    mTrigSFWeight_doubleMu80xDown[0]   = (27.221/35.827)*SF_BCDEFG[1] + (8.606/35.827)*SF_H[1]*SF_DZ[1]
			    mTrigSFWeight_doubleMu80xUp[0] = (27.221/35.827)*SF_BCDEFG[2] + (8.606/35.827)*SF_H[2]*SF_DZ[2]

		    if tree.Vtype_new == 1:
			    
			    eTrigSFWeight_doubleEle80x[0]     = eff1*eff2
			    eTrigSFWeight_doubleEle80xUp[0]   = eff1Up*eff2Up 
			    eTrigSFWeight_doubleEle80xDown[0] = eff1Down*eff2Down

			    #print '\nEle Trigger SF Leg 1:', eff1
			    #print 'Ele Trigger SF Leg 2:', eff2
			    #print 'Final Ele SF:', eTrigSFWeight_doubleEle80x[0]
			    
			    


		    '''
		    # Now assign the lepton event weight based on vType
		    pTcut = 22;

                    DR = [999, 999]
                    debug = False
		    
                    # dR matching
                    for k in range(0,2):
                        for l in range(0,len(tree.trgObjects_hltIsoMu18_eta)):
                            dr_ = deltaR(tree.vLeptons_new_eta[k], tree.vLeptons_new_phi[k], tree.trgObjects_hltIsoMu18_eta[l], tree.trgObjects_hltIsoMu18_phi[l])
                            if dr_ < DR[k] and tree.vLeptons_new_pt[k] > 22:
                                DR[k] = dr_

                    Mu1pass = DR[0] < 0.5
                    Mu2pass = DR[1] < 0.5
		    
                    SF1 = tree.vLeptons_new_SF_HLT_RunD4p2[0]*0.1801911165 + tree.vLeptons_new_SF_HLT_RunD4p3[0]*0.8198088835
                    SF2 = tree.vLeptons_new_SF_HLT_RunD4p2[1]*0.1801911165 + tree.vLeptons_new_SF_HLT_RunD4p3[1]*0.8198088835
                    eff1 = tree.vLeptons_new_Eff_HLT_RunD4p2[0]*0.1801911165 + tree.vLeptons_new_Eff_HLT_RunD4p3[0]*0.8198088835
                    eff2 = tree.vLeptons_new_Eff_HLT_RunD4p2[1]*0.1801911165 + tree.vLeptons_new_Eff_HLT_RunD4p3[1]*0.8198088835

                    #print 'vLeptSFw is', vLeptons_new_SFweight_HLT[0]
                    #print 'Vtype_new is', tree.Vtype_new
		    
                    if tree.Vtype_new == 1:
			    vLeptons_new_SFweight_HLT[0] = eTrigSFWeight*eIDTightSFWeight
                    elif tree.Vtype_new == 0:
			vLeptons_new_SFweight_HLT[0] = 1    
                        if not Mu1pass and not Mu2pass:
                            vLeptons_new_SFweight_HLT[0] = 0
                        elif Mu1pass and not Mu2pass:
                            vLeptons_new_SFweight_HLT[0] = SF1
                        elif not Mu1pass and Mu2pass:
                            vLeptons_new_SFweight_HLT[0] = SF2
                        elif Mu1pass and Mu2pass:
                            effdata = 1 - (1-SF1*eff1)*(1-SF2*eff2);
                            effmc = 1 - (1-eff1)*(1-eff2);
                            vLeptons_new_SFweight_HLT[0] = effdata/effmc
		    '''	    
                		
	    # end if not Data
	    newtree.Fill()
	    # end event loop	



		

    print count	    
    print 'Exit loop'
    newtree.AutoSave()
    print 'Save'
    output.Close()
    input.Close()
    print 'Close'
    
    #t3 specific
    # targetStorage = pathOUT.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')+'/'+job.prefix+job.identifier+'.root'
    #command = 'lcg-del -b -D srmv2 -l %s' %(targetStorage)
    #print(command)
    #subprocess.call([command], shell=True)
    # command = 'lcg-cp -b -D srmv2 file:///%s %s' %(tmpDir+'/'+job.prefix+job.identifier+'.root',targetStorage)
    #print(command)
    #subprocess.call([command], shell=True)
