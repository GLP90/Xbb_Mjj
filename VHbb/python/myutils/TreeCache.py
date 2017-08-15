from __future__ import print_function
import os,sys,subprocess,hashlib
import ROOT
from samplesclass import Sample
from multiprocessing import Pool
import fileinput


class TreeCache:
    def __init__(self, cutList, sampleList, path, config):
        ROOT.gROOT.SetBatch(True)
        self.path = path
        self._cutList = []
        for cut in cutList:
            self._cutList.append('(%s)'%cut.replace(' ',''))
        try:
            self.__tmpPath = os.environ["TMPDIR"]
        except KeyError:
            #print("\x1b[32;5m %s \x1b[0m" %open('%s/data/vhbb.txt' %config.get('Directories','vhbbpath')).read())
            print("\x1b[31;5;1m\n\t>>> %s: Please set your TMPDIR and try again... <<<\n\x1b[0m" %os.getlogin())
            #sys.exit(-1)

        VHbbNameSpace=config.get('VHbbNameSpace','library')
        ROOT.gSystem.Load(VHbbNameSpace)
        
        self.__doCache = True
        if config.has_option('Directories','tmpSamples'):
            self.__tmpPath = config.get('Directories','tmpSamples')
        self.__hashDict = {}
        self.minCut = None
        self.__find_min_cut()
        self.__sampleList = sampleList
        
        print('\n\t>>> Caching FILES <<<\n')
        
        self.__cache_samples(config)

                
    def __find_min_cut(self):
        effective_cuts = []
        for cut in self._cutList:
            if not cut in effective_cuts:
                effective_cuts.append(cut)
        self._cutList = effective_cuts
        self.minCut = '||'.join(self._cutList)

    def __trim_tree(self, sample, config):

        theName = sample.name
        sample_name = sample.get_path.replace('./', '')

        print ('Reading sample <<<< %s' %sample)
        print ('----> From Directory: ', self.path)
        print ('----> File: ', sample_name)
                
        source = '%s/%s' %(self.path, sample_name)
        checksum = self.get_checksum(source)
        theHash = hashlib.sha224('%s_s%s_%s' %(sample,checksum,self.minCut)).hexdigest()
        self.__hashDict[theName] = theHash
        tmpSource = '%s/tmp_%s.root'%(self.__tmpPath,theHash)

        print ('temp File:', tmpSource)

        #make temp file for checks
        if os.path.isfile('temp_file.txt'):
            os.system('rm temp_file.txt')

        if 'eoscms' in tmpSource:
            eosPath = tmpSource.replace('root://eoscms//eos/cms', '')
            print ('eosPath:', eosPath)
            os.system("eos ls "+eosPath+" >> temp_file.txt")
            for line in fileinput.input("temp_file.txt", inplace=True):
                tFile = line.replace('\n', '')
            print ('file line:',tFile)
            fileName = eosPath.replace('/store/user/dcurry/heppy//files/tmp//','')
            print ('file name:',fileName)

            if tFile == fileName:
                print ('----> Temp File: ', tmpSource)
                return

        elif self.__doCache and self.file_exists(tmpSource):
            print ('----> Temp File: ', tmpSource)
            return

        output = ROOT.TFile.Open(tmpSource,'create')
        input = ROOT.TFile.Open(source,'read')

        print ('tmpsrc:', tmpSource)
        print ('Input:', input)  
        print ('Output:', output)

        output.cd()
        tree = input.Get(sample.tree)

        print ('Input Tree:', tree)

        try:
            CountWithPU = input.Get("CountWithPU")
            CountWithPU2011B = input.Get("CountWithPU2011B")
            sample.count_with_PU = CountWithPU.GetBinContent(1) 
            sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1)
        except:
            print('WARNING: No Count with PU histograms available. Using 1.')
            sample.count_with_PU = 1.
            CountWithPU = input.Get("Count")
            sample.count_with_PU = CountWithPU.GetBinContent(1)
            sample.count_with_PU2011B = 1.

        input.cd()
        obj = ROOT.TObject
        print ('Input Tree Object:', obj)
        
        for key in ROOT.gDirectory.GetListOfKeys():
            input.cd()
            obj = key.ReadObj()
            if obj.GetName() == 'tree':
                continue
            output.cd()
            obj.Write(key.GetName())
        output.cd()

        theCut = self.minCut
        #ROOT.TFormula.SetMaxima(1000,1000,1000)

        if sample.subsample:
            theCut += '&(%s)' %(sample.subcut)
            
        #print ('Tree Cut:', theCut)

        cuttedTree = tree.CopyTree(theCut)
        #print ('Cutted Tree:', theCut)

        cuttedTree.Write()
        output.Write()
        input.Close()
        del input
        output.Close()
        #tmpSourceFile = ROOT.TFile.Open(tmpSource,'read')
        #if tmpSourceFile.IsZombie():
        #    print("@ERROR: Zombie file")
        del output



    def __cache_samples(self,config):
        
        for job in self.__sampleList:
            self.__trim_tree(job, config)
            

    

    def get_tree(self, sample, cut):
        
        input = ROOT.TFile('%stmp_%s.root'%(self.__tmpPath,self.__hashDict[sample.name]),'read')
        tree = input.Get(sample.tree)
        
        print ('sample:', sample.name)
        print ('input file:', input)
        print ('tree:', tree)
        
        try:
            CountWithPU = input.Get("CountWithPU")
            CountWithPU2011B = input.Get("CountWithPU2011B")
            sample.count_with_PU = CountWithPU.GetBinContent(1) 
            sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1) 
        except:
            print('WARNING: No Count with PU histograms available. Using 1.')
            sample.count_with_PU = 1.
            CountWithPU = input.Get("Count")
            sample.count_with_PU = CountWithPU.GetBinContent(1)            
            sample.count_with_PU2011B = 1.

        if sample.subsample:
            cut += '& (%s)' %(sample.subcut)
        
        ROOT.gROOT.cd()
        
        #print ('Tree Cut:', cut)
        
        cuttedTree=tree.CopyTree(cut)
        
        cuttedTree.SetDirectory(0)
        
        input.Close()
        del input
        del tree
        return cuttedTree

    #@staticmethod
    def get_scale(self, sample, config, lumi = None):

        print ('----> Getting Sample Scale...')

        # get the weights from the file,. not the tree
        input = ROOT.TFile('%stmp_%s.root'%(self.__tmpPath,self.__hashDict[sample.name]),'read')
        posWeight = input.Get('CountPosWeight')
        negWeight = input.Get('CountNegWeight')
        #print ('posWeight:',posWeight)
        
        anaTag=config.get('Analysis','tag')
        
        theScale = 1.
        
        lumi = float(sample.lumi)
        print ('sample:', sample)
        print ('xsec:', sample.xsec)
        print ('lumi:', sample.lumi)
        print ('SF:', sample.sf)
        print ('posWeight:', posWeight.GetBinContent(1))
        print ('negWeight:', negWeight.GetBinContent(1))
        theScale = lumi*sample.xsec/(posWeight.GetBinContent(1)-negWeight.GetBinContent(1))
        
        return theScale

    def get_scale_BDT(self, sample, config, lumi = None):

        print ('----> Getting Sample Scale...')

        # get the weights from the file,. not the tree
        input = ROOT.TFile('%stmp_%s.root'%(self.__tmpPath,self.__hashDict[sample.name]),'read')
        posWeight = input.Get('CountPosWeight')
        negWeight = input.Get('CountNegWeight')
        #print ('posWeight:',posWeight)
        
        anaTag=config.get('Analysis','tag')
        
        theScale = 1.
        
        lumi = float(sample.lumi)
        print ('sample:', sample)
        print ('xsec:', sample.xsec)
        print ('lumi:', sample.lumi)
        print ('SF:', sample.sf)
        print ('posWeight:', posWeight.GetBinContent(1))
        print ('negWeight:', negWeight.GetBinContent(1))
        print ('Special Weight:', sample.specialweight)
        theScale = float(sample.specialweight)*lumi*sample.xsec/(posWeight.GetBinContent(1)-negWeight.GetBinContent(1))
        
        return theScale



    #@staticmethod
    def get_scale_LHEscale(self, sample, config, lhe_scale, lumi = None):

        print ('----> Getting Sample Scale...')

        # get the weights from the file,. not the tree
        input = ROOT.TFile('%stmp_%s.root'%(self.__tmpPath,self.__hashDict[sample.name]),'read')
        posWeight = input.Get('CountPosWeight')
        negWeight = input.Get('CountNegWeight')
        Weight = input.Get('CountWeighted')
        lumi = float(sample.lumi)
        
        # for LHE weights
        countWeightedLHEWeightScale = input.Get('CountWeightedLHEWeightScale')

        #print ('\nLHE Index:', lhe_scale)
        #print (countWeightedLHEWeightScale)        
        #print (countWeightedLHEWeightScale.GetBinContent(2))
        
        anaTag=config.get('Analysis','tag')

        scaled_count = 0.
        
        if lhe_scale == 0:
            scaled_count = countWeightedLHEWeightScale.GetBinContent(0+1)
        elif lhe_scale == 1:
            scaled_count = countWeightedLHEWeightScale.GetBinContent(1+1)
        elif lhe_scale == 2:
            scaled_count = countWeightedLHEWeightScale.GetBinContent(2+1)
        elif lhe_scale == 3:
            scaled_count = countWeightedLHEWeightScale.GetBinContent(3+1)

        count = (posWeight.GetBinContent(1) - negWeight.GetBinContent(1))
        countWeightNoPU = (posWeight.GetBinContent(1) + negWeight.GetBinContent(1))
        countWeightPU = Weight.GetBinContent(1)

        #if scaled_count > 0:
        #    countWeightNoPU = (posWeight.GetBinContent(1) + negWeight.GetBinContent(1))
        #    countWeightPU = Weight.GetBinContent(1)
        #    return lumi*sample.xsec*sample.sf/(scaled_count*(countWeightNoPU/countWeightPU))
        #else:
        #    return lumi*sample.xsec*sample.sf/count
        
        if scaled_count == 0:
            return 0.
        else:
            return (countWeightNoPU/count)*lumi*sample.xsec*sample.sf/(scaled_count*(countWeightNoPU/countWeightPU))



    @staticmethod
    def get_checksum(file):
        if 'gsidcap://t3se01.psi.ch:22128' in file:
            srmPath = 'srm://t3se01.psi.ch:8443/srm/managerv2?SFN='
            command = 'lcg-ls -b -D srmv2 -l %s' %file.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
            lines = p.stdout.readlines()
            if any('No such' in line for line in lines):
                print('File not found')
                print(command)
            line = lines[1].replace('\t* Checksum: ','')
            checksum = line.replace(' (adler32)\n','')
        else:
            command = 'md5sumi %s' %file
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
            lines = p.stdout.readlines()
            checksum = lines[0]
        return checksum
    
    @staticmethod
    def file_exists(file):
        if 'gsidcap://t3se01.psi.ch:22128' in file:
            srmPath = 'srm://t3se01.psi.ch:8443/srm/managerv2?SFN='
            command = 'lcg-ls %s' %file.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
            line = p.stdout.readline()
            return not 'No such file or directory' in line
        else:
            return os.path.exists(file)
