#include "TROOT.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TBranch.h"
#include "TLeaf.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TMath.h"

#include <iostream>
#include <string>
#include <vector>

using namespace std;

void SetPlotStyle();
void mySmallText(Double_t x,Double_t y,Color_t color,Double_t tsize,char *text); 


void btagEff() {
  
  SetPlotStyle();
  
  //gStyle->SetPadLeftMargin(0.12);
  //gStyle->SetPadRightMargin(0.14);


  // files
  TFile* f_max700    = new TFile("btag_max700.root");
  TFile* f_700to1000 = new TFile("btag_700to1000.root");
  TFile* f_1000toInf = new TFile("btag_1000toInf.root");

  TString eta[3] = {"C","M","H"};
  TString flavor[3] = {"b","c","l"};
  TString cut[3] = {"","2","3"};

  TH1F* h_num;
  TH1F* h_den;
  TH1F* h_num_700to1000;
  TH1F* h_den_700to1000;
  TH1F* h_num_1000toInf;
  TH1F* h_den_1000toInf;

  for (int ic=0; ic<3; ic++) {
    for (int ifl=0; ifl<3; ifl++) {
      
      TH1F* h_eff[3];

      for (int ie=0; ie<3; ie++) {
	
	//histograms
	h_num = (TH1F*) f_max700->Get("btageff"+cut[ic]+"_"+eta[ie]+"_num_"+flavor[ifl]);
	h_den = (TH1F*) f_max700->Get("btageff"+cut[ic]+"_"+eta[ie]+"_den_"+flavor[ifl]);
	h_num_700to1000 = (TH1F*) f_700to1000->Get("btageff"+cut[ic]+"_"+eta[ie]+"_num_"+flavor[ifl]);
	h_den_700to1000 = (TH1F*) f_700to1000->Get("btageff"+cut[ic]+"_"+eta[ie]+"_den_"+flavor[ifl]);
	h_num_1000toInf = (TH1F*) f_1000toInf->Get("btageff"+cut[ic]+"_"+eta[ie]+"_num_"+flavor[ifl]);
	h_den_1000toInf = (TH1F*) f_1000toInf->Get("btageff"+cut[ic]+"_"+eta[ie]+"_den_"+flavor[ifl]);

	//scale
	h_num->Scale(245.8*1000.*19.7/21675970.); 
	h_den->Scale(245.8*1000.*19.7/21675970.); 
	h_num_700to1000->Scale(245.8*1000.*0.074*19.7/3082812.); 
	h_den_700to1000->Scale(245.8*1000.*0.074*19.7/3082812.); 
	h_num_1000toInf->Scale(245.8*1000.*0.015*19.7/1249111.); 
	h_den_1000toInf->Scale(245.8*1000.*0.015*19.7/1249111.); 

	h_num->Sumw2();  
	h_den->Sumw2();  
	h_num_700to1000->Sumw2();  
	h_den_700to1000->Sumw2();  
	h_num_1000toInf->Sumw2();  
	h_den_1000toInf->Sumw2();  

	h_num->Add(h_num_700to1000);  
	h_num->Add(h_num_1000toInf);  

	h_den->Add(h_den_700to1000);  
	h_den->Add(h_den_1000toInf);  

	//ptbins = array('d',[30, 40, 50, 60, 70, 80, 100, 120, 160, 220, 300, 400, 600, 800])
	double ptbins[9] = {30, 50, 70, 100, 160, 220, 300, 400, 800};
	TH1F* h_num_new = (TH1F*) h_num->Rebin(8,"num_new",ptbins);
	TH1F* h_den_new = (TH1F*) h_den->Rebin(8,"den_new",ptbins);

	h_eff[ie] = (TH1F*) h_num_new->Clone("efficiency_"+eta[ie]);
	h_eff[ie]->Reset();
	h_eff[ie]->Divide(h_num_new, h_den_new, 1.0, 1.0, "B");

      }//end eta region
      
      TCanvas c;
      h_eff[1]->SetMarkerStyle(22);
      h_eff[1]->SetMarkerColor(2);
      h_eff[1]->SetLineColor(2);
      h_eff[2]->SetMarkerStyle(24);
      h_eff[2]->SetMarkerColor(4);
      h_eff[2]->SetLineColor(4);

      if (ifl==0) h_eff[0]->SetAxisRange(0,1.0,"Y");
      if (ifl==1) h_eff[0]->SetAxisRange(0,0.5,"Y");
      if (ifl==2) h_eff[0]->SetAxisRange(0,0.1,"Y");
      h_eff[0]->GetXaxis()->SetTitle("jet p_{T} [GeV]");
      h_eff[0]->GetYaxis()->SetTitle("Efficiency");

      h_eff[0]->Draw("ep");
      h_eff[1]->Draw("ep,same");
      h_eff[2]->Draw("ep,same");
      
      // legend
      TLegend* leg = new TLegend(0.67,0.7,0.9,0.9);
      leg->SetBorderSize(0);
      leg->SetFillStyle(0);
      leg->SetTextFont(42);
      leg->SetTextSize(0.042);
      leg->AddEntry(h_eff[0], "|#eta| < 0.8", "pel");
      leg->AddEntry(h_eff[1], "0.8 < |#eta| < 1.6", "pel");
      leg->AddEntry(h_eff[2], "1.6 < |#eta| < 2.4", "pel");
      leg->Draw();

      c.SaveAs("eff"+cut[ic]+"_"+flavor[ifl]+".png");
      c.SaveAs("eff"+cut[ic]+"_"+flavor[ifl]+".eps");

      if (ic==2) {

	cout << "****** "<< flavor[ifl] << "-jet efficiency ******" << endl;
	cout << "eff_" << flavor[ifl] << "_C = [";
	for (int ib=0; ib<h_eff[0]->GetNbinsX(); ib++) {
	  cout << h_eff[0]->GetBinContent(ib+1) << ", ";
	}
	cout << "]" << endl;
	cout << "eff_" << flavor[ifl] << "_M = [";
	for (int ib=0; ib<h_eff[1]->GetNbinsX(); ib++) {
	  cout << h_eff[1]->GetBinContent(ib+1) << ", ";
	}
	cout << "]" << endl;
	cout << "eff_" << flavor[ifl] << "_H = [";
	for (int ib=0; ib<h_eff[2]->GetNbinsX(); ib++) {
	  cout << h_eff[2]->GetBinContent(ib+1) << ", ";
	}
	cout << "]" << endl;

      }


    }//end flavor
  }//end cut option


}


