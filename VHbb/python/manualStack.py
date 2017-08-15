#!/usr/bin/env python
import pickle
import ROOT 
from array import array
import sys, os
from optparse import OptionParser
from copy import copy,deepcopy
from math import sqrt, log10
ROOT.gROOT.SetBatch(True)
from myutils import TdrStyles


###### Manual Settings #######

dir = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/limits/v24_ICHEP_VV_11_22_noRP/'

outpath = '/afs/cern.ch/user/d/dcurry/www/v24_ICHEP_preSF_11_22/PostFit_VH/'
#outpath = '/afs/cern.ch/user/d/dcurry/www/v24_ICHEP_preSF_11_9_NLOWeight/PostFit_VV/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath

os.system(temp_string2)
os.system(temp_string3)

##############################

#setup = ['ZH', 'ggZH', 'DYlight','DY1b', 'DY2b', 'TT', 'VVLF', 'VVHF', 'ST']

setup = ['Zj0b', 'Zj1b', 'ZH', 'ggZH', 'TT', 'VVLF', 'VVHF', 's_Top', 'ggZH', 'DYlight','DY1b', 'DY2b']



#CONFIGURE
argv = sys.argv
parser = OptionParser()
parser.add_option("-R", "--region", dest="region", default="",
                      help="region to plot")
parser.add_option("-M", "--figure_of_merit", dest="fom", default="",
                      help="figure of merit to be used to weight the plots. Possibilities: s/b, s/sqrt(b)")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
parser.add_option("-S", "--subtracted", dest="sub", default="False",
                      help="subtracted plot")
parser.add_option("-L", "--rescale", dest="rescale", default="True",
                      help="rescale by 1/max_weight")
parser.add_option("-T", "--type", dest="type", default="mjj",
                      help="type of plot you want to make: mjj, log10")
parser.add_option("-F", "--format", dest="format", default="pdf",
                      help="outut format for the plot: pdf, root, png, C, jpg, etc.")


(opts, args) = parser.parse_args(argv)
if opts.config =="":
        opts.config = "config"
        
from myutils import BetterConfigParser, printc, ParseInfo, mvainfo, StackMaker, HistoMaker


opts.config.append('13TeVconfig/plots')
opts.config.append('13TeVconfig/configPlot_vars')
opts.config.append('13TeVconfig/paths')
config = BetterConfigParser()
config.read(opts.config)
TdrStyles.tdrStyle()




def get_s_or_b(fName,binmin,binmax,sb):

    #print '\n\n-----> Running def get_s_or_b()...'	
    #print 'fname:', fName
    #print 'binmin:', binmin
    #print 'binmax:', binmax
    #print 's or b:', sb

    s=0
    b=0

    if isinstance(fName,str):
            #histos = get_th1(fName)
            histos = get_th1_allRegions(fName)
    else:
            histos = [fName]
	    
    print '\n\n\t\tget_s_or_b Histos:', histos

    for histo in histos:
        
        print 'Histo:', histo

        if 'data' in histo.GetName(): continue
        for i in range(binmin,binmax+1):
            if 'ZH' in histo.GetName():
                s+=histo.GetBinContent(i)
		print '\n\n\t\t -----> ZH bin content: ', s
            else:
                b+=histo.GetBinContent(i)
                print '\n\n\t\t -----> BKG bin content: ', b

    if 's' in sb:
        return s
    else:
        return b



def get_s_over_b(fName,binmin,binmax):

    print '\n\n\t-----> Running def get_s_over_b...'	
	
    s = get_s_or_b(fName,binmin,binmax,'s')
    b = get_s_or_b(fName,binmin,binmax,'b')
    
    print 'S:', s
    print 'B:', b
    print 's/b:', s/b
    
    return s/b

def get_s_over_sb(fName,binmin,binmax):
    
    print '\n\n\t-----> Running def get_s_over_sb...'

    s = get_s_or_b(fName,binmin,binmax,'s')
    b = get_s_or_b(fName,binmin,binmax,'b')

    print 'S:',s
    print 'B:', b
    print 's/(S+b):', s/(s+b)

    return s/(s+b)

