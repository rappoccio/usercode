
#include "TCanvas.h"
#include "TH1.h"
#include "TFile.h"
#include "THStack.h"
#include "TLegend.h"
#include "TF1.h"
#include "TMath.h"
#include "TGraphErrors.h"

Double_t fitf(Double_t *v, Double_t *par)
{
   Double_t arg1 = 0;
   if (par[2] != 0) arg1 = (v[0] - par[1])/par[2];
   Double_t arg2 = 0;
   if (par[3] != 0) arg2 = (v[0] - par[1])/par[3];

 
   Double_t fitval = 0;

   if ( v[0] > par[1] ) 
     fitval = par[0]*TMath::Exp(-0.5*arg1*arg1);
   else
     fitval = par[4]*TMath::Exp(-0.5*arg1*arg1) + (par[0] - par[4])*TMath::Exp(-0.5*arg2*arg2);     
   return fitval;
  
}
 



void plot_signal()
{


  const char * filenames[] = {
//     "kinematic_histos_rs_750_fastsim.root",
    "kinematic_histos_rs_1000_fastsim.root",
    "kinematic_histos_rs_1250_fastsim.root",
    "kinematic_histos_rs_1500_fastsim.root",
    "kinematic_histos_rs_2000_fastsim.root",
    "kinematic_histos_rs_2500_fastsim.root",
    "kinematic_histos_rs_3000_fastsim.root"
  };
  
  const int nfiles = sizeof( filenames ) / sizeof( const char *);


  int colors[] = {
//     kSpring,
    kTeal,
    kRed,
    kGreen + 3,
    kBlue,
    kMagenta,
    kBlack
  };

  const char * titles[] = {
//     "M = 750",
    "M = 1000",
    "M = 1250",
    "M = 1500",
    "M = 2000",
    "M = 2500",
    "M = 3000",
  };

  const char * fitnames [] = {
//     "m750",
    "m1000",
    "m1250",
    "m1500",
    "m2000",
    "m2500",
    "m3000",
  };


  double xs [] = {
//     1.151 ,
    0.272 ,
    0.079 ,
    2.617e-2 ,
    4.142e-3 ,
    7.857e-4 ,
    1.721e-4
  };
  
  int nentries [] = {
//     19000  ,
    18000  ,
    18000  ,
    19000  ,
    19000  ,
    16000  ,
    16000
  };

  double Lum = 100.0;
  
  THStack * hs = new THStack("hs", "Dijet Mass, 100 pb^{-1};Dijet Mass (GeV/c^{2});Number per 100 GeV");

  TLegend * leg = new TLegend(0.8, 0.6, 1.0, 1.0);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);

  TF1 * funcs[nfiles];

  for ( int i = 0; i < nfiles; ++i ) {
    TFile * f= new TFile(filenames[i]);
    TH1 * hist_top_dijetmass = (TH1*)f->Get("hist_top_dijetmass");
    
    hist_top_dijetmass->Sumw2();

    hist_top_dijetmass->SetFillColor(colors[i]);
    hist_top_dijetmass->Scale( Lum * xs[i] / (double)nentries[i] );
 
    hs->Add( hist_top_dijetmass );
//     leg->AddEntry( hist_top_dijetmass, titles[i], "f");


    funcs[i] = new TF1(fitnames[i],fitf,
		       0,
		       hist_top_dijetmass->GetMean() +
		       2 * hist_top_dijetmass->GetRMS(),
		       5);
 //    TF1 *func = new TF1(fitnames[i],"gaus",0,5000);
    funcs[i]->SetParameter(0, xs[i]);
    funcs[i]->SetParameter(1, hist_top_dijetmass->GetMean());
    funcs[i]->SetParameter(2, hist_top_dijetmass->GetRMS());
    funcs[i]->SetParameter(3, hist_top_dijetmass->GetRMS());
    funcs[i]->SetParameter(4, xs[i]);
    funcs[i]->SetParNames("Constant", 
			  "Peak",
			  "Core Width",
			  "Tail Width",
			  "Tail Peak" );
    hist_top_dijetmass->Fit(funcs[i], "R0");
    funcs[i] = hist_top_dijetmass->GetFunction(fitnames[i]);
    funcs[i]->SetLineColor(colors[i]);
    leg->AddEntry( funcs[i], titles[i], "l");
  }

  double resolution_x[nfiles] = { 1000, 1250, 1500, 2000, 2500, 3000};
  double resolution_dx[nfiles]= {    0,    0,    0,    0,    0,    0};
  double resolution_y[nfiles] = {};
  double resolution_dy[nfiles] = {};
  TCanvas * c1 = new TCanvas("c1", "c1");
  TH1D * foraxes = new TH1D("foraxes", "Resonance Resolutions in 100 pb^{-1};Dijet Mass (GeV/c^{2});Number", 5000, 0, 5000);
  foraxes->SetMinimum(1e-6);
  foraxes->SetMaximum(1.0);
  foraxes->Draw();
  foraxes->GetYaxis()->SetTitleOffset(1.0);
  for ( int i = 0; i < nfiles; ++i ) {
    funcs[i]->Draw("same");
    resolution_y[i] = funcs[i]->GetParameter(2);
    resolution_dy[i] = funcs[i]->GetParError(2);
  }
  leg->Draw();
  c1->SetLogy();

  TCanvas * c2 = new TCanvas("c2", "c2");
  TGraphErrors * resolution = new TGraphErrors(nfiles, 
					       resolution_x, resolution_y,
					       resolution_dx, resolution_dy );
			
  TH1D * foraxes2 = new TH1D("foraxes2", "Dijet Resolution Expectation;Dijet Mass (GeV/c^{2});Resolution (GeV)", 5000,0, 5000);
  foraxes2->Draw();
  foraxes2->SetMaximum(200);
  foraxes2->GetYaxis()->SetTitleOffset(1.0);
  resolution->Draw("LP");

//   hs->Draw("nostack");
//   leg->Draw();
//   hs->GetYaxis()->SetTitleOffset(1.0);
//   gPad->Print("signal_dijetmass_100pb_linear.gif", "gif");
//   gPad->Print("signal_dijetmass_100pb_linear.eps", "eps");
//   gPad->SetLogy();
//   gPad->Print("signal_dijetmass_100pb_log.gif", "gif");
//   gPad->Print("signal_dijetmass_100pb_log.eps", "eps");
}
