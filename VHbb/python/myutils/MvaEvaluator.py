
import ROOT
from array import array
from mvainfos import mvainfo

class MvaEvaluator:
    def __init__(self, config, MVAinfo):

        self.varset = MVAinfo.varset

        #Define reader
        self.reader = ROOT.TMVA.Reader("!Color:!Silent")
        MVAdir=config.get('Directories','vhbbpath')
        self.systematics=config.get('systematics','systematics').split(' ')
        self.MVA_Vars={}
        self.MVAname = MVAinfo.MVAname

        print '\n Systematics:', self.systematics

        for systematic in self.systematics:
        
            self.MVA_Vars[systematic]=config.get(self.varset,systematic)
            self.MVA_Vars[systematic]=self.MVA_Vars[systematic].split(' ')
            
            print '\nSetting vars for SYS:', systematic
            print '\n-----> MVA training Variables: ', self.MVA_Vars[systematic]
            

        #define variables and specatators
        self.MVA_var_buffer = []

        for i in range(len( self.MVA_Vars['Nominal'])):
            self.MVA_var_buffer.append(array( 'f', [ 0 ] ))
            self.reader.AddVariable( self.MVA_Vars['Nominal'][i],self.MVA_var_buffer[i])

        print '\n-----> Initializing MVA: ', MVAinfo.MVAname   
        print '\t with weights: ', MVAdir+'/python/weights/'+MVAinfo.getweightfile()

        self.reader.BookMVA(MVAinfo.MVAname,MVAdir+'/python/weights/'+MVAinfo.getweightfile())

        #print '\n-----> MVA ', self.MVAname, 'is now booked...'


    def setVariables(self, tree, job):

        #Set formulas for all vars
        self.MVA_formulas={}

        for systematic in self.systematics: 

            if job.type == 'DATA' and not systematic == 'Nominal': 
                continue

            print '\n-----> Setting MVA variables for systematic: ', systematic

            self.MVA_formulas[systematic]=[]

            for j in range(len( self.MVA_Vars['Nominal'])):
                self.MVA_formulas[systematic].append(ROOT.TTreeFormula("MVA_formula%s_%s"%(j,systematic),self.MVA_Vars[systematic][j],tree))

                print '\n\t Adding Variable: ', self.MVA_Vars[systematic][j]
                
                # Next line is a bug fix in new root/python version
                #print ' self.MVA_formulas[systematic]:',  self.MVA_formulas[systematic][0]
        

                
    def evaluate(self,MVA_values,job):
        
        #Evaluate all vars and fill the branches
        #print '\n-----> evaluating MVA: ', self.MVAname
        #print self.systematics

        for systematic in self.systematics:
            
            #print '\n-----> systematic: ', systematic
            
            
            for j in range(len(self.MVA_Vars['Nominal'])):
                
                if job.type == 'DATA' and not systematic == 'Nominal': 
                    continue
                
                #print '\t Adding Variable to MVA: ', self.MVA_formulas[systematic][j]
                self.MVA_formulas[systematic][j].GetNdata()
                self.MVA_var_buffer[j][0] = self.MVA_formulas[systematic][j].EvalInstance()                

                #print 'index', self.systematics.index(systematic)

            MVA_values[self.systematics.index(systematic)] = self.reader.EvaluateMVA(self.MVAname)
            #print '\t ',MVA_values[self.systematics.index(systematic)]    
            
