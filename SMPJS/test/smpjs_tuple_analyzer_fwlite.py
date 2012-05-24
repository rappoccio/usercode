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
                  default='smpjs_fwlite',
                  dest='outname',
                  help='output name')

# jet collection names to use. 
parser.add_option('--collName', metavar='F', type='string', action='append',
                  default=['Trimmed', 'Filtered', 'Pruned'],
                  dest='collName',
                  help='RECO collection name')


# Use MC information, otherwise use trigger information
parser.add_option('--useMC', action='store_true',
                  default=True,
                  dest='useMC',
                  help='Use MC Weight (True) or weight by trigger prescale (False)')


# JEC systematics
parser.add_option('--jecUnc', type='int', action='store',
                  default=None,
                  dest='jecUnc',
                  help='Jet energy correction uncertainty: 1 for up, -1 for down, None for nominal')



# JER systematics
parser.add_option('--jerSmearVal', type='float', action='store',
                  default=0.1,
                  dest='jerSmearVal',
                  help='Jet energy resolution smearing value. Set to : 0.0, 0.1, 0.2')

# JAR systematics
parser.add_option('--jarSmearVal', type='float', action='store',
                  default=0.1,
                  dest='jarSmearVal',
                  help='Jet angular resolution smearing value. Set to : 0.0, 0.1, 0.2')


# PU Weighting
parser.add_option('--puWeighting', type='int', action='store',
                  default=0,
                  dest='puWeighting',
                  help='PU Weighting. None=no weighting, 0=Nominal, -1=Down, +1=Up')

parser.add_option('--puMCFile', metavar='F', type='string', action='store',
                  default='PUMC_dist.root',
                  dest='puMCFile',
                  help='PU Monte Carlo file')

parser.add_option('--puDataFile', metavar='F', type='string', action='store',
                  default='PUData_dist.root',
                  dest='puDataFile',
                  help='PU Data file')


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


if not options.useMC :
    print 'This macro is for MC only now! Please use the smpjs_tuple_analyzer_fwlite_data.py for data.'
    exit(0)

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


if options.useMC :
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
if options.jecUnc is not None:
    jecUnc = ROOT.JetCorrectionUncertainty( jecUncStr )
    upOrDown = options.jecUnc > 0.0
else :
    jecUnc = None
    upOrDown = None

if options.puWeighting is not None:
    if options.puWeighting == 0 :
        LumiWeights = ROOT.edm.Lumi3DReWeighting(options.puMCFile, options.puDataFile,
                                                 "pileup", "pileup", "Weight_3D.root")
        LumiWeights.weight3D_init( 1.08 )

    elif options.puWeighting > 0:
        LumiWeights = ROOT.edm.Lumi3DReWeighting(options.puMCFile, options.puDataFile,
                                                 "pileup", "pileup", "Weight_3D_up.root")
        LumiWeights.weight3D_init( 1.16 )

    elif options.puWeighting < 0:
        LumiWeights = ROOT.edm.Lumi3DReWeighting(options.puMCFile, options.puDataFile,
                                                 "pileup", "pileup", "Weight_3D_down.root")
        LumiWeights.weight3D_init( 1.00 )

trigsToKeep = trigHelper.trigsToKeep

############################################
# Collection names, etc #
############################################

# Ungroomed collection.
#   Used for trigger matching, and used as
#   primary "key". GenJets and GroomedJets matched from
#   these.


# List of reco jets
ak7Objs = [PyFWLiteJetColl( 'ak7Lite', jec=jec, jecUnc=jecUnc, upOrDown=upOrDown, jerSmear=options.jerSmearVal, jarSmear=options.jarSmearVal )]
for igroom in options.collName :
    ak7Objs.append( PyFWLiteJetColl( 'ak7' + igroom + 'Lite', jec=jec, jecUnc=jecUnc, upOrDown=upOrDown, jerSmear=options.jerSmearVal, jarSmear=options.jarSmearVal) )
    
# List of gen Jets
ak7GenObjs = [PyFWLiteJetColl( 'ak7Gen', useGen=True )]
for igroom in options.collName :
    ak7GenObjs.append( PyFWLiteJetColl('ak7' + igroom + 'GenLite', useGen=True) )


