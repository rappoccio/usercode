# !/bin/python

import subprocess

idir='/uscms_data/d2/rappocc/analysis/TopTagging36x/CMSSW_3_6_1_TopTagging/src/Analysis/EDBoostedTopAnalysis/test'

crabfiles = [
    ['crab_ttbsmAug10_r1.cfg', 'ttbsmAug10_381on36x_r1_version1'],
    ['crab_ttbsmAug10_r2.cfg', 'ttbsmAug10_381on36x_r2_version1'],
    ['crab_ttbsmAug10_r3.cfg', 'ttbsmAug10_381on36x_r3_version1'],
    ['crab_ttbsmAug10_r4.cfg', 'ttbsmAug10_381on36x_r4_version1'],
    ['crab_ttbsmAug10_r5.cfg', 'ttbsmAug10_381on36x_r5_version1'],
    ['crab_ttbsmAug10_r6.cfg', 'ttbsmAug10_381on36x_r6_version1']
    ]

for crabfile in crabfiles :
    s = 'crab -create -cfg ' + crabfile[0]
    print s
    subprocess.call( [s], shell=True )
    t = 'crab -submit -c ' + crabfile[1]
    print t
    subprocess.call( [t], shell=True )

