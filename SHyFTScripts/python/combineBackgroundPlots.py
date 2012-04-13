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


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--input', metavar='F', type='string', action='store',
                  default='v17_allsys',
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
                  default='btagReweighted71pb_jes',
                  dest='outputLabel',
                  help='output label for the output root file')

parser.add_option('--minJets', metavar='N', type='int', action='store',
                  default=1,
                  dest='minJets',
                  help='Minimum number of jets')

parser.add_option('--useData', metavar='B', action='store_true',
                  default=False,
                  dest='useData',
                  help='Use data in estimates')

parser.add_option('--useDataQCD', metavar='B', action='store_true',
                  default=False,
                  dest='useDataQCD',
                  help='Use data-driven QCD in estimates')

parser.add_option('--lum', metavar='L', action='store',
                  default=15.0,
                  dest='lum',
                  help='Luminosity of the data')

(options, args) = parser.parse_args()

inFileEnd = options.input
tempstr   = options.histdir
outlabel  = options.outputLabel
minJets   = options.minJets
useData   = options.useData
useDataQCD = options.useDataQCD

histdir = tempstr+'/'
outfilestr = tempstr + '_' + outlabel
histdirData = options.histdirData + '/'
templatedir = options.templatedir + '/'

argv = []


from ROOT import *
from array import *

from stitchFlavorHistory import *
from addSingleTops import *
from addSimple import *

# load up root
gROOT.Macro("rootlogon.C")

# ---------------------------------------------
# Get the files from whatever samples you want to stitch
# ---------------------------------------------
f_ttbar = TFile('TTbarJets-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')
f_wjets = TFile('WJets-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')
f_zjets = TFile('ZJets-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')
f_vqq   = TFile('VqqJets-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')
f_qcd   = TFile('InclusiveMu15_shyftana_38xOn35x_'+inFileEnd+'.root')
f_st_s  = TFile('SingleTop_sChannel-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')
f_st_t  = TFile('SingleTop_tChannel-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')
f_st_tW = TFile('SingleTop_tWChannel-madgraph_shyftana_38xOn35x_'+inFileEnd+'.root')

#f_data   = TFile('shyftStudies_data_2sep2010.root')
f_data = TFile('data_15invpb_anashyft_v2.root')
if useDataQCD :
    if tempstr.find('pf') > -1 :
        f_qcd_data = TFile('pf_normalized_qcd_templates.root')
        f_qcd_data_0tag_templates = TFile('pf_0tag_scaled_qcd_templates.root')
    elif tempstr.find('jpt') > -1 :
        f_qcd_data = TFile('jpt_normalized_qcd_templates.root')    
        f_qcd_data_0tag_templates = TFile('jpt_0tag_scaled_qcd_templates.root')

# ---------------------------------------------
# Assumed luminosity (pb-1)
# ---------------------------------------------
lum = options.lum

globalSF = 0.91 # From muon trigger efficiency

# ---------------------------------------------
# Leading order cross sections (pb)
# ---------------------------------------------
xs_ttbar =   157.5 * globalSF
xs_wjets = 24170.0 * globalSF # LO
xs_wtot  = 31314.0 * globalSF # NNLO
xs_zjets =  3048.0 * globalSF
xs_vqq   =    35.8 * globalSF
xs_qcd   = 79688.0 * globalSF
xs_st_t  =    20.93 * globalSF
xs_st_s  =     0.0 * globalSF # xs_singS  =     4.6 * 0.32442
xs_st_tW =    10.6 * globalSF


# ---------------------------------------------
# Relative "k" factors.
# There is an overall K-factor to get to the
# NLO (or NNLO) cross section,
# and then individual factors for each
# heavy flavor species, which can be different.
# ---------------------------------------------

k_wtot = xs_wtot / xs_wjets
s_wbb = 1.0
s_wcc = 1.0
s_wqq = 1.0


# ---------------------------------------------
# Number of generated events
# ---------------------------------------------
n_ttbar =  1483404
n_wjets = 10068895
n_zjets =  1084921
n_vqq   =   936242
n_qcd   =  4377187
n_st_t  =   528593
n_st_s  =   412055
n_st_tW =   466437

# ---------------------------------------------
# get the output file
# ---------------------------------------------
f_out = TFile('shyftPlots_stitched_' + outfilestr + '.root', 'RECREATE')