# Mean-pt-per-unit-area
rhoHandle = Handle("double")
rhoLabel = ( "kt6PFJets", "rho")

# Pileup information
puHandle = Handle("std::vector<PileupSummaryInfo>")
puLabel = ( "addPileupInfo", "")

# Generator information
generatorHandle = Handle("GenEventInfoProduct")
generatorLabel = ( "generator", "")


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

############## Versus EtaMax ##############

# Mjj and <Mjet> versus |eta_max|. Either data or MC. #
hists = HistsGroomed(options.outname, options.collName)

hists.book2F('histAK7MjjVsEtaMax',
             'AK7 m_{jj} Versus #eta_{max};m_{jj} (GeV);#eta_{max}(radians)',
             nx=70, x1=0., x2=7000., ny=5, y1=0.0, y2=2.5)
hists.book2F('histAK7MjetVsEtaMax',
             'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV);#eta_{max}(radians)',
             nx=60, x1=0., x2=300., ny=5, y1=0.0, y2=2.5)



# GENERATED Mjj and <Mjet> versus |eta_max|. only for MC.
hists.book2F('histAK7MjjGenVsEtaMax',
             'AK7 m_{jj}^{GEN} Versus #eta_{max};m_{jj}^{GEN} (GeV);#eta_{max}(radians)',
             nx=70, x1=0., x2=7000., ny=5, y1=0.0, y2=2.5)
hists.book2F('histAK7MjetGenVsEtaMax',
             'AK7 m_{jet}^{GEN} Versus #eta_{max};m_{jj}^{GEN} (GeV);#eta_{max}(radians)',
             nx=60, x1=0., x2=300., ny=5, y1=0.0, y2=2.5)


# Mjj and <Mjet> versus GENERATED Mjj and <Mjet>. Only for MC. 
hists.book3F('histAK7MjjGenVsRecoVsEtaMax', 'AK7 m_{jj} Response Matrix;m_{jj}^{GEN} (GeV);m_{jj}^{RECO} (GeV);#eta_{max} (radians)',
              nx=70, x1=0., x2=7000., ny=70, y1=0., y2=7000., nz=5, z1=0., z2=2.5)
hists.book3F('histAK7MjetGenVsRecoVsEtaMax', 'AK7 <m_{jet}> Response Matrix ;<m_{jet}>^{GEN} (GeV);<m_{jet}>^{RECO} (GeV);#eta_{max} (radians)',
              nx=60, x1=0., x2=300., ny=60, y1=0., y2=300., nz=5, z1=0., z2=2.5)

# Mjj and <Mjet> versus GENERATED Mjj and <Mjet>. Only for MC. 
hists.book3F('histAK7MjjResponseVsEtaMax', 'AK7 m_{jj} Response;m_{jj} (GeV);#eta_{max}(radians)',
             nx=70, x1=0., x2=7000., ny=80, y1=0.8, y2=1.2, nz=5, z1=0.0, z2=2.5)
hists.book3F('histAK7MjetResponseVsEtaMax', 'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV);#eta_{max}(radians)',
             nx=60, x1=0., x2=300., ny=20, y1=0.0, y2=2.0, nz=5, z1=0.0, z2=2.5)


############## Versus PtAvg ##############

