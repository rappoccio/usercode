#include "TH1.h"
#include "TFile.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TStyle.h"

void dijet_analysis()
{

  // -------
  // Do the actual analysis for the dijet bump search for 100 pb-1
  // -------

  // Background is generic QCD dijets derived from the
  // mistag parameterization.
  // These are input from the function "combine_mistag_predictions_scalelum.C".
  // This function produces the file "xcheck_summary_scalelum.root". 
  //
  // In this file, the following plots are made:
  //   KEY: TH1D	total;1	Total Rate
  //   KEY: TH1D	total_pred;1	Total Rate
  //   KEY: TH1D	jet_et;1	Predicted Jet E_{T}
  //   KEY: TH1D	jet_et_pred;1	Predicted Jet E_{T}
  //   KEY: TH1D	jet_eta;1	Predicted Jet #eta
  //   KEY: TH1D	jet_eta_pred;1	Predicted Jet #eta
  //   KEY: TH1D	jet_phi;1	Predicted Jet #phi
  //   KEY: TH1D	jet_phi_pred;1	Predicted Jet #phi
  //   KEY: TH1D	dijetmass;1	Predicted Dijet Mass
  //   KEY: TH1D	dijetmass_pred;1	Predicted Dijet Mass
  // These are scaled to 100 pb-1 and constitute the observed and predicted
  // rates expected from QCD. These correspond to 1/2 of the contribution
  // to be used, since they are derived from only 1/2 of the total sample.

  double LUM[] = {10, 100, 1000};

  // Now get the background estimate:
  TFile * xcheck_summary_scalelum = new TFile("xcheck_summary_scalelum.root");
  TH1D * dijetmass_pred_lum100 = (TH1D*)(xcheck_summary_scalelum->Get("dijetmass_pred")->Clone());
  dijetmass_pred_lum100->SetName("lum100");

  // 

  // Scale by 2 to account for the fact that only 1/2 of the events are used
  // in this prediction, and scale to the Luminosity.
  dijetmass_pred_lum100->Scale(2.0 * LUM[1]);
  // Prettify
  dijetmass_pred_lum100->SetTitle("Dijet Mass Expectation from QCD Dijets;Dijet mass (GeV/c^{2});Number/100 GeV/c^{2}");
  dijetmass_pred_lum100->SetMarkerColor(2);
  dijetmass_pred_lum100->SetLineColor(2);

  // Draw prediction
  TCanvas * pred = new TCanvas("pred", "pred");
  dijetmass_pred_lum100->Draw("e");
  dijetmass_pred_lum100->GetYaxis()->SetTitleOffset(1.1);
  pred->Print("dijetmass_pred_100invpb.gif", "gif");
  pred->Print("dijetmass_pred_100invpb.eps", "eps");

  // Now make estimate of discovery reach
  TH1D * discovery_reach_lum100 = new TH1D(*dijetmass_pred_lum100);
  discovery_reach_lum100->SetLineColor(4);
  discovery_reach_lum100->SetFillColor(0);
  discovery_reach_lum100->SetTitle("5 #sigma Discovery Reach for 100 pb^{-1};Dijet mass (GeV/c^{2});Cross Section #times BR #times Eff (pb)");

  // Discovery reach is given by
  // X = S / sqrt(B + dB^2)
  // If X = 5 sigma, have
  // 5 = xs * BR * LUM / sqrt(B+dB^2)
  // So discovery reach for xs*BR is
  // R = 5 * sqrt(B+dB^2) / LUM
  for ( int i = 0; i <= discovery_reach_lum100->GetNbinsX(); ++i ) {
    double B = discovery_reach_lum100->GetBinContent(i);
    double dB = discovery_reach_lum100->GetBinError(i);
    double Y =  TMath::Sqrt(B + dB*dB );
    double VAL = 5. * Y / LUM[1];
    discovery_reach_lum100->SetBinContent( i, VAL );
    discovery_reach_lum100->SetBinError( i, 0. );
  }

  // Draw discovery reach
  gStyle->SetOptStat(000000);
  TCanvas * reach = new TCanvas("reach", "reach");
  discovery_reach_lum100->Draw("C");
  discovery_reach_lum100->SetMinimum(1e-02);
  discovery_reach_lum100->SetMaximum(1.0);
//   discovery_reach_lum100->GetXaxis()->SetRangeUser(1000, 5000);
  reach->SetLogy();
  reach->Print("reach.gif", "gif");
  reach->Print("reach.eps", "eps");
}
