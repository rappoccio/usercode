#!/usr/bin/env python
# ==============================================================================
#  File and Version Information:
#       $Id: RooUnfoldExample.py 302 2011-09-30 20:39:20Z T.J.Adye $
#
#  Description:
#       Simple example usage of the RooUnfold package using toy MC.
#
#  Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================


from optparse import OptionParser

parser = OptionParser()


parser.add_option('--samples', metavar='F', type='string', action='append',
                  default=['pythia6_z2','pythia8_4c','herwigpp_23'],
                  dest='samples',
                  help='Samples')


parser.add_option('--sys', metavar='F', type='string', action='append',
                  default=['jecup', 'jecdn'],
                  dest='sys',
                  help='Systematics')


(options, args) = parser.parse_args()


from ROOT import *

gROOT.Macro("rootlogon.C")


from array import *

# ==============================================================================
#  Example Unfolding
# ==============================================================================

files = []
for sample in options.samples:
    f = TFile("unfoldOut_" + sample + ".root") 
    files.append( f )

files_sys = []
sysnominal = options.samples[0]
for sys in options.sys:
    f = TFile("unfoldOut_" + sysnominal + '_' + sys + ".root") 
    files_sys.append( f )

stacks = []
colors = [2, 8, 4]
canvs = []

finalPlots = []


for iptBin in range(2,10) :
    print 'Looking at pt bin ' + str(iptBin)
    hs = THStack( 'hs' + str(iptBin), 'hs' + str(iptBin) )
    for isample in range(0,len(options.samples)) :
        print 'Getting response_' + options.samples[isample] + '_pt' + str(iptBin)
        hist = files[isample].Get( 'response_' + options.samples[isample] + '_pt' + str(iptBin) )
        hist.SetLineColor(colors[isample])
        hist.SetLineWidth(1)
        hs.Add( hist )
        if isample == 0 :
            hfinal = hist.Clone()
            hfinal.SetName('hfinal' + str(iptBin) )
            hfinal.SetLineColor(1)
            finalPlots.append(hfinal)
            
            for isys in range(0,len(options.sys)):
                print 'Getting response_' + options.samples[isample] + '_pt' + str(iptBin) + '_' + options.sys[isys]
                syshist = files_sys[isys].Get( 'response_' + options.samples[isample] + '_pt' + str(iptBin) + '_' + options.sys[isys] )
                htemp = finalPlots[iptBin-2]
                for ibin in range(1,htemp.GetNbinsX()) :
                    err0 = htemp.GetBinError(ibin)
                    diff = abs(htemp.GetBinContent(ibin) - syshist.GetBinContent(ibin))
                    err1 = sqrt(err0*err0 + diff*diff)
                    htemp.SetBinError( ibin, err1 )
                
            
        elif isample == 2 :
            htemp = finalPlots[iptBin-2]
            for ibin in range(1,htemp.GetNbinsX()) :
                err0 = htemp.GetBinError(ibin)
                diff = abs(htemp.GetBinContent(ibin) - hist.GetBinContent(ibin))
                err1 = sqrt(err0*err0 + diff*diff)
                htemp.SetBinError( ibin, err1 )
                htemp.SetBinError( ibin, diff )

    c = TCanvas('c' + str(iptBin), 'c' + str(iptBin) )
    hs.Draw('nostack hist')
    finalPlots[iptBin-2].Draw('e same')
    stacks.append(hs)
    c.SetLogy()
    canvs.append(c)
    
    
