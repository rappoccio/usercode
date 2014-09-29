from ROOT import *
gROOT.Macro("rootlogon.C")
gROOT.ForceStyle()

if __name__ ==  "__main__" :
    #dataFile = TFile("../crossChecks/Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3.root")
    #dataFile = TFile("Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3_KinOnlyBkg.root")
    dataFile = TFile("TTHadronicAnalyzer_Jet_PD_May10ReReco_PromptReco_range1_range2.root")
#    ttbarFile = TFile("crab_TTbarJets_ttbsm_v4_ttbsmTuple.root")
    #lumi = 188.0
    lumi = 679.
    ttXS = 157.0

    mttRebin = 20

    mea = dataFile.Get( "mttMass" )
#    ttbarHist = ttbarFile.Get( "mttMass" )
#    ttbarHist.Scale( lumi*ttXS/1285626. )
    bkg = dataFile.Get( "mttBkgWithMistagModMass" )
#    bkg = dataFile.Get( "mttBkgWithMistag" )
#    ttMistagBkg = ttbarFile.Get("mttBkgWithMistag")
#    ttMistagBkg.Scale( lumi*ttXS/1285626. )
#    print ttbarHist.Integral(), ttMistagBkg.Integral()

    c = TCanvas()
    mea.Rebin( mttRebin )
    mea.Sumw2()
#    ttbarHist.Rebin( mttRebin )
    bkg.Rebin( mttRebin )

    mea.SetLineColor( kBlack )
    mea.SetMarkerStyle( 20 )
    mea.SetMarkerColor( kBlack )

 #   ttbarHist.SetFillColor( kRed )
    bkg.SetFillColor( kYellow )

    stack = THStack("ttMass", "; m_{t#bar{t}} (GeV/c^{2}); # Events / 100 GeV")
    stack.Add( bkg, "Hist" )
#    stack.Add( ttbarHist, "Hist" )

    leg = TLegend( 0.6, 0.6, 0.85, 0.8 )
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    leg.AddEntry( mea, "Data", "LP" )
    leg.AddEntry( bkg, "QCD Bkg Estimate", "F" )
#    leg.AddEntry( ttbarHist, "SM t#bar{t}", "F" )

    stack.SetMaximum( max(mea.GetMaximum(),stack.GetMaximum()) * 1.2 )
    stack.Draw()
    stack.GetXaxis().SetRangeUser(500,3000)
    mea.Draw("samee")
    leg.Draw()
    prelim = TLatex()
    prelim.SetNDC()
    prelim.DrawLatex( 0.5, 0.91, "#scale[0.8]{CMS Preliminary, 679 pb^{-1}, Type I+II}" )



    c.Print("TTMASS_TYPE12_JET300_TopMistagBkg.png")
    c.Print("TTMASS_TYPE12_JET300_TopMistagBkg.pdf")



