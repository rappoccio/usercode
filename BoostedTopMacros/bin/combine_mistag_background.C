#include "TH2D.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TLegend.h"
#include "THStack.h"

#include "palette.C"

#include <iostream>

using namespace std;

void combine_mistag_background() // pb-1
{

  const char * names [] = {
    "mistag_background_qcd_230.root", 
    "mistag_background_qcd_300.root", 
    "mistag_background_qcd_380.root", 
    "mistag_background_qcd_470.root", 
    "mistag_background_qcd_600.root", 
    "mistag_background_qcd_800.root", 
    "mistag_background_qcd_1000.root", 
    "mistag_background_qcd_1400.root", 
    "mistag_background_qcd_1800.root", 
    "mistag_background_qcd_2200.root", 
    "mistag_background_qcd_2600.root", 
    "mistag_background_qcd_3000.root", 
    "mistag_background_qcd_3500.root"
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

  TFile * output = new TFile("mistag_backgrounds_100pb.root", "RECREATE");
  static const int N = sizeof( names ) / sizeof ( const char * );

  palette(8);

  TH1D * pred_sum = 0;
  TH1D * obs_sum = 0;

  THStack * pred_hs = new THStack("pred_hs", "Predicted Dijet Spectrum, 100 pb^{-1};Dijet Mass (GeV/c^{2});Number per 50 GeV/c");
  THStack * obs_hs  = new THStack("obs_hs",  "Observed  Dijet Spectrum, 100 pb^{-1};Dijet Mass (GeV/c^{2});Number per 50 GeV/c");


  TLegend * leg = new TLegend(0.7, 0.5, 1.0, 1.0);
  leg->SetFillColor(0); 
  leg->SetLineColor(0);
  leg->SetBorderSize(0);
  int colcount = 0;

  for ( int i = 0; i < N; ++i ) {
    TFile * f = new TFile(names[i]);
    TH1D * pred = (TH1D*) f->Get("dijetmass_pred");
    TH1D * obs = (TH1D*) f->Get("dijetmass");


//     pred->GetXaxis()->SetRangeUser(0., 1500.);
//     obs->GetXaxis()->SetRangeUser(0., 1500.);


      if ( pred->Integral() > 0.0001 ) {
	pred->SetFillColor(251 + colcount);
	obs->SetFillColor(251 + colcount);

	pred_hs->Add( pred );
	obs_hs->Add( obs );
	
	leg->AddEntry( pred, filetitles[i], "f");

	if ( colcount == 0 ) {
	  output->cd();
	  pred_sum = new TH1D(*pred);
	  obs_sum = new TH1D(*obs);
	  pred_sum->SetName("pred_sum");
	  obs_sum->SetName("obs_sum");
	} else {
	  pred_sum->Add( pred );
	  obs_sum->Add( obs );
	}

	++colcount;
      }
      char buff[1000];
      sprintf(buff, "%35s & %6.3f & %6.3f ", names[i], obs->Integral(), pred->Integral() );
      cout << buff << endl;

    
  }




  TCanvas * c = new TCanvas("c", "c");

  output->cd();
//   pred_hs->SetMinimum(0.1);
  pred_hs->Draw("hist");
  pred_sum->Draw("e same");
  pred_hs->SetMaximum(0.8);
  leg->Draw();

  pred_hs->Write();
  pred_sum->Write();
  obs_hs->Write();
  obs_sum->Write();

  pred_hs->GetYaxis()->SetTitle("Number per 100 GeV");
//   obs_hs->GetYaxis()->SetTitle("Number per 100 GeV");

  pred_hs->GetYaxis()->SetTitleOffset(1.1);
//   obs_hs->GetYaxis()->SetTitleOffset(1.1);

//   pred_hs->GetXaxis()->SetRangeUser(0., 1500.);
//   obs_hs->GetXaxis()->SetRangeUser(0., 1500.);

//   output->cd();
//   pred_sum->Write();
//   obs_sum->Write();
//   mistag_rate->Write();

  c->Print("mistag_background_100pb.gif", "gif");
  c->Print("mistag_background_100pb.eps", "eps");

}
