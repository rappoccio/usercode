#!/usr/bin/ python
# ==============================================================================
#  File and Version Information:
#        merge_files.py 
#        01/16/14 
#        Maral Alyari
#  Purpose : Put all of the histograms from several files together into one.
# ==============================================================================

from ROOT import *
import glob

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--files', metavar='D', type='string', action='store',
                  dest='files',
                  help='Files to input')

parser.add_option('--output', metavar='D', type='string', action='store',
                  default='mujets.root',
                  dest='output',
                  help='File to output')

(options, args) = parser.parse_args()

argv = []

gROOT.Macro("rootlogon.C")

hists = []

inputfilestrs = glob.glob( options.files ) 
inputfiles = []

for ifile in inputfilestrs :
    print 'processing file : ' + ifile
    f = TFile( ifile ) 
    inputfiles.append( f )
    keys = f.GetListOfKeys()
    for key in keys :
        print 'Adding ' + key.GetName()
        hists.append( key ) 


fout = TFile(options.output , 'RECREATE')



fout.cd()

for hist in hists : 
    hist.Write()


fout.Close()


