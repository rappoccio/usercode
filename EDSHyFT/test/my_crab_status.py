#!/bin/python

import subprocess
import os

from sys import argv
if len(argv)<2:
    print "usage: python my_crab_status_ele.py COMMAND"
    print "where COMMAND can be status, getoutput, etc"
    exit()

argument=""
for i in argv[1:]:
    argument += i+" "

crabPath='/uscms_data/d2/skhalil/ShyftTemplates11'


crabFiles = [
    'SingleElectron_ttbsm_423_v7_p1',
    'SingleElectron_ttbsm_423_v7_p2',
    'SingleElectron_ttbsm_423_v7_p3',
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

