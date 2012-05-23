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
                  default=False,
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
                  default=None,
                  dest='puWeighting',
                  help='PU Weighting. None=no weighting, 0=Nominal, -1=Down, +1=Up')



# Print verbose information
parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print verbose information')

# job splitting
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

#from CondFormats.JetMETObjects import *

#############################
# Matching one jet to another in some other collection
# Uses DR < 0.5 matching
#############################
def findJetInColl( jet0, jets ) :
    minDR = 0.5
    for jet in jets :
        dR = jet0.DeltaR( jet )
        if dR < minDR :
            return jet
    return None


#############################
# Utility for printing
#############################
def printJetColl( jets ) :
    for ijet in xrange(len(jets)) :
        jet = jets[ijet]
        if jet is None :
            print '-----> None!'
        else :
            print '{0:6.0f} : (pt,y,phi,m) = ({1:6.2f},{2:6.2f},{3:6.2f},{4:6.2f})'.format(
                ijet, jet.Perp(), jet.Rapidity(), jet.Phi(), jet.M()
            )

#############################
# Utility for finding bin
#############################
def findBin( x, bins ) :
    for ibin in xrange(len(bins) - 1) :
        if x >= bins[ibin] and x < bins[ibin+1] :
            return ibin
    return None

#############################
# Histogramming utility to  #
# book each hist for each   #
# jet grooming technique    #
#############################
class HistsGroomed :
    def __init__(self, outname, grooms) :
        self.f = ROOT.TFile(outname + '.root', 'recreate')
        self.grooms = grooms
        self.hists = []

    def get(self, name) :
        return self.f.FindObject(name)

    def write(self) :
        self.f.cd()
        self.f.Write()
        self.f.Close()

    def getFile(self) :
        return self.f

    def makeQuickHists(self) :
        for hist in self.hists :
            setattr(self,hist[0].GetName(), hist[0])
            setattr(self,hist[0].GetName() + '_Groom', [])
            for igroom in range(0,len(hist[1])):
                getattr(self,hist[0].GetName() + '_Groom').append( hist[1][igroom] )

    def book1F(self, *args, **kwargs) :
        name=args[0]
        title=args[1]
        nx=kwargs.get('nx')
        x1=kwargs.get('x1',None)
        x2=kwargs.get('x2',None)
        xbins=kwargs.get('xbins',None)
        bookGrooms=kwargs.get('bookGrooms', True)
        self.f.cd()
        ihists = []
        h1 = None
        if xbins is None :
            h1 = ROOT.TH1F(name,title,nx,x1,x2)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH1F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2)
                    ihists.append(hi)
        else :
            h1 = ROOT.TH1F(name,title,nx,xbins)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH1F(name + '_' + igroom,title + ', ' + igroom,nx,xbins)
                    ihists.append(hi)
        self.hists.append([h1, ihists])


    def book2F(self, *args, **kwargs) :
        name=args[0]
        title=args[1]
        nx=kwargs.get('nx')
        x1=kwargs.get('x1',None)
        x2=kwargs.get('x2',None)
        xbins=kwargs.get('xbins',None)
        ny=kwargs.get('ny')
        y1=kwargs.get('y1',None)
        y2=kwargs.get('y2',None)
        ybins=kwargs.get('ybins',None)
        bookGrooms=kwargs.get('bookGrooms', True)
        self.f.cd()
        ihists = []
        h1 = None
        if x1 is not None and y1 is not None :
            h1 = ROOT.TH2F(name,title,nx,x1,x2,ny,y1,y2)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2,ny,y1,y2)
                    ihists.append(hi)
        elif x1 is not None and y1 is None :
            h1 = ROOT.TH2F(name,title,nx,x1,x2,ny,ybins)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2,ny,ybins)
                    ihists.append(hi)
        elif x1 is None and y1 is not None :
            h1 = ROOT.TH2F(name,title,nx,xbins,ny,y1,y2)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,xbins,ny,y1,y2)
                    ihists.append(hi)
        else :
            h1 = ROOT.TH2F(name,title,nx,xbins,ny,ybins)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,xbins,ny,ybins)
                    ihists.append(hi)
        self.hists.append([h1, ihists])

    def book3F(self, *args, **kwargs) :
        name=args[0]
        title=args[1]
        nx=kwargs.get('nx')
        x1=kwargs.get('x1')
        x2=kwargs.get('x2')
        ny=kwargs.get('ny')
        y1=kwargs.get('y1')
        y2=kwargs.get('y2')
        nz=kwargs.get('nz')
        z1=kwargs.get('z1')
        z2=kwargs.get('z2')
        bookGrooms=kwargs.get('bookGrooms', True)
        self.f.cd()
        ihists = []
        h1 = ROOT.TH3F(name,title,nx,x1,x2,ny,y1,y2,nz,z1,z2)
        if bookGrooms :
            for igroom in self.grooms :
                hi = ROOT.TH3F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2,ny,y1,y2,nz,z1,z2)
                ihists.append(hi)
        self.hists.append([h1, ihists])

