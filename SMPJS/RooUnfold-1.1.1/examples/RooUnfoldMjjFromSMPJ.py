#!/usr/bin/env python


from optparse import OptionParser


parser = OptionParser()


parser.add_option('--ieta', metavar='F', type='int', action='store',
                  dest='iieta',
                  help='Eta bin to plot: 0: [0.0,0.5]\n'\
                       '                 1: [0.5,1.0]\n'\
                       '                 2: [1.0,1.5]\n'\
                       '                 3: [1.5,2.0]\n'\
                       '                 4: [2.0,2.5]\n'
                  )

(options, args) = parser.parse_args()

argv = []



from ROOT import *

gROOT.Macro("rootlogon.C")





from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
from ROOT import RooUnfoldBinByBin

from array import *


# ==============================================================================
#  Example Unfolding
# ==============================================================================

fbins = open('fbinsFromKostas.txt', 'r')

bins = array('d', [])
binlines = fbins.readlines()
for binline in binlines:
  binstr = binline.rstrip()
  bins.append( float(binstr) )

#print bins

# Get a response matrix that has equal bin sizes when plotted on a log-log plot
## x0 = 0.2
## delta = 0.05
## bins = array('d', [x0, x0 + delta])
## logbins = array('d', [log10(x0), log10(x0+delta)] )
## for ibin in range(2,14) :
##   val = bins[ibin-1]*bins[ibin-1] / bins[ibin-2]
##   bins.append(val)
##   logbins.append(log10(val))

## for ibin in range(0,len(bins)):
##   print 'ibin {0:4.0f} = {1:6.2f}'.format(ibin, bins[ibin])
## for ibin in range(0,len(logbins)):
##   print 'ibin {0:4.0f} = {1:6.4f}'.format(ibin, logbins[ibin])

hbins = TH1F("hbins", "hbins", len(bins)-1, bins)

response= RooUnfoldResponse ( hbins, hbins )
#response = TH2D('responsePlot', 'responsePlot', len(bins)-1, bins, len(bins)-1, bins)

## eta :  0.00- 0.50, A =   0.0275, B =   0.0106, C =   0.8344
## eta :  0.50- 1.00, A =   0.0298, B =   0.0092, C =   0.9796
## eta :  1.00- 1.50, A =   0.0353, B =   0.0068, C =   1.4355
## eta :  1.50- 2.00, A =   0.0248, B =   0.0144, C =   0.6164
## eta :  2.00- 2.50, A =  -9.1008, B =   9.1404, C =   0.0004



# Steps are :
#  1. Input the bins
#   Then, for each eta bin :
#     2. Input histogram of generated spectrum from MC (spectrum_hist)
#     3. Fit spectrum_hist (with spectrum_fit) to the form:
#              [0]*pow(2*x/7000,-[1])*pow(1-x/7000,[2])
#     4. Input resolution function (sigma_yi)
#     for (all toys) :
#       5. Get a deviate for the mass (m) in a uniform distribution (0--3500.)
#       6. The smeared x is a gaussian centered around m with width sigma_yi
#       7. The weight is the reconstructed spectrum at m, divided by the bin width at m


iieta = options.iieta

if iieta > 4 :
  print 'iieta out of range'
  exit()

etabins = [
  0.0, 0.5, 1.0, 1.5, 2.0, 2.5
  ]

resolutionFitParams = [
  [ 0.0275,  0.0275, 0.8344],
  [ 0.0298,  0.0298, 0.9796],
  [ 0.0353,  0.0353, 1.4355],
  [ 0.0248,  0.0248, 0.6164],
  [-9.1008, -9.1008, 0.0004]
  ]

fitRanges = [
  [200, 4000],
  [300, 4000],
  [400, 4000],
  [600, 4000],
  [1000,4000]
  ]

fobs = TFile("rawDataMCComparisons_histAK7MjjVsEtaMax.root")

obsHistRaw = fobs.Get('jetdata_' + str(iieta))


f = TFile("QCD_pythia6_z2_v10beta_plots.root")


cinput = TCanvas('cinput', 'cinput')
cinput.SetLogy()


