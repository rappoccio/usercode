#!/usr/bin/env python

from run_iheartny import *

import shlex



samples = [
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           title='W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           title='W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           title='W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_slc6/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           title='W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_el',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el',
           pu='sts', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el',
           pu='stt', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el',
           pu='sttw', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el',
           pu='stsb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el',
           pu='sttb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele'),
    Sample(directory='/uscms_data/d3/maral87/TopXS/ntuples_e_012114/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el',
           pu='sttwb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True, flags='--lepType=ele')
]

# run the different channels
run_threads( samples )