#############################
#  Get a collection from    #
#  the event record, and    #
#  correct them. Return     #
#  list of corrected p4's   #
#############################
class PyFWLiteJetColl :
    def __init__ ( self, coll, jec=None, jecUnc=None, upOrDown=True, useGen = False, jetPtMin = 20.0, jetEtaMax = 2.5):
        self.jetCollPxHandle         = Handle( "std::vector<float>" )
        self.jetCollPxLabel          = ( coll ,   "px" )
        self.jetCollPyHandle         = Handle( "std::vector<float>" )
        self.jetCollPyLabel          = ( coll ,   "py" )
        self.jetCollPzHandle         = Handle( "std::vector<float>" )
        self.jetCollPzLabel          = ( coll ,   "pz" )
        self.jetCollEnergyHandle     = Handle( "std::vector<float>" )
        self.jetCollEnergyLabel      = ( coll ,   "energy" )
        self.jetCollJetAreaHandle    = Handle( "std::vector<float>" )
        self.jetCollJetAreaLabel     = ( coll ,   "jetArea" )
        self.jetCollJecFactorHandle  = Handle( "std::vector<float>" )
        self.jetCollJecFactorLabel   = ( coll ,   "jecFactor" )
        self.jetColl = []
        self.jec = jec
        self.jecUnc = jecUnc
        self.upOrDown = upOrDown
        self.useGen = useGen
        self.jetPtMin = jetPtMin
        self.jetEtaMax = jetEtaMax

    def getJets( self, event, rho=None ) :
        self.jetColl = []
        event.getByLabel( self.jetCollPxLabel, self.jetCollPxHandle )
        self.jetCollPxs = self.jetCollPxHandle.product()
        event.getByLabel( self.jetCollPyLabel, self.jetCollPyHandle )
        self.jetCollPys = self.jetCollPyHandle.product()
        event.getByLabel( self.jetCollPzLabel, self.jetCollPzHandle )
        self.jetCollPzs = self.jetCollPzHandle.product()
        event.getByLabel( self.jetCollEnergyLabel, self.jetCollEnergyHandle )
        self.jetCollEnergys = self.jetCollEnergyHandle.product()
        if not self.useGen :
            event.getByLabel( self.jetCollJetAreaLabel, self.jetCollJetAreaHandle )
            self.jetCollJetAreas = self.jetCollJetAreaHandle.product()
            event.getByLabel( self.jetCollJecFactorLabel, self.jetCollJecFactorHandle )
            self.jetCollJecFactors = self.jetCollJecFactorHandle.product()

            for idef in range(0,len(self.jetCollPxs)):
                jdefRaw = ROOT.TLorentzVector(
                    self.jetCollPxs[idef] * self.jetCollJecFactors[idef],
                    self.jetCollPys[idef] * self.jetCollJecFactors[idef],
                    self.jetCollPzs[idef] * self.jetCollJecFactors[idef],
                    self.jetCollEnergys[idef] * self.jetCollJecFactors[idef]
                    )

                if self.jec is not None :
                    self.jec.setJetEta(jdefRaw.Eta())
                    self.jec.setJetPt(jdefRaw.Perp())
                    self.jec.setJetA(self.jetCollJetAreas[idef])
                    self.jec.setRho(rho)
                    factor = self.jec.getCorrection()

                    if self.jecUnc is not None:
                        self.jecUnc.setJetEta( jdefRaw.Eta() )
                        self.jecUnc.setJetPt( jdefRaw.Perp() * factor ); 
                        unc = jecUnc.getUncertainty( self.upOrDown )
                        factor *= (1 + unc)
                                                  
                else :
                    factor = 1.0
                    


                jdef = ROOT.TLorentzVector(
                    jdefRaw.Px() * factor,
                    jdefRaw.Py() * factor,
                    jdefRaw.Pz() * factor,
                    jdefRaw.Energy() * factor
                    )

                if jdef.Perp() > self.jetPtMin and abs(jdef.Rapidity()) < self.jetEtaMax:
                    self.jetColl.append( jdef )
        else :
            for idef in range(0,len(self.jetCollPxs)):
                jdefRaw = ROOT.TLorentzVector(
                    self.jetCollPxs[idef] ,
                    self.jetCollPys[idef] ,
                    self.jetCollPzs[idef] ,
                    self.jetCollEnergys[idef] 
                    )
                self.jetColl.append(jdefRaw)
        return self.jetColl


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

