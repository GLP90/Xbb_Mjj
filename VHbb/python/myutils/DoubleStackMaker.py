import ROOT 
ROOT.gROOT.SetBatch(True)
import sys,os
from BetterConfigParser import BetterConfigParser
import TdrStyles
from Ratio import getRatio
from HistoMaker import HistoMaker

class StackMaker:
    def __init__(self, config, var,region,SignalRegion,setup=None):
        section='Plot:%s'%region
        self.var = var
        self.SignalRegion=SignalRegion
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

        '''    
        if not SignalRegion: 
            if 'ZH' in self.setup:
                self.setup.remove('ZH')
            if 'WH' in self.setup:
                self.setup.remove('WH')
        '''

        self.rebin = 1
        if config.has_option(section,'rebin'):
            self.rebin = eval(config.get(section,'rebin'))
        if config.has_option(section,'nBins'):
            self.nBins = int(eval(config.get(section,'nBins'))/self.rebin)
        else:
            self.nBins = int(eval(config.get('plotDef:%s'%var,'nBins'))/self.rebin)
        print self.nBins
        if config.has_option(section,'min'):
            self.xMin = eval(config.get(section,'min'))
        else:
            self.xMin = eval(config.get('plotDef:%s'%var,'min'))
        if config.has_option(section,'max'):
            self.xMax = eval(config.get(section,'max'))
        else:
            self.xMax = eval(config.get('plotDef:%s'%var,'max'))
        self.name = config.get('plotDef:%s'%var,'relPath')
        self.mass = config.get(section,'Signal')
        data = config.get(section,'Datas')
        if '<mass>' in self.name:
            self.name = self.name.replace('<mass>',self.mass)
            print self.name
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
        self.maxRatioUncert = 0.5
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
        print self.setup

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
                self.histos[i].Scale(1./self.histos[i].Integral())
            if self.histos[i].GetMaximum() > maximum:
                maximum = self.histos[i].GetMaximum()
            l.AddEntry(self.histos[j],self.typLegendDict[self.typs[j]],'l')
        aStack.SetMinimum(0.)
        aStack.SetMaximum(maximum*1.5)
        aStack.GetXaxis().SetTitle(self.xAxis)
        aStack.Draw('HISTNOSTACK')
        if self.overlay:
            if self.overlay.Integral() > 0.:
                self.overlay.Scale(1./self.overlay.Integral())
            self.overlay.Draw('hist,same')
            l.AddEntry(self.overlay,self.typLegendDict['Overlay'],'L')
        l.Draw()
        name = '%s/comp_%s' %(self.plotDir,self.options['pdfName'])
        c.Print(name)

    def doPlot(self):
        TdrStyles.tdrStyle()
        histo_dict = HistoMaker.orderandadd([{self.typs[i]:self.histos[i]} for i in range(len(self.histos))],self.setup)
        #sort
        self.histos=[histo_dict[key] for key in self.setup]
        self.typs=self.setup
    
        c = ROOT.TCanvas(self.var,'', 600, 600)
        c.SetFillStyle(4000)
        c.SetFrameFillStyle(1000)
        c.SetFrameFillColor(0)

        #oben = ROOT.TPad('oben','oben',0,0.3 ,1.0,1.0)
        oben = ROOT.TPad('oben','oben',0,0.5 ,1.0,1.0)
        oben.SetBottomMargin(0)
        oben.SetFillStyle(4000)
        oben.SetFrameFillStyle(1000)
        oben.SetFrameFillColor(0)
        #unten = ROOT.TPad('unten1','unten1',0,0.0,1.0,0.17)
        unten = ROOT.TPad('unten1','unten1',0,0.0,1.0,0.29)
        unten.SetTopMargin(0.)
        unten.SetBottomMargin(0.35)
        unten.SetFillStyle(4000)
        unten.SetFrameFillStyle(1000)
        unten.SetFrameFillColor(0)
        #unten1 = ROOT.TPad('unten2','unten2',0,0.17,1.0,0.3)
        unten1 = ROOT.TPad('unten2','unten2',0,0.29,1.0,0.5)
        unten1.SetTopMargin(0.)
        unten1.SetBottomMargin(0.)
        unten1.SetFillStyle(4000)
        unten1.SetFrameFillStyle(1000)
        unten1.SetFrameFillColor(0)


        oben.Draw()
        unten.Draw()
        unten1.Draw()

        oben.cd()
        allStack = ROOT.THStack(self.var,'')     
        #l = ROOT.TLegend(0.68, 0.65,0.92,0.92)
        l = ROOT.TLegend(0.6, 0.5,0.92,0.92)
        l.SetLineWidth(2)
        l.SetBorderSize(0)
        l.SetFillColor(0)
        l.SetFillStyle(4000)
        l.SetTextFont(62)
        #l.SetTextSize(0.035)
        l.SetTextSize(0.052)
        MC_integral=0
        MC_entries=0

        for histo in self.histos:
            MC_integral+=histo.Integral()
        print "\033[1;32m\n\tMC integral = %s\033[1;m"%MC_integral

        #ORDER AND ADD TOGETHER
        #print typs
        #print setup


        if not 'DYc' in self.typs: self.typLegendDict.update({'DYlight':self.typLegendDict['DYlc']})
        print self.typLegendDict

        k=len(self.histos)
    
        for j in range(0,k):
            #print histos[j].GetBinContent(1)
            i=k-j-1
            self.histos[i].SetFillColor(int(self.colorDict[self.typs[i]]))
            self.histos[i].SetLineColor(1)
            allStack.Add(self.histos[i])

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
        elif 'Wtn' in self.datanames:
	        addFlag = 'W(#tau#nu)H(b#bar{b})'
        else:
            addFlag = 'pp #rightarrow VH; H #rightarrow b#bar{b}'
        for i in range(0,len(self.datas)):
            d1.Add(self.datas[i],1)
        print "\033[1;32m\n\tDATA integral = %s\033[1;m"%d1.Integral()
        flow = d1.GetEntries()-d1.Integral()
        if flow > 0:
            print "\033[1;31m\tU/O flow: %s\033[1;m"%flow

        if self.overlay:
            self.overlay.SetLineColor(2)
            self.overlay.SetLineWidth(2)
            self.overlay.SetFillColor(0)
            self.overlay.SetFillStyle(4000)
            self.overlay.SetNameTitle('Overlay','Overlay')

        l.AddEntry(d1,datatitle,'P')
        for j in range(0,k):
            l.AddEntry(self.histos[j],self.typLegendDict[self.typs[j]],'F')
        if self.overlay:
            l.AddEntry(self.overlay,self.typLegendDict['Overlay'],'L')
    
        if self.normalize:
            if MC_integral != 0:	stackscale=d1.Integral()/MC_integral
            if self.overlay:
                self.overlay.Scale(stackscale)
            stackhists=allStack.GetHists()
            for blabla in stackhists:
        	    if MC_integral != 0: blabla.Scale(stackscale)
   
        #if self.SignalRegion:
        #    allMC=allStack.GetStack().At(allStack.GetStack().GetLast()-1).Clone()
        #else:
        allMC=allStack.GetStack().Last().Clone()
        bkgMC=allStack.GetStack().First().Clone()

        sigRatio = allMC.Clone()
        sigRatio.Divide(bkgMC)

        allStack.SetTitle()
        allStack.Draw("hist")
        allStack.GetXaxis().SetTitle('')
        yTitle = 'Entries'
        if not '/' in yTitle:
            yAppend = '%.2f' %(allStack.GetXaxis().GetBinWidth(1)) 
            yTitle = '%s / %s' %(yTitle, yAppend)
        allStack.GetYaxis().SetTitle(yTitle)
        allStack.GetXaxis().SetRangeUser(self.xMin,self.xMax)
        allStack.GetYaxis().SetRangeUser(0,20000)
        allStack.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*1.3)
        allStack.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 1.3)
        allStack.GetYaxis().SetTitleOffset(0.9)
        theErrorGraph = ROOT.TGraphErrors(allMC)
        theErrorGraph.SetFillColor(ROOT.kGray+3)
        theErrorGraph.SetFillStyle(3013)
        theErrorGraph.Draw('SAME2')
        #l.AddEntry(theErrorGraph,"B total uncert.","fl")
        l.AddEntry(theErrorGraph,"Background uncert.","fl")
        Ymax = max(allStack.GetMaximum(),d1.GetMaximum())*1.7
        if self.log:
            allStack.SetMinimum(0.1)
            #Ymax = Ymax*ROOT.TMath.Power(10,1.2*(ROOT.TMath.Log(1.2*(Ymax/0.1))/ROOT.TMath.Log(10)))*(0.2*0.1)
            Ymax = Ymax*ROOT.TMath.Power(10,0.9*(ROOT.TMath.Log(0.9*(Ymax/0.1))/ROOT.TMath.Log(10)))*(0.2*0.1)
            ROOT.gPad.SetLogy()
        allStack.SetMaximum(Ymax)
        c.Update()
        ROOT.gPad.SetTicks(1,1)
        #allStack.Draw("hist")
        l.SetFillColor(0)
        l.SetBorderSize(0)
        
        #if self.overlay:
        #    self.overlay.Draw('hist,same')
        d1.Draw("E,same")
        l.Draw()

        #tPrel = self.myText("CMS",0.17,0.88,1.04)
        #tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%('7TeV',(float(5000.)/1000.)),0.17,0.83)
        #tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%(self.anaTag,(float(self.lumi)/1000.)),0.17,0.78)
        #tAddFlag = self.myText(addFlag,0.17,0.78)
        tPrel = self.myText("CMS Preliminary",0.17,0.85,1.56)
        #tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%('7TeV',(float(5000.)/1000.)),0.17,0.77,1.2)
        tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%(self.anaTag,(float(self.lumi)/1000.)),0.17,0.69,1.2)
        tAddFlag = self.myText(addFlag,0.17,0.61,1.2)
        #tLumi = self.myText("#sqrt{s} =  %s, L = %.1f fb^{-1}"%(self.anaTag,(float(self.lumi)/1000.)),0.17,0.77,1.2)
        #tAddFlag = self.myText(addFlag,0.17,0.69,1.2)

        unten.cd()
        ROOT.gPad.SetTicks(1,1)

        l2 = ROOT.TLegend(0.5, 0.82,0.92,0.95)
        l2.SetLineWidth(2)
        l2.SetBorderSize(0)
        l2.SetFillColor(0)
        l2.SetFillStyle(4000)
        l2.SetTextFont(62)
        #l2.SetTextSize(0.035)
        l2.SetNColumns(2)

        ratio, error = getRatio(d1,allMC,self.xMin,self.xMax,"",self.maxRatioUncert)
        ksScore = d1.KolmogorovTest( allMC )
        chiScore = d1.Chi2Test( allMC , "UWCHI2/NDF")
        print ksScore
        print chiScore
        ratio.SetStats(0)
        ratio.GetXaxis().SetTitle(self.xAxis)
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
            self.AddErrors.SetFillColor(5)
            self.AddErrors.SetFillStyle(1001)
            self.AddErrors.Draw('SAME2')

            l2.AddEntry(self.AddErrors,"MC uncert. (stat. + syst.)","f")

            #ksScore = d1.KolmogorovTest( self.AddErrors )
            #chiScore = d1.Chi2Test( self.AddErrors , "UWCHI2/NDF")


        l2.AddEntry(ratioError,"MC uncert. (stat.)","f")

        #l2.Draw()

        ratioError.Draw('SAME2')
        #ratio.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*3.6)
        ratio.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.6)
        ratio.GetXaxis().SetTitleOffset(0.9)
        #ratio.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 3.6)
        ratio.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.6)
        #ratio.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.8)
        #ratio.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.8)
        ratio.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.0)
        ratio.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.0)
        ratio.GetYaxis().SetTitleOffset(0.55)
        ratio.Draw("E1SAME")
        ratio.SetTitle("")
        ratio.SetYTitle("#frac{Data}{MC(S+B)}")
        if not self.blind:
            tKsChi = self.myText("#chi^{2}_{ }#lower[0.1]{/^{}#it{dof} = %.2f}"%(chiScore),0.17,0.9,1.7)
        m_one_line = ROOT.TLine(self.xMin,1,self.xMax,1)
        m_one_line.SetLineStyle(ROOT.kDashed)
        m_one_line.Draw("Same")
        
        unten1.cd()
        ROOT.gPad.SetTicks(1,1)
        
        ratio1, error1 = getRatio(d1,bkgMC,self.xMin,self.xMax,"",self.maxRatioUncert)
        chiScore1 = d1.Chi2Test( bkgMC , "UWCHI2/NDF")
        ratio1.Draw("E1")
        #l2.Draw()

        ratioError1 = ROOT.TGraphErrors(error1)
        ratioError1.SetFillColor(ROOT.kGray+3)
        ratioError1.SetFillStyle(3013)
        ratioError1.Draw('SAME2')
        sigRatio.SetFillStyle(0)
        sigRatio.SetLineColor(2)
        sigRatio.SetLineWidth(2)
        sigRatio.Draw('HISTSAME')
        ratio1.Draw("E1SAME")
        ratio1.SetTitle("")
        ratio1.SetYTitle("#frac{Data}{MC(B)}")
        #ratio1.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*3.7)
        ratio1.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.7)
        ratio1.GetYaxis().SetTitleOffset(0.4)
        #ratio1.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 3.7)
        ratio1.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.7)

        m_one_line.Draw("Same")

        if not self.blind:
            tKsChi1 = self.myText("#chi^{2}_{ }#lower[0.1]{/^{}#it{dof} = %.2f}"%(chiScore1),0.17,0.865,2.3)
        t0 = ROOT.TText()
        t0.SetTextSize(ROOT.gStyle.GetLabelSize()*2.4)
        t0.SetTextFont(ROOT.gStyle.GetLabelFont())
        if not self.log:
    	    t0.DrawTextNDC(0.1059,0.96, "0")
        if not os.path.exists(self.plotDir):
            os.makedirs(os.path.dirname(self.plotDir))
        name = '%s/%s' %(self.plotDir,self.options['pdfName'])
        c.Print(name)
        fOut = ROOT.TFile.Open(name.replace('.pdf','.root'),'RECREATE')
        for theHist in allStack.GetHists():
            theHist.SetDirectory(fOut)
            if theHist.GetName() == 'ZH' or theHist.GetName() == 'WH':
                theHist.SetName('VH')
            theHist.Write()
        d1.SetName('data_obs')
        d1.SetDirectory(fOut)
        d1.Write()
        fOut.Close()
        #self.doCompPlot(allStack,l)
