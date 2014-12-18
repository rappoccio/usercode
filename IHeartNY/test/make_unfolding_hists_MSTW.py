import subprocess

for s in [ 

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom_2Dcut_nom_odd --makeResponse --semilep=1 --mttGenMax=700. --pileup=ttbar --jerSys=0.1  --pdfSys=0.0 --pdfSet=1.0 --use2Dcut --oddeven=1", 

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom_2Dcut_nom_even --makeResponse --semilep=1 --mttGenMax=700. --pileup=ttbar --jerSys=0.1  --pdfSys=0.0 --pdfSet=1.0 --use2Dcut --oddeven=2",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom_2Dcut_nom_odd --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1  --pdfSys=0.0 --pdfSet=1.0 --use2Dcut --oddeven=1",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom_2Dcut_nom_even --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1  --pdfSys=0.0 --pdfSet=1.0 --use2Dcut --oddeven=2",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom_2Dcut_nom_odd --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1 --use2Dcut  --pdfSys=0.0 --pdfSet=1.0 --oddeven=1",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_nom_2Dcut_nom_even --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1 --use2Dcut  --pdfSys=0.0 --pdfSet=1.0 --oddeven=2",

#################################################################################
           
           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup_2Dcut_nom_odd --makeResponse --semilep=1 --mttGenMax=700. --pileup=ttbar --jerSys=0.1  --pdfSys=1.0 --pdfSet=1.0 --use2Dcut --oddeven=1", 

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup_2Dcut_nom_even --makeResponse --semilep=1 --mttGenMax=700. --pileup=ttbar --jerSys=0.1  --pdfSys=1.0 --pdfSet=1.0 --use2Dcut --oddeven=2",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup_2Dcut_nom_odd --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1  --pdfSys=1.0 --pdfSet=1.0 --use2Dcut --oddeven=1",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup_2Dcut_nom_even --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1  --pdfSys=1.0 --pdfSet=1.0 --use2Dcut --oddeven=2",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup_2Dcut_nom_odd --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1 --use2Dcut  --pdfSys=1.0 --pdfSet=1.0 --oddeven=1",
           
           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfup_2Dcut_nom_even --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1 --use2Dcut  --pdfSys=1.0 --pdfSet=1.0 --oddeven=2",

#################################################################################

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown_2Dcut_nom_odd --makeResponse --semilep=1 --mttGenMax=700. --pileup=ttbar --jerSys=0.1  --pdfSys=-1.0 --pdfSet=1.0 --use2Dcut --oddeven=1", 

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown_2Dcut_nom_even --makeResponse --semilep=1 --mttGenMax=700. --pileup=ttbar --jerSys=0.1  --pdfSys=-1.0 --pdfSet=1.0 --use2Dcut --oddeven=2",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown_2Dcut_nom_odd --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1  --pdfSys=-1.0 --pdfSet=1.0 --use2Dcut --oddeven=1",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown_2Dcut_nom_even --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1  --pdfSys=-1.0 --pdfSet=1.0 --use2Dcut --oddeven=2",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown_2Dcut_nom_odd --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1 --use2Dcut  --pdfSys=-1.0 --pdfSet=1.0 --oddeven=1",

           "python iheartny_topxs_fwlite.py --files=/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu/res/\*root --outname=TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_MSTW_pdfdown_2Dcut_nom_even --makeResponse --semilep=1 --pileup=ttbar --jerSys=0.1 --use2Dcut  --pdfSys=-1.0 --pdfSet=1.0 --oddeven=2",

            ] : 
    print s
    subprocess.call( [s, ""], shell=True )