############################################
#     Trigger information                  #
############################################
# Use the same trigger thresholds as QCD-11-004 in AN-364-v4 Table 8
trigsToKeep = [
    'HLT_Jet60',
    'HLT_Jet110',
    'HLT_Jet190',
    'HLT_Jet240',
    'HLT_Jet370',
    ]
# Here are the trigger thresholds for the various eta bins.
# In the following, each entry is an eta bin. The
# two fields are then [etamin,etamax], and the
# list of mjj thresholds for HLT_Jet60,110,190,240,370.
trigThresholds = [
[[0.0, 0.5], [ 178.,  324.,  533.,  663.,  970., 7000.] ],
[[0.5, 1.0], [ 240.,  390.,  645.,  820., 1218., 7000.] ],
[[1.0, 1.5], [ 369.,  615.,  998., 1261., 1904., 7000.] ],
[[1.5, 2.0], [ 530.,  920., 1590., 1985., 3107., 7000.] ],
[[2.0, 2.5], [ 913., 1549., 2665., 3700., 4000., 7000.] ]
    ]



############################################
# Collection names, etc #
############################################

# Ungroomed collection.
#   Used for trigger matching, and used as
#   primary "key". GenJets and GroomedJets matched from
#   these.
ak7Obj = PyFWLiteJetColl( 'ak7Lite', jec=jec, jecUnc=jecUnc, upOrDown=upOrDown )

# List of groomed jets
ak7GroomObj = []

for igroom in options.collName :
    ak7GroomObj.append( PyFWLiteJetColl( 'ak7' + igroom + 'Lite', jec=jec, jecUnc=jecUnc, upOrDown=upOrDown ) )
    
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

# Generator information
generatorHandle = Handle("GenEventInfoProduct")
generatorLabel = ( "generator", "")

# Trigger information. 
trigHandle = Handle("std::vector<std::string>")
trigLabel = ( "dijetTriggerFilter", 'jetPaths')



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


# Mjj and <Mjet> versus |eta_max| for the different triggers. Only data. #
for trig in trigsToKeep :
    hists.book2F('histAK7MjjVsEtaMax_' + trig,
                 'AK7 m_{jj} Versus #eta_{max}' + trig +';m_{jj} (GeV);#eta_{max}(radians)',
                 nx=70, x1=0., x2=7000., ny=5, y1=0.0, y2=2.5)
    hists.book2F('histAK7MjetVsEtaMax_' + trig,
                 'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV)' + trig + ';#eta_{max}(radians)',
                 nx=60, x1=0., x2=300., ny=5, y1=0.0, y2=2.5)


# GENERATED Mjj and <Mjet> versus |eta_max|. only for MC.
hists.book2F('histAK7MjjGenVsEtaMax',
             'AK7 m_{jj}^{GEN} Versus #eta_{max};m_{jj}^{GEN} (GeV);#eta_{max}(radians)',
             nx=70, x1=0., x2=7000., ny=5, y1=0.0, y2=2.5, bookGrooms=False)
hists.book2F('histAK7MjetGenVsEtaMax',
             'AK7 m_{jet}^{GEN} Versus #eta_{max};m_{jj}^{GEN} (GeV);#eta_{max}(radians)',
             nx=60, x1=0., x2=300., ny=5, y1=0.0, y2=2.5, bookGrooms=False)


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

