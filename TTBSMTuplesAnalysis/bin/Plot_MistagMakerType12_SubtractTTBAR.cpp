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

	TFile *ROOT 			= new TFile("TTHadronicAnalyzerCombined_Jet_PD_May10ReReco_PromptReco_range1_range2_v4_mistag.root");
	TFile *ROOT_TTBAR 		= new TFile("TTHadronicAnalyzerCombined_TTJets_TuneZ2_mistag.root");

    TH1D * topTagPt			=  ROOT	-> Get("type2KinTopTag");
	TH1D * topProbePt		=  ROOT -> Get("type2KinTopProbe");
	
	TH1D * topTagPtTTBAR		=  ROOT_TTBAR -> Get("type2KinTopTag");
	TH1D * topProbePtTTBAR		=  ROOT_TTBAR -> Get("type2KinTopProbe");
	
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
	
	TH1D *topTagPtSubtractTTBAR         = topTagPt->Clone();
	TH1D *topProbePtSubtractTTBAR       = topProbePt->Clone();
	
	topTagPtSubtractTTBAR       ->Add( topTagPtTTBAR,-1);
	topProbePtSubtractTTBAR     ->Add( topProbePtTTBAR,-1);
	
	// Rebin with small bins
 	Int_t num_bins=26;
    Double_t bins[num_bins+1]= {350,355,360,365,370,375,380,385,390,395,400,410,420,430,440,450,460,480,500,525,550,600,650,700,800,1000,1200}; 
	TH1D *topTagPt_rebin 		= topTagPt			->Rebin(num_bins,"topTagPt_rebin",bins); 
	TH1D *topProbePt_rebin 		= topProbePt		->Rebin(num_bins,"topProbePt_rebin",bins); 
	
	TH1D *topTagPtTTBAR_rebin 		= topTagPtTTBAR			->Rebin(num_bins,"topTagPtTTBAR_rebin",bins); 
	TH1D *topProbePtTTBAR_rebin 	= topProbePtTTBAR		->Rebin(num_bins,"topProbePtTTBAR_rebin",bins); 
	
	TH1D *topTagPtSubtractTTBAR_rebin 		= topTagPtSubtractTTBAR			->Rebin(num_bins,"topTagPtSubtractTTBAR_rebin",bins); 
	TH1D *topProbePtSubtractTTBAR_rebin 	= topProbePtSubtractTTBAR		->Rebin(num_bins,"topProbePtSubtractTTBAR_rebin",bins); 
	
	// Rebin with large bins
 	Int_t num_bins2=9;
    Double_t bins2[num_bins2+1]= {350,375,400,450,500,600,700,800,1000,1200}; 
	TH1D *topTagPt_rebin2 		= topTagPt			->Rebin(num_bins2,"topTagPt_rebin2",bins2); 
	TH1D *topProbePt_rebin2 	= topProbePt		->Rebin(num_bins2,"topProbePt_rebin2",bins2); 
		
	TH1D *topTagPtTTBAR_rebin2 		 = topTagPtTTBAR		->Rebin(num_bins2,"topTagPtTTBAR_rebin2",bins2); 
	TH1D *topProbePtTTBAR_rebin2 	 = topProbePtTTBAR		->Rebin(num_bins2,"topProbePtTTBAR_rebin2",bins2); 
	
	TH1D *topTagPtSubtractTTBAR_rebin2 		 = topTagPtSubtractTTBAR		->Rebin(num_bins2,"topTagPtSubtractTTBAR_rebin2",bins2); 
	TH1D *topProbePtSubtractTTBAR_rebin2 	 = topProbePtSubtractTTBAR		->Rebin(num_bins2,"topProbePtSubtractTTBAR_rebin2",bins2); 
	
	
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
	c1000->SaveAs("mistag_plots/Type12_MISTAG_RATE.png");
	
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
    c1000->SaveAs("mistag_plots/Type12_MISTAG_RATE_LARGEBINS.png");

		
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
	c1000->SaveAs("mistag_plots/Type12_MISTAG_RATE_TTBAR.png");

	// Large bin
 	
	TH1D *MISTAG_RATE_TTBAR2 = topProbePtTTBAR_rebin2->Clone();
    MISTAG_RATE_TTBAR2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_TTBAR2->Sumw2();
    MISTAG_RATE_TTBAR2->Divide(topTagPtTTBAR_rebin2,topProbePtTTBAR_rebin2,1.,1.,"B");
    MISTAG_RATE_TTBAR2->SetMarkerStyle(20);
    MISTAG_RATE_TTBAR2->SetMarkerColor(1);
    MISTAG_RATE_TTBAR2->SetLineColor(1);
    MISTAG_RATE_TTBAR2->Draw();
    c1000->SaveAs("mistag_plots/Type12_MISTAG_RATE_TTBAR_LARGEBINS.png");

		
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
	c1000->SaveAs("mistag_plots/Type12_MISTAG_RATE_SubtractTTBAR.png");

	// Large bin
 	
	TH1D *MISTAG_RATE_SubtractTTBAR2 = topProbePtSubtractTTBAR_rebin2->Clone();
    MISTAG_RATE_SubtractTTBAR2->SetTitle(";Jet p_{T} (GeV/c); Top Mistag Rate");
    MISTAG_RATE_SubtractTTBAR2->Sumw2();
    MISTAG_RATE_SubtractTTBAR2->Divide(topTagPtSubtractTTBAR_rebin2,topProbePtSubtractTTBAR_rebin2,1.,1.,"B");
    MISTAG_RATE_SubtractTTBAR2->SetMarkerStyle(20);
    MISTAG_RATE_SubtractTTBAR2->SetMarkerColor(1);
    MISTAG_RATE_SubtractTTBAR2->SetLineColor(1);
    MISTAG_RATE_SubtractTTBAR2->Draw();
    c1000->SaveAs("mistag_plots/Type12_MISTAG_RATE_SubtractTTBAR_LARGEBINS.png");

  

	//------------------------------------------------------------------------------------------------------------//
	
	MISTAG_RATE->Draw();
	MISTAG_RATE_SubtractTTBAR->Draw("same");
	 double legXmin=0.3;
    double legYmin=0.18;
    double legXmax=0.8;//0.58
    double legYmax=0.35;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(MISTAG_RATE,"Data","LP");
    leg->AddEntry(MISTAG_RATE_SubtractTTBAR,"Data with TTbar subtracted","LP");
    leg->Draw("same");
	c1000->SaveAs("mistag_plots/Type12_DATAsubtractTTBAR_MISTAG_RATE.png");


	//------------------------------------------------------------------------------------------------------------//
  
	MISTAG_RATE             ->SetName("TYPE12_KIN_MISTAG");
    MISTAG_RATE2            ->SetName("TYPE12_KIN_MISTAG_LARGEBINS");
	MISTAG_RATE_SubtractTTBAR           ->SetName("TYPE12_KIN_MISTAG_SUBTRACT_TTBAR");
	MISTAG_RATE_SubtractTTBAR2          ->SetName("TYPE12_KIN_MISTAG_SUBTRACT_TTBAR_LARGEBINS");
  
  
    TH1D * TYPE2_TOP_TAG_MASS			=  ROOT	-> Get("type2TopTagMass");
    TYPE2_TOP_TAG_MASS->SetName("TYPE2_TOP_TAG_MASS");
  
    TFile *Out;
	Out = new TFile("MISTAG_RATE_TYPE12_SUBTRACT.root","RECREATE");
	Out->cd();
	
	
	TYPE2_TOP_TAG_MASS->Write();
	MISTAG_RATE->Write();
	MISTAG_RATE2->Write();
	MISTAG_RATE_SubtractTTBAR->Write();
	MISTAG_RATE_SubtractTTBAR2->Write();
	
	Out->ls();      
	Out->Write();

  
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // test plots
    
    TCanvas *c1000= new TCanvas("c1000","",200,10,700,650);	

	topProbePt_rebin		->SetLineColor(1);
	topTagPt_rebin			->SetLineColor(2);
	

	topProbePt_rebin			->Draw();
	topTagPt_rebin				->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/Type12_PT_rebin.png");
	c1000->SetLogy(0);
    
    // Data PT plots
    
    topProbePt			->Rebin(10);
	topTagPt			->Rebin(10);
	
	
	topProbePt	    ->SetLineColor(1);
	topTagPt	    ->SetLineColor(2);


	topProbePt	->Draw();
	topTagPt    ->Draw("same");
	
	double legXmin=0.62;
    double legYmin=0.76;
    double legXmax=0.97;//0.58
    double legYmax=0.88;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePt,"topProbePt","LP");
    leg->AddEntry(topTagPt,"topTagPt","LP");
    leg->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/Type12_PT_Data.png");
	c1000->SetLogy(0);


  

    // TTBAR PT plots
    
    topProbePtTTBAR			->Rebin(10);
	topTagPtTTBAR			->Rebin(10);
	
	topProbePtTTBAR	    ->SetLineColor(1);
	topTagPtTTBAR	    ->SetLineColor(2);
	
	topProbePtTTBAR	->Draw();
	topTagPtTTBAR    ->Draw("same");
	
	double legXmin=0.62;
    double legYmin=0.76;
    double legXmax=0.97;//0.58
    double legYmax=0.88;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePtTTBAR,"topProbePtTTBAR","LP");
    leg->AddEntry(topTagPtTTBAR,"topTagPtTTBAR","LP");
    
    leg->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/Type12_PT_ttbar.png");
	c1000->SetLogy(0);


     // Data with TTBAR subtracted PT plots
    
    topProbePtSubtractTTBAR			->Rebin(10);
	topTagPtSubtractTTBAR			->Rebin(10);
	
	topProbePtSubtractTTBAR	    ->SetLineColor(1);
	topTagPtSubtractTTBAR	    ->SetLineColor(2);
	
	topProbePtSubtractTTBAR	->Draw();
	topTagPtSubtractTTBAR    ->Draw("same");
	
	
	double legXmin=0.62;
    double legYmin=0.76;
    double legXmax=0.97;//0.58
    double legYmax=0.88;

    leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePtSubtractTTBAR,"topProbePtSubtractTTBAR","LP");
    leg->AddEntry(topTagPtSubtractTTBAR,"topTagPtSubtractTTBAR","LP");
    
    leg->Draw("same");
	
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/Type12_PT_SubtractTTBAR.png");
	c1000->SetLogy(0);


    // Compare
    topTagPt->SetTitle(";Tagged Probe Jet p_{T};");
    topTagPt->Rebin(1);
    topTagPtTTBAR->Rebin(1);
    topTagPtSubtractTTBAR->Rebin(1);
    
    topTagPt->SetLineColor(1);
    topTagPtTTBAR->SetLineColor(2);
    topTagPtSubtractTTBAR->SetLineColor(3);
	
	topTagPt->Draw();
	topTagPtTTBAR->Draw("same");
	topTagPtSubtractTTBAR->Draw("HISTsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topTagPt,"Data","LP");
    leg->AddEntry(topTagPtTTBAR,"TTBAR MC","LP");
    leg->AddEntry(topTagPtSubtractTTBAR,"Data with TTBAR subtracted","LP");
    leg->Draw("same");
	
	c1000->SaveAs("mistag_plots/Type12_DATAsubtractTTBAR_TaggedProbePT.png");
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/Type12_DATAsubtractTTBAR_TaggedProbePT_LOG.png");
	c1000->SetLogy(0);
	
	 // Compare
    topProbePt->SetTitle(";Probe Jet p_{T};");
    topProbePt->Rebin(1);
    topProbePtTTBAR->Rebin(1);
    topProbePtSubtractTTBAR->Rebin(1);
    
    topProbePt->SetLineColor(1);
    topProbePtTTBAR->SetLineColor(2);
    topProbePtSubtractTTBAR->SetLineColor(3);
	
	topProbePt->Draw();
	topProbePtTTBAR->Draw("same");
	topProbePtSubtractTTBAR->Draw("HISTsame");
	
	leg = new TLegend(legXmin,legYmin,legXmax,legYmax);
    leg->SetBorderSize(1);
    leg->SetFillColor(0);
    leg->AddEntry(topProbePt,"Data","LP");
    leg->AddEntry(topProbePtTTBAR,"TTBAR MC","LP");
    leg->AddEntry(topProbePtSubtractTTBAR,"Data with TTBAR subtracted","LP");
    leg->Draw("same");
	
	c1000->SaveAs("mistag_plots/Type12_DATAsubtractTTBAR_ProbePT.png");
	c1000->SetLogy();
	c1000->SaveAs("mistag_plots/Type12_DATAsubtractTTBAR_ProbePT_LOG.png");
	c1000->SetLogy(0);
}
	
