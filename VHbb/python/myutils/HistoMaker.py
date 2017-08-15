
import sys,os
import pickle
import ROOT 
from array import array
from printcolor import printc
from BetterConfigParser import BetterConfigParser
from TreeCache import TreeCache
from math import sqrt
from copy import copy
import numpy as np
from math import floor
import pdb
#from array import *
import array as ar
#from builtins import any as b_any

class HistoMaker:
    def __init__(self, samples, path, config, optionsList,GroupDict=None):
        self.path = path
        self.config = config
        self.optionsList = optionsList
        self.nBins = optionsList[0]['nBins']
        self.xMin  = optionsList[0]['xMin']
        self.lumi=0.
        self.cuts = []
        self.weight = []
        self.sys_cuts = []

        for options in optionsList:
            self.cuts.append(options['cut'])
            self.weight.append(options['weight'])
            #self.sys_cuts.append(options['sys_cut'])
            
        print '  with Cuts  : ', self.cuts[0]
        print '  and Weights: ', self.weight[0]

        self.tc = TreeCache(self.cuts, samples, path, config)

        self._rebin = False
        self.mybinning = None
        self.GroupDict=GroupDict
        self.calc_rebin_flag = False

        self.Custom_BDT_bins = False
        
        VHbbNameSpace=config.get('VHbbNameSpace','library')
        ROOT.gSystem.Load(VHbbNameSpace)
        
        

    def get_histos_from_tree(self,job,cutOverWrite=None):

        #if self.lumi == 0: 
        #    raise Exception("You're trying to plot with no lumi")
         
        hTreeList=[]
        
        #get the conversion rate in case of BDT plots
        TrainFlag = eval(self.config.get('Analysis','TrainFlag'))
        if TrainFlag:
            BDT_test_cut = 'evt%2!=0'
            #print '\n======== Filling Datacard with BDT Test Events =========='
        else: 
            BDT_test_cut = 'evt%2==0'
            #print '\n======== Filling Datacard with BDT Train Events =========='

        plot_path   = self.config.get('Directories','plotpath')
        addOverFlow = eval(self.config.get('Plot_general','addOverFlow'))
        
        # Get the tree for this sample(not actually cut yet)
        CuttedTree = self.tc.get_tree(job,'1')
        
        # Get the lumiweighted cross section and genWeight from the tree
        if job.type != 'DATA':
            xSec = self.tc.get_scale(job, self.config)
            
            '''
            # FOr temp DY special weights
            if 'Vpt100to250' in job.name:
                 xSec = xSec*(1.0-0.66)
            if 'Vpt250to400' in job.name:
                xSec = xSec*(1.0-0.85)
            if 'Vpt400to650' in job.name:
                xSec =xSec*(1.0-0.98)
            if 'Vpt650toInf' in job.name:
                xSec =xSec*(1.0-1.0)
            '''    
            
            
        if job.type == 'DATA':
            xSec = 1
            
        #print '-----> Job Name, Type: ', job.name, job.type
        #print '       xSec: ', xSec
        #print '       Tree: ', CuttedTree
        #print '    Entries: ', CuttedTree.GetEntries()
        #print '    treeCut: ', options['cut']
        
        eval(self.config.get('Analysis','TrainFlag'))                        
        for options in self.optionsList:
            
            name = job.name
            
            if self.GroupDict is None:
                group=job.group
            else:
                group=self.GroupDict[job.name]
                
                    
            treeVar = options['var']
            name    = options['name']
            #print 'Options:', options
            #print 'Type: ', job.type
            #print 'Name: ', name
            
            if self._rebin or self.calc_rebin_flag:
                nBins = self.nBins
            else:
                nBins = int(options['nBins'])

            xMin = float(options['xMin'])
            xMax = float(options['xMax'])

            if cutOverWrite:
                treeCut=cutOverWrite
            else:
                treeCut='%s'%(options['cut'])
                
            # Add the JEC/JER sys cuts by hand
            #if 'gg_plus_' in treeVar or 'VV' in treeVar:
            if 'Up' in treeVar or 'Down' in treeVar:
                if options['sys_cut']:
                    treeCut='%s'%(options['sys_cut'])
                    print treeVar
                    print '\n\t!!!! JER/JEC Tree SYS Cut:', treeCut

            if 'minCMVA' in treeVar:
                if options['sys_cut']:
                     treeCut='%s'%(options['sys_cut'])
                     print treeVar
                     print '\n\t!!!! JER/JEC Tree SYS Cut:', treeCut


            weightF = '%s'%(options['weight'])    
            
            ##############################
            #Add any special weights here
            if 'Zudsg' in job.name or 'Zcc' in job.name or 'Z1b' in job.name or 'Z2b' in job.name:
                weightF = weightF+'*VHbb::LOtoNLOWeightBjetSplitEtabb(abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]]),Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons))'
                weightF = weightF+'*VHbb::ptWeightEWK_Zll(nGenVbosons[0], GenVbosons_pt[0], VtypeSim, nGenTop, nGenHiggsBoson)'
                weightF = weightF+'*('+job.specialweight+')'
            if '2L2Q' in job.name:
                print '\n\t----> Adding ZZ_2L2Q special weights...'
                weightF = weightF+'*('+job.specialweight+')'
            if 'ttbar' in job.name:
                weightF = weightF+'*VHbb::ttbar_reweight(GenTop_pt[0],GenTop_pt[1],nGenTop)'
            #if 'ZH' in job.name and not 'ggZH' in job.name:
                #weightF = weightF+'*VHbb::ptWeightEWK_Zll_v25(nGenVbosons[0], GenVbosons_pt[0], VtypeSim)'

            ### For temp Inclusive testing ###
            if 'Zudsg' == job.name or 'Z1b' == job.name or 'Z2b' == job.name:
                print '\n\t----> Adding Inclusive lheHT cut...'
                treeCut = treeCut+' & lheHT < 100'
                
            # For high/low SF
            if str(self.config.get('Plot_general', 'doSF')) == 'True':
                
                # PAS SFs
                # if 'V_new_pt >= 50' in treeCut or 'V_new_pt > 50' in treeCut:
                #     print '\n\t !!! Adding RateParam !!!'
                #     if 'Zudsg' in job.name or 'Zcc' in job.name: weightF = weightF+'*(1.01)'
                #     if 'Z1b' in job.name: weightF = weightF+'*(0.98)'
                #     if 'Z2b' in job.name: weightF = weightF+'*(1.09)'
                #     if 'ttbar' in job.name: weightF = weightF+'*(1.00)'
                    
                # if 'V_new_pt >= 150' in treeCut or 'V_new_pt > 150' in treeCut:
                #     print '\n\t !!! Adding RateParam !!!'
                #     if 'Zudsg' in job.name or 'Zcc' in job.name: weightF = weightF+'*(1.02)'
                #     if 'Z1b' in job.name: weightF = weightF+'*(1.02)'
                #     if 'Z2b' in job.name: weightF = weightF+'*(1.28)'
                #     if 'ttbar' in job.name: weightF = weightF+'*(1.04)'
                
                # Zll only SFs
                if 'V_new_pt >= 50' in treeCut or 'V_new_pt > 50' in treeCut:
                    print '\n\t !!! Adding RateParam !!!'
                    if 'Zudsg' in job.name or 'Zcc' in job.name: weightF = weightF+'*(0.97226)'
                    if 'Z1b' in job.name: weightF = weightF+'*(0.98195)'
                    if 'Z2b' in job.name: weightF = weightF+'*(1.158)'
                    if 'ttbar' in job.name: weightF = weightF+'*(1.0435)'
                    
                if 'V_new_pt >= 150' in treeCut or 'V_new_pt > 150' in treeCut:
                    print '\n\t !!! Adding RateParam !!!'
                    if 'Zudsg' in job.name or 'Zcc' in job.name: weightF = weightF+'*(0.99019)'
                    if 'Z1b' in job.name: weightF = weightF+'*(0.94770)'
                    if 'Z2b' in job.name: weightF = weightF+'*(1.3366)'
                    if 'ttbar' in job.name: weightF = weightF+'*(1.1055)'




            # New test for variable BDT bins
            if 'gg_plus' in treeVar or 'VV' in treeVar:
                # binBoundaries = [-1., 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.]
                # nBins = 8.
                # bins = array('f', binBoundaries)
                # hTree = ROOT.TH1F('%s'%job.name,'%s'%job.name,nBins,bins)
                hTree = ROOT.TH1F('%s'%job.name,'%s'%job.name,nBins,xMin,xMax)
            else:
                hTree = ROOT.TH1F('%s'%job.name,'%s'%job.name,nBins,xMin,xMax)
            
            hTree.Sumw2()
            hTree.SetTitle(job.name)
                        
            print '\n-----> Making histograms for variable:', treeVar
            print 'Job.name:', job.name
            print 'weightF:', weightF
            print 'nBins:', nBins, xMin, xMax
            

            if job.type != 'DATA':
                
                if CuttedTree.GetEntries():
                    
                    #if 'trainBDT' in treevar:
                    #    drawoption = '(%s)*(%s & %s)'%(weightF,treeCut,BDT_train_cut)
                    
                    if 'gg_plus' in treeVar or 'VV' in treeVar:
                        print '\n----> Filling Histogram with BDT Test Events Only...'
                        drawoption = '(sign(genWeight))*(%s)*(%s & %s)'%(weightF, treeCut, BDT_test_cut)
                        

                    elif 'vtx' in treeVar or 'EmEF' in treeVar or '_lepton' in treeVar:
                        drawoption = '(sign(genWeight))*(%s)*(%s)' % (weightF,treeCut+' && '+treeVar+' > 0')
                        '''    
                        elif 'minCSV' in treeVar:
                        if 'Zudsg' in job.name or 'Zcc' in job.name: 
                        xMin = 0.0
                            xMax = 0.55
                        if 'Z1b' in job.name or 'Z2b' in job.name or 'ttbar' in job.name:
                            xMin = 0.4
                            xMax = 1.0
                            drawoption = '(sign(genWeight))*(%s)*(%s)' % (weightF,treeCut)
                            '''        
                    else: 
                        #drawoption = '(sign(genWeight))*(%s)*(%s)*(%s)' % (weightF,treeCut,xSec)
                        drawoption = '(sign(genWeight))*(%s)*(%s)' % (weightF,treeCut)
                        
                    print 'Draw Option:',drawoption

                    #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), drawoption, "goff,e")
                    #TD = ROOT.treedraw()
                    #hTree = TD.TreeDraw(CuttedTree, hTree, '%s>>%s' %(treeVar,job.name), drawoption)
                    CuttedTree.Draw('%s>>%s' %(treeVar,job.name), drawoption, "goff,e")
                    
                    full = True

                else:
                    full=False

            elif job.type == 'DATA':

                print '\n----> Job Type: Data...'
                print '            Name: ', job.name
                
                print '\n---->Drawing Tree for variable: ',treeVar
                print '  with Cuts: ', treeCut
                
   
                if 'gg_plus' in treeVar or 'VV' in treeVar:
                    
                    if options['blind']:
                        
                        print '\n\n====== BLINDED ======'
                        print treeCut
                   
                        #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                        CuttedTree.Draw('%s>>%s' %(treeVar,job.name),'%s' %treeCut, "goff,e")
                    else:
                        #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                        CuttedTree.Draw('%s>>%s' %(treeVar,job.name),'%s' %treeCut, "goff,e")
                        
                elif '_corr' in treeVar:
                    print 'VAR:',treeVar
                    if '[0]' in treeVar:
                        new_treeVar = 'Jet_pt[hJCidx[0]]/Jet_rawPt[hJCidx[0]]'
                    if '[1]' in treeVar:
                        new_treeVar = 'Jet_pt[hJCidx[1]]/Jet_rawPt[hJCidx[1]]'
                    #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(new_treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                    CuttedTree.Draw('%s>>%s' %(treeVar,job.name),'%s' %treeCut, "goff,e")

                elif 'vtx' in treeVar or 'EmEF' in treeVar or '_lepton' in treeVar:
                    #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut+' && '+treeVar+' > 0', "goff,e")
                    CuttedTree.Draw('%s>>%s' %(treeVar,job.name),'%s' %treeCut+' && '+treeVar+' > 0', "goff,e")
                    
                #else:
                #    if options['blind']:
                #        print '!!!!BLINDING!!!'
                #        CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s & V_pt < 50.' %treeCut, "goff,e")

                elif 'LHE' in treeVar or 'HT' in treeVar or 'lhe' in treeVar:
                    #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %('Jet_pt[hJCidx[1]]',job.name,nBins,xMin,xMax), '%s' %treeCut+' && Jet_pt[hJCidx[1]] < 0.0', "goff,e")
                    CuttedTree.Draw('%s>>%s' %(treeVar,job.name),'%s' %treeCut+' && Jet_pt[hJCidx[1]] < 0.0', "goff,e")
                    
                else:
                    print '!!!!NOT BLINDING!!!'
                    #CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                    CuttedTree.Draw('%s>>%s' %(treeVar,job.name),'%s' %treeCut, "goff,e")
                    

                print CuttedTree
                
                '''
                hReg_metric = hReg.GetRMS()/hReg.GetMean()
                hNom_metric = hNom.GetRMS()/hNom.GetMean()
                percent_improvement = (1-(hReg_metric/hNom_metric))*100
                hReg_std = str(round(hReg.GetRMS(),3))
                hReg_mu  = str(round(hReg.GetMean(),3))
                hNom_std = str(round(hNom.GetRMS(),3))
                hNom_mu  = str(round(hNom.GetMean(),3))
                '''
 
                full = True

            # if full:
            #     hTree = ROOT.gDirectory.Get(job.name)
            #     print '\nJob name: ',job.name
            #     print 'hTree: ', hTree
                
            #     # Get Stats
            #     #hTree.GetRMS()
            #     #hTree.GetMean()
            #     #print '\t Mean: ', hTree.GetMean()
            #     #print '\t RMS : ', hTree.GetRMS()
                

            # else:
            #     hTree = ROOT.TH1F('%s'%name,'%s'%name,nBins,xMin,xMax)
            #     hTree.Sumw2()
                
            # NOW scale the histograms    
            if job.type != 'DATA':

                if 'gg_plus' in treeVar or 'VV' in treeVar:
                    if TrainFlag:
                        MC_rescale_factor=2.
                        print 'I RESCALE BY 2.0'
                    else: 
                        MC_rescale_factor = 1.
    
                    ScaleFactor = self.tc.get_scale(job, self.config)*MC_rescale_factor

                    # for LHE scale shapes we need a different norm
                    if 'LHE_weights_scale_wgt[0]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 0)*MC_rescale_factor
                    elif 'LHE_weights_scale_wgt[1]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 1)*MC_rescale_factor
                    elif 'LHE_weights_scale_wgt[2]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 2)*MC_rescale_factor
                    elif 'LHE_weights_scale_wgt[3]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 3)*MC_rescale_factor
                    
                    print '\n-----> Histogram Scale Factor: ', ScaleFactor
                else: 
                    ScaleFactor = self.tc.get_scale(job, self.config)
                    
                    # for LHE scale shapes we need a different norm
                    if 'LHE_weights_scale_wgt[0]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 0)
                    elif 'LHE_weights_scale_wgt[1]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 1)
                    elif 'LHE_weights_scale_wgt[2]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 2)
                    elif 'LHE_weights_scale_wgt[3]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 3)
                    
                    print '\n-----> Histogram Scale Factor: ', ScaleFactor
                
                if ScaleFactor != 0:
                    hTree.Scale(ScaleFactor)

     
            #print '\t-->import %s\t Integral: %s'%(job.name,hTree.Integral())
            if addOverFlow:
            	uFlow = hTree.GetBinContent(0)+hTree.GetBinContent(1)
            	oFlow = hTree.GetBinContent(hTree.GetNbinsX()+1)+hTree.GetBinContent(hTree.GetNbinsX())
            	uFlowErr = ROOT.TMath.Sqrt(ROOT.TMath.Power(hTree.GetBinError(0),2)+ROOT.TMath.Power(hTree.GetBinError(1),2))
            	oFlowErr = ROOT.TMath.Sqrt(ROOT.TMath.Power(hTree.GetBinError(hTree.GetNbinsX()),2)+ROOT.TMath.Power(hTree.GetBinError(hTree.GetNbinsX()+1),2))
            	hTree.SetBinContent(1,uFlow)
            	hTree.SetBinContent(hTree.GetNbinsX(),oFlow)
            	hTree.SetBinError(1,uFlowErr)
            	hTree.SetBinError(hTree.GetNbinsX(),oFlowErr)

            hTree.SetDirectory(0)
            gDict = {}

            if self._rebin:
                gDict[group] = self.mybinning.rebin(hTree)
                del hTree
            else: 
                #print 'not rebinning %s'%job.name 
                gDict[group] = hTree

            hTreeList.append(gDict)

        CuttedTree.IsA().Destructor(CuttedTree)
        del CuttedTree
        return hTreeList


       
    @property
    def rebin(self):
        return self._rebin

    @property
    def rebin(self, value):
        if self._rebin and value:
            return True
        elif self._rebin and not value:
            self.nBins = self.norebin_nBins
            self._rebin = False
        elif not self._rebin and value:
            if self.mybinning is None:
                raise Exception('define rebinning first')
            else:
                self.nBins = self.rebin_nBins
                self._rebin = True
                return True
        elif not self._rebin and not self.value:
            return False

    def calc_rebin(self, bg_list, nBins_start=1000, tolerance=0.35):
        self.calc_rebin_flag = True
        self.norebin_nBins = copy(self.nBins)
        self.rebin_nBins = nBins_start
        self.nBins = nBins_start
        i=0

        #add all together:
        print '\n\t...calculating rebinning on list:', bg_list
        
        for job in bg_list:

            #print 'Rebinner BKG_sample:', job.name

            htree = self.get_histos_from_tree(job)[0].values()[0]
            #print 'Rebinner htree:', htree
            
            if not i:
                totalBG = copy(htree)
            else:
                totalBG.Add(htree,1)
            del htree
            i+=1

        ErrorR=0
        ErrorL=0
        TotR=0
        TotL=0
        binR=self.rebin_nBins
        binL=1
        rel=1.0

        #---- from right
        while rel > tolerance:
            TotR+=totalBG.GetBinContent(binR)
            ErrorR=sqrt(ErrorR**2+totalBG.GetBinError(binR)**2)
            binR-=1
            if binR < 0: break
            if TotR < 1.: continue
            if not TotR <= 0 and not ErrorR == 0:
                rel=ErrorR/TotR
                #print rel
        print 'upper bin is %s'%binR
        print 'BDT value at bin is ', totalBG.GetBinCenter(binR)
        
        #---- from left
        rel=1.0
        while rel > tolerance:
            TotL+=totalBG.GetBinContent(binL)
            ErrorL=sqrt(ErrorL**2+totalBG.GetBinError(binL)**2)
            binL+=1
            if binL > nBins_start: break
            if TotL < 1.: continue
            if not TotL <= 0 and not ErrorL == 0:
                rel=ErrorL/TotL
                #print rel
        #it's the lower edge
        binL+=1
        print 'lower bin is %s'%binL
        print 'BDT value at bin is ', totalBG.GetBinCenter(binL)
        
        inbetween=binR-binL
        stepsize=int(inbetween)/(int(self.norebin_nBins)-2)
        modulo = int(inbetween)%(int(self.norebin_nBins)-2)

        print 'stepsize %s'% stepsize
        print 'modulo %s'%modulo
        binlist=[binL]
        for i in range(0,int(self.norebin_nBins)-3):
            binlist.append(binlist[-1]+stepsize)
        binlist[-1]+=modulo
        binlist.append(binR)
        binlist.append(self.rebin_nBins+1)
        
        print 'binning set to %s'%binlist
        print 'binlist BDT values:', array('d',[-1.0]+[totalBG.GetBinCenter(i) for i in binlist])
                
        print 'bin low edge array:', array('d',[self.xMin]+[totalBG.GetBinLowEdge(i) for i in binlist])
        #print array('d',[-1.0]+[totalBG.GetBinLowEdge(i) for i in binlist])
        
        #self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[-1.0]+[totalBG.GetBinLowEdge(i) for i in binlist]),True)
        #self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[self.xMin]+[totalBG.GetBinLowEdge(i) for i in binlist]),True)
        self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[self.xMin]+[totalBG.GetBinLowEdge(i) for i in binlist]),True,self.Custom_BDT_bins)

        self._rebin = True
        print '\t > rebinning is set <\n'

    # def calc_rebin(self, bg_list, nBins_start=1000, tolerance=0.35):
    #     #print "START calc_rebin"
    #     self.calc_rebin_flag = True
    #     self.norebin_nBins = copy(self.nBins)
    #     self.rebin_nBins = nBins_start
    #     self.nBins = nBins_start
    #     i=0
    #     #add all together:
    #     print '\n\t...calculating rebinning...'
    #     for job in bg_list:
    #         #print "job",job
    #         htree = self.get_histos_from_tree(job)[0].values()[0]
    #         #print "Integral",job,htree.Integral()
    #         if not i:
    #             totalBG = copy(htree)
    #         else:
    #             totalBG.Add(htree,1)
    #         del htree
    #         i+=1
    #     ErrorR=0
    #     ErrorL=0
    #     TotR=0
    #     TotL=0
    #     binR=self.rebin_nBins
    #     binL=1
    #     rel=1.0
    #     #print "START loop from right"
    #     #print "totalBG.Draw("","")",totalBG.Integral()
    #     #---- from right
    #     while rel > tolerance :
    #         TotR+=totalBG.GetBinContent(binR)
    #         ErrorR=sqrt(ErrorR**2+totalBG.GetBinError(binR)**2)
    #         binR-=1
    #         if binR < 0: break
    #         if TotR < 1.: continue
    #         #print 'binR is', binR
    #         #print 'TotR is', TotR
    #         #print 'ErrorR is', ErrorR
    #         if not TotR <= 0 and not ErrorR == 0:
    #             rel=ErrorR/TotR
    #             #print 'rel is',  rel
    #     #print 'upper bin is %s'%binR
    #     #print "END loop from right"

    #     #Custom bins will be applied if this is true. Rebinning from left is not needed (big lower bin should have enough stats).
    #     if self.Custom_BDT_bins:
    #         if self.Custom_BDT_bins[-2] > totalBG.GetBinLowEdge(binR):
    #             print '@ERROR: highest BDT bins doesn\'t satifie rebinning condition when using variable size bins, please change the bin size accordinly.Aborting'
    #             print 'binR x-range should be', totalBG.GetBinLowEdge(binR)
    #             sys.exit()
    #         self.mybinning = Rebinner(len(self.Custom_BDT_bins)-1,array('d',self.Custom_BDT_bins),True, True)
    #     else:
    #         #---- from left
    #         rel=1.0
    #         print "START loop from left"
    #         while rel > tolerance:
    #             TotL+=totalBG.GetBinContent(binL)
    #             ErrorL=sqrt(ErrorL**2+totalBG.GetBinError(binL)**2)
    #             binL+=1
    #             if binL > nBins_start: break
    #             if TotL < 1.: continue
    #             if not TotL <= 0 and not ErrorL == 0:
    #                 rel=ErrorL/TotL
    #                 print rel
    #         #it's the lower edge
    #         print "STOP loop from left"
    #         binL+=1
    #         print 'lower bin is %s'%binL

    #         inbetween=binR-binL
    #         stepsize=int(inbetween)/(int(self.norebin_nBins)-2)
    #         modulo = int(inbetween)%(int(self.norebin_nBins)-2)

    #         print 'stepsize %s'% stepsize
    #         print 'modulo %s'%modulo
    #         binlist=[binL]
    #         for i in range(0,int(self.norebin_nBins)-3):
    #             binlist.append(binlist[-1]+stepsize)
    #         binlist[-1]+=modulo
    #         binlist.append(binR)
    #         binlist.append(self.rebin_nBins+1)
    #         print 'binning set to %s'%binlist
    #         #print "START REBINNER"
    #         #self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[-1.0]+[totalBG.GetBinLowEdge(i) for i in binlist]),True)
    #         self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[self.xMin]+[totalBG.GetBinLowEdge(i) for i in binlist]),True)
    #     self._rebin = True
    #     print '\t > rebinning is set <\n'

    @staticmethod
    def orderandadd(histo_dicts,setup):
        ordered_histo_dict = {}
        for sample in setup:
            nSample = 0
            for histo_dict in histo_dicts:
                if histo_dict.has_key(sample):
                    if nSample == 0:
                        ordered_histo_dict[sample] = histo_dict[sample].Clone()
                    else:
                        #printc('magenta','','\t--> added %s to %s'%(sample,sample))
                        ordered_histo_dict[sample].Add(histo_dict[sample])
                    nSample += 1
        del histo_dicts
        return ordered_histo_dict 

    