def get_th1(fName, region):
    
    infile = ROOT.TFile.Open(fName,'read')
    
    #print infile  
    
    # Get prefit, or postfit(b or s+b fit)
    fit = 'prefit'
    #fit = 'fit_s'
    
    infile.cd('shapes_'+fit)
    
    '''
    if region == 'Zee_high':
        infile.cd('shapes_'+fit+'/Zee_SIG_high')
    if region == 'Zuu_high':
        infile.cd('shapes_'+fit+'/Zmm_SIG_high')
    if region == 'Zuu_low':
        infile.cd('shapes_'+fit+'/Zmm_SIG_low')
    if region == 'Zee_low':
        infile.cd('shapes_'+fit+'/Zee_SIG_low')
        '''


    # Get the region directory
    if region == 'Zee_high':
        infile.cd('shapes_'+fit+'/ch4_Zee_SIG_high')
    if region == 'Zuu_high':
        infile.cd('shapes_'+fit+'/ch3_Zuu_SIG_high')
    if region == 'Zuu_low':
        infile.cd('shapes_'+fit+'/ch1_Zmm_SIG_low')
    if region == 'Zee_low':
        infile.cd('shapes_'+fit+'/ch2_Zee_SIG_low')

        
    #print 'Current Dir:',ROOT.gDirectory.GetPath()

    th1 = []
    for key in ROOT.gDirectory.GetListOfKeys():
        
        #print key
        
        #infile.cd(str(key.GetTitle()))
        
        #print 'Current Key:', key.GetTitle()
        
        #for key in ROOT.gDirectory.GetListOfKeys():
        
        th1.append(key.ReadObj())

    print '/nTH1 List:', th1
    return th1


def get_th1_allRegions(fName):
    
    #infile = ROOT.TFile.Open(fName,'read')
    
    #print infile  
    
    # Get prefit, or postfit(b or s+b fit)
    fit = 'prefit'
    #fit = 'fit_s'

    th1 = []

    # Get the region directory
    region_list = ['shapes_'+fit+'/ch4_Zee_SIG_high', 'shapes_'+fit+'/ch3_Zmm_SIG_high', 'shapes_'+fit+'/ch1_Zmm_SIG_low', 'shapes_'+fit+'/ch2_Zee_SIG_low']
    #infile.cd('shapes_'+fit+'/ch2_Zee_SIG_low')
    
    for reg in region_list:
     
        infile = ROOT.TFile.Open(fName,'read')
   
        infile.cd(reg)
        
        #print 'Current Dir:',ROOT.gDirectory.GetPath()
  
        for key in ROOT.gDirectory.GetListOfKeys():
            
            #print key
        
            #infile.cd(str(key.GetTitle()))
        
            #print 'Current Key:', key.GetTitle()
            #print 'Title:', str(key.GetTitle())
            
            #for key in ROOT.gDirectory.GetListOfKeys():
            
            if 'Total' in str(key.GetTitle()): continue
            if 'Process' in str(key.GetTitle()): continue
            if 'fit' in str(key.GetTitle()): continue
            if '-' in str(key.GetTitle()): continue
            
            th1.append(key.ReadObj())

    #print '\n\n\t\tTH1 List:', th1
    return th1



