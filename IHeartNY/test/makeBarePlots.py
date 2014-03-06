#!/usr/bin/env python
# ==============================================================================
# January 2014
# ==============================================================================

import time
import copy
from optparse import OptionParser


parser = OptionParser()

  

parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='mujets',
                  dest='outname',
                  help='Output name for png and pdf files')


parser.add_option('--hist', metavar='F', type='string', action='store',
                  default='ptRecoTop',
                  dest='hist',
                  help='Histogram to plot')
                  
                  
parser.add_option('--NQCD', metavar='F', type='float', action='store',
                  default=15.0 ,
                  dest='NQCD',
                  help='QCD Normalization')
                  

parser.add_option('--maxy', metavar='F', type='float', action='store',
                  default=500,
                  dest='maxy',
                  help='Maximum y in histogram')

parser.add_option('--ignoreData', metavar='F', action='store_true',
                  default=False,
                  dest='ignoreData',
                  help='Ignore plotting data')

parser.add_option('--ignoreQCD', metavar='F', action='store_true',
                  default=False,
                  dest='ignoreQCD',
                  help='Ignore plotting QCD')


parser.add_option('--drawLegend', metavar='F', action='store_true',
                  default=False,
                  dest='drawLegend',
                  help='Draw a legend')

(options, args) = parser.parse_args()

argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor

gROOT.Macro("rootlogon.C")


gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(1.0, "X")
gStyle.SetTitleOffset(1.0, "Y")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(20, "XYZ")


# Performance numbers
lum = 19.7 # fb-1
SF_b = 0.97
SF_t = 1.0
#SF_t = 0.94

# Cross sections (in fb) and the number of MC events
sigma_ttbar_NNLO = 245.8 * 1000.    # fb, from http://arxiv.org/pdf/1303.6254.pdf
sigma_T_t_NNLO = 56.4 * 1000.       # 
sigma_Tbar_t_NNLO = 30.7 * 1000.    # All single-top approx NNLO cross sections from
sigma_T_s_NNLO = 3.79 * 1000.       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
sigma_Tbar_s_NNLO = 1.76 * 1000.    # 
sigma_T_tW_NNLO = 11.1 * 1000.      # 
sigma_Tbar_tW_NNLO = 11.1 * 1000.   # 
sigma_WJets_NNLO = 36703.2 * 1000.  # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV

# MC event counts from B2G twiki here :
# https://twiki.cern.ch/twiki/bin/view/CMS/B2GTopLikeBSM53X#Backgrounds
Nmc_ttbar = 21675970
Nmc_T_t = 3758227
Nmc_Tbar_t = 1935072
Nmc_T_s = 259961
Nmc_Tbar_s = 139974
Nmc_T_tW = 497658
Nmc_Tbar_tW = 493460
Nmc_WJets = 57709905
Nmc_TT_Mtt_700_1000 = 3082812
Nmc_TT_Mtt_1000_Inf = 1249111

# QCD Normalization from MET fits
NQCD = options.NQCD

# ttbar filter efficiencies
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.014
e_TT_Mtt_0_700 = 1.0 - e_TT_Mtt_700_1000 - e_TT_Mtt_1000_Inf
# 


thetaNamingDict = {
    'nom':'',
    'qcd':'qcd',
    'jecdn':'jec__down',
    'jecup':'jec__up',
    'jerdn':'jer__down',
    'jerup':'jer__up',
    'pdfdn':'pdf__down',
    'pdfup':'pdf__up',
    'scaledown':'scale__down',
    'scaleup':'scale__up'
    }
plots = [ 'nom', 'jecdn' , 'jecup' , 'jerdn' , 'jerup' , 'pdfdn' , 'pdfup']# , 'scaledown' , 'scaleup']
canvs = []
histsData = []

# Open the output file 

fout = TFile("normalized_" + options.outname + '_' + options.hist + ".root" , "RECREATE")


# ==============================================================================
#  Example Unfolding
# ==============================================================================


