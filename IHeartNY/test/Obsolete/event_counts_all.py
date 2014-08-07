#!/bin/python

import subprocess
import commands
import sys
import tokenize
import glob

from event_flow_crab import event_flow_crab

tokens = [
          'hltSelectionMu',
          'pileup'
    ]


dirs = glob.glob( sys.argv[1] )


for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
