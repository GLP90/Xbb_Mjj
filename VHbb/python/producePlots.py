import os, subprocess

# ======= Plots from Datacards Options ========

isMjj = False
#isMjj = True

isBDT = False
isBDT = True


# =============================================




def runPlot(opts):
    command = './stack_from_dc.py -D %(dc)s -B %(bin)s -C %(config)s -V %(var)s -R %(region)s' %(opts)
    print command
    subprocess.call([command], shell=True)
    #command = './stack_from_dc.py -D %(dc)s -B %(bin)s -C %(config)s -V %(var)s -M %(mlfit)s' %opts
    #print command
    #subprocess.call([command], shell=True)


def runAll():

    if isBDT:

        path = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/'

        configuration = '13TeVconfig/configPlot_dc_BDT'
        
        modes = ['Zll', 'gg_plusZll']
        #modes = ['gg_plusZll']
        #modes = ['Zll']
    
        cards = {'Zll': 'vhbb_DC_TH_BDT_M125_Zuu_HighPt_13TeV.txt', \
                 'gg_plusZll': 'vhbb_DC_TH_BDT_gg_plusZH_M125_Zuu_HighPt_13TeV.txt' \
                 }

        # bin structure:  'channel': [datacard bin, name of BDT method in tree,  cut region to make BDT method]
        #bins = {'Zll': [['Zuu_lowZpt_13TeV', 'ZH125_Zuu_lowZpt', 'bdt_Zuu_low_Zpt'], ['Zuu_highZpt_13TeV', 'ZH125_Zuu_highZpt', 'bdt_Zuu_high_Zpt'], \
        #                ['Zee_lowZpt_13TeV', 'ZH125_Zee_lowZpt', 'bdt_Zee_low_Zpt'], ['Zee_highZpt_13TeV', 'ZH125_Zee_highZpt', 'bdt_Zee_high_Zpt']\
        #                ], \
        #        'gg_plusZll': [['Zuu_lowZpt_13TeV', 'gg_plus_ZH125_Zuu_lowZpt', 'bdt_Zuu_low_Zpt'], ['Zuu_highZpt_13TeV', 'gg_plus_ZH125_Zuu_highZpt', 'bdt_Zuu_high_Zpt'], \
        #                  ]\
        #        }

        # temp machinery
        bins = {'Zll'        : [['Zuu_HighPt_13TeV', 'ZH125_Zuu_highZpt', 'bdt_Zuu_high_Zpt']], \
                'gg_plusZll' : [['Zuu_HighPt_13TeV', 'gg_plus_ZH125_Zuu_highZpt', 'bdt_Zuu_high_Zpt']]\
                }
        
        

        
    if isMjj:

        path = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/'

        configuration = '13TeVconfig/configPlot_dc_Mjj'
        
        modes = ['Zll']

        cards = {'Zll': 'vhbb_DC_TH_MJJ_M125_13TeV_Combined.txt'}

        bins = {'Zll': [['Zuu_LowPt_13TeV', 'HCSV_mass', 'signal_Zuu_low_Zpt'], ['Zee_LowPt_13TeV', 'HCSV_mass', 'signal_Zee_low_Zpt'], \
                        ['Zuu_MedPt_13TeV', 'HCSV_mass', 'signal_Zuu_med_Zpt'], ['Zee_MedPt_13TeV', 'HCSV_mass', 'signal_Zee_med_Zpt'], \
                        ['Zuu_HighPt_13TeV', 'HCSV_mass', 'signal_Zuu_high_Zpt'], ['Zee_HighPt_13TeV', 'HCSV_mass', 'signal_Zee_high_Zpt']\
                        ]}

        
    
    # Run the stackMaker
    for mode in modes:
        for bin in bins[mode]:
            opts = {}
            opts['region'] = bin[2]
            opts['bin'] = bin[0]
            opts['var'] = bin[1]
            opts['config'] = '%s' %configuration
            opts['dc'] = '%s%s' %(path,cards[mode])
            opts['mlfit'] = '%s/mlfit.root' %(path)
            runPlot(opts)

runAll()
