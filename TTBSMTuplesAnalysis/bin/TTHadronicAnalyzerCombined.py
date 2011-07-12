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
from Analysis.TTBSMTuplesAnalysis.Type11Analyzer import Type11Analyzer
from Analysis.TTBSMTuplesAnalysis.MistagMakerType1 import MistagMakerType1
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

parser.add_option('--veto11', action='store_true',
                  default=False,
                  dest='veto11',
                  help='Veto the type 1+1 selection in the type 1+2 selection')


parser.add_option('-m', '--mistagFile', metavar='N', type='string', action='store',
                  default='MISTAG',
                  dest='mistagFile',
                  help='mistag file')

parser.add_option('-l', '--collectionLabelSuffix', metavar='N', type='string', action='store',
                  default='',
                  dest='collectionLabelSuffix',
                  help='Collection label')



(options, args) = parser.parse_args()

files = glob.glob( options.dirs + "*.root" )
print files




events = Events (files)


myAnaTrigs = [
     7#    'HLT_Jet240_v1',
   ,14#    'HLT_Jet300_v1',
   ,15#    'HLT_Jet300_v2',
   ,16#    'HLT_Jet300_v3',
   ,17#    'HLT_Jet300_v4',
   ,18#    'HLT_Jet300_v5',
   ,19#    'HLT_Jet300_v6',
   ,20#    'HLT_Jet300_v7',
   ,21#    'HLT_Jet370_v1',
   ,22#    'HLT_Jet370_v2',
   ,23#    'HLT_Jet370_v3',
   ,24#    'HLT_Jet370_v4',
   ,25#    'HLT_Jet370_v5',
   ,26#    'HLT_Jet370_v6',
   ,27#    'HLT_Jet370_v7'
    ]

triggerSelection = TriggerAndEventSelectionObject( myAnaTrigs )


if options.analyzer == "Type12Analyzer" :
    analyzer = Type12Analyzer(options.useMC, options.outfile + '_type12_'+options.collectionLabelSuffix,
                              options.mistagFile, options.collectionLabelSuffix,
                              options.veto11 )
elif options.analyzer == "MistagMaker" :
    analyzer = MistagMaker( options.outfile + '_mistag')
elif options.analyzer == "Type11Analyzer" :
    analyzer = Type11Analyzer(options.useMC, options.outfile + '_type11_'+options.collectionLabelSuffix, options.mistagFile, options.collectionLabelSuffix)
elif options.analyzer == "MistagMakerType1" :
    analyzer = MistagMakerType1( options.outfile + '_mistag1')
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
