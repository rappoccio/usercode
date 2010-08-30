# !/bin/python

import subprocess




crabFiles = [
['crab_shyft_Mu-range1.cfg', 'shyft_38xOn35x_v1_r1'],
['crab_shyft_Mu-range2.cfg', 'shyft_38xOn35x_v1_r2'],
['crab_shyft_Mu-range3.cfg', 'shyft_38xOn35x_v1_r3']
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
