# !/bin/python

import subprocess

idir='/uscms_data/d2/rappocc/analysis/TopTagging36x/CMSSW_3_6_1_TopTagging/src/Analysis/EDBoostedTopAnalysis/test'

datasets = [
'/QCDDiJet_Pt80to120/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt800to1000/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt600to800/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt50to80/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt470to600/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt380to470/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt30to50/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt300to380/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt3000to3500/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt2600to3000/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt230to300/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt2200to2600/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt20to30/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt1800to2200/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt170to230/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt15to20/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt1400to1800/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt120to170/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt1000to1400/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
'/QCDDiJet_Pt0to15/srappocc-ttbsm_361_v1-0dc303dee610603ff84e9ada0c4a27a9/USER',
]

for dataset in datasets :
    toks = dataset.split('/')
    s = './my_multicrab.pl crab_dummy_hadronic_analysis.cfg hadronicEDAnalyzer_cfg.py '  + dataset + ' ttbsm_361_v1 -1 5 condor 0 ' + idir + ' ' + toks[1] + '_reweighted_pt_gt25_templates'
    print s
    subprocess.call( [s], shell=True )
