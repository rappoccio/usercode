from ROOT import *

gStyle.SetOptStat(000000)
gStyle.SetPaintTextFormat( '.2f' )

labels = ['beta_signal', 'btag', 'jec', 'jer', 'lumi', 'rate_qcd', 'rate_st', 'rate_vjets', 'toptag']

cov =[[ 0.00827093, -0.01850917, -0.02047882,  0.00865546, -0.02076744,
        -0.02994491, -0.00298191,  0.00358319, -0.03325376],
       [-0.01850917,  0.92315916, -0.02661647, -0.00372143,  0.004404  ,
         0.08575654, -0.00134654,  0.0268001 ,  0.08753502],
       [-0.02047882, -0.02661647,  0.29549189, -0.07829519,  0.0106217 ,
         0.0330823 ,  0.0119684 , -0.1044007 ,  0.05231509],
       [ 0.00865546, -0.00372143, -0.07829519,  0.55702056, -0.00455914,
        -0.02809484,  0.00482886,  0.01065692, -0.0364468 ],
       [-0.02076744,  0.004404  ,  0.0106217 , -0.00455914,  1.00969974,
        -0.06055625, -0.02701858, -0.06974548,  0.01187872],
       [-0.02994491,  0.08575654,  0.0330823 , -0.02809484, -0.06055625,
         0.33049526, -0.08058636, -0.02695519,  0.13860314],
       [-0.00298191, -0.00134654,  0.0119684 ,  0.00482886, -0.02701858,
        -0.08058636,  0.70911489, -0.01361277,  0.00156026],
       [ 0.00358319,  0.0268001 , -0.1044007 ,  0.01065692, -0.06974548,
        -0.02695519, -0.01361277,  0.05875349,  0.00579767],
       [-0.03325376,  0.08753502,  0.05231509, -0.0364468 ,  0.01187872,
         0.13860314,  0.00156026,  0.00579767,  0.17322256]]
    

    

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