void SetPlotStyle() {
  
  // from ATLAS plot style macro
  
  // use plain black on white colors
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameFillColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetStatColor(0);
  gStyle->SetHistLineColor(1);
  
  gStyle->SetPalette(1);
  
  // set the paper & margin sizes
  gStyle->SetPaperSize(20,26);
  /*
    gStyle->SetPadTopMargin(0.05);
    gStyle->SetPadRightMargin(0.05);
    gStyle->SetPadBottomMargin(0.16);
    gStyle->SetPadLeftMargin(0.16);
  */
  gStyle->SetPadTopMargin(0.07);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.18);
  
  // set title offsets (for axis label)
  gStyle->SetTitleXOffset(1.4);
  gStyle->SetTitleYOffset(1.2);
  
  // use large fonts
  gStyle->SetTextFont(42);
  gStyle->SetTextSize(0.05);
  gStyle->SetLabelFont(42,"x");
  gStyle->SetTitleFont(42,"x");
  gStyle->SetLabelFont(42,"y");
  gStyle->SetTitleFont(42,"y");
  gStyle->SetLabelFont(42,"z");
  gStyle->SetTitleFont(42,"z");
  gStyle->SetLabelSize(0.05,"x");
  gStyle->SetTitleSize(0.05,"x");
  gStyle->SetLabelSize(0.05,"y");
  gStyle->SetTitleSize(0.05,"y");
  gStyle->SetLabelSize(0.05,"z");
  gStyle->SetTitleSize(0.05,"z");
  
  // use bold lines and markers
  gStyle->SetMarkerStyle(20);
  gStyle->SetMarkerSize(1.2);
  gStyle->SetHistLineWidth(2.);
  gStyle->SetLineStyleString(2,"[12 12]");
  
  // get rid of error bar caps
  gStyle->SetEndErrorSize(0.);
  
  // do not display any of the standard histogram decorations
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);
  
  // put tick marks on top and RHS of plots
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  
}


void mySmallText(Double_t x,Double_t y,Color_t color,Double_t tsize, char *text) {
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
