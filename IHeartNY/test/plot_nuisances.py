from ROOT import *

ttbar_list = {'TTbar': {'jer': [(0.22061353421695032, 0.5240085500407996)], 'toptag': [(-0.098329869366054909, 0.34601707591990111)], 'btag': [(0.75455085428390811, 0.94746928847860412)], 'rate_nonsemi': [(-0.12018787388471373, 0.97084722143026347)], 'beta_signal': [(0.73760976089773345, 0.091740726306888343)], 'jec': [(1.1835010107547841, 0.60816395821912095)], 'rate_vjets': [(-0.81649074481469397, 0.27704899410344025)], '__nll': [-28855.883529467937], 'lumi': [(-0.3255111547263464, 0.99809496593146629)], 'rate_st': [(-0.87411566567303001, 0.84292348484379798)]}}


signal_list = ttbar_list['TTbar']

nuisances = TGraphErrors()
gr1sig = TGraphErrors()
gr2sig = TGraphErrors()

nPoint = -1
for systematic in sorted(signal_list.keys()):

	if systematic is '__nll' or systematic is "beta_signal":
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
	if systematic is '__nll' or systematic is 'beta_signal':
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


