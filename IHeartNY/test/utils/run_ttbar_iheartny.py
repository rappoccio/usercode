#!/usr/bin/env python

from run_iheartny import run_threads, Sample
import shlex



samples = [
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700.', pdfsys=False, jersys=False, jecsys=False),
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=False, jersys=False, jecsys=False),
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=False, jersys=False, jecsys=False)
]

# run the different channels
run_threads( samples )
