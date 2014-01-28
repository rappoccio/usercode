#!/usr/bin/env python

from run_iheartny import *
import shlex



samples = [
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012A_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012A', jersys=False, jecsys=False, pdfsys=False ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012B_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012B', jersys=False, jecsys=False, pdfsys=False ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012C', jersys=False, jecsys=False, pdfsys=False ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012D', jersys=False, jecsys=False, pdfsys=False )
]

for sample in samples :
    run_iheartny( sample )
