#!/usr/bin/env python
import pickle
import sys, os
from optparse import OptionParser
from copy import copy,deepcopy
from math import sqrt
import math
from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.CombinedLimit.ShapeTools     import *
#from ROOT import *
from collections import Counter
import array as ar

isVV = False
#isVV = True

# import ROOT with a fix to get batch mode (http://root.cern.ch/phpBB3/viewtopic.php?t=3198)
hasHelp = False
argv = sys.argv
for X in ("-h", "-?", "--help"):
    if X in argv:
        hasHelp = True
        argv.remove(X)
argv.append( '-b-' )
import ROOT
from myutils import StackMaker, BetterConfigParser

ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
argv.remove( '-b-' )
if hasHelp: argv.append("-h")

#CONFIGURE
parser = OptionParser()
parser.add_option("-D", "--datacard", dest="dc", default="",
                      help="Datacard to be plotted")
parser.add_option("-B", "--bin", dest="bin", default="",
                      help="DC bin to plot")
parser.add_option("-M", "--mlfit", dest="mlfit", default="",
                      help="mlfit file for nuisances")
parser.add_option("-F", "--fitresult", dest="fit", default="s",
                      help="Fit result to be used, 's' (signal+background)  or 'b' (background only), default is 's'")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
parser.add_option("-V", "--variable", dest="var", default="",
                      help="variable to be fitted")
parser.add_option("-R", "--region", dest="region", default="",
                  help="region to be plotted")

(opts, args) = parser.parse_args(argv)

print opts


def rebinHist(hist, nbin, xmin, xmax, dirname, subdir, prefit_error_histos, postfit_error_histos, stat_hists, bin):

    '''The postfit plots stored in the mlfit.root don't have the proper bin size. A rebinning is therefor necessary.
       PostFit Shapes will be given preFit errors in order to seperate out MC and SYS errors.
    '''

    h_new = ROOT.TH1F(hist.GetName(), hist.GetName(), nbin, xmin, xmax)
    h_new_postfit = ROOT.TH1F(subdir.GetName()+'_postfit', subdir.GetName()+'_postfit', nbin, xmin, xmax)
    h_new_prefit = ROOT.TH1F(subdir.GetName()+'_prefit', subdir.GetName()+'_prefit', nbin, xmin, xmax)

    # if Wlv make variable histogram
    # if 'WmnHighPt' in bin or 'WenHighPt' in bin:
        
    #     bin_array = ar.array('d',[0.3, 0.4, 0.5, 0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.0])

    #     h_new = ROOT.TH1F(hist.GetName(), hist.GetName(), len(bin_array)-1, bin_array)
    #     h_new_postfit = ROOT.TH1F(subdir.GetName()+'_postfit', subdir.GetName()+'_postfit', len(bin_array)-1, bin_array)
    #     h_new_prefit = ROOT.TH1F(subdir.GetName()+'_prefit', subdir.GetName()+'_prefit', len(bin_array)-1, bin_array)

        
    print '\n Making PostFit Rebinned Hist for ', hist.GetName(), h_new
    

    for b in range(1,nbin+1):
        
        # if 'ZH' not in hist.GetName() or 'WH' not in hist.GetName():
        #   h_new.SetBinContent(b, hist.GetBinContent(b))
        # else:
        #    print '\nSetting Signal PreFit Error(dirname,subdir)', dirname, subdir
        #    ROOT.gDirectory.cd('/shapes_prefit/'+dirname)
        #    pre_hist = ROOT.gDirectory.Get(subdir.GetName()).Clone()
        #    h_new.SetBinContent(b, pre_hist.GetBinContent(b))
        #     # change back
        #    ROOT.gDirectory.cd('/shapes_fit_s/'+dirname)
        
        h_new.SetBinContent(b, hist.GetBinContent(b))
        h_new.SetBinError(b, hist.GetBinError(b))
        h_new.SetBinError(b, stat_hists[hist.GetName()].GetBinError(b))
        h_new_postfit.SetBinContent(b, hist.GetBinContent(b))
        h_new_postfit.SetBinError(b, sqrt(hist.GetBinError(b)*hist.GetBinError(b)+stat_hists[hist.GetName()].GetBinError(b)*stat_hists[hist.GetName()].GetBinError(b)))
        print '\nBin content:', hist.GetBinContent(b)
        print 'Stat Bin ',b, 'error:', stat_hists[hist.GetName()].GetBinError(b)
        print 'Post Fit Bin ',b, 'error:', hist.GetBinError(b)


    postfit_error_histos.append(h_new_postfit)
        
    # Set bin error to preFit
    print '\nSetting preFit Error(dirname,subdir)', dirname, subdir    
    ROOT.gDirectory.cd('/shapes_prefit/'+dirname)
    #ROOT.gDirectory.cd('/tree_prefit/'+dirname)

    pre_hist = ROOT.gDirectory.Get(subdir.GetName()).Clone()
    #h_new_prefit = ROOT.TH1F(subdir.GetName()+'_prefit', subdir.GetName()+'_prefit', nbin, xmin, xmax)
    for b in range(1,nbin+1):
        h_new_prefit.SetBinContent(b, pre_hist.GetBinContent(b))
        h_new_prefit.SetBinError(b, pre_hist.GetBinError(b)+stat_hists[hist.GetName()].GetBinError(b))
        print 'Bin ',b, 'error:', h_new_prefit.GetBinError(b)
    prefit_error_histos.append(h_new_prefit)
    #print 'PreFit Error Hist:', prefit_error_histos
    
    
    ROOT.gDirectory.cd('/shapes_fit_s/'+dirname)
    #ROOT.gDirectory.cd('/tree_fit_sb/'+dirname)

    return h_new