class Sample :
    # make some aliases for indices
    name  = "None"
    hist  = ""
    default="nom"
    color = None
    sysnames = [ 'nom', 'jecdn', 'jecup', 'jerdn', 'jerup', 'qcd']
    files = []
    hists = {}
    def __init__( self, fname, name, hist, norm, color=None, sysnames=None, default=None) : # expects fname to have a {s} where the sysname should go
        self.name = name
        self.hist = hist
        if color != None : 
            self.color = color
        if sysnames != None :
            self.sysnames = sysnames
        if default != None :
            self.default = default
        isys = 0
        for sys in self.sysnames :
            self.files.append( TFile(fname.format(sys) ) )
            h = self.files[isys].Get( self.hist ).Clone()
            if sys == "nom" : 
                h.SetName( self.hist + '__' + self.name  )
            else :
                h.SetName( self.hist + '__' + self.name + '__' + thetaNamingDict[sys] )
            h.Scale( norm )
            if self.color != None : 
                h.SetFillColor( self.color )
            else :
                h.SetMarkerStyle( 20 )
            self.hists[sys] = h 
            isys+=1

    def setName( self, name ) :
        self.name = name
            
    def operate_(self, samples, sign=+1.0, hist=None ) :
        """ Add or subtract  histograms from a bunch of samples to this sample
        """
        if hist != None : 
            for relative in samples : 
                self.hists[hist].Add( relative.hists[hist], sign )
        else : 
            for relative in samples : 
                for sys in self.sysnames :
                    self.hists[sys].Add( relative.hists[sys], sign )

    def add( self, samples, hist=None ) :
        """ Convenience function for adding
        """        
        self.operate_( samples, hist=hist, sign=+1.0  )
    def sub( self, samples, hist=None ) :
        """ Convenience function for subtracting
        """        
        self.operate_( samples, hist=hist, sign=-1.0 )
                            
    def get(self, hist) :
        """ Return a histogram with description "hist"
        """
        if hist in self.hists : 
            return self.hists[hist]
        else :
            print '%%% INFO : histogram ' + hist + ' not found for species ' + self.name + ', using default = ' + self.default
            return self.hists[self.default]
    def writeForTheta(self, fout) :
        fout.cd()
        for key,hist in self.hists.iteritems() :
            if hist != None :
                hist.Write()        


Data            = Sample (fname="histfiles/SingleMu_iheartNY_V1_mu_Run2012_{0}_type1.root",
                            name="DATA",
                            hist=options.hist,
                            norm=1.0,
                            color=None,
                            sysnames=["nom"]
                            )
QCD             = Sample( fname="histfiles/SingleMu_iheartNY_V1_mu_Run2012_{0}_type1.root",
                            name="QCD_SingleMu",
                            hist=options.hist,
                            norm=options.NQCD,
                            color=TColor.kYellow,
                            sysnames = ["qcd"],
                            default='qcd'
                            )
T_t             = Sample( fname="histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="T_t",
                            hist=options.hist,
                            color=TColor.kMagenta,
                            norm = sigma_T_t_NNLO*lum / float(Nmc_T_t) * SF_b * SF_t
                            )
Tbar_t          = Sample( fname="histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="Tbar_t",
                            hist=options.hist,
                            color=TColor.kMagenta,
                            norm = sigma_Tbar_t_NNLO*lum / float(Nmc_Tbar_t) * SF_b * SF_t
                            )
T_s             = Sample( fname="histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="T_s",
                            hist=options.hist,
                            color=TColor.kMagenta,
                            norm = sigma_T_s_NNLO*lum / float(Nmc_T_s) * SF_b * SF_t
                            )
Tbar_s          = Sample( fname="histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_{0}_type1.root",
                            name="Tbar_s",
                            hist=options.hist,
                            color=TColor.kMagenta,
                            norm = sigma_Tbar_s_NNLO*lum / float(Nmc_Tbar_s) * SF_b * SF_t
                            )
T_tW            = Sample( fname="histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="T_tW",
                            hist=options.hist,
                            color=TColor.kMagenta,
                            norm = sigma_T_tW_NNLO*lum / float(Nmc_T_tW) * SF_b * SF_t
                            )
Tbar_tW         = Sample( fname="histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="Tbar_tW",
                            hist=options.hist,
                            color=TColor.kMagenta,
                            norm = sigma_Tbar_tW_NNLO*lum / float(Nmc_Tbar_tW) * SF_b * SF_t
                            )
WJets           = Sample( fname="histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_{0}_type1.root",
                            name="WJets",
                            hist=options.hist,
                            color=TColor.kGreen,
                            norm = sigma_WJets_NNLO*lum / float(Nmc_WJets) * SF_b * SF_t
                            )
TT_Mtt_0_700    = Sample( fname="histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="TT_Mtt_0_700",
                            hist=options.hist,
                            color=TColor.kRed,
                            norm = sigma_ttbar_NNLO*lum / float(Nmc_ttbar) * SF_b * SF_t * e_TT_Mtt_0_700,
                            sysnames = [ 'nom', 'jecdn', 'jecup', 'jerdn', 'jerup', 'pdfup', 'pdfdn', 'qcd']
                            )
TT_Mtt_700_1000 = Sample( fname="histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="TT_Mtt_700_1000",
                            hist=options.hist,
                            color=TColor.kRed,
                            norm = sigma_ttbar_NNLO*lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t * e_TT_Mtt_700_1000,
                            sysnames = [ 'nom', 'jecdn', 'jecup', 'jerdn', 'jerup', 'pdfup', 'pdfdn', 'qcd']
                            )