def log_s_over_b(fileList, region):

    print '-----> Running def log_s_over_b() for region', region	
    
    #--------------
    # log s  over b
    #--------------

    histosL={}
    s_b_d_histos = {}
    for file in fileList:
        print file
        name = '%s' %file
        histosL[name] = []
        for th1 in get_th1(file, region):
            
            if 'btag' in th1.GetName(): continue
            if '_stats_' in th1.GetName():continue
            if '_j_' in th1.GetName():continue
            if 'eff' in th1.GetName(): continue
            if 'LHE' in th1.GetName(): continue
            if 'total' in th1.GetName(): continue
            if 'total_signal' in th1.GetName(): continue
            if 'total_background' in th1.GetName(): continue
            
            print '\n\t Retrieving TH1 from file: ', th1.GetName(), th1.Integral()
            
            histosL[name].append(th1)

        i = 0
	j = 0

        print ' histosL:',  histosL

        for hist in histosL[name]:
	    
            if 'ZH' == hist.GetName() or 'ggZH' == hist.GetName():

		print '\n\t Setting ',hist, ' as signal...'    
                
		if j == 0:
			hSignal = hist.Clone()
		else:
			hSignal.Add(hist)
		j += 1
			
            elif 'data_obs' in hist.GetName():
                hData = hist.Clone()

            else:
                if i == 0:
                    hBkg = hist.Clone()
                else:
	            #print '\n\t Setting ',hist, ' as background...' 		
                    hBkg.Add(hist)
                i += 1

	# temp hack
        hData = hBkg + hSignal
        
        s_b_d_histos[name] = {'b': hBkg, 's': hSignal, 'd': hData}
        
        
    bmin=-4
    bmax=0
    nbins=10

    log_s_over_b_b = ROOT.TH1F("log_s_over_b_b","log_s_over_b_b",nbins,bmin,bmax)
    log_s_over_b_b.SetFillColor(4)
    log_s_over_b_b.GetXaxis().SetTitle("log(S/B)")
    log_s_over_b_b.GetYaxis().SetTitle("Events")
    log_s_over_b_s = ROOT.TH1F("log_s_over_b_s","log_s_over_b_s",nbins,bmin,bmax)
    log_s_over_b_s.SetFillColor(2)
    log_s_over_b_d = ROOT.TH1F("log_s_over_b_d","log_s_over_b_d",nbins,bmin,bmax)
    log_s_over_b = ROOT.THStack("log_s_over_b","log_s_over_b")

    stack_log_s_over_b = ROOT.THStack("stack_log_s_over_b","stack_log_s_over_b")

    print '\ns_b_d_histos',s_b_d_histos

    for key, s_b_d in s_b_d_histos.iteritems():

	print '\n-----> Looping over Histogram: ', key, s_b_d    

        #for bin in range(0,s_b_d['b'].GetNbinsX()+1):
        for bin in range(1,nbins+1):
            s = s_b_d['s'].GetBinContent(bin)
            b = s_b_d['b'].GetBinContent(bin)
            d = s_b_d['d'].GetBinContent(bin)
            sErr = s_b_d['s'].GetBinError(bin)
            bErr = s_b_d['b'].GetBinError(bin)
            dErr = s_b_d['d'].GetBinError(bin)

            logsb = -3.9
            if b > 0. and s > 0.:
                logsb = log10(s/b)
            elif s > 0.:
                logsb = -0.

	    print '\n\t Calculating log_s/b for bin', bin	
	    print '\t\t sig:',s,'   bgk:',b
            print '\t\t Log_s/b',logsb 
            print '\t\t Data Obs', d

            newBin = log_s_over_b_b.FindBin(logsb) 
            log_s_over_b_b.SetBinContent(newBin, b+log_s_over_b_b.GetBinContent(newBin))
            log_s_over_b_s.SetBinContent(newBin, s+log_s_over_b_s.GetBinContent(newBin))
            log_s_over_b_d.SetBinContent(newBin, d+log_s_over_b_d.GetBinContent(newBin))
            log_s_over_b_b.SetBinError(newBin, sqrt(bErr*bErr+log_s_over_b_b.GetBinError(newBin)*log_s_over_b_b.GetBinError(newBin)))
            #log_s_over_b_s.SetBinError(newBin, sqrt(sErr*sErr+log_s_over_b_s.GetBinError(newBin)*log_s_over_b_s.GetBinError(newBin)))
            log_s_over_b_d.SetBinError(newBin, sqrt(dErr*dErr+log_s_over_b_d.GetBinError(newBin)*log_s_over_b_d.GetBinError(newBin)))
            
    stack = StackMaker(config,'logSB','plot1',False)
    stack.setup = ['ZH','BKG']
    stack.typs = ['ZH','BKG']
    stack.lumi = 12900.
    stack.histos = [log_s_over_b_s,log_s_over_b_b]
    stack.datas = [log_s_over_b_d]
    
    #stack.datanames='data_obs'
    if 'Zee' in region:
        stack.datanames='Zee'
    if 'Zuu' in region:
        stack.datanames='Zuu'
    
    stack.overlay = log_s_over_b_s
    stack.filename = region
    stack.doPlot()
    
    


