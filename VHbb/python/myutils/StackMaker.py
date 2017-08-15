
import ROOT 
ROOT.gROOT.SetBatch(True)
import sys,os
from BetterConfigParser import BetterConfigParser
import TdrStyles
from Ratio import getRatio
from HistoMaker import HistoMaker
import numpy as np
from array import *
from ROOT import TH1

isVV = False
#isVV = True

isOverlay = False
#isOverlay = True

class StackMaker:

    def __init__(self, config, var,region,SignalRegion,setup=None):
        
        section='Plot:%s'%region
        
        self.var = var
        
        self.SignalRegion=SignalRegion
        
        self.region = region
        self.normalize = eval(config.get(section,'Normalize'))
        self.log = eval(config.get(section,'log'))
        if config.has_option('plotDef:%s'%var,'log') and not self.log:
            self.log = eval(config.get('plotDef:%s'%var,'log'))
        self.blind = eval(config.get(section,'blind'))
        if setup is None:
            self.setup=config.get('Plot_general','setup')
            if self.log:
                self.setup=config.get('Plot_general','setupLog')
            self.setup=self.setup.split(',')
        else:
            self.setup=setup
 
        #print '### !!! Setup !!! ###', self.setup
        #print SignalRegion

        '''
        if not SignalRegion: 
            if 'ZH' in self.setup:
                self.setup.remove('ZH')
            if 'WH' in self.setup:
                self.setup.remove('WH')
    
        print '### !!! Setup 2 !!! ###', self.setup
        '''
                
        self.rebin = 1

        if config.has_option(section,'rebin'):
            self.rebin = eval(config.get(section,'rebin'))

        if config.has_option(section,'nBins'):
            self.nBins = int(eval(config.get(section,'nBins'))/self.rebin)
        else:
            self.nBins = int(eval(config.get('plotDef:%s'%var,'nBins'))/self.rebin)
        
        if config.has_option(section,'min'):
            self.xMin = eval(config.get(section,'min'))
        else:
            self.xMin = eval(config.get('plotDef:%s'%var,'min'))

        if config.has_option(section,'max'):
            self.xMax = eval(config.get(section,'max'))
        else:
            self.xMax = eval(config.get('plotDef:%s'%var,'max'))
    
        print 'self.xMax:', self.xMin
        print 'self.xMax:', self.xMax

        self.name = config.get('plotDef:%s'%var,'relPath')
        
        if SignalRegion:
            self.mass = config.get(section,'Signal')
        else:
            self.mass = '125' #use a dummy value

        data = config.get(section,'Datas')

        if '<mass>' in self.name:
            self.name = self.name.replace('<mass>',self.mass)

        if config.has_option('Cuts',region):
            cut = config.get('Cuts',region)
        else:
            cut = None

        if config.has_option(section, 'Datacut'):
            cut=config.get(section, 'Datacut')

        if config.has_option(section, 'doFit'):
            self.doFit=eval(config.get(section, 'doFit'))
        else:
            self.doFit = False

        self.colorDict=eval(config.get('Plot_general','colorDict'))
        self.typLegendDict=eval(config.get('Plot_general','typLegendDict'))
        self.anaTag = config.get("Analysis","tag")
        self.xAxis = config.get('plotDef:%s'%var,'xAxis')

        self.options = {'var': self.name,'name':'','xAxis': self.xAxis, 'nBins': self.nBins, 'xMin': self.xMin, 'xMax': self.xMax,'pdfName': '%s_%s_%s.pdf'%(region,var,self.mass),'cut':cut,'mass': self.mass, 'data': data, 'blind': self.blind}

        if config.has_option('Weights','weightF'):
            self.options['weight'] = config.get('Weights','weightF')
        else:
            self.options['weight'] = None

        self.plotDir = config.get('Directories','plotpath')
        self.maxRatioUncert = 1000.5
        #self.maxRatioUncert = 0.75

        if self.SignalRegion:
            self.maxRatioUncert = 1000.

        self.config = config
        self.datas = None
        self.datatyps = None
        self.overlay = None
        self.lumi = None
        self.histos = None
        self.typs = None
        
        self.AddErrors = None
        self.AddErrors_Postfit = None

        self.addFlag2 = ''
        self.filename = None
        
        
        # for preFit overlay
        self.prefit_overlay = None
        
        print '!!!Region!!!: ', self.region
        print self.options
        if 'Low' in self.region or 'low' in self.region:
            if 'Wen' not in self.region and 'Wmn' not in self.region:
                self.addFlag2 = 'Low p_{T}(V)'
            else:
                self.addFlag2 = 'Low M(jj)'
        if 'High' in self.region or 'high' in self.region:
            if 'Wen' not in self.region and 'Wmn' not in self.region:
                self.addFlag2 = 'High p_{T}(V)'
            elif 'WenHighPt' not in self.region and 'WmnHighPt' not in self.region:
                self.addFlag2 = 'High M(jj)'
        



    @staticmethod
    def myText(txt="CMS Preliminary",ndcX=0,ndcY=0,size=0.8):
        ROOT.gPad.Update()
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextColor(ROOT.kBlack)
        text.SetTextSize(text.GetTextSize()*size)
        text.DrawLatex(ndcX,ndcY,txt)
        return text

    def doCompPlot(self,aStack,l):

        print '----> Making Comparitive Plots...'

        c = ROOT.TCanvas(self.var+'Comp','',600,600)
        c.SetFillStyle(4000)
        c.SetFrameFillStyle(1000)
        c.SetFrameFillColor(0)
        k=len(self.histos)
        l.Clear()
        maximum = 0.
        for j in range(0,k):
            #print histos[j].GetBinContent(1)
            i=k-j-1
            self.histos[i].SetLineColor(int(self.colorDict[self.typs[i]]))
            self.histos[i].SetFillColor(0)
            self.histos[i].SetLineWidth(3)
            if self.histos[i].Integral() > 0.:
                print '---> Normalizing Histograms'
                self.histos[i].Scale(1./self.histos[i].Integral())
                
            if self.histos[i].GetMaximum() > maximum:
                maximum = self.histos[i].GetMaximum()
            l.AddEntry(self.histos[j],self.typLegendDict[self.typs[j]],'l')
        aStack.SetMinimum(0.)
        aStack.SetMaximum(maximum*1.5)
        aStack.GetXaxis().SetTitle(self.xAxis)
        aStack.Draw('HISTNOSTACK')
        l.Draw()

        PlotDir = self.plotDir+self.region
        name = '%s/comp_%s' %(PlotDir,self.options['pdfName'])
        c.Print(name)
        
        # Now in png form
        name2 = name.replace('.pdf', '.png', 2)
        c.Print(name2)


    def doPlot(self):

        #if 'low' in self.filename:
        #    self.addFlag2 = 'Low p_{T}(V)'
        #else: self.addFlag2 = 'High p_{T}(V)'

        TdrStyles.tdrStyle()

        print 'histos:', self.histos
        print 'self.typs:', self.typs
        print 'self.setup:',self.setup

        histo_dict = HistoMaker.orderandadd([{self.typs[i]:self.histos[i]} for i in range(len(self.histos))],self.setup)
        
        print 'histo dict:', histo_dict
        print 'histos:', self.histos
        print 'self.typs:', self.typs

        self.histos=[histo_dict[key] for key in self.setup]
        self.typs=self.setup
    
        #print 'self.histos:', self.histos
        #print 'self.typs:', self.typs
        #print 'histo dict:', histo_dict

        c = ROOT.TCanvas(self.var,'', 600, 600)
        c.SetFillStyle(4000)
        c.SetFrameFillStyle(1000)
        c.SetFrameFillColor(0)
        
        #                               xlow  ylow  xup yup
        oben = ROOT.TPad('oben','oben', 0.0, 0.3, 1.0, 1.0)
        oben.SetBottomMargin(0.0)
        oben.SetFillStyle(4000)
        oben.SetFrameFillStyle(1000)
        oben.SetFrameFillColor(0)
        unten = ROOT.TPad('unten','unten', 0.0, 0.0, 1.0, 0.29)
        unten.SetTopMargin(0.)
        unten.SetBottomMargin(0.35)
        unten.SetFillStyle(4000)
        unten.SetFrameFillStyle(1000)
        unten.SetFrameFillColor(0)

        oben.Draw()
        unten.Draw()

        oben.cd()
        allStack = ROOT.THStack(self.var,'')     
        l = ROOT.TLegend(0.45, 0.6,0.75,0.92)
        l.SetLineWidth(2)
        l.SetBorderSize(0)
        l.SetFillColor(0)
        l.SetFillStyle(4000)
        l.SetTextFont(62)
        l.SetTextSize(0.035)
        l_2 = ROOT.TLegend(0.68, 0.6,0.92,0.92)
        l_2.SetLineWidth(2)
        l_2.SetBorderSize(0)
        l_2.SetFillColor(0)
        l_2.SetFillStyle(4000)
        l_2.SetTextFont(62)
        l_2.SetTextSize(0.035)
        MC_integral=0
        MC_entries=0

        for histo in self.histos:
            MC_integral+=histo.Integral()
            #print histo
            #print 'MC RMS:', histo.GetRMS()
            #print 'MC Mean:', histo.GetMean()

        print "\033[1;32m\n\tMC integral = %s\033[1;m"%MC_integral

        #ORDER AND ADD TOGETHER

        if not 'DYc' in self.typs: self.typLegendDict.update({'DYlight':self.typLegendDict['DYlc']})
        #print self.typLegendDict

        print 'All histos:', self.histos
        
        k=len(self.histos)
        for j in range(0,k):
            i=k-j-1
            data4bin=0
            print '\nColor:', self.histos[i], int(self.colorDict[self.typs[i]]), self.histos[i].Integral()
            self.histos[i].SetFillColor(int(self.colorDict[self.typs[i]]))
            self.histos[i].SetLineColor(1)
            allStack.Add(self.histos[i])
            print '# of MC bins:', self.histos[i].GetNbinsX()+1
            for bin in range(0,self.histos[i].GetNbinsX()+1):
                print 'MC in bin ', bin, ':', self.histos[i].GetBinContent(bin)
                if bin > 11: data4bin += self.histos[i].GetBinContent(bin)
            
            print 'Region:',  self.histos[i]
            print '==== MC in 4 most sensitive BDT bins:', data4bin

            

        print 'StackMaker Data Bins:', self.nBins,self.xMin,self.xMax
        d1 = ROOT.TH1F('noData','noData',self.nBins,self.xMin,self.xMax)
        
        print 'self.datanames:', self.datanames
        print 'Self.var:', self.var
        
        # if 'Wmn' in self.datanames and not 'CMVA' in self.var or 'Wen' in self.datanames and not 'CMVA' in self.var:
        #     if not isVV:
        #         binBoundaries = [0.3, 0.4, 0.5, 0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.0]
                
        #     if isVV:
        #         binBoundaries = [0.3, 0.4, 0.5, 0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 1.0]
                 
        #     bins = array('f', binBoundaries)  
        #     d1 = ROOT.TH1F('noData','noData',self.nBins,bins)
            
            
        # if 'Znn' in self.datanames and 'CMVA' not in self.var:
        #     print 'Rebin Znn'
        #     d1 = ROOT.TH1F('noData','noData',35, -0.8, 1)
        #     Znn_temp_data = ROOT.TH1F('noData','noData',35, -0.8, 1)
            
        Znn_temp_data = d1

        datatitle='Data'
        addFlag = ''

        # if 'Zee' in self.datanames and 'Zuu' in self.datanames or 'Zll' in self.datanames:
        #     if isVV: 
	#         addFlag = '2-lep: Z(l^{-}l^{+})Z(b#bar{b})'
        #     else: addFlag = '2-lep: Z(l^{-}l^{+})H(b#bar{b})'
        # elif 'Zee' in self.datanames:
        #     if isVV: addFlag = '2-lep: Z(e^{-}e^{+})Z(b#bar{b})'
        #     else: addFlag = '2-lep: Z(e^{-}e^{+})H(b#bar{b})'
        # elif 'Zuu' in self.datanames:
        #     if isVV: addFlag = '2-lep: Z(#mu^{-}#mu^{+})Z(b#bar{b})'
        #     else: addFlag = '2-lep: Z(#mu^{-}#mu^{+})H(b#bar{b})'
        # elif 'Znn' in self.datanames:
        #     if isVV: addFlag = '0-lep: Z(#nu#nu)Z(b#bar{b})'
        #     else: addFlag = '0-lep: Z(#nu#nu)H(b#bar{b})'
        # elif 'Wmn' in self.datanames:
        #     if isVV:
        #         addFlag = '1-lep: W(#mu#nu)Z(b#bar{b})'
        #     else: addFlag = '1-lep: W(#mu#nu)H(b#bar{b})'
        # elif 'Wen' in self.datanames:
        #     if isVV: addFlag = '1-lep: W(e#nu)Z(b#bar{b})'
        #     else: addFlag = '1-lep: W(e#nu)H(b#bar{b})'
        # elif 'Wtn' in self.datanames:
	#         addFlag = 'W(#tau#nu)H(b#bar{b})'

        if 'Zee' in self.datanames:
            addFlag = '2-lep (e)'
        elif 'Zuu' in self.datanames:
            addFlag = '2-lep (#mu)'
        elif 'Znn' in self.datanames:
            addFlag = '0-lep'
        elif 'Wmn' in self.datanames:
            addFlag = '1-lep (#mu)'
        elif 'Wen' in self.datanames:
            addFlag = '1-lep (e)'
            
        
        addFlag3 = ''

        if 'Zlf' in self.options['pdfName'] or 'Zlight' in self.options['pdfName']:
            addFlag3 = 'Z+udscg enriched'
        if 'Zhf' in self.options['pdfName'] or 'Zbb' in self.options['pdfName']:
            addFlag3 = 'Z+b#bar{b} enriched'
        if 'TT' in self.options['pdfName'] or 'tt' in self.options['pdfName']:
            addFlag3 = 't#bar{t} enriched'
        if 'whf' in self.options['pdfName']:
            addFlag3 = 'W+b#bar{b} enriched'
        if 'wlf' in self.options['pdfName']:
            addFlag3 = 'W+udscg enriched'
        
        data4bin = 0

        print 'Datafile:', self.datas
        print self.datas[i].GetNbinsX()

        for i in range(0,len(self.datas)):
            print 'Datas:', self.datas
            for bin in range(1,self.datas[i].GetNbinsX()+1):
                print 'Data in bin ', bin, ':', self.datas[i].GetBinContent(bin)
                if bin > 11: data4bin += self.datas[i].GetBinContent(bin)
                
                #if 'Znn' in self.datanames and 'gg_plus' in self.var and bin < 36:
                #   print 'Rebin Znn Data'
                #   Znn_temp_data.SetBinContent(bin, self.datas[i].GetBinContent(bin))
            
            #if 'Znn' in self.datanames and 'gg_plus' in self.var: 
            #    d1.Add(Znn_temp_data,1)
            #else: 
            d1.Add(self.datas[i],1)
            
        print 'Data Region:',  self.options['pdfName']
        print '\n\t ==== Data in 4 most sensitive BDT bins:', data4bin 

        #print "\033[1;32m\n\tDATA integral = %s\033[1;m"%d1.Integral()
        flow = d1.GetEntries()-d1.Integral()

        #print 'Data Mean:', d1.GetRMS()
        #print 'Data RMS:', d1.GetMean()

        if flow > 0:
            print "\033[1;31m\tU/O flow: %s\033[1;m"%flow
        
        #print 'self.xMax:', self.xMin
        #print 'self.xMax:', self.xMax

        if not isOverlay:
            self.overlay = False

        if self.overlay and not isinstance(self.overlay,list):
            self.overlay = [self.overlay]
        if self.overlay:
            print '\n\n\t\t========OVERLAY==========',self.overlay    
            for _overlay in self.overlay:
                #if _overlay.GetName() == 'ZH125':
                if 'ZH' in _overlay.GetName() or 'WH' in _overlay.GetName() or 'log' in _overlay.GetName() and not isVV:
                    _overlay.SetLineColor(int(self.colorDict['ZH']))
                    _overlay.SetLineWidth(2)
                    _overlay.SetFillColor(0)
                    _overlay.SetFillStyle(4000)
                #if _overlay.GetName() == 'ggZH125':
                #if 'ggZH' in _overlay.GetName():
                #    _overlay.SetLineColor(int(self.colorDict['ggZH']))
                #    _overlay.SetLineWidth(2)
                #    _overlay.SetFillColor(0)
                #    _overlay.SetFillStyle(4000)
                
                if isVV:
                    _overlay.SetLineColor(int(self.colorDict['VVHF']))
                

        # PREfit overlay
        if self.prefit_overlay:
            print '\n\n\t\t========PREFIT OVERLAY==========',self.prefit_overlay
            for _prefit_overlay in self.prefit_overlay:
                _prefit_overlay.SetLineColor(6)
                _prefit_overlay.SetLineWidth(2)
                _prefit_overlay.SetFillColor(0)
                _prefit_overlay.SetFillStyle(4000)
                l_2.AddEntry(_prefit_overlay,'PreFit','L')
        
                
        numLegend = 2+k
        if self.overlay:
            numLegend += len(self.overlay)
        l.AddEntry(d1,datatitle,'P')
        for j in range(0,k):
            if j < numLegend/2.-1:
                l.AddEntry(self.histos[j],self.typLegendDict[self.typs[j]],'F')
            else:
                 l_2.AddEntry(self.histos[j],self.typLegendDict[self.typs[j]],'F')
        
        if self.overlay:
            overScale = 100000
            for _overlay in self.overlay: #find minimum scale to use for all overlays
                stackMax = allStack.GetMaximum()
                overMax = _overlay.GetMaximum()
                print 'Overlay:', self.overlay
                print "overScale=",overScale,
                print "overMax=",overMax,
                print "stackMax=",stackMax,
                print "stackMax/overMax=",stackMax/overMax,
                overScale = min(overScale,stackMax/overMax)
                if overScale >= 100000: overScale=100000
                elif overScale >= 50000: overScale=50000
                elif overScale >= 20000: overScale=20000
                elif overScale >= 10000: overScale=10000
                elif overScale >= 5000: overScale=5000
                elif overScale >= 2000: overScale=2000
                elif overScale >= 1000: overScale=1000
                elif overScale >= 500: overScale=500
                elif overScale >= 200: overScale=200
                elif overScale >= 100: overScale=100
                elif overScale >= 50: overScale=50
                elif overScale >= 20: overScale=20
                elif overScale >= 10: overScale=10
                elif overScale >= 5: overScale=5
                elif overScale >= 2: overScale=2
                else: overScale=1
            for _overlay in self.overlay:
                #_overlay.Scale(overScale)
                print '\n\tOverScale:', overScale
                
                #if 'ZH' in _overlay.GetName() or 'log' in _overlay.GetName() and not isVV:
                if not isVV:
                    #l_2.AddEntry(_overlay,self.typLegendDict['VH']+" x"+str(overScale),'L')
                    l_2.AddEntry(_overlay,self.typLegendDict['VH'], 'L')

                    #if 'ZH'in _overlay.GetName():
                    #l_2.AddEntry(_overlay,self.typLegendDict['ZH'],'L')
                    #if 'ggZH' in _overlay.GetName():
                    #l_2.AddEntry(_overlay,self.typLegendDict['ggZH'],'L')
                    
                #if 'VV' in _overlay.GetName():
                if isVV:
                    l_2.AddEntry(_overlay,"VV x"+str(overScale),'L')
                    
                #if 'WH' in _overlay.GetName():
                #    l_2.AddEntry(_overlay,self.typLegendDict['VH']+" x"+str(overScale),'L')

    
        #if self.normalize:
        #if MC_integral != 0:
        #    stackscale = d1.Integral()/MC_integral
                #stackscale = MC_integral
        #else: stackscale = 1

        stackscale = 1
        
        #if self.overlay:
        #    for _overlay in self.overlay:
        #        _overlay.Scale(stackscale)

        #if self.prefit_overlay:
        #    for _prefit_overlay in self.prefit_overlay:
        #        _prefit_overlay.Scale(1)
        
        stackhists = allStack.GetHists()
        #for blabla in stackhists:
        #    if MC_integral != 0: blabla.Scale(stackscale)
       
        allMC = allStack.GetStack().Last().Clone()

        #print 'allStack:', allStack
        #print 'allMC:', allMC
        #print '# of Hists in stack:', allStack.ls()

        allStack.SetTitle()
        allStack.Draw("hist")
        allStack.GetXaxis().SetTitle('')
        
        
        # Tline temp hack for pt balance
        #pt_balance_line = ROOT.TLine(1, 0, 1, 1400)
        #pt_balance_line.SetLineStyle(ROOT.kSolid)
        #pt_balance_line.SetLineColor(ROOT.kRed)
        #pt_balance_line.Draw("Same")
        

        if not d1.GetSumOfWeights() % 1 == 0.0:
            #yTitle = 'S/(S+B) weighted entries'
            yTitle = 'Entries'
        else:
            yTitle = 'Entries'

        if not '/' in yTitle:
            if 'GeV' in self.xAxis:
                yAppend = '%.0f' %(allStack.GetXaxis().GetBinWidth(1)) 
            else:
                yAppend = '%.2f' %(allStack.GetXaxis().GetBinWidth(1)) 
            yTitle = '%s / %s' %(yTitle, yAppend)
            if 'GeV' in self.xAxis:
                yTitle += ' GeV'
        allStack.GetYaxis().SetTitle(yTitle)
        allStack.GetYaxis().SetRangeUser(0,20000)

        allStack.GetXaxis().SetRangeUser(self.xMin,self.xMax)
        #allStack.GetHistogram().GetXaxis().SetTickLength(0)
        allStack.GetHistogram().GetXaxis().SetLabelOffset(999)

        #allStack.GetHistogram().GetYaxis().SetLabelSize(0.01)

        theErrorGraph = ROOT.TGraphErrors(allMC)
        theErrorGraph.SetFillColor(ROOT.kGray+3)
        theErrorGraph.SetFillStyle(3013)
        theErrorGraph.Draw('SAME2')

        l_2.AddEntry(theErrorGraph,"MC uncert. (stat.)","fl")

        # Add mu signal strength
        #l_2.AddEntry(0, '#mu = 1.19', '') 
        
        Ymax = max(allStack.GetMaximum(),d1.GetMaximum())*1.7

        if self.log:
            allStack.SetMinimum(0.1)
            Ymax = Ymax*ROOT.TMath.Power(10,1.2*(ROOT.TMath.Log(1.2*(Ymax/0.1))/ROOT.TMath.Log(10)))*(0.2*0.1)
            #Ymax = Ymax*ROOT.TMath.Power(10,1.3*(ROOT.TMath.Log(1.3*(Ymax/0.1))/ROOT.TMath.Log(10)))*(0.3*0.1)
            ROOT.gPad.SetLogy()
        allStack.SetMaximum(Ymax)
        c.Update()
        ROOT.gPad.SetTicks(1,1)
        l.SetFillColor(0)
        l.SetBorderSize(0)
        l_2.SetFillColor(0)
        l_2.SetBorderSize(0)
        
        if self.overlay:
            for _overlay in self.overlay:
                _overlay.Draw('hist same')

        d1.SetBinErrorOption(TH1.kPoisson)

        d1.Draw("E,same")
        
        # this shows poisson errors for empty data points
        # d1.Draw("E0,same")

        l.Draw()
        l_2.Draw()

        if self.prefit_overlay:
            for _prefit_overlay in self.prefit_overlay:
                _prefit_overlay.Draw('same')
        #d1.Draw("E,same")
        #l.Draw()
        #l_2.Draw()

        tPrel = self.myText("CMS Preliminary",0.17,0.88,0.8)
        if not d1.GetSumOfWeights() % 1 == 0.0:
            tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%(self.anaTag,(float(self.lumi)/1000.)),0.17,0.83)
            #tLumi = self.myText("#sqrt{s} =  %s, L = %.1f pb^{-1}"%(self.anaTag,(float(self.lumi))),0.17,0.78)
        else:
            tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%(self.anaTag,(float(self.lumi)/1000.)),0.17,0.83)
            #tLumi = self.myText("#sqrt{s} =  %s, L = %.1f pb^{-1}"%(self.anaTag,(float(self.lumi))),0.17,0.83)

        tAddFlag = self.myText(addFlag,0.17,0.78)
        #print 'Add Flag %s' %self.addFlag2
        if self.addFlag2:
            tAddFlag2 = self.myText(self.addFlag2,0.17,0.73)
            if addFlag3:
                tAddFlag3 = self.myText(addFlag3,0.17,0.68)
        else:
            if addFlag3:
                tAddFlag3 = self.myText(addFlag3,0.17,0.73)

        unten.cd()
        ROOT.gPad.SetTicks(1,1)

        l2 = ROOT.TLegend(0.3, 0.85,0.93,0.97)
        l2.SetLineWidth(2)
        l2.SetBorderSize(0)
        l2.SetFillColor(0)
        l2.SetFillStyle(4000)
        l2.SetTextSize(0.075)
        l2.SetNColumns(2)

        # Ratio Maker
        ratio, error = getRatio(d1, allMC, self.xMin, self.xMax, "", self.maxRatioUncert)
        ksScore = d1.KolmogorovTest( allMC )
        chiScore = d1.Chi2Test( allMC , "UWCHI2/NDF")

        #For BDT handle the empty data points
        # if 'BDT' in self.xAxis and 'Znn' not in self.options['pdfName'] and 'CR' not in self.options['pdfName']:
            
        #     for bin in range(1,ratio.GetNbinsX()+1):
        #         #print 'Ratio in bin ', bin, ':', ratio.GetBinContent(bin)
        #         #print 'Error in bin ', bin, ':', ratio.GetBinError(bin) 
        #         if ratio.GetBinContent(bin) == 0:
        #             ratio.SetBinContent(bin,0.0001)
                    #print '\t\tRatio in bin ', bin, ':', ratio.GetBinContent(bin)

                    # Set the ratio error for zero data bins.
                    # Formula is ratio^2 * sqrt( (dx/x)^2 + (dy/y)^2) -> delta data/ # MC in that bin
                    #print '\t\tdata error, MC count:', np.sqrt(allStack.GetStack().Last().GetBinContent(bin)), allStack.GetStack().Last().GetBinContent(bin)
                    #temp_error = 1.8 / allStack.GetStack().Last().GetBinContent(bin)
                    #ratio.SetBinError(bin,temp_error)
                    #print '\t\tError in bin ', bin, ':', ratio.GetBinError(bin)

        
        ratio.SetStats(0)
        ratio.GetXaxis().SetTitle(self.xAxis)
        ratio.GetXaxis().SetLabelSize(0.09)
        ratio.GetXaxis().SetLabelOffset(0.03)
        ratio.GetYaxis().SetLabelSize(0.07)
        ratio.GetYaxis().SetLabelFont(22)
        ratio.GetYaxis().SetTitleFont(22)
        print 'Label size:', ratio.GetXaxis().GetLabelSize(), ratio.GetXaxis().GetLabelOffset()

        # Make the Ratio error bars
        ratioError = ROOT.TGraphErrors(error)
        ratioError.SetFillColor(ROOT.kGray+3)
        ratioError.SetFillStyle(3013)
        ratio.Draw("E1")
        if self.doFit:
            fitData = ROOT.TF1("fData", "gaus",0.7, 1.3)
            fitMC = ROOT.TF1("fMC", "gaus",0.7, 1.3)
            print 'Fit on data'
            d1.Fit(fitData,"R")
            print 'Fit on simulation'
            allMC.Fit(fitMC,"R")

        if not self.AddErrors == None:
            self.AddErrors.SetLineColor(1)
            self.AddErrors.SetFillColor(5)
            self.AddErrors.SetFillStyle(3001)
            self.AddErrors.Draw('SAME2')
            l2.AddEntry(self.AddErrors,"MC(stat.+Prefit syst.)","f")

        if not self.AddErrors_Postfit == None:
            self.AddErrors_Postfit.SetLineColor(1)
            #self.AddErrors_Postfit.SetFillColorAlpha(2, 0.60)
            self.AddErrors_Postfit.SetFillColor(5)
            self.AddErrors_Postfit.SetFillStyle(3001)
            self.AddErrors_Postfit.Draw('SAME2')
            l2.AddEntry(self.AddErrors_Postfit,"MC(stat.+Postfit syst.)","f")
            


        l2.AddEntry(ratioError,"MC(stat.)","f")

        ratioError.Draw('SAME2')
        ratio.Draw("E1SAME")
        ratio.SetTitle("")
                
        l2.Draw()
        
        m_one_line = ROOT.TLine(self.xMin,1,self.xMax,1)
        m_one_line.SetLineStyle(ROOT.kSolid)
        m_one_line.Draw("Same")
        
        
        if not self.blind:
            #tKsChi = self.myText("#chi_{#nu}^{2} = %.3f K_{s} = %.3f"%(chiScore,ksScore),0.17,0.9,1.5)
            tKsChi = self.myText("#chi^{2}_{ }#lower[0.1]{/^{}#it{dof} = %.2f}"%(chiScore),0.17,0.895,1.55)
            temp = 0

        #t0 = ROOT.TText()
        #t0.SetTextSize(ROOT.gStyle.GetLabelSize()*2.4)
        #t0.SetTextFont(ROOT.gStyle.GetLabelFont())
        #if not self.log:
    	#    t0.DrawTextNDC(0.1059,0.96, "0")

        PlotDir = self.plotDir+self.region
        if not os.path.exists(PlotDir):
            os.makedirs(os.path.dirname(PlotDir+'/'))
        name = '%s/%s' %(PlotDir, self.options['pdfName'])
        
        if self.log:
            name = '%s/log_%s' %(PlotDir, self.options['pdfName'])
       
        if self.filename != None:
            name = '%s/%s_%s' %(PlotDir, self.filename, self.options['pdfName'])

        if isVV:
            name = '%s/VV_%s' %(PlotDir, self.options['pdfName'])

        c.Print(name)

        # Now in png form
        name2 = name.replace('.pdf', '.png', 2)
        #print '---> name:', name2
        c.Print(name2)
        
        name3= name2.replace('.png', '.root', 3)
        #print '---> name:', name3
        c.Print(name3)
        
        name4= name3.replace('.root', '.C', 4)
        #print '---> name:', name4
        c.Print(name4)
        
        
        
        #print "DATA INTEGRAL: %s" %d1.Integral(d1.GetNbinsX()-2,d1.GetNbinsX()) 
        #fOut = ROOT.TFile.Open(name.replace('.pdf','.root'),'RECREATE')
        #for theHist in allStack.GetHists():
        #    if not self.AddErrors == None and not theHist.GetName() in ['ZH','WH','VH']:
                #print theHist.GetNbinsX()
                #print self.AddErrors.GetN()
                #print error.GetNbinsX()
        #        for bin in range(0,theHist.GetNbinsX()):
        #            theRelativeTotalError = self.AddErrors.GetErrorY(bin)
        #            if error.GetBinError(bin+1) > 0.:
        #                theRelativeIncrease = theRelativeTotalError/error.GetBinError(bin+1)
        #            else:
        #                theRelativeIncrease = 1.
                    #print 'TheTotalRelativeIncrease is: %.2f' %theRelativeIncrease
                    #print 'TheTotalStatError is: %.2f' %error.GetBinError(bin+1)
                    #print 'TheTotalError is: %.2f' %theRelativeTotalError
        #            theHist.SetBinError(bin,theHist.GetBinError(bin)*theRelativeIncrease)
        #    theHist.SetDirectory(fOut)
        #    if theHist.GetName() == 'ZH' or theHist.GetName() == 'WH':
        #        theHist.SetName('VH')
        #    theHist.Write()
        #d1.SetName('data_obs')
        #d1.SetDirectory(fOut)
        #d1.Write()
        #fOut.Close()

        # Make comparison normalized plots
        #self.doCompPlot(allStack,l)
        

    def doSubPlot(self,signal):
        
        TdrStyles.tdrStyle()
        histo_dict = HistoMaker.orderandadd([{self.typs[i]:self.histos[i]} for i in range(len(self.histos))],self.setup)
        
        print '\n\thisto_dict:', histo_dict
        
        sig_histos=[]
        sub_histos=[histo_dict[key] for key in self.setup]
        self.typs=self.setup
        
        print '\n\tSignal List:', signal

        print '\n\tSub histos:', sub_histos

        for key in self.setup:
            if key in signal:
                sig_histos.append(histo_dict[key])
        
        print '\n\tSignal Histos:', sig_histos

        c = ROOT.TCanvas(self.var,'', 600, 600)
        c.SetFillStyle(4000)
        c.SetFrameFillStyle(1000)
        c.SetFrameFillColor(0)
        c.SetTopMargin(0.035)
        c.SetBottomMargin(0.12)

        allStack = ROOT.THStack(self.var,'')
        bkgStack = ROOT.THStack(self.var,'')     
        sigStack = ROOT.THStack(self.var,'')     

        l = ROOT.TLegend(0.55, 0.65,0.86,0.94)
        l.SetLineWidth(2)
        l.SetBorderSize(0)
        l.SetFillColor(0)
        l.SetFillStyle(4000)
        l.SetTextFont(62)
        l.SetTextSize(0.035)
        l_2 = ROOT.TLegend(0.68, 0.6,0.92,0.92)
        l_2.SetLineWidth(2)
        l_2.SetBorderSize(0)
        l_2.SetFillColor(0)
        l_2.SetFillStyle(4000)
        l_2.SetTextFont(62)
        l_2.SetTextSize(0.035)
        MC_integral=0
        MC_entries=0

        for histo in sub_histos:
            MC_integral+=histo.Integral()
            print histo

        print "\033[1;32m\n\tMC integral = %s\033[1;m"%MC_integral
        


        if not 'DYc' in self.typs: self.typLegendDict.update({'DYlight':self.typLegendDict['DYlc']})
        print self.typLegendDict

        k=len(sub_histos)

        # debug
        print '\n\tsub_histos:', sub_histos 
        print 'sig_histos:', sig_histos
    
        for j in range(0,k):
            #print histos[j].GetBinContent(1)
            i=k-j-1
            sub_histos[i].SetFillColor(int(self.colorDict[self.typs[i]]))
            sub_histos[i].SetLineColor(1)
            allStack.Add(sub_histos[i])
            print sub_histos[i].GetName()
            print sub_histos[i].Integral()
            if not sub_histos[i] in sig_histos:
                bkgStack.Add(sub_histos[i])
            if sub_histos[i] in sig_histos:
                sigStack.Add(sub_histos[i])


        sub_d1 = ROOT.TH1F('subData','subData',self.nBins,self.xMin,self.xMax)
        sub_mc = ROOT.TH1F('subMC','subMC',self.nBins,self.xMin,self.xMax)

        d1 = ROOT.TH1F('noData','noData',self.nBins,self.xMin,self.xMax)
        datatitle='Data'
        addFlag = ''
        if 'Zee' in self.datanames and 'Zmm' in self.datanames:
	        addFlag = 'Z(l^{-}l^{+})H(b#bar{b})'
        elif 'Zee' in self.datanames:
	        addFlag = 'Z(e^{-}e^{+})H(b#bar{b})'
        elif 'Zmm' in self.datanames:
	        addFlag = 'Z(#mu^{-}#mu^{+})H(b#bar{b})'
        elif 'Znn' in self.datanames:
	        addFlag = 'Z(#nu#nu)H(b#bar{b})'
        elif 'Wmn' in self.datanames:
	        addFlag = 'W(#mu#nu)H(b#bar{b})'
        elif 'Wen' in self.datanames:
                addFlag = 'W(e#nu)H(b#bar{b})'
        else:
                addFlag = 'pp #rightarrow VH; H #rightarrow b#bar{b}'
        for i in range(0,len(self.datas)):
            print 'DATAs:', self.datas
            print self.datas[i]

            d1.Add(self.datas[i],1)

        print "\033[1;32m\n\tDATA integral = %s\033[1;m"%d1.Integral()
        flow = d1.GetEntries()-d1.Integral()
        if flow > 0:
            print "\033[1;31m\tU/O flow: %s\033[1;m"%flow
        

        numLegend = 1+k
        if self.overlay:
            numLegend += len(self.overlay)
        l.AddEntry(d1,datatitle,'P')
