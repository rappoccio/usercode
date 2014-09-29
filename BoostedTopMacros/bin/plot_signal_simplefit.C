#include "TCanvas.h"
#include "TH1.h"
#include "TFile.h"
#include "THStack.h"
#include "TLegend.h"
#include "TF1.h"
#include "TMath.h"
#include "TGraphErrors.h"
#include "TString.h"

#include <iostream>




void plot_signal()
{


  const char * filenames[] = {
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

  double masses [] = {
    1000,
    1250,
    1500,
    2000,
    2500,
    3000
  };

  double bins[][2] = {
    {500,  1300}, // 1000
    {900,  1400}, // 1250
    {1200, 1600}, // 1500
    {1700, 2200}, // 2000
    {2200, 2800}, // 2500
    {2600, 3200}  // 3000
  };

  double Lum = 100.0;
  
  THStack * hs = new THStack("hs", "Dijet Mass, 100 pb^{-1};Dijet Mass (GeV/c^{2});Number per 100 GeV");

  TLegend * leg = new TLegend(0.8, 0.6, 1.0, 1.0);
  leg->SetFillColor(0);
  leg->SetLineColor(0);
  leg->SetBorderSize(0);

  TF1 * funcs[nfiles];

  TCanvas * c0 = new TCanvas("c0", "c0");

  for ( int i = 0; i < nfiles; ++i ) {
    TFile * f= new TFile(filenames[i]);
    TH1 * hist_top_dijetmass = (TH1*)f->Get("hist_top_dijetmass");
    
    hist_top_dijetmass->Sumw2();

    hist_top_dijetmass->SetFillColor(colors[i]);
    hist_top_dijetmass->Scale( Lum * xs[i] / (double)nentries[i] );
 
    hs->Add( hist_top_dijetmass );
//     leg->AddEntry( hist_top_dijetmass, titles[i], "f");


    double mean = hist_top_dijetmass->GetMean();
    double rms  = hist_top_dijetmass->GetRMS();
    funcs[i] = new TF1(fitnames[i],"gaus", bins[i][0], bins[i][1] );


    hist_top_dijetmass->Fit(funcs[i], "R");
//     funcs[i] = hist_top_dijetmass->GetFunction(fitnames[i]);
    funcs[i]->SetLineColor(colors[i]);

    // Now print function parameters correctly


    leg->AddEntry( funcs[i], titles[i], "l");
    TString outname1("fit_");
    outname1 += fitnames[i];
    outname1 += ".gif";
    c0->Print(outname1.Data(), "gif");
    TString outname2("fit_");
    outname2 += fitnames[i];
    outname2 += ".eps";
    c0->Print(outname2.Data(), "eps");
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
    double mean = funcs[i]->GetParameter(1);
    double dmean = funcs[i]->GetParError(1);

    double sigma = funcs[i]->GetParameter(2);
    double dsigma = funcs[i]->GetParError(2);

    double f = sigma / mean;

    double df = TMath::Sqrt( dsigma*dsigma / (mean*mean) + (sigma*sigma*dmean*dmean)/(mean*mean*mean*mean) );

    resolution_y[i] = f;
    resolution_dy[i] = df;
  }
  leg->Draw();
  c1->SetLogy();
  c1->Print("resolution_fits.gif", "gif");
  c1->Print("resolution_fits.eps", "eps");

  TCanvas * c2 = new TCanvas("c2", "c2");
  TGraphErrors * resolution = new TGraphErrors(nfiles, 
					       resolution_x, resolution_y,
					       resolution_dx, resolution_dy );
			
  TH1D * foraxes2 = new TH1D("foraxes2", "Dijet Resolution Expectation;Dijet Mass (GeV/c^{2});Resolution (GeV)", 5000,0, 5000);
  foraxes2->Draw();
  foraxes2->SetMaximum(160);
  foraxes2->SetMinimum(70);
  foraxes2->GetYaxis()->SetTitleOffset(1.0);
  resolution->Draw("LP");

  c2->Print("resolution_function.gif", "gif");
  c2->Print("resolution_function.eps", "eps");

//   hs->Draw("nostack");
//   leg->Draw();
//   hs->GetYaxis()->SetTitleOffset(1.0);
//   gPad->Print("signal_dijetmass_100pb_linear.gif", "gif");
//   gPad->Print("signal_dijetmass_100pb_linear.eps", "eps");
//   gPad->SetLogy();
//   gPad->Print("signal_dijetmass_100pb_log.gif", "gif");
//   gPad->Print("signal_dijetmass_100pb_log.eps", "eps");
}

