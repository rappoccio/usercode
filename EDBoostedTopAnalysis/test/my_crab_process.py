#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'QCDDiJet_Pt0to15_reweighted_pt_gt50',
'QCDDiJet_Pt1000to1400_reweighted_pt_gt50',
'QCDDiJet_Pt120to170_reweighted_pt_gt50',
'QCDDiJet_Pt1400to1800_reweighted_pt_gt50',
'QCDDiJet_Pt15to20_reweighted_pt_gt50',
'QCDDiJet_Pt170to230_reweighted_pt_gt50',
'QCDDiJet_Pt1800to2200_reweighted_pt_gt50',
'QCDDiJet_Pt20to30_reweighted_pt_gt50',
'QCDDiJet_Pt2200to2600_reweighted_pt_gt50',
'QCDDiJet_Pt230to300_reweighted_pt_gt50',
'QCDDiJet_Pt2600to3000_reweighted_pt_gt50',
'QCDDiJet_Pt3000to3500_reweighted_pt_gt50',
'QCDDiJet_Pt300to380_reweighted_pt_gt50',
'QCDDiJet_Pt30to50_reweighted_pt_gt50',
'QCDDiJet_Pt380to470_reweighted_pt_gt50',
'QCDDiJet_Pt470to600_reweighted_pt_gt50',
'QCDDiJet_Pt50to80_reweighted_pt_gt50',
'QCDDiJet_Pt600to800_reweighted_pt_gt50',
'QCDDiJet_Pt800to1000_reweighted_pt_gt50',
'QCDDiJet_Pt80to120_reweighted_pt_gt50'
]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
