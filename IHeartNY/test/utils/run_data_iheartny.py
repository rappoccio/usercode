#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex




samples = [
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012A_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012A', jersys=None, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=True, flags='--isData'),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012B_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012B', jersys=None, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=True, flags='--isData'),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012C', jersys=None, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=True, flags='--isData'),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan',
           title='SingleMu_iheartNY_V1_mu_Run2012D', jersys=None, jecsys=False, pdfsys=False, qcd=True, pu=None, noms=True, flags='--isData')
]

run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
