#!/usr/bin/python

import sys
import os, commands

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--path', metavar='F', type='string', action='store',
                  default = '/pnfs/cms/WAX/11/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',
                  dest='path',
                  help='Input path')

parser.add_option('--outputText', metavar='F', type='string', action='store',
                  default = "outputText",
                  dest='outputText',
                  help='output file')

# Parse and get arguments
(options, args) = parser.parse_args()

#path = sys.argv[1]
path = options.path
textName = options.outputText

cmd = 'ls %s/' %(path)

f = open(textName+'.txt', 'w')

for i in commands.getoutput(cmd).split('\n'):
    #print path+"/"+i
    f.write(path+"/"+i+'\n')
    
    
