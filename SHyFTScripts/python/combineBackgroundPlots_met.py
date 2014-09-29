#!/bin/python

# ===================================================
#             stitchFlavorHistory.py
#
#   - Inputs number of events separated by path from
#     various files
#   - Inputs a template for each flavor (b,c,q)
#   - Scales the templates to the number of events
#     in each path
#   - Sums the contributions
#   - Outputs the sum
# ===================================================
# Usage:
#   - Parameters:
#        * lum : luminosity in pb-1
#        * xs  : Leading order cross sections
#        * xs_wtot: Full cross section to scale to
#        * n   : Number of *total* events generated
#   - File to path assignment
#
# ===================================================

from sys import argv
import sys

from optparse import OptionParser

import re

parser = OptionParser()

parser.add_option('--input', metavar='F', type='string', action='store',
                  default='ttbsm_415_v7',
                  dest='input',
                  help='input file tag to be used')

parser.add_option('--mcDir', metavar='D1', type='string', action='store',
                  default='pfShyftAna',
                  dest='histdir',
                  help='TFileDirectory from where to get the hists for MC')

parser.add_option('--dataDir', metavar='D2', type='string', action='store',
                  default='pfShyftAna',
                  dest='histdirData',
                  help='TFileDirectory from where to get the hists for data')

parser.add_option('--templateDir', metavar='D3', type='string', action='store',
                  default='pfShyftAnaMC',
                  dest='templatedir',
                  help='TFileDirectory from where to get the templates for MC')

parser.add_option('--outputLabel', metavar='L', type='string', action='store',
                  default='btagReweighted_jes',
                  dest='outputLabel',
                  help='output label for the output root file')

parser.add_option('--var0tag', metavar='V0', type='string', action='store',
                  default='MET',
                  dest='var0tag',
                  help='name of 0-tag variable: (%default default)')

parser.add_option('--var1tag', metavar='V1', type='string', action='store',
                  default='secvtxMass',
                  dest='var1tag',
                  help='name of 1-tag variable: (%default default)')

parser.add_option('--var2tag', metavar='V2', type='string', action='store',
                  default='secvtxMass',
                  dest='var2tag',
                  help='name of 2-tag variable: (%default default)')

parser.add_option('--output', metavar='OUT', type='string', action='store',
                  default='',
                  dest='output',
                  help='Force output name to be "OUT" instead of default name')

parser.add_option('--massTemplateDir', metavar='MTD', type='string',
                  default='pfShyftAnaMC',
                  dest='massTemplateDir',
                  help='Directory from which to get high statistics mass templates')

parser.add_option('--globalSF', metavar='SF', type='float',
                  default=0.9604,##By Misha for electrons
                  dest='globalSF',
                  help='Global lepton SF (%default default)')


parser.add_option('--minJets', metavar='N', type='int', action='store',
                  default=1,
                  dest='minJets',
                  help='Minimum number of jets')

parser.add_option('--useData', metavar='B', action='store_true',
                  default=True,
                  dest='useData',
                  help='Use data in estimates')

parser.add_option('--dataFile', metavar='F', type='string', action='store',
                  default='../RootFiles_v5/SingleElectron_tlbsm_424_v8.root',
                  dest='dataFile',
                  help='If useData is True, this is the file from which to get the data histograms')

parser.add_option('--noQCD', metavar='B', action='store_true',
                  default=True,
                  dest='noQCD',
                  help='noQCD')

parser.add_option('--useDataQCD', metavar='B', action='store_true',
                  default=True,
                  dest='useDataQCD',
                  help='Use data-driven QCD in estimates')

parser.add_option('--dataQCDFile', metavar='F', type='string', action='store',
                  default='qcd_eleEB_127.1.root',
                  dest='dataQCDFile',
                  help='If useDataQCD is True, this is the file from which to get the data QCD histograms')

parser.add_option('--makePretagPlots', action='store_true',
                  default=False,
                  dest='makePretagPlots',
                  help='Plot everything with muon eta rather than secvtx mass')

parser.add_option('--wjetsQ2Var', metavar='V', type='string', action='store',
                  default=None,
                  dest='wjetsQ2Var',
                  help='Use a Q^2 variation for WJets and VQQ. Options are scaleup or scaledown')

