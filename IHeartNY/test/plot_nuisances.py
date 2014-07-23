from ROOT import *

ttbar_list = {'TTbar': {'jer': [(0.23702397679044959, 0.52965130625772006)], 'toptag': [(0.054810758433977209, 0.36120044113105382)], 'btag': [(0.45351420369770623, 0.96121554090549544)], 'rate_nonsemi': [(-0.036910895496673098, 0.98587665209178377)], 'beta_signal': [(0.74282593747419901, 0.093701869648684988)], 'jec': [(1.0980726837203341, 0.60342279663016352)], 'rate_vjets': [(-0.72296875569147101, 0.2797271792739997)], '__nll': [-28857.675163650867], 'lumi': [(-0.17121646887137462, 1.0035520402561324)], 'rate_qcd': [(-1.1985110609613625, 0.70524449562279345)], 'rate_st': [(-0.75055777574116544, 0.85614337937406759)]}}



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


