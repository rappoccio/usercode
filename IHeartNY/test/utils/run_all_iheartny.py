#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700.',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_15_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown',
           pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
           ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_15_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup',
           pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
            title='TT_700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown',
            pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
            ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup',
            pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
            ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown',
            pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
            ),            
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup',
            pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
            ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu',
           title='WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True, pu='wjets'
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
        pdfsys=True, noms=True, jersys=True, jecsys=True, qcd=True
    )
]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
