from ROOT import *

gROOT.Macro( "rootlogon.C" )

f = TFile( "allJet_data.root" )
ttbar = TFile( "TTbarJets-madgraph_ttbsm_38on35.root" )

idir = "wPlusBJetAna/"

probe = f.Get( idir + "probeWMass" )

sideband0 = f.Get( idir + "sideBandWMass0" )
sideband1 = f.Get( idir + "sideBandWMass1" )

colors = [ kBlack, kRed, kBlue ]

histos = [ probe, sideband0, sideband1 ]



stack1 = THStack( "wMass0", "W Jet Mass;Jet Mass (GeV/c^{2})" )
stack1.Add( probe, "PE1" )
probe.SetMarkerStyle(20)
probe.SetMarkerColor( kBlack )
probe.Rebin(2)
stack1.Add( sideband0 )
sideband0.SetLineColor( kRed )
sideband0.Rebin(2)
stack1.Add( sideband1 )
sideband1.SetLineColor( kBlue )
sideband1.Rebin(2)

c = TCanvas()
stack1.Draw("nostack")
c.Print("wMass.png")


stack1 = THStack( "wMass1", "W Jet Mass;Jet Mass (GeV/c^{2})" )
stack1.Add( probe, "PE1" )
probe.SetMarkerStyle(20)
probe.SetMarkerColor( kBlack )
norm = probe.Integral(2,6)
stack1.Add( sideband0 )
sideband0.SetLineColor( kRed )
norm0 = sideband0.Integral(2,6)
sideband0.Scale( norm/norm0 )
stack1.Add( sideband1 )
sideband1.SetLineColor( kBlue )
norm1 = sideband1.Integral(2,6)
sideband1.Scale( norm/norm1 )

c = TCanvas()
stack1.Draw("nostack")
c.Print("wMass1.png")






