
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

// Fit to two double Gaussians, split.
// Constrain to be continuous and differentiable
// at the mean value
Double_t fitf(Double_t *v, Double_t *par)
{

  // Central value is always the same
  double x0 = par[0];

  //
  // Standard Deviations
  //
  // Core Gaussian
  double s1 = par[1];
  // Left tail
  double s2 = par[2];
  // Right tail
  double s3 = par[3];

  //
  // Amplitudes
  //
  double A1 = par[4]; // Left core amplitude
  double A2 = par[5]; // Left tail amplitude
  double B1;          // Right core amplitude... constrained
  double B2;          // Right tail amplitude... constrained

  // Set the constrains from requiring to be continuously differentiable at center

  double s12 = s1*s1;
  double s22 = s2*s2;
  double s32 = s3*s3;
  if ( fabs(s32 - s12) < 0.000001 ) // Initialization must be dealt with
    B1 = par[4];
  else 
    B1 = (-A1/s12 - A2/s22 + (A1+A2)/s32) / (1/s32 - 1/s12);
  B2 = A1 + A2 - B1;

//   cout << "Setting stuff : " << endl;
//   cout << "A1 = " << A1 << endl;
//   cout << "A2 = " << A2 << endl;
//   cout << "B1 = " << B1 << endl;
//   cout << "B2 = " << B2 << endl;
//   cout << "x0 = " << x0 << endl;
//   cout << "s1 = " << s1 << endl;
//   cout << "s2 = " << s2 << endl;
//   cout << "s3 = " << s3 << endl;

  
  
   Double_t arg1 = 0;
   if (s1 != 0) arg1 = (v[0] - x0)/s1;
   Double_t arg2 = 0;
   if (s2 != 0) arg2 = (v[0] - x0)/s2;
   Double_t arg3 = 0;
   if (s3 != 0) arg3 = (v[0] - x0)/s3;

//    cout << "arg1 = " << arg1 << endl;
//    cout << "arg2 = " << arg2 << endl;
//    cout << "arg3 = " << arg3 << endl;
 
   Double_t fitval = 0;

   if ( v[0] < x0 ) {
     fitval = A1*TMath::Exp(-0.5*arg1*arg1) + A2 * TMath::Exp(-0.5*arg2*arg2);
   }
   else {
     fitval = B1*TMath::Exp(-0.5*arg1*arg1) + B2 * TMath::Exp(-0.5*arg3*arg3);
   }

//    cout << "fitval = " << fitval << endl;

//    char ci;
//    cin >> ci;
   return fitval;
  
}
 



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


    funcs[i] = new TF1(fitnames[i],fitf,0,5000,6);
    double mean = hist_top_dijetmass->GetMean();
    double rms  = hist_top_dijetmass->GetRMS();
    funcs[i]->SetParameter(0, mean );  // Peak value
    funcs[i]->SetParameter(1, rms  );  // Core width
    funcs[i]->SetParameter(2, rms  );  // Left width
    funcs[i]->SetParameter(3, rms  );  // Right width
    funcs[i]->SetParameter(4, xs[i]);  // Core amplitude 1
    funcs[i]->SetParameter(5, xs[i]);  // Tail amplitude left side


    funcs[i]->SetParNames("Peak",
			  "CoreWidth",
			  "LeftTail",
			  "RightTail",
			  "CoreAmp",
			  "LeftAmp" );
    hist_top_dijetmass->Fit(funcs[i], "R");
    funcs[i] = hist_top_dijetmass->GetFunction(fitnames[i]);
    funcs[i]->SetLineColor(colors[i]);

    // Now print function parameters correctly


    double s1 = funcs[i]->GetParameter(1);
    // Left tail
    double s2 = funcs[i]->GetParameter(2);
    // Right tail
    double s3 = funcs[i]->GetParameter(3);


  double s12 = s1*s1;
  double s22 = s2*s2;
  double s32 = s3*s3;    

    double A1 = funcs[i]->GetParameter(4);
    double A2 = funcs[i]->GetParameter(5);

    double B1 = (-A1/s12 - A2/s22 + (A1+A2)/s32) / (1/s32 - 1/s12);
    double B2 =  A1 + A2 - B1;

    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s3 = " << s3 << endl;
    cout << "A1 = " << A1 << endl;
    cout << "A2 = " << A2 << endl;
    cout << "B1 = " << B1 << endl;
    cout << "B2 = " << B2 << endl;


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

//   double resolution_x[nfiles] = { 1000, 1250, 1500, 2000, 2500, 3000};
//   double resolution_dx[nfiles]= {    0,    0,    0,    0,    0,    0};
//   double resolution_y[nfiles] = {};
//   double resolution_dy[nfiles] = {};
//   TCanvas * c1 = new TCanvas("c1", "c1");
//   TH1D * foraxes = new TH1D("foraxes", "Resonance Resolutions in 100 pb^{-1};Dijet Mass (GeV/c^{2});Number", 5000, 0, 5000);
//   foraxes->SetMinimum(1e-6);
//   foraxes->SetMaximum(1.0);
//   foraxes->Draw();
//   foraxes->GetYaxis()->SetTitleOffset(1.0);
//   for ( int i = 0; i < nfiles; ++i ) {
//     funcs[i]->Draw("same");
//     resolution_y[i] = funcs[i]->GetParameter(1);
//     resolution_dy[i] = funcs[i]->GetParError(1);
//   }
//   leg->Draw();
//   c1->SetLogy();

//   TCanvas * c2 = new TCanvas("c2", "c2");
//   TGraphErrors * resolution = new TGraphErrors(nfiles, 
// 					       resolution_x, resolution_y,
// 					       resolution_dx, resolution_dy );
			
//   TH1D * foraxes2 = new TH1D("foraxes2", "Dijet Resolution Expectation;Dijet Mass (GeV/c^{2});Resolution (GeV)", 5000,0, 5000);
//   foraxes2->Draw();
//   foraxes2->SetMaximum(200);
//   foraxes2->GetYaxis()->SetTitleOffset(1.0);
//   resolution->Draw("LP");

//   hs->Draw("nostack");
//   leg->Draw();
//   hs->GetYaxis()->SetTitleOffset(1.0);
//   gPad->Print("signal_dijetmass_100pb_linear.gif", "gif");
//   gPad->Print("signal_dijetmass_100pb_linear.eps", "eps");
//   gPad->SetLogy();
//   gPad->Print("signal_dijetmass_100pb_log.gif", "gif");
//   gPad->Print("signal_dijetmass_100pb_log.eps", "eps");
}
