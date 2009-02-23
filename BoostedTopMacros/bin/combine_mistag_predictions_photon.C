#include "TH2D.h"
#include "TCanvas.h"
#include "TFile.h"
#include "THStack.h"
#include <iostream>

using namespace std;

void combine_mistag_predictions( double Lum = 1.0 )
{

  const char * names [] = {
    "xchecks_gammaplusjet_photonjet_300.root", 
    "xchecks_gammaplusjet_photonjet_470.root", 
    "xchecks_gammaplusjet_photonjet_800.root", 
//     "xchecks_gammaplusjet_pe_photonjet_1400.root", 
//     "xchecks_gammaplusjet_pe_photonjet_2200.root", 
//     "xchecks_gammaplusjet_pe_photonjet_3000.root"
  };

  static const int nnames = sizeof( names ) / sizeof ( const char * );


  double weights[] = {
    4.193   ,
    4.515e-1,
    2.003e-2 ,
    2.686e-4 ,
    1.522e-6 ,
    5.332e-9
  };


  int nevents[] = {
    1104000,
    1092000,
    1104000,
    1100000,
    1100000,
    1100000
  };

  const char * plotnames[] = {
    "total",
    "jet_et",
    "jet_eta",
    "jet_phi"

  };

  bool logy[] = {
    false,
    false,
    false,
    false
  };

  static const int nplots = sizeof( plotnames ) / sizeof ( const char * );
 

  TFile * output = new TFile("xcheck_summary_photons.root", "RECREATE");


  TFile * f [nnames] = {0};

  for ( int iplot = 0; iplot < nplots; ++iplot ) {
    TH1D * obs_sum = 0;
    TH1D * pred_sum = 0;



    TString obs_name( plotnames[iplot] );
    TString pred_name( plotnames[iplot] ); pred_name += "_pred";

    for ( int i = 0; i < nnames; ++i ) {
      if ( f[i] == 0 ) {
	f[i] = new TFile(names[i]);
      } 

      TH1D * obs = (TH1D*) f[i]->Get(obs_name.Data());
      TH1D * pred = (TH1D*) f[i]->Get(pred_name.Data());

      obs->Scale( Lum * weights[i] / (double)nevents[i] );
      pred->Scale( Lum * weights[i] / (double)nevents[i] );


      if ( i == 0 ) {
	output->cd();
	obs_sum = new TH1D(*obs);
	pred_sum = new TH1D(*pred);
// 	obs_sum->Scale( weights[i] / (double)nevents[i]);
// 	pred_sum->Scale( weights[i] / (double)nevents[i]);
      } else {
	obs_sum->Add( obs );
	pred_sum->Add( pred );
      }
    }



//     obs_sum->Rebin(10);
//     pred_sum->Rebin(10);

    TCanvas * c = new TCanvas(obs_name.Data(),obs_name.Data());

    pred_sum->SetLineColor(2);
    pred_sum->SetFillColor(2);
    pred_sum->SetMarkerColor(2);

    obs_sum->SetMinimum(0);

    TString hsname( obs_name ); hsname += +"_hs";

    THStack * hs = new THStack ( hsname.Data(), obs_name.Data() );

    if ( logy[iplot] ) {
      obs_sum->SetMinimum(0.1);
      pred_sum->SetMinimum(0.1);
    }

    hs->Add( pred_sum, "E");
    hs->Add( obs_sum, "E" );


    hs->Draw("nostack");


    if ( logy[iplot] ) {

      hs->SetMinimum(0.1);
      gPad->SetLogy();
    }

    output->cd();
    obs_sum->Write();
    pred_sum->Write();

    TString canvout( obs_name ); canvout += "_predictions_photons.gif";
    c->Print(canvout, "gif");

    TString canvouteps( obs_name ); canvouteps += "_predictions_photons.eps";
    c->Print(canvouteps, "eps");

    if ( iplot == 0 ) {
      char buff[200];
      sprintf( buff, "Obs  = %6.2f +- %6.2f", obs_sum->GetBinContent(2), obs_sum->GetBinError(2));
      cout << buff << endl;
      sprintf( buff, "Pred = %6.2f +- %6.2f", pred_sum->GetBinContent(2), pred_sum->GetBinError(2));
      cout << buff << endl;

    }

  }

}
