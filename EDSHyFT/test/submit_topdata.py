# !/bin/python

import subprocess




crabFiles = [
['crab_shyft_Mu-range1_skim.cfg', 'shyft_38xOn35x_v1_r1_skim'],
['crab_shyft_Mu-range2_skim.cfg', 'shyft_38xOn35x_v1_r2_skim'],
['crab_shyft_Mu-range3_skim.cfg', 'shyft_38xOn35x_v1_r3_skim']
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
