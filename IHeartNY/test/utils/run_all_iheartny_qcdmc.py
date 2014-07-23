#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
#Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_fixPDF',
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --semilep=1.0', 
           pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
#Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_fixPDF',
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu', 
           flags='--semilep=1.0', 
           pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
#Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_fixPDF',
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu', 
           flags='--semilep=1.0', 
           pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
#Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_fixPDF',
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --semilep=-1.0', 
           pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
#Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_fixPDF',
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu', 
           flags='--semilep=-1.0', 
           pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
#Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_fixPDF',
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu', 
           flags='--semilep=-1.0', 
           pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
#    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu',
#           title='WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu',
#           pu='wjets', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
#    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sts', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stt', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttw', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu',
           pu='stsb', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttb', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttwb', pdfsys=False, noms=False, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=True
    )
]

# run the different channels
run_threads( samples )
