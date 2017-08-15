import ROOT

def renewHist(hist,reference,min,max):
    theHist = hist.Clone()
    theReference = reference.Clone()
    theHist.SetLineWidth(1)
    theHist.SetMarkerSize(1)
    return theHist, theReference
    nBins = int((max-min)/hist.GetBinWidth(1))
    theHist = ROOT.TH1F('hist%s' %(hist.GetName()), 'hist%s' %(hist.GetName()), nBins, min, max)
    theHist.SetDefaultSumw2(ROOT.kTRUE)
    theReference = ROOT.TH1F('reference%s' %(hist.GetName()), 'reference%s' %(hist.GetName()), nBins, min, max)
    theReference.SetDefaultSumw2(ROOT.kTRUE)
    for i in range(0,hist.GetNbinsX()+1):
        weAreAt = hist.GetBinCenter(i)
        if hist.GetBinLowEdge(i) < min: continue
        if hist.GetBinLowEdge(i)+hist.GetBinWidth(i) > max: continue
        theHist.SetBinContent(theHist.FindBin(weAreAt),hist.GetBinContent(i))
        theHist.SetBinError(theHist.FindBin(weAreAt),hist.GetBinError(i))
    for i in range(0,reference.GetNbinsX()+1):
        weAreAt = reference.GetBinCenter(i)
        if reference.GetBinLowEdge(i) < min: continue
        if reference.GetBinLowEdge(i)+reference.GetBinWidth(i) > max: continue
        theReference.SetBinContent(theReference.FindBin(weAreAt),reference.GetBinContent(i))
        theReference.SetBinError(theReference.FindBin(weAreAt),reference.GetBinError(i))
    return theHist, theReference

def getRatio(hist, reference, min, max, yTitle="", maxUncertainty = 1000.000, restrict=True):

    from ROOT import gROOT
   
    theHist, theReference = renewHist(hist, reference, min, max)
    #ROOT.gSystem.Load('./myutils/Ratio_C.so') 
    ROOT.gSystem.Load('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_4_7/src/VHbb/python/myutils/Ratio_C.so')
    #ROOT.gSystem.Load('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/python/myutils/Ratio_C.so')
    
    from ROOT import coolRatio

    thePlotter = coolRatio()
    theRatio = thePlotter.make_rebinned_ratios(theHist,theReference,maxUncertainty,False,0)
    refError = thePlotter.make_rebinned_ratios(theHist,theReference,maxUncertainty,False,1)
    theRatio.GetXaxis().SetRangeUser(min,max)
    if restrict:
        theRatio.SetMinimum(0.0)
        theRatio.SetMaximum(1.99)
        #theRatio.SetMinimum(0.5)
        #theRatio.SetMaximum(1.74)
    else:
        theRatio.SetMinimum(int(theRatio.GetMinimum()))
        theRatio.SetMaximum(int(theRatio.GetMaximum()*1.5))
    #theRatio.GetYaxis().SetNdivisions(104)
    theRatio.GetYaxis().SetNdivisions(505)
    theRatio.GetYaxis().SetTitle("Ratio")
    theRatio.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.2)
    theRatio.GetYaxis().SetTitleOffset(0.6)
    theRatio.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.2)
    theRatio.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.2)
    theRatio.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.2)
    theRatio.GetYaxis().SetTitleOffset(0.4)
    theRatio.GetYaxis().CenterTitle(ROOT.kTRUE)
    theRatio.GetYaxis().SetDrawOption("M")
    theRatio.SetXTitle(yTitle)
    theRatio.SetYTitle("Data/MC")
    return theRatio, refError
    
