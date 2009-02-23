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

  const char * names [] = {
    "mistag_parameterization_qcd_230.root", 
    "mistag_parameterization_qcd_300.root", 
    "mistag_parameterization_qcd_380.root", 
    "mistag_parameterization_qcd_470.root", 
    "mistag_parameterization_qcd_600.root", 
    "mistag_parameterization_qcd_800.root", 
    "mistag_parameterization_qcd_1000.root", 
    "mistag_parameterization_qcd_1400.root", 
    "mistag_parameterization_qcd_1800.root", 
    "mistag_parameterization_qcd_2200.root", 
    "mistag_parameterization_qcd_2600.root", 
    "mistag_parameterization_qcd_3000.root", 
    "mistag_parameterization_qcd_3500.root"
  };


  double xs[] = {
    10623.2,
    2634.94,
    722.099,
    240.983,
    62.4923,
    9.42062,
    2.34357,
    0.1568550,
    0.013811,
    0.00129608,
    0.00011404,
    0.0000084318,
    0.00000018146
  };


  int nevents[] = {
    54000,
    54000,
    51840,
    27648,
    28620,
    20880,
    24640,
    27744,
    22848,
    22560,
    22800,
    20880,
    34320
  };


  const char * filetitles[] = {
    "QCD Dijets, #hat{pt} = 230-300",
    "QCD Dijets, #hat{pt} = 300-380",
    "QCD Dijets, #hat{pt} = 380-470",
    "QCD Dijets, #hat{pt} = 470-600",
    "QCD Dijets, #hat{pt} = 600-800",
    "QCD Dijets, #hat{pt} = 800-1000",
    "QCD Dijets, #hat{pt} = 1000-1400",
    "QCD Dijets, #hat{pt} = 1400-1800",
    "QCD Dijets, #hat{pt} = 1800-2200",
    "QCD Dijets, #hat{pt} = 2200-2600",
    "QCD Dijets, #hat{pt} = 2600-3000",
    "QCD Dijets, #hat{pt} = 3000-3500",
    "QCD Dijets, #hat{pt} = 3500-Inf"
  };


  static const int N = sizeof( names ) / sizeof ( const char * );

  palette(7);

  TFile * output = new TFile("mistag_parameterization_100pb.root", "RECREATE");
  TH1D * numerator_sum = 0;
  TH1D * denominator_sum = 0;

  THStack * numerator_hs = new THStack("numerator_hs", "Fake Tag Rate Numerator, 100 pb^{-1};Jet E_{T} (GeV/c^{2});Number per 100 GeV/c");
  THStack * denominator_hs = new THStack("denominator_hs", "Fake Tag Rate Denominator, 100 pb^{-1};Jet E_{T} (GeV/c^{2});Number per 100 GeV/c");

  TLegend * leg = new TLegend(0.7, 0.5, 1.0, 1.0);
  leg->SetFillColor(0); 
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  int colcount = 0;

  for ( int i = 0; i < N; ++i ) {
    TFile * f = new TFile(names[i]);
    TH1D * numerator = (TH1D*) f->Get("numerator");
    TH1D * denominator = (TH1D*) f->Get("denominator");

    numerator->Scale(Lum);
    denominator->Scale(Lum);

    numerator->GetXaxis()->SetRangeUser(0., 1500.);
    denominator->GetXaxis()->SetRangeUser(0., 1500.);


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

  TH1D * mistag_rate = new TH1D(*numerator_sum);
  mistag_rate->SetName("mistag_rate");
  mistag_rate->SetTitle("Fake Tag Parameterization");
  
  mistag_rate->Divide( numerator_sum, denominator_sum, 1.0, 1.0, "b");


  cout << "Parameterization: " << endl;
  for ( int i = 0; i <= mistag_rate->GetNbinsX(); ++i ) {
    char buff[400];
    sprintf(buff, "%8.4f +- %8.4f = %8.4f / %8.4f", 
	    mistag_rate->GetBinContent(i),
	    mistag_rate->GetBinError(i),
	    numerator_sum->GetBinContent(i),
	    denominator_sum->GetBinContent(i) );
    cout << buff << endl;
  }

  TCanvas * c = new TCanvas("c", "c", 600, 800);

  c->Divide(1,3);
  c->cd(1);
  numerator_hs->SetMinimum(0.1);
  numerator_hs->Draw("nostack hist");
  leg->Draw();
  gPad->SetLogy();
  c->cd(2);
  denominator_hs->SetMinimum(0.1);
  denominator_hs->Draw("nostack hist");
  gPad->SetLogy();
  c->cd(3);
  gStyle->SetOptStat(000000);
  mistag_rate->SetMinimum(0.0);
  mistag_rate->SetMaximum(0.06);
  mistag_rate->Draw("e");
  


  numerator_hs->GetYaxis()->SetTitle("Number per 100 GeV/c");
  denominator_hs->GetYaxis()->SetTitle("Number per 100 GeV/c");

  numerator_hs->GetYaxis()->SetTitleOffset(1.1);
  denominator_hs->GetYaxis()->SetTitleOffset(1.1);

  numerator_hs->GetXaxis()->SetRangeUser(0., 1500.);
  denominator_hs->GetXaxis()->SetRangeUser(0., 1500.);

  output->cd();
  numerator_sum->Write();
  denominator_sum->Write();
  mistag_rate->Write();

  c->Print("mistag_param_lum.gif", "gif");
  c->Print("mistag_param_lum.eps", "eps");

}
