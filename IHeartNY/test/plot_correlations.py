from ROOT import *

gStyle.SetOptStat(000000)
gStyle.SetPaintTextFormat( '.2f' )
gStyle.SetTitleFont(42);
gStyle.SetTitleFont(42, "XYZ");

gStyle.SetPadRightMargin(0.12);
gStyle.SetPadLeftMargin(0.15);
gStyle.SetPadTopMargin(0.15);
gStyle.SetPadBottomMargin(0.15);


pdfnames = ["CT10_nom"]
#channels = ["mu", "el", "comb"]
channels = ["comb"]

### THESE BELOW ARE FOR EXTERNALIZE LUMINOSITY & B-TAGGING !!! ###

for pdfname in pdfnames :
    for ich in channels :

        # ---------------------------------- muon only fit ----------------------------------
        if pdfname=="CT10_nom" and ich=="mu": 
            cov = [[  7.26173597e-03,  -8.17942964e-03,  -1.81491378e-03,
         -1.99551022e-02,  -3.40003322e-04,  -2.03303814e-03,
         -3.33854017e-02],
       [ -8.17942964e-03,   4.77008932e-01,   4.73645065e-02,
          1.11888447e-02,  -1.91191681e-02,  -6.96937506e-02,
          2.50413227e-02],
       [ -1.81491378e-03,   4.73645065e-02,   6.62263280e-01,
          2.73651446e-02,   1.61268913e-02,  -2.41555108e-02,
          3.40399211e-03],
       [ -1.99551022e-02,   1.11888447e-02,   2.73651446e-02,
          1.17545329e-01,  -5.90937919e-02,  -1.72527682e-02,
          9.49058091e-02],
       [ -3.40003322e-04,  -1.91191681e-02,   1.61268913e-02,
         -5.90937919e-02,   7.65312900e-01,  -6.19170544e-03,
         -1.16518527e-02],
       [ -2.03303814e-03,  -6.96937506e-02,  -2.41555108e-02,
         -1.72527682e-02,  -6.19170544e-03,   2.50959513e-02,
          1.21556171e-02],
       [ -3.33854017e-02,   2.50413227e-02,   3.40399211e-03,
          9.49058091e-02,  -1.16518527e-02,   1.21556171e-02,
          1.78628903e-01]]

        # ---------------------------------- electron only fit ----------------------------------
        if pdfname=="CT10_nom" and ich=="el": 
            cov = [[ 0.0072308 , -0.01015937, -0.00910761,  0.00817062, -0.02284004,
        -0.00955794, -0.02131413],
       [-0.01015937,  0.24815932,  0.0825822 ,  0.02030345,  0.02387121,
        -0.04298847,  0.01160481],
       [-0.00910761,  0.0825822 ,  0.57042136,  0.01339384,  0.06426294,
        -0.02175608,  0.01881723],
       [ 0.00817062,  0.02030345,  0.01339384,  0.11537226,  0.02090396,
        -0.04353637, -0.03751366],
       [-0.02284004,  0.02387121,  0.06426294,  0.02090396,  0.86537826,
        -0.02706541,  0.05736799],
       [-0.00955794, -0.04298847, -0.02175608, -0.04353637, -0.02706541,
         0.03793725,  0.03705956],
       [-0.02131413,  0.01160481,  0.01881723, -0.03751366,  0.05736799,
         0.03705956,  0.08519223]]

        # ---------------------------------- combined fit ----------------------------------
        if pdfname=="CT10_nom" and ich=="comb": 
            cov = [[  4.15192541e-03,  -9.03560364e-03,  -4.71360725e-03,
          1.59342201e-05,  -5.71167741e-03,  -2.59067348e-02,
         -3.43885056e-03,  -1.09158492e-02],
       [ -9.03560364e-03,   2.52814503e-01,   6.66165293e-02,
          1.29371319e-03,   4.70627640e-02,  -2.28577153e-03,
         -3.89545516e-02,   1.00868641e-02],
       [ -4.71360725e-03,   6.66165293e-02,   5.31127044e-01,
          5.03774271e-04,   5.32669293e-02,   4.06790872e-02,
         -1.98936218e-02,   5.86239576e-03],
       [  1.59342201e-05,   1.29371319e-03,   5.03774271e-04,
          2.87341529e-02,   3.90554268e-02,  -4.34369265e-03,
         -7.25267117e-03,  -1.85548763e-03],
       [ -5.71167741e-03,   4.70627640e-02,   5.32669293e-02,
          3.90554268e-02,   2.20068198e-01,  -1.58384280e-03,
         -2.20873632e-02,   1.00191026e-02],
       [ -2.59067348e-02,  -2.28577153e-03,   4.06790872e-02,
         -4.34369265e-03,  -1.58384280e-03,   8.35792677e-01,
         -7.18263892e-03,   6.56928000e-02],
       [ -3.43885056e-03,  -3.89545516e-02,  -1.98936218e-02,
         -7.25267117e-03,  -2.20873632e-02,  -7.18263892e-03,
          1.86985753e-02,   1.33981907e-02],
       [ -1.09158492e-02,   1.00868641e-02,   5.86239576e-03,
         -1.85548763e-03,   1.00191026e-02,   6.56928000e-02,
          1.33981907e-02,   3.80998142e-02]]
            

        if ich=="comb":
            labels = ['#beta_{signal}', 'JEC', 'JER', 'N(el QCD)', 'N(mu QCD)', 'N(single top)', 'N(W+jet)', 'Top-tagging']
        elif ich=="mu" :
            labels = ['#beta_{signal}', 'JEC', 'JER', 'N(mu QCD)', 'N(single top)', 'N(W+jet)', 'Top-tagging']
        else:
            labels = ['#beta_{signal}', 'JEC', 'JER', 'N(el QCD)', 'N(single top)', 'N(W+jet)', 'Top-tagging']


        nvars = len(cov[0])
        corhist = TH2F('corhist', '', nvars, 0, nvars, nvars, 0, nvars )

        for x in xrange(nvars) :
            corhist.GetXaxis().SetLabelSize(0.055)
            corhist.GetXaxis().SetLabelOffset(0.01)
            corhist.GetYaxis().SetLabelSize(0.055)
            corhist.GetXaxis().SetBinLabel( x+1, labels[x] )
            corhist.GetYaxis().SetBinLabel( x+1, labels[x] )
    
        for irow in xrange(nvars) :
            for icol in xrange( nvars) :
                correlation = cov[irow][icol] / ( sqrt(cov[irow][irow]) * sqrt(cov[icol][icol]) )
                corhist.SetBinContent( irow+1, icol+1, correlation)

        c = TCanvas('c', 'c', 700, 600)
        c.SetLeftMargin(0.18)
        c.SetRightMargin(0.14)
        c.SetTopMargin(0.09)
        c.SetBottomMargin(0.14)

        corhist.GetZaxis().SetLabelSize(0.045)
        corhist.SetMaximum(1.0)
        corhist.SetMinimum(-1.0)
        corhist.SetMarkerSize(1.4)
        corhist.Draw('colz text')

        cmsTextSize = 0.054;
        extraOverCmsTextSize = 0.76
        extraTextSize = extraOverCmsTextSize*cmsTextSize

        t1 = TLatex()
        t1.SetNDC()
        t1.SetTextFont(61)
        t1.SetTextAngle(0)
        t1.SetTextColor(1)
        t1.SetTextSize(cmsTextSize)
        if (ich=="comb"): 
            t1.DrawLatex(0.18,0.93, "CMS")

        t2 = TLatex()
        t2.SetNDC()
        t2.SetTextFont(52)
        t2.SetTextColor(1)
        t2.SetTextSize(extraTextSize)
        #if (ich=="comb"): 
        #    t2.DrawLatex(0.28,0.93, "Preliminary")

        t3 = TLatex()
        t3.SetNDC()
        t3.SetTextFont(42)
        t3.SetTextColor(1)
        t3.SetTextSize(extraTextSize)
        if (ich=="comb"): 
            t3.DrawLatex(0.64,0.93, "19.7 fb^{-1} (8 TeV)")

        c.Print("correlations_"+pdfname+"_"+ich+"_extlumibtag.pdf")
        c.Print("correlations_"+pdfname+"_"+ich+"_extlumibtag.png")

        corhist.Delete()
