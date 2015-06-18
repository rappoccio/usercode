/* -------------------------------------------------------------------------------------------------------------------------
  Script for making the following plots:
  pt_rel distribution, toptagging efficiency vs. top jet pt/eta for ttbar MC
  -------------------------------------------------------------------------------------------------------------------------
*/
//  -------------------------------------------------------------------------------------
//  load options & set plot style
//  -------------------------------------------------------------------------------------
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
#include "THStack.h"
#include "TH2.h"
#include "TF1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TMath.h"

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include <cmath>

using namespace std;

const double LUM = 19.7;

// Signal ttbar norms: color: kRed +1
const int nMass = 3;
const int nttbar = 3;
const int nq2 = 3;
TString ttbar_names[nMass] = {
    "TT_max700_CT10",
    "TT_Mtt-700to1000_CT10",
    "TT_Mtt-1000toInf_CT10"
};

double ttbar_xs[nttbar] = {
    245.8 * 1000. * LUM,  // nominal
    252.0 * 1000. * LUM,  // q2 up
    237.4 * 1000. * LUM   // q2 down
};
double ttbar_nevents[nq2][nttbar] = {
    {21675970.,3082812.,1249111.},  // nominal
    {14983686.,2243672.,1241650.},  // q2 up
    {14545715*89./102.,2170074.,1308090.}   // q2 down
};
double ttbar_eff[nq2][nttbar] = {
    {1.0, 0.074, 0.015},  // nominal
    {1.0, 0.074, 0.014},  // q2 up
    {1.0, 0.081, 0.016}   // q2 down
};

unsigned int iq2 = 0;
  //if ( pdfdir.Contains("scaleup") ) iq2 = 1;
  //if ( pdfdir.Contains("scaledown") )iq2 = 2;

double ttbar_norms[nttbar] = {    
    ttbar_xs[iq2] * ttbar_eff[iq2][0] / ttbar_nevents[iq2][0],
    ttbar_xs[iq2] * ttbar_eff[iq2][1] / ttbar_nevents[iq2][1],
    ttbar_xs[iq2] * ttbar_eff[iq2][2] / ttbar_nevents[iq2][2],
};

