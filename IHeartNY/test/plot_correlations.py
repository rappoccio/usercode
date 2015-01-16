from ROOT import *

gStyle.SetOptStat(000000)
gStyle.SetPaintTextFormat( '.2f' )

gStyle.SetPadRightMargin(0.12);
gStyle.SetPadLeftMargin(0.12);

labels = ['beta_signal', 'btag', 'jec', 'jer', 'lumi', 'rate_qcd', 'rate_st', 'rate_vjets', 'toptag']

cov = [[  7.55608435e-03,  -1.94122033e-02,  -8.87050992e-03,
          3.85588288e-03,  -2.01439882e-02,  -2.21803682e-02,
          9.06988020e-04,   1.72079187e-03,  -3.10536397e-02],
       [ -1.94122033e-02,   9.08078658e-01,  -2.80519658e-03,
         -2.34470310e-03,   2.59747792e-03,   5.36842130e-02,
          1.61452726e-03,   1.39863643e-02,   8.37091592e-02],
       [ -8.87050992e-03,  -2.80519658e-03,   1.39007482e-01,
         -5.36582209e-02,   3.93566401e-03,   2.29408586e-02,
         -4.85979135e-03,  -5.20007301e-02,   2.95633816e-02],
       [  3.85588288e-03,  -2.34470310e-03,  -5.36582209e-02,
          4.41862340e-01,  -8.85610966e-04,  -1.98216642e-02,
          8.34078508e-03,   1.17039243e-02,  -1.79549155e-02],
       [ -2.01439882e-02,   2.59747792e-03,   3.93566401e-03,
         -8.85610966e-04,   1.01153585e+00,  -6.10480570e-02,
         -2.48937598e-02,  -6.64934901e-02,   4.49174626e-03],
       [ -2.21803682e-02,   5.36842130e-02,   2.29408586e-02,
         -1.98216642e-02,  -6.10480570e-02,   2.07375611e-01,
         -7.64241099e-02,  -2.95173949e-02,   1.07626804e-01],
       [  9.06988020e-04,   1.61452726e-03,  -4.85979135e-03,
          8.34078508e-03,  -2.48937598e-02,  -7.64241099e-02,
          7.14888543e-01,  -5.39724472e-03,  -1.73863376e-02],
       [  1.72079187e-03,   1.39863643e-02,  -5.20007301e-02,
          1.17039243e-02,  -6.64934901e-02,  -2.95173949e-02,
         -5.39724472e-03,   3.82222223e-02,   2.00822710e-03],
       [ -3.10536397e-02,   8.37091592e-02,   2.95633816e-02,
         -1.79549155e-02,   4.49174626e-03,   1.07626804e-01,
         -1.73863376e-02,   2.00822710e-03,   1.66776380e-01]]
    

nvars = len(cov[0])
corhist = TH2F('corhist', '', nvars, 0, nvars, nvars, 0, nvars )

for x in xrange(nvars) :
    corhist.GetXaxis().SetBinLabel( x+1, labels[x] )
    corhist.GetYaxis().SetBinLabel( x+1, labels[x] )
    
for irow in xrange(nvars) :
    for icol in xrange( nvars) :
        correlation = cov[irow][icol] / ( sqrt(cov[irow][irow]) * sqrt(cov[icol][icol]) )
        corhist.SetBinContent( irow+1, icol+1, correlation)

c = TCanvas('c', 'c', 700, 600)
corhist.SetMaximum(1.0)
corhist.SetMinimum(-1.0)
corhist.Draw('colz text')
    

c.Print("correlations.pdf")
c.Print("correlations.png")


