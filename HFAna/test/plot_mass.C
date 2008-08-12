{

  TFile * f1 = new TFile("wbbAna.root");
  TFile * f2 = new TFile("wccAna.root");
  TFile * f3 = new TFile("wcAna.root");
  TFile * f4 = new TFile("wjetsAna.root");

  TH1F * h_mass_wbb = (TH1F*)f1->Get("wbbAna/hfana/svMass");
  TH1F * h_mass_wcc = (TH1F*)f2->Get("wccAna/hfana/svMass");
  TH1F * h_mass_wc = (TH1F*)f3->Get("wcAna/hfana/svMass");
  TH1F * h_mass_wjets = (TH1F*)f4->Get("wjetsAna/hfana/svMass");

  THStack * hs = new THStack("svMass", "Secondary Vertex Mass");

  h_mass_wbb->Scale(1.0 / h_mass_wbb->GetEntries() );
  h_mass_wcc->Scale(1.0 / h_mass_wcc->GetEntries() );
  h_mass_wc->Scale(1.0 / h_mass_wc->GetEntries() );
  h_mass_wjets->Scale(1.0 / h_mass_wjets->GetEntries() );

  h_mass_wbb->SetLineColor(1);
  h_mass_wcc->SetLineColor(2);
  h_mass_wc->SetLineColor(4);
  h_mass_wjets->SetLineColor(6);

  hs->Add(h_mass_wbb );
  hs->Add(h_mass_wcc );
  hs->Add(h_mass_wc );
//   hs->Add(h_mass_wjets );

  TLegend * leg = new TLegend(0.8, 0.8, 1.0, 1.0);
  leg->AddEntry(h_mass_wbb, "W+bb", "l" );
  leg->AddEntry(h_mass_wcc, "W+cc", "l" );
  leg->AddEntry(h_mass_wc, "W+c", "l" );
//   leg->AddEntry(h_mass_wjets, "W+jets", "l" );


  hs->Draw("nostack");
  leg->Draw();

}