parser.add_option('--ttbarIFSR', metavar='V', type='string', action='store',
                  default=None,
                  dest='ttbarIFSR',
                  help='Use IFSR ttbar samples. Options are smallerISRFSR or largerISRFSR or pileup')

parser.add_option('--lum', metavar='L', action='store',
                  default=771.5,
                  #default=1.0,
                  dest='lum',
                  help='Luminosity of the data')

(options, args) = parser.parse_args()

inFileEnd = options.input
tempstr   = options.histdir
outlabel  = options.outputLabel
minJets   = options.minJets
useData   = options.useData
useDataQCD = options.useDataQCD
var0tag   = options.var0tag
var1tag   = options.var1tag
var2tag   = options.var2tag

histdir = tempstr+'/'

# strip out any '/'s in the filename
if options.outputLabel != "All":
    outfilestr = re.sub (r'/', '', tempstr)
else:
    outfilestr = tempstr+'_'+outlabel
print 'outfile------->',  outfilestr   
#outfilestr = tempstr.strip('/eleEB')+'_' + outlabel
histdirData = options.histdirData + '/'
templatedir = options.templatedir + '/'

argv = []


from ROOT import *
from array import *

from stitchFlavorHistory import *
from addSingleTops import *
from addSimple import *


# load up root
gROOT.Macro("~/rootlogon.C")

# ---------------------------------------------
# Get the files from whatever samples you want to stitch
# ---------------------------------------------
#f_ttbar = TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_'+inFileEnd+'.root')

if not options.noQCD:
    f_qcd   = TFile('../RootFiles_v4/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_ttbsm_'+inFileEnd+'.root')
f_st_s  = TFile('../RootFiles_v5/TToBLNu_TuneZ2_s-channel_7TeV-madgraph_tlbsm_415_v7.root')
f_st_t  = TFile('../RootFiles_v5/TToBLNu_TuneZ2_t-channel_7TeV-madgraph_tlbsm_415_v7.root')
f_st_tW = TFile('../RootFiles_v5/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_tlbsm_415_v7.root')
f_ttbar = TFile('../RootFiles_v5/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')
f_wjets = TFile('../RootFiles_v5/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')
f_zjets = TFile('../RootFiles_v5/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8.root')
   
f_data = TFile(options.dataFile)
if useDataQCD :
    f_qcd_data = TFile(options.dataQCDFile)

if  (options.dataFile.find('pf') >= 0 and options.dataQCDFile.find('pf') == -1) or (options.dataFile.find('jpt') >= 0 and options.dataQCDFile.find('jpt') == -1) :
    print 'Inconsistent files! Data file is ' + options.dataFile + 'and QCD file is ' + options.dataQCDFile
    quit
    

# ---------------------------------------------
# Assumed luminosity (pb-1)
# ---------------------------------------------
lum = options.lum

globalSF = options.globalSF # From

# ---------------------------------------------
# Leading order cross sections (pb)
# ---------------------------------------------
#xs_ttbar = 1
xs_ttbar =   157.5 * globalSF
xs_wjets = 24170.0 * globalSF # LO
xs_wtot  = 31314.0 * globalSF # NNLO
xs_zjets =  2289.0 * globalSF # LO
xs_ztot  =  3048.0 * globalSF # NNLO
xs_qcd   = 79688.0 * globalSF # Dummy for e+jets
xs_st_t  =   20.93 * globalSF
xs_st_s  =    1.53 * globalSF # xs_singS  =     4.6 * 0.32442
xs_st_tW =    10.6 * globalSF


# ---------------------------------------------
# Relative "k" factors.
# There is an overall K-factor to get to the
# NLO (or NNLO) cross section,
# and then individual factors for each
# heavy flavor species, which can be different.
# ---------------------------------------------

k_wtot = xs_wtot / xs_wjets
k_ztot = xs_ztot / xs_zjets
s_wbb = 1.0
s_wcc = 1.0
s_wqq = 1.0