#        l.AddEntry(sub_d1,datatitle,'P')
        for j in range(0,k):
            if self.typs[j] in signal:
                if j < numLegend/2.:
                    l.AddEntry(sub_histos[j],self.typLegendDict[self.typs[j]],'F')
                else:
                    l_2.AddEntry(sub_histos[j],self.typLegendDict[self.typs[j]],'F')
        if self.overlay:
            for _overlay in self.overlay:
                l_2.AddEntry(_overlay,self.typLegendDict['Overlay'+_overlay.GetName()],'L')
     
        if self.normalize:
            if MC_integral != 0: stackscale=d1.Integral()/MC_integral
            if self.overlay:
                for _overlay in self.overlay:
                    _overlay.Scale(stackscale)
            stackhists=allStack.GetHists()
            for blabla in stackhists:
        	    if MC_integral != 0: blabla.Scale(stackscale)
   
        allMC=allStack.GetStack().Last().Clone()
        bkgMC=bkgStack.GetStack().Last().Clone()

        bkgMC_noError = bkgMC.Clone()
        for bin in range(0,bkgMC_noError.GetNbinsX()):
            bkgMC_noError.SetBinError(bin,0.)
        sub_d1 = d1.Clone()
        sub_d1.Sumw2()
        sub_d1.Add(bkgMC_noError,-1)
        sub_mc = allMC.Clone()
        sub_mc.Sumw2()
        sub_mc.Add(bkgMC_noError,-1)

        sigStack.SetTitle()
        sigStack.Draw("hist")
        sigStack.GetXaxis().SetTitle('')
        yTitle = '#sigma weighted entries'
        if not '/' in yTitle:
            yAppend = '%.0f' %(sigStack.GetXaxis().GetBinWidth(1)) 
            yTitle = '%s / %s' %(yTitle, yAppend)
        sigStack.GetYaxis().SetTitle(yTitle)
        sigStack.GetYaxis().SetTitleOffset(1.3)
        sigStack.GetXaxis().SetRangeUser(self.xMin,self.xMax)
        sigStack.GetYaxis().SetRangeUser(-2000,20000)
        sigStack.GetXaxis().SetTitle(self.xAxis)

        theMCOutline = bkgMC.Clone()
        for i in range(1,theMCOutline.GetNbinsX()+1):
            theMCOutline.SetBinContent(i,theMCOutline.GetBinError(i))
        theNegativeOutline = theMCOutline.Clone()
        theNegativeOutline.Add(theNegativeOutline,-2.)

        theMCOutline.SetLineColor(4)
        theNegativeOutline.SetLineColor(4)
        theMCOutline.SetLineWidth(2)
        theNegativeOutline.SetLineWidth(2)
        theMCOutline.SetFillColor(0)
        theNegativeOutline.SetFillColor(0)
        theMCOutline.Draw("hist same")
        theNegativeOutline.Draw("hist same")
        l.AddEntry(theMCOutline,"Sub. MC uncert.","fl")
        
        theErrorGraph = ROOT.TGraphErrors(sigStack.GetStack().Last().Clone())
        theErrorGraph.SetFillColor(ROOT.kGray+3)
        theErrorGraph.SetFillStyle(3013)
        theErrorGraph.Draw('SAME2')
        l.AddEntry(theErrorGraph,"VH + VV MC uncert.","fl")

        Ymax = max(sigStack.GetMaximum(),sub_d1.GetMaximum())*1.7
        Ymin = max(-sub_mc.GetMinimum(),-sub_d1.GetMinimum())*2.7
        if self.log:
            sigStack.SetMinimum(0.1)
            Ymax = Ymax*ROOT.TMath.Power(10,1.2*(ROOT.TMath.Log(1.2*(Ymax/0.1))/ROOT.TMath.Log(10)))*(0.2*0.1)
            ROOT.gPad.SetLogy()
        sigStack.SetMaximum(Ymax)
        sigStack.SetMinimum(-Ymin)
        c.Update()
        ROOT.gPad.SetTicks(1,1)
        #sigStack.Draw("hist")
        l.SetFillColor(0)
        l.SetBorderSize(0)
        
        if self.overlay:
            for _overlay in self.overlay:
                _overlay.Draw('hist,same')
        sub_d1.Draw("E,same")
        l.Draw()

        if self.prefit_overlay:
            for _prefit_overlay in self.prefit_overlay:
                _prefit_overlay.Draw('hist,same')
        sub_d1.Draw("E,same")
        l.Draw()


        tPrel = self.myText("CMS Preliminary",0.17,0.9,0.8)
        #tLumi = self.myText("#sqrt{s} =  7TeV, L = 5.0 fb^{-1}",0.17,0.85)
        tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%(self.anaTag,(float(self.lumi)/1000.)),0.17,0.80)
        tAddFlag = self.myText(addFlag,0.17,0.75)

        ROOT.gPad.SetTicks(1,1)

        l2 = ROOT.TLegend(0.5, 0.82,0.92,0.95)
        l2.SetLineWidth(2)
        l2.SetBorderSize(0)
        l2.SetFillColor(0)
        l2.SetFillStyle(4000)
        l2.SetTextFont(62)
        #l2.SetTextSize(0.035)
        l2.SetNColumns(2)



        if not self.AddErrors == None:
            self.AddErrors.SetFillColor(5)
            self.AddErrors.SetFillStyle(1001)
            self.AddErrors.Draw('SAME2')

            l2.AddEntry(self.AddErrors,"MC uncert. (stat. + syst.)","f")

        print 'plot path:', self.plotDir    
        if not os.path.exists(self.plotDir):
            os.makedirs(os.path.dirname(self.plotDir))
        name = '%s/%s' %(self.plotDir,self.options['pdfName'])
        c.Print(name)
