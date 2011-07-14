{
#include <math.h>
#include <TMath.h>
#include <TMatrixT.h>
#include <TMatrixD.h>
#include <TVectorT.h>
#include <TVectorD.h>
#include <TLatex.h>
#include <iostream>
#include <TTree.h>
#include <TH1D.h>
#include <TH2F.h>
#include <sstream>
#include <TFile.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TVirtualPad.h>
#include <TPostScript.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TColor.h>
#include <iomanip>
#include <iostream>
#include <vector>
#include <algorithm> // sort, max_element, random_shuffle, keep_if, lower_bound 
#include <functional> // greater, bind2nd
	
using namespace std;

//////////////////////////////////////////////////////////////////////////////////////////
	gROOT->SetStyle("Plain");
	//-----------------------------------------
	//    Canvas
	//-----------------------------------------
	//gStyle->SetCanvasBorderMode(0);
	//gStyle->SetCanvasColor(10);
	//-----------------------------------------
	//   StatsBox
	//-----------------------------------------
	gStyle->SetOptStat(0);
	//gStyle->SetOptStat("eou");
	//gStyle->SetOptStat(111111);
	//gStyle->SetStatColor(10);
	//gStyle->SetStatBorderSize(5);
	//gStyle->SetStatFontSize(0.08);
	//-----------------------------------------
	//    Histogram Attributes
	//-----------------------------------------
	gStyle->SetHistLineWidth(2);
	//gStyle->SetPalette(52,0); 
	gStyle->SetHatchesSpacing(0.5);
	gStyle->SetHatchesLineWidth(1.7);
	//-----------------------------------------
	//    Pad .  Use Canvas->SetLeftMargin(0.08) to do individually 
	//-----------------------------------------
	gStyle->SetPadTopMargin(0.05);
	gStyle->SetPadBottomMargin(0.13);
	gStyle->SetPadLeftMargin(0.16);
	gStyle->SetPadRightMargin(0.04); 
	//gStyle->SetPadBorderMode(0);
	//-----------------------------------------
	//    Title, axis labels, and axis numbers
	//-----------------------------------------
	//gStyle->SetTitleColor();
	gStyle->SetTitleBorderSize(0);
	gStyle->SetTitleXOffset(1.2);
	gStyle->SetTitleYOffset(1.7);  //gStyle->SetTitleOffset(2.9,"Y"); also works
	//gStyle->SetTitleXSize(0.05);
	//gStyle->SetTitleYSize(0.05);
	//gStyle->SetTitleSize(30);
	gStyle->SetTitleX(0.02); 
	gStyle->SetTitleY(0.99);
	gStyle->SetTitleW(0.5);
	//gStyle->SetTitleFontSize(0.06);	// Change size of histogram title
	//gStyle->SetTitleSize(0.05,"XY");	// Change the size of the axis labels    
	//gStyle->SetTitleOffset(10,"Y");
	//gStyle->SetTitleOffset(2,"X");
	//gStyle->SetLabelSize(0.08,"XY");	// Change size of axis numbers
	gStyle->SetLabelOffset(0.012,"X");
	gStyle->SetPadTickX(1);  
	gStyle->SetPadTickY(1);
	gStyle->SetTickLength(0.03, "XYZ");
	//-----------------------------------------
	//--- Force Style
	//-----------------------------------------
	gROOT->UseCurrentStyle();
	gROOT->ForceStyle();// forces the style chosen above to be used, not the style the rootfile was made with
	gROOT->Reset();
    /////////////////////////////////////////////////////////////////////////////////////////
	TCanvas *c1000 = new TCanvas("c1000","",10,10,700,550);

	TFile *ROOT 			= new TFile("TTHadronicAnalyzerCombined_Jet_PD_May10ReReco_PromptReco_range1_range2_v4_New_mistag1.root");
	TFile *ROOT_TTBAR 		= new TFile("TTHadronicAnalyzerCombined_TTJets_TuneZ2_mistag1.root");

    TH1D * topTagPt			=  ROOT	-> Get("topTagPt");
	TH1D * topProbePt		=  ROOT -> Get("topProbePt");
	TH1D * massCutTagPt		=  ROOT -> Get("testTagPt");
	TH1D * massCutProbePt	=  ROOT -> Get("testProbePt");	

	TH1D * topTagPtTTBAR		=  ROOT_TTBAR -> Get("topTagPt");
	TH1D * topProbePtTTBAR		=  ROOT_TTBAR -> Get("topProbePt");
	TH1D * massCutTagPtTTBAR	=  ROOT_TTBAR -> Get("testTagPt");
	TH1D * massCutProbePtTTBAR	=  ROOT_TTBAR -> Get("testProbePt");	
	
	double luminosity = 888.4;  
	double DataSetNevents_TT_TuneZ2  = 3701947;
	double sigma_TT_TuneZ2   =  157;//  94;
	double scale_TT_TuneZ2 = sigma_TT_TuneZ2 * luminosity / DataSetNevents_TT_TuneZ2;
    double PatTupleNevents_TT_TuneZ2 = 3683795;
    double tagging_eff_scale_factor = 0.93; 			//  based on W tagging but also used for top tagging (0.92 +- 0.06) * (1.01 +- 0.11) = 0.93 +- 0.12

	topTagPtTTBAR	    ->Sumw2();
	topTagPtTTBAR	    ->Scale(scale_TT_TuneZ2);
	topTagPtTTBAR	    ->Scale(tagging_eff_scale_factor);
	topProbePtTTBAR	    ->Sumw2();
	topProbePtTTBAR	    ->Scale(scale_TT_TuneZ2);
	topProbePtTTBAR	    ->Scale(tagging_eff_scale_factor);
	massCutTagPtTTBAR	->Sumw2();
	massCutTagPtTTBAR	->Scale(scale_TT_TuneZ2);
	massCutTagPtTTBAR	->Scale(tagging_eff_scale_factor);
	massCutProbePtTTBAR	->Sumw2();
	massCutProbePtTTBAR	->Scale(scale_TT_TuneZ2);
	massCutProbePtTTBAR	->Scale(tagging_eff_scale_factor);
	
	TH1D *topTagPtSubtractTTBAR         = topTagPt->Clone();
	TH1D *topProbePtSubtractTTBAR       = topProbePt->Clone();
	TH1D *massCutTagPtSubtractTTBAR     = massCutTagPt->Clone();
	TH1D *massCutProbePtSubtractTTBAR   = massCutProbePt->Clone();
	
	topTagPtSubtractTTBAR       ->Add( topTagPtTTBAR,-1);
	topProbePtSubtractTTBAR     ->Add( topProbePtTTBAR,-1);
	massCutTagPtSubtractTTBAR   ->Add( massCutTagPtTTBAR,-1);
	massCutProbePtSubtractTTBAR ->Add( massCutProbePtTTBAR,-1);
	//topTagPtSubtractTTBAR       ->Add( topTagPtSubtractTTBAR,       topTagPtTTBAR,1,-1);
	//topProbePtSubtractTTBAR     ->Add( topProbePtSubtractTTBAR,     topProbePtTTBAR,1,-1);
	//massCutTagPtSubtractTTBAR   ->Add( massCutTagPtSubtractTTBAR,   massCutTagPtTTBAR,1,-1);
	//massCutProbePtSubtractTTBAR ->Add( massCutProbePtSubtractTTBAR, massCutProbePtTTBAR,1,-1);
	
	
	
	// Rebin with small bins
 	Int_t num_bins=26;
    Double_t bins[num_bins+1]= {350,355,360,365,370,375,380,385,390,395,400,410,420,430,440,450,460,480,500,525,550,600,650,700,800,1000,1200}; 
	TH1D *topTagPt_rebin 		= topTagPt			->Rebin(num_bins,"topTagPt_rebin",bins); 
	TH1D *topProbePt_rebin 		= topProbePt		->Rebin(num_bins,"topProbePt_rebin",bins); 
	TH1D *massCutTagPt_rebin 	= massCutTagPt		->Rebin(num_bins,"massCutTagPt_rebin",bins); 
	TH1D *massCutProbePt_rebin 	= massCutProbePt	->Rebin(num_bins,"massCutProbePt_rebin",bins); 

	TH1D *topTagPtTTBAR_rebin 		= topTagPtTTBAR			->Rebin(num_bins,"topTagPtTTBAR_rebin",bins); 
	TH1D *topProbePtTTBAR_rebin 	= topProbePtTTBAR		->Rebin(num_bins,"topProbePtTTBAR_rebin",bins); 
	TH1D *massCutTagPtTTBAR_rebin 	= massCutTagPtTTBAR		->Rebin(num_bins,"massCutTagPtTTBAR_rebin",bins); 
	TH1D *massCutProbePtTTBAR_rebin = massCutProbePtTTBAR	->Rebin(num_bins,"massCutProbePtTTBAR_rebin",bins); 
	
	TH1D *topTagPtSubtractTTBAR_rebin 		= topTagPtSubtractTTBAR			->Rebin(num_bins,"topTagPtSubtractTTBAR_rebin",bins); 
	TH1D *topProbePtSubtractTTBAR_rebin 	= topProbePtSubtractTTBAR		->Rebin(num_bins,"topProbePtSubtractTTBAR_rebin",bins); 
	TH1D *massCutTagPtSubtractTTBAR_rebin 	= massCutTagPtSubtractTTBAR		->Rebin(num_bins,"massCutTagPtSubtractTTBAR_rebin",bins); 
	TH1D *massCutProbePtSubtractTTBAR_rebin = massCutProbePtSubtractTTBAR	->Rebin(num_bins,"massCutProbePtSubtractTTBAR_rebin",bins); 
	
	// Rebin with large bins
 	Int_t num_bins2=9;
    Double_t bins2[num_bins2+1]= {350,375,400,450,500,600,700,800,1000,1200}; 
	TH1D *topTagPt_rebin2 		= topTagPt			->Rebin(num_bins2,"topTagPt_rebin2",bins2); 
	TH1D *topProbePt_rebin2 	= topProbePt		->Rebin(num_bins2,"topProbePt_rebin2",bins2); 
	TH1D *massCutTagPt_rebin2 	= massCutTagPt		->Rebin(num_bins2,"massCutTagPt_rebin2",bins2); 
	TH1D *massCutProbePt_rebin2 = massCutProbePt	->Rebin(num_bins2,"massCutProbePt_rebin2",bins2); 
		
	TH1D *topTagPtTTBAR_rebin2 		 = topTagPtTTBAR		->Rebin(num_bins2,"topTagPtTTBAR_rebin2",bins2); 
	TH1D *topProbePtTTBAR_rebin2 	 = topProbePtTTBAR		->Rebin(num_bins2,"topProbePtTTBAR_rebin2",bins2); 
	TH1D *massCutTagPtTTBAR_rebin2 	 = massCutTagPtTTBAR	->Rebin(num_bins2,"massCutTagPtTTBAR_rebin2",bins2); 
	TH1D *massCutProbePtTTBAR_rebin2 = massCutProbePtTTBAR	->Rebin(num_bins2,"massCutProbePtTTBAR_rebin2",bins2); 
	
	TH1D *topTagPtSubtractTTBAR_rebin2 		 = topTagPtSubtractTTBAR		->Rebin(num_bins2,"topTagPtSubtractTTBAR_rebin2",bins2); 
	TH1D *topProbePtSubtractTTBAR_rebin2 	 = topProbePtSubtractTTBAR		->Rebin(num_bins2,"topProbePtSubtractTTBAR_rebin2",bins2); 
	TH1D *massCutTagPtSubtractTTBAR_rebin2 	 = massCutTagPtSubtractTTBAR	->Rebin(num_bins2,"massCutTagPtSubtractTTBAR_rebin2",bins2); 
	TH1D *massCutProbePtSubtractTTBAR_rebin2 = massCutProbePtSubtractTTBAR	->Rebin(num_bins2,"massCutProbePtSubtractTTBAR_rebin2",bins2); 
	
	
	//------------------------------------------------------------------------------------------------------------//
    // Data Mistag rate
    
    // small bin
	TH1D *MISTAG_RATE = topProbePt_rebin->Clone();
	MISTAG_RATE->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
	MISTAG_RATE->Sumw2();
	MISTAG_RATE->Divide(topTagPt_rebin,topProbePt_rebin,1.,1.,"B");
	MISTAG_RATE->SetMarkerStyle(21);
	MISTAG_RATE->SetMarkerColor(2);
	MISTAG_RATE->SetLineColor(2);
	MISTAG_RATE->Draw();
	MISTAG_RATE->SetName("TYPE11_MISTAG");
	c1000->SaveAs("mistag_plots/MISTAG_RATE.png");

	TH1D *MISTAG_RATE_MASSCUT = massCutProbePt_rebin->Clone();
	MISTAG_RATE_MASSCUT->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
	MISTAG_RATE_MASSCUT->Sumw2();
	MISTAG_RATE_MASSCUT->Divide(massCutTagPt_rebin,massCutProbePt_rebin,1.,1.,"B");
	MISTAG_RATE_MASSCUT->SetMarkerStyle(22);
	MISTAG_RATE_MASSCUT->SetMarkerColor(4);
	MISTAG_RATE_MASSCUT->SetLineColor(4);
	MISTAG_RATE_MASSCUT->Draw("");
	MISTAG_RATE_MASSCUT->SetName("TYPE11_MISTAG_MASSCUT");
	c1000->SaveAs("mistag_plots/MISTAG_RATE_MASSCUT.png");
	
	MISTAG_RATE_MASSCUT->Draw("");
	MISTAG_RATE->Draw("same");

    double legXmin=0.3;
    double legYmin=0.18;
    double legXmax=0.8;//0.58
    double legYmax=0.35;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(MISTAG_RATE,"Anti-tag and probe","LP");
    leg->AddEntry(MISTAG_RATE_MASSCUT,"Pass mass cut anti-tag and probe","LP");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Compare_NminusOne_MISTAG_RATE.png");

    // Large bin mistag rate 	
	TH1D *MISTAG_RATE2 = topProbePt_rebin2->Clone();
    MISTAG_RATE2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE2->Sumw2();
    MISTAG_RATE2->Divide(topTagPt_rebin2,topProbePt_rebin2,1.,1.,"B");
    MISTAG_RATE2->SetMarkerStyle(21);
    MISTAG_RATE2->SetMarkerColor(2);
    MISTAG_RATE2->SetLineColor(2);
    MISTAG_RATE2->Draw();
    MISTAG_RATE2->SetName("TYPE11_MISTAG_LARGEBINS");
    c1000->SaveAs("mistag_plots/MISTAG_RATE_LARGEBINS.png");

    TH1D *MISTAG_RATE_MASSCUT2 = massCutProbePt_rebin2->Clone();
    MISTAG_RATE_MASSCUT2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_MASSCUT2->Sumw2();
    MISTAG_RATE_MASSCUT2->Divide(massCutTagPt_rebin2,massCutProbePt_rebin2,1.,1.,"B");
    MISTAG_RATE_MASSCUT2->SetMarkerStyle(22);
    MISTAG_RATE_MASSCUT2->SetMarkerColor(4);
    MISTAG_RATE_MASSCUT2->SetLineColor(4);
    MISTAG_RATE_MASSCUT2->Draw("");
    MISTAG_RATE_MASSCUT2->SetName("TYPE11_MISTAG_MASSCUT_LARGEBINS");
    c1000->SaveAs("mistag_plots/MISTAG_RATE_MASSCUT_LARGEBINS.png");

    MISTAG_RATE_MASSCUT2->Draw("");
    MISTAG_RATE2->Draw("same");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Compare_NminusOne_MISTAG_RATE_LARGEBINS.png");

	
	
	//------------------------------------------------------------------------------------------------------------//
    //------------------------------------------------------------------------------------------------------------//
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// TTBAR Mistag plots
	
    // small bin
	TH1D *MISTAG_RATE_TTBAR = topProbePtTTBAR_rebin->Clone();
	MISTAG_RATE_TTBAR->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
	MISTAG_RATE_TTBAR->Sumw2();
	MISTAG_RATE_TTBAR->Divide(topTagPtTTBAR_rebin,topProbePtTTBAR_rebin,1.,1.,"B");
	MISTAG_RATE_TTBAR->SetMarkerStyle(20);
	MISTAG_RATE_TTBAR->SetMarkerColor(1);
	MISTAG_RATE_TTBAR->SetLineColor(1);
	MISTAG_RATE_TTBAR->Draw();
	c1000->SaveAs("mistag_plots/MISTAG_RATE_TTBAR.png");

	TH1D *MISTAG_RATE_TTBAR_MASSCUT = massCutProbePtTTBAR_rebin->Clone();
	MISTAG_RATE_TTBAR_MASSCUT->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
	MISTAG_RATE_TTBAR_MASSCUT->Sumw2();
	MISTAG_RATE_TTBAR_MASSCUT->Divide(massCutTagPtTTBAR_rebin,massCutProbePtTTBAR_rebin,1.,1.,"B");
	MISTAG_RATE_TTBAR_MASSCUT->SetMarkerStyle(23);
	MISTAG_RATE_TTBAR_MASSCUT->SetMarkerColor(3);
	MISTAG_RATE_TTBAR_MASSCUT->SetLineColor(3);
	MISTAG_RATE_TTBAR_MASSCUT->Draw("");
	c1000->SaveAs("mistag_plots/MISTAG_RATE_TTBAR_MASSCUT.png");
	
	MISTAG_RATE_TTBAR_MASSCUT->Draw("");
	MISTAG_RATE_TTBAR->Draw("same");

    double legXmin=0.3;
    double legYmin=0.18;
    double legXmax=0.8;//0.58
    double legYmax=0.35;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(MISTAG_RATE_TTBAR,"Anti-tag and probe","LP");
    leg->AddEntry(MISTAG_RATE_TTBAR_MASSCUT,"Pass mass cut anti-tag and probe","LP");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Compare_NminusOne_MISTAG_RATE_TTBAR.png");
	
	// Large bin
 	
	TH1D *MISTAG_RATE_TTBAR2 = topProbePtTTBAR_rebin2->Clone();
    MISTAG_RATE_TTBAR2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_TTBAR2->Sumw2();
    MISTAG_RATE_TTBAR2->Divide(topTagPtTTBAR_rebin2,topProbePtTTBAR_rebin2,1.,1.,"B");
    MISTAG_RATE_TTBAR2->SetMarkerStyle(20);
    MISTAG_RATE_TTBAR2->SetMarkerColor(1);
    MISTAG_RATE_TTBAR2->SetLineColor(1);
    MISTAG_RATE_TTBAR2->Draw();
    c1000->SaveAs("mistag_plots/MISTAG_RATE_TTBAR_LARGEBINS.png");

    TH1D *MISTAG_RATE_TTBAR_MASSCUT2 = massCutProbePtTTBAR_rebin2->Clone();
    MISTAG_RATE_TTBAR_MASSCUT2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_TTBAR_MASSCUT2->Sumw2();
    MISTAG_RATE_TTBAR_MASSCUT2->Divide(massCutTagPtTTBAR_rebin2,massCutProbePtTTBAR_rebin2,1.,1.,"B");
    MISTAG_RATE_TTBAR_MASSCUT2->SetMarkerStyle(23);
    MISTAG_RATE_TTBAR_MASSCUT2->SetMarkerColor(3);
    MISTAG_RATE_TTBAR_MASSCUT2->SetLineColor(3);
    MISTAG_RATE_TTBAR_MASSCUT2->Draw("");
    c1000->SaveAs("mistag_plots/MISTAG_RATE_TTBAR_MASSCUT_LARGEBINS.png");

    MISTAG_RATE_TTBAR_MASSCUT2->Draw("");
    MISTAG_RATE_TTBAR2->Draw("same");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Compare_NminusOne_MISTAG_RATE_TTBAR_LARGEBINS.png");

		
	//------------------------------------------------------------------------------------------------------------//
    //------------------------------------------------------------------------------------------------------------//
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// SubtractTTBAR Mistag plots
	
    // small bin
	TH1D *MISTAG_RATE_SubtractTTBAR = topProbePtSubtractTTBAR_rebin->Clone();
	MISTAG_RATE_SubtractTTBAR->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
	MISTAG_RATE_SubtractTTBAR->Sumw2();
	MISTAG_RATE_SubtractTTBAR->Divide(topTagPtSubtractTTBAR_rebin,topProbePtSubtractTTBAR_rebin,1.,1.,"B");
	MISTAG_RATE_SubtractTTBAR->SetMarkerStyle(20);
	MISTAG_RATE_SubtractTTBAR->SetMarkerColor(1);
	MISTAG_RATE_SubtractTTBAR->SetLineColor(1);
	MISTAG_RATE_SubtractTTBAR->Draw();
	c1000->SaveAs("mistag_plots/MISTAG_RATE_SubtractTTBAR.png");

	TH1D *MISTAG_RATE_SubtractTTBAR_MASSCUT = massCutProbePtSubtractTTBAR_rebin->Clone();
	MISTAG_RATE_SubtractTTBAR_MASSCUT->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
	MISTAG_RATE_SubtractTTBAR_MASSCUT->Sumw2();
	MISTAG_RATE_SubtractTTBAR_MASSCUT->Divide(massCutTagPtSubtractTTBAR_rebin,massCutProbePtSubtractTTBAR_rebin,1.,1.,"B");
	MISTAG_RATE_SubtractTTBAR_MASSCUT->SetMarkerStyle(23);
	MISTAG_RATE_SubtractTTBAR_MASSCUT->SetMarkerColor(3);
	MISTAG_RATE_SubtractTTBAR_MASSCUT->SetLineColor(3);
	MISTAG_RATE_SubtractTTBAR_MASSCUT->Draw("");
	c1000->SaveAs("mistag_plots/MISTAG_RATE_SubtractTTBAR_MASSCUT.png");
	
	MISTAG_RATE_SubtractTTBAR_MASSCUT->Draw("");
	MISTAG_RATE_SubtractTTBAR->Draw("same");

    double legXmin=0.3;
    double legYmin=0.18;
    double legXmax=0.8;//0.58
    double legYmax=0.35;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(MISTAG_RATE_SubtractTTBAR,"Anti-tag and probe","LP");
    leg->AddEntry(MISTAG_RATE_SubtractTTBAR_MASSCUT,"Pass mass cut anti-tag and probe","LP");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Compare_NminusOne_MISTAG_RATE_SubtractTTBAR.png");
	
	// Large bin
 	
	TH1D *MISTAG_RATE_SubtractTTBAR2 = topProbePtSubtractTTBAR_rebin2->Clone();
    MISTAG_RATE_SubtractTTBAR2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_SubtractTTBAR2->Sumw2();
    MISTAG_RATE_SubtractTTBAR2->Divide(topTagPtSubtractTTBAR_rebin2,topProbePtSubtractTTBAR_rebin2,1.,1.,"B");
    MISTAG_RATE_SubtractTTBAR2->SetMarkerStyle(20);
    MISTAG_RATE_SubtractTTBAR2->SetMarkerColor(1);
    MISTAG_RATE_SubtractTTBAR2->SetLineColor(1);
    MISTAG_RATE_SubtractTTBAR2->Draw();
    c1000->SaveAs("mistag_plots/MISTAG_RATE_SubtractTTBAR_LARGEBINS.png");

    TH1D *MISTAG_RATE_SubtractTTBAR_MASSCUT2 = massCutProbePtSubtractTTBAR_rebin2->Clone();
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->Sumw2();
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->Divide(massCutTagPtSubtractTTBAR_rebin2,massCutProbePtSubtractTTBAR_rebin2,1.,1.,"B");
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->SetMarkerStyle(23);
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->SetMarkerColor(3);
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->SetLineColor(3);
    MISTAG_RATE_SubtractTTBAR_MASSCUT2->Draw("");
    c1000->SaveAs("mistag_plots/MISTAG_RATE_SubtractTTBAR_MASSCUT_LARGEBINS.png");

    MISTAG_RATE_SubtractTTBAR_MASSCUT2->Draw("");
    MISTAG_RATE_SubtractTTBAR2->Draw("same");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Compare_NminusOne_MISTAG_RATE_SubtractTTBAR_LARGEBINS.png");

	//------------------------------------------------------------------------------------------------------------//
	
	MISTAG_RATE_MASSCUT2->Draw();
	MISTAG_RATE_SubtractTTBAR_MASSCUT2->Draw("same");
	 double legXmin=0.3;
    double legYmin=0.18;
    double legXmax=0.8;//0.58
    double legYmax=0.35;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(MISTAG_RATE_MASSCUT2,"Data","LP");
    leg->AddEntry(MISTAG_RATE_SubtractTTBAR_MASSCUT2,"Data with TTbar subtracted","LP");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/DATAsubtractTTBAR_MISTAG_RATE_MASSCUT2.png");

	//------------------------------------------------------------------------------------------------------------//
  
	MISTAG_RATE             ->SetName("TYPE11_MISTAG");
	MISTAG_RATE_MASSCUT     ->SetName("TYPE11_MISTAG_MASSCUT");
    MISTAG_RATE2            ->SetName("TYPE11_MISTAG_LARGEBINS");
    MISTAG_RATE_MASSCUT2    ->SetName("TYPE11_MISTAG_MASSCUT_LARGEBINS");
	MISTAG_RATE_SubtractTTBAR           ->SetName("TYPE11_MISTAG_SUBTRACT_TTBAR");
	MISTAG_RATE_SubtractTTBAR_MASSCUT   ->SetName("TYPE11_MISTAG_MASSCUT_SUBTRACT_TTBAR");
	MISTAG_RATE_SubtractTTBAR2          ->SetName("TYPE11_MISTAG_SUBTRACT_TTBAR_LARGEBINS");
	MISTAG_RATE_SubtractTTBAR_MASSCUT2  ->SetName("TYPE11_MISTAG_MASSCUT_SUBTRACT_TTBAR_LARGEBINS");
  
    TFile *Out;
	Out = new TFile("MISTAG_RATE_TYPE1_SUBTRACT.root","RECREATE");
	Out->cd();
	
	MISTAG_RATE->Write();
	MISTAG_RATE_MASSCUT->Write();
	MISTAG_RATE2->Write();
	MISTAG_RATE_MASSCUT2->Write();
	MISTAG_RATE_SubtractTTBAR->Write();
	MISTAG_RATE_SubtractTTBAR_MASSCUT->Write();
	MISTAG_RATE_SubtractTTBAR2->Write();
	MISTAG_RATE_SubtractTTBAR_MASSCUT2->Write();
	
	Out->ls();      
	Out->Write();

  
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // test plots
    
    TCanvas *c1000= new TCanvas("c1000","",200,10,700,650);	

	topProbePt_rebin		->SetLineColor(1);
	topTagPt_rebin			->SetLineColor(2);
	massCutProbePt_rebin	->SetLineColor(3);
	massCutTagPt_rebin		->SetLineColor(4);

	topProbePt_rebin			->Draw();
	topTagPt_rebin				->Draw("same");
	massCutProbePt_rebin	->Draw("same");
	massCutTagPt_rebin	->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/PT_rebin.png");
	c1000->SetLogy(0);
    
    // Data PT plots
    
    topProbePt			->Rebin(10);
	topTagPt			->Rebin(10);
	massCutProbePt	    ->Rebin(10);
	massCutTagPt		->Rebin(10);
	
	topProbePt	    ->SetLineColor(1);
	topTagPt	    ->SetLineColor(2);
	massCutProbePt  ->SetLineColor(3);
	massCutTagPt    ->SetLineColor(4);

	topProbePt	->Draw();
	topTagPt    ->Draw("same");
	massCutProbePt->Draw("same");
	massCutTagPt->Draw("same");
	
	double legXmin=0.62;
    double legYmin=0.76;
    double legXmax=0.97;//0.58
    double legYmax=0.88;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePt,"topProbePt","LP");
    leg->AddEntry(topTagPt,"topTagPt","LP");
    leg->AddEntry(massCutProbePt,"massCutProbePt","LP");
    leg->AddEntry(massCutTagPt,"massCutTagPt","LP");
    leg->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/PT_Data.png");
	c1000->SetLogy(0);


  

    // TTBAR PT plots
    
    topProbePtTTBAR			->Rebin(10);
	topTagPtTTBAR			->Rebin(10);
	massCutProbePtTTBAR	    ->Rebin(10);
	massCutTagPtTTBAR		->Rebin(10);
	
	topProbePtTTBAR	    ->SetLineColor(1);
	topTagPtTTBAR	    ->SetLineColor(2);
	massCutProbePtTTBAR  ->SetLineColor(3);
	massCutTagPtTTBAR    ->SetLineColor(4);

	topProbePtTTBAR	->Draw();
	topTagPtTTBAR    ->Draw("same");
	massCutProbePtTTBAR->Draw("same");
	massCutTagPtTTBAR->Draw("same");
	
	double legXmin=0.62;
    double legYmin=0.76;
    double legXmax=0.97;//0.58
    double legYmax=0.88;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePtTTBAR,"topProbePtTTBAR","LP");
    leg->AddEntry(topTagPtTTBAR,"topTagPtTTBAR","LP");
    leg->AddEntry(massCutProbePtTTBAR,"massCutProbePtTTBAR","LP");
    leg->AddEntry(massCutTagPtTTBAR,"massCutTagPtTTBAR","LP");
    leg->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/PT_ttbar.png");
	c1000->SetLogy(0);


     // Data with TTBAR subtracted PT plots
    
    topProbePtSubtractTTBAR			->Rebin(10);
	topTagPtSubtractTTBAR			->Rebin(10);
	massCutProbePtSubtractTTBAR	    ->Rebin(10);
	massCutTagPtSubtractTTBAR		->Rebin(10);
	
	topProbePtSubtractTTBAR	    ->SetLineColor(1);
	topTagPtSubtractTTBAR	    ->SetLineColor(2);
	massCutProbePtSubtractTTBAR  ->SetLineColor(3);
	massCutTagPtSubtractTTBAR    ->SetLineColor(4);

	topProbePtSubtractTTBAR	->Draw();
	topTagPtSubtractTTBAR    ->Draw("same");
	massCutProbePtSubtractTTBAR->Draw("same");
	massCutTagPtSubtractTTBAR->Draw("same");
	
	double legXmin=0.62;
    double legYmin=0.76;
    double legXmax=0.97;//0.58
    double legYmax=0.88;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePtSubtractTTBAR,"topProbePtSubtractTTBAR","LP");
    leg->AddEntry(topTagPtSubtractTTBAR,"topTagPtSubtractTTBAR","LP");
    leg->AddEntry(massCutProbePtSubtractTTBAR,"massCutProbePtSubtractTTBAR","LP");
    leg->AddEntry(massCutTagPtSubtractTTBAR,"massCutTagPtSubtractTTBAR","LP");
    leg->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/PT_SubtractTTBAR.png");
	c1000->SetLogy(0);


    // Compare
    massCutTagPt->SetTitle(";Tagged Probe Jet p_{T};");
    massCutTagPt->Rebin(1);
    massCutTagPtTTBAR->Rebin(1);
    massCutTagPtSubtractTTBAR->Rebin(1);
    
    massCutTagPt->SetLineColor(1);
    massCutTagPtTTBAR->SetLineColor(2);
    massCutTagPtSubtractTTBAR->SetLineColor(3);
	
	massCutTagPt->Draw();
	massCutTagPtTTBAR->Draw("same");
	massCutTagPtSubtractTTBAR->Draw("HISTsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(massCutTagPt,"Data","LP");
    leg->AddEntry(massCutTagPtTTBAR,"TTBAR MC","LP");
    leg->AddEntry(massCutTagPtSubtractTTBAR,"Data with TTBAR subtracted","LP");
    leg->Draw("same");
	
	c1000->SaveAs("mistag_plots/DATAsubtractTTBAR_TaggedProbePT.png");
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/DATAsubtractTTBAR_TaggedProbePT_LOG.png");
	c1000->SetLogy(0);
	
	 // Compare
    massCutProbePt->SetTitle(";Probe Jet p_{T};");
    massCutProbePt->Rebin(1);
    massCutProbePtTTBAR->Rebin(1);
    massCutProbePtSubtractTTBAR->Rebin(1);
    
    massCutProbePt->SetLineColor(1);
    massCutProbePtTTBAR->SetLineColor(2);
    massCutProbePtSubtractTTBAR->SetLineColor(3);
	
	massCutProbePt->Draw();
	massCutProbePtTTBAR->Draw("same");
	massCutProbePtSubtractTTBAR->Draw("HISTsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(massCutProbePt,"Data","LP");
    leg->AddEntry(massCutProbePtTTBAR,"TTBAR MC","LP");
    leg->AddEntry(massCutProbePtSubtractTTBAR,"Data with TTBAR subtracted","LP");
    leg->Draw("same");
	
	c1000->SaveAs("mistag_plots/DATAsubtractTTBAR_ProbePT.png");
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/DATAsubtractTTBAR_ProbePT_LOG.png");
	c1000->SetLogy(0);
}
	
