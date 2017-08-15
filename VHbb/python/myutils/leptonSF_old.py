import os
import json

class LeptonSF:
    def __init__(self, lep_json, lep_name, lep_binning) :
        self.init(lep_json, lep_name, lep_binning)

    def init(self, lep_json, lep_name, lep_binning) :
        f = open(lep_json, 'r')             
        results = json.load(f)
        if lep_name not in results.keys():
            return False
        self.res = results[lep_name]
        self.lep_binning = lep_binning
        f.close()

    def get_2D(self, pt, eta):

        stripForEta = 5
        if self.lep_binning not in self.res.keys():
            return [1.0, 0.0]

        if "pt_abseta_ratio" in self.lep_binning:
            eta = abs(eta)
            stripForEta = 8
            
            for ptKey, values in sorted(self.res[self.lep_binning].iteritems()) :
                ptL = float(((ptKey[4:]).rstrip(']').split(',')[0]))
                ptH = float(((ptKey[4:]).rstrip(']').split(',')[1]))
                if not (pt>ptL and pt<ptH):
                    continue

                for etaKey, result in sorted(values.iteritems()) :
                    #print etaKey
                    etaL = float(((etaKey[stripForEta:]).rstrip(']').split(',')[0]))
                    etaH = float(((etaKey[stripForEta:]).rstrip(']').split(',')[1]))
                    if not (eta>etaL and eta<etaH):
                        continue
                    
                    return [result["value"], result["error"]]

        else:
            for etaKey, values in sorted(self.res[self.lep_binning].iteritems()) :
                #print etaKey
                etaL = float(((etaKey[stripForEta:]).rstrip(']').split(',')[0]))
                etaH = float(((etaKey[stripForEta:]).rstrip(']').split(',')[1]))
                if not (eta>etaL and eta<etaH):
                    continue 

                for ptKey, result in sorted(values.iteritems()) :
                    ptL = float(((ptKey[4:]).rstrip(']').split(',')[0]))
                    ptH = float(((ptKey[4:]).rstrip(']').split(',')[1]))                
                    if not (pt>ptL and pt<ptH):
                        continue 
                    return [result["value"], result["error"]]

        # if nothing was found, return 1 +/- 0
        return [1.0, 0.0]


    def get_1D(self, eta):

        stripForEta = 5
        if self.lep_binning not in self.res.keys():
            return [1.0, 0.0]

        print 'eta:', eta

        for etaKey, values in sorted(self.res[self.lep_binning].iteritems()) :
            print etaKey
            print etaKey.strip("[]").split(',')
            print etaKey.strip("[]").split(',')[0]
            etaL = float(((etaKey[stripForEta:]).rstrip(']').split(',')[0]))
            etaH = float(((etaKey[stripForEta:]).rstrip(']').split(',')[1]))
            if not (eta>etaL and eta<etaH):
                continue 

            return [result["value"], result["error"]]

        # if nothing was found, return 1 +/- 0
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