# Mjj and <Mjet> versus ptAvg for the different triggers. Only data. #
for trig in trigsToKeep :
    hists.book2F('histAK7MjjVsPtAvg_' + trig,
                 'AK7 m_{jj} Versus p_{T}^{AVG} ' + trig +';m_{jj} (GeV);p_{T}^{AVG} (GeV)',
                 nx=70, x1=0., x2=7000., ny=len(ptBins)-1, ybins=ptBins)
    hists.book2F('histAK7MjetVsPtAvg_' + trig,
                 'AK7 <m_{jet}> Versus p_{T}^{AVG} ;<m_{jet}> (GeV)' + trig + ';p_{T}^{AVG} (GeV)',
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
responses_Groom = []

for ibin in range(0,len(ptBins)-1) :
    response = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
    response.SetName('response_pt' + str(ibin))
    response_Groom = []
    for igroom in range(0,len(ak7GroomObj)):
        res = ROOT.RooUnfoldResponse(60, 0., 300., 60, 0., 300.)
        res.SetName('response_' + options.collName[igroom] + '_pt' + str(ibin) )
        response_Groom.append( res )
    responses.append(response)
    responses_Groom.append( response_Groom )

hists.makeQuickHists()

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
    for event in events:

        # Histogram filling weight
        weight = 1.0

        # Histogram index for data (Jet60,110,190,240,370)
        iTrigHist = None

        if count % 10000 == 0 or options.verbose :
            print 'Processing event ' + str(count)

        count += 1

        # Event-level variables:
        npv = -1         # Number of Primary Vertices observed
        npu = -1         # Number of pileup interactions simulated
        mjjReco = None   # reconstructed dijet mass
        mjjGen = None    # particle-level dijet mass
        mjetReco = None  # reconstructed average jet mass
        mjetGen = None   # generated average jet mass
        etaMax = None    # maximum eta of the dijet system
        ptAvg = None     # average pt of the dijet system

        event.getByLabel( rhoLabel, rhoHandle )
        rho = rhoHandle.product()[0]

        # First get the jets.
        # For data, only reco (obviously).
        ak7Def = ak7Obj.getJets( event, rho )


        # response pt bin
        responsePtBin = None

        # For MC, get the gen jets, and also the gen jets matched to reco jets.
        # If desired, modify the jet energy resolution appropriately. 
        ptAvgGenOnly = None
        mjetGenOnly = None
        mjjGenOnly = None
        if options.useMC :
            ak7Gen = ak7GenObj.getJets( event )
            if len(ak7Gen) > 1 :
                ptAvgGenOnly = (ak7Gen[0].Perp() + ak7Gen[1].Perp()) * 0.5
                mjetGenOnly = (ak7Gen[0].M() + ak7Gen[1].M()) * 0.5
                mjjGenOnly = (ak7Gen[0] + ak7Gen[1]).M()
                # Denominators for reconstructed jet efficiency as a function of generated ptAvg
                hists.recoEffDen.Fill( mjetGenOnly )
                if options.verbose :
                    print 'recoEffDen filled ' + str(ptAvgGenOnly)
                for igroom in range(0,len(ak7GroomObj)) :
                    hists.recoEffDen_Groom[igroom].Fill( mjetGenOnly )
        ak7GenMatched = []
        foundMatchedGen = True
        if options.useMC :
            for idef in range(0,len(ak7Def)):
                jdef = ak7Def[idef]
                jgen = findJetInColl( jdef, ak7Gen )
                if jgen is None and idef < 2:
                    foundMatchedGen = False
                else :
                    # Here we add the genjet matched to the reco jet
                    ak7GenMatched.append( jgen )
                    # Here we change the jet energy and angular resolution based on the
                    # matched genjet
                    if options.jarSmearVal is not None and jgen is not None:
                        recoeta = jdef.Eta()
                        geneta = jgen.Eta()
                        deltaeta = (recoeta-geneta)*options.jarSmearVal
                        etaSmear = max(0.0,(recoeta+deltaeta)/recoeta)
                        recophi = jdef.Phi()
                        genphi = jgen.Phi()
                        deltaphi = (recophi-genphi)*options.jarSmearVal 
                        phiSmear = max(0.0,(recophi+deltaphi)/recophi)

                        jdef.SetPtEtaPhiE( jdef.Perp(), jdef.Eta()*etaSmear, jdef.Phi()*phiSmear, jdef.Energy() )

                    if options.jerSmearVal is not None and jgen is not None: 
                        recopt = jdef.Perp()
                        genpt = jgen.Perp()
                        deltapt = (recopt-genpt)*options.jerSmearVal
                        ptSmear = max(0.0, (recopt+deltapt)/recopt)
                        jdef.SetPerp( jdef.Perp() * ptSmear )

                    
                if options.verbose :
                    print ' corrjet {0:4.0f}, (pt,eta,phi,m) = ({1:6.2f},{2:6.2f},{3:6.2f},{4:6.2f})'.format( idef, jdef.Perp(), jdef.Eta(), jdef.Phi(), jdef.M() )
                    if options.useMC and jgen is not None :
                        print ' gen jet {0:4.0f}, (pt,eta,phi,m) = ({1:6.2f},{2:6.2f},{3:6.2f},{4:6.2f})'.format( idef, jgen.Perp(), jgen.Eta(), jgen.Phi(), jgen.M() )

        # Check to make sure we have two reconstructed jets
        if len(ak7Def) < 2 :
            if options.verbose :
                print 'Less than two reconstructed jets!'

            # Set the response bin to the "gen-only" bin
            responsePtBin = findBin( ptAvgGenOnly, ptBins )
            if responsePtBin is None :
                continue
            response = responses[responsePtBin]
            response_Groom = responses_Groom[responsePtBin]
            # Here we didn't get 2 reconstructed jets
            if options.useMC == True and mjetGenOnly is not None :
                # if using MC, then check to see if there are gen jets.
                # If so, it's a response "Miss", so fill and continue.
                # Otherwise, it's not interesting, so just continue. 
                if ptAvgGenOnly is not None :
                    # if there are gen jets, then it's a response "miss"
                    if options.verbose :
                        print 'Missed reconstructed jet!'
                        print 'Reconstructed : ' 
                        printJetColl( ak7Def )
                        print 'Generated : '
                        printJetColl( ak7Gen )
                    response.Miss( mjetGenOnly )
                    if options.verbose :
                        print 'response miss mjetGenOnly = ' + str(mjetGenOnly)
                    for igroom in range(0,len(ak7GroomObj)) :
                        response_Groom[igroom].Miss( mjetGenOnly )
                    
                continue
            else :
                # If not using MC, just skip the event
                continue

        # Here we have two reconstructed jets. Get the
        # average jet mass, dijet mass, etaMax, average pt,
        # and trigger bin
        dijetCandReco = ak7Def[0] + ak7Def[1]
        mjetReco = (ak7Def[0].M() + ak7Def[1].M()) * 0.5
        mjjReco = dijetCandReco.M()
        ptAvg = (ak7Def[0].Perp() + ak7Def[1].Perp()) * 0.5
        etaMax = abs(ak7Def[0].Rapidity())
        responsePtBin = findBin( ptAvg, ptBins )
        if responsePtBin is None :
            continue
        response = responses[responsePtBin]
        if abs(ak7Def[0].Rapidity()) < abs(ak7Def[1].Rapidity()) :
            etaMax = abs(ak7Def[1].Rapidity())
        trigEtaBin = -1
        for ibin in range(0, len(trigThresholds)) :
            if etaMax >= trigThresholds[ibin][0][0] and etaMax < trigThresholds[ibin][0][1] :
                trigEtaBin = ibin
                break
        mjjThresholds = trigThresholds[ibin][1]
        if options.verbose :
            print 'mjjReco = ' + str(mjjReco) + ', etaMax = ' + str(etaMax) + ', trig eta bin = ' + str(trigEtaBin)
            print 'mjj thresholds : '
            print mjjThresholds


        # Now fill truth information for MC
        dijetCandGen  = None
        mjjGen = None
        mjetGen = None
        ptAvgGen = None

        if options.useMC :
            
            # Here, we have 2 reconstructed jets but at least one is
            # not matched to a gen jet, so this is a response fake. 
            if foundMatchedGen is False:
                if options.verbose :
                    print 'Fake jet! No Gen Jet'
                    printJetColl( ak7Def )
                    printJetColl( ak7Gen )
                response.Fake( mjetReco )
                if options.verbose :
                    print 'response fake mjetReco = ' + str(mjetReco)
                for igroom in range(0,len(ak7GroomObj)) :
                    response_Groom[igroom].Fake( mjetReco )
            # Here, we have 2 reconstructed jets, both matched
            # to a gen jet, so this is a fully-filled event
            else :
                dijetCandGen  = ak7GenMatched[0] + ak7GenMatched[1]
                mjjGen = dijetCandGen.M()
                mjetGen = (ak7GenMatched[0].M() + ak7GenMatched[1].M()) * 0.5
                ptAvgGen = (ak7GenMatched[0].Perp() + ak7GenMatched[1].Perp()) * 0.5
                response.Fill( mjetReco , mjetGen )
                if options.verbose :
                    print 'response successfully filled, mjetReco = ' + str(mjetReco) + ', mjetGen = ' + str(mjetGen)
            #NOTE: Response "Miss"-es are filled above. 

        #------------------------------------------
        # Now get the event weight.
        #
        # For MC:
        #   - Weight by the generator weight (cross section for this event)
        # For Data:
        #   - Weight by trigger prescale of *highest* pt-threshold jet trigger that passed
        #------------------------------------------
        passEvent = False
        if options.useMC :
            passGen = False
            # Get the generator product
            event.getByLabel( generatorLabel, generatorHandle )
            if generatorHandle.isValid() :
                generatorInfo = generatorHandle.product()
                # weight is the generator weight
                weight *= generatorInfo.weight()
                if options.verbose :
                    print 'generator info weight = ' + str(weight)
                passGen = True

            passMjjTrig = False
            if options.verbose :
                print 'testing MC mjjReco = ' + str(mjjReco) + ', etamax = ' + str(etaMax) + ', threshold = ' + str(mjjThresholds[0])
            if mjjReco >= mjjThresholds[0] :
                if options.verbose :
                    print '  ----> passed!'
                passMjjTrig = True

            passEvent = passMjjTrig and passGen

        else :
            # Get the pat::TriggerEvent
            event.getByLabel( trigLabel, trigHandle )
            trigs = trigHandle.product()
            acceptedPaths = []
            trigPassedName = None
            passMjjTrig = False

            # If there are any accepted paths, cache them. Then match to the lookup table "trigThresholds" to see if
            # the event is in the correct mjj bin for the trigger in question.
            if len( trigs ) > 0 :
                for ipath in xrange( len(trigs)-1, -1, -1) :
                    path = trigs[ipath]
                    for ikeep in xrange(len(trigsToKeep)-1, -1, -1) :
                        if options.verbose :
                            print '   ----- checking trigger ' + trigsToKeep[ikeep] + ' : mjjThreshold = ' + str(mjjThresholds[ikeep])
                        if path.find( trigsToKeep[ikeep] ) >= 0 and mjjReco >= mjjThresholds[ikeep] and mjjReco < mjjThresholds[ikeep + 1]:
                            trigPassedName = path
                            iTrigHist = ikeep
                            passMjjTrig = True
                            if options.verbose :
                                print '    -----------> Joy and elation, it worked! trigger = ' + trigsToKeep[iTrigHist]
                            break
                    if passMjjTrig == True :
                        break

            passEvent = passMjjTrig



        if passEvent :
            if options.verbose :
                print 'event passed! OH happy day!'
                print 'Filling mjjReco = ' + str(mjjReco) + ', mjetReco = ' + str(mjetReco) + ', etaMax = ' + str(etaMax) + ', weight = ' + str(weight)


            hists.histAK7MjjVsEtaMax.Fill( mjjReco, etaMax, weight )
            hists.histAK7MjetVsEtaMax.Fill( mjetReco, etaMax, weight )

            hists.histAK7MjjVsPtAvg.Fill( mjjReco, ptAvg, weight )
            hists.histAK7MjetVsPtAvg.Fill( mjetReco, ptAvg, weight )

            if options.useMC  :

                # gen-jet efficiency as a function of reconstructed ptAvg
                if options.verbose :
                    print 'genEffDen filling ' + str(ptAvg)
                hists.genEffDen.Fill( mjetReco )

                if mjjGen is not None:
                    
                    # Reconstructed efficiency as a function of generated ptAvg
                    hists.recoEffNum.Fill( mjetGenOnly )

                    # Generator efficiency as a function of reconstructed ptAvg
                    hists.genEffNum.Fill( mjetReco )

                    if options.verbose :
                        print 'recoEffNum filling ' + str(mjetGenOnly)
                        print 'genEffNum  filling ' + str(mjetReco)
                    
                    # Also get the number of simulated pileup interactions
                    #event.getByLabel( puLabel, puHandle )
                    #puInfos = puHandle.product()
                    #npu = puInfos[0].getPU_NumInteractions()

                    response0 = ak7Def[0].Perp() / ak7GenMatched[0].Perp()
                    mjjResponse = mjjReco / mjjGen
                    mjetResponse = mjetReco / mjetGen
                    ptGen0 = ak7GenMatched[0].Perp()
                    etaGen0 = ak7GenMatched[0].Rapidity()
                    hists.histAK7PtResponse.Fill( ptGen0, response0 )
                    hists.histAK7EtaResponse.Fill( etaGen0, response0 )

                    hists.histAK7MjjResponseVsEtaMax.Fill( mjjGen, mjjResponse, etaMax )
                    hists.histAK7MjetResponseVsEtaMax.Fill( mjetGen, mjetResponse, etaMax )
                    hists.histAK7MjjGenVsEtaMax.Fill( mjjGen, etaMax, weight )
                    hists.histAK7MjetGenVsEtaMax.Fill( mjetGen, etaMax, weight )
                    hists.histAK7MjjGenVsRecoVsEtaMax.Fill( mjjGen, mjjReco, etaMax )
                    hists.histAK7MjetGenVsRecoVsEtaMax.Fill( mjetGen, mjetReco, etaMax )

                    hists.histAK7MjjResponseVsPtAvg.Fill( mjjGen, mjjResponse, ptAvg )
                    hists.histAK7MjetResponseVsPtAvg.Fill( mjetGen, mjetResponse, ptAvg )
                    hists.histAK7MjjGenVsRecoVsPtAvg.Fill( mjjGen, mjjReco, ptAvg )
                    hists.histAK7MjetGenVsRecoVsPtAvg.Fill( mjetGen, mjetReco, ptAvg )
                    hists.histAK7MjjGenVsRecoVsPtAvgHighPt.Fill( mjjGen, mjjReco, ptAvg )
                    hists.histAK7MjetGenVsRecoVsPtAvgHighPt.Fill( mjetGen, mjetReco, ptAvg )


                    hists.histAK7MjjGenVsPtAvg.Fill( mjjGen, ptAvg, weight )
                    hists.histAK7MjetGenVsPtAvg.Fill( mjetGen, ptAvg, weight )

            elif iTrigHist is not None :
                if options.verbose :
                    print ' Filling histogram ' + str(iTrigHist) + ' which corresponds to trigger ' + trigsToKeep[iTrigHist]
                hists.get('histAK7MjjVsEtaMax_' + trigsToKeep[iTrigHist]).Fill( mjjReco, etaMax, weight )
                hists.get('histAK7MjetVsEtaMax_' + trigsToKeep[iTrigHist]).Fill( mjetReco, etaMax, weight )                
                hists.get('histAK7MjjVsPtAvg_' + trigsToKeep[iTrigHist]).Fill( mjjReco, ptAvg, weight )
                hists.get('histAK7MjetVsPtAvg_' + trigsToKeep[iTrigHist]).Fill( mjetReco, ptAvg, weight )                
            else :
                print 'Error in trigger assignment!'
                continue





            for igroom in range(0,len(ak7GroomObj)):
                igroomObj = ak7GroomObj[igroom]
                ak7Groom = igroomObj.getJets( event, rho )
                ak7GroomMatched = []
                keep = True
                if options.useMC :
                    igroomGenObj = ak7GenGroomObj[igroom]
                    ak7GenGroom = igroomGenObj.getJets( event )
                    ak7GenGroomMatched = []
                iijet = 0
                for ijet in ak7Def :
                    toput = findJetInColl(ijet, ak7Groom )
                    if toput is None and ijet < 2 :
                        keep=False
                    ak7GroomMatched.append( toput )
                    if options.useMC :
                        toputgen = findJetInColl( ijet, ak7GenGroom )
                        if toputgen is None and iijet < 2 :
                            keep = False
                        ak7GenGroomMatched.append( toputgen )
                    iijet += 1

                if len(ak7GroomMatched) < 2 or keep == False :
                    continue

                

                ptAvgGroom = (ak7GroomMatched[0].Perp() + ak7GroomMatched[1].Perp()) * 0.5
                dijetCandRecoGroom = ak7GroomMatched[0] + ak7GroomMatched[1]
                mjetRecoGroom = (ak7GroomMatched[0].M() + ak7GroomMatched[1].M()) * 0.5
                mjjRecoGroom = dijetCandRecoGroom.M()
                hists.histAK7MjjVsEtaMax_Groom[igroom].Fill( mjjRecoGroom , etaMax, weight)
                hists.histAK7MjetVsEtaMax_Groom[igroom].Fill(mjetRecoGroom , etaMax, weight )

                hists.histAK7MjjVsPtAvg_Groom[igroom].Fill( mjjRecoGroom , ptAvg, weight)
                hists.histAK7MjetVsPtAvg_Groom[igroom].Fill(mjetRecoGroom , ptAvg, weight )
                responsePtBin = findBin( ptAvgGroom, ptBins )
                if responsePtBin is None :
                    continue
                response_Groom = responses_Groom[responsePtBin]
        
                if options.useMC :

                    if len(ak7GroomMatched) < 2 :
                        continue


                    if len(ak7GenGroomMatched) < 2 or ak7GenGroomMatched[0] is None or ak7GenGroomMatched[1] is None:
                        print 'ak7GenGroomMatched has a problem'
                        print 'Reco jets'
                        printJetColl( ak7Def )
                        print 'Gen jets'
                        printJetColl( ak7Gen )
                        print 'Gen jets matched'
                        printJetColl( ak7GenMatched )
                        print 'Groomed jets'
                        printJetColl( ak7GroomMatched )
                        print 'Groomed gen jets' 
                        printJetColl( ak7GenGroomMatched )

                        continue
                    
                    dijetCandGroomGen  = ak7GenGroomMatched[0] + ak7GenGroomMatched[1]
                    mjjGroomGen = dijetCandGroomGen.M()
                    mjetGroomGen = (ak7GenGroomMatched[0].M() + ak7GenGroomMatched[1].M()) * 0.5
                    

                    # gen-jet efficiency as a function of reconstructed ptAvgGroom
                    hists.genEffDen_Groom[igroom].Fill( mjetRecoGroom )

                    
                    if mjjGroomGen is not None :


                        # Groomed reconstructed efficiency as a function of generated ptAvg
                        hists.recoEffNum_Groom[igroom].Fill( mjetGroomGen )

                        # Generator efficiency as a function of reconstructed ptAvgGroom
                        hists.genEffNum_Groom[igroom].Fill( mjetRecoGroom )

                        # response matrix
                        response_Groom[igroom].Fill( mjetRecoGroom , mjetGroomGen )


                        # Also get the number of simulated pileup interactions
                        #event.getByLabel( puLabel, puHandle )
                        #puInfos = puHandle.product()
                        #npu = puInfos[0].getPU_NumInteractions()

                        response0 = ak7GroomMatched[0].Perp() / ak7GenGroomMatched[0].Perp()
                        mjjResponse = mjjRecoGroom / mjjGroomGen
                        mjetResponse = mjetRecoGroom / mjetGroomGen
                        ptGen0 = ak7GenGroomMatched[0].Perp()
                        etaGen0 = ak7GenGroomMatched[0].Rapidity()

                        hists.histAK7PtResponse_Groom[igroom].Fill( ptGen0, response0 )
                        hists.histAK7EtaResponse_Groom[igroom].Fill( etaGen0, response0 )
                        hists.histAK7MjjResponseVsEtaMax_Groom[igroom].Fill( mjjGroomGen, mjjResponse, etaMax )
                        hists.histAK7MjetResponseVsEtaMax_Groom[igroom].Fill( mjetGroomGen, mjetResponse, etaMax )

                        hists.histAK7MjjResponseVsPtAvg_Groom[igroom].Fill( mjjGroomGen, mjjResponse, ptAvgGroom )
                        hists.histAK7MjetResponseVsPtAvg_Groom[igroom].Fill( mjetGroomGen, mjetResponse, ptAvgGroom )

                        hists.histAK7MjjResponseVsEtaMax_Groom[igroom].Fill( mjjGroomGen, mjjResponse, etaMax )
                        hists.histAK7MjetResponseVsEtaMax_Groom[igroom].Fill( mjetGroomGen, mjetResponse, etaMax )
                        hists.histAK7MjjGenVsRecoVsEtaMax_Groom[igroom].Fill( mjjGroomGen, mjjRecoGroom, etaMax )
                        hists.histAK7MjetGenVsRecoVsEtaMax_Groom[igroom].Fill( mjetGroomGen, mjetRecoGroom, etaMax )

                        hists.histAK7MjjResponseVsPtAvg_Groom[igroom].Fill( mjjGroomGen, mjjResponse, ptAvgGroom )
                        hists.histAK7MjetResponseVsPtAvg_Groom[igroom].Fill( mjetGroomGen, mjetResponse, ptAvgGroom )
                        hists.histAK7MjjGenVsRecoVsPtAvg_Groom[igroom].Fill( mjjGroomGen, mjjRecoGroom, ptAvgGroom )
                        hists.histAK7MjetGenVsRecoVsPtAvg_Groom[igroom].Fill( mjetGroomGen, mjetRecoGroom, ptAvgGroom )
                        hists.histAK7MjjGenVsRecoVsPtAvgHighPt_Groom[igroom].Fill( mjjGroomGen, mjjRecoGroom, ptAvgGroom )
                        hists.histAK7MjetGenVsRecoVsPtAvgHighPt_Groom[igroom].Fill( mjetGroomGen, mjetRecoGroom, ptAvgGroom )

                        hists.histAK7MjjGenVsPtAvg_Groom[igroom].Fill( mjjGroomGen, ptAvgGroom, weight )
                        hists.histAK7MjetGenVsPtAvg_Groom[igroom].Fill( mjetGroomGen, ptAvgGroom, weight )
                    


                elif iTrigHist is not None :
                    if options.verbose :
                        print ' Filling histogram ' + str(iTrigHist) + ' which corresponds to trigger ' + trigsToKeep[iTrigHist]
                    hists.get('histAK7MjjVsEtaMax_' + trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjjRecoGroom, etaMax, weight )
                    hists.get('histAK7MjetVsEtaMax_' + trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjetRecoGroom, etaMax, weight )                
                    hists.get('histAK7MjjVsPtAvg_' + trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjjRecoGroom, ptAvgGroom, weight )
                    hists.get('histAK7MjetVsPtAvg_' + trigsToKeep[iTrigHist] + '_' + options.collName[igroom]).Fill( mjetRecoGroom, ptAvgGroom, weight )
                else :
                    print 'Error in trigger assignment!'
                    continue

hists.getFile().cd()
for response in responses :
    response.Write()
for response_Groom in responses_Groom :
    for res in response_Groom :
        res.Write()
    
hists.write()

