#! /usr/bin/env python
import os
import glob
import math
from array import *

from optparse import OptionParser

parser = OptionParser()


############################################
#            Job steering                  #
############################################

# Input files to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
parser.add_option('--files', metavar='F', type='string', action='store',
		  dest='files',
                  help='Input files')

# Output name to use. 
parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='smpjs_fwlite_dijettriggerana',
                  dest='outname',
                  help='output name')

# jet collection names to use. 
parser.add_option('--collName', metavar='F', type='string', action='append',
                  default=['Trimmed', 'Filtered', 'Pruned'],
                  dest='collName',
                  help='RECO collection name')



# Print verbose information
parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print verbose information')

# job splitting

parser.add_option('--max', type='int', action='store',
                  default=None,
                  dest='max',
                  help='Max number')
parser.add_option('--nsplit', type='int', action='store',
                  default=None,
                  dest='nsplit',
                  help='Number of split jobs')
parser.add_option('--isplit', type='int', action='store',
                  default=None,
                  dest='isplit',
		  help='Index of job (0...nsplit)')

(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

ROOT.gSystem.Load('libCondFormatsJetMETObjects')
ROOT.gSystem.Load('libPhysicsToolsUtilities')

from PyFWLiteJetColl import PyFWLiteJetColl, printRawColl
from HistsGroomed import HistsGroomed
from TrigHelper import TrigHelper

trigHelper = TrigHelper()



#############################
# Utility for finding bin
#############################
def findBin( x, bins ) :
    for ibin in xrange(len(bins) - 1) :
        if x >= bins[ibin] and x < bins[ibin+1] :
            return ibin
    return None

#############################
# Get the input files,
# and split them to increase
# processing speed. 
#############################

print 'Getting files from this dir: ' + options.files

files = []
# Get the file list.
if options.files.find('.txt') >= 0 :
    infile = open( options.files, 'r')
    tmpfiles = infile.readlines()
    for ifile in tmpfiles :
        s = ifile.rstrip()
        print s
        files.append( s )

elif options.nsplit is None :
    files = glob.glob( options.files )
    for ifile in files:
        print ifile
elif options.nsplit is not None :


    tmpfiles = glob.glob( options.files )
    print 'All files : '  + str(len(tmpfiles))
    for ifile in tmpfiles :
        print ifile

    tot = len(tmpfiles)
    nsplit = options.nsplit
    isplit = options.isplit
    msplit = tot / nsplit
    print 'Splitting into ' + str(nsplit) + ' jobs with ' + str(msplit) + ' elements each, this job is index ' + str(isplit)
    end = min( tot, (isplit + 1) * msplit )
    for i in range( isplit * msplit, end ) :
        files.append( tmpfiles[i] )
    print 'Selected files : '
    for ifile in files :
        print ifile

if len(files) == 0 :
    print 'No files, exiting'
    exit(0)

# Create the output file. 
f = ROOT.TFile(options.outname + ".root", "recreate")
f.cd()


# Make histograms
print "Creating histograms"

nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )


############################################
#     Jet energy scale and uncertainties   #
############################################

useMC= False

if useMC :
    jecStr = [
        'GR_R_42_V23_L1FastJet_AK7PFchs.txt',
        'GR_R_42_V23_L2Relative_AK7PFchs.txt',
        'GR_R_42_V23_L3Absolute_AK7PFchs.txt',
    ]
else :
    jecStr = [
        'GR_R_42_V23_L1FastJet_AK7PFchs.txt',
        'GR_R_42_V23_L2Relative_AK7PFchs.txt',
        'GR_R_42_V23_L3Absolute_AK7PFchs.txt',
        'GR_R_42_V23_L2L3Residual_AK7PFchs.txt',
    ]

jecPars = ROOT.std.vector(ROOT.JetCorrectorParameters)()

for ijecStr in jecStr :
    ijec = ROOT.JetCorrectorParameters( ijecStr )
    jecPars.push_back( ijec )
    

jec = ROOT.FactorizedJetCorrector(jecPars)

jecUncStr = ROOT.std.string('GR_R_42_V23_Uncertainty_AK7PFchs.txt')
jecUnc = None
upOrDown = None


############################################
# Collection names, etc #
############################################

