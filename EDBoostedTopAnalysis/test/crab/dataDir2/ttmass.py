from ROOT import *

gROOT.Macro("rootlogon.C")

f = TFile("allJet_data.root")
ttbar = TFile( "TTbarJets-madgraph_ttbsm_38on35.root" )

idir = "wPlusBJetAna/"

sel = f.Get( idir + "ttMassType22" )
exp = f.Get( idir + "ttMassType22_pred" )
ttsel = ttbar.Get( idir + "ttMassType22" )

sel.Rebin(5)
exp.Rebin(5)
ttsel.Rebin(5)

ttsel.Scale( 165.0*34.7/1482609.0 )


c = TCanvas()
leg = TLegend( 0.6, 0.7, 0.85, 0.82 )
leg.SetBorderSize(1)
leg.SetFillStyle(0)


stack = THStack( "ttmass", ";t#bar{t} Mass (GeV/c^{2});Number of Events" )

exp.SetLineColor(kBlack)
ttsel.SetLineColor(kBlack)
exp.SetFillColor(kYellow)
ttsel.SetFillColor(kRed+1)
sel.SetMarkerStyle(20)

stack.Add(exp)
stack.Add(ttsel)
stack.SetMaximum(2.5)

print "QCD Exp Integral %.2f" % exp.Integral()
print "tt Integral %.2f" % ttsel.Integral()
print "Data Integral %.2f" % sel.Integral()

leg.AddEntry( exp, "QCD Exp" , "F")
leg.AddEntry( ttsel, "t#bar{t}" , "F" )
leg.AddEntry( sel, "Data" , "P" )

stack.Draw()
sel.Draw("samePE")
leg.Draw()

c.Print("ttmass.png")






