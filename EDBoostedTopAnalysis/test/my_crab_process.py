#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'ttbsmAug10_381on36x_r1_version1',
'ttbsmAug10_381on36x_r2_version1',
'ttbsmAug10_381on36x_r3_version1',
'ttbsmAug10_381on36x_r4_version1',
'ttbsmAug10_381on36x_r5_version1',
'ttbsmAug10_381on36x_r6_version1'

]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