# Get the 3-dimensional response matrix (mjj vs etamax vs response)
#   and get "this" eta bin's projection along the mjj axis
h2dMC = f.Get('histAK7MjjGenVsEtaMax')
bin0 = h2dMC.GetYaxis().FindBin( etabins[iieta] )
spectrum_hist_yi = h2dMC.ProjectionX('spectrum_hist_yi_0', bin0, bin0)
spectrum_hist_yi.Scale( obsHistRaw.Integral() / spectrum_hist_yi.Integral() )
spectrum_hist_yi.SetTitle('AK7 generated m_{jj}, ' + str(etabins[iieta]) + ' < |#eta_{max}| <' + str(etabins[iieta+1]) +  ';m_{jj} (GeV)')

trueHist = spectrum_hist_yi.Rebin( len(bins)-1, 'trueHist_yi', bins )

# Now fit the generator-level spectrum with a falling function
spectrum_fit_yi = TF1('spectrum_fit_yi', '[0]*pow(2*x/7000,-[1])*pow(1-x/7000,[2])', fitRanges[iieta][0], fitRanges[iieta][1] )
spectrum_fit_yi.SetParameters(1e1, 5, 10)
spectrum_hist_yi.Draw()
gStyle.SetOptStat(000000)
gStyle.SetOptFit(1111)
spectrum_hist_yi.Fit('spectrum_fit_yi', 'R', 'same')

spectrum_hist_yi.GetXaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])

cinput.Print('input_yi_' + str(iieta) + '.png', 'png')
cinput.Print('input_yi_' + str(iieta) + '.pdf', 'pdf')

# Get the resolution function
sigma_yi = TF1('sigma_yi', '[0] + [1] / TMath::Power(x/1000.,[2])', 0, 7000.)
sigma_yi.SetParameter(0, resolutionFitParams[iieta][0])
sigma_yi.SetParameter(1, resolutionFitParams[iieta][1])
sigma_yi.SetParameter(2, resolutionFitParams[iieta][2])

cresponse = TCanvas('cresponse', 'cresponse', 500, 500)

# Loop over a bunch of toys
for ievent in xrange(10000) :
  # m is the mass (the deviate)
  m      = gRandom.Uniform(0.,3500.)

  # d is the width of the binning at mass m
  responseBin = hbins.GetXaxis().FindBin( m )
  d      = hbins.GetBinWidth(responseBin)

  # x_i are the smeared values of m, according to sigma_yi (resolution)
  x_1 = gRandom.Gaus(m,m*sigma_yi.Eval(m))
#  x_2 = gRandom.Gaus(m,1.10*m*fSigma[iy]->Eval(m/1000.))
#  x_3 = gRandom.Gaus(m,0.95*m*fSigma[iy]->Eval(m/1000.))

  # w_i are the weights of the falling generated spectrum,
  #   ultimately divided by the bin width
  w_1 = spectrum_fit_yi.Eval( m )

#  print 'm = {0:6.2f}, d = {1:6.2f}, x_1 = {2:6.2f}, w_1 = {3:6.2f}, w_1/d = {4:6.2f}'.format(
#    m, d, x_1, w_1, w_1 / d )
#  w_2 = fSpectrum[iy].at(1).Eval(m)
#  w_3 = fSpectrum[iy].at(2).Eval(m)
  response.Fill( m, x_1, w_1 / d )



# Plot the response
responsePlot = response.Hresponse()
responsePlot.Sumw2()
responsePlot.SetTitle("Response Matrix, " + str(etabins[iieta]) + ' < |#eta_{max}| <' + str(etabins[iieta+1]) + ";m_{jj}^{GEN} (GeV);m_{jj}^{RECO} (GeV)")
#responsePlot.Scale( 1.0 / responsePlot.Integral() )
responsePlot.Draw('colz')
responsePlot.Draw('box same')
gPad.SetLogy()
gPad.SetLogx()
responsePlot.GetXaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])
responsePlot.GetYaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])
responsePlot.GetXaxis().SetMoreLogLabels()
responsePlot.GetYaxis().SetMoreLogLabels()
responsePlot.GetXaxis().SetNoExponent()
responsePlot.GetYaxis().SetNoExponent()
gPad.Update()
cresponse.Print('response_yi_' + str(iieta) + '.png', 'png')
cresponse.Print('response_yi_' + str(iieta) + '.pdf', 'pdf')


