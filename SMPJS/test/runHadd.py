#! /usr/bin/env python
import os
import glob
import sys
import subprocess


files = [
'Jet_plots_nominal',
'QCD_herwigpp_23_plots_nominal',
'QCD_pythia6_z2_plots_jardn',
'QCD_pythia6_z2_plots_jarup',
'QCD_pythia6_z2_plots_jecdn',
'QCD_pythia6_z2_plots_jecup',
'QCD_pythia6_z2_plots_jerdn',
'QCD_pythia6_z2_plots_jerup',
'QCD_pythia6_z2_plots_nominal',
'QCD_pythia6_z2_plots_puDn',
'QCD_pythia6_z2_plots_puNominal',
'QCD_pythia6_z2_plots_puUp',
'QCD_pythia8_4c_plots_nominal',

    ]



for ifile in files:
    rootfiles = glob.glob( ifile + '/res/*.root')
    sout = ifile + '.root'
    outstr = 'hadd ' + sout + ' ' + ifile + '/res/*.root'
    print 'executing: ' + outstr
    subprocess.call( [outstr, ""], shell=True )
