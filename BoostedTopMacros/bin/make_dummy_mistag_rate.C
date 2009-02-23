{

  TH1D * num = new TH1D("num", "num", 10, 0, 10);
  TH1D * den = new TH1D("den", "den", 10, 0, 10);

  for ( int i = 0; i < 10000; ++i ) {
    double x = gRandom->Uniform(0, 10);
    den->Fill( x );
    double irand = gRandom->Uniform();
    if ( irand < 0.3 )
      num->Fill( x ); 
  }

  TH1D * ratio = new TH1D("ratio", "ratio", 10, 0, 10);

  num->Sumw2();
  den->Sumw2();
  ratio->Divide( num, den, 1.0, 1.0, "b");

  ratio->Draw("e");

  TFile * f = new TFile("dummy_output.root", "RECREATE");
  f->cd();
  ratio->Write();
  num->Write();
  den->Write();
  f->Close();
}