# Ungroomed collection.
#   Used for trigger matching, and used as
#   primary "key". GenJets and GroomedJets matched from
#   these.
ak7Obj = PyFWLiteJetColl( 'ak7Lite', jec=jec )

# List of groomed jets
ak7GroomObj = []

for igroom in options.collName :
    ak7GroomObj.append( PyFWLiteJetColl( 'ak7' + igroom + 'Lite', jec=jec ))
    
# GenJets
ak7GenObj = PyFWLiteJetColl( 'ak7Gen', useGen=True )
ak7GenGroomObj = []
for igroom in options.collName :
    ak7GenGroomObj.append( PyFWLiteJetColl('ak7' + igroom + 'GenLite', useGen=True) )


# Mean-pt-per-unit-area
rhoHandle = Handle("double")
rhoLabel = ( "kt6PFJets", "rho")

# Pileup information
puHandle = Handle("std::vector<PileupSummaryInfo>")
puLabel = ( "addPileupInfo", "")
npvHandle = Handle("double")
npvLabel = ( "pvCount", "npv")

trigLabel = ( "dijetTriggerFilter", 'jetPaths')
trigHandle = Handle("std::vector<std::string>")

trigsToKeep = [
    'HLT_Jet60_v',
    'HLT_Jet110_v',
    'HLT_Jet190_v',
    'HLT_Jet240_v',
    'HLT_Jet370_v',
    ]

histos = {None:None}
for itrig in trigsToKeep :
    hnum = ROOT.TH1F( itrig + 'Num', itrig + 'Num', 100, 0, 1000)
    histos.update( {itrig:hnum} )

############################################
#               Histograms                 #
#      For each histogram, we have the     #
#      standard collection (ungroomed),    #
#      as well as several groomed          #
#      collections. These are stored       #
#      as simple lists. The matched        #
#      groomed jets are plotted there,     #
#      but the trigger assignment is done  #
#      with the ungroomed collections.     #
############################################

mjjPtCut = 50.0
mjjEtaCut = 2.0

############################################
#               Event loop                 #
#    Loop over events.                     #
#    For each event:                       #
#        1. Get the ungroomed reco jets    #
#        2. if MC, get the gen jets        #
#        3. Correct the ungroomed reco     #
#           jets, and match to genjets.    #
#        4. Find the mjj, etaMax bins, and #
#           event weight.                  #
#        5. If the event passes that,      #
#           fill histograms for ungroomed  #
#           jets, and get the groomed jets #
#        6. For each groom, fill the histos#
############################################

count = 0

for ifile in files :

    ifiles = [ ifile ]

    events = Events (ifiles)

    print "Start looping on file " + ifiles[0]

    if options.max is not None:
        if count > options.max :
            break

    for event in events:

        if options.max is not None:
            if count > options.max :
                break

        # Histogram filling weight
        weight = 1.0

        # Histogram index for data (Jet60,110,190,240,370)
        iTrigHist = None
        
        if count % 10000 == 0 or options.verbose :
            print '-------------------------------------------------  Processing event ' + str(count) + '--------------------------------------'


        count += 1

        
        # For printing and comparison
        mjetFinal = []

        event.getByLabel( rhoLabel, rhoHandle )
        rho = rhoHandle.product()[0]
#        event.getByLabel( npvLabel, npvHandle )
#        nvtx = npvHandle.product()[0]

        # Now get the ungroomed jets
	if useMC is False :
	    ak7Def = ak7Obj.getJets( event, rho=rho )

        

        passEvent = False
        #------------------------------------------
        # Data Preprocessing: 
        #  Check if the event passed the trigger
        #------------------------------------------
        if len(ak7Def) < 2 :
            continue
        dijetCandReco = ak7Def[0]+ak7Def[1]
        ptAvg = (ak7Def[0].Perp() + ak7Def[1].Perp()) * 0.5

        event.getByLabel( trigLabel, trigHandle )
        trigs = trigHandle.product()



        for itrig in range(0,len(trigsToKeep)) :
            trig = trigsToKeep[itrig]
            found = False
            for strtrig in trigs :
                if trig == strtrig :
                    found = True
            if found :
                histos[trig].Fill( ptAvg )

f.cd()
f.Write()
f.Close()


