{

  double systematic = sqrt( 0.044*0.044 + 0.033*0.033 + 0.029*0.029 + 0.029*0.029);

  const char * files[] = {
    "kinematic_histos_zprime_m1000_w100_v5.root",
    "kinematic_histos_zprime_m2000_w200_v5.root",
    "kinematic_histos_zprime_m3000_w300_v5.root",
    "kinematic_histos_zprime_m4000_w400_v5.root",
  };

  TH1D * hist_tagged_top_jetPt = 0;
  TH1D * hist_top_jetPt = 0;

  TF1 * erf = new TF1("erf", "[0] * TMath::Erf((x - [1]) / [2])", 0, 1600);

  erf->SetParameter(0,0.3);
  erf->SetParameter(1,300);
  erf->SetParameter(2,100);

  erf->SetParName(0, "Constant");
  erf->SetParName(1, "Offset");
  erf->SetParName(2, "Width");


  const int NFILES = sizeof(files)/sizeof(const char *);

  for (int i = 0; i < NFILES; ++i ) {
    cout << "Processing i = " << i << ",  file = " << files[i] << endl;
    TFile * f = new TFile(files[i]);
    TH1D * h1 = (TH1D*)f->Get("hist_tagged_top_jetPt");
    TH1D * h2 = (TH1D*)f->Get("hist_top_jetPt");

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
      hist_tagged_top_jetPt = new TH1D(*h1);
      hist_tagged_top_jetPt->SetName("total_tagged_top_jetPt");
      hist_tagged_top_jetPt->SetTitle("CATopTag Efficiency;Jet p_{T} (GeV/c);Efficiency");
      hist_top_jetPt = new TH1D(*h2);
      hist_top_jetPt->SetName("total_top_jetPt");
    } else {
      cout << "Adding histograms" << endl;
      hist_tagged_top_jetPt->Add(h1);
      hist_top_jetPt->Add(h2);
    }
  }

  cout << "About to plot" << endl;
  if ( hist_tagged_top_jetPt == 0 ) {
    cout << "error! about to crash" << endl;
  } else {
    hist_tagged_top_jetPt->Sumw2();
    hist_top_jetPt->Sumw2();

    TH1D * eff = new TH1D(*hist_tagged_top_jetPt);

    eff->Divide( hist_tagged_top_jetPt, hist_top_jetPt, 1.0, 1.0, "b");

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

    const int N_STEP = 100;

    double xmin = 0;
    double xmax = 1600;
    double diff = xmax - xmin;
    double step = diff / (double)N_STEP;

    double smooth_x [N_STEP];
    double smooth_y [N_STEP];
    double smooth_ex [N_STEP];
    double smooth_ey [N_STEP];

    for ( int i = 0; i < 100; ++i ) {
      smooth_x[i] = i*step+xmin;
      smooth_y[i] = erf->Eval(i*step+xmin);
      smooth_ex[i] = 0.0;
      smooth_ey[i] = 0.044 * fabs(smooth_y[i]);
      cout << "y = " << smooth_y[i] << " +- " << smooth_ey[i] << endl;
    }

    TGraphErrors * smooth = new TGraphErrors( N_STEP, smooth_x, smooth_y, smooth_ex, smooth_ey );
    
    smooth->SetFillColor(4);
    smooth->SetFillStyle(3244);


    smooth->Draw("3 same");

    eff2->Draw("same");


    leg->AddEntry( eff2, "Monte Carlo Statistics", "p");
//     leg->AddEntry( eff,  "+ 4.4% Systematic", "f");
    leg->AddEntry( smooth,  "Smoothed Fit + 6.9% Systematic", "f");
    eff2->GetXaxis()->SetRangeUser(0, 1600);
    eff2->GetYaxis()->SetTitleOffset(1.1);
    eff2->SetMaximum(1.0);
    eff2->SetMinimum(0.0);
    leg->Draw();
    gPad->Print("eff_catoptag_systematic.eps", "eps");
    gPad->Print("eff_catoptag_systematic.gif", "gif");
  }
}