# ---------------------------------------------
# Number of generated events
# ---------------------------------------------
n_qcd   =  29504866 ##Dummy for e+jets
n_st_s  =  494967
n_st_t  =  484060
n_st_tW =  489417
n_wjets =  49484941 ##Summer11
n_zjets =  32512091 ##Summer11
n_ttbar =  3688248  ##Summer11

# ---------------------------------------------
# get the output file
# ---------------------------------------------
outputName = options.output or ('DummyFiles/stitched_' + outfilestr + '.root')
f_out = TFile(outputName, 'RECREATE')


# ---------------------------------------------
# maximum number of jets and tags
# ---------------------------------------------
maxJets = 6
maxTags = 3

# ---------------------------------------------
# ---------------------------------------------
#                   STEP 1 : W/Z+Jets
# ---------------------------------------------
# ---------------------------------------------

pathNamesW = [
      ['Wjets'    , f_wjets ,n_wjets, xs_wjets ],
    ]

pathNamesZ = [
    ['Zjets'    , f_zjets ,n_zjets, xs_zjets ],# path 1   
    ]

suffixes = [
    ['_b', '_c', '_q'],
    ['_b', '_c', '_q'],
    ['_b', '_c', '_q'],    
    ]


# now hard coded location
bmass  = f_ttbar.Get( '%s/bmass'  % options.massTemplateDir)
cmass  = f_ttbar.Get( '%s/cmass'  % options.massTemplateDir)
lfmass = f_wjets.Get( '%s/lfmass' % options.massTemplateDir)

bmass.Scale(1.0/bmass.Integral())
cmass.Scale(1.0/cmass.Integral())
lfmass.Scale(1.0/lfmass.Integral())

templates = [bmass, cmass, lfmass]
ibmass  = 0
icmass  = 1
ilfmass = 2

if options.makePretagPlots is False :
    tagDists = [
        var0tag,
        var1tag,
        var2tag
        ]
    wjetsTemplates = [
        None,
        templates,
        templates
        ]
else :
    tagDists = [
        var0tag,
        var0tag,
        var0tag
        ]
    wjetsTemplates = [
        None,
        None,
        None
        ]


wbxHists = []
wcxHists = []
wqqHists = []
zbxHists = []
zcxHists = []
zqqHists = []


maxJets = 6
maxTags = 3

for ijet in range(1,maxJets) :
    for itag in range(0,maxTags):
        if itag > ijet :
            continue
        tagDist = tagDists[itag]
        itemplates = wjetsTemplates[itag]
        #if (ijet >3 and itag ==2):
        #    s = 'dijetMass_' + str(ijet) + 'j_' + str(itag) + 't' 
        #else:     
        s = tagDist + '_' + str(ijet) + 'j_' + str(itag) + 't'
        [iwbx, iwcx, iwqq] = stitchFlavorHistory( ['Wbx_', 'Wcx_', 'Wqq_'],
                                                  lum,
                                                  histdir , s, k_wtot,
                                                  pathNamesW, itemplates, suffixes[itag], verbose=False)
        wbxHists.append( iwbx )
        wcxHists.append( iwcx )
        wqqHists.append( iwqq )        

        [izbx, izcx, izqq] = stitchFlavorHistory( ['Zbx_', 'Zcx_', 'Zqq_'],
                                                  lum,
                                                  histdir , s, k_ztot,
                                                  pathNamesZ, itemplates, suffixes[itag], verbose=False )
        zbxHists.append( izbx )
        zcxHists.append( izcx )
        zqqHists.append( izqq )        



# ---------------------------------------------
# ---------------------------------------------
#                   STEP 2 : Single Top
# ---------------------------------------------
# ---------------------------------------------

singleTopHists = []


singleTopSamples = [
    ['SingleToptW_', f_st_tW, xs_st_tW, n_st_tW],
    ['SingleTopT_',  f_st_t,  xs_st_t,  n_st_t],
    ['SingleTopS_',  f_st_s,  xs_st_s,  n_st_s]
    ]

singleTopLabel = 'SingleTop_'


for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        tagDist = tagDists[itag]
        #if (ijet >3 and itag ==2):
        #    s = 'dijetMass_' + str(ijet) + 'j_' + str(itag) + 't'
        #    print s
        #else:
        s = tagDist + '_' + str(ijet) + 'j_' + str(itag) + 't'
        hist = addSingleTops( singleTopLabel, lum, histdir, templatedir, s , 1.0,
                              singleTopSamples)
        singleTopHists.append(hist)


