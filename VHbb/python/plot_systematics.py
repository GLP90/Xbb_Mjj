#!/usr/bin/env python
import ROOT 
ROOT.gROOT.SetBatch(True)
from ROOT import TFile
from optparse import OptionParser
import sys
from myutils import BetterConfigParser, TdrStyles, getRatio
import os


argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
config = BetterConfigParser()
config.read(opts.config)

print config


#---------- yes, this is not in the config yet---------
 
# mode = 'BDT'
# xMin=-0.8
# xMax=1
# masses = ['125']
# Abins = ['LowPt']#,'HighPt']
# channels = ['Zee']

# For Mjj
mode = 'Mjj'
xMin=60
xMax=180
masses = ['125']
Abins = ['HighPt']#,'HighPt']
channels = ['Zee']


#------------------------------------------------------

#---------- Control Regions ---------------------------------------
# mode = 'CR'
# xMin=-1
# xMax=1
# masses = ['125']
# Abins = ['Zlf']#, 'Zhf']
# channels= ['Zll']


#------------------------------------------------------

#path = config.get('Directories','limits')
#outpath = config.get('Directories','plotpath')

path = '~/public/shared/datacards/MjjZll_Datacards_Mjj_12bin60to180_8_1/'
#path = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/ZllHbb_Datacards_Minus08to1_JECfix_7_3'

outpath = '/afs/cern.ch/user/d/dcurry/www/v25_Systematics_Mjj_8_5_v1/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath

os.system(temp_string2)
os.system(temp_string3)

setup = eval(config.get('LimitGeneral','setup'))
Dict = eval(config.get('LimitGeneral','Dict'))
MCs = [Dict[s] for s in setup]

sys_BDT= eval(config.get('LimitGeneral','sys_BDT'))
systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming'))

#for syst in ["JES", "LF", "HF", "LFStats1", "LFStats2", "HFStats1", "HFStats2", "cErr1", "cErr2"]:
#    for ipt in range(0,5):
#        for ieta in range(1,4):
#            sys_BDT.append("btagWeightCSV_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta))
#            systematicsnaming["btagWeightCSV_"+syst+"_pt"+str(ipt)+"_eta"+str(ieta)] = 'CMS_vhbb_btagWeight'+syst+'_pt'+str(ipt)+'_eta'+str(ieta)

print '\nSystematics:', sys_BDT
print '\nSystematicsnaming:', systematicsnaming

systs=[systematicsnaming[s] for s in sys_BDT]


def myText(txt="CMS Preliminary",ndcX=0,ndcY=0,size=0.8):
    ROOT.gPad.Update()
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextColor(ROOT.kBlack)
    text.SetTextSize(text.GetTextSize()*size)
    text.DrawLatex(ndcX,ndcY,txt)
    return text


print '\n\n\t\tMaking Plots for Systematics: ', systs

print '\n\t ---> Output: ', outpath

