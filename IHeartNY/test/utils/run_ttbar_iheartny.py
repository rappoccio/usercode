#!/usr/bin/env python

from run_iheartny import run_threads, Sample
import shlex



samples = [
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),            
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--makeResponse=1 --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags=' --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags=' --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
           ),
Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
    ),            
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False
    ),

]

# run the different channels
run_threads( samples )
