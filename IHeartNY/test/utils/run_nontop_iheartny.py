#!/usr/bin/env python

from run_iheartny import *

import shlex



samples = [
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu',
           title='WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu',
           pdfsys=False),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=False),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=False),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=False),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu',
           pdfsys=False),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=False),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
        pdfsys=False)
]

for sample in samples :
    run_iheartny( sample )
