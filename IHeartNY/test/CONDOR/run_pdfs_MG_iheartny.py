#!/usr/bin/env python

from run_iheartny_unfold import run_threads, Sample

import shlex



samples = [
    
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_MG_mu',
           title='TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_mu',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_MG_el',
           title='TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_el',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TTJets_HadronicMGDecays_8TeV-madgraph_iheartNY_mu/res',
           title='TTJets_HadronicMGDecays_8TeV-madgraph_iheartNY_V1_mu',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TTJets_HadronicMGDecays_8TeV-madgraph_iheartNY_el/res',
           title='TTJets_HadronicMGDecays_8TeV-madgraph_iheartNY_V1_el',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TTJets_FullLeptMGDecays_8TeV-madgraph_iheartNY_mu/res',
           title='TTJets_FullLeptMGDecays_8TeV-madgraph_iheartNY_V1_mu',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TTJets_FullLeptMGDecays_8TeV-madgraph_iheartNY_el/res',
           title='TTJets_FullLeptMGDecays_8TeV-madgraph_iheartNY_V1_el',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    
]


run_threads( samples )
# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