obsHist = obsHistRaw.Rebin( len(bins)-1, 'obsHist_yi', bins )


craw = TCanvas('craw', 'craw')
obsHistRaw.Draw()
craw.SetLogy()
obsHistRaw.GetXaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])

craw.Print('raw_yi_' + str(iieta) + '.png', 'png')
craw.Print('raw_yi_' + str(iieta) + '.pdf', 'pdf')

cobs = TCanvas('cobs', 'cobs')
obsHist.Draw()
cobs.SetLogy()
obsHist.GetXaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])

cobs.Print('obs_yi_' + str(iieta) + '.png', 'png')
cobs.Print('obs_yi_' + str(iieta) + '.pdf', 'pdf')

ctrue = TCanvas('ctrue', 'ctrue')
trueHist.Draw()
ctrue.SetLogy()
trueHist.GetXaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])

ctrue.Print('true_yi_' + str(iieta) + '.png', 'png')
ctrue.Print('true_yi_' + str(iieta) + '.pdf', 'pdf')

for ibin in xrange(0, obsHist.GetNbinsX() ) :
  if obsHist.GetBinContent(ibin) < 1 :
    obsHist.SetBinContent(ibin, 0.0)


#obsHist.Scale( 1.0 / 4900. / 0.5)
## print "==================================== UNFOLD ==================================="
#unfold= RooUnfoldBayes     (response, obsHist, 4)    #  last is regularization parameter
#unfold= RooUnfoldSvd       (response, obsHist, 20)   #  last is regularization parameter
unfold= RooUnfoldBinByBin  (response, obsHist)   #  OR



cunfold=  TCanvas("cunfold","",200,10,960,800)
p1 = TPad("p1","p1",0.0,0.3,1.0,0.97)
p1.SetBottomMargin(0.00)
p1.SetNumber(1)
p2 = TPad("p2","p2",0.0,0.00,1.0,0.3)
p2.SetNumber(2)
p2.SetTopMargin(0.00)
p2.SetBottomMargin(0.33)



p1.cd()
hReco= unfold.Hreco()
hReco.SetTitle(  str(etabins[iieta]) + ' < |#eta_{max}| <' + str(etabins[iieta+1]) + ';;d#sigma / dm_{jj} d#eta')
unfold.PrintTable(cout)
hReco.Draw()
obsHist.SetMarkerStyle(22)
obsHist.Draw('same')
trueHistPretty=trueHist.Clone()
trueHistPretty.SetName( trueHist.GetName() + 'Pretty')
trueHistPretty.SetFillColor(8)
trueHistPretty.Draw('hist same')
hReco.Draw('same')
hReco.GetXaxis().SetRangeUser(fitRanges[iieta][0], fitRanges[iieta][1])


leg = TLegend(0.5, 0.6, 0.8, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.AddEntry( hReco, 'Unfolded', 'p')
leg.AddEntry( obsHist, 'Raw', 'f')
leg.AddEntry( trueHistPretty, 'Truth', 'f')
leg.Draw()
p1.SetLogy()
cunfold.cd()
p1.Draw()
p1.RedrawAxis()

p2.cd()
hRatio = hReco.Clone()
hRatio.SetName(hReco.GetName() + 'Ratio')
hRatio.Sumw2()
trueHistPretty.Sumw2()
hRatio.Add( trueHistPretty, -1.0 )
hRatio.Divide(trueHistPretty)
hRatio.Draw()
hRatio.SetMinimum(-2.0)
hRatio.SetMaximum(2.0)
hRatio.SetTitle(';m_{jj} (GeV);(Reco-True)/True')
hRatio.GetXaxis().SetLabelSize(0.10)
hRatio.GetXaxis().SetTitleSize(0.12)
cunfold.cd()
p2.Draw()


cunfold.Update()
cunfold.Print('unfold_yi_' + str(iieta) + '.png', 'png')
cunfold.Print('unfold_yi_' + str(iieta) + '.pdf', 'pdf')
