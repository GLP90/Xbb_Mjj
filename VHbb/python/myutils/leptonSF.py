import os
import json

class LeptonSF:
    def __init__(self, lep_json, lep_name, lep_binning, extrapolateFromClosestBin=True) :
        if not os.path.isfile(lep_json):
            self.valid = False
            if lep_json!="":
                pass
                #print "[LeptonSF]: Warning: ", lep_json, " is not a valid file. Return."
            else:
                pass
                #print "[LeptonSF]: No file has been specified. Return."
        else:
            self.init(lep_json, lep_name, lep_binning, extrapolateFromClosestBin)

    def init(self, lep_json, lep_name, lep_binning, extrapolateFromClosestBin) :
        f = open(lep_json, 'r')             
        #print '[LeptonSF]: Initialize with the following parameters:'
        #print '\tfile:',lep_json
        #print '\titem:', lep_name
        #print '\tbinning:', lep_binning
        results = json.load(f)
        if lep_name not in results.keys():
            self.valid = False
            #print "[LeptonSF]: Warning: ", lep_name , " is not a valid item. Return."
            return False
        self.res = results[lep_name]
        self.lep_name = lep_name
        self.lep_binning = lep_binning
        self.valid = True
        self.extrapolateFromClosestBin = extrapolateFromClosestBin
        f.close()

    


    def get_2D(self, pt, eta):

        stripForPt= 4

        stripForEta = 5
        if self.lep_binning not in self.res.keys():
            return [1.0, 0.0]

        if "abseta" in self.lep_binning:
            eta = abs(eta)
            stripForEta = 8

        if "pt_eta_ratio" in self.lep_binning:
            stripForEta = 4
            stripForPt= 5

        if "pt_abseta_ratio" in self.lep_binning:
            eta = abs(eta)
            stripForEta = 8
                    
        # if no bin is found, search for closest one, and double the uncertainty
        closestEtaBin = ""
        closestPtBin = ""
        closestEta = 9999.
        closestPt = 9999.

        etaFound = False
        for etaKey, values in sorted(self.res[self.lep_binning].iteritems()):
            #print etaKey
            #etaL = float(((etaKey[stripForEta:]).rstrip(']').split(',')[0]))
            #etaH = float(((etaKey[stripForEta:]).rstrip(']').split(',')[1]))
            etaL = float(((etaKey[etaKey.find('[')+1:]).rstrip(']').split(',')[0]))
            etaH = float(((etaKey[etaKey.find('[')+1:]).rstrip(']').split(',')[1]))
            
            ptFound = False

            if abs(etaL-eta)<closestEta or abs(etaH-eta)<closestEta and not etaFound:
                closestEta = min(abs(etaL-eta), abs(etaH-eta))
                closestEtaBin = etaKey

            if (eta>etaL and eta<etaH):
                closestEtaBin = etaKey
                etaFound = True                

            for ptKey, result in sorted(values.iteritems()) :
                #ptL = float(((ptKey[stripForPt:]).rstrip(']').split(',')[0]))
                #ptH = float(((ptKey[stripForPt:]).rstrip(']').split(',')[1]))                
                ptL = float(((ptKey[ptKey.find('[')+1:]).rstrip(']').split(',')[0]))
                ptH = float(((ptKey[ptKey.find('[')+1:]).rstrip(']').split(',')[1]))


                if abs(ptL-pt)<closestPt or abs(ptH-pt)<closestPt and not ptFound:
                    closestPt = min(abs(ptL-pt), abs(ptH-pt))
                    closestPtBin = ptKey

                if (pt>ptL and pt<ptH):
                    closestPtBin = ptKey
                    ptFound = True

                if etaFound and ptFound:
                    return [result["value"], result["error"]]

        if self.extrapolateFromClosestBin and not (closestPtBin=="" or closestEtaBin==""):
            return [self.res[self.lep_binning][closestEtaBin][closestPtBin]["value"], 
                    2*self.res[self.lep_binning][closestEtaBin][closestPtBin]["error"]] 
        else:
            return [1.0, 0.0]


    
    def get_2D_eta_pt(self, eta, pt):

        stripForEta = 5
        if self.lep_binning not in self.res.keys():
            return [1.0, 0.0]

        #print '\nLepton Eta:', eta
        #print 'Lepton Pt:', pt

        for etaKey, values in sorted(self.res[self.lep_binning].iteritems()) :
            #print etaKey
            etaL = float(((etaKey[stripForEta:]).rstrip(']').split(',')[0]))
            etaH = float(((etaKey[stripForEta:]).rstrip(']').split(',')[1]))
            #print 'EtaL:', etaL
            #print 'EtaH:', etaH

            if not (eta>etaL and eta<etaH):
                continue

            for ptKey, result in sorted(values.iteritems()) :
                #print ptKey
                ptL = float(((ptKey[4:]).rstrip(']').split(',')[0]))
                ptH = float(((ptKey[4:]).rstrip(']').split(',')[1]))
                #print 'PtL:', ptL
                #print 'PtH:', ptH
                
                if not (pt>ptL and pt<ptH):
                    continue
                
                #print 'SF:', result["value"]
                return [result["value"], result["error"]]

            

        # if nothing was found, return 1 +/- 0
        return [1.0, 0.0]


    def get_1D(self, pt):
        if not self.valid:
            return [1.0, 0.0]

        if self.lep_binning not in self.res.keys():
            return [1.0, 0.0]

        # if no bin is found, search for closest one, and double the uncertainty
        closestPtBin = ""
        closestPt = 9999.

        ptFound = False

        for ptKey, result in sorted(self.res[self.lep_binning].iteritems()) :
            ptL = float(((ptKey[ptKey.find(':')+2:]).rstrip(']').split(',')[0]))
            ptH = float(((ptKey[ptKey.find(':')+2:]).rstrip(']').split(',')[1]))

            #print 'ptL is', ptL
            #print 'ptH is', ptH

            if abs(ptL-pt)<closestPt or abs(ptH-pt)<closestPt and not ptFound:
                closestPt = min(abs(ptL-pt), abs(ptH-pt))
                closestPtBin = ptKey

                if (pt>ptL and pt<ptH):

                    closestPtBin = ptKey
                    ptFound = True

                if ptFound:
                    return [result["value"], result["error"]]

        if self.extrapolateFromClosestBin and not (closestPtBin==""):
            return [self.res[self.lep_binning][closestPtBin]["value"],2*self.res[self.lep_binning][closestPtBin]["error"]]
        else:
            return [1.0, 0.0]
    



##################################################################################################
# EXAMPLE 

#jsons = {
#    'SingleMuonTrigger_Z_RunCD_Reco74X_Dec1.json' : ['runD_IsoMu20_OR_IsoTkMu20_HLTv4p3_PtEtaBins', 'abseta_pt_ratio'],
#    'MuonIso_Z_RunCD_Reco74X_Dec1.json' : ['NUM_LooseRelIso_DEN_LooseID_PAR_pt_spliteta_bin1', 'abseta_pt_ratio'], 
#    'MuonID_Z_RunCD_Reco74X_Dec1.json' : ['NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1', 'abseta_pt_ratio'] ,
#    'CutBasedID_LooseWP.json' : ['CutBasedID_LooseWP', 'eta_pt_ratio'],
#    'CutBasedID_TightWP.json' : ['CutBasedID_TightWP', 'eta_pt_ratio'],
#    }

# example
#pt = 40.01
#eta = -1.68

#for j, name in jsons.iteritems():
#    lepCorr = LeptonSF(j , name[0], name[1])
#    weight = lepCorr.get_2D( pt , eta)
#    val = weight[0]
#    err = weight[1]
#    print j, name[0], ': ',  val, ' +/- ', err

