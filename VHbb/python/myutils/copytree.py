import ROOT 
from printcolor import printc
import time

        
def copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,Acut):

    start = time.time()

    print "##### COPY TREE - BEGIN ######"
    print "Input File : %s/%s%s.root " %(pathIN,prefix,file)
    print "Output File : %s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file)
    
    
    #input = ROOT.TFile.Open("%s/%s%s.root" %(pathIN,prefix,file),'read')
    input = ROOT.TFile.Open("%s/%s%s%s.root" %(pathIN,newprefix,Aprefix,file),'read')
    output = ROOT.TFile.Open("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'recreate')
    
    
    input.cd()

    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        #print obj.GetName()
        if obj.GetName() == 'tree':
            continue
        output.cd()
        #print key.GetName()
        obj.Write(key.GetName())
        
    inputTree = input.Get("tree")
    nEntries = inputTree.GetEntries()

    # Turn of branches we do not need
    inputTree = branch_reduce(inputTree)

    output.cd()
    print '\n\t copy file: %s with cut: %s' %(file,Acut)
    outputTree = inputTree.CopyTree(Acut)
    kEntries = outputTree.GetEntries()
    printc('blue','',"\t before cuts\t %s" %nEntries)
    printc('green','',"\t survived\t %s" %kEntries)
    outputTree.AutoSave()
    output.ls()
    print "Writing output file"
    output.Write()
    print "Closing output file"
    output.Close()
    print "Closing input file"
    input.Close()

    print "##### COPY TREE - END ######"
    
    end = time.time()
    
    print '\n-----> Total Prep Time: ', end - start



def branch_reduce(tree):

    print '\n     ----> Reducing Branches...'

    tree.SetBranchStatus('gg_plus*', 0)

    tree.SetBranchStatus('Flag*', 0)

    #tree.SetBranchStatus('HLT*', 0)

    tree.SetBranchStatus('bTagWeightCSV*', 0)

    tree.SetBranchStatus('met_shifted*', 0)

    tree.SetBranchStatus('H3cj*', 0)

    tree.SetBranchStatus('ungroomed*', 0)

    #tree.SetBranchStatus('GenLep*', 0)

    #tree.SetBranchStatus('GenVbosons*', 0)

    #tree.SetBranchStatus('GenTop*', 0)

    #tree.SetBranchStatus('aLeptons*', 0)

    tree.SetBranchStatus('GenNu*', 0)

    #tree.SetBranchStatus('selLeptons*', 0)

    tree.SetBranchStatus('TauGood*', 0)

    #tree.SetBranchStatus('GenHad*', 0)

    tree.SetBranchStatus('GenGluon*', 0)

    tree.SetBranchStatus('htt*', 0)

    #tree.SetBranchStatus('GenWZ*', 0)

    tree.SetBranchStatus('GenBQuarkFromHafter*', 0)

    tree.SetBranchStatus('trimmedFat*', 0)

    #tree.SetBranchStatus('GenBQuarkFromTop*', 0)
    
    tree.SetBranchStatus('Fat*', 0)
    
    tree.SetBranchStatus('nFat*', 0)
    
    tree.SetBranchStatus('ntrg*', 0)

    tree.SetBranchStatus('Subjet*', 0)
    
    tree.SetBranchStatus('Discarded*', 0)

    tree.SetBranchStatus('l1*', 0)
    

    return tree
