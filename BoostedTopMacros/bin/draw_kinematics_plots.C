#include "TFile.h"
#include "TH1.h"
#include "THStack.h"
#include "TLegend.h"

void draw_kinematics_plots()
{

  const char * filenames[] = {
//     "kinematic_histos_rs_750.root",
//     "kinematic_histos_rs_1000.root",
//     "kinematic_histos_rs_1250.root",
    "kinematic_histos_rs_750_fastsim.root",
    "kinematic_histos_rs_1000_fastsim.root",
    "kinematic_histos_rs_1250_fastsim.root",
    "kinematic_histos_rs_1500_fastsim.root",
    "kinematic_histos_rs_2000_fastsim.root",
    "kinematic_histos_rs_2500_fastsim.root",
    "kinematic_histos_rs_3000_fastsim.root",

  };

  const char * desc[] = {
//     "RS M = 750 GeV/c^{2}",
//     "RS M = 1000 GeV/c^{2}",
//     "RS M = 1250 GeV/c^{2}",
    "RS M = 750  GeV, FastSim",
    "RS M = 1000 GeV, FastSim",
    "RS M = 1250 GeV, FastSim",
    "RS M = 1500 GeV, FastSim",
    "RS M = 2000 GeV, FastSim",
    "RS M = 2500 GeV, FastSim",
    "RS M = 3000 GeV, FastSim",
  };

  int colors[] = {
    kRed,
    kGreen + 2,
    kBlue + 2,
    kMagenta,
    kCyan,
    kViolet,
    kAzure
  };

  static const int NFILES = sizeof( filenames ) / sizeof(const char *);


  const char * histnames[] = {
    "hist_top_jetEt",
    "hist_top_jetEta",
    "hist_top_jetMass",
    "hist_top_jetMinMass",
    "hist_top_dijetmass"
  };

  const char * hs_names[] = {
    "hs_jetEt",
    "hs_jetEta",
    "hs_jetMass",
    "hs_jetMinMass",
    "hs_dijetmass"
  };

  const char * hs_titles[] = {
    "Jet E_{T}",
    "Jet #eta",
    "Jet Mass",
    "Jet Min Mass",
    "Dijet Mass"
  };


  static const int NHISTS = sizeof( histnames ) / sizeof( const char *);


  TCanvas * canv[NHISTS];

  TFile * files[NFILES];


  THStack * stacks[NHISTS];

  for ( int j = 0; j < NHISTS; ++j ) {
    TString cname (hs_names[j] );
    cname += "_canv";
    canv[j] = new TCanvas( cname.Data(), cname.Data() );
    stacks[j] = new THStack( hs_names[j], hs_titles[j] );
  }

  TLegend * leg = new TLegend(0.8, 0.8, 1.0, 1.0);
  leg->SetLineColor(0);
  leg->SetFillColor(0);


  for ( int i = 0; i < NFILES; ++i ) {

    files[i] = new TFile(filenames[i]);

    for ( int j = 0; j < NHISTS; ++j ) {
      TH1D * h = (TH1D*)files[i]->Get(histnames[j]);
      h->Sumw2();
      h->Scale( 1.0 / h->GetEntries() );
      h->SetLineColor(colors[i]);
      if ( j == 0 ) leg->AddEntry(h,desc[i], "l");
      stacks[j]->Add( h );
    }
  }

  
  for ( int j = 0; j < NHISTS; ++j ) {
    canv[j]->cd();
    stacks[j]->Draw("nostack hist");
    leg->Draw();
    TString gifname(hs_names[j]);
    gifname += ".gif";
    TString epsname(hs_names[j]);
    epsname += ".eps";

    canv[j]->Print( gifname.Data(), "gif");
    canv[j]->Print( epsname.Data(), "eps");
  }


}
