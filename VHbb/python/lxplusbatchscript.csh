# Lxplus Batch Job Script
set CMSSW_PROJECT_SRC="cmssw_projects/13X/cmssw131hlt6/src"
set CFG_FILE="cfgs/steps2_3_4_5.cfg"
set OUTPUT_FILE="Analyzer_Output.root"
set TOP="$PWD"

cd /afs/cern.ch/work/d/dcurry/public/cmva_heppy/CMSSW_7_1_5/src/VHbb/python/
eval `scramv1 runtime -csh`
python ../myMacros/classification/bdt_classifier_training_loop.py