def log_s_over_b_allRegions(fileList, Region):
    
    print '-----> Running def log_s_over_b() for All Regions'
    
    #--------------
    # log s  over b
    #--------------
    
    region_list = ['Zuu_high', 'Zee_high', 'Zuu_low', 'Zee_low']

    histosL={}
    s_b_d_histos = {}

    for file in fileList:
        for region in region_list:

            #print '\n\tRegion:', region
            
            #print file
            name = '%s' %file
            histosL[region] = []
            for th1 in get_th1(file, region):
            
                if 'btag' in th1.GetName(): continue
                if '_stats_' in th1.GetName():continue
                if '_j_' in th1.GetName():continue
                if 'eff' in th1.GetName(): continue
                if 'LHE' in th1.GetName(): continue
                if 'total' in th1.GetName(): continue
                if 'total_signal' in th1.GetName(): continue
                if 'total_background' in th1.GetName(): continue

                #print '\n\t Retrieving TH1 from file: ', th1.GetName(), th1.Integral()
            
                histosL[region].append(th1)

            i = 0
            j = 0

            #print ' histosL:',  histosL

            for hist in histosL[region]:
	    
                if 'ZH' == hist.GetName() or 'ggZH' == hist.GetName():

                    #print '\n\t Setting ',hist, ' as signal...'    
                
                    if j == 0:
			hSignal = hist.Clone()
                    else:
			hSignal.Add(hist)
                    j += 1
			
                elif 'data_obs' in hist.GetName():
                    hData = hist.Clone()

                else:
                    if i == 0:
                        hBkg = hist.Clone()
                    else:
                        hBkg.Add(hist)
                    i += 1

            # temp hack
            hData = hBkg + hSignal
        
            s_b_d_histos[region] = {'b': hBkg, 's': hSignal, 'd': hData}

    
    bmin=-4
    bmax=0
    nbins=10
    
    log_s_over_b_b = ROOT.TH1F("log_s_over_b_b","log_s_over_b_b",nbins,bmin,bmax)
    log_s_over_b_b.SetFillColor(4)
    log_s_over_b_b.GetXaxis().SetTitle("log(S/B)")
    log_s_over_b_b.GetYaxis().SetTitle("Events")
    log_s_over_b_s = ROOT.TH1F("log_s_over_b_s","log_s_over_b_s",nbins,bmin,bmax)
    log_s_over_b_s.SetFillColor(2)
    log_s_over_b_d = ROOT.TH1F("log_s_over_b_d","log_s_over_b_d",nbins,bmin,bmax)
    log_s_over_b = ROOT.THStack("log_s_over_b","log_s_over_b")

    stack_log_s_over_b = ROOT.THStack("stack_log_s_over_b","stack_log_s_over_b")
    
    print '\ns_b_d_histos',s_b_d_histos

    for key, s_b_d in s_b_d_histos.iteritems():

	print '\n-----> Looping over Histogram: ', key, s_b_d    

        #for bin in range(0,s_b_d['b'].GetNbinsX()+1):
        for bin in range(1,nbins+1):
            s = s_b_d['s'].GetBinContent(bin)
            b = s_b_d['b'].GetBinContent(bin)
            d = s_b_d['d'].GetBinContent(bin)
            sErr = s_b_d['s'].GetBinError(bin)
            bErr = s_b_d['b'].GetBinError(bin)
            dErr = s_b_d['d'].GetBinError(bin)

            logsb = -3.9
            if b > 0. and s > 0.:
                logsb = log10(s/b)
            elif s > 0.:
                logsb = -0.

	    print '\n\t Calculating log_s/b for bin', bin	
	    print '\t\t sig:',s,'   bgk:',b
            print '\t\t Log_s/b',logsb 
            print '\t\t Data Obs', d
            
            newBin = log_s_over_b_b.FindBin(logsb) 
            log_s_over_b_b.SetBinContent(newBin, b+log_s_over_b_b.GetBinContent(newBin))
            log_s_over_b_s.SetBinContent(newBin, s+log_s_over_b_s.GetBinContent(newBin))
            log_s_over_b_d.SetBinContent(newBin, d+log_s_over_b_d.GetBinContent(newBin))
            log_s_over_b_b.SetBinError(newBin, sqrt(bErr*bErr+log_s_over_b_b.GetBinError(newBin)*log_s_over_b_b.GetBinError(newBin)))
            #log_s_over_b_s.SetBinError(newBin, sqrt(sErr*sErr+log_s_over_b_s.GetBinError(newBin)*log_s_over_b_s.GetBinError(newBin)))
            log_s_over_b_d.SetBinError(newBin, sqrt(dErr*dErr+log_s_over_b_d.GetBinError(newBin)*log_s_over_b_d.GetBinError(newBin)))

    stack = StackMaker(config,'logSB','plot1',False)
    stack.setup = ['ZH','BKG']
    stack.typs = ['ZH','BKG']
    stack.lumi = 12900.
    stack.histos = [log_s_over_b_s,log_s_over_b_b]
    stack.datas = [log_s_over_b_d]
    stack.datanames='data_obs'
    stack.overlay = log_s_over_b_s
    stack.filename = Region
    stack.doPlot()
    

