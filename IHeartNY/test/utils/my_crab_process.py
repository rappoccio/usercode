#!/bin/python
#
# my_crab_process trivially executes several CRAB commands on a bunch of different directories. 
# This is mostly because "multicrab" stopped working a long time ago. 
#
#
#

import subprocess
import sys
import glob


from optparse import OptionParser

usage = 'my_crab_process --files=[input CRAB directories, glob format] --command=[CRAB command to run]'
parser = OptionParser(usage)

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input CRAB directories, glob format')

parser.add_option('--command', metavar = 'C', type='string', action='store',
                  dest='command',
                  default='status',
                  help='CRAB command to run')

(options, args) = parser.parse_args()


argv = []

dirs = glob.glob( options.files )

for idir in dirs :
    print '--------------------------------'
    print '--------------------------------'
    print '--------------------------------'    
    s = "crab -" + options.command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