def drawFromDC():

    config = BetterConfigParser()
    config.read(opts.config)

    region = opts.region

    print "\nopts.config:",opts.config
    print "opts:", opts
    print "var:", opts.var
    print "bin:", opts.bin
    
    dataname = 'Zll'
    
    if 'Zuu' in opts.bin: dataname = 'Zuu'
    elif 'Zee' in opts.bin: dataname = 'Zee'
    elif 'Wmn' in opts.bin: dataname = 'Wmn'
    elif 'Wen' in opts.bin: dataname = 'Wen'
    elif 'Znn' in opts.bin: dataname = 'Znn'
    elif 'Wtn' in opts.bin: dataname = 'Wtn'
    
    
    if (opts.var == ''):
        var = 'BDT'
        if dataname == 'Zmm' or dataname == 'Zee': var = 'BDT_Zll' 
        elif dataname == 'Wmn' or dataname == 'Wen': var = 'BDT_Wln' 
        elif dataname == 'Znn': var = 'BDT_Znn' 
            #if 'HighPt' in opts.bin: var = 'BDT_ZnnHighPt' 
            #if 'LowPt' in opts.bin: var = 'BDT_ZnnLowPt' 
            #if 'LowCSV' in opts.bin: var = 'BDT_ZnnLowCSV' 
        if dataname == '' or var == 'BDT': raise RuntimeError, 'Did not recognise mode or var from '+opts.bin
    else:
        var = opts.var
    
    
    if opts.var == 'BDT':
        if 'LowPt' in opts.bin: var = 'gg_plus_ZH125_low_Zpt'
        elif 'MedPt' in opts.bin: var = 'gg_plus_ZH125_med_Zpt'
        elif 'HighPt' in opts.bin: var = 'gg_plus_ZH125_high_Zpt'
        elif 'VV' in opts.bin: var = 'VV_bdt'
        else: var = 'gg_plus_ZH125_high_Zpt'

    if opts.var == 'CRBDT':
        if 'LowPt' in opts.bin: var = 'gg_plus_ZH125_low_Zpt_CR'
        elif 'MedPt' in opts.bin: var = 'gg_plus_ZH125_med_Zpt_CR'
        elif 'HighPt' in opts.bin: var = 'gg_plus_ZH125_high_Zpt_CR'
        else: var = 'gg_plus_ZH125_high_Zpt_CR'


    #if 'BDT' in var:
    #    region = 'BDT'    
    #else:
    
    region = opts.bin

    ws_var = config.get('plotDef:%s'%var,'relPath')

    print 'ws_var:', ws_var
    
    if opts.var == 'BDT':
        ws_var = ROOT.RooRealVar(ws_var,ws_var,-1, 1.)
    else:
        ws_var = ROOT.RooRealVar(ws_var,ws_var, -1, 1.)

    blind = eval(config.get('Plot:%s'%region,'blind'))
    #blind = True
 
        
    print 'config:', config
    print 'var: ', var
    print 'region: ', region
    
    Stack=StackMaker(config,var,region,True)
    
    if 'low' in opts.bin or 'ch1_Wenu' == opts.bin or 'ch2_Wmunu' == opts.bin:
        Stack.addFlag2 = 'Low p_{T}(V)'
    elif 'MedPt' in opts.bin or 'ch1_Wenu2' == opts.bin or 'ch2_Wmunu2' == opts.bin:
        Stack.addFlag2 = 'Intermediate p_{T}(V)'
    elif 'high' in opts.bin or 'ch1_Wenu3' == opts.bin or 'ch2_Wmunu3' == opts.bin:
        Stack.addFlag2 = 'High p_{T}(V)'
        

    # check for pre or post fit options    
    preFit = False
    addName = 'PostFit_%s' %(opts.fit)
    if not opts.mlfit:
        addName = 'PreFit'
        preFit = True

    print '\n-----> Fit Type(opts.fit)  : ', opts.fit
    print '               (opts.mlfit): ', opts.mlfit
    print '               preFit      : ', preFit
    print '               opts.bin    : ', opts.bin
    
    Stack.options['pdfName'] = '%s_%s_%s.pdf'  %(var,opts.bin,addName)
    
    log = eval(config.get('Plot:%s'%region,'log'))
    

    if 'Zll' in opts.bin or 'Zee' in opts.bin or 'Zuu' in opts.bin or 'Zmm' in opts.bin:
        #setup = config.get('Plot_general','setup').split(',')
        setup = ['ZH', 'ggZH', 'DY2b', 'DY1b', 'DYlight', 'TT', 'VVHF', 'VVLF', 'ST']
        signalList = ['ZH']
        
        #channel = 'ZllHbb'

        # For my own fits
        channel = 'ZllHbb'

        if 'Zee' in opts.bin: lep_channel = 'Zee'
        elif 'Zuu' in opts.bin: lep_channel = 'Zmm'

        region_dic = {'BDT':'SIG',' Zlf':'Zlf','Zhf':'Zhf','TT':'TT', '13TeV':'SIG'}
        region_name =  [region_dic[key] for key in region_dic if (key in opts.bin)]
        
        if 'minCMVA' not in opts.var:
            region_name = region_name[0]
        else:
            if 'Zlf' in opts.bin: region_name = 'Zlf'
            if 'Zhf' in opts.bin: region_name = 'Zhf'
            if 'ttbar' in opts.bin: region_name = 'TT'
        
        if 'low' in opts.bin or 'Low' in opts.bin: pt_region_name  = 'low'
        if 'high' in opts.bin or 'High' in opts.bin: pt_region_name = 'high'

        
        # ['ZllHbb', 'ch1', 'Zmm', 'SIG', 'low']
        if 'Zmm' in lep_channel and 'low' in pt_region_name: zll_index = 'ch1'
        if 'Zmm' in lep_channel and 'high' in pt_region_name: zll_index = 'ch3'
        if 'Zee' in lep_channel and 'high' in pt_region_name: zll_index = 'ch4'
        if 'Zee' in lep_channel and 'low' in pt_region_name: zll_index = 'ch2'

        # binning
        nBins = Stack.nBins
        xMin  = Stack.xMin
        xMax  = Stack.xMax

        # for stat hists
        if 'Zee' in lep_channel and 'low' in pt_region_name and 'minCMVA' not in opts.var:
            stat_name = 'ZeeLowPt_13TeV'
        if 'Zee' in lep_channel and 'high' in pt_region_name and 'minCMVA' not in opts.var:
            stat_name = 'ZeeHighPt_13TeV'
        if 'Zmm' in lep_channel and 'low' in pt_region_name and 'minCMVA' not in opts.var:
            stat_name = 'ZuuLowPt_13TeV'
        if 'Zmm' in lep_channel and 'high' in pt_region_name and 'minCMVA' not in opts.var:
            stat_name = 'ZuuHighPt_13TeV'
        
        if 'minCMVA' in opts.var:    
            if 'low' in pt_region_name:
                if 'Zmm' in lep_channel:
                    if 'Zlf' in region_name: stat_name = 'Zlf_low_Zuu'
                    if 'Zhf' in region_name: stat_name = 'Zhf_low_Zuu'
                    if 'TT' in region_name: stat_name = 'ttbar_low_Zuu'
                else:
                    if 'Zlf' in region_name: stat_name = 'Zlf_low_Zee'
                    if 'Zhf' in region_name: stat_name = 'Zhf_low_Zee'
                    if 'TT' in region_name: stat_name = 'ttbar_low_Zee'

            if 'high' in pt_region_name:
                if 'Zmm' in lep_channel:
                    if 'Zlf' in region_name: stat_name = 'Zlf_high_Zuu'
                    if 'Zhf' in region_name: stat_name = 'Zhf_high_Zuu'
                    if 'TT' in region_name: stat_name = 'ttbar_high_Zuu'
                else:
                    if 'Zlf' in region_name: stat_name = 'Zlf_high_Zee'
                    if 'Zhf' in region_name: stat_name = 'Zhf_high_Zee'
                    if 'TT' in region_name: stat_name = 'ttbar_high_Zee'



    if 'Wmn' in opts.bin or 'Wen' in opts.bin:
        setup = ['WH', 'ZH', 'Wj2b', 'Wj1b', 'Wj0b','DY2b', 'DY1b', 'DYlight', 'TT', 'VVHF', 'VVLF', 'ST']
        signalList = ['ZH','WH']

        channel = 'WlnHbb'
        if 'Wmn' in opts.bin: lep_channel = 'Wmn'
        if 'Wen' in opts.bin: lep_channel = 'Wen'

        pt_region_name = 'none'

        if opts.var == 'BDT':

            region_name = 'SR'
            #region_name = lep_channel+'HighPt'
            
            # binning
            nBins = 23
            xMin  = -1
            xMax  = 1
            
            #nBins = 10
            #xMin  = 0.3
            #xMax  = 1

            #if 'Zbb' in opts.dc:
            #    print '--> Zbb Cards!!!'
            #    nBins = 11
            #    xMin  = 0.2
            #    xMax  = 1

                    
            stat_name = 'BDT_'+lep_channel+'HighPt_'
            
        else:
            if 'tt' in region: region_name  = 'TTCR'
            
            if 'whf' in region: 
                if 'High' in opts.bin:
                    region_name = 'WHFCRhigh'
                else:
                    region_name = 'WHFCRlow'

            if 'wlf' in region: region_name = 'WLFCR'

            # if 'tt' in region: region_name  = 'tt'+lep_channel
            
            # if 'whf' in region: 
            #     if 'High' in opts.bin:
            #         region_name = 'whf'+lep_channel+'High'
            #     else: region_name = 'whf'+lep_channel+'Low'

            # if 'wlf' in region: region_name = 'wlf'+lep_channel

            stat_name = 'BDT_'+opts.bin+'_'
            
            
            # binning
            nBins = 15
            xMin  = -1
            xMax  = 1

    if 'Znn' in opts.bin:
        setup = ['ZH', 'ggZH', 'WH', 'DY2b', 'DY1b', 'DYlight', 'Wj2b', 'Wj1b', 'Wj0b','TT', 'VVHF', 'VVLF', 'ST']
        signalList = ['ZH', 'WH']
        
        channel = 'ZnnHbb'
        lep_channel = 'ZnnHbb'
        pt_region_name = 'HighPt'

        if opts.var == 'BDT': 
            region_name = 'Signal'
            # binning
            nBins = 35
            xMin  = -0.8
            xMax  = 1

            stat_name = 'Znn_13TeV_Signal'

        else:
            if 'QCD' in opts.dc: 
                region_name = 'QCD'
                stat_name = 'Znn_13TeV_QCD'
            if 'TT' in opts.dc: 
                region_name = 'TT'
                stat_name = 'Znn_13TeV_TT'
            if 'Zbb' in opts.dc and 'TT' not in opts.dc: 
                region_name = 'Zbb'
                stat_name = 'Znn_13TeV_Zbb'
            if 'Zlight' in opts.dc: 
                region_name = 'Zlight'
                stat_name = 'Znn_13TeV_Zlight'

            # binning
            nBins = 40
            xMin  = -1
            xMax  = 1
            

    print '############'
    print 'Channel is', channel
    print 'lepton channel is', lep_channel
    print 'region_name is', region_name
    print 'pt region_name is', pt_region_name
        

    print '/n----> The Binning:'
    print 'nBins:', nBins
    print 'xMin:', xMin
    print 'xMax:', xMax
    

    if dataname == 'Zmm' or dataname == 'Zee': 
        try:
            setup.remove('W1b')
            setup.remove('W2b')
            setup.remove('Wlight')
            setup.remove('WH')
        except:
            print '@INFO: Wb / Wligh / WH not present in the datacard'
    if not dataname == 'Znn' and 'QCD' in setup: 
        setup.remove('QCD')


    Stack.setup = setup

    Dict = eval(config.get('LimitGeneral','Dict'))
    lumi = eval(config.get('Plot_general','lumi'))
    
    options = copy(opts)
    options.dataname = "data_obs"
    options.mass = 0
    options.format = "%8.3f +/- %6.3f"
    options.channel = opts.bin
    options.excludeSyst = []
    options.norm = False
    options.stat = False
    options.bin = True # fake that is a binary output, so that we parse shape lines
    options.out = "tmp.root"
    options.fileName = args[0]
    options.filename = region
    options.cexpr = False
    options.fixpars = False
    options.libs = []
    options.verbose = 0
    options.poisson = 0
    options.nuisancesToExclude = []
    options.noJMax = None
    
    theBinning = ROOT.RooFit.Binning(nBins,xMin,xMax)
    
    # for prefit erros
    prefit_error_histos  = []
    postfit_error_histos = []

    histos = []
    typs = []
    shapes = {}
    shapesUp = [[] for _ in range(0,len(setup))]
    shapesDown = [[] for _ in range(0,len(setup))]

    sigCount = 0
    Overlay = []
    prefit_overlay = []

    dirname = ''
    ####
    #Open the mlfit.root and retrieve the mc
    file = ROOT.TFile.Open(opts.mlfit)
    if file == None: raise RuntimeError, "Cannot open file %s" % opts.mlfit
    print '\n\n-----> Fit File: ',file

    fit_dir = 'shapes_fit_s'

    #if not ROOT.gDirectory.cd('shapes_fit_s'):
    if not ROOT.gDirectory.cd(fit_dir):
        print '@ERROR: didn\'t find the shapes_fit_s directory. Aborting'
        sys.exit()

    for dir in ROOT.gDirectory.GetListOfKeys():

        dirinfo = dir.GetName().split('_')

        print 'dirinfo:', dirinfo

        if 'Znn' in dirinfo[0] and 'Znn' not in opts.bin: continue
        if 'ZllHbb' in dirinfo[0] and ('Zmm' not in lep_channel and 'Zee' not in lep_channel): continue
        if 'W' in dirinfo[0] and 'W' not in opts.bin: continue
        
        if 'W' in opts.bin:
            print 'channel, lepton channel, region_name:', channel, lep_channel, region_name
            #if not (dirinfo[0] == channel and dirinfo[1] == lep_channel and dirinfo[2] == region_name):
            if not (dirinfo[0] == channel and dirinfo[1] == lep_channel and dirinfo[2] == region_name): 
                continue
            else: print '!!! Match !!!'


        if 'Znn' in opts.bin:
            print 'channel, lepton channel, region_name, pt_region_name:', channel, lep_channel, region_name, pt_region_name
            if not (dirinfo[0] == channel and dirinfo[1] == lep_channel and dirinfo[2] == region_name):
                continue
            else: print '!!! Match !!!'
    

        if 'Zuu' in opts.bin or 'Zee' in opts.bin:
            print 'channel, zll index, lepton channel, region_name, pt_region_name:', channel, zll_index, lep_channel, region_name, pt_region_name
            if not (dirinfo[0] == channel and dirinfo[1] == zll_index and dirinfo[2] == lep_channel and dirinfo[3] == region_name and dirinfo[4] == pt_region_name):
                continue
            else: print '!!! Match !!!'


        print 'Directory:', dir.GetName()
        
        dirname = dir.GetName()

        # Pull out the MC stat uncertainties first
        #hists_WenHighPt40.root
        #vhbb_WenHighPt40_13TeV.txt

        if 'W' in opts.bin:
            stat_filename = opts.dc.replace('.txt', '.root')
            stat_filename = stat_filename.replace('vhbb', 'hists')
            stat_filename = stat_filename.replace('_13TeV', '')

        else :
            stat_filename = opts.dc.replace('.txt', '.root')
            stat_filename = stat_filename.replace('DC_', '')
        

        print '\n Opening card for MC stat hists:', stat_filename
        print 'Dir name:', stat_name

        stat_file = ROOT.TFile.Open(stat_filename)
        if 'W' not in opts.bin: ROOT.gDirectory.cd(stat_name)
        stat_hists = {}
        
        for s in setup:
            for dir in ROOT.gDirectory.GetListOfKeys():
                #print 'dir:', dir.GetName()
                
                if 'W' in opts.bin:
                    wlvname = dir.GetName().replace(stat_name,'')
                    if wlvname == Dict[s]:
                        stat_hists[wlvname] = ROOT.gDirectory.Get(dir.GetName()).Clone()
                        
                if dir.GetName() == Dict[s]:
                    stat_hists[dir.GetName()] = ROOT.gDirectory.Get(dir.GetName()).Clone()
                 
                    
       
        #stat_file.Close()
        print '\nStat_hists:', stat_hists

        file = ROOT.TFile.Open(opts.mlfit)
        #ROOT.gDirectory.cd('shapes_fit_s')
        ROOT.gDirectory.cd(fit_dir)

        ROOT.gDirectory.cd(dirname)
        subdir_list = [x for x in ROOT.gDirectory.GetListOfKeys()]
        i = 0
        for s in setup:
            print '\ns:', s
            found = False
            
            #for subdir in ROOT.gDirectory.GetListOfKeys():
            for subdir in subdir_list:
                print 'subdir name is', subdir.GetName()
                print 'Dict Key is', Dict[s]
                if subdir.GetName() == Dict[s]:
                    found = True
                    
                    # Set Histos postFit shapes and preFit errors
                    hist = rebinHist(ROOT.gDirectory.Get(subdir.GetName()).Clone(), nBins, xMin, xMax, dirname, subdir, prefit_error_histos, postfit_error_histos, stat_hists, opts.bin)

                    histos.append(hist)
                    typs.append(s)
                    
                    
                    if s in signalList:
                        hist.SetTitle(s)
                        if i==0:
                            Overlay.append(hist)
                            i+=1
                        else:
                            Overlay[0].Add(hist)


                    break

            if not found:
                print '@ERROR: didn\'t find  the postfit histogram. Aborting'
                hist = ROOT.TH1F(Dict[s], Dict[s], nBins, xMin, xMax)
                histos.append(hist)
                typs.append(s)
                #sys.exit()
        #ROOT.gDirectory.cd('/shapes_prefit/'+dirname)
        #total = rebinHist(ROOT.gDirectory.Get('total').Clone(), Stack.nBins, Stack.xMin, Stack.xMax)
        #total.SetTitle('prefit')
        #prefit_overlay.append(total)
        break


    # Get the total pre/post fit error
    #print '\n Calculating final pre/post fit errors'
    #print prefit_error_histos
    for i,iErrorHist in enumerate(prefit_error_histos):
        #print i,iErrorHist
        if i == 0: 
            temp_prefit_error = iErrorHist.Clone()
        else:
            temp_prefit_error.Add(iErrorHist)
    
    for i,iErrorHist in enumerate(postfit_error_histos):
        #print i,iErrorHist
        if i == 0:
            temp_postfit_error = iErrorHist.Clone()
        else:
            temp_postfit_error.Add(iErrorHist)

    final_prefit_error = ROOT.TGraphAsymmErrors(temp_prefit_error)
    final_postfit_error = ROOT.TGraphAsymmErrors(temp_postfit_error)

    total   = [[]]*nBins
    errUp   = [[]]*nBins
    errDown = [[]]*nBins

    total_post   = [[]]*nBins
    errUp_post   = [[]]*nBins
    errDown_post = [[]]*nBins

    # rebin the final errors
    for bin in range(1,nBins+1):
        binError = temp_prefit_error.GetBinError(bin)
        total[bin-1] = temp_prefit_error.GetBinContent(bin)
        errUp[bin-1] = [binError]
        errDown[bin-1] = [binError]

        binError_post = temp_postfit_error.GetBinError(bin)
        total_post[bin-1] = temp_postfit_error.GetBinContent(bin)
        errUp_post[bin-1] = [binError_post]
        errDown_post[bin-1] = [binError_post]

    #Add all in quadrature
    totErrUp   =[sqrt(sum([x**2 for x in bin])) for bin in errUp]
    totErrDown =[sqrt(sum([x**2 for x in bin])) for bin in errDown]
    
    totErrUp_post   =[sqrt(sum([x**2 for x in bin])) for bin in errUp_post]
    totErrDown_post =[sqrt(sum([x**2 for x in bin])) for bin in errDown_post]

    for bin in range(1,nBins+1):
        if not total[bin-1] == 0:
            point = histos[0].GetXaxis().GetBinCenter(bin)
            final_prefit_error.SetPoint(bin-1,point,1)
            final_prefit_error.SetPointEYlow(bin-1,totErrDown[bin-1]/total[bin-1])
            final_prefit_error.SetPointEYhigh(bin-1,totErrUp[bin-1]/total[bin-1])
            
        if not total_post[bin-1] == 0:
            point = histos[0].GetXaxis().GetBinCenter(bin)
            final_postfit_error.SetPoint(bin-1,point,1)
            final_postfit_error.SetPointEYlow(bin-1,totErrDown_post[bin-1]/total_post[bin-1])
            final_postfit_error.SetPointEYhigh(bin-1,totErrUp_post[bin-1]/total_post[bin-1])


    # =================================================
    ##### Read data
    print '\n#### Datafile is ',opts.dc
    dc_file= open(opts.dc, "r")
    os.chdir(os.path.dirname(opts.dc))
    DC = parseCard(dc_file, options)
    if not DC.hasShapes: DC.hasShapes = True
    MB = ShapeBuilder(DC, options)
    data0 = MB.getShape(opts.bin,'data_obs')
    print data0
    if (data0.InheritsFrom("RooDataHist")):
        data0 = ROOT.RooAbsData.createHistogram(data0,'data_obs',ws_var,theBinning)
        data0.SetName('data_obs')
    datas=[data0]
    datatyps = [None]
    datanames=[dataname] 
    
    print '\nDATA HIST:', data0
    print 'Data name:', dataname
    
    # if opts.var == 'BDT':
    #     print '!!!! Blinding !!!!'
        
    #     if 'Zee' in dataname or 'Zuu' in dataname:
    #         for bin in range(4,datas[0].GetNbinsX()+1):
    #             datas[0].SetBinContent(bin,0)

    #     if 'Znn' in dataname:
    #         for bin in range(20,datas[0].GetNbinsX()+1):
    #             datas[0].SetBinContent(bin,0)

    #     if 'W' in dataname:
    #         for bin in range(4,datas[0].GetNbinsX()+1):
    #             #print datas[0].GetBinContent(bin,0)
    #             datas[0].SetBinContent(bin,0)


    for bin in range(1,datas[0].GetNbinsX()):
        print 'Data in Bin', bin, ':', datas[0].GetBinContent(bin,0)
            
    # =======================================================
    
    #if 'VV' in opts.bin:
    if isVV:
        signalList = ['VVHF',' VVHF']

    print 'Signal List:', signalList 

    #histos.append(copy(Overlay))

    if 'ZH' in signalList and 'WH' in signalList:
        #typs.append('WH')
        #if 'ZH' in Stack.setup: Stack.setup.remove('ZH')
        #if 'WH' in Stack.setup: Stack.setup.remove('WH')
        #Stack.setup.insert(0,'WH')
        #print 'Stack.setup:', Stack.setup
        typs.append('WH')
        typs.append('ZH')

    #elif 'ZH' in signalList:
        #Stack.setup.remove('WH')
        #typs.append('ggZH')
    #    typs.append('ZH')

    if 'VVb' in signalList or 'VVHF' in signalList:
        typs.append('WH')
        typs.append('ZH')
        typs.append('VVHF')

        if 'VVHF' in Stack.setup: 
            Stack.setup.remove('VVHF')
            Stack.setup.insert(0,'VVHF')
        
        if 'ZH' in Stack.setup: 
            Stack.setup.remove('ZH')
            Stack.setup.insert(-1,'ZH')

        if 'WH' in Stack.setup: 
            Stack.setup.remove('WH')
            Stack.setup.insert(-1,'WH')

        if 'ggZH' in Stack.setup: 
            Stack.setup.remove('ggZH')
            Stack.setup.insert(-1,'ggZH')

            

    Stack.nBins = nBins
    Stack.xMin  = xMin
    Stack.xMax  = xMax
    
    print '\n-----> Stack.setup(double check)...', Stack
    print 'Post Histos:', histos
    print 'Datas:', datas
    print 'typs:', typs
    print 'setup:', Stack.setup

        
    Stack.histos = histos
    Stack.typs = typs
    Stack.datas = datas
    Stack.datatyps = datatyps
    Stack.datanames= datanames
    Stack.filename = region
    
    #if opts.var is not 'BDT':
    #Stack.prefit_overlay = [prefit_overlay]

    #if '13TeV' in region:
    Stack.overlay = Overlay
    print '\n\n\t\t Overlay: ',Stack.overlay
    
    
    # Add custom postFit errors
    #Stack.AddErrors = final_prefit_error
    Stack.AddErrors_Postfit = final_postfit_error
    
    if dataname == 'Wtn': 
        lumi = 18300.
    Stack.lumi = lumi
    Stack.doPlot()

    print 'i am done!\n'
#-------------------------------------------------


if __name__ == "__main__":
    drawFromDC()
    sys.exit(0)

#  LocalWords:  Zee
