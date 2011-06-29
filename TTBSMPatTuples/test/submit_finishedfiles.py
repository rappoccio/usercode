# !/bin/python

import subprocess

import glob

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

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