TT_Mtt_1000_Inf = Sample( fname="histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_{0}_type1.root",
                            name="TT_Mtt_1000_Inf",
                            hist=options.hist,
                            color=TColor.kRed,
                            norm = sigma_ttbar_NNLO*lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t * e_TT_Mtt_1000_Inf,
                            sysnames = [ 'nom', 'jecdn', 'jecup', 'jerdn', 'jerup', 'pdfup', 'pdfdn', 'qcd']
                            )



SingleTop = copy.deepcopy(T_t)
SingleTop.add( samples=[Tbar_t, T_s, Tbar_s, T_tW, Tbar_tW] )
SingleTop.setName ( "SingleTop" )
TTbar = copy.deepcopy( TT_Mtt_0_700)
TTbar.add( samples=[TT_Mtt_700_1000, TT_Mtt_1000_Inf] )
TTbar.setName ( "TTbar" )
QCD.sub( samples=[SingleTop,WJets,TTbar], hist="qcd")

#fTT_Mtt_less_700_scaledown = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown_type1.root")
#fTT_Mtt_less_700_scaleup   = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup_type1.root")
#fTT_Mtt_700_1000_scaledown = TFile("histfiles/TT_700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown_type1.root")
#fTT_Mtt_700_1000_scaleup   = TFile("histfiles/TT_700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup_type1.root")
#fTT_Mtt_1000_Inf_scaledown = TFile("histfiles/TT_1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown_type1.root")
#fTT_Mtt_1000_Inf_scaleup   = TFile("histfiles/TT_1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup_type1.root")



print "==================================== Get Hists ====================================="

stacks = []

legs = []

for m in range(0,len(plots)):

    

    leg = TLegend(0.5, 0.55, 0.84, 0.84)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)

    hMeas_TTbar     = TTbar.get(plots[m])
    hMeas_SingleTop = SingleTop.get(plots[m])
    hMeas_WJets     = WJets.get(plots[m])
    hMeas_QCD       = QCD.get(plots[m])

    hRecoData       = Data.get(plots[m])
     
    leg.AddEntry( hMeas_TTbar, 't#bar{t}', 'f')
    leg.AddEntry( hMeas_SingleTop, 'single top', 'f')
    leg.AddEntry( hMeas_WJets, 'W+jets', 'f')
    leg.AddEntry( hMeas_QCD, 'QCD' , 'f')

    
    if 'vtxMass' in  options.hist :
        for zerohist in [hMeas_WJets, hMeas_SingleTop, hMeas_TTbar, hMeas_QCD ] :
            zerohist.SetBinContent(1, 0.0)
        if options.ignoreData == False :
            hRecoData.SetBinContent(1, 0.0)
    
    # Make a stack plot of the MC to compare to data
    hMC_stack = THStack("hMC_stack",
                        hMeas_TTbar.GetTitle() + ';' +
                        hMeas_TTbar.GetXaxis().GetTitle() + ';' +
                        hMeas_TTbar.GetYaxis().GetTitle()
                        )
    hMC_stack.Add( hMeas_QCD )
    hMC_stack.Add( hMeas_WJets )
    hMC_stack.Add( hMeas_SingleTop )
    hMC_stack.Add( hMeas_TTbar )


    print 'Normalizations : ttbar = {0:10.2f}, single top = {1:10.2f}, wjets = {2:10.2f}, qcd = {3:10.2f}   ===== data = {4:10.2f}'.format(
        hMeas_TTbar.Integral(), hMeas_SingleTop.Integral(), hMeas_WJets.Integral(), hMeas_QCD.Integral(), hRecoData.Integral()
            )

    stacks.append( hMC_stack )
    # TO DO : NEED TO FIX THE BINNING FOR QCD : 
    #MC_stack.Add( hRecoQCD )
    #hMC_stack.Add( hRecoMC )

   
    c = TCanvas("datamc" + plots[m] , "datamc" + plots[m])
    if not options.ignoreData :
        leg.AddEntry( hRecoData, '19.6 fb^{-1}', 'p')
        hRecoData.UseCurrentStyle()
        hRecoData.Draw('e')
        hMC_stack.Draw("hist same")
        hRecoData.Draw('e same')
        hRecoData.SetMaximum( options.maxy )
    else :
        hMC_stack.UseCurrentStyle()
        hMC_stack.Draw("hist")
    if options.drawLegend :
        leg.Draw()

    canvs.append(c)
    legs.append(leg)
    if not options.ignoreData : 
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '.png' )
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '.pdf' )
    else : 
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '_nodata.png' )
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '_nodata.pdf' )


        
    # write the histogram in a rootfile



for sample in [Data, QCD, TTbar, SingleTop, WJets]:
    sample.writeForTheta(fout)

fout.Close()
   
    
