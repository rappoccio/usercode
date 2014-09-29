#include "TH2D.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TLegend.h"
#include "THStack.h"

#include "palette.C"

#include <iostream>

using namespace std;

void combine_mistag_rates(double Lum = 1.0)
{

  double deff = 0.065; // fractional efficiency uncertainty

  const char * names [] = {
    "mistag_parameterization_qcd_230_v5.root", 
    "mistag_parameterization_qcd_300_v5.root", 
    "mistag_parameterization_qcd_380_v5.root", 
    "mistag_parameterization_qcd_470_v5.root", 
    "mistag_parameterization_qcd_600_v5.root", 
    "mistag_parameterization_qcd_800_v5.root", 
    "mistag_parameterization_qcd_1000_v5.root", 
    "mistag_parameterization_qcd_1400_v5.root", 
    "mistag_parameterization_qcd_1800_v5.root", 
    "mistag_parameterization_qcd_2200_v5.root", 
    "mistag_parameterization_qcd_2600_v5.root", 
    "mistag_parameterization_qcd_3000_v5.root", 
    "mistag_parameterization_qcd_3500_v5.root",
    "mistag_parameterization_ttbar_v5.root",
  };


//   double xs[] = {
//     10623.2,
//     2634.94,
//     722.099,
//     240.983,
//     62.4923,
//     9.42062,
//     2.34357,
//     0.1568550,
//     0.013811,
//     0.00129608,
//     0.00011404,
//     0.0000084318,
//     0.00000018146
//   };


//   int nevents[] = {
//     54000,
//     54000,
//     51840,
//     27648,
//     28620,
//     20880,
//     24640,
//     27744,
//     22848,
//     22560,
//     22800,
//     20880,
//     34320
//   };


  const char * filetitles[] = {
    "#hat{pt} = 230-300",
    "#hat{pt} = 300-380",
    "#hat{pt} = 380-470",
    "#hat{pt} = 470-600",
    "#hat{pt} = 600-800",
    "#hat{pt} = 800-1000",
    "#hat{pt} = 1000-1400",
    "#hat{pt} = 1400-1800",
    "#hat{pt} = 1800-2200",
    "#hat{pt} = 2200-2600",
    "#hat{pt} = 2600-3000",
    "#hat{pt} = 3000-3500",
    "#hat{pt} = 3500-Inf",
    "t#bar{t} Continuum"
  };


  static const int N = sizeof( names ) / sizeof ( const char * );

  TColor appended = TColor(259, 0, 0, 1.0);

  palette(8, 251, 1, &appended);

  TFile * output = new TFile("mistag_parameterization_100pb.root", "RECREATE");
  TH1D * numerator_sum = 0;
  TH1D * denominator_sum = 0;

  THStack * numerator_hs = new THStack("numerator_hs", "Fake Tag Rate Numerator, 100 pb^{-1};Jet p_{T} (GeV/c);Number");
  THStack * denominator_hs = new THStack("denominator_hs", "Fake Tag Rate Denominator, 100 pb^{-1};Jet p_{T} (GeV/c);Number");

  TLegend * leg = new TLegend(0.6, 0.5, 0.9, 1.0);
  leg->SetFillColor(0); 
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  int colcount = 0;

  // get the sum which is a proxy for the data
  for ( int i = 0; i < N; ++i ) {
    TFile * f = new TFile(names[i]);
    TH1D * numerator = (TH1D*) f->Get("numerator");
    TH1D * denominator = (TH1D*) f->Get("denominator");

    numerator->Scale(Lum);
    denominator->Scale(Lum);

    numerator->GetXaxis()->SetRangeUser(0., 2000.);
    denominator->GetXaxis()->SetRangeUser(0., 2000.);


      if ( numerator->Integral() > 1.0 ) {
	++colcount;
	numerator->SetFillColor(251 + colcount);
	denominator->SetFillColor(251 + colcount);

	numerator_hs->Add( numerator );
	denominator_hs->Add( denominator );

	leg->AddEntry( numerator, filetitles[i], "f");
      }
      char buff[1000];
      sprintf(buff, "%30s & %6.0f & %6.0f ", names[i], denominator->GetEntries(), numerator->GetEntries() );
      cout << buff << endl;

      if ( i == 0 ) {
	output->cd();
	numerator_sum = new TH1D(*numerator);
	denominator_sum = new TH1D(*denominator);
      } else {
	numerator_sum->Add( numerator );
	denominator_sum->Add( denominator );
      }
    
  }

  

  // Now clear the errors, and set them to what would be Poisson on the absolute number with luminosity

  for ( int i = 0; i <= numerator_sum->GetNbinsX(); ++i ) {
    double a = numerator_sum->GetBinContent(i);
    double b = denominator_sum->GetBinContent(i);
    
    numerator_sum->SetBinError(i, sqrt(a) );
    denominator_sum->SetBinError(i, sqrt(b) );
  }

  cout << "Subtracting off ttbar" << endl;
  // Now subtract off the ttbar contribution, and add 100% of the subtraction as a systematic
  TFile * ttbar = new TFile(names[N-1]);
  TH1D * ttbar_num = (TH1D*)ttbar->Get("numerator");
  TH1D * ttbar_den = (TH1D*)ttbar->Get("denominator");

  cout << "Scaling ttbar" << endl;
  ttbar_num->Scale(Lum);
  ttbar_den->Scale(Lum);

  cout << "Making corrected numerator" << endl;
  TH1D * numerator_sum_corrected = new TH1D(*numerator_sum);
  numerator_sum_corrected->SetName("numerator_sum_corrected");
  numerator_sum_corrected->Add( ttbar_num, -1.0);


  cout << "Making corrected denominator" << endl;
  TH1D * denominator_sum_corrected = new TH1D(*denominator_sum);
  denominator_sum_corrected->SetName("denominator_sum_corrected");
  denominator_sum_corrected->Add( ttbar_den, -1.0);

  cout << "Setting mistag rates" << endl;
  TH1D * mistag_rate = new TH1D(*numerator_sum);
  mistag_rate->SetName("mistag_rate");
  mistag_rate->SetTitle("Fake Tag Parameterization;Jet p_{T}(GeV/c);Rate");
  mistag_rate->GetXaxis()->SetTitleSize(0.06);
  mistag_rate->GetXaxis()->SetTitleFont(42);
  mistag_rate->GetYaxis()->SetTitleSize(0.06);
  mistag_rate->GetYaxis()->SetTitleFont(42);
  mistag_rate->GetXaxis()->SetLabelSize(0.05);
  mistag_rate->GetXaxis()->SetLabelFont(42);
  mistag_rate->GetYaxis()->SetLabelSize(0.05);
  mistag_rate->GetYaxis()->SetLabelFont(42);
  mistag_rate->SetLineColor(2);

  mistag_rate->Sumw2();
  mistag_rate->Divide( numerator_sum, denominator_sum, 1.0, 1.0, "b");

  TH1D * mistag_rate_stat = new TH1D(*numerator_sum_corrected);
  mistag_rate_stat->SetName("mistag_rate_stat");
  mistag_rate_stat->SetTitle("Fake Tag Parameterization;Jet p_{T}(GeV/c);Rate");
  mistag_rate_stat->GetXaxis()->SetTitleSize(0.06);
  mistag_rate_stat->GetXaxis()->SetTitleFont(42);
  mistag_rate_stat->GetYaxis()->SetTitleSize(0.06);
  mistag_rate_stat->GetYaxis()->SetTitleFont(42);
  mistag_rate_stat->GetXaxis()->SetLabelSize(0.05);
  mistag_rate_stat->GetXaxis()->SetLabelFont(42);
  mistag_rate_stat->GetYaxis()->SetLabelSize(0.05);
  mistag_rate_stat->GetYaxis()->SetLabelFont(42);
  mistag_rate_stat->SetLineColor(2);


  TH1D * mistag_rate_statsys = new TH1D(*numerator_sum_corrected);
  mistag_rate_statsys->SetName("mistag_rate_statsys");
  mistag_rate_statsys->SetTitle("Fake Tag Parameterization;Jet p_{T}(GeV/c);Rate");
  mistag_rate_statsys->GetXaxis()->SetTitleSize(0.06);
  mistag_rate_statsys->GetXaxis()->SetTitleFont(42);
  mistag_rate_statsys->GetYaxis()->SetTitleSize(0.06);
  mistag_rate_statsys->GetYaxis()->SetTitleFont(42);
  mistag_rate_statsys->GetXaxis()->SetLabelSize(0.05);
  mistag_rate_statsys->GetXaxis()->SetLabelFont(42);
  mistag_rate_statsys->GetYaxis()->SetLabelSize(0.05);
  mistag_rate_statsys->GetYaxis()->SetLabelFont(42);
  mistag_rate_statsys->SetLineColor(4);

  cout << "Dividing corrected" << endl;
  mistag_rate_statsys->Sumw2();
  mistag_rate_stat->Sumw2();

  cout << "Parameterization: " << endl;

  char bufftitle[1000];
  //                  bin    pt   raw1    raw2    fraw    corr1   corr2   fcorr   ntt     ftt     stat   sys     statsys 
  sprintf( bufftitle, "%4s & %8s  & %8s & %8s & %8s & %8s & %8s & %8s & %8s & %8s & %8s & %8s & %8s \\",
	   "Bin",
	   "Pt",
	   "Num",
	   "Den",
	   "f",
	   "Ntt",
	   "Ftt",
	   "CorrNum",
	   "CorrDen",
	   "Corrf",
	   "Stat",
	   "Sys",
	   "Stat+Sys"
	   );
  cout << bufftitle << endl;
  for ( int i = 0; i <= mistag_rate->GetNbinsX(); ++i ) {

    double a = numerator_sum->GetBinContent(i);
    double b = denominator_sum->GetBinContent(i);     // for stat error, need total, not corrected total
    
    double val = ( b > 0.) ? a / b : 0.0;
    double err = ( b > 0.) ? sqrt(val*(1-val)/b) : 0.0;
    
    double ntt = ttbar_num->GetBinContent(i);
    double N   = denominator_sum->GetBinContent(i);

    double err2 = 0.0;
    double ftt = 0.0;
    if ( N > 0 ) {
      ftt = ntt / N;
      err2 = ftt * (1+deff);
    }

    double corr_a = numerator_sum_corrected->GetBinContent(i);
    double corr_b = denominator_sum_corrected->GetBinContent(i);

    double corrval = (corr_b > 0.0) ? corr_a/corr_b : 0.0;

    mistag_rate_stat->SetBinContent( i, corrval);
    mistag_rate_stat->SetBinError(i, err );

    mistag_rate_statsys->SetBinContent( i, corrval);
    mistag_rate_statsys->SetBinError(i, sqrt(err*err + err2*err2) );

    double pt = mistag_rate_statsys->GetXaxis()->GetBinUpEdge( i );

//     cout << "Bin i = " << i << endl;
//     cout << "       raw rate = " << numerator_sum->GetBinContent(i) << " / " << denominator_sum->GetBinContent(i) << " = " << val << endl;
//     cout << " corrected rate = " << numerator_sum_corrected->GetBinContent(i) << " / " << denominator_sum_corrected->GetBinContent(i) << " = " << corrval << endl;
//     cout << "            ftt = " << ntt << " / " << N << " = " << ftt << endl;
//     cout << "       stat err = " << err << endl;
//     cout << "        sys err = " << err2 << endl;
//     cout << "     stat + sys = " << mistag_rate_statsys->GetBinError(i) << endl;

    char buff[1000];
    //            bin    pt       raw1    raw2    fraw    ntt     ftt     corr1   corr2   fcorr   stat   sys     statsys 
    sprintf(buff, "%4d & %8.0f  & %8.1f & %8.1f & %8.2e & %8.1f & %8.2e & %8.1f & %8.1f & %8.2e & %8.2e & %8.2e & %8.2e \\\\",
	    i, 
	    pt, 
	    numerator_sum->GetBinContent(i),
	    denominator_sum->GetBinContent(i),
	    val,
	    ntt,
	    ftt,
	    numerator_sum_corrected->GetBinContent(i),
	    denominator_sum_corrected->GetBinContent(i),
	    corrval,
	    err,
	    err2, 
	    mistag_rate_statsys->GetBinError(i) );
    cout << buff << endl;
  }

  cout << "Drawing" << endl;
  TCanvas * c = new TCanvas("c", "c", 600, 800);

  c->Divide(1,3);
  c->cd(1);
  numerator_hs->SetMinimum(0.1);
  numerator_hs->SetMaximum(3e2);
  numerator_hs->Draw("nostack hist");
  leg->Draw();
  gPad->SetLogy();
  c->cd(2);
  denominator_hs->SetMinimum(0.1);
  denominator_hs->Draw("nostack hist");
  gPad->SetLogy();
  c->cd(3);
  gStyle->SetOptStat(000000);
  mistag_rate_statsys->SetMinimum(0.0);
  mistag_rate_statsys->SetMaximum(0.08);
  mistag_rate_statsys->SetMarkerStyle(20);
  mistag_rate_statsys->Draw("e1");
  mistag_rate_stat->Draw("e1 same");

//   mistag_rate_statsys->SetMinimum(1e-5);
//   mistag_rate_statsys->SetMaximum(5e-1);

  TLegend * leg_eff = new TLegend( 0.2, 0.6, 0.4, 0.8);
  leg_eff->AddEntry( mistag_rate_statsys, "Stat #oplus Sys", "l");
  leg_eff->AddEntry( mistag_rate_stat,    "Stat", "l");
  leg_eff->SetFillColor(0);
  leg_eff->SetBorderSize(0);
  leg_eff->Draw();

  numerator_hs->GetYaxis()->SetTitle("Number");
  denominator_hs->GetYaxis()->SetTitle("Number");

  numerator_hs->GetYaxis()->SetTitleOffset(1.1);
  denominator_hs->GetYaxis()->SetTitleOffset(1.1);
  mistag_rate_statsys->GetYaxis()->SetTitleOffset(1.1);

  numerator_hs->GetXaxis()->SetRangeUser(0., 2000.);
  denominator_hs->GetXaxis()->SetRangeUser(0., 2000.);
  mistag_rate_statsys->GetXaxis()->SetRangeUser(0., 2000.);
  mistag_rate->GetXaxis()->SetRangeUser(0., 2000.);

  output->cd();
  numerator_sum->Write();
  denominator_sum->Write();
  mistag_rate->Write();
  mistag_rate_statsys->Write();

  c->Print("mistag_param_lum.gif", "gif");
  c->Print("mistag_param_lum.eps", "eps");

}
