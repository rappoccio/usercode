from ROOT import *

gROOT.Macro( "rootlogon.C" )

f = TFile( "allJet_data.root" )
ttbar = TFile( "TTbarJets-madgraph_ttbsm_38on35.root" )

idir = "wPlusBJetAna/"

probe = f.Get( idir + "probeWMass" )
probe.Rebin(2)

exp = f.Get( idir + "probeWMassExp" )
exp.Rebin(2)

ttprobe = ttbar.Get( idir + "probeWMass" )
ttprobe.Rebin(2)
ttprobe.Scale( 165.0*34.7/1482609.0 )

leg = TLegend( 0.6, 0.7, 0.85, 0.82 )
leg.SetBorderSize(1)
leg.SetFillStyle(0)

stack = THStack( "probeMass", ";Jet Mass (GeV/c^2);Number of Jets" )
stack.SetMaximum(9.5)
exp.SetLineWidth(long(1))
exp.SetLineColor(1)
exp.SetFillColor(kYellow)

ttprobe.SetLineColor(1)
ttprobe.SetLineWidth(long(1))
ttprobe.SetFillColor(kRed+1)

stack.Add( exp )
stack.Add( ttprobe )

probe.SetLineColor(1)
probe.SetLineWidth(long(1.3))
probe.SetMarkerStyle(20)

leg.AddEntry( exp, "QCD Exp", "F" )
leg.AddEntry( ttprobe, "t#bar{t}", "F" )
leg.AddEntry( probe, "Data", "P" )

c = TCanvas()
stack.Draw()
probe.Draw("samePE")
leg.Draw()
c.Print("wmass.png")