# ---------------------------------------------
# ---------------------------------------------
#              STEP 3 : QCD From Fits to Data
# ---------------------------------------------

qcdDataHists = []
if useDataQCD :

    qcd_0tag_data_names = [
    'h_qcd_'+var0tag+'_1j_0t',
    'h_qcd_'+var0tag+'_2j_0t',
    'h_qcd_'+var0tag+'_3j_0t',
    'h_qcd_'+var0tag+'_4j_0t',
    'h_qcd_'+var0tag+'_5j_0t'

        ]

    if options.makePretagPlots is False:
        qcd_data_names = [
            'h_qcd_'+var1tag+'_1j_1t',
            'h_qcd_'+var1tag+'_2j_1t',
            'h_qcd_'+var1tag+'_3j_1t',
            'h_qcd_'+var1tag+'_4j_1t',
            'h_qcd_'+var1tag+'_5j_1t'            
            ]
        qcd_data_names2 = [
            'h_qcd_'+var2tag+'_2j_2t',
            'h_qcd_'+var2tag+'_3j_2t',
            #'h_qcd_dijetMass_4j_2t',
            #'h_qcd_dijetMass_5j_2t',
            'h_qcd_'+var2tag+'_4j_2t',
            'h_qcd_'+var2tag+'_5j_2t'
        ]

    else :
        qcd_data_names = [
            'h_qcd_'+var0tag+'_1j_1t',
            'h_qcd_'+var0tag+'_2j_1t',
            'h_qcd_'+var0tag+'_3j_1t',
            'h_qcd_'+var0tag+'_4j_1t',
            'h_qcd_'+var0tag+'_5j_1t'            
            ]
        qcd_data_names2 = [
            'h_qcd_'+var0tag+'_2j_2t',
            'h_qcd_'+var0tag+'_3j_2t',
            'h_qcd_'+var0tag+'_4j_2t',
            'h_qcd_'+var0tag+'_5j_2t'
            ] 

    for ijet in range (1, maxJets):
        h0 = f_qcd_data.Get( qcd_0tag_data_names[ijet-1]).Clone()
        h0.SetName('QCD_B_'+var0tag+'_'+ str(ijet) + 'j_0t')
        qcdDataHists.append( h0 )
        
        h1 = f_qcd_data.Get( qcd_data_names[ijet-1]).Clone()
        if options.makePretagPlots is False :
            h1.SetName('QCD_B_'+var1tag+'_'+ str(ijet) + 'j_1t')
        else :
            h1.SetName('QCD_B_'+var0tag+'_'+ str(ijet) + 'j_1t')            
        qcdDataHists.append( h1 )
        if ijet > 1 :
            if options.makePretagPlots is False :
                h2 = f_qcd_data.Get( qcd_data_names2[ijet-2]).Clone()
                #if ijet>3:
                #    h2.SetName('QCD_B_dijetMass_'+ str(ijet) + 'j_2t')
                #else:    
                h2.SetName('QCD_B_'+var2tag+'_'+ str(ijet) + 'j_2t')
                qcdDataHists.append( h2 )
            else:
                h2 = f_qcd_data.Get( qcd_data_names2[ijet-2]).Clone()
                h2.SetName('QCD_B_'+var0tag+'_'+ str(ijet) + 'j_2t')
                qcdDataHists.append( h2 )
            
# ---------------------------------------------
# ---------------------------------------------
#                   STEP 4 : Simple hists
# ---------------------------------------------
# ---------------------------------------------

quicksamples = []

if not useDataQCD and not options.noQCD :
    quicksamples.append( ['QCD_', f_qcd, f_qcd,    xs_qcd,   n_qcd,   False] )

quicksamples.append( ['Top_', f_ttbar, f_ttbar,  xs_ttbar, n_ttbar, False] )

if useData :
    quicksamples.append( ['Data_', f_data, f_data, 1.0, None, True ] )

