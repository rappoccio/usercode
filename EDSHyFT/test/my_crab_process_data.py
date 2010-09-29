#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
    'shyft_38xOn35x_v3_r1',
    'shyft_38xOn35x_v3_r2',
    'shyft_38xOn35x_v3_r3'
]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