void ptRel() {
	bool doElectron=true;

	TString muOrEl = "mu";
	if (doElectron) muOrEl = "el";

	TString DIR = "2Dhists";
	if (doElectron) DIR = "2Dhists_el";

	TFile* fttbar_nom[nMass];
	TFile* fttbar_qcd[nMass];
	TH2F* check1;

	// get the histfiles
	cout << "Getting the histfiles"<<endl;
	for (int iMass=0; iMass<nMass; iMass++) {
		fttbar_nom[iMass] = new TFile("histfiles_CT10_nom/"+ DIR +"/"+ttbar_names[iMass]+"_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+ muOrEl +"_CT10_nom_2Dcut_nom.root","READ");
		fttbar_qcd[iMass] = new TFile("histfiles_CT10_nom/"+ DIR +"/"+ttbar_names[iMass]+"_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+ muOrEl +"_CT10_nom_2Dcut_qcd.root","READ");
	}
	cout<<"checking"<<endl;
	check1 = (TH2F*) fttbar_qcd[2]->Get("dRvspT4")->Clone();
	cout<<"DEBUG: after reading the file array dRvspT4 for TT_Mtt-1000toInf_CT10 = "<< check1->GetSum()<<endl;

	// get the dRvspT4 distribution
	cout<<"Getting the dRvspT4 distribution"<<endl;
	vector<TH2F*> dRvspT4_nom; vector<TH2F*> dRvspT4_qcd;
	for (int iMass=0; iMass<nMass; iMass++) {
		dRvspT4_nom.push_back( (TH2F*) fttbar_nom[iMass]->Get("dRvspT4")->Clone() );
		dRvspT4_qcd.push_back( (TH2F*) fttbar_qcd[iMass]->Get("dRvspT4")->Clone() );
	}


	for (int iMass=0; iMass<nMass; iMass++) {
		dRvspT4_nom[iMass]->Sumw2();
		dRvspT4_qcd[iMass]->Sumw2();
	}

	// add nom and qcd
	vector<TH2F*> dRvspT4;
	for (int iMass=0; iMass<nMass; iMass++) {
		dRvspT4.push_back( (TH2F*) dRvspT4_nom[iMass]->Clone() );
		dRvspT4[iMass]->Add( (TH2F*)dRvspT4_qcd[iMass], 1);

	}

	// normalize
	cout<<"Normalizing the hists"<<endl;
	for (int iMass=0; iMass<nMass; iMass++) {
		dRvspT4[iMass]->Scale(ttbar_norms[iMass]);
	}

	
	// do the stitching
	cout<<"stitching mass ranges"<<endl;
	TH2F* h_dRvspT4; 
	h_dRvspT4 = (TH2F*)dRvspT4[0]->Clone();
	for (int iMass=1; iMass<nMass; iMass++){
		h_dRvspT4->Add( (TH2F*)dRvspT4[iMass], 1);
	}

	
	// Project the 2-D histogram into a 1-D histogram along Y
	TH1D* h_ptRel = h_dRvspT4->ProjectionY();
	h_ptRel->Rebin(2.5);

	// plot
	cout<<"plotting ptRel"<<endl;
	TCanvas* c1 = new TCanvas("c" , "" , 800, 600);
	c1->cd();
	gStyle->SetOptStat(0);

	h_ptRel-> Draw("");
	h_ptRel->SetLabelOffset(0.005);
	h_ptRel->GetYaxis()->SetTitleOffset(1.4);
	h_ptRel->GetYaxis()->SetLabelSize(0.035);
	h_ptRel->GetYaxis()->SetTitleSize(0.035);
	h_ptRel->GetXaxis()->SetLabelSize(0.035);
	h_ptRel->GetXaxis()->SetTitleSize(0.035);
	h_ptRel->GetYaxis()->SetRangeUser(0,200);
	h_ptRel->SetLineColor(1);
	h_ptRel->SetLineWidth(2.0);
	h_ptRel->SetMarkerColor(1);
	h_ptRel->SetMarkerStyle(24);

	c1->Draw();
	c1->SaveAs("ptRel_"+ muOrEl +".png", "png");

}


void toptagging_e() {

	bool doElectron=true;

	TString muOrEl = "mu";
	if (doElectron) muOrEl = "el";

	TString DIR = "2Dhists";
	if (doElectron) DIR = "2Dhists_el";

	TFile* fttbar[nMass];
	TH1F* check0;

	// get the histfiles
	cout << "Getting the histfiles"<<endl;
	for (int iMass=0; iMass<nMass; iMass++) {
		fttbar[iMass] = new TFile("histfiles_CT10_nom/"+ DIR +"/"+ttbar_names[iMass]+"_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+ muOrEl +"_CT10_nom_2Dcut_nom.root","READ");
	}
	check0 = (TH1F*) fttbar[2]->Get("hadtop_pt4")->Clone();
	cout<<"DEBUG: after reading the file array hadtop_pt4 for TT_Mtt-1000toInf_CT10 = "<< check0->GetSum()<<endl;

	// get the hadtop_pt4, hadtop_pt6, hadtop_eta4, hadtop_eta6 distribution for ttbar MC
	vector<TH1F*> hadtopPt4; vector<TH1F*> hadtopPt6; vector<TH1F*> hadtopEta4; vector<TH1F*> hadtopEta6;
	for (int iMass=0; iMass<nMass; iMass++) {
		hadtopPt4.push_back( (TH1F*) fttbar[iMass]->Get("hadtop_pt4")->Clone() );
		hadtopPt6.push_back( (TH1F*) fttbar[iMass]->Get("hadtop_pt6")->Clone() );
		hadtopEta4.push_back( (TH1F*) fttbar[iMass]->Get("hadtop_eta4")->Clone() );
		hadtopEta6.push_back( (TH1F*) fttbar[iMass]->Get("hadtop_eta6")->Clone() );
	}

	for (int iMass=0; iMass<nMass; iMass++) {
		hadtopPt4[iMass]->Sumw2();
		hadtopPt6[iMass]->Sumw2();
		hadtopEta4[iMass]->Sumw2();
		hadtopEta6[iMass]->Sumw2();
	}
	
	// normalize
	cout<<"Normalizing the hists"<<endl;
	for (int iMass=0; iMass<nMass; iMass++) {
		hadtopPt4[iMass]->Scale(ttbar_norms[iMass]);
		hadtopPt6[iMass]->Scale(ttbar_norms[iMass]);
		hadtopEta4[iMass]->Scale(ttbar_norms[iMass]);
		hadtopEta6[iMass]->Scale(ttbar_norms[iMass]);
	}	


	// do the stitching
	cout<<"stitching mass ranges"<<endl;
	TH1F* h_hadtopPt4; TH1F* h_hadtopPt6; TH1F* h_hadtopEta4; TH1F* h_hadtopEta6;
	h_hadtopPt4 = (TH1F*)hadtopPt4[0]->Clone();
	h_hadtopPt6 = (TH1F*)hadtopPt6[0]->Clone();
	h_hadtopEta4 = (TH1F*)hadtopEta4[0]->Clone();
	h_hadtopEta6 = (TH1F*)hadtopEta6[0]->Clone();
	for (int iMass=1; iMass<nMass; iMass++){
		h_hadtopPt4->Add( (TH1F*)hadtopPt4[iMass], 1);
		h_hadtopPt6->Add( (TH1F*)hadtopPt6[iMass], 1);
		h_hadtopEta4->Add( (TH1F*)hadtopEta4[iMass], 1);
		h_hadtopEta6->Add( (TH1F*)hadtopEta6[iMass], 1);
	}

	// rebin
	double ptbins[9] = {400,450,500,550,600,700,800,1000,1200};
	TH1F* h_num_new = (TH1F*) h_hadtopPt6->Rebin(8,"num_new",ptbins);
	TH1F* h_den_new = (TH1F*) h_hadtopPt4->Rebin(8,"den_new",ptbins);

	h_hadtopEta6->Rebin(5);
	h_hadtopEta4->Rebin(5);
	

	// divide and get the errors accounted for properly (eff = hadtop_pt6/hadtop_pt4)
	TH1F* h_eff_pt;
	h_eff_pt = (TH1F*)h_num_new->Clone();
	h_eff_pt->Divide( (TH1F*)h_num_new, (TH1F*)h_den_new, 1.0, 1.0, "B");

	// divide and get the errors accounted for properly (eff = hadtop_eta6/hadtop_eta4)
	TH1F* h_eff_eta;
	h_eff_eta = (TH1F*)h_hadtopEta6->Clone();
	h_eff_eta->Divide( (TH1F*)h_hadtopEta6, (TH1F*)h_hadtopEta4, 1.0, 1.0, "B");

	// plot
	cout<<"plotting top-tagging efficiency pt for "+ muOrEl +" channel"<<endl;
	TCanvas* c2 = new TCanvas("c" , "" , 800, 600);
	c2->cd();
	gStyle->SetOptStat(0);

	h_eff_pt-> Draw("");
	h_eff_pt->SetLabelOffset(0.005);
	h_eff_pt->GetYaxis()->SetTitleOffset(1.4);
	h_eff_pt->GetYaxis()->SetLabelSize(0.035);
	h_eff_pt->GetYaxis()->SetTitleSize(0.035);
	h_eff_pt->GetXaxis()->SetLabelSize(0.034);
	h_eff_pt->GetXaxis()->SetTitleSize(0.035);
	h_eff_pt->GetXaxis()->SetRangeUser(400,1200);
	h_eff_pt->GetYaxis()->SetRangeUser(0,0.4);
	h_eff_pt->GetYaxis()->SetTitle("top-tagging efficiency "+ muOrEl +" channel");
	h_eff_pt->SetLineColor(1);
	h_eff_pt->SetLineWidth(2.0);
	h_eff_pt->SetMarkerColor(1);
	h_eff_pt->SetMarkerStyle(24);

	c2->Draw();
	c2->SaveAs("toptagging_efficiency_pt_"+ muOrEl +".png", "png");

	cout<<"plotting top-tagging efficiency eta for "+ muOrEl +" channel"<<endl;
	TCanvas* c3 = new TCanvas("c" , "" , 800, 600);
	c3->cd();
	gStyle->SetOptStat(0);

	h_eff_eta-> Draw("");
	h_eff_eta->SetLabelOffset(0.005);
	h_eff_eta->GetYaxis()->SetTitleOffset(1.4);
	h_eff_eta->GetYaxis()->SetLabelSize(0.035);
	h_eff_eta->GetYaxis()->SetTitleSize(0.035);
	h_eff_eta->GetXaxis()->SetLabelSize(0.034);
	h_eff_eta->GetXaxis()->SetTitleSize(0.035);
	h_eff_eta->GetYaxis()->SetRangeUser(0,0.4);
	h_eff_eta->GetYaxis()->SetTitle("top-tagging efficiency "+ muOrEl +" channel");
	h_eff_eta->SetLineColor(1);
	h_eff_eta->SetLineWidth(2.0);
	h_eff_eta->SetMarkerColor(1);
	h_eff_eta->SetMarkerStyle(24);

	c3->Draw();
	c3->SaveAs("toptagging_efficiency_eta_"+ muOrEl +".png", "png");

}



