class Rebinner:

    #def __init__(self,nBins,lowedgearray,active=True):
    def __init__(self,nBins,lowedgearray,active=True,var_bins=False):
        self.lowedgearray=lowedgearray
        self.nBins=nBins
        self.active=active
        self.var_bins=var_bins

    def rebin(self, histo):
        if not self.active: return histo
        #print histo.Integral()
        print '!!!!! Rebinning FInal Step !!!!!'
        print 'Xmin(low edge):', self.lowedgearray[0]
        print 'Xmax(high edge):', self.lowedgearray[-1]
        ROOT.gDirectory.Delete('hnew')
        histo.Rebin(self.nBins,'hnew',self.lowedgearray)
        binhisto=ROOT.gDirectory.Get('hnew')
        
        newhisto=ROOT.TH1F('new','new',self.nBins,self.lowedgearray[0],self.lowedgearray[-1])
        newhisto.Sumw2()
        for bin in range(1,self.nBins+1):
            #print 'Bin # ',bin, 'low edge:', binhisto.GetBinLowEdge(bin), binhisto.GetBinContent(bin)
            newhisto.SetBinContent(bin,binhisto.GetBinContent(bin))
            newhisto.SetBinError(bin,binhisto.GetBinError(bin))
        newhisto.SetName(binhisto.GetName())
        newhisto.SetTitle(binhisto.GetTitle())
        
        if self.var_bins:
            print '\n\t Making variable bin histogram...'
            print 'LowEdgeArray:', self.lowedgearray
            print 'Merging from -1 to 0'
            merge_low, merge_high = -1.0, 0.0
            var_lowedgearray = array('d',[x for x in self.lowedgearray if not(merge_low < x < merge_high)])
            print '\tVar_lowedgearray:', var_lowedgearray
            
            ROOT.gDirectory.Delete('hnew2')
            histo.Rebin(len(var_lowedgearray)-1, "hnew2", var_lowedgearray)
            Varbinhisto=ROOT.gDirectory.Get('hnew2')
            newhisto2=ROOT.TH1F('new2','new2', len(var_lowedgearray)-1, var_lowedgearray)
            newhisto2.Sumw2()
            for bin in range(1,len(var_lowedgearray)):
                print 'bin #',bin,'Low edge:', Varbinhisto.GetBinLowEdge(bin), Varbinhisto.GetBinContent(bin)
                newhisto2.SetBinContent(bin, Varbinhisto.GetBinContent(bin))
                newhisto2.SetBinError(bin, Varbinhisto.GetBinError(bin))
            newhisto2.SetName(binhisto.GetName())
            newhisto2.SetTitle(binhisto.GetTitle())
            
            del histo
            del binhisto
            del newhisto
            del Varbinhisto
            return copy(newhisto2)

        else:
            del histo
            del binhisto
            return copy(newhisto)

