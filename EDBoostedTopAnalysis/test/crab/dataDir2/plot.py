from ROOT import *

gROOT.Macro("rootlogon.C")

f = TFile.Open("data.root")

pred = f.Get("wPlusBJetAna/minPairMass1Type33_pred")

sel = f.Get("wPlusBJetAna/minPairMass1Type33_sel")

leg = TLegend( 0.6, 0.7, 0.8, 0.9 )
leg.SetFillStyle(0)
leg.SetBorderSize(0)

c = TCanvas()

pred.Rebin(2)
pred.Scale(1.2)
sel.Rebin(2)
pred.Draw()

sel.SetMarkerStyle(20)
sel.SetTitle("Min Pair Inv Mass;Mass (GeV/c^{2});Numbers in 7pb^{-1}")

#pred.Draw()
sel.Draw("e")
pred.Draw("same")

leg.AddEntry( pred, "Prediction", "l" )
leg.AddEntry( sel, "Selection", "P" )
leg.Draw()

c.Print("test.png")
