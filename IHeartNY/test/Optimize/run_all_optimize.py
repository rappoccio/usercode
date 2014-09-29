#!/usr/bin/env python

from run_optimize import run_threads, Sample

import shlex



samples = [
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           flags='--mttGenMax=700.',
           noms=True, jersys=False, jecsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           noms=True, jersys=False, jecsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/rappocc/nobackup/analysis/B2G/CMSSW_5_3_14_patch1_TOPXS/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           noms=True, jersys=False, jecsys=False, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu/res/*root',
           title='WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_optimize_mu',
           pu='wjets', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           pu='sts', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           pu='stt', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           pu='sttw', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           pu='stsb', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           pu='sttb', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms/home/maral87/nobackup/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/*root',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_optimize_mu',
           pu='sttwb', noms=True, jersys=True, jecsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012A_22Jan/res/*root',
           title='SingleMu_optimize_mu_Run2012A', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012B_22Jan/res/*root',
           title='SingleMu_optimize_mu_Run2012B', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_1*.root',
           title='SingleMu_optimize_mu_Run2012C_1', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_2*.root',
           title='SingleMu_optimize_mu_Run2012C_2', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_3*.root',
           title='SingleMu_optimize_mu_Run2012C_3', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_4*.root',
           title='SingleMu_optimize_mu_Run2012C_4', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_5*.root',
           title='SingleMu_optimize_mu_Run2012C_5', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_6*.root',
           title='SingleMu_optimize_mu_Run2012C_6', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_7*.root',
           title='SingleMu_optimize_mu_Run2012C_7', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_8*.root',
           title='SingleMu_optimize_mu_Run2012C_8', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012C_22Jan/res/shyft_ultraslim_9*.root',
           title='SingleMu_optimize_mu_Run2012C_9', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_1*root',
           title='SingleMu_optimize_mu_Run2012D_1', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_2*root',
           title='SingleMu_optimize_mu_Run2012D_2', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_3*root',
           title='SingleMu_optimize_mu_Run2012D_3', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_4*root',
           title='SingleMu_optimize_mu_Run2012D_4', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_5*root',
           title='SingleMu_optimize_mu_Run2012D_5', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_6*root',
           title='SingleMu_optimize_mu_Run2012D_6', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_7*root',
           title='SingleMu_optimize_mu_Run2012D_7', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_8*root',
           title='SingleMu_optimize_mu_Run2012D_8', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/SingleMu_Run2012D_22Jan/res/shyft_ultraslim_9*root',
           title='SingleMu_optimize_mu_Run2012D_9', 
           jersys=None, jecsys=False, qcd=True, pu=None, noms=True, flags='--isData'
    ),

]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
