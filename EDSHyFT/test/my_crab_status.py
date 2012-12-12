#!/bin/python

import subprocess

dirs = [
'shyft_EG-v1/',
'shyft_EG-v2/',
'shyft_JetMETTau-v1/',
'shyft_JetMETTau-v2/',
'shyft_May6thPDSkim2_SD_EG-v1/',
'shyft_May6thPDSkim2_SD_JetMETTau-v1/',
'shyft_May6thPDSkim2_SD_Mu-v1/',
'shyft_Mu-v1/',
'shyft_Mu-v2/'

]

for idir in dirs :
    s = "crab -status -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
