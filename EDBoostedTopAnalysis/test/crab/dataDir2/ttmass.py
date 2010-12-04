from ROOT import *

gROOT.Macro("rootlogon.C")
gROOT.ForceStyle()

lumi = 7.0

f = TFile("data.root")

h1 = f.Get("wPlusBJetAna/ttMassType22_pred")
h2 = f.Get("wPlusBJetAna/ttMassType23_pred")
h3 = f.Get("wPlusBJetAna/ttMassType33_pred")
data = f.Get("wPlusBJetAna/ttMassType33")


c = TCanvas()
h1.GetYaxis().SetTitle("Numbers in 7pb^{-1}")
h1.GetXaxis().SetTitle("t#bar{t} Mass (GeV/c^{2})")
h1.Rebin(5)
h1.SetMaximum(1.1)
h1.Draw()
print h1.Integral()
c.Print("tt22.png")

h2.GetYaxis().SetTitle("Numbers in 7pb^{-1}")
h2.GetXaxis().SetTitle("t#bar{t} Mass (GeV/c^{2})")
h2.Rebin(5)
h2.SetMaximum(1.1)
h2.Draw()
print h2.Integral()
c.Print("tt23.png")

h3.GetYaxis().SetTitle("Numbers in 7pb^{-1}")
h3.GetXaxis().SetTitle("t#bar{t} Mass (GeV/c^{2})")
h3.Rebin(5)
h3.SetMaximum(1.1)
data.Rebin(5)
data.SetMarkerStyle(20)
data.SetLineColor(kRed)
print h3.Integral()
h3.Draw()
data.Draw("same")
c.Print("tt33.png")

