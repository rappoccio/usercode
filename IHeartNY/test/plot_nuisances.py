from ROOT import *
from array import array

ttbar_list = {'TTbar': {'jer': [(1.3720065092111926, 0.72889076411245524)], 'toptag': [(-0.21344366134194681, 0.50402046494389297)], 'btag': [(-0.27107395498587028, 0.96419665993009396)], 'beta_signal': [(1.2362048297981083, 0.21722942839515347)], 'jec': [(0.81085746828223448, 0.46027473951679682)], 'rate_vjets': [(-0.61107012963979601, 0.23150519663137117)], '__nll': [-32816.955537504473], 'lumi': [(-0.031239573996700482, 1.0058038360806474)], 'rate_qcd': [(0.7044942082940796, 0.43105272058103949)], 'rate_st': [(-0.59111771192436169, 0.8700533461761113)]}}

signal_list = ttbar_list['TTbar']

nuisances = TGraphErrors()
gr1sig = TGraphErrors()
gr2sig = TGraphErrors()

nPoint = -1
for systematic in sorted(signal_list.keys()):

	if systematic is '__nll' or systematic is "beta_signal" or systematic is '__cov':
		continue

	nPoint += 1

	print systematic, signal_list[systematic][0][0], signal_list[systematic][0][1]


	nuisances.SetPoint(nPoint, signal_list[systematic][0][0], nPoint+0.5)
	nuisances.SetPointError(nPoint, signal_list[systematic][0][1], 0)

	gr1sig.SetPoint(nPoint, 0, nPoint)
	gr1sig.SetPointError(nPoint, 1, 1)
	
	gr2sig.SetPoint(nPoint, 0, nPoint)
	gr2sig.SetPointError(nPoint, 2, 1)
	





c1 = TCanvas("c1", "c1", 600, 800)
c1.Draw()
c1.SetLeftMargin(0.15)

gr2sig.SetLineWidth(0)
gr1sig.SetLineWidth(0)
gr2sig.SetLineColor(kYellow)
gr1sig.SetLineColor(kGreen)
gr2sig.SetFillStyle(1001)
gr2sig.SetFillColor(kYellow)

gr2sig.Draw("A5")
gr2sig.GetYaxis().Set(nPoint+1, 0, nPoint+1)
gr2sig.GetXaxis().Set(10,-4.5,4.5)

nBin = 0
for systematic in sorted(signal_list.keys()):
	if systematic is '__nll' or systematic is 'beta_signal' or systematic is '__cov':
		continue
	gr2sig.GetYaxis().SetBinLabel(nBin+1, systematic)
	nBin += 1

gr2sig.GetXaxis().SetTitle("Post-Fit Nuisance Parameter Value (#sigma)")
gr2sig.GetYaxis().SetTitle("Nuisance Parameter")
gr2sig.GetYaxis().SetTitleOffset(3)

gr1sig.SetFillStyle(1001)
gr1sig.SetFillColor(kGreen)
gr1sig.Draw("5 same")

nuisances.SetMarkerStyle(21)
nuisances.Draw("P same")
gPad.RedrawAxis()

label = TLatex()
label.SetNDC(1)

c1.Print("nuisances.pdf")
c1.Print("nuisances.png")


