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
  
ptBins = [0., 50.,125.,200., 300., 400., 500., 600., 800., 1000., 1500., 7000.]

names = [
    ["pythia6_z2", None],
    ["pythia6_z2", 'jecup'],
    ["pythia6_z2", 'jecdn'],
    ["pythia8_4c", None],
    ["herwigpp_23", None]
    ]

njobs = 10

grooms = ['', '_Groom0', '_Groom1', '_Groom2']
outgrooms = ['', '_Trimmed', '_Filtered', '_Pruned']

for sample in range(0,len(names)) :
    print "Processing sample " + str(sample) + " : " + names[sample][0]
    igroom = 0
    for groom in grooms :
        
        for ibin in range(0,len(ptBins)-1) :
            print "   Processing bin " + str(ibin)
            for i in range(0,njobs) : 
                print "     Processing job " + str(i)
                if names[sample][1] is None :
                    s = "QCD_" + names[sample][0] + "_v10beta_plots" + str(i) + ".root"
                else :
                    s = "QCD_" + names[sample][0] + "_v10beta_" + names[sample][1]  + "_plots" + str(i) + ".root"
                fin = TFile( s, "r")
                s = "response_pt" + str(ibin) + groom
                print "Getting RUR " + s
                rur = fin.Get(s)
                if i == 0 :
                    output = rur
                    if names[sample][1] is None :
                        s = "response_" + names[sample][0] + "_pt" + str(ibin) + outgrooms[igroom]
                    else :
                        s = "response_" + names[sample][0] + "_pt" + str(ibin) + '_' +  names[sample][1] + outgrooms[igroom]
                    output.SetName(s)
                    print "Setting RUR name to " + s
                else :
                    output.Add( rur )

            fout.cd()
            output.Write()
        igroom += 1
fout.Close()