def plot(fileList):

    print '-----> Running def plot()...'	

    signalRegion = True
    region = 'signal_Zuu_low_Zpt'
    var = 'HCSV_mass'
    
    # for subtracted bkg mass plot
    #mjj_sub = True
    
    opts.fom = 's/s+b'
    

    print '-----> Making Stacks...'
    stack = StackMaker(config,var,region,signalRegion)

    histosL = []
    overlayL = []

    #7-9 for the higgs
    #5-6 for the VV
    
    binmin=7
    binmax=9

    #binmin=5
    #binmax=6

    max_sb = 0
    max_ssb = 0
    for file in fileList:
        if max_sb < get_s_over_b(file,binmin,binmax):
            max_sb = get_s_over_b(file,binmin,binmax)
        if max_ssb < get_s_over_sb(file,binmin,binmax):
            max_ssb = get_s_over_sb(file,binmin,binmax)
                        
    print '-----> max_ssb: ', max_ssb
    print '-----> max_sb : ', max_sb
    
    for file in fileList:

        #if eval(opts.rescale) == False:
        #        max_sb = 1.
        #        max_ssb = 1.
        for th1 in get_th1_allRegions(file):
        
            print 'Scaling factor for ', th1, ':', get_s_over_sb(file,binmin,binmax)

            if 's/b' in opts.fom:
                th1.Scale(get_s_over_b(th1,binmin,binmax)/max_sb)
            if 's/s+b' in opts.fom:
                print '--->Scaling by s/s+b...'
                #th1.Scale(get_s_over_sb(th1,binmin,binmax)/max_ssb)
                th1.Scale(get_s_over_sb(file,binmin,binmax))

            if 'Zj1b' in th1.GetName():
                    th1.SetName('DY1b')
            if 'Zj2b' in th1.GetName():
                    th1.SetName('DY2b')
            if 'Zj0b' in th1.GetName():
                    th1.SetName('DYlight')
            if 's_Top' in th1.GetName():
                    th1.SetName('ST')

            if 'Wj1b' in th1.GetName():
                    th1.SetName('Wj1b')

            #if mjj_sub:
            #    if 'VVHF' in th1.GetName():
            #        th1.SetName('VV')
            #    if 'VH' in th1.GetName():
            #        th1.SetName('VH')
                    

            # new stack for the overlay plot
            if 'VH' in th1.GetName() or 'VVHF' in th1.GetName() or 'ZH' in th1.GetName():
                    overlayL.append(th1)
            histosL.append(th1)

    print 'histoL'
    print histosL
    typs = []
    typsL = []
    datas = []
    datasL = []

    overlay_typs=[]

    #append the name just once
    for histo in histosL:
        typsL.append(histo.GetName())

        if 'data' in histo.GetName():
            datasL.append(histo)
        
        if 'VH' in histo.GetName() or 'VV' in histo.GetName() or 'ZH' in th1.GetName():
            overlay_typs.append(histo.GetName())

        if 'TT' in histo.GetName(): datasL.append(histo) # temp hack

    #datasL.append(datas)
    #typsL.append(typs)
    print typsL
    print 'Overlay list'
    print overlayL

    #overlay_histo_dict = HistoMaker.orderandadd([{overlay_typs[i]:overlayL[i]} for i in range(len(overlayL))],['VH','VV'])
    
    overlayL2=[]
    stack.histos = histosL
    stack.typs = typsL
    stack.datas = datasL
     #    stack.datatyps = Ldatatyps[v]
    stack.datanames='data_obs'
    
    #for key in overlay_histo_dict:
    #     overlayL2.append(overlay_histo_dict[key])

    mjj_sub = eval(opts.sub)
    
    #if not mjj_sub:
    #     stack.overlay = overlayL2
         
    appendix = ''
    if(eval(opts.rescale) == True):
            appendix = '_rescaled_'
    
    if 's/s+b' in opts.fom:
            stack.options['pdfName'] = stack.options['pdfName'].replace('.pdf','_combined78tev_postFit_s_over_sb'+appendix+'.'+opts.format)
    elif 's/b' in opts.fom:
            stack.options['pdfName'] = stack.options['pdfName'].replace('.pdf','_combined78tev_postFit_s_over_b'+appendix+'.'+opts.format)
    else:
            stack.options['pdfName'] = stack.options['pdfName'].replace('.pdf','_unweighted.'+opts.format)            
    