allsimpleHists = []
for isample in range(0,len(quicksamples)) :
    simpleHists = []
    for ijet in range(1,maxJets) :
        for itag in range(0,maxTags) :
            if itag > ijet :
                continue
            if quicksamples[isample][0] is not 'Data_' :
                hist = addSimple( lum, histdir, templatedir, tagDists[itag]+'_'+str(ijet)+'j_'+str(itag)+'t', 1.0,
                                  quicksamples[isample])
            else :
                hist = addSimple( lum, histdirData, None, tagDists[itag]+'_'+str(ijet)+'j_'+str(itag)+'t', 1.0,
                                  quicksamples[isample])
            simpleHists.append(hist)
    allsimpleHists.append( simpleHists )


# ---------------------------------------------
# ---------------------------------------------
#                   STEP 5 : Print it all out
# ---------------------------------------------
# ---------------------------------------------



f_out.cd()

allHists = [
    wbxHists,
    wcxHists,
    wqqHists,
    zbxHists,
    zcxHists,
    zqqHists,
    singleTopHists
    ]
if useDataQCD :
    allHists.append( qcdDataHists )

for iall in allsimpleHists :
    allHists.append( iall )

table = [
    ['1 jet', '0 tag', []],
    ['1 jet', '1 tag', []],
    ['2 jet', '0 tag', []],
    ['2 jet', '1 tag', []],
    ['2 jet', '2 tag', []],
    ['3 jet', '0 tag', []],
    ['3 jet', '1 tag', []],
    ['3 jet', '2 tag', []],
    ['4 jet', '0 tag', []],
    ['4 jet', '1 tag', []],
    ['4 jet', '2 tag', []],
    ['5 jet', '0 tag', []],
    ['5 jet', '1 tag', []],
    ['5 jet', '2 tag', []]
    ]

headers = [
    'Wbx', 'Wcx', 'Wqq',
    'Zbx', 'Zcx', 'Zqq',
    'Single Top']
if useDataQCD :
    headers.append( 'QCD' )
else :
    headers.append( 'QCD (MC)' )

headers.append('Top')


if useData :
    headers.append( 'Data' )


ihistgroup = 0
for histgroup in allHists :
    ihistgroup = ihistgroup + 1
    itable = 0
    for ihist in histgroup :
        table[itable][2].append( ihist.Integral() )
        ihist.Write()
        itable = itable + 1        


from operator import itemgetter, attrgetter

sortedtable = sorted(table, key=itemgetter(1,0))

print  '                  ',
for iheader in headers :
    print '& {0:>10s}'.format( iheader),
print '\\\\'

for itable in sortedtable:
    s = ' {0:15s} '
    print s.format( itable[0] + ', ' + itable[1] ),
    numbers = itable[2]
    for number in numbers :
        print ' & {0:8.2f} '.format( number ),
    print '\\\\'

s = ' {0:15s} '
print s.format( 'Total' ),

from quicksumtable import *

for icol in range(0, len(headers) ) :
    print ' & {0:8.2f} '.format( quicksumtable( sortedtable, icol ) ),
print '\\\\'

#if options.noQCD:
#     sys.exit()

# ---------------------------------------------
# ---------------------------------------------
#                   STEP 6 : >=3 jet and >=4 jet cut-and-count
# ---------------------------------------------
# ---------------------------------------------

from geNJets import *
from doCutAndCount_ele import *

