# !/bin/python
# Script for submitting multiple prepared crab configuration files.
# Usage :
# python submit_finishedfiles.py --files=*.cfg
#
# This supports "glob" wildcard formats :
# http://docs.python.org/2/library/glob.html
#

import subprocess

import glob

from optparse import OptionParser

usage = "python submit_finishedfiles.py --files=[input files go here, glob format]"

parser = OptionParser(usage=usage)

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files in python "glob" format')

(options, args) = parser.parse_args()

argv = []


crabFiles = glob.glob( options.files )


print 'Submitting crab files: '
print crabFiles

for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile
    print s
    subprocess.call( [s], shell=True )
    f = open( crabFile, 'r')
    lines = f.readlines()
    for line in lines :
        isub = line.find( 'ui_working_dir' )
        if isub >= 0 :
            isubend = line.find('=')
            ssub = line[isubend + 1:]
            break
    f.close()

    s = 'crab -submit -c ' + ssub
    print s
    subprocess.call( [s], shell=True )
