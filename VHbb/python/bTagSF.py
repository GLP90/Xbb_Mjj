import ROOT
import os
import sys
import multiprocessing
import numpy as np
from myutils.printcolor import printc
#ROOT.gROOT.SetBatch(True)

debug_btagSF = False

print '\nLoading Calibration...\n'

# load the BTagCalibrationStandalone.cc macro from https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration
#csvpath = os.environ['CMSSW_BASE']+"/src/VHbbAnalysis/Heppy/data/csv/"
ROOT.gSystem.Load("./BTagCalibrationStandalone.so")
#ROOT.gROOT.ProcessLine('.L ../interface/BTagCalibrationStandalone.cpp+')

# from within CMSSW:
#ROOT.gSystem.Load('libCondFormatsBTauObjects') 

print '\nCompilation done...\n'

# CSVv2
#calib_csv = ROOT.BTagCalibration("csvv2", "./ttH_BTV_CSVv2_13TeV_2016All_36p5_2017_1_10.csv")
calib_csv = ROOT.BTagCalibration("csvv2", "./CSVv2_Moriond17_B_H.csv")

# cMVAv2
#calib_cmva = ROOT.BTagCalibration("cmvav2", "./ttH_BTV_cMVAv2_13TeV_2016All_36p5_2017_1_26.csv")
calib_cmva = ROOT.BTagCalibration("cmvav2", "cMVAv2_Moriond17_B_H.csv")

print "\nCalibration Init...\n"

# map between algo/flavour and measurement type
sf_type_map = {
    "CSV" : {
        "file" : calib_csv,
        "bc" : "comb",
        "l" : "incl",
        },
    "CMVAV2" : {
        "file" : calib_cmva,
        "bc" : "ttbar",
        "l" : "incl",
        }
    }

# map of calibrators. E.g. btag_calibrators["CSVM_nominal_bc"], btag_calibrators["CSVM_up_l"], ...
btag_calibrators = {}
#for algo in ["CSV", "CMVAV2"]:
#    for wp in [ [0, "L"],[1, "M"], [2,"T"] ]:
#        for syst in ["central", "up", "down"]:
#            for fl in ["bc", "l"]:
#                print "[btagSF]: Loading calibrator for algo:", algo, ", WP:", wp[1], ", systematic:", syst, ", flavour:", fl
#                btag_calibrators[algo+wp[1]+"_"+syst+"_"+fl] = ROOT.BTagCalibrationReader(sf_type_map[algo]["file"], wp[0], sf_type_map[algo][fl], syst)

for algo in ["CSV", "CMVAV2"]:
    for syst in ["central", "up_jes", "down_jes", "up_lf", "down_lf", "up_hf", "down_hf", "up_hfstats1", "down_hfstats1", "up_hfstats2", "down_hfstats2", "up_lfstats1", "down_lfstats1", "up_lfstats2", "down_lfstats2", "up_cferr1", "down_cferr1", "up_cferr2", "down_cferr2"]:
        print "[btagSF]: Loading calibrator for algo:", algo, "systematic:", syst
        btag_calibrators[algo+"_iterative_"+syst] = ROOT.BTagCalibrationReader(sf_type_map[algo]["file"], 3 , "iterativefit", syst)


print "\nCalibration Done...\n"


# depending on flavour, only a sample of systematics matter
def applies( flavour, syst ):
    if flavour==5 and syst not in ["central", "up_jes", "down_jes",  "up_lf", "down_lf",  "up_hfstats1", "down_hfstats1", "up_hfstats2", "down_hfstats2"]:
        return False
    elif flavour==4 and syst not in ["central", "up_cferr1", "down_cferr1", "up_cferr2", "down_cferr2" ]:
        return False
    elif flavour==0 and syst not in ["central", "up_jes", "down_jes", "up_hf", "down_hf",  "up_lfstats1", "down_lfstats1", "up_lfstats2", "down_lfstats2" ]:
        return False

    return True


