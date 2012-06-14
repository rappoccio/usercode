#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()



parser.add_option('--outname', metavar='D', type='string', action='store',
                  default='plotResponse',
                  dest='outname',
                  help='Output name')


(options, args) = parser.parse_args()

argv = []

from ROOT import *

from array import *

gROOT.Macro("rootlogon.C")

bins = array('d', [])
fbins = open('fbinsFromKostas.txt', 'r')
binlines = fbins.readlines()
for binline in binlines :
    bins.append( float(binline.rstrip())  )
nbins = len(bins)-1

h = TH2D('h', 'h', nbins, bins, nbins, bins )


for i in xrange(1000):
  #xt= pow(10.0, gRandom.Uniform()) / 10.0 * 7.
  #xt = h1dMC.GetRandom() / 1000.
  #xt = gRandom.Uniform() * 4.
  itrand = int( gRandom.Uniform() * float(len(bins)))
  xt = bins[itrand] + 0.001

  for j in xrange(100):
      x = gRandom.Gaus(xt, xt * 0.05)
      h.Fill(xt, x)

#h.FillRandom('func', 10000)

h.Draw('colz')
h.Draw('box same')
h.GetXaxis().SetRangeUser(200., 4000.)
h.GetYaxis().SetRangeUser(200., 4000.)
gPad.SetLogx()
gPad.SetLogy()

h.GetXaxis().SetMoreLogLabels()
h.GetXaxis().SetNoExponent()
h.GetYaxis().SetMoreLogLabels()
h.GetYaxis().SetNoExponent()
gPad.Update()