#for mass in ['110','115','120','125','130','135']:
for mass in masses:
    for Abin in Abins:
        for channel in channels:

            if mode == 'BDT':
                input = TFile.Open(path+'/vhbb_TH_BDT_'+channel+'_'+Abin+'.root','read')

            if mode == 'CR':
                input = TFile.Open(path+'/vhbb_TH_'+Abin+'.root','read')
                
            if mode == 'Mjj':
                input = TFile.Open(path+'/vhbb_TH_Mjj_'+channel+'_'+Abin+'.root','read')


            print '\n-----> Input: ', input     

            for MC in MCs:

                print 'MC sample: ',MC

                if MC == 's_Top': continue

                for syst in systs:
                    print '\n\t Plotting Systematic: ', syst
                #['CMS_res_j','CMS_scale_j','CMS_eff_b','CMS_fake_b_8TeV','UEPS']:
                #for syst in ['CMS_vhbb_stats_']:

                    if '_eff_' in syst:
                        if 'Zuu' in channels and '_e_' in syst: continue
                        if 'Zee' in channels and '_m_' in syst:continue

                    TdrStyles.tdrStyle()

                    c = ROOT.TCanvas('','', 600, 600)
                    c.SetFillStyle(4000)
                    c.SetFrameFillStyle(1000)
                    c.SetFrameFillColor(0)
                    oben = ROOT.TPad('oben','oben',0,0.3 ,1.0,1.0)
                    oben.SetBottomMargin(0)
                    oben.SetFillStyle(4000)
                    oben.SetFrameFillStyle(1000)
                    oben.SetFrameFillColor(0)
                    unten = ROOT.TPad('unten','unten',0,0.0,1.0,0.3)
                    unten.SetTopMargin(0.)
                    unten.SetBottomMargin(0.35)
                    unten.SetFillStyle(4000)
                    unten.SetFrameFillStyle(1000)
                    unten.SetFrameFillColor(0)
                    oben.Draw()
                    unten.Draw()
                    oben.cd()

                    ROOT.gPad.SetTicks(1,1)
                    
                    if mode == 'BDT':
                        input.cd(channel+Abin+'_13TeV')
                    if mode == 'CR':
                        input.cd(Abin)
                    if mode == 'Mjj':
                        input.cd(channel+Abin+'_13TeV')
                

                    Ntotal=ROOT.gDirectory.Get(MC)

                    #if 'pu' not in syst and '_eff_' not in syst:
                    #if '_j_' in syst:
                    #    if 'High' in Abin:
                    #        Utotal=ROOT.gDirectory.Get(MC+syst+'_highVptUp')
                    #        Dtotal=ROOT.gDirectory.Get(MC+syst+'_highVptDown')
                    #    if 'Low' in Abin:
                    #        Utotal=ROOT.gDirectory.Get(MC+syst+'_lowVptUp')
                    #        Dtotal=ROOT.gDirectory.Get(MC+syst+'_lowVptDown')

                    #else:
                    Utotal=ROOT.gDirectory.Get(MC+syst+'Up')
                    Dtotal=ROOT.gDirectory.Get(MC+syst+'Down')

                    print '\n\t Input: ', channel+Abin+'_13TeV'
                    print input
                    print '\n\t NOM : ', MC
                    print Ntotal
                    print '\n\t UP  : ', MC+syst+'Up'
                    print Utotal
                    print '\n\t DOWN: ', MC+syst+'Down'
                    print Dtotal


                    l = ROOT.TLegend(0.17, 0.8, 0.37, 0.65)
                    
                    l.SetLineWidth(2)
                    l.SetBorderSize(0)
                    l.SetFillColor(0)
                    l.SetFillStyle(4000)
                    l.SetTextFont(62)
                    l.SetTextSize(0.035)
                    
                    l.AddEntry(Ntotal,'nominal(%s)'%round(Ntotal.Integral(),3),'PL')
                    l.AddEntry(Utotal,'up(%s)'%round(Utotal.Integral(),3),'PL')
                    l.AddEntry(Dtotal,'down(%s)'%round(Dtotal.Integral(),3),'PL')
                    Ntotal.GetYaxis().SetRangeUser(0,1.5*Ntotal.GetBinContent(Ntotal.GetMaximumBin()))
                    Ntotal.SetMarkerStyle(8)
                    Ntotal.SetLineColor(1)
                    Ntotal.SetStats(0)
                    Ntotal.SetTitle(MC +' '+syst)
                    Ntotal.Draw("P0")
                    Ntotal.Draw("same")
                    Utotal.SetLineColor(4)    
                    Utotal.SetLineStyle(4)
                    Utotal.SetLineWidth(2)        
                    Utotal.Draw("same hist")
                    Dtotal.SetLineColor(2)
                    Dtotal.SetLineStyle(3)
                    Dtotal.SetLineWidth(2)  
                    Dtotal.Draw("same hist")
                    l.SetFillColor(0)
                    l.SetBorderSize(0)
                    l.Draw()
                    
                    if 'High' in Abin:
                        title=myText('%s in %s'%(syst,MC+'_'+channel+'_highZpt'),0.17,0.85)
                    if 'Low' in Abin:
                        title=myText('%s in %s'%(syst,MC+'_'+channel+'_lowZpt'),0.17,0.85)
                        

                    print 'Shape Systematic %s in %s'%(syst,MC)
                    print 'Up:     \t%s'%Utotal.Integral()
                    print 'Nominal:\t%s'%Ntotal.Integral()
                    print 'Down:   \t%s'%Dtotal.Integral()
                    
                    unten.cd()
                    ROOT.gPad.SetTicks(1,1)

                    ratioU, errorU  = getRatio(Utotal,Ntotal,xMin,xMax)
                    ratioD, errorD  = getRatio(Dtotal,Ntotal,xMin,xMax)

                    ksScoreU = Ntotal.KolmogorovTest( Utotal )
                    chiScoreU = Ntotal.Chi2Test( Utotal , "WWCHI2/NDF")
                    ksScoreD = Ntotal.KolmogorovTest( Dtotal )
                    chiScoreD = Ntotal.Chi2Test( Dtotal , "WWCHI2/NDF")

                    yUp   = 1.1
                    yDown = 0.9


                    ratioU.SetStats(0)
                    ratioU.GetYaxis().SetRangeUser(yDown, yUp)
                    ratioU.GetYaxis().SetNdivisions(502,0)
                    ratioD.SetStats(0)
                    ratioD.GetYaxis().SetRangeUser(yDown, yUp)
                    ratioD.GetYaxis().SetNdivisions(502,0)
                    ratioD.GetYaxis().SetLabelSize(0.05)
                    ratioD.SetLineColor(2)
                    ratioD.SetLineStyle(3)
                    ratioD.SetLineWidth(2)  
                    ratioU.SetLineColor(4)    
                    ratioU.SetLineStyle(4)
                    ratioU.SetLineWidth(2)

                    fitRatioU = ratioU.Fit("pol2","S")
                    ratioU.GetFunction("pol2").SetLineColor(4)
                    fitRatioD = ratioD.Fit("pol2","S")
                    ratioU.Draw("APSAME")
                    ratioD.GetXaxis().SetTitle('BDT Output')
                    ratioD.GetYaxis().SetTitle('Ratio')
                    ratioD.GetYaxis().SetTitleSize(0.1)
                    ratioD.GetYaxis().SetTitleOffset(0.2)
                    fitRatioU.Draw("SAME")
                    fitRatioD.Draw("SAME")
                    
                    ratioD.Draw("SAME")

                    #ratioU.GetYaxis().SetTitleSize(0.2)
                    #ratioU.GetYaxis().SetTitleOffset(0.2)
                    #ratioU.GetXaxis().SetLabelColor(10)
                    
                    #fitRatioU = ratioU.Fit("pol2","S")
                    #fitRatioU.Draw("SAME")

                    #ratioD.GetYaxis().SetTitleSize(0.2)
                    #ratioD.GetYaxis().SetTitleOffset(0.2)
                    #ratioD.GetXaxis().SetLabelColor(10)
                    
                    #fitRatioD = ratioD.Fit("pol2","S")
                    #fitRatioD.Draw("SAME")

                    m_one_line = ROOT.TLine(xMin,1,xMax,1)
                    m_one_line.SetLineStyle(7)
                    m_one_line.SetLineColor(1)
                    m_one_line.Draw("Same")


                    #name = outpath+Abin+'_M'+mass+'_'+channel+'_'+MC+syst+'.png'
                    #c.Print(name)

                    if mode == 'CR':
                        name = outpath+'systPlot_'+Abin+'_'+channel+'_'+MC+'_'+syst+'.pdf'
                        c.Print(name)
                        name2 = outpath+'systPlot_'+Abin+'_'+channel+'_'+MC+'_'+syst+'.png'
                        c.Print(name2)
                        
                    else:
                        name = outpath+'systPlot_'+Abin+'_M'+mass+'_'+channel+'_'+MC+syst+'.pdf'
                        c.Print(name)
                        name2 = outpath+'systPlot_'+Abin+'_M'+mass+'_'+channel+'_'+MC+syst+'.png'
                        c.Print(name2)


            input.Close()
