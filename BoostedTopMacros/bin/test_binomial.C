{

  TH1D * h1 = new TH1D("h1", "h1", 5, 0, 5);
  TH1D * h2 = new TH1D("h2", "h2", 5, 0, 5);

  h1->Sumw2();
  h2->Sumw2();

  h1->Fill( 0 );
  h1->Fill( 1 );
  h1->Fill( 1 );
  h1->Fill( 2 );
  h1->Fill( 2 );
  h1->Fill( 2 );

  h2->Fill( 2 );
  h2->Fill( 3 );
  h2->Fill( 3 );
  h2->Fill( 3 );
  h2->Fill( 4 );
  h2->Fill( 4 );
  h2->Fill( 5 );

  TH1D * h = new TH1D("h", "h", 5, 0, 5);

  h->Add( h1, 1. / 3. );
  h->Add( h2 );


  cout << "bin contents of bin 3:" << endl;
  cout << "h1 : " << h1->GetBinContent(3) << " +- " << h1->GetBinError(3) << endl;
  cout << "h2 : " << h2->GetBinContent(3) << " +- " << h2->GetBinError(3) << endl;
  cout << "h : " << h->GetBinContent(3) << " +- " << h->GetBinError(3) << endl;

//   TCanvas * c = new TCanvas("c", "c", 600, 800);
//   c->Divide(1,3);

//   c->cd(1);
//   h1->Draw("e");
//   c->cd(2);
//   h2->Draw("e");
//   c->cd(3);
//   h->Draw("e");
  
}
