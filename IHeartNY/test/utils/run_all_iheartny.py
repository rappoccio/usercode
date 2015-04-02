#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
    #------------------------------    
    # Nominal samples, CT10
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=0.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Up samples, CT10
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Down samples, CT10
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfdown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=-1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfdown',
           flags='--makeResponse  --semilep=1.0 --pdfSys=-1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfdown',
           flags='--makeResponse  --semilep=1.0 --pdfSys=-1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfdown',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=-1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),




    #------------------------------    
    # Nominal samples, MSTW
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=0.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Up samples, MSTW
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Down samples, MSTW
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=-1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown',
           flags='--makeResponse  --semilep=1.0 --pdfSys=-1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown',
           flags='--makeResponse  --semilep=1.0 --pdfSys=-1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=-1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_MSTW_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),


    
    #------------------------------    
    # Nominal samples, NNPDF
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_nom',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_nom',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_nom',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_nom',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=0.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Up samples, NNPDF
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfup',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Down samples, NNPDF
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfdown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=-1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfdown',
           flags='--makeResponse  --semilep=1.0 --pdfSys=-1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfdown',
           flags='--makeResponse  --semilep=1.0 --pdfSys=-1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfdown',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=-1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_NNPDF_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_NNPDF_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=2.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),


        
    #------------------------------    
    # Q2 Scale up and down samples
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),            
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),            
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    #------------------------------
    # Non-ttbar samples
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sts', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stt', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttw', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stsb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttwb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    )
]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
