from ROOT import *

gStyle.SetOptStat(000000)
gStyle.SetPaintTextFormat( '.2f' )

labels = ['beta_signal', 'btag', 'jec', 'jer', 'lumi', 'rate_qcd', 'rate_st', 'rate_vjets', 'toptag']

cov = [[ 0.04730126, -0.08223549, -0.02173233,  0.02348511, -0.03504324,
        -0.05901038,  0.00501204, -0.00563679, -0.10325914],
       [-0.08223549,  0.9296752 , -0.00493752, -0.03004868,  0.00390794,
         0.10434267, -0.01062205,  0.03487091,  0.18884864],
       [-0.02173233, -0.00493752,  0.21185284, -0.07367887,  0.00546447,
         0.02545981, -0.00214589, -0.078417  ,  0.02175854],
       [ 0.02348511, -0.03004868, -0.07367887,  0.53128175, -0.00150444,
        -0.02916242,  0.01266804,  0.00772774, -0.04921528],
       [-0.03504324,  0.00390794,  0.00546447, -0.00150444,  1.01164136,
        -0.06250657, -0.02173958, -0.06646386,  0.00551358],
       [-0.05901038,  0.10434267,  0.02545981, -0.02916242, -0.06250657,
         0.18580645, -0.0825089 , -0.01626393,  0.13858121],
       [ 0.00501204, -0.01062205, -0.00214589,  0.01266804, -0.02173958,
        -0.0825089 ,  0.75699283, -0.00853734, -0.01862727],
       [-0.00563679,  0.03487091, -0.078417  ,  0.00772774, -0.06646386,
        -0.01626393, -0.00853734,  0.05359466,  0.02964679],
       [-0.10325914,  0.18884864,  0.02175854, -0.04921528,  0.00551358,
         0.13858121, -0.01862727,  0.02964679,  0.25403663]]
    

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