ptBins = array('d', [0., 50.,125.,200., 300., 400., 500., 600., 800., 1000., 1500., 7000.])

    
# Mjj and <Mjet> versus ptAvg. Either data or MC. #
hists.book2F('histAK7MjjVsPtAvg',
             'AK7 m_{jj} Versus p_{T}^{AVG} ;m_{jj} (GeV);p_{T}^{AVG} (GeV)',
             nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
hists.book2F('histAK7MjetVsPtAvg',
             'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV);p_{T}^{AVG} (GeV)',
             nx=60, x1=0., x2=300., ny=len(ptBins)-1, ybins=ptBins)


# GENERATED Mjj and <Mjet> versus ptAvg. only for MC.
hists.book2F('histAK7MjjGenVsPtAvg',
             'AK7 m_{jj}^{GEN} Versus p_{T}^{AVG} ;m_{jj}^{GEN} (GeV);p_{T}^{AVG} (GeV)',
             nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
hists.book2F('histAK7MjetGenVsPtAvg',
               'AK7 m_{jet}^{GEN} Versus p_{T}^{AVG} ;m_{jj}^{GEN} (GeV);p_{T}^{AVG} (GeV)',
               nx=60, x1=0., x2=300., ny=len(ptBins)-1, ybins=ptBins)


# Mjj and <Mjet> versus GENERATED Mjj and <Mjet>. Only for MC.
hists.book3F('histAK7MjjGenVsRecoVsPtAvg', 'AK7 m_{jj} Response Matrix;m_{jj}^{GEN} (GeV);m_{jj}^{RECO} (GeV);p_{T}^{AVG} (GeV)',
              nx=70, x1=0., x2=7000., ny=70, y1=0., y2=7000., nz=8, z1=0., z2=200.)
hists.book3F('histAK7MjetGenVsRecoVsPtAvg', 'AK7 <m_{jet}> Response Matrix ;<m_{jet}>^{GEN} (GeV);<m_{jet}>^{RECO} (GeV);p_{T}^{AVG} (GeV)',
              nx=60, x1=0., x2=300., ny=60, y1=0., y2=300., nz=8, z1=0., z2=200.)

# Same as above, but TH3 in root doesn't play nicely with variable bin widths. grrrrr...
hists.book3F('histAK7MjjGenVsRecoVsPtAvgHighPt', 'AK7 m_{jj} Response Matrix;m_{jj}^{GEN} (GeV);m_{jj}^{RECO} (GeV);p_{T}^{AVG} (GeV)',
              nx=70, x1=0., x2=7000., ny=70, y1=0., y2=7000., nz=14, z1=200., z2=1600.)
hists.book3F('histAK7MjetGenVsRecoVsPtAvgHighPt', 'AK7 <m_{jet}> Response Matrix ;<m_{jet}>^{GEN} (GeV);<m_{jet}>^{RECO} (GeV);p_{T}^{AVG} (GeV)',
              nx=60, x1=0., x2=300., ny=60, y1=0., y2=300., nz=14, z1=200., z2=1600.)


# Mjj and <Mjet> versus GENERATED/RECO Mjj and <Mjet>. Only for MC. 
hists.book3F('histAK7MjjResponseVsPtAvg', 'AK7 m_{jj} Response;m_{jj} (GeV);p_{T}^{AVG} (GeV)',
              nx=70, x1=0., x2=7000., ny=80, y1=0.8, y2=1.2, nz=10, z1=0., z2=1000.)
hists.book3F('histAK7MjetResponseVsPtAvg', 'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV);p_{T}^{AVG} (GeV)',
              nx=60, x1=0., x2=300., ny=20, y1=0.0, y2=2.0, nz=10, z1=0., z2=1000.)

############## Responses ##############


# Pt and eta response. Only for MC
hists.book2F('histAK7PtResponse',  ';p_{T}^{GEN} (GeV);p_{T}^{RECO} / p_{T}^{GEN}', nx=50, x1=0., x2=500., ny=20, y1=0.5, y2=1.5)
hists.book2F('histAK7EtaResponse', ';#eta^{GEN} (GeV);p_{T}^{RECO} / p_{T}^{GEN}', nx=50, x1=-5.0, x2=5.0, ny=20, y1=0.5, y2=1.5)

hists.book1F('recoEffNum', 'reco efficiency numerator;p_{T}^{GEN} (GeV)', nx=60, x1=0., x2=300.)
hists.book1F('recoEffDen', 'reco efficiency denominator;p_{T}^{GEN} (GeV)', nx=60, x1=0., x2=300.)
hists.book1F('genEffNum', 'gen efficiency numerator;p_{T}^{RECO} (GeV)', nx=60, x1=0., x2=300.)
hists.book1F('genEffDen', 'gen efficiency denominator;p_{T}^{RECO} (GeV)', nx=60, x1=0., x2=300.)


mjjPtCut = 50.0
mjjEtaCut = 2.0

## for ibin in xrange(len(ptBins)-1) :
##     resp = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
##     resp.SetName( 'response' + str(ibin))
##     responses.append(resp)

responses = []

for ibin in range(0,len(ptBins)-1) :
    res = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
    res.SetName('response_pt' + str(ibin))
    response = [res]
    for igroom in range(0,len(options.collName)):
        res = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
        res.SetName('response_' + options.collName[igroom] + '_pt' + str(ibin) )
        response.append( res )
    responses.append(response)

hists.makeQuickHists()

#############################################
#               Event loop                  #
#    Loop over events.                      #
#    For each event:                        #
#        1. Get the gen jets for all types  #
#        2. Get the reco jets for all types #
#        3. Fill response matrix            #
#        4. Get mjj, etaMax bin, and weight #
#        5. Fake the trigger                #
#        6. If it passes, fill the histos   #
#############################################
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



        # If using PU reweighting, get the number of simulated pileup interactions
        if options.puWeighting is not None:
            weight *= LumiWeights.weight3D( event.object() )

        #------------------------------------------
        # Now get the event weight.
        #   - Weight by the generator weight (cross section for this event)
        #------------------------------------------
        passGen = False
        # Get the generator product
        event.getByLabel( generatorLabel, generatorHandle )
        if generatorHandle.isValid() :
            generatorInfo = generatorHandle.product()
            # weight is the generator weight
            weight *= generatorInfo.weight()
            passGen = True


        if options.verbose :
            print 'event weight = ' + str(weight)
                

        # Get mean-pt-per-unit-area
        event.getByLabel( rhoLabel, rhoHandle )
        rho = rhoHandle.product()[0]

        # Get the gen jets for each grooming algorithm (ungroomed is position 0)
        ak7Gens = []
        for igen in xrange(len(ak7GenObjs)) :
            ak7Gens.append(ak7GenObjs[igen].getJets(event))
            
        # Get the reco jets for each grooming algorithm (ungroomed is position 0).
        # Also match the reco jets to the ungroomed reco jets (at position 0). 
        ak7Recos = [ak7Objs[0].getJets( event, rho=rho, genToMatch=ak7Gens[0] )]
        for igroom in range(1,len(ak7Objs)) :
            ak7Recos.append( ak7Objs[igroom].getJets(event, rho=rho,genToMatch=ak7Gens[igroom],recoToMatch=ak7Recos[0]) )


        if options.verbose:
            print 'Gen jets'
            for igen in xrange(len(ak7GenObjs)) :
                print 'igen = ' + str(igen)
                ak7GenObjs[igen].printJetColl()
            print 'Reco jets'
            for ireco in xrange(len(ak7Objs)) :
                print 'ireco = ' + str(ireco)
                ak7Objs[ireco].printJetColl()


        # Now looop over the grooming algorithms,
        # fill the response matrix, fake the trigger,
        # and fill the histograms.
        mjjForTrig = None
        for igroom in range(0,len(ak7Objs)):
            ak7GenObj = ak7GenObjs[igroom]  # object for gen
            ak7Obj = ak7Objs[igroom]        # object for reco
            ak7Gen = ak7Gens[igroom]        # 4-vector coll for gen
            ak7Reco = ak7Recos[igroom]      # 4-vector coll for reco

            ak7GenIndices = ak7Obj.getMatchedGenIndices()   # List of indices for matched gen jets
            ak7GenMatched = ak7Obj.getMatchedGen()          # List of 4-vectors for matched gen jets

            # check to see that the leading two reco jets match the leading two gen jets.
            # If not, it's a miss (gen, no reco), or a fake (reco, no gen)
            isMiss = False
            isFake = False

            # Here's the ptAvg, mjj, and mjet to use. Depending on whether this is
            # a miss, a fake, or a match, these mean slightly different things.
            ptAvg = None
            mjj = None
            mjet = None
            responsePtBin = None

            # First check miss: values set to gen-only
            if len(ak7Reco) < 2 and len(ak7Gen) >= 2:
                isMiss = True
                ptAvg = (ak7Gen[0].Perp() + ak7Gen[1].Perp()) * 0.5
                mjj = (ak7Gen[0] + ak7Gen[1]).M()
                mjet = (ak7Gen[0].M() + ak7Gen[1].M()) * 0.5
                responsePtBin = findBin( ptAvg, ptBins )
                if responsePtBin is None :
                    continue
                response = responses[responsePtBin][igroom]
                response.Miss( mjet )

            # Next check fake: values set to reco
            # Fake condition is if the leading two reco jets do not match
            # to the leading two gen jets
            fake0Condition = len(ak7GenMatched) < 2
            fake1Condition = len(ak7GenMatched) >= 2 and (ak7GenMatched[0] is None or ak7GenMatched[1] is None)
            if len(ak7Reco) >= 2 and (fake0Condition or fake1Condition) :
                isFake = True
                ptAvg = (ak7Reco[0].Perp() + ak7Reco[1].Perp()) * 0.5
                mjj = (ak7Reco[0] + ak7Reco[1]).M()
                mjet = (ak7Reco[0].M() + ak7Reco[1].M()) * 0.5
                responsePtBin = findBin( ptAvg, ptBins )
                if responsePtBin is None :
                    continue
                response = responses[responsePtBin][igroom]
                response.Fake( mjet )

            # Skip events which have misses or fakes
            if isMiss or isFake :
                continue

            # Finally, we have a "match" where there are two
            # reco jets and two gen jets. We fill the response
            # matrix, and the rest of the plots.
            if len(ak7Reco) >= 2 and len(ak7GenMatched) >= 2 :
                ptAvg = (ak7Reco[0].Perp() + ak7Reco[1].Perp()) * 0.5
                mjj = (ak7Reco[0] + ak7Reco[1]).M()
                mjet = (ak7Reco[0].M() + ak7Reco[1].M()) * 0.5
                responsePtBin = findBin( ptAvg, ptBins )
                if responsePtBin is None :
                    continue
                ptAvgGen = (ak7GenMatched[0].Perp() + ak7GenMatched[1].Perp()) * 0.5
                mjjGen = (ak7GenMatched[0] + ak7GenMatched[1]).M()
                mjetGen = (ak7GenMatched[0].M() + ak7GenMatched[1].M()) * 0.5

                response = responses[responsePtBin][igroom]
                response.Fill( mjet, mjetGen )

                etaMax = ak7Reco[0].Rapidity()
                if abs(ak7Reco[0].Rapidity()) < abs(ak7Reco[1].Rapidity()) :
                    etaMax = abs(ak7Reco[1].Rapidity())


                #------------------------------------------
                # Now fake the trigger
                #------------------------------------------
                if igroom == 0 :
                    mjjForTrig = mjj
                passTrig = trigHelper.passEventMC( event, mjjForTrig, etaMax ) 

                #------------------------------------------
                # To pass the event, the faked trigger and the gen product
                # must both pass.
                #------------------------------------------
                passEvent = passTrig and passGen
                if not passEvent :
                    continue


                #------------------------------------------
                # Finally fill histograms.
                #------------------------------------------
                response0 = ak7Reco[0].Perp() / ak7GenMatched[0].Perp()
                mjjResponse = mjj / mjjGen
                mjetResponse = mjet / mjetGen
                ptGen0 = ak7GenMatched[0].Perp()
                etaGen0 = ak7GenMatched[0].Rapidity()


                if igroom == 0 :
                    hists.histAK7MjjVsEtaMax.Fill( mjj, etaMax, weight )
                    hists.histAK7MjetVsEtaMax.Fill( mjet, etaMax, weight )
                    hists.histAK7MjjVsPtAvg.Fill( mjj, ptAvg, weight )
                    hists.histAK7MjetVsPtAvg.Fill( mjet, ptAvg, weight )
                    hists.histAK7PtResponse.Fill( ptGen0, response0 )
                    hists.histAK7EtaResponse.Fill( etaGen0, response0 )

                    hists.histAK7MjjResponseVsEtaMax.Fill( mjjGen, mjjResponse, etaMax )
                    hists.histAK7MjetResponseVsEtaMax.Fill( mjetGen, mjetResponse, etaMax )
                    hists.histAK7MjjGenVsEtaMax.Fill( mjjGen, etaMax, weight )
                    hists.histAK7MjetGenVsEtaMax.Fill( mjetGen, etaMax, weight )
                    hists.histAK7MjjGenVsRecoVsEtaMax.Fill( mjjGen, mjj, etaMax )
                    hists.histAK7MjetGenVsRecoVsEtaMax.Fill( mjetGen, mjet, etaMax )

                    hists.histAK7MjjResponseVsPtAvg.Fill( mjjGen, mjjResponse, ptAvg )
                    hists.histAK7MjetResponseVsPtAvg.Fill( mjetGen, mjetResponse, ptAvg )
                    hists.histAK7MjjGenVsRecoVsPtAvg.Fill( mjjGen, mjj, ptAvg )
                    hists.histAK7MjetGenVsRecoVsPtAvg.Fill( mjetGen, mjet, ptAvg )
                    hists.histAK7MjjGenVsRecoVsPtAvgHighPt.Fill( mjjGen, mjj, ptAvg )
                    hists.histAK7MjetGenVsRecoVsPtAvgHighPt.Fill( mjetGen, mjet, ptAvg )
                    hists.histAK7MjjGenVsPtAvg.Fill( mjjGen, ptAvg, weight )
                    hists.histAK7MjetGenVsPtAvg.Fill( mjetGen, ptAvg, weight )

                else :
                    # NOTE: The hists fill the _Groom vector only for groomed jets,
                    # whereas we're counting the ungroomed above as "igroom=0", so
                    # we offset the hists _Groom vector by 1. 
                    hists.histAK7MjjVsEtaMax_Groom[igroom-1].Fill( mjj, etaMax, weight )
                    hists.histAK7MjetVsEtaMax_Groom[igroom-1].Fill( mjet, etaMax, weight )
                    hists.histAK7MjjVsPtAvg_Groom[igroom-1].Fill( mjj, ptAvg, weight )
                    hists.histAK7MjetVsPtAvg_Groom[igroom-1].Fill( mjet, ptAvg, weight )
                    hists.histAK7PtResponse_Groom[igroom-1].Fill( ptGen0, response0 )
                    hists.histAK7EtaResponse_Groom[igroom-1].Fill( etaGen0, response0 )

                    hists.histAK7MjjResponseVsEtaMax_Groom[igroom-1].Fill( mjjGen, mjjResponse, etaMax )
                    hists.histAK7MjetResponseVsEtaMax_Groom[igroom-1].Fill( mjetGen, mjetResponse, etaMax )
                    hists.histAK7MjjGenVsEtaMax_Groom[igroom-1].Fill( mjjGen, etaMax, weight )
                    hists.histAK7MjetGenVsEtaMax_Groom[igroom-1].Fill( mjetGen, etaMax, weight )
                    hists.histAK7MjjGenVsRecoVsEtaMax_Groom[igroom-1].Fill( mjjGen, mjj, etaMax )
                    hists.histAK7MjetGenVsRecoVsEtaMax_Groom[igroom-1].Fill( mjetGen, mjet, etaMax )

                    hists.histAK7MjjResponseVsPtAvg_Groom[igroom-1].Fill( mjjGen, mjjResponse, ptAvg )
                    hists.histAK7MjetResponseVsPtAvg_Groom[igroom-1].Fill( mjetGen, mjetResponse, ptAvg )
                    hists.histAK7MjjGenVsRecoVsPtAvg_Groom[igroom-1].Fill( mjjGen, mjj, ptAvg )
                    hists.histAK7MjetGenVsRecoVsPtAvg_Groom[igroom-1].Fill( mjetGen, mjet, ptAvg )
                    hists.histAK7MjjGenVsRecoVsPtAvgHighPt_Groom[igroom-1].Fill( mjjGen, mjj, ptAvg )
                    hists.histAK7MjetGenVsRecoVsPtAvgHighPt_Groom[igroom-1].Fill( mjetGen, mjet, ptAvg )
                    hists.histAK7MjjGenVsPtAvg_Groom[igroom-1].Fill( mjjGen, ptAvg, weight )
                    hists.histAK7MjetGenVsPtAvg_Groom[igroom-1].Fill( mjetGen, ptAvg, weight )
        
hists.getFile().cd()
for response in responses :
    for groomResponse in response :
        groomResponse.Write()
    
hists.write()

