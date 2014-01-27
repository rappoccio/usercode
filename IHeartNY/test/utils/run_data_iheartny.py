#!/usr/bin/env python

from run_iheartny import *
import shlex



samples = [
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012*_22Jan',
           title='SingleMu_iheartNY_V1_mu', jersys=False, jecsys=False, pdfsys=False )
]

for sample in samples :
    run_iheartny( sample )