for isignalRegion in [3, 4] :
    wbx_signalregion = geNJets( wbxHists, isignalRegion )
    wcx_signalregion = geNJets( wcxHists, isignalRegion )
    wqq_signalregion = geNJets( wqqHists, isignalRegion )

    zbx_signalregion = geNJets( zbxHists, isignalRegion )
    zcx_signalregion = geNJets( zcxHists, isignalRegion )
    zqq_signalregion = geNJets( zqqHists, isignalRegion )

    singleTop_signalregion = geNJets( singleTopHists, isignalRegion )

    qcd_signalregion = -1
    top_signalregion = -1
    if useDataQCD :
        qcd_signalregion = geNJets( qcdDataHists, isignalRegion )
        top_signalregion = geNJets( allsimpleHists[0], isignalRegion )
        if useData :
            data_signalregion = geNJets( allsimpleHists[1], isignalRegion)
    else :
        qcd_signalregion = geNJets( allsimpleHists[0], isignalRegion )
        top_signalregion = geNJets( allsimpleHists[1], isignalRegion )
        if useData :
            data_signalregion = geNJets( allsimpleHists[2], isignalRegion)        


    print '--------------- >= ' + str(isignalRegion) + ' jet Counts -------------'
    print 'Wbx        : {0:6.2f}'.format( wbx_signalregion )
    print 'Wcx        : {0:6.2f}'.format( wcx_signalregion )
    print 'Wqq        : {0:6.2f}'.format( wqq_signalregion )
    print 'Zbx        : {0:6.2f}'.format( zbx_signalregion )
    print 'Zcx        : {0:6.2f}'.format( zcx_signalregion )
    print 'Zqq        : {0:6.2f}'.format( zqq_signalregion )
    print 'Single top : {0:6.2f}'.format( singleTop_signalregion )
    print 'QCD        : {0:6.2f}'.format( qcd_signalregion )
    print 'Top        : {0:6.2f}'.format( top_signalregion )
    if useData :
        print 'Data       : {0:6.2f}'.format( data_signalregion )
        doCutAndCount( lum,
                       top_signalregion,
                       singleTop_signalregion,
                       qcd_signalregion,
                       wbx_signalregion,
                       wcx_signalregion,
                       wqq_signalregion,                       
                       zbx_signalregion,
                       zcx_signalregion,
                       zqq_signalregion,
                       data_signalregion 
                       )




# ---------------------------------------------
# ---------------------------------------------
#                   STEP 6 : >=2 tag, >=3 jet cut-and-count
# ---------------------------------------------
# ---------------------------------------------

from geNTags import *

for isignalRegion in [2] :
    wbx_signalregion = geNTags( wbxHists, isignalRegion )
    wcx_signalregion = geNTags( wcxHists, isignalRegion )
    wqq_signalregion = geNTags( wqqHists, isignalRegion )

    zbx_signalregion = geNTags( zbxHists, isignalRegion )
    zcx_signalregion = geNTags( zcxHists, isignalRegion )
    zqq_signalregion = geNTags( zqqHists, isignalRegion )

    singleTop_signalregion = geNTags( singleTopHists, isignalRegion )

    qcd_signalregion = -1
    top_signalregion = -1
    if useDataQCD :
        qcd_signalregion = geNTags( qcdDataHists, isignalRegion )
        top_signalregion = geNTags( allsimpleHists[0], isignalRegion )
        if useData :
            data_signalregion = geNTags( allsimpleHists[1], isignalRegion)
    else :
        qcd_signalregion = geNTags( allsimpleHists[0], isignalRegion )
        top_signalregion = geNTags( allsimpleHists[1], isignalRegion )
        if useData :
            data_signalregion = geNTags( allsimpleHists[2], isignalRegion)        


    print '--------------- >= ' + str(isignalRegion) + ' tag Counts -------------'
    print 'Wbx        : {0:6.2f}'.format( wbx_signalregion )
    print 'Wcx        : {0:6.2f}'.format( wcx_signalregion )
    print 'Wqq        : {0:6.2f}'.format( wqq_signalregion )
    print 'Zbx        : {0:6.2f}'.format( zbx_signalregion )
    print 'Zcx        : {0:6.2f}'.format( zcx_signalregion )
    print 'Zqq        : {0:6.2f}'.format( zqq_signalregion )
    print 'Single top : {0:6.2f}'.format( singleTop_signalregion )
    print 'QCD        : {0:6.2f}'.format( qcd_signalregion )
    print 'Top        : {0:6.2f}'.format( top_signalregion )
    if useData :
        print 'Data       : {0:6.2f}'.format( data_signalregion )
        doCutAndCount( lum,
                       top_signalregion,
                       singleTop_signalregion,
                       qcd_signalregion,
                       wbx_signalregion,
                       wcx_signalregion,
                       wqq_signalregion,                       
                       zbx_signalregion,
                       zcx_signalregion,
                       zqq_signalregion,
                       data_signalregion,
                       isignalRegion
                       )
        


f_out.Close()