#    stack.options['pdfName'] = stack.options['pdfName'].replace('.pdf','_highPt_7tev.pdf')
#    stack.options['pdfName'] = stack.options['pdfName'].replace('.pdf','_combined_postFit_s_over_b_Hpt_weight_1.pdf'
    stack.lumi = 18940

    if mjj_sub == False:
        print '\n\t----> Making Nominal Mass plot...'
        stack.doPlot()
    elif mjj_sub == True:
        print '\n\t----> Making Subtracted Mass plot...'
        stack.options['pdfName'] = stack.options['pdfName'].replace('.'+opts.format,'_subtracted.'+opts.format)
        #stack.doSubPlot(['VH','VV'])
        stack.doSubPlot(['VVHF','ZH','ggZH'])

    print 'i am done!\n'





##########################
#### ____ main _____ #####
##########################


### ==== For Mjj =====
fileList = [dir+'mlfit.root']

plot(fileList)


bdt_fileList = []

bdt_fileList += [dir+'mlfit.root']

# Run the modules
print '-----> File Type: ', opts.type 

#log_s_over_b(bdt_fileList, 'Zuu_high')
#log_s_over_b(bdt_fileList, 'Zee_high')
#log_s_over_b(bdt_fileList, 'Zuu_low')
#log_s_over_b(bdt_fileList, 'Zee_low')

#log_s_over_b_allRegions(bdt_fileList, 'AllRegions')

# Move plots to website
os.system("cp /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/plots/basic_out/plot1/*plot1_logSB_125.p* "+ outpath)

os.system("cp /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/plots/basic_out/signal_Zuu_low_Zpt/VV_signal_Zuu_low_Zpt_HCSV_mass_ZH125,ggZH125* "+ outpath)


sys.exit(0)    





