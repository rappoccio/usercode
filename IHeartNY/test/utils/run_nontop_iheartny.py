#!/usr/bin/env python

from run_iheartny import *

import shlex



samples = [
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_010315/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_010315/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sts', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stt', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttw', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stsb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttwb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True)
]

# run the different channels
run_threads( samples )
