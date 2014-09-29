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

# jet collection names to use. 
parser.add_option('--alg', metavar='F', type='string', action='store',
                  default='ak7',
                  dest='alg',
                  help='Algorithms to plot')


# JEC systematics
parser.add_option('--jecUnc', type='int', action='store',
                  default=None,
                  dest='jecUnc',
                  help='Jet energy correction uncertainty: 1 for up, -1 for down, None for nominal')



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

if options.alg == 'ak5' :
    jecStr = [
        'Jec11_V3_L1FastJet_AK5PFchs.txt',
        'Jec11_V3_L2Relative_AK5PFchs.txt',
        'Jec11_V3_L3Absolute_AK5PFchs.txt',
        'Jec11_V3_L2L3Residual_AK5PFchs.txt'
        ]
    jecUncStr = ROOT.std.string('Jec11_V3_Uncertainty_AK5PFchs.txt')
else :
    jecStr = [
        'GR_R_42_V23_L1FastJet_AK7PFchs.txt',
        'GR_R_42_V23_L2Relative_AK7PFchs.txt',
        'GR_R_42_V23_L3Absolute_AK7PFchs.txt',
        'GR_R_42_V23_L2L3Residual_AK7PFchs.txt',
    ]
    jecUncStr = ROOT.std.string('GR_R_42_V23_Uncertainty_AK7PFchs.txt')



jecPars = ROOT.std.vector(ROOT.JetCorrectorParameters)()

for ijecStr in jecStr :
    ijec = ROOT.JetCorrectorParameters( ijecStr )
    jecPars.push_back( ijec )
    

jec = ROOT.FactorizedJetCorrector(jecPars)

if options.jecUnc is not None:
    jecUnc = ROOT.JetCorrectionUncertainty( jecUncStr )
    upOrDown = options.jecUnc > 0.0
else :
    jecUnc = None
    upOrDown = None



############################################
# Collection names, etc #
############################################

# Ungroomed collection.
#   Used for trigger matching, and used as
#   primary "key". GenJets and GroomedJets matched from
#   these.
ak7Obj = PyFWLiteJetColl( options.alg + 'Lite', jec=jec, jecUnc=jecUnc, upOrDown=upOrDown, flatUnc=None, jerSmear=None, jarSmear=None )

# List of groomed jets
ak7GroomObj = []

for igroom in options.collName :
    ak7GroomObj.append( PyFWLiteJetColl( options.alg + igroom + 'Lite', jec=jec, jecUnc=jecUnc, upOrDown=upOrDown, flatUnc=0.01, jerSmear=None, jarSmear=None) )


# Mean-pt-per-unit-area
rhoHandle = Handle("double")
rhoLabel = ( "kt6PFJets", "rho")

# Pileup information
puHandle = Handle("std::vector<PileupSummaryInfo>")
puLabel = ( "addPileupInfo", "")
npvHandle = Handle("double")
npvLabel = ( "pvCount", "npv")






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
             nx=30, x1=0., x2=300., ny=5, y1=0.0, y2=2.5)


# Mjj and <Mjet> versus |eta_max| for the different triggers. Only data. #
for trig in trigHelper.trigsToKeep :
    hists.book2F('histAK7MjjVsEtaMax_' + trig,
                 'AK7 m_{jj} Versus #eta_{max}' + trig +';m_{jj} (GeV);#eta_{max}(radians)',
                 nx=70, x1=0., x2=7000., ny=5, y1=0.0, y2=2.5)
    hists.book2F('histAK7MjetVsEtaMax_' + trig,
                 'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV)' + trig + ';#eta_{max}(radians)',
                 nx=30, x1=0., x2=300., ny=5, y1=0.0, y2=2.5)


############## Versus PtAvg ##############

ptBins = array('d', [0., 50., 125., 150., 220., 300., 450., 500., 600., 800., 1000., 1500., 7000.])
    