# ---------------------------------------------
# Template name
# ---------------------------------------------
#histnameTag = 'secvtxMass_'
#histnames0Tag = ['muEta']
#histnames0Tag = ['MET', 'hT', 'wMT', 'muEta']
#histnamesSing = ['nJets', 'nTags', 'm3']


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
    ['VqqW_path1'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 1
    ['VqqW_path2'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 2
    ['VqqW_path3'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 3
    ['WjetsW_path4'    , f_wjets ,n_wjets, xs_wjets ],# path 4
    ['WjetsW_path5'    , f_wjets ,n_wjets, xs_wjets ],# path 5
    ['WjetsW_path6'    , f_wjets ,n_wjets, xs_wjets ],# path 6
    ['WjetsW_path11'   , f_wjets ,n_wjets, xs_wjets ],# path 11
    ]

pathNamesZ = [
    ['VqqZ_path1'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 1
    ['VqqZ_path2'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 2
    ['VqqZ_path3'      , f_vqq   ,n_vqq,   xs_vqq   ],# path 3
    ['ZjetsZ_path4'    , f_zjets ,n_zjets, xs_zjets ],# path 4
    ['ZjetsZ_path5'    , f_zjets ,n_zjets, xs_zjets ],# path 5
    ['ZjetsZ_path6'    , f_zjets ,n_zjets, xs_zjets ],# path 6
    ['ZjetsZ_path11'   , f_zjets ,n_zjets, xs_zjets ] # path 11    
    ]

suffixes = [
    ['_b', '_c', '_q'],
    ['_b', '_c', '_q'],
    ['_b', '_c', '_q'],    
    ]



bmass = f_ttbar.Get( templatedir + 'bmass')
cmass = f_ttbar.Get( templatedir + 'cmass')
lfmass = f_wjets.Get( templatedir + 'lfmass')

bmass.Scale(1.0/bmass.Integral())
cmass.Scale(1.0/cmass.Integral())
lfmass.Scale(1.0/lfmass.Integral())

templates = [bmass, cmass, lfmass]
ibmass = 0
icmass = 1
ilfmass = 2

tagDists = [
    'muEta',
    'secvtxMass',
    'secvtxMass'
    ]
wjetsTemplates = [
    None,
    templates,
    templates
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
        s = tagDist + '_' + str(ijet) + 'j_' + str(itag) + 't'
        [iwbx, iwcx, iwqq] = stitchFlavorHistory( ['Wbx_', 'Wcx_', 'Wqq_'],
                                                  lum,
                                                  histdir , s, k_wtot,
                                                  pathNamesW, itemplates, suffixes[itag], verbose=False )
        wbxHists.append( iwbx )
        wcxHists.append( iwcx )
        wqqHists.append( iwqq )        

        [izbx, izcx, izqq] = stitchFlavorHistory( ['Zbx_', 'Zcx_', 'Zqq_'],
                                                  lum,
                                                  histdir , s, k_wtot,
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
    ['SingleTopTWChan_', f_st_tW, xs_st_tW, n_st_tW],
    ['SingleTopTChan_',  f_st_t,  xs_st_t,  n_st_t],
    ['SingleTopSChan_',  f_st_s,  xs_st_s,  n_st_s]
    ]

singleTopLabel = 'SingleTop_'


for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        tagDist = tagDists[itag]
        hist = addSingleTops( singleTopLabel, lum, histdir, templatedir, tagDist+'_'+str(ijet)+'j_'+str(itag)+'t', 1.0,
                              singleTopSamples)
        singleTopHists.append(hist)


# ---------------------------------------------
# ---------------------------------------------
#                   STEP 3 : QCD From Data
# ---------------------------------------------

qcdDataHists = []
if useDataQCD :

    qcd_0tag_data_names = [
    'proj_Data_muEta_QCD_1_0t',
    'proj_Data_muEta_QCD_2_0t',
    'proj_Data_muEta_QCD_3_0t',
    'proj_Data_muEta_QCD_4_0t',
    'proj_Data_muEta_QCD_5_0t'

        ]

    
    qcd_data_names = [
    'proj_Data_secvtxMass_1_1t',
    'proj_Data_secvtxMass_2_1t',
    'proj_Data_secvtxMass_3_1t',
    'proj_Data_secvtxMass_4_1t',
    'proj_Data_secvtxMass_5_1t'

        ]

    for ijet in range (1, maxJets):
        h0 = f_qcd_data_0tag_templates.Get( qcd_0tag_data_names[ijet-1]).Clone()
        h0.SetName('QCD_B_muEta_'+ str(ijet) + 'j_0t')
        qcdDataHists.append( h0 )
        
        h1 = f_qcd_data.Get( qcd_data_names[ijet-1]).Clone()
        h1.SetName('QCD_B_secvtxMass_'+ str(ijet) + 'j_1t')
        qcdDataHists.append( h1 )
        if ijet > 1 :
            h2 = TH1F('QCD_B_secvtxMass_'+ str(ijet) + 'j_2t',
                      'QCD_B_secvtxMass_'+ str(ijet) + 'j_2t',
                      h1.GetNbinsX(),
                      h1.GetXaxis().GetBinLowEdge(1),
                      h1.GetXaxis().GetBinLowEdge(h1.GetNbinsX() + 1),
                      )
            qcdDataHists.append(h2)


# ---------------------------------------------
# ---------------------------------------------
#                   STEP 4 : Simple hists
# ---------------------------------------------
# ---------------------------------------------

quicksamples = []

if useDataQCD is False :
    quicksamples.append( ['QCD_', f_qcd,     xs_qcd,   n_qcd,   False] )

quicksamples.append( ['Top_', f_ttbar,   xs_ttbar, n_ttbar, False] )

if useData :
    quicksamples.append( ['Data_', f_data, 1.0, None, True ] )

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
    headers.append( 'QCD (Data)' )
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


# ---------------------------------------------
# ---------------------------------------------
#                   STEP 6 : >=3 jet and >=4 jet cut-and-count
# ---------------------------------------------
# ---------------------------------------------

from geNJets import *
from doCutAndCount import *

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
