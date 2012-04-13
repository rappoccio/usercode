#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [

'Zprime_M1TeV_W10GeV-madgraph_semilep',
'Zprime_M1500GeV_W150GeV-madgraph_semilep',
'WJets-madgraph_semilep',
'TTbarJets-madgraph_semilep',
'InclusiveMu15_semilep'
]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