# Mjj and <Mjet> versus ptAvg. Either data or MC. #
hists.book2F('histAK7MjjVsPtAvg',
             'AK7 m_{jj} Versus p_{T}^{AVG} ;m_{jj} (GeV);p_{T}^{AVG} (GeV)',
             nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
hists.book2F('histAK7MjetVsPtAvg',
             'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV);p_{T}^{AVG} (GeV)',
             nx=30, x1=0., x2=300., ny=len(ptBins)-1, ybins=ptBins)

# Mjj and <Mjet> versus ptAvg for the different triggers. Only data. #
for trig in trigHelper.trigsToKeep :
    hists.book2F('histAK7MjjVsPtAvg_' + trig,
                 'AK7 m_{jj} Versus p_{T}^{AVG} ' + trig +';m_{jj} (GeV);p_{T}^{AVG} (GeV)',
                 nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
    hists.book2F('histAK7MjetVsPtAvg_' + trig,
                 'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV)' + trig + ';p_{T}^{AVG} (GeV)',
                 nx=30, x1=0., x2=300., ny=len(ptBins)-1, ybins=ptBins)

    
## # Mjj and <Mjet> versus ptAvg. Either data or MC. #
## hists.book2F('histAK7PtAvgVsNvtx',
##              'AK7 m_{jj} Versus p_{T}^{AVG} ;m_{jj} (GeV);p_{T}^{AVG} (GeV)',
##              nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
## hists.book2F('histAK7MjetVsNvtx',
##              'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV);p_{T}^{AVG} (GeV)',
##              nx=30, x1=0., x2=300., ny=len(ptBins)-1, ybins=ptBins)

## # Mjj and <Mjet> versus ptAvg for the different triggers. Only data. #
## for trig in trigHelper.trigsToKeep :
##     hists.book2F('histAK7PtAvgVsNvtx_' + trig,
##                  'AK7 m_{jj} Versus p_{T}^{AVG} ' + trig +';m_{jj} (GeV);p_{T}^{AVG} (GeV)',
##                  nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
##     hists.book2F('histAK7MjetVsNvtx_' + trig,
##                  'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV)' + trig + ';p_{T}^{AVG} (GeV)',
##                  nx=30, x1=0., x2=300., ny=len(ptBins)-1, ybins=ptBins)


############## Basic distributions ##############
hists.book1F('histAK7DeltaPhi',  ';#Delta #phi', nx=25,x1=0,x2=ROOT.TMath.Pi())
hists.book1F('histAK7DeltaY',    ';#Delta y', nx=25,x1=0,x2=ROOT.TMath.Pi()*2.0)

hists.book2F('histAK7PtAvgVsNvtx',  ';N_{VTX};p_{T}^{RECO} (GeV)',   nx=25,x1=0,x2=25, ny=280, y1=0, y2=7000)
hists.book2F('histAK7MjetVsNvtx',   ';N_{VTX};m_{jet}^{RECO} (GeV)', nx=25,x1=0,x2=25, ny=30, y1=0, y2=300)
hists.book2F('histAK7PtAvgVsMjetGroomOverReco',   ';m_{jet}^{GROOM}/m_{jet}^{RECO};p_{T}^{AVG}', nx=51,x1=0.0,x2=1.02, ny=len(ptBins)-1, ybins=ptBins)

# Mjj and <Mjet> versus ptAvg for the different triggers. Only data. #
for trig in trigHelper.trigsToKeep :
    hists.book1F('histAK7DeltaPhi_' + trig,  trig + ';#Delta #phi', nx=25,x1=0,x2=ROOT.TMath.Pi())
    hists.book1F('histAK7DeltaY_' + trig,    trig + ';#Delta y', nx=25,x1=0,x2=ROOT.TMath.Pi())
    hists.book2F('histAK7PtAvgVsNvtx_' + trig,
                 trig +';N_{VTX};p_{T}^{RECO} (GeV)',
                 nx=25,x1=0,x2=25, ny=280, y1=0, y2=7000)
    hists.book2F('histAK7MjetVsNvtx_' + trig,
                 trig +';N_{VTX};p_{T}^{RECO} (GeV)',
                 nx=25,x1=0,x2=25, ny=30, y1=0, y2=300)
    hists.book2F('histAK7PtAvgVsMjetGroomOverReco_' + trig,
                 trig +';m_{jet}^{GROOM}/m_{jet}^{RECO};p_{T}^{AVG}',
                 nx=51,x1=0.0,x2=1.02, ny=len(ptBins)-1, ybins=ptBins)


mjjPtCut = 50.0
mjjEtaCut = 2.0

hists.makeQuickHists()

############################################
#               Event loop                 #
#    Loop over events.                     #
#    For each event:                       #
#        1. Get the ungroomed reco jets    #
#        2. Use the ungroomed jets to find #
#           the trigger bin                #
#        3. Get the groomed jets.          # 
#        4. Make plots.                    #
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
        event.getByLabel( npvLabel, npvHandle )
        nvtx = npvHandle.product()[0]

        # Now get the ungroomed jets
        ak7Def = ak7Obj.getJets( event, rho=rho )

        
        mjjReco = None
	if options.verbose :
	    print 'Jet collection for AK7 jets: '
	    ak7Obj.printJetColl()



        passEvent = False
        #------------------------------------------
        # Data Preprocessing: 
        #  Check if the event passed the trigger
        #------------------------------------------
        if len(ak7Def) < 2 :
            continue
        dijetCandReco = ak7Def[0]+ak7Def[1]

        mjjReco = dijetCandReco.M()
        etaMax = abs(ak7Def[0].Rapidity())
        if abs(ak7Def[0].Rapidity()) < abs(ak7Def[1].Rapidity()) :
            etaMax = abs(ak7Def[1].Rapidity())

        mjetReco = (ak7Def[0].M() + ak7Def[1].M()) * 0.5
        ptAvg = (ak7Def[0].Perp() + ak7Def[1].Perp()) * 0.5
        mjetFinal.append(mjetReco)

        deltaPhi = abs(ak7Def[0].DeltaPhi( ak7Def[1] ))
        deltaY = abs(ak7Def[0].Rapidity() - ak7Def[1].Rapidity())


        [passEvent,iTrigHist] = trigHelper.passEventData(event, ptAvg )

        if not passEvent :
            continue


        # Here we have two reconstructed jets. Get the
        # average jet mass, dijet mass, etaMax, average pt,
        # and trigger bin



        if options.verbose :
            print 'mjjReco = ' + str(mjjReco) + ', etaMax = ' + str(etaMax)


        if options.verbose :
            print 'event passed! OH happy day!'
            print 'Filling mjjReco = ' + str(mjjReco) + ', mjetReco = ' + str(mjetReco) + ', etaMax = ' + str(etaMax) + ', weight = ' + str(weight)

        hists.histAK7MjjVsEtaMax.Fill( mjjReco, etaMax, weight )
        hists.histAK7MjetVsEtaMax.Fill( mjetReco, etaMax, weight )

        hists.histAK7MjjVsPtAvg.Fill( mjjReco, ptAvg, weight )
        hists.histAK7MjetVsPtAvg.Fill( mjetReco, ptAvg, weight )

        hists.histAK7PtAvgVsNvtx.Fill( nvtx, ptAvg, weight )
        hists.histAK7MjetVsNvtx.Fill( nvtx, mjetReco, weight )
        hists.histAK7PtAvgVsMjetGroomOverReco.Fill( 1.0, ptAvg, weight )

        if iTrigHist is not None :
            if options.verbose :
                print ' Filling histogram ' + str(iTrigHist) + ' which corresponds to trigger ' + trigHelper.trigsToKeep[iTrigHist]
            hists.get('histAK7MjjVsEtaMax_' + trigHelper.trigsToKeep[iTrigHist]).Fill( mjjReco, etaMax, weight )
            hists.get('histAK7MjetVsEtaMax_' + trigHelper.trigsToKeep[iTrigHist]).Fill( mjetReco, etaMax, weight )                
            hists.get('histAK7MjjVsPtAvg_' + trigHelper.trigsToKeep[iTrigHist]).Fill( mjjReco, ptAvg, weight )
            hists.get('histAK7MjetVsPtAvg_' + trigHelper.trigsToKeep[iTrigHist]).Fill( mjetReco, ptAvg, weight )
            hists.get('histAK7DeltaPhi_' + trigHelper.trigsToKeep[iTrigHist]).Fill( deltaPhi, weight )
            hists.get('histAK7DeltaY_' + trigHelper.trigsToKeep[iTrigHist]).Fill( deltaY, weight )
            hists.get('histAK7PtAvgVsNvtx_' + trigHelper.trigsToKeep[iTrigHist]).Fill( nvtx, ptAvg, weight )
            hists.get('histAK7MjetVsNvtx_' + trigHelper.trigsToKeep[iTrigHist]).Fill( nvtx, mjetReco, weight )
            hists.get('histAK7PtAvgVsMjetGroomOverReco_' + trigHelper.trigsToKeep[iTrigHist]).Fill( 1.0, ptAvg, weight )


        else :
            print 'Error in trigger assignment!'
            continue





        for igroom in range(0,len(ak7GroomObj)):
            if options.verbose :
                print '--------- groom ' + options.collName[igroom]

            ak7Groom = ak7GroomObj[igroom].getJets( event, rho=rho, recoToMatch=ak7Def )

            if len(ak7Groom) < 2 :
                continue
            
            ptAvgGroom = (ak7Groom[0].Perp() + ak7Groom[1].Perp()) * 0.5
            dijetCandRecoGroom = ak7Groom[0] + ak7Groom[1]
            mjetRecoGroom = (ak7Groom[0].M() + ak7Groom[1].M()) * 0.5
            mjjRecoGroom = dijetCandRecoGroom.M()
            mjetGroomOverMjet = mjetRecoGroom / mjetReco

            deltaPhiGroom = abs(ak7Groom[0].DeltaPhi( ak7Groom[1] ))
            deltaYGroom = abs(ak7Groom[0].Rapidity() - ak7Groom[1].Rapidity())


            mjetFinal.append( mjetRecoGroom )
            if options.verbose :
                print 'Groomed jets'
                ak7GroomObj[igroom].printJetColl( )
                print 'Filling mjjRecoGroom = ' + str(mjjRecoGroom) + ', mjetRecoGroom = ' + str(mjetRecoGroom)
                print 'Filling mjjReco      = ' + str(mjjReco)      + ', mjetReco      = ' + str(mjetReco) + ', ratio = ' + str(mjetGroomOverMjet)

            hists.histAK7MjjVsEtaMax_Groom[igroom].Fill( mjjRecoGroom , etaMax, weight)
            hists.histAK7MjetVsEtaMax_Groom[igroom].Fill(mjetRecoGroom , etaMax, weight )

            hists.histAK7MjjVsPtAvg_Groom[igroom].Fill( mjjRecoGroom , ptAvgGroom, weight)
            hists.histAK7MjetVsPtAvg_Groom[igroom].Fill(mjetRecoGroom , ptAvgGroom, weight )
            
            hists.histAK7PtAvgVsNvtx_Groom[igroom-1].Fill( nvtx, ptAvgGroom, weight )
            hists.histAK7MjetVsNvtx_Groom[igroom-1].Fill( nvtx, mjetRecoGroom, weight )
            hists.histAK7PtAvgVsMjetGroomOverReco_Groom[igroom-1].Fill( mjetGroomOverMjet, ptAvgGroom, weight )


            if iTrigHist is not None :
                if options.verbose :
                    print ' Filling histogram ' + str(iTrigHist) + ' which corresponds to trigger ' + trigHelper.trigsToKeep[iTrigHist]
                hists.get('histAK7MjjVsEtaMax_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjjRecoGroom, etaMax, weight )
                hists.get('histAK7MjetVsEtaMax_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjetRecoGroom, etaMax, weight )                
                hists.get('histAK7MjjVsPtAvg_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjjRecoGroom, ptAvgGroom, weight )
                hists.get('histAK7MjetVsPtAvg_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjetRecoGroom, ptAvgGroom, weight )
                hists.get('histAK7DeltaPhi_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( deltaPhiGroom, weight )
                hists.get('histAK7DeltaY_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( deltaYGroom, weight )
                hists.get('histAK7PtAvgVsNvtx_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( nvtx, ptAvgGroom, weight )
                hists.get('histAK7MjetVsNvtx_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( nvtx, mjetRecoGroom, weight )
                hists.get('histAK7PtAvgVsMjetGroomOverReco_' + trigHelper.trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjetGroomOverMjet, ptAvgGroom, weight )


            else :
                print 'Error in trigger assignment!'
                continue

hists.getFile().cd()    
hists.write()

