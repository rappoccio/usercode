{

  TFile * ttbar_cont = new TFile("kinematic_histos_ttbar_v5.root");
  gStyle->SetPadTopMargin(0.13);

  gSystem->CompileMacro("palette.C", "k");
  gSystem->CompileMacro("add_plots.C", "k");
  gSystem->CompileMacro("divide_thstack.C", "k");
  gSystem->CompileMacro("append_to_thstack.C", "k");

  double N_TTBAR = 1028322;
  double Lum = 100.0;

  TCanvas * c0 = new TCanvas("c", "c");
  TLegend * leg0 = new TLegend(0.7, 0.55, 1.0, 1.0);
  leg0->SetFillColor(0);
  leg0->SetLineColor(0);
  THStack * hs_untagged = add_plots(Lum, leg0, "kinematic_histos", "hist_nontop_jetPt", "Jet p_{T}, Pretagged Jets;Jet p_{T} (GeV/c);Number Per 50 GeV");
  TH1 * hist_top_jetPt = (TH1*)ttbar_cont->Get("hist_top_jetPt");
  append_to_thstack( hs_untagged, hist_top_jetPt, leg0, "ttbar continuum", 317 * 1.4 * Lum / N_TTBAR, 4);
  hs_untagged->Draw();
  leg0->Draw();
  hs_untagged->GetYaxis()->SetTitleSize(0.05);
  hs_untagged->GetYaxis()->SetLabelSize(0.04);
  hs_untagged->GetXaxis()->SetTitleSize(0.05);
  hs_untagged->GetXaxis()->SetLabelSize(0.04);
  hs_untagged->GetYaxis()->SetTitleOffset(1.2);
  hs_untagged->GetXaxis()->SetRangeUser(0, 1600);
//   hs_untagged->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   hs_untagged->SetMinimum(1e-13);
//   hs_untagged->SetMaximum(1e5);
  // gPad->SetLogy();
  gPad->Print("jet_et_untagged.gif", "gif");
  gPad->Print("jet_et_untagged.eps", "eps");



  TCanvas * c1 = new TCanvas("c", "c");
  TLegend * leg1 = new TLegend(0.7, 0.55, 1.0, 1.0);
  leg1->SetFillColor(0);
  leg1->SetLineColor(0);
  THStack * hs_tagged = add_plots(Lum, leg1, "kinematic_histos", "hist_tagged_nontop_jetPt", "Jet p_{T}, Tagged Jets;Jet p_{T} (GeV/c);Number Per 50 GeV");
  TH1 * hist_tagged_top_jetPt = (TH1*)ttbar_cont->Get("hist_tagged_top_jetPt");
  append_to_thstack( hs_tagged, hist_tagged_top_jetPt, leg1, "ttbar continuum", 317 * 1.4 * Lum / N_TTBAR, 4);
  hs_tagged->Draw();
  leg1->Draw();
  hs_tagged->GetYaxis()->SetTitleSize(0.05);
  hs_tagged->GetYaxis()->SetLabelSize(0.04);
  hs_tagged->GetXaxis()->SetTitleSize(0.05);
  hs_tagged->GetXaxis()->SetLabelSize(0.04);
  hs_tagged->GetYaxis()->SetTitleOffset(1.2);
  hs_tagged->GetXaxis()->SetRangeUser(0, 1600);
//   hs_tagged->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   hs_tagged->SetMinimum(1e-13);
//   hs_tagged->SetMaximum(1e5);
  // gPad->SetLogy();
  gPad->Print("jet_et_tagged.gif", "gif");
  gPad->Print("jet_et_tagged.eps", "eps");


  TCanvas * c2 = new TCanvas("c", "c");
  TLegend * leg2 = new TLegend(0.7, 0.55, 1.0, 1.0);
  leg2->SetFillColor(0);
  leg2->SetLineColor(0);
  THStack * dijetmass = add_plots(Lum, leg2, "kinematic_histos", "hist_nontop_dijetmass", "Dijet Mass;Dijet Mass, Pretagged Events (GeV);Number Per 50 GeV");
  TH1 * hist_top_dijetmass = (TH1*)ttbar_cont->Get("hist_top_dijetmass");
  append_to_thstack( dijetmass, hist_top_dijetmass, leg2, "ttbar continuum", 317 * 1.4 * Lum / N_TTBAR, 4);
  dijetmass->Draw();
  leg2->Draw();
  dijetmass->GetYaxis()->SetTitleSize(0.05);
  dijetmass->GetYaxis()->SetLabelSize(0.04);
  dijetmass->GetXaxis()->SetTitleSize(0.05);
  dijetmass->GetXaxis()->SetLabelSize(0.04);
  dijetmass->GetYaxis()->SetTitleOffset(1.2);
//   dijetmass->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   dijetmass->SetMinimum(1e-13);
//   dijetmass->SetMaximum(1e5);
  // gPad->SetLogy();
  gPad->Print("dijetmass_untagged.gif", "gif");
  gPad->Print("dijetmass_untagged.eps", "eps");


  TCanvas * c3 = new TCanvas("c", "c");
  TLegend * leg3 = new TLegend(0.7, 0.55, 1.0, 1.0);
  leg3->SetFillColor(0);
  leg3->SetLineColor(0);
  THStack * dijetmass_tagged = add_plots(Lum, leg3, "kinematic_histos", "hist_tagged_nontop_dijetmass", "Dijet Mass, Double Tagged Events;Dijet Mass (GeV);Number Per 50 GeV");
  TH1 * hist_tagged_top_dijetmass = (TH1*)ttbar_cont->Get("hist_tagged_top_dijetmass");
  append_to_thstack( dijetmass_tagged, hist_tagged_top_dijetmass, leg3, "ttbar continuum", 317 * 1.4 * Lum / N_TTBAR, 4);
  dijetmass_tagged->Draw();
  leg3->Draw();
  dijetmass_tagged->GetYaxis()->SetTitleSize(0.05);
  dijetmass_tagged->GetYaxis()->SetLabelSize(0.04);
  dijetmass_tagged->GetXaxis()->SetTitleSize(0.05);
  dijetmass_tagged->GetXaxis()->SetLabelSize(0.04);
  dijetmass_tagged->GetYaxis()->SetTitleOffset(1.2);
//   dijetmass_tagged->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   dijetmass_tagged->SetMinimum(1e-13);
//   dijetmass_tagged->SetMaximum(1e5);
  // gPad->SetLogy();
  gPad->Print("dijetmass_tagged.gif", "gif");
  gPad->Print("dijetmass_tagged.eps", "eps");




  TCanvas * c4 = new TCanvas("c", "c");
  TLegend * leg4 = new TLegend(0.7, 0.55, 1.0, 1.0);
  leg4->SetFillColor(0);
  leg4->SetLineColor(0);
  THStack * dijetmass_onetagged = add_plots(Lum, leg4, "kinematic_histos", "hist_onetagged_nontop_dijetmass", "Dijet Mass, Single Tagged Events;Dijet Mass (GeV);Number Per 50 GeV");
  TH1 * hist_onetagged_top_dijetmass = (TH1*)ttbar_cont->Get("hist_onetagged_top_dijetmass");
  append_to_thstack( dijetmass_onetagged, hist_onetagged_top_dijetmass, leg4, "ttbar continuum", 317 * 1.4 * Lum / N_TTBAR, 4);
  dijetmass_onetagged->Draw();
  leg4->Draw();
  dijetmass_onetagged->GetYaxis()->SetTitleSize(0.05);
  dijetmass_onetagged->GetYaxis()->SetLabelSize(0.04);
  dijetmass_onetagged->GetXaxis()->SetTitleSize(0.05);
  dijetmass_onetagged->GetXaxis()->SetLabelSize(0.04);
  dijetmass_onetagged->GetYaxis()->SetTitleOffset(1.2);
//   dijetmass_onetagged->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   dijetmass_onetagged->SetMinimum(1e-13);
//   dijetmass_onetagged->SetMaximum(1e5);
  // gPad->SetLogy();
  gPad->Print("dijetmass_onetagged.gif", "gif");
  gPad->Print("dijetmass_onetagged.eps", "eps");


//   THStack * hs_tagged = add_plots(Lum, "kinematic_histos", "hist_nontop_dijetmass", "Dijet Mass;Mass (GeV);Number Per 20 GeV");
//   hs_tagged->GetYaxis()->SetTitleSize(0.05);
//   hs_tagged->GetYaxis()->SetLabelSize(0.04);
//   hs_tagged->GetXaxis()->SetTitleSize(0.05);
//   hs_tagged->GetXaxis()->SetLabelSize(0.04);
//   hs_tagged->GetYaxis()->SetTitleOffset(1.2);
//   hs_tagged->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   hs_tagged->SetMinimum(1e-13);
//   hs_tagged->SetMaximum(1e5);
//   // gPad->SetLogy();
//   gPad->Print("dijetmass_qcd_untagged.gif", "gif");

//   THStack * hs_tagged = add_plots(Lum, "kinematic_histos", "hist_tagged_nontop_dijetmass", "Dijet Mass;Mass (GeV);Number Per 20 GeV");
//   hs_tagged->GetYaxis()->SetTitleSize(0.05);
//   hs_tagged->GetYaxis()->SetLabelSize(0.04);
//   hs_tagged->GetXaxis()->SetTitleSize(0.05);
//   hs_tagged->GetXaxis()->SetLabelSize(0.04);
//   hs_tagged->GetYaxis()->SetTitleOffset(1.2);
//   hs_tagged->GetYaxis()->SetRangeUser(1e-13, 1e5);
//   hs_tagged->SetMinimum(1e-13);
//   hs_tagged->SetMaximum(1e5);
//   // gPad->SetLogy();
//   gPad->Print("qcd_dijetmass_qcd_tagged.gif", "gif");


//   THStack * hs_jetmass = add_plots(Lum, "kinematic_histos", "hist_nontop_jetMass", "Jet Mass, Untagged Jets;Jet Mass (GeV);Number Per 10 GeV");
//   gPad->Print("qcd_untagged_jetmass.gif", "gif");

//   THStack * hs_minmass = add_plots(Lum, "kinematic_histos", "hist_nontop_jetMinMass", "Jet Min Mass, Untagged Jets;Jet Min Mass (GeV);Number Per 4 GeV");
//   gPad->Print("qcd_tagged_jetmass.gif", "gif");

//   TH1D * frac = divide_thstack(hs_tagged, hs_untagged, "mistag", "Mistag Rate versus Jet p_{T};Jet p_{T} (GeV/c)");
//   TCanvas * c = new TCanvas("c", "c");
//   frac->Draw("l");
//   gPad->Print("mistag_rate.gif", "gif");
}