# function that reads the SF
def get_SF(pt=30., eta=0.0, fl=5, val=0.0, syst="central", algo="CSV", wp="M", shape_corr=False, btag_calibrators=btag_calibrators):

    # no SF for pT<20 GeV or pt>1000 or abs(eta)>2.4
    if abs(eta)>2.4 or pt>1000. or pt<20.:
        return 1.0

    # the .csv files use the convention: b=0, c=1, l=2. Convert into hadronFlavour convention: b=5, c=4, f=0
    fl_index = min(-fl+5,2)
    # no fl=1 in .csv for CMVAv2 (a bug???)
    #if not shape_corr and "CMVAV2" in algo and fl==4:
    #    fl_index = 0

    if shape_corr:
        if applies(fl,syst):
            sf = btag_calibrators[algo+"_iterative_"+syst].eval(fl_index ,eta, pt, val)
            #print 'shape_corr SF:', sf
            return sf
        else:
            sf = btag_calibrators[algo+"_iterative_central"].eval(fl_index ,eta, pt, val)
            #print 'shape_corr for central SF:', sf
            return sf 
        

    # pt ranges for bc SF: needed to avoid out_of_range exceptions
    pt_range_high_bc = 670.-1e-02 if "CSV" in algo else 320.-1e-02
    pt_range_low_bc = 30.+1e-02

    # b or c jets
    if fl>=4:
        # use end_of_range values for pt in [20,30] or pt in [670,1000], with double error
        out_of_range = False
        if pt>pt_range_high_bc or pt<pt_range_low_bc:
            out_of_range = True        
        pt = min(pt, pt_range_high_bc)
        pt = max(pt, pt_range_low_bc)
        sf = btag_calibrators[algo+wp+"_"+syst+"_bc"].eval(fl_index ,eta, pt)
        # double the error for pt out-of-range
        if out_of_range and syst in ["up","down"]:
            sf = max(2*sf - btag_calibrators[algo+wp+"_central_bc"].eval(fl_index ,eta, pt), 0.)
        #print sf
        return sf
    # light jets
    else:
        sf = btag_calibrators[algo+wp+"_"+syst+"_l"].eval( fl_index ,eta, pt)
        #print sf
        return  sf

def get_event_SF(ptmin, ptmax, etamin, etamax, jets=[], syst="central", algo="CSV", btag_calibrators=btag_calibrators):
    weight = 1.0

    for jet in jets:
        if (jet.pt > ptmin and jet.pt < ptmax and abs(jet.eta) > etamin and abs(jet.eta) < etamax):
            weight *= get_SF(pt=jet.pt, eta=jet.eta, fl=jet.hadronFlavour, val=jet.csv, syst=syst, algo=algo, wp="", shape_corr=True, btag_calibrators=btag_calibrators)
        else:
            weight *= get_SF(pt=jet.pt, eta=jet.eta, fl=jet.hadronFlavour, val=jet.csv, syst="central", algo=algo, wp="", shape_corr=True, btag_calibrators=btag_calibrators)
    return weight                             

##########

if debug_btagSF:
    print "POG WP:"
    for algo in ["CMVAV2"]:
        for wp in [ "L", "M", "T" ]:
            print algo+wp+":"
            for syst in ["central", "up", "down"]:
                print "\t"+syst+":"
                for pt in [19.,25.,31.,330., 680.]:
                    print ("\t\tB(pt=%.0f, eta=0.0): %.3f" % (pt, get_SF(pt=pt, eta=0.0, fl=5, val=0.0, syst=syst, algo=algo, wp=wp, shape_corr=False)))
                    print ("\t\tC(pt=%.0f, eta=0.0): %.3f" % (pt, get_SF(pt=pt, eta=0.0, fl=4, val=0.0, syst=syst, algo=algo, wp=wp, shape_corr=False)))
                    print ("\t\tL(pt=%.0f, eta=0.0): %.3f" % (pt, get_SF(pt=pt, eta=0.0, fl=0, val=0.0, syst=syst, algo=algo, wp=wp, shape_corr=False)))

    print "Iterative:"
    for algo in ["CMVAV2"]:
        print algo+":"
        for syst in ["central", "up_jes", "down_jes", "up_lf", "down_lf", "up_hf", "down_hf", "up_hfstats1", "down_hfstats1", "up_hfstats2", "down_hfstats2", "up_lfstats1", "down_lfstats1", "up_lfstats2", "down_lfstats2", "up_cferr1", "down_cferr1", "up_cferr2", "down_cferr2"]:
            print "\t"+syst+":"
            for pt in [50.]:
                print ("\t\tB(pt=%.0f, eta=0.0): %.3f" % (pt, get_SF(pt=pt, eta=0.0, fl=5, val=0.89, syst=syst, algo=algo, wp="", shape_corr=True)))
                print ("\t\tC(pt=%.0f, eta=0.0): %.3f" % (pt, get_SF(pt=pt, eta=0.0, fl=4, val=0.89, syst=syst, algo=algo, wp="", shape_corr=True)))
                print ("\t\tL(pt=%.0f, eta=0.0): %.3f" % (pt, get_SF(pt=pt, eta=0.0, fl=0, val=0.89, syst=syst, algo=algo, wp="", shape_corr=True)))

