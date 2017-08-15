#!/usr/bin/env python

import sys,hashlib,ROOT
ROOT.gROOT.SetBatch(True)
from array import array
from optparse import OptionParser

def getTotal( bin, fileList ):
    total = 0.
    for i in range(0,len(fileList)):
        total = total + fileList[i][2][bin]
    return total


argv = sys.argv
parser = OptionParser()

parser.add_option("-C", "--config", dest="config", default=[], action="append",
                              help="configuration defining bins")
parser.add_option("-A", "--apply", dest="apply", default=True, action="store_true",
                              help="configuration defining the")
parser.add_option("-W", "--weight", dest="weights", default=True, action="store_false",
                              help="Calculate the weights")
parser.add_option("-V", "--validate", dest="validate", default=False, action="store_false",
                              help="Make validation plot the weights")
(opts, args) = parser.parse_args(argv)
if opts.config =="":
    opts.config = "config"

from myutils import BetterConfigParser

print opts.config
config = BetterConfigParser()
config.read(opts.config)
prefix = config.get('lheWeights','prefix')
newpostfix = config.get('lheWeights','newpostfix')
inclusive = config.get('lheWeights','inclusive')
files = eval(config.get('lheWeights','fileList'))
lheBin = eval(config.get('lheWeights','lheBin'))

print '\n========= Looping over Drell Yan Samples ==========\n'

fileList = []
for file in files:
    new_entry = [prefix+file+'.root',files[file],[]]
    print new_entry
    if file == inclusive:
        fileList.insert(0, new_entry)
    else:
        fileList.append(new_entry)

#print fileList
#print lheBin

def get_weights(fileList,lheBin):    

    print '\n-----> Getting Weights...'

    for file in fileList:

        infile = ROOT.TFile.Open(file[0],"READ")
        tree = infile.Get('tree')
        
        print '\n-----> accessing file: ', infile
        #print '                 tree: ', tree

        for bin in lheBin:
            file[2].append( float(tree.GetEntries(bin)) )

        #try:
        #    count = infile.Get('CountWithPU')
        #except:
        #    print('WARNING: No Count with PU histograms available. Using Count.')
        count = infile.Get("Count")
        
        file.append( count.GetBinContent(1) )

        infile.Close()

        del tree
    
    CountIncl = fileList[0][3]
    xSecIncl = fileList[0][1]

    #print fileList
    #print 'Inclusive cross-section %.2f pb' %xSecIncl

    #total -> total numer of events in each lheBin
    total = []
    weight= []
    for bin in range(0, len(lheBin) ):
        
        total.append(getTotal(bin, fileList))

        #to better stich we need the highest stat (that should correspond to the binned sample relative to the bin)
        fileList.sort( key=lambda file: file[2][bin], reverse=True )

        if total[bin] > 0.:
            #the first is always the one with the highest N in the bin: 
            weight.append( (fileList[0][1]/fileList[0][3]) * (CountIncl/xSecIncl) * fileList[0][2][bin]/total[bin] )
        else:
            weight.append(1.)

    weight_map = {}
    for bin in range(0, len(lheBin) ):
        print '%s: %.2f' %(lheBin[bin], weight[bin])
        weight_map[lheBin[bin]] = weight[bin]
    return weight_map


def apply_weights(fileList,weight_map,inclusive,newpostfix):    

    print '\n-----> Applying Weights...'

    #now add the branch with the weight normalized to the inclusive
    for file in fileList:

        outfile = ROOT.TFile.Open(file[0].replace('.root',newpostfix),'RECREATE')
        print 'outfile:', outfile
        infile = ROOT.TFile.Open(file[0],"READ")

        histoInfile = ROOT.TFile.Open(inclusive+'.root',"READ")
        histoInfile.cd()
        obj = ROOT.TObject
        for key in ROOT.gDirectory.GetListOfKeys():
            histoInfile.cd()
            obj = key.ReadObj()
            #print obj.GetName()
            if obj.GetName() == 'tree':
                continue
            outfile.cd()
            #print key.GetName()
            obj.Write(key.GetName())
            
        infile.cd()
        tree = infile.Get('tree')
        outfile.cd()
        newtree = tree.CloneTree(0)
        lheWeight = array('f',[0])
        newtree.Branch('lheWeight',lheWeight,'lheWeight/F')
        
        nEntries = tree.GetEntries()
        theBinForms = {}
        for bin in weight_map:
            theBinForms[bin] = ROOT.TTreeFormula("Bin_formula_%s"%(bin),bin,tree)
        for entry in range(0,nEntries):
            tree.GetEntry(entry)
            match_bin = None
            for bin in weight_map:
                if theBinForms[bin].EvalInstance() > 0.:
                    match_bin = bin
            if match_bin:
                lheWeight[0] = weight_map[match_bin]
            else:
                lheWeight[0] = 1.
            newtree.Fill()
                   
        newtree.AutoSave()
        outfile.Write()
        outfile.Close()
        infile.Close()
        del tree
        del newtree
        
def do_validation(fileList,inclusive,newpostfix):
    histo = ROOT.TH1F("lheV_pt","lheV_pt",300,0,300)
    histo1 = ROOT.TH1F("lheV_ptInc","lheV_ptInc",300,0,300)
    histo.SetDirectory(0)
    histo1.SetDirectory(0)

    for file in fileList: 

        h_name=str(hashlib.sha224(file[0]).hexdigest())
        #print file[0]
        #print h_name

        tfile = ROOT.TFile.Open(file[0].replace('.root',newpostfix),"read")
        tree = tfile.Get("tree")
        h_tmp = ROOT.TH1F(h_name,h_name,300,0,300)
        #ROOT.gDirectory.ls()
        tree.Draw("lheV_pt>>"+str(h_name),"(lheWeight)*(lheV_pt < 300.)","goff")
        if inclusive in file[0]:
            h_tmp1 = ROOT.TH1F(h_name+'Inc',h_name+'Inc',300,0,300)
            tree.Draw("lheV_pt>>"+str(h_name+'Inc'),"(lheV_pt < 300.)","goff")
            histo1.Add(h_tmp1)
        histo.Add(h_tmp)
        tfile.Close()
        del tree


    canvas = ROOT.TCanvas("lheV_pt","lheV_pt",600,600)
    ROOT.gPad.SetLogy()
    histo.Draw()
    histo1.Draw('SAME')

    #print histo.Integral(100,300)
    #print histo1.Integral(100,300)

    histo1.SetLineColor(ROOT.kRed)

    canvas.Print("validation_lheV_pt.pdf","pdf")

if opts.weights:
    weight_map = get_weights(fileList,lheBin)
    config.set('lheWeights', 'weights_per_bin', '%s' %weight_map)
    f = open('13TeVconfig/lheWeights', 'w')
    for section in config.sections():
        if not section == 'lheWeights':
            config.remove_section(section)
    config.write(f)
    f.close()

elif opts.apply:
    weight_map = eval(config.get('lheWeights', 'weights_per_bin'))

if opts.apply:
    apply_weights(fileList,weight_map,prefix+inclusive,newpostfix)

if opts.validate:
    do_validation(fileList,inclusive,newpostfix)
