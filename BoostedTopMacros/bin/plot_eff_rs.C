{

  double systematic = 0.044;

  const char * files[] = {
    "kinematic_histos_rs_750_fastsim.root",
    "kinematic_histos_rs_1000_fastsim.root",
    "kinematic_histos_rs_1250_fastsim.root",
    "kinematic_histos_rs_1500_fastsim.root",
    "kinematic_histos_rs_2000_fastsim.root",
    "kinematic_histos_rs_2500_fastsim.root",
    "kinematic_histos_rs_3000_fastsim.root",
  };

  TH1D * hist_tagged_top_jetEt = 0;
  TH1D * hist_top_jetEt = 0;

  TF1 * erf = new TF1("erf", "[0] * TMath::ATan((x - [1]) / [2]) + [3]", 300, 1600);

  erf->SetParameter(0,0.3);
  erf->SetParameter(1,300);
  erf->SetParameter(2,100);
  erf->SetParameter(3,0.1);

  const int NFILES = sizeof(files)/sizeof(const char *);

  for (int i = 0; i < NFILES; ++i ) {
    cout << "Processing i = " << i << ",  file = " << files[i] << endl;
    TFile * f = new TFile(files[i]);
    TH1D * h1 = (TH1D*)f->Get("hist_tagged_top_jetEt");
    TH1D * h2 = (TH1D*)f->Get("hist_top_jetEt");

    TH1D * h_untagged = (TH1D*)f->Get("hist_top_dijetmass");
    TH1D * h_onetagged = (TH1D*)f->Get("hist_onetagged_top_dijetmass");
    TH1D * h_twotagged = (TH1D*)f->Get("hist_tagged_top_dijetmass");

    char buff[400];
    sprintf(buff, " & %6d  & %6d  & %6d  &  %6d  & %6d",
	    h2->GetEntries(),
	    h1->GetEntries(),
	    h_untagged->GetEntries(),
	    h_onetagged->GetEntries(),
	    h_twotagged->GetEntries());
    cout << buff << endl;
    
    cout << 
    if ( i == 0 ) {
      cout << "Setting up histograms" << endl;
      hist_tagged_top_jetEt = new TH1D(*h1);
      hist_tagged_top_jetEt->SetName("total_tagged_top_jetEt");
      hist_tagged_top_jetEt->SetTitle("CATopTag Efficiency;Jet E_{T} (GeV/c^{2});Efficiency");
      hist_top_jetEt = new TH1D(*h2);
      hist_top_jetEt->SetName("total_top_jetEt");
    } else {
      cout << "Adding histograms" << endl;
      hist_tagged_top_jetEt->Add(h1);
      hist_top_jetEt->Add(h2);
    }
  }

  cout << "About to plot" << endl;
  if ( hist_tagged_top_jetEt == 0 ) {
    cout << "error! about to crash" << endl;
  } else {
    hist_tagged_top_jetEt->Sumw2();
    hist_top_jetEt->Sumw2();

    TH1D * eff = new TH1D(*hist_tagged_top_jetEt);

    eff->Divide( hist_tagged_top_jetEt, hist_top_jetEt, 1.0, 1.0, "b");

    TH1D * eff2 = (TH1D*)eff->Clone();
    eff2->SetName("eff2");

    for ( int i = 0; i <= eff->GetNbinsX(); ++i ) {
      double ieff = eff->GetBinContent(i);
      double dieff = eff->GetBinError(i);
      if ( ieff > 0 ) {
	double newerr = TMath::Sqrt( TMath::Power(dieff/ieff,2.0) + TMath::Power(systematic, 2.0) ) * ieff;
	eff->SetBinError( i, newerr );
      }
    }

    eff->SetFillColor(4);
    eff->SetFillStyle(3244);
    eff2->SetMarkerStyle(20);
    erf->SetLineColor(kBlue + 3 );
    erf->SetLineWidth(3);

    TLegend * leg = new TLegend(0.25, 0.65, 0.65, 0.85);

    leg->SetFillColor(0);
    leg->SetFillStyle(0);
    leg->SetLineColor(0);
    leg->SetLineStyle(0);
    leg->SetBorderSize(0);

    
    gStyle->SetOptStat(000000);
    gStyle->SetOptFit(1111);
//     eff->Draw("e3");
//     eff2->Draw("e same");
    eff2->Fit("erf", "RM");


    TGraph * upper = new TGraph( 100 );
    TGraph * lower = new TGraph( 100 );

    double xmin = 300;
    double xmax = 1600;
    double diff = xmax - xmin;
    double step = diff / 100.0;

    for ( int i = 0; i < 100; ++i ) {
      upper->SetPoint(i, i*step + xmin, 1.044 * erf->Eval(i*step+xmin) );
      lower->SetPoint(i, i*step + xmin, 0.956 * erf->Eval(i*step+xmin) );
    }


    upper->SetFillColor(4);
    upper->SetFillStyle(3244);
    upper->SetLineColor(0);

    lower->SetFillColor(0);
    lower->SetLineColor(0);

    upper->Draw("F same");
    lower->Draw("F same");

    eff2->Draw("same");


    leg->AddEntry( eff2, "Monte Carlo Statistics", "p");
//     leg->AddEntry( eff,  "+ 4.4% Systematic", "f");
    leg->AddEntry( upper,  "Smoothed Fit + 4.4% Systematic", "f");
    eff2->GetXaxis()->SetRangeUser(300, 1600);
    eff2->GetYaxis()->SetTitleOffset(1.1);
    eff2->SetMaximum(0.6);
    eff2->SetMinimum(0.0);
    leg->Draw();
    gPad->Print("eff_catoptag_systematic.eps", "eps");
    gPad->Print("eff_catoptag_systematic.gif", "gif");
  }
}