################################################################
# A dummy class of a jet object

class Jet :
    def __init__(self, pt, eta, fl, csv) :
        self.pt = pt
        self.eta = eta
        self.hadronFlavour = fl
        self.csv = csv

    #def hadronFlavour(self):
    #    return self.mcFlavour
    #def btag(self, name):
    #    return self.btagCSV
    #def pt(self):
    #    return self.pt
    #def eta(self):
    #    return self.eta


################################################################

# sample prefix
prefix = 'v25_'
#prefix = ''

#inpath = '/exports/uftrig01a/dcurry/heppy/files/jec_out/'
#outpath = '/exports/uftrig01a/dcurry/heppy/files/btag_out/'

inpath = '/exports/uftrig01a/dcurry/heppy/files/MVA_out_VV/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out_VV/'

# List of files to add btag weights to
bkg_list = ['ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

DY_list = ['DY_600to800_ext1', 'DY_600to800_ext2','DY_600to800_ext3','DY_600to800_ext4','DY_600to800_ext5', 'DY_600to800_ext6']


ST_list = ['ST_s', 'ST_tW_top', 'ST_tW_antitop', 'ST_t_antitop']


temp_list = ['WZ']

#file_list = bkg_list + signal_list + ST_list + DY_list
file_list = temp_list


file_list1 = ST_list + ['WZ','DY_Bjets','DY_inclusive', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'DY_1200to2500', 'DY_2500toInf',
                        'DY_100to200', 'DY_200to400', 'DY_400to600']

file_list2 = signal_list + ['ttbar', 'DY_Bjets_Vpt100to200', 'DY_Bjets_Vpt200toInf']

file_list3 = DY_list

file_list4 = ['DY_800to1200_ext1','DY_800to1200_ext2','DY_Bjets_Vpt100to200_ext2', 'DY_Bjets_Vpt200toInf_ext2']


#for file in file_list:
def osSystem(file):
    
    # map from the systematic names we prefer to keep the same as before
    # to the new names
    sysRefMap = {}

    def MakeSysRefMap():
        sysRefMap["JESUp"] = tree.btagWeightCSV_up_jes
        sysRefMap["JESDown"] = tree.btagWeightCSV_down_jes
        sysRefMap["LFUp"] = tree.btagWeightCSV_up_lf
        sysRefMap["LFDown"] = tree.btagWeightCSV_down_lf
        sysRefMap["HFUp"] = tree.btagWeightCSV_up_hf
        sysRefMap["HFDown"] = tree.btagWeightCSV_down_hf
        sysRefMap["HFStats1Up"] = tree.btagWeightCSV_up_hfstats1
        sysRefMap["HFStats1Down"] = tree.btagWeightCSV_down_hfstats1
        sysRefMap["HFStats2Up"] = tree.btagWeightCSV_up_hfstats2
        sysRefMap["HFStats2Down"] = tree.btagWeightCSV_down_hfstats2
        sysRefMap["LFStats1Up"] = tree.btagWeightCSV_up_lfstats1
        sysRefMap["LFStats1Down"] = tree.btagWeightCSV_down_lfstats1
        sysRefMap["LFStats2Up"] = tree.btagWeightCSV_up_lfstats2
        sysRefMap["LFStats2Down"] = tree.btagWeightCSV_down_lfstats2
        sysRefMap["cErr1Up"] = tree.btagWeightCSV_up_cferr1
        sysRefMap["cErr1Down"] = tree.btagWeightCSV_down_cferr1
        sysRefMap["cErr2Up"] = tree.btagWeightCSV_up_cferr2
        sysRefMap["cErr2Down"] = tree.btagWeightCSV_down_cferr2
        
    sysMap = {}
    sysMap["JESUp"] = "up_jes"
    sysMap["JESDown"] = "down_jes"
    sysMap["LFUp"] = "up_lf"
    sysMap["LFDown"] = "down_lf"
    sysMap["HFUp"] = "up_hf"
    sysMap["HFDown"] = "down_hf"
    sysMap["HFStats1Up"] = "up_hfstats1"
    sysMap["HFStats1Down"] = "down_hfstats1"
    sysMap["HFStats2Up"] = "up_hfstats2"
    sysMap["HFStats2Down"] = "down_hfstats2"
    sysMap["LFStats1Up"] = "up_lfstats1"
    sysMap["LFStats1Down"] = "down_lfstats1"
    sysMap["LFStats2Up"] = "up_lfstats2"
    sysMap["LFStats2Down"] = "down_lfstats2"
    sysMap["cErr1Up"] = "up_cferr1"
    sysMap["cErr1Down"] = "down_cferr1"
    sysMap["cErr2Up"] = "up_cferr2"
    sysMap["cErr2Down"] = "down_cferr2"
        

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

    # # Zero out any old batg branches
    # tree.SetBranchStatus('bTagWeightCSV_Moriond',0)
    # tree.SetBranchStatus('bTagWeightCMVAv2_Moriond',0)
    # for syst in ["JES", "LF", "HF", "LFStats1", "LFStats2", "HFStats1", "HFStats2", "cErr1", "cErr2"]:
    #     for sdir in ["Up", "Down"]:
    #         tree.SetBranchStatus("bTagWeightCMVAV2_Moriond_"+syst+sdir,0)
    #         tree.SetBranchStatus("bTagWeightCSV_Moriond_"+syst+sdir,0)
    #         for systcat in ["HighCentral","LowCentral","HighForward","LowForward"]:
    #             tree.SetBranchStatus("bTagWeightCMVAV2_Moriond_"+syst+systcat+sdir,0)
    #             tree.SetBranchStatus("bTagWeightCSV_Moriond_"+syst+systcat+sdir,0)

    otree = tree.CloneTree(0)

    bTagWeights = {}
    bTagWeights["bTagWeightCMVAV2_Moriond"] = np.zeros(1, dtype=float)
    otree.Branch("bTagWeightCMVAv2_Moriond", bTagWeights["bTagWeightCMVAV2_Moriond"], "bTagWeightCMVAV2_Moriond/D")
    
    #bTagWeights["bTagWeightCSV_Moriond"] = np.zeros(1, dtype=float)
    #otree.Branch("bTagWeightCSV_Moriond", bTagWeights["bTagWeightCSV_Moriond"], "bTagWeightCSV_Moriond/D")
    

    for syst in ["JES", "LF", "HF", "LFStats1", "LFStats2", "HFStats1", "HFStats2", "cErr1", "cErr2"]:
        for sdir in ["Up", "Down"]:

            bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+sdir] = np.zeros(1, dtype=float)
            otree.Branch("bTagWeightCMVAV2_Moriond_"+syst+sdir, bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+sdir], "bTagWeightCMVAV2_Moriond_"+syst+sdir+"/D")

            #bTagWeights["bTagWeightCSV_Moriond_"+syst+sdir] = np.zeros(1, dtype=float)
            #otree.Branch("bTagWeightCSV_Moriond_"+syst+sdir, bTagWeights["bTagWeightCSV_Moriond_"+syst+sdir], "bTagWeightCSV_Moriond_"+syst+sdir+"/D")

            #for systcat in ["HighCentral","LowCentral","HighForward","LowForward"]:
            for ipt in range(0,5):
                for ieta in range(1,4):
                    bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir] = np.zeros(1, dtype=float)
                    otree.Branch("bTagWeightCMVAV2_Moriond_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir, bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir], "bTagWeightCMVAV2_Moriond_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir+"/D")


    nentries = tree.GetEntries()
    print file," has nentries = ",nentries
    for entry in range(nentries):

        if (entry%10000 == 0): printc('green', '', "\t processing entry: %i" % entry)
        
        #if entry > 1000: continue

        tree.GetEntry(entry)

        MakeSysRefMap()

        if 'Zee' in file or 'Zuu' in file:
            bTagWeights["bTagWeightCMVAv2_Moriond"][0] = 1.0
            #bTagWeights["bTagWeightCSV_Moriond"][0] = 1.0
            otree.Fill()
            continue

        jets_csv = []
        jets_cmva = []
        
        for i in range(tree.nJet):
            if (tree.Jet_pt_reg[i] > 20 and abs(tree.Jet_eta[i]) < 2.4): 
                #jet_csv = Jet(tree.Jet_pt_reg[i], tree.Jet_eta[i], tree.Jet_hadronFlavour[i], tree.Jet_btagCSV[i])
                #jets_csv.append(jet_csv)
                jet_cmva = Jet(tree.Jet_pt_reg[i], tree.Jet_eta[i], tree.Jet_hadronFlavour[i], tree.Jet_btagCMVAV2[i])
                jets_cmva.append(jet_cmva)

        ptmin = 20.
        ptmax = 1000.
        etamin = 0.
        etamax = 2.4
                        
        bTagWeights["bTagWeightCMVAV2_Moriond"][0] = get_event_SF(ptmin, ptmax, etamin, etamax, jets_cmva, "central", "CMVAV2", btag_calibrators)
        #bTagWeights["bTagWeightCSV_Moriond"][0] = get_event_SF(ptmin, ptmax, etamin, etamax, jets_csv, "central", "CSV", btag_calibrators)
        
        #print 'btag CMVAV2 Event Weight:', bTagWeights["bTagWeightCMVAV2_Moriond"][0]
        #print 'btag CSV Event Weight   :', bTagWeights["bTagWeightCSV_Moriond"][0]
        
        for syst in ["JES", "LF", "HF", "LFStats1", "LFStats2", "HFStats1", "HFStats2", "cErr1", "cErr2"]:
            for sdir in ["Up", "Down"]:
                
                bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+sdir][0] = get_event_SF( ptmin, ptmax, etamin, etamax, jets_cmva, sysMap[syst+sdir], "CMVAV2", btag_calibrators)
                #bTagWeights["bTagWeightCSV_Moriond_"+syst+sdir][0] = get_event_SF( ptmin, ptmax, etamin, etamax, jets_csv, sysMap[syst+sdir], "CSV", btag_calibrators)
                                
                #for systcat in ["HighCentral","LowCentral","HighForward","LowForward"]:
                for ipt in range(0,5):

                    ptmin = 20.
                    ptmax = 1000.
                    etamin = 0.
                    etamax = 2.4
                    
                    if ipt == 0:
                        ptmin = 20.
                        ptmax = 30.
                    elif ipt == 1:
                        ptmin = 30.
                        ptmax = 40.
                    elif ipt ==2:
                        ptmin = 40.
                        ptmax = 60.
                    elif ipt ==3:
                        ptmin = 60.
                        ptmax = 100.
                    elif ipt ==4:
                        ptmin = 100.
                        ptmax = 1000.

                    for ieta in range(1,4):

                        #print '\n Btag for SYS:', syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir
                        if ieta ==1:
                            etamin = 0.
                            etamax = 0.8
                        elif ieta ==2:
                            etamin = 0.8
                            etamax = 1.6
                        elif ieta ==3:
                            etamin = 1.6
                            etamax = 2.4
                            
                            #bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+systcat+sdir][0] = get_event_SF(ptmin, ptmax, etamin, etamax, jets_cmva, sysMap[syst+sdir], "CMVAV2", btag_calibrators)
                        bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir][0] = get_event_SF(ptmin, ptmax, etamin, etamax, jets_cmva, sysMap[syst+sdir], "CMVAV2", btag_calibrators)

                        #print 'bTagWeights[bTagWeightCMVAV2_Moriond_'+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir, bTagWeights["bTagWeightCMVAV2_Moriond_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)+sdir][0]
                            

        otree.Fill()

    
    #ofile.cd()
    #otree.Write()
    otree.AutoSave()
    ofile.Close()
    ifile.Close()
    print 'Finished...'


# Done
# p = multiprocessing.Pool()
# results = p.imap(osSystem, file_list)
# p.close()
# p.join()


p = multiprocessing.Pool()
results = p.imap(osSystem, file_list2)
p.close()
p.join()

p = multiprocessing.Pool()
results = p.imap(osSystem, file_list3)
p.close()
p.join()

p = multiprocessing.Pool()
results = p.imap(osSystem, file_list1)
p.close()
p.join()

p = multiprocessing.Pool()
results = p.imap(osSystem, file_list4)
p.close()
p.join()
