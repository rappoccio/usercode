#! /usr/bin/env python
import os
import glob
import math
from array import *

from optparse import OptionParser

parser = OptionParser()

(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
from ROOT import *
gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

gSystem.Load('libCondFormatsJetMETObjects')


fout = TFile("response_full.root", "RECREATE")
  
ptBins = [0., 50., 125., 150., 220., 300., 450., 500., 600., 800., 1000., 1500., 7000.]

names = [
'QCD_pythia6_z2_plots_nominal',
'QCD_pythia6_z2_plots_jecup',
'QCD_pythia6_z2_plots_jecdn',
'QCD_herwigpp_23_plots_nominal',
'QCD_pythia8_4c_plots_nominal',
'QCD_pythia6_z2_plots_jerup',
'QCD_pythia6_z2_plots_jerdn',
'QCD_pythia6_z2_plots_jarup',
'QCD_pythia6_z2_plots_jardn',
'QCD_pythia6_z2_plots_puNominal',
'QCD_pythia6_z2_plots_puUp',
'QCD_pythia6_z2_plots_puDn'
    ]

grooms = ['', '_Trimmed', '_Filtered', '_Pruned']

for sample in range(0,len(names)) :
    print "Processing sample " + str(sample) + " : " + names[sample]
    igroom = 0

    sfiles = names[sample] + '/res/*.root'
    files = glob.glob( sfiles )
    print 'Files are : '
    for sfile in files :
        print sfile
    njobs = len(files)


    for groom in grooms:
        for iptBin in range(0,len(ptBins)-1) :

            iifile = 0
            for ifile in files :
                fin = TFile( ifile, 'r')
        
                s = 'response' + groom + '_pt' + str(iptBin)
                print 'Getting s = ' + s + ' from file ' + ifile,        
                rur = fin.Get(s)

                if iifile == 0 :
                    output = rur
                    s = "response_" + names[sample] + groom + "_pt" + str(iptBin)
                    output.SetName(s)
                    print "Setting RUR, using name " + s
                else :
                    print '--- Adding to RUR'
                    output.Add( rur )
                iifile += 1

            fout.cd()
            output.Write()

fout.Close()

