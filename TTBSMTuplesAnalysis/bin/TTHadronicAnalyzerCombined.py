#! /usr/bin/env python
import os
import glob




import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle

from Analysis.TTBSMTuplesAnalysis.TriggerAndEventSelectionObject import TriggerAndEventSelectionObject
from Analysis.TTBSMTuplesAnalysis.Type12Analyzer import Type12Analyzer
from Analysis.TTBSMTuplesAnalysis.MistagMaker import MistagMaker
from Analysis.TTBSMTuplesAnalysis.TTKinPlotsAnalyzer import TTKinPlotsAnalyzer

from optparse import OptionParser


parser = OptionParser()

parser.add_option('-i', '--dirs', metavar='F', type='string', action='store',
                  default='Jet_Run2011A-PromptReco-v4_range1_ttbsm_v6_ttbsmTuples_v3',
                  dest='dirs',
                  help='Input Directories (glob format)')


parser.add_option('-a', '--analyzer', metavar='F', type='string', action='store',
                  default='Type12Analyzer',
                  dest='analyzer',
                  help='Analyzer to run. Options are Type12Analyzer, MistagMaker')


parser.add_option('-o', '--outfile', metavar='N', type='string', action='store',
                  default='TTHadronicAnalyzerCombined_Jet_PD_May10ReReco_PromptReco_range1_range2',
                  dest='outfile',
                  help='output file')

parser.add_option('--useMC', action='store_true',
                  default=False,
                  dest='useMC',
                  help='Use Monte Carlo')

parser.add_option('-m', '--mistagFile', metavar='N', type='string', action='store',
                  default='MISTAG',
                  dest='mistagFile',
                  help='mistag file')


(options, args) = parser.parse_args()

files = glob.glob( options.dirs + "*.root" )
print files




events = Events (files)

myAnaTrigs = [
    0,#'HLT_Jet240_v1',
    1,#'HLT_Jet300_v1',
    2,#'HLT_Jet300_v2',
    3,#'HLT_Jet300_v3',
    4,#'HLT_Jet300_v4',
    5,#'HLT_Jet300_v5',
    6,#'HLT_Jet300_v6',
    7,#'HLT_Jet300_v7',
    8,#'HLT_Jet370_v1',
    9,#'HLT_Jet370_v2',
    10,#'HLT_Jet370_v3',
    11,#'HLT_Jet370_v4',
    12,#'HLT_Jet370_v5',
    13,#'HLT_Jet370_v6',
    14,#'HLT_Jet370_v7'
    ]

triggerSelection = TriggerAndEventSelectionObject( myAnaTrigs )


if options.analyzer == "Type12Analyzer" :
    analyzer = Type12Analyzer(options.useMC, options.outfile + '_type12', options.mistagFile)
elif options.analyzer == "MistagMaker" :
    analyzer = MistagMaker( options.outfile + '_mistag')
elif options.analyzer == "TTKinPlotsAnalyzer" :
    analyzer = TTKinPlotsAnalyzer( options.outfile + '_kinplots')
else :
    print 'Invalid analyzer ' + analyzer
    exit(0)


# loop over events
count = 0
ntotal = events.size()
print "Start looping"
for event in events:

    count = count + 1
    if count % 10000 == 0 :
        percentDone = float(count) / float(ntotal) * 100.0
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.2f} %'.format(
            count, ntotal, percentDone )


    if not options.useMC :
        eventPassed = triggerSelection.select(event)

        if not eventPassed :
            continue

    
    analyzer.analyze(event)



print 'Adieu!'
