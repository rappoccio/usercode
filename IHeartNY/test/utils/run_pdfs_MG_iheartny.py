#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
    
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_mu',
           title='TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_mu',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
