#!/usr/bin/env python

from run_iheartny import run_threads, Sample
import shlex



samples = [
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --makeResponse',
           pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ),
    ## Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
    ##        title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
    ##         flags='--makeResponse',
    ##        pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ## ),
    ## Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
    ##        title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
    ##        flags='--makeResponse',
    ##        pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ## ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_15_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --makeResponse',
           pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
           ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_15_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --makeResponse',
           pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
           ),
    ## Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
    ##         title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
    ##         flags='--makeResponse',
    ##         pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ##         ),
    ## Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
    ##        title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
    ##        flags='--makeResponse',
    ##        pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ##         ),
    ## Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
    ##        title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
    ##        flags='--makeResponse',
    ##        pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ##         ),            
    ## Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
    ##        title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
    ##        flags='--makeResponse',
    ##        pdfsys=False, noms=True, jersys=False, jecsys=False, qcd=False
    ##        )
]

# run the different channels
run_threads( samples )
