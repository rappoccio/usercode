#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex




samples = [
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012A_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012A', jersys=False, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=False ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012B_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012B', jersys=False, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=False),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012C', jersys=False, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=False ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012D', jersys=False, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=False )
]

run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
