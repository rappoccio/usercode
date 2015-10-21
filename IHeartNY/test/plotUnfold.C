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
#include "TPad.h"
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
void drawCMS(Double_t x,Double_t y, bool pad, bool prel, bool forPublic);

void plot(TString channel, TString toUnfold, bool wobtag, bool do2step, bool doNormalized, bool doLogscale, bool doAverageErr);

void plotUnfold(TString channel, TString toUnfold="pt") {

  bool doNormalized = false;   // normalized differential?
  bool doLogscale   = true;   // plot distributions on log scale?
  bool doAverageErr = true;   // average up/down systematic uncertainties? 

  plot(channel,toUnfold,true,true, doNormalized,doLogscale,doAverageErr);
  plot(channel,toUnfold,true,false, doNormalized,doLogscale,doAverageErr);
  plot(channel,toUnfold,false,true, doNormalized,doLogscale,doAverageErr);
  plot(channel,toUnfold,false,false, doNormalized,doLogscale,doAverageErr);

}

void plot(TString channel, TString toUnfold, bool wobtag, bool do2step, bool doNormalized, bool doLogscale, bool doAverageErr) {
  
  SetPlotStyle();
    
  bool doQ2 = true;
  
  if (!doQ2) cout << endl << "WARNING! Running WITHOUT Q2 uncertainty" << endl << endl;

  TString nobtag = "_nobtag";
  if (!wobtag) nobtag = "";

  TString twoStep = "_2step";
  if (!do2step) twoStep = "";
  
  TString muOrEl = "";
  if (channel == "el") muOrEl = "_el";

  bool forpub = false; // plot for public?
  if (wobtag && do2step && channel == "comb") forpub=true; 


  // ---------------------------------------------------------------------------------------------------------------
  // get files & histograms
  // ---------------------------------------------------------------------------------------------------------------
  
  cout << endl << "Getting files and hists..." << endl;

  const int nSYST = 1+10+4+2+1; //nominal+expSyst+thSyst
  TString name_syst[nSYST] = {"_CT10_nom_nom",
			      "_CT10_nom_jecup",
			      "_CT10_nom_jecdn",
			      "_CT10_nom_jerup",
			      "_CT10_nom_jerdn",			      
			      "_CT10_nom_btagup",
			      "_CT10_nom_btagdn",
			      "_CT10_nom_toptagup",
			      "_CT10_nom_toptagdn",
			      "_CT10_nom_nom_bkgup",
			      "_CT10_nom_nom_bkgdn",
			      "_CT10_pdfup_nom",
			      "_CT10_pdfdown_nom",
			      "_scaleup_nom",
			      "_scaledown_nom",
			      "_CT10_nom_toptagHIGHPTup",
			      "_CT10_nom_toptagHIGHPTdn",
			      "_PS"
  };
  
  if (channel == "comb") const int nCHANNEL = 2;
  else const int nCHANNEL = 1;

  TString channel_name[nCHANNEL];
  if (nCHANNEL == 1) channel_name[0] = channel;
  else if (nCHANNEL == 2) {
    channel_name[0] = "el";
    channel_name[1] = "mu";
  }
  else return; //shouldn't happen


  TFile* f_syst[nCHANNEL][nSYST];

  TH1F* h_true_tmp[nCHANNEL];
  TH1F* h_unfolded_tmp[nCHANNEL][nSYST];
  TH1F* h_part_tmp[nCHANNEL];
  TH1F* h_unfolded_part_tmp[nCHANNEL][nSYST];

  TFile* fMG[nCHANNEL];
  TH1F* h_trueMG_tmp[nCHANNEL];
  TH1F* h_partMG_tmp[nCHANNEL];

  TFile* fMCNLO[nCHANNEL];
  TH1F* h_trueMCNLO_tmp[nCHANNEL];
  TH1F* h_partMCNLO_tmp[nCHANNEL];

  if (channel == "comb") {

    //MadGraph
    fMG[0] = new TFile("UnfoldingPlots/unfold"+twoStep+"_"+toUnfold+"_MG_nom_nobtag.root");
    fMG[1] = new TFile("UnfoldingPlots/unfold_el"+twoStep+"_"+toUnfold+"_MG_nom_nobtag.root");

    h_trueMG_tmp[0] = (TH1F*) fMG[0]->Get(toUnfold+"_genTop")->Clone();
    h_trueMG_tmp[0]->SetName(toUnfold+"_genTop_MG_el");
    if (toUnfold == "pt") h_trueMG_tmp[0]->SetAxisRange(400,1150,"X");

    h_trueMG_tmp[1] = (TH1F*) fMG[1]->Get(toUnfold+"_genTop")->Clone();
    h_trueMG_tmp[1]->SetName(toUnfold+"_genTop_MG_mu");
    if (toUnfold == "pt") h_trueMG_tmp[1]->SetAxisRange(400,1150,"X");    

    //MC@NLO
    fMCNLO[0] = new TFile("UnfoldingPlots/unfold"+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag.root");
    fMCNLO[1] = new TFile("UnfoldingPlots/unfold_el"+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag.root");

    h_trueMCNLO_tmp[0] = (TH1F*) fMCNLO[0]->Get(toUnfold+"_genTop")->Clone();
    h_trueMCNLO_tmp[0]->SetName(toUnfold+"_genTop_MCNLO_el");
    if (toUnfold == "pt") h_trueMCNLO_tmp[0]->SetAxisRange(400,1150,"X");

    h_trueMCNLO_tmp[1] = (TH1F*) fMCNLO[1]->Get(toUnfold+"_genTop")->Clone();
    h_trueMCNLO_tmp[1]->SetName(toUnfold+"_genTop_MCNLO_mu");
    if (toUnfold == "pt") h_trueMCNLO_tmp[1]->SetAxisRange(400,1150,"X");    
        
    if (twoStep == "_2step") {
      h_partMG_tmp[0] = (TH1F*) fMG[0]->Get(toUnfold+"_partTop")->Clone();
      h_partMG_tmp[0]->SetName(toUnfold+"_partTop_MG_el");
      if (toUnfold == "pt") h_partMG_tmp[0]->SetAxisRange(400,1150,"X");
      h_partMG_tmp[1] = (TH1F*) fMG[1]->Get(toUnfold+"_partTop")->Clone();
      h_partMG_tmp[1]->SetName(toUnfold+"_partTop_MG_mu");
      if (toUnfold == "pt") h_partMG_tmp[1]->SetAxisRange(400,1150,"X");

      h_partMCNLO_tmp[0] = (TH1F*) fMCNLO[0]->Get(toUnfold+"_partTop")->Clone();
      h_partMCNLO_tmp[0]->SetName(toUnfold+"_partTop_MCNLO_el");
      if (toUnfold == "pt") h_partMCNLO_tmp[0]->SetAxisRange(400,1150,"X");
      h_partMCNLO_tmp[1] = (TH1F*) fMCNLO[1]->Get(toUnfold+"_partTop")->Clone();
      h_partMCNLO_tmp[1]->SetName(toUnfold+"_partTop_MCNLO_mu");
      if (toUnfold == "pt") h_partMCNLO_tmp[1]->SetAxisRange(400,1150,"X");
    }
  }
  else if (channel == "el") {
    //MadGraph
    fMG[0] = new TFile("UnfoldingPlots/unfold_el"+twoStep+"_"+toUnfold+"_MG_nom_nobtag.root");
    h_trueMG_tmp[0] = (TH1F*) fMG[0]->Get(toUnfold+"_genTop")->Clone();
    h_trueMG_tmp[0]->SetName(toUnfold+"_genTop_el");
    if (toUnfold == "pt") h_trueMG_tmp[0]->SetAxisRange(400,1150,"X");
    if (twoStep == "_2step") {
      h_partMG_tmp[0] = (TH1F*) fMG[0]->Get(toUnfold+"_partTop")->Clone();
      h_partMG_tmp[0]->SetName(toUnfold+"_partTop_el");
      if (toUnfold == "pt") h_partMG_tmp[0]->SetAxisRange(400,1150,"X");
    }

    //MC@NLO
    fMCNLO[0] = new TFile("UnfoldingPlots/unfold_el"+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag.root");
    h_trueMCNLO_tmp[0] = (TH1F*) fMCNLO[0]->Get(toUnfold+"_genTop")->Clone();
    h_trueMCNLO_tmp[0]->SetName(toUnfold+"_genTop_el");
    if (toUnfold == "pt") h_trueMCNLO_tmp[0]->SetAxisRange(400,1150,"X");
    if (twoStep == "_2step") {
      h_partMCNLO_tmp[0] = (TH1F*) fMCNLO[0]->Get(toUnfold+"_partTop")->Clone();
      h_partMCNLO_tmp[0]->SetName(toUnfold+"_partTop_el");
      if (toUnfold == "pt") h_partMCNLO_tmp[0]->SetAxisRange(400,1150,"X");
    }
  }
  else if (channel == "mu") {
    //MadGraph
    fMG[0] = new TFile("UnfoldingPlots/unfold"+twoStep+"_"+toUnfold+"_MG_nom_nobtag.root");
    h_trueMG_tmp[0] = (TH1F*) fMG[0]->Get(toUnfold+"_genTop")->Clone();
    h_trueMG_tmp[0]->SetName(toUnfold+"_genTop_mu");
    if (toUnfold == "pt") h_trueMG_tmp[0]->SetAxisRange(400,1150,"X");
    if (twoStep == "_2step") {
      h_partMG_tmp[0] = (TH1F*) fMG[0]->Get(toUnfold+"_partTop")->Clone();
      h_partMG_tmp[0]->SetName(toUnfold+"_partTop_mu");
      if (toUnfold == "pt") h_partMG_tmp[0]->SetAxisRange(400,1150,"X");
    }

    //MC@NLO
    fMCNLO[0] = new TFile("UnfoldingPlots/unfold"+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag.root");
    h_trueMCNLO_tmp[0] = (TH1F*) fMCNLO[0]->Get(toUnfold+"_genTop")->Clone();
    h_trueMCNLO_tmp[0]->SetName(toUnfold+"_genTop_mu");
    if (toUnfold == "pt") h_trueMCNLO_tmp[0]->SetAxisRange(400,1150,"X");
    if (twoStep == "_2step") {
      h_partMCNLO_tmp[0] = (TH1F*) fMCNLO[0]->Get(toUnfold+"_partTop")->Clone();
      h_partMCNLO_tmp[0]->SetName(toUnfold+"_partTop_mu");
      if (toUnfold == "pt") h_partMCNLO_tmp[0]->SetAxisRange(400,1150,"X");
    }
  }


  for (int ic=0; ic<nCHANNEL; ic++) {
    for (int is=0; is<nSYST; is++) {
      
      if (name_syst[is]=="_PS") {
	if (channel == "comb") {
	  if (ic==0) f_syst[ic][is] = new TFile("UnfoldingPlots/unfold"+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag_closure_reverse.root");
	  else if (ic==1) f_syst[ic][is] = new TFile("UnfoldingPlots/unfold_el"+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag_closure_reverse.root");
	  else return; //shouldn't happen
	}
	else {
	  if (ic==0) f_syst[ic][is] = new TFile("UnfoldingPlots/unfold"+muOrEl+twoStep+"_"+toUnfold+"_mcnlo_nom_nobtag_closure_reverse.root");
	  else return; //shouldn't happen
	}

	h_unfolded_tmp[ic][is] = (TH1F*) f_syst[ic][is]->Get("UnfoldedMC")->Clone();
	h_unfolded_tmp[ic][is]->SetName("UnfoldedMC"+name_syst[is]+"_"+channel_name[ic]);
	if (toUnfold == "pt") h_unfolded_tmp[ic][is]->SetAxisRange(400,1150,"X");
	
	if (twoStep == "_2step") {
	  h_unfolded_part_tmp[ic][is] = (TH1F*) f_syst[ic][is]->Get("UnfoldedMC_rp")->Clone();
	  h_unfolded_part_tmp[ic][is]->SetName("UnfoldedMC_part"+name_syst[is]+"_"+channel_name[ic]);
	  if (toUnfold == "pt") h_unfolded_part_tmp[ic][is]->SetAxisRange(400,1150,"X");
	}

      }
      else {
	if (channel == "comb") {
	  if (ic==0) f_syst[ic][is] = new TFile("UnfoldingPlots/unfold"+twoStep+"_"+toUnfold+name_syst[is]+nobtag+".root");
	  else if (ic==1) f_syst[ic][is] = new TFile("UnfoldingPlots/unfold_el"+twoStep+"_"+toUnfold+name_syst[is]+nobtag+".root");
	  else return; //shouldn't happen
	}
	else {
	  if (ic==0) f_syst[ic][is] = new TFile("UnfoldingPlots/unfold"+muOrEl+twoStep+"_"+toUnfold+name_syst[is]+nobtag+".root");
	  else return; //shouldn't happen
	}

	h_unfolded_tmp[ic][is] = (TH1F*) f_syst[ic][is]->Get("UnfoldedData")->Clone();
	h_unfolded_tmp[ic][is]->SetName("UnfoldedData"+name_syst[is]+"_"+channel_name[ic]);
	if (toUnfold == "pt") h_unfolded_tmp[ic][is]->SetAxisRange(400,1150,"X");
	
	if (twoStep == "_2step") {
	  h_unfolded_part_tmp[ic][is] = (TH1F*) f_syst[ic][is]->Get("UnfoldedData_rp")->Clone();
	  h_unfolded_part_tmp[ic][is]->SetName("UnfoldedData_part"+name_syst[is]+"_"+channel_name[ic]);
	  if (toUnfold == "pt") h_unfolded_part_tmp[ic][is]->SetAxisRange(400,1150,"X");
	}

      }
   
      if (is==0) {
	h_true_tmp[ic] = (TH1F*) f_syst[ic][is]->Get(toUnfold+"_genTop")->Clone();
	h_true_tmp[ic]->SetName(toUnfold+"_genTop_"+channel_name[ic]);
	if (toUnfold == "pt") h_true_tmp[ic]->SetAxisRange(400,1150,"X");
	
	if (twoStep == "_2step") {
	  h_part_tmp[ic] = (TH1F*) f_syst[ic][is]->Get(toUnfold+"_partTop")->Clone();
	  h_part_tmp[ic]->SetName(toUnfold+"_partTop_"+channel_name[ic]);
	  if (toUnfold == "pt") h_part_tmp[ic]->SetAxisRange(400,1150,"X");
	}
      }
          
    }//end systematic loop
  }//end channel loop



  // ----------------------------------------------------------------------------------------------------------------
  // possibly perform combination of electron+muon channels
  // ----------------------------------------------------------------------------------------------------------------

  // histograms that need to be combined:
  // h_true_tmp[ic] --> top pt @ parton-level
  // h_unfolded_tmp[ic][is] --> data unfolded to parton-level
  // h_part_tmp[ic] --> top pt @ particle-level
  // h_unfolded_part_tmp[ic][is] --> data unfolded to particle-level


  TH1F* h_true;
  TH1F* h_unfolded[nSYST];
  TH1F* h_part;
  TH1F* h_unfolded_part[nSYST];

  TH1F* h_trueMG;
  TH1F* h_trueMCNLO;
  TH1F* h_partMG;
  TH1F* h_partMCNLO;


  // ----------------------------------------------------------------------------------------------------------------
  // no combination -- just copy the electron/muon histograms
  if (channel != "comb") {

    h_true = (TH1F*) h_true_tmp[0]->Clone();
    h_true->SetName(toUnfold+"_genTop");
    if (twoStep == "_2step") {
      h_part = (TH1F*) h_part_tmp[0]->Clone();
      h_part->SetName(toUnfold+"_partTop");
    }

    h_trueMG = (TH1F*) h_trueMG_tmp[0]->Clone();
    h_trueMG->SetName(toUnfold+"_genTop_MG");
    h_trueMCNLO = (TH1F*) h_trueMCNLO_tmp[0]->Clone();
    h_trueMCNLO->SetName(toUnfold+"_genTop_MCNLO");
    if (twoStep == "_2step") {
      h_partMG = (TH1F*) h_partMG_tmp[0]->Clone();
      h_partMG->SetName(toUnfold+"_partTop_MG");
      h_partMCNLO = (TH1F*) h_partMCNLO_tmp[0]->Clone();
      h_partMCNLO->SetName(toUnfold+"_partTop_MCNLO");
    }

    for (int is=0; is<nSYST; is++) {
      h_unfolded[is] = (TH1F*) h_unfolded_tmp[0][is]->Clone();
      h_unfolded[is]->SetName("UnfoldedData"+name_syst[is]);
      if (twoStep == "_2step") {
	h_unfolded_part[is] = (TH1F*) h_unfolded_part_tmp[0][is]->Clone();
	h_unfolded_part[is]->SetName("UnfoldedData_part"+name_syst[is]);
      }
    }

  }
  // ----------------------------------------------------------------------------------------------------------------
  // combination of the channels
  else {

    int nBIN = h_true_tmp[0]->GetNbinsX();

    // first create empty histograms
    h_true = (TH1F*) h_true_tmp[0]->Clone();
    h_true->SetName(toUnfold+"_genTop");
    h_true->Reset();
    if (twoStep == "_2step") {
      h_part = (TH1F*) h_part_tmp[0]->Clone();
      h_part->SetName(toUnfold+"_partTop");
      h_part->Reset();
    }

    h_trueMG = (TH1F*) h_trueMG_tmp[0]->Clone();
    h_trueMG->SetName(toUnfold+"_genTop_MG");
    h_trueMG->Reset();
    h_trueMCNLO = (TH1F*) h_trueMCNLO_tmp[0]->Clone();
    h_trueMCNLO->SetName(toUnfold+"_genTop_MCNLO");
    h_trueMCNLO->Reset();
    if (twoStep == "_2step") {
      h_partMG = (TH1F*) h_partMG_tmp[0]->Clone();
      h_partMG->SetName(toUnfold+"_partTop_MG");
      h_partMG->Reset();
      h_partMCNLO = (TH1F*) h_partMCNLO_tmp[0]->Clone();
      h_partMCNLO->SetName(toUnfold+"_partTop_MCNLO");
      h_partMCNLO->Reset();
    }

    for (int is=0; is<nSYST; is++) {
      h_unfolded[is] = (TH1F*) h_unfolded_tmp[0][is]->Clone();
      h_unfolded[is]->SetName("UnfoldedData"+name_syst[is]);
      h_unfolded[is]->Reset();
      if (twoStep == "_2step") {
	h_unfolded_part[is] = (TH1F*) h_unfolded_part_tmp[0][is]->Clone();
	h_unfolded_part[is]->SetName("UnfoldedData_part"+name_syst[is]);
	h_unfolded_part[is]->Reset();
      }
    }

    
    //then do the combination
    float nel = 0;
    float nmu = 0;
    float ncomb = 0;
    float snel = 0;
    float snmu = 0;
    float sncomb = 0;

    for (int ib=0; ib<nBIN; ib++) {
    
      // h_true
      nel = h_true_tmp[0]->GetBinContent(ib+1);
      nmu = h_true_tmp[1]->GetBinContent(ib+1);
      snel = h_true_tmp[0]->GetBinError(ib+1);
      snmu = h_true_tmp[1]->GetBinError(ib+1);
      if (snel==0 || snmu==0) {
	ncomb = 0;
	sncomb = 0;
      }
      else {
	ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	sncomb = sqrt(sncomb);
      }
      h_true->SetBinContent(ib+1,ncomb);
      h_true->SetBinError(ib+1,sncomb);

      // h_trueMG
      nel = h_trueMG_tmp[0]->GetBinContent(ib+1);
      nmu = h_trueMG_tmp[1]->GetBinContent(ib+1);
      snel = h_trueMG_tmp[0]->GetBinError(ib+1);
      snmu = h_trueMG_tmp[1]->GetBinError(ib+1);
      if (snel==0 || snmu==0) {
	ncomb = 0;
	sncomb = 0;
      }
      else {
	ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	sncomb = sqrt(sncomb);
      }
      h_trueMG->SetBinContent(ib+1,ncomb);
      h_trueMG->SetBinError(ib+1,sncomb);

      // h_trueMCNLO
      nel = h_trueMCNLO_tmp[0]->GetBinContent(ib+1);
      nmu = h_trueMCNLO_tmp[1]->GetBinContent(ib+1);
      snel = h_trueMCNLO_tmp[0]->GetBinError(ib+1);
      snmu = h_trueMCNLO_tmp[1]->GetBinError(ib+1);
      if (snel==0 || snmu==0) {
	ncomb = 0;
	sncomb = 0;
      }
      else {
	ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	sncomb = sqrt(sncomb);
      }
      h_trueMCNLO->SetBinContent(ib+1,ncomb);
      h_trueMCNLO->SetBinError(ib+1,sncomb);

      // h_part
      if (twoStep == "_2step") {
	nel = h_part_tmp[0]->GetBinContent(ib+1);
	nmu = h_part_tmp[1]->GetBinContent(ib+1);
	snel = h_part_tmp[0]->GetBinError(ib+1);
	snmu = h_part_tmp[1]->GetBinError(ib+1);
	if (snel==0 || snmu==0) {
	  ncomb = 0;
	  sncomb = 0;
	}
	else {
	  ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = sqrt(sncomb);
	}
	h_part->SetBinContent(ib+1,ncomb);
	h_part->SetBinError(ib+1,sncomb);

	// MG
	nel = h_partMG_tmp[0]->GetBinContent(ib+1);
	nmu = h_partMG_tmp[1]->GetBinContent(ib+1);
	snel = h_partMG_tmp[0]->GetBinError(ib+1);
	snmu = h_partMG_tmp[1]->GetBinError(ib+1);
	if (snel==0 || snmu==0) {
	  ncomb = 0;
	  sncomb = 0;
	}
	else {
	  ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = sqrt(sncomb);
	}
	h_partMG->SetBinContent(ib+1,ncomb);
	h_partMG->SetBinError(ib+1,sncomb);

	// MC@NLO
	nel = h_partMCNLO_tmp[0]->GetBinContent(ib+1);
	nmu = h_partMCNLO_tmp[1]->GetBinContent(ib+1);
	snel = h_partMCNLO_tmp[0]->GetBinError(ib+1);
	snmu = h_partMCNLO_tmp[1]->GetBinError(ib+1);
	if (snel==0 || snmu==0) {
	  ncomb = 0;
	  sncomb = 0;
	}
	else {
	  ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = sqrt(sncomb);
	}
	h_partMCNLO->SetBinContent(ib+1,ncomb);
	h_partMCNLO->SetBinError(ib+1,sncomb);
      }


      for (int is=0; is<nSYST; is++) {
	// h_unfolded
	nel = h_unfolded_tmp[0][is]->GetBinContent(ib+1);
	nmu = h_unfolded_tmp[1][is]->GetBinContent(ib+1);
	snel = h_unfolded_tmp[0][is]->GetBinError(ib+1);
	snmu = h_unfolded_tmp[1][is]->GetBinError(ib+1);
	if (snel==0 || snmu==0) {
	  ncomb = 0;
	  sncomb = 0;
	}
	else {
	  ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	  sncomb = sqrt(sncomb);
	}
	h_unfolded[is]->SetBinContent(ib+1,ncomb);
	h_unfolded[is]->SetBinError(ib+1,sncomb);

	// h_unfolded_part
	if (twoStep == "_2step") {
	  nel = h_unfolded_part_tmp[0][is]->GetBinContent(ib+1);
	  nmu = h_unfolded_part_tmp[1][is]->GetBinContent(ib+1);
	  snel = h_unfolded_part_tmp[0][is]->GetBinError(ib+1);
	  snmu = h_unfolded_part_tmp[1][is]->GetBinError(ib+1);
	  if (snel==0 || snmu==0) {
	    ncomb = 0;
	    sncomb = 0;
	  }
	  else {
	    ncomb = (nel/(snel*snel) + nmu/(snmu*snmu)) / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	    sncomb = 1.0 / (1.0/(snel*snel) + 1.0/(snmu*snmu));
	    sncomb = sqrt(sncomb);
	  }
	  h_unfolded_part[is]->SetBinContent(ib+1,ncomb);
	  h_unfolded_part[is]->SetBinError(ib+1,sncomb);
	}
	
      }//end loop systematics

    }//end bin loop
  }//end do combination



  TH1F* h_dummy = (TH1F*) h_unfolded[0]->Clone("dummy");
  h_dummy->Reset();
  
  TH1F* h_dummy_r = (TH1F*) h_unfolded[0]->Clone("dummy_r");
  h_dummy_r->Reset();

  TH1F* h_dummy_part = (TH1F*) h_unfolded[0]->Clone("dummy_part");
  h_dummy_part->Reset();
    
  TH1F* h_dummy_r_part = (TH1F*) h_unfolded[0]->Clone("dummy_r_part");
  h_dummy_r_part->Reset();
    
  if (doNormalized) {
    if (toUnfold == "pt"){
      h_dummy->GetYaxis()->SetTitle("1/#sigma d#sigma/dp_{T} (1/GeV)");
      h_dummy->SetAxisRange(0,0.008,"Y");
      h_dummy_part->GetYaxis()->SetTitle("1/#sigma d#sigma/dp_{T} (1/GeV)");
      h_dummy_part->SetAxisRange(0,0.008,"Y");
    }
    else if (toUnfold == "y"){
      h_dummy->GetYaxis()->SetTitle("1/#sigma d#sigma/dy");
      h_dummy->SetAxisRange(0,1,"Y");
      h_dummy_part->GetYaxis()->SetTitle("1/#sigma d#sigma/dy");
      h_dummy_part->SetAxisRange(0,1,"Y");
    }
  }
  else {
    if (toUnfold == "pt"){
      h_dummy->GetYaxis()->SetTitle("d#sigma/dp_{T} (fb/GeV)");
      h_dummy->SetAxisRange(0,12,"Y");
      h_dummy_part->GetYaxis()->SetTitle("d#sigma/dp_{T} (fb/GeV)");
      h_dummy_part->SetAxisRange(0,10,"Y");
    }
    else if (toUnfold == "y"){
      h_dummy->GetYaxis()->SetTitle("d#sigma/dy (fb)");
      h_dummy->SetAxisRange(0,40000,"Y");
      h_dummy_part->GetYaxis()->SetTitle("d#sigma/dy (fb)");
      h_dummy_part->SetAxisRange(0,10000,"Y");
    }
  }


  // ----------------------------------------------------------------------------------------------------------------
  // colors and stuff
  // ----------------------------------------------------------------------------------------------------------------
  
  h_true->SetLineColor(2);
  h_true->SetLineWidth(2);
  h_trueMG->SetLineColor(4);
  h_trueMG->SetLineWidth(2);
  h_trueMG->SetLineStyle(7);
  h_trueMCNLO->SetLineColor(kOrange+1);
  h_trueMCNLO->SetLineWidth(2);
  h_trueMCNLO->SetLineStyle(9);

  h_unfolded[0]->SetLineColor(1);
  h_unfolded[0]->SetLineWidth(2);
  h_unfolded[0]->SetMarkerColor(1);
  h_unfolded[0]->SetMarkerStyle(8);
  

  if (twoStep == "_2step") {
    h_part->SetLineColor(2);
    h_part->SetLineWidth(2);
    h_partMG->SetLineColor(4);
    h_partMG->SetLineWidth(2);
    h_partMG->SetLineStyle(7);
    h_partMCNLO->SetLineColor(kOrange+1);
    h_partMCNLO->SetLineWidth(2);
    h_partMCNLO->SetLineStyle(9);
    
    h_unfolded_part[0]->SetLineColor(1);
    h_unfolded_part[0]->SetLineWidth(2);
    h_unfolded_part[0]->SetMarkerColor(1);
    h_unfolded_part[0]->SetMarkerStyle(8);
  }
  
  float tmp_max = 0;
  
  
  // ----------------------------------------------------------------------------------------------------------------
  // systematics for ratio plot
  // ----------------------------------------------------------------------------------------------------------------

  TH1F* h_stat_up = (TH1F*) h_true->Clone("stat");
  TH1F* h_stat_dn = (TH1F*) h_true->Clone("stat");
  h_stat_up->Reset();
  h_stat_dn->Reset();

  TH1F* h_systEXP_up = (TH1F*) h_true->Clone("syst_up_exp");
  TH1F* h_systEXP_dn = (TH1F*) h_true->Clone("syst_dn_exp");
  h_systEXP_up->Reset();
  h_systEXP_dn->Reset();
  
  TH1F* h_systTH_up = (TH1F*) h_true->Clone("syst_up_th");
  TH1F* h_systTH_dn = (TH1F*) h_true->Clone("syst_dn_th");
  h_systTH_up->Reset();
  h_systTH_dn->Reset();

  TH1F* h_systTOT_up = (TH1F*) h_true->Clone("syst_up_tot");
  TH1F* h_systTOT_dn = (TH1F*) h_true->Clone("syst_dn_tot");
  h_systTOT_up->Reset();
  h_systTOT_dn->Reset();

  // experimental  
  TH1F* h_syst_jec    = (TH1F*) h_true->Clone("syst_jec");
  TH1F* h_syst_jer    = (TH1F*) h_true->Clone("syst_jer");
  TH1F* h_syst_btag   = (TH1F*) h_true->Clone("syst_btag");
  TH1F* h_syst_toptag = (TH1F*) h_true->Clone("syst_toptag");
  TH1F* h_syst_toptagHIGHPT = (TH1F*) h_true->Clone("syst_toptagHIGHPT");
  TH1F* h_syst_bkg    = (TH1F*) h_true->Clone("syst_bkg");
  // statistics
  TH1F* h_syst_stat   = (TH1F*) h_true->Clone("syst_stat");
  // theory
  TH1F* h_syst_pdf    = (TH1F*) h_true->Clone("syst_pdf");
  TH1F* h_syst_Q2     = (TH1F*) h_true->Clone("syst_Q2");
  TH1F* h_syst_PS     = (TH1F*) h_true->Clone("syst_PS");

  TH1F* h_lumi    = (TH1F*) h_true->Clone("lumi");

  TH1F* h_syst_tot = (TH1F*) h_true->Clone("syst_tot");
  
  h_syst_jec->Reset();   
  h_syst_jer->Reset(); 
  h_syst_btag->Reset();   
  h_syst_toptag->Reset(); 
  h_syst_toptagHIGHPT->Reset(); 
  h_syst_bkg->Reset(); 
  h_syst_stat->Reset(); 
  h_syst_tot->Reset(); 
  h_syst_pdf->Reset();
  h_syst_Q2->Reset(); 
  h_syst_PS->Reset();
  h_lumi->Reset();
  
  
  float count[nSYST] = {0};
  float sig[nSYST] = {0};

  float xsec_meas = 0;
  float xsec_true = 0;


  // ----------------------------------------------------------------------------------------------------------------
  // loop over bins
  // ----------------------------------------------------------------------------------------------------------------

  cout << endl << "*** unfolding result (parton-level) for " << channel << " channel ***" << endl;

  for (int i=0; i<h_unfolded[0]->GetNbinsX(); i++) {
    
    for (int is=0; is<nSYST; is++) {
      count[is] = h_unfolded[is]->GetBinContent(i+1);
      sig[is]   = h_unfolded[is]->GetBinError(i+1);
    }
    float truth = h_true->GetBinContent(i+1);
    float this_syst_PS = fabs(count[17]-truth)/truth*count[0];

    float this_lumi = 0.026 * count[0];
    
    // experimental
    float this_systEXP_up = 0;
    this_systEXP_up += (count[1]-count[0])*(count[1]-count[0]); //jec
    this_systEXP_up += (count[3]-count[0])*(count[3]-count[0]); //jer
    this_systEXP_up += (count[5]-count[0])*(count[5]-count[0]); //btag
    this_systEXP_up += (count[7]-count[0])*(count[7]-count[0]); //toptag
    this_systEXP_up += (count[9]-count[0])*(count[9]-count[0]); //background normalizations
    this_systEXP_up += (count[15]-count[0])*(count[15]-count[0]); //toptag highpt
    this_systEXP_up = sqrt(this_systEXP_up);
    
    float this_systEXP_dn = 0;
    this_systEXP_dn += (count[2]-count[0])*(count[2]-count[0]);
    this_systEXP_dn += (count[4]-count[0])*(count[4]-count[0]);
    this_systEXP_dn += (count[6]-count[0])*(count[6]-count[0]);
    this_systEXP_dn += (count[8]-count[0])*(count[8]-count[0]);
    this_systEXP_dn += (count[10]-count[0])*(count[10]-count[0]);
    this_systEXP_dn += (count[16]-count[0])*(count[16]-count[0]);
    this_systEXP_dn = sqrt(this_systEXP_dn);
    
    // theory
    float this_systTH_up = 0;
    this_systTH_up += (count[11]-count[0])*(count[11]-count[0]); //pdf
    if (doQ2) this_systTH_up += (count[13]-count[0])*(count[13]-count[0]); //q2
    this_systTH_up += this_syst_PS*this_syst_PS; //PS
    this_systTH_up = sqrt(this_systTH_up);
    
    float this_systTH_dn = 0;
    this_systTH_dn += (count[12]-count[0])*(count[12]-count[0]);
    if (doQ2) this_systTH_dn += (count[14]-count[0])*(count[14]-count[0]);
    this_systTH_dn += this_syst_PS*this_syst_PS; //PS
    this_systTH_dn = sqrt(this_systTH_dn);

    // theory + experimental + statistical (+ lumi)
    float this_systTOT_up = this_systEXP_up*this_systEXP_up + this_systTH_up*this_systTH_up + sig[0]*sig[0];
    if (doNormalized == false) this_systTOT_up += this_lumi*this_lumi;
    this_systTOT_up = sqrt(this_systTOT_up);
    float this_systTOT_dn = this_systEXP_dn*this_systEXP_dn + this_systTH_dn*this_systTH_dn + sig[0]*sig[0];
    if (doNormalized == false) this_systTOT_dn += this_lumi*this_lumi;
    this_systTOT_dn = sqrt(this_systTOT_dn);
    

    // fill histograms for ratio plot
    h_stat_up->SetBinContent(i+1,count[0]+sig[0]);
    h_stat_dn->SetBinContent(i+1,count[0]-sig[0]);
    
    cout << "DEBUG: central value in bin " << i << " is " << count[0] << endl;
    cout << "DEBUG: stat error in bin " << i << " is " << sig[0] << endl;
    
    if (doAverageErr) {
      h_systEXP_up->SetBinContent(i+1,count[0]+(this_systEXP_up+this_systEXP_dn)/2);
      h_systEXP_dn->SetBinContent(i+1,count[0]-(this_systEXP_up+this_systEXP_dn)/2);   
      h_systTH_up->SetBinContent(i+1,count[0]+(this_systTH_up+this_systTH_dn)/2);
      h_systTH_dn->SetBinContent(i+1,count[0]-(this_systTH_up+this_systTH_dn)/2);  
      h_systTOT_up->SetBinContent(i+1,count[0]+(this_systTOT_up+this_systTOT_dn)/2);
      h_systTOT_dn->SetBinContent(i+1,count[0]-(this_systTOT_up+this_systTOT_dn)/2);  
    }
    else {
      h_systEXP_up->SetBinContent(i+1,count[0]+this_systEXP_up);
      h_systEXP_dn->SetBinContent(i+1,count[0]-this_systEXP_dn);   
      h_systTH_up->SetBinContent(i+1,count[0]+this_systTH_up);
      h_systTH_dn->SetBinContent(i+1,count[0]-this_systTH_dn);  
      h_systTOT_up->SetBinContent(i+1,count[0]+this_systTOT_up);
      h_systTOT_dn->SetBinContent(i+1,count[0]-this_systTOT_dn);  
    }

    // histograms for uncertainty plots
    // experimental
    double syst_jecup   = fabs((count[1]-count[0])/count[0])*100;
    double syst_jecdn   = fabs((count[2]-count[0])/count[0])*100;
    double syst_jerup   = fabs((count[3]-count[0])/count[0])*100;
    double syst_jerdn   = fabs((count[4]-count[0])/count[0])*100;
    double syst_btagup   = fabs((count[5]-count[0])/count[0])*100;
    double syst_btagdn   = fabs((count[6]-count[0])/count[0])*100;
    double syst_toptagup = fabs((count[7]-count[0])/count[0])*100;
    double syst_toptagdn = fabs((count[8]-count[0])/count[0])*100;
    double syst_toptagHIGHPTup = fabs((count[15]-count[0])/count[0])*100;
    double syst_toptagHIGHPTdn = fabs((count[16]-count[0])/count[0])*100;
    double syst_bkgup   = fabs((count[9]-count[0])/count[0])*100;
    double syst_bkgdn   = fabs((count[10]-count[0])/count[0])*100;
    // statistics    
    double syst_stat   = sig[0]/count[0]*100;
    // theoretical
    double syst_pdfup   = fabs((count[11]-count[0])/count[0])*100;
    double syst_pdfdn   = fabs((count[12]-count[0])/count[0])*100;
    double syst_scaleup = fabs((count[13]-count[0])/count[0])*100;
    double syst_scaledn = fabs((count[14]-count[0])/count[0])*100;
    // parton shower
    double syst_PS = this_syst_PS/count[0]*100;

    double max_syst_jec = 0;
    double max_syst_jer = 0;
    double max_syst_btag = 0;
    double max_syst_toptag = 0;
    double max_syst_toptagNOM = 0;
    double max_syst_toptagHIGHPT = 0;
    double max_syst_bkg = 0;
    double max_syst_pdf = 0;
    double max_syst_Q2  = 0;

    if (doAverageErr) {
      max_syst_jec = (syst_jecup+syst_jecdn)/2;
      max_syst_jer = (syst_jerup+syst_jerdn)/2;
      max_syst_btag = (syst_btagup+syst_btagdn)/2;
      max_syst_toptagNOM = (syst_toptagup+syst_toptagdn)/2;
      max_syst_toptagHIGHPT = (syst_toptagHIGHPTup+syst_toptagHIGHPTdn)/2;
      max_syst_bkg = (syst_bkgup+syst_bkgdn)/2;
      max_syst_pdf = (syst_pdfup+syst_pdfdn)/2;
      max_syst_Q2  = (syst_scaleup+syst_scaledn)/2;
    }
    else {
      max_syst_jec = max(syst_jecup,syst_jecdn);
      max_syst_jer = max(syst_jerup,syst_jerdn);
      max_syst_btag = max(syst_btagup,syst_btagdn);
      max_syst_toptagNOM = max(syst_toptagup,syst_toptagdn);
      max_syst_toptagHIGHPT = max(syst_toptagHIGHPTup,syst_toptagHIGHPTdn);
      max_syst_bkg = max(syst_bkgup,syst_bkgdn);
      max_syst_pdf = max(syst_pdfup,syst_pdfdn);
      max_syst_Q2  = max(syst_scaleup,syst_scaledn);
    }

    max_syst_toptag = sqrt(max_syst_toptagNOM*max_syst_toptagNOM + max_syst_toptagHIGHPT*max_syst_toptagHIGHPT);

    if (!doQ2) {
      syst_scaleup = 0;
      syst_scaledn = 0;
      max_syst_Q2 = 0;
    }

    double syst_totalEXP_up = sqrt(syst_jecup*syst_jecup + syst_jerup*syst_jerup + syst_btagup*syst_btagup + 
				   syst_toptagup*syst_toptagup + syst_toptagHIGHPTup*syst_toptagHIGHPTup + syst_bkgup*syst_bkgup);
    double syst_totalEXP_dn = sqrt(syst_jecdn*syst_jecdn + syst_jerdn*syst_jerdn + syst_btagdn*syst_btagdn + 
				   syst_toptagdn*syst_toptagdn + syst_toptagHIGHPTdn*syst_toptagHIGHPTdn + syst_bkgdn*syst_bkgdn);
    double syst_totalTH_up = sqrt(syst_scaleup*syst_scaleup + syst_pdfup*syst_pdfup + syst_PS*syst_PS);
    double syst_totalTH_dn = sqrt(syst_scaledn*syst_scaledn + syst_pdfdn*syst_pdfdn + syst_PS*syst_PS);
    double syst_total_up = sqrt(syst_totalEXP_up*syst_totalEXP_up + syst_totalTH_up*syst_totalTH_up);
    double syst_total_dn = sqrt(syst_totalEXP_dn*syst_totalEXP_dn + syst_totalTH_dn*syst_totalTH_dn);

    double syst_totaltotal_up = sqrt(syst_total_up*syst_total_up + syst_stat*syst_stat);
    double syst_totaltotal_dn = sqrt(syst_total_dn*syst_total_dn + syst_stat*syst_stat);

    // Add lumi uncertainty
    if (doNormalized == false) syst_totaltotal_up = sqrt(syst_totaltotal_up*syst_totaltotal_up+2.6*2.6);
    if (doNormalized == false) syst_totaltotal_dn = sqrt(syst_totaltotal_dn*syst_totaltotal_dn+2.6*2.6);
    
    double max_syst_totalEXP = 0;
    double max_syst_totalTH = 0;
    double max_syst_total = 0;
    double max_syst_totaltotal = 0;

    if (doAverageErr) {
      max_syst_totalEXP = (syst_totalEXP_up+syst_totalEXP_dn)/2;
      max_syst_totalTH = (syst_totalTH_up+syst_totalTH_dn)/2;
      max_syst_total = (syst_total_up+syst_total_dn)/2;
      max_syst_totaltotal = (syst_totaltotal_up+syst_totaltotal_dn)/2;
    }
    else {
      max_syst_totalEXP = max(syst_totalEXP_up,syst_totalEXP_dn);
      max_syst_totalTH = max(syst_totalTH_up,syst_totalTH_dn);
      max_syst_total = max(syst_total_up,syst_total_dn);
      max_syst_totaltotal = max(syst_totaltotal_up,syst_totaltotal_dn);
    }

    h_syst_jec->SetBinContent(i+1,max_syst_jec);    
    h_syst_jer->SetBinContent(i+1,max_syst_jer);    
    h_syst_btag->SetBinContent(i+1,max_syst_btag);   
    h_syst_toptag->SetBinContent(i+1,max_syst_toptag); 
    h_syst_bkg->SetBinContent(i+1,max_syst_bkg); 
    h_syst_stat->SetBinContent(i+1,syst_stat);  
    h_syst_pdf->SetBinContent(i+1,max_syst_pdf);
    h_syst_Q2->SetBinContent(i+1,max_syst_Q2);  
    h_syst_PS->SetBinContent(i+1,syst_PS);  
    h_syst_tot->SetBinContent(i+1,max_syst_total);
    if (doNormalized == false) h_lumi->SetBinContent(i+1,2.6);
    
    h_syst_jec->SetBinError(i+1,0.001);
    h_syst_jer->SetBinError(i+1,0.001);
    h_syst_btag->SetBinError(i+1,0.001);
    h_syst_toptag->SetBinError(i+1,0.001);
    h_syst_bkg->SetBinError(i+1,0.001);
    h_syst_stat->SetBinError(i+1,0.001);
    h_syst_pdf->SetBinError(i+1,0.001);
    h_syst_Q2->SetBinError(i+1,0.001);  
    h_syst_PS->SetBinError(i+1,0.001);  
    h_syst_tot->SetBinError(i+1,0.001);
    if (doNormalized == false) h_lumi->SetBinError(i+1,0.001);


    // ----------------------------------------------------------------------------------------------------------------
    // print outs for cross-section table
    // ----------------------------------------------------------------------------------------------------------------

    int ibin1 = h_systEXP_up->GetBin(i+1);
    int ibin2 = h_systEXP_up->GetBin(i+2);
    int lowedge = h_systEXP_up->GetBinLowEdge(ibin1);
    int highedge = h_systEXP_up->GetBinLowEdge(ibin2);

    if (toUnfold == "pt"){

      if (lowedge > 300 && highedge < 1300) {
	cout << (float)lowedge << "--" << (float)highedge << " & " << count[0] << " & " << syst_stat << " & " 
	     << max_syst_totalEXP << " & " << max_syst_totalTH << " & " << max_syst_totaltotal << " & " 
	     << h_true->GetBinContent(i+1) << " & " 
	     << h_trueMG->GetBinContent(i+1) << " & " 
	     << h_trueMCNLO->GetBinContent(i+1) << endl;
      }
      
      if (lowedge > 300.) {
	xsec_meas += count[0]*h_true->GetBinWidth(i+1);
	xsec_true += h_true->GetBinContent(i+1)*h_true->GetBinWidth(i+1);
      }
   
      cout << "TOTAL cross section (parton level), measured = " << xsec_meas << " true = " << xsec_true << endl;
    }
  }


  // ----------------------------------------------------------------------------------------------------------------
  // RATIO PLOTS !!!!!!!
  // ----------------------------------------------------------------------------------------------------------------
  
  Float_t f_textSize=0.057;
  gStyle->SetPadLeftMargin(0.12);
  gStyle->SetPadRightMargin(0.1);
  gStyle->SetTextSize(f_textSize);
  gStyle->SetLabelSize(f_textSize,"x");
  gStyle->SetTitleSize(f_textSize,"x");
  gStyle->SetLabelSize(f_textSize,"y");
  gStyle->SetTitleSize(f_textSize,"y");
  gStyle->SetOptStat(0);
 

  TH1F* h_fullunc = (TH1F*) h_unfolded[0]->Clone("fullunc");

  for (int ib=0; ib<h_fullunc->GetNbinsX(); ib++) {
    if (h_fullunc->GetBinContent(ib+1) > 0) {
      float up = h_systTOT_up->GetBinContent(ib+1);
      float dn = h_systTOT_dn->GetBinContent(ib+1);
      h_fullunc->SetBinError(ib+1,(up-dn)/2);
    }
  }

  gStyle->SetEndErrorSize(5);

  TCanvas *c = new TCanvas("c", "", 700, 625);
  
  float ratio_size = 0.35;
  
  TPad* p1 = new TPad("p1","p1",0,ratio_size+0.0,1,1);
  p1->SetBottomMargin(0.01);
  p1->SetTopMargin(0.10);
  p1->SetLeftMargin(0.16);
  p1->SetRightMargin(0.075);
  
  TPad* p2 = new TPad("p2","p2",0,0,1,ratio_size-0.0);
  p2->SetTopMargin(0.06);
  p2->SetBottomMargin(0.34);
  p2->SetLeftMargin(0.16);
  p2->SetRightMargin(0.075);
  
  p1->Draw();
  p2->Draw();
    
  p1->cd();

  if (doLogscale && doNormalized) {
    h_dummy->SetAxisRange(0.000015,0.015,"Y");
    h_true->SetAxisRange(0.000015,0.015,"Y");
    h_trueMG->SetAxisRange(0.000015,0.015,"Y");
    h_trueMCNLO->SetAxisRange(0.000015,0.015,"Y");
    h_unfolded[0]->SetAxisRange(0.000015,0.015,"Y");
    h_fullunc->SetAxisRange(0.000015,0.015,"Y");
    gPad->SetLogy();
  }
  else if (doLogscale) {
    if (toUnfold == "y") {
      h_dummy->SetAxisRange(500,50000,"Y");
      h_true->SetAxisRange(500,50000,"Y");
      h_trueMG->SetAxisRange(500,50000,"Y");
      h_trueMCNLO->SetAxisRange(500,50000,"Y");
      h_unfolded[0]->SetAxisRange(500,50000,"Y");
      h_fullunc->SetAxisRange(500,50000,"Y");
      gPad->SetLogy();
    }
    else {
      h_dummy->SetAxisRange(0.015,30,"Y");
      h_true->SetAxisRange(0.015,30,"Y");
      h_trueMG->SetAxisRange(0.015,30,"Y");
      h_trueMCNLO->SetAxisRange(0.015,30,"Y");
      h_unfolded[0]->SetAxisRange(0.015,30,"Y");
      h_fullunc->SetAxisRange(0.015,30,"Y");
      gPad->SetLogy();
    }
  }

  h_dummy->GetYaxis()->SetTitleSize(0.075);    
  if (doLogscale) h_dummy->GetYaxis()->SetTitleOffset(0.8);
  else h_dummy->GetYaxis()->SetTitleOffset(1.1);
  h_dummy->GetYaxis()->SetLabelSize(0.065);
  h_dummy->GetXaxis()->SetTitleSize(0);
  h_dummy->GetXaxis()->SetLabelSize(0);

  h_dummy->Draw("hist");
  h_true->Draw("hist,same");
  h_trueMG->Draw("hist,same");  
  h_trueMCNLO->Draw("hist,same");  
  TExec *setex1 = new TExec("setex1","gStyle->SetErrorX(0)");
  setex1->Draw();
  h_fullunc->Draw("hist,ep,same");
  h_unfolded[0]->Draw("hist,E1p,same");
  TExec *setex2 = new TExec("setex2","gStyle->SetErrorX(0.5)");
  setex2->Draw();
  h_dummy->Draw("hist,axis,same"); 

  
  // ----------------------------------------------------------------------------------------------------------------
  // making ratio part of plot
  // ----------------------------------------------------------------------------------------------------------------
  
  TString baselab = h_unfolded[0]->GetName();
  TH1F* h_ratio = (TH1F*) h_unfolded[0]->Clone(baselab+"_ratio");

  TH1F* h_ratioSTAT_up = (TH1F*) h_stat_up->Clone(baselab+"_ratioSTAT_up");
  TH1F* h_ratioSTAT_dn = (TH1F*) h_stat_dn->Clone(baselab+"_ratioSTAT_dn");

  TH1F* h_ratioEXP_up = (TH1F*) h_systEXP_up->Clone(baselab+"_ratioEXP_up");
  TH1F* h_ratioEXP_dn = (TH1F*) h_systEXP_dn->Clone(baselab+"_ratioEXP_dn");
  
  TH1F* h_ratioTOT_up = (TH1F*) h_systTOT_up->Clone(baselab+"_ratioTOT_up");
  TH1F* h_ratioTOT_dn = (TH1F*) h_systTOT_dn->Clone(baselab+"_ratioTOT_dn");

  TH1F* h_ratioTH_up = (TH1F*) h_systTH_up->Clone(baselab+"_ratioTH_up");
  TH1F* h_ratioTH_dn = (TH1F*) h_systTH_dn->Clone(baselab+"_ratioTH_dn");

  TH1F* h_ratioGEN = (TH1F*) h_true->Clone(baselab+"_ratioGEN");
  TH1F* h_ratioMG = (TH1F*) h_trueMG->Clone(baselab+"_ratioMG");
  TH1F* h_ratioMCNLO = (TH1F*) h_trueMCNLO->Clone(baselab+"_ratioMCNLO");

  h_ratio->Divide(h_unfolded[0]);
  h_ratioSTAT_up->Divide(h_unfolded[0]);
  h_ratioSTAT_dn->Divide(h_unfolded[0]);
  h_ratioEXP_up->Divide(h_unfolded[0]);
  h_ratioEXP_dn->Divide(h_unfolded[0]);
  h_ratioTH_up->Divide(h_unfolded[0]);
  h_ratioTH_dn->Divide(h_unfolded[0]);
  h_ratioTOT_up->Divide(h_unfolded[0]);
  h_ratioTOT_dn->Divide(h_unfolded[0]);
  h_ratioGEN->Divide(h_unfolded[0]);
  h_ratioMG->Divide(h_unfolded[0]);
  h_ratioMCNLO->Divide(h_unfolded[0]);

  
  // ----------------------------------------------------------------------------------------------------------------
  TH1F* blaSTAT = (TH1F*) h_ratioSTAT_up->Clone("blaSTAT");
  blaSTAT->Reset();
  for (int i=0; i<blaSTAT->GetNbinsX(); i++) {
    float up = h_ratioSTAT_up->GetBinContent(i+1);
    float dn = h_ratioSTAT_dn->GetBinContent(i+1);
    
    blaSTAT->SetBinContent(i+1,(up-dn)/2+dn);
    blaSTAT->SetBinError(i+1,(up-dn)/2);
  }
  
  TH1F* blaEXP = (TH1F*) h_ratioEXP_up->Clone("blaEXP");
  blaEXP->Reset();
  for (int i=0; i<blaEXP->GetNbinsX(); i++) {
    float up = h_ratioEXP_up->GetBinContent(i+1);
    float dn = h_ratioEXP_dn->GetBinContent(i+1);
    
    blaEXP->SetBinContent(i+1,(up-dn)/2+dn);
    blaEXP->SetBinError(i+1,(up-dn)/2);
  }
  
  TH1F* blaTH = (TH1F*) h_ratioTH_up->Clone("blaTOT");
  blaTH->Reset();
  for (int i=0; i<blaTH->GetNbinsX(); i++) {
    float up = h_ratioTH_up->GetBinContent(i+1);
    float dn = h_ratioTH_dn->GetBinContent(i+1);
    
    blaTH->SetBinContent(i+1,(up-dn)/2+dn);
    blaTH->SetBinError(i+1,(up-dn)/2);
  }

  TH1F* blaTOT = (TH1F*) h_ratioTOT_up->Clone("blaTOT");
  blaTOT->Reset();
  for (int i=0; i<blaTOT->GetNbinsX(); i++) {
    float up = h_ratioTOT_up->GetBinContent(i+1);
    float dn = h_ratioTOT_dn->GetBinContent(i+1);
    
    blaTOT->SetBinContent(i+1,(up-dn)/2+dn);
    blaTOT->SetBinError(i+1,(up-dn)/2);
  }
  
  //blaSTAT->SetLineColor(1);
  //blaSTAT->SetLineWidth(1);
  blaSTAT->SetMarkerSize(0);
  blaSTAT->SetLineColor(0);
  blaSTAT->SetLineWidth(0);
  blaSTAT->SetFillColor(18);
  blaSTAT->SetFillStyle(1001);

  blaEXP->SetMarkerSize(0);
  blaEXP->SetLineColor(0);
  blaEXP->SetFillColor(kAzure);
  blaEXP->SetFillStyle(1001);

  blaTH->SetMarkerSize(0);
  blaTH->SetLineColor(0);
  blaTH->SetFillColor(kBlue);
  blaTH->SetFillStyle(3453);

  blaTOT->SetMarkerSize(0);
  blaTOT->SetLineColor(0);
  blaTOT->SetFillColor(kAzure-9);
  blaTOT->SetFillStyle(1001);
  

  // ----------------------------------------------------------------------------------------------------------------
  double legx = 0.52;
  double legy = 0.4;
  if (toUnfold == "y"){
    legx = 0.35;
    legy = 0.08;
  }
  
  TLegend* leg = new TLegend(legx,legy,legx+0.33,legy+0.35);  
  leg->AddEntry(h_unfolded[0],"Data","pe1");
  leg->AddEntry(h_true,"Powheg+Pythia6 t#bar{t}","l");
  leg->AddEntry(h_trueMG,"MadGraph+Pythia6 t#bar{t}","l");
  leg->AddEntry(h_trueMCNLO,"MC@NLO+Herwig6 t#bar{t}","l");
  //leg->AddEntry(blaEXP,"Experimental uncertainty","f");
  //leg->AddEntry(blaTH,"Theory uncertainty","f");
  //leg->AddEntry(blaTOT,"Stat. #oplus exp. #oplus theory","f");
  leg->AddEntry(blaSTAT,"Stat. Uncertainty","f");
  if (doNormalized) leg->AddEntry(blaTOT,"Stat. #oplus Syst.","f");
  else leg->AddEntry(blaTOT,"Stat. #oplus Syst. #oplus Lumi","f");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.055);
  leg->SetTextFont(42);
  leg->Draw();

  drawCMS(0.53,0.8,true,true,forpub);


  // ----------------------------------------------------------------------------------------------------------------

  p2->cd();
  p2->SetGridy();

  h_ratio->GetXaxis()->SetTitleSize(0.14);
  h_ratio->GetYaxis()->SetTitleSize(0.14);
  h_ratio->GetXaxis()->SetLabelSize(0.12);
  h_ratio->GetYaxis()->SetLabelSize(0.1);

  h_ratio->GetYaxis()->SetTitle("Theory/Data");
  if (toUnfold == "pt") h_ratio->GetXaxis()->SetTitle("Top quark p_{T} (GeV)");
  else if (toUnfold == "y") h_ratio->GetXaxis()->SetTitle("Top quark rapidity");
  h_ratio->GetYaxis()->SetTitleOffset(0.8);
  h_ratio->GetYaxis()->SetNdivisions(505);
  //h_ratio->GetYaxis()->SetNdivisions(510);
  h_ratio->GetYaxis()->SetTitleOffset(0.38);
  h_ratio->GetXaxis()->SetTitleOffset(1.0);

  if (toUnfold == "y"){
    h_ratio->SetAxisRange(0.3,1.7,"Y");
    h_ratioGEN->SetAxisRange(0.3,1.7,"Y");
    h_ratioMG->SetAxisRange(0.3,1.7,"Y");
    h_ratioMCNLO->SetAxisRange(0.3,1.7,"Y");
  }  
  else if (doNormalized) {
    h_ratio->SetAxisRange(0.6,1.4,"Y");
    h_ratioGEN->SetAxisRange(0.6,1.4,"Y");
    h_ratioMG->SetAxisRange(0.6,1.4,"Y");
    h_ratioMCNLO->SetAxisRange(0.6,1.4,"Y");
  }
  else {
    h_ratio->SetAxisRange(0.3,1.7,"Y");
    h_ratioGEN->SetAxisRange(0.3,1.7,"Y");
    h_ratioMG->SetAxisRange(0.3,1.7,"Y");
    h_ratioMCNLO->SetAxisRange(0.3,1.7,"Y");
  }
  h_ratio->Draw("hist");
  blaTOT->Draw("same,e2");
  //blaEXP->Draw("same,e2");
  //blaTH->Draw("same,e2");
  //blaSTAT->Draw("same,ep");
  
  blaSTAT->Draw("same,e2");
  h_ratioGEN->Draw("same,hist");
  h_ratioMG->Draw("same,hist");
  h_ratioMCNLO->Draw("same,hist");
  //blaSTAT->Draw("same,ep");
  h_ratio->Draw("same,hist");
  h_ratio->Draw("same,axis");
  
  c->SaveAs("UnfoldingPlots/unfoldWithError_"+toUnfold+"_"+channel+twoStep+nobtag+".png");
  c->SaveAs("UnfoldingPlots/unfoldWithError_"+toUnfold+"_"+channel+twoStep+nobtag+".eps");
  c->SaveAs("UnfoldingPlots/unfoldWithError_"+toUnfold+"_"+channel+twoStep+nobtag+".pdf");


  
  TCanvas *c1 = new TCanvas("c1", "", 800, 600);
  c1->SetTopMargin(0.08);
  c1->SetRightMargin(0.05);
  c1->SetBottomMargin(0.14);
  c1->SetLeftMargin(0.16);
  

  if (toUnfold == "pt") h_dummy_r->GetXaxis()->SetTitle("Top quark p_{T} (GeV)");
  else if (toUnfold == "y") h_dummy_r->GetXaxis()->SetTitle("Top quark rapidity");
  h_dummy_r->GetYaxis()->SetTitle("Uncertainty [%]");
  if (toUnfold == "pt") h_dummy_r->SetAxisRange(400,1150,"X");
  if (toUnfold == "y") h_dummy_r->SetAxisRange(0,100,"Y");
  if (doQ2 && channel == "comb" && doNormalized) h_dummy_r->SetAxisRange(0,40,"Y");
  else if (doQ2) h_dummy_r->SetAxisRange(0,70,"Y");
  else h_dummy_r->SetAxisRange(0,25,"Y");
  
  h_dummy_r->GetYaxis()->SetTitleSize(0.055);    
  h_dummy_r->GetYaxis()->SetTitleOffset(1.1);
  h_dummy_r->GetYaxis()->SetLabelSize(0.045);
  
  h_dummy_r->GetXaxis()->SetTitleSize(0.05);
  h_dummy_r->GetXaxis()->SetTitleOffset(1.2);
  h_dummy_r->GetXaxis()->SetLabelSize(0.0455);
  
  c1->cd();


  h_syst_tot->SetFillColor(17);
  h_syst_tot->SetFillStyle(3344);
  h_syst_tot->SetLineColor(16);
  h_syst_tot->SetLineWidth(2);

  h_syst_stat->SetLineColor(1);
  h_syst_stat->SetLineWidth(2);
  h_syst_stat->SetMarkerColor(1);
  h_syst_stat->SetMarkerStyle(20);

  h_syst_jec->SetLineColor(4);
  h_syst_jec->SetLineWidth(2);
  h_syst_jec->SetMarkerColor(4);
  h_syst_jec->SetMarkerStyle(21);
  
  h_syst_jer->SetLineColor(8);
  h_syst_jer->SetLineWidth(2);
  h_syst_jer->SetMarkerColor(8);
  h_syst_jer->SetMarkerStyle(22);
  
  h_syst_toptag->SetLineColor(2);
  h_syst_toptag->SetLineWidth(2);
  h_syst_toptag->SetMarkerColor(2);
  h_syst_toptag->SetMarkerStyle(23);

  h_syst_btag->SetLineColor(1);
  h_syst_btag->SetLineWidth(2);
  h_syst_btag->SetMarkerColor(1);
  h_syst_btag->SetMarkerStyle(24);  

  h_syst_bkg->SetLineColor(kOrange+1);
  h_syst_bkg->SetLineWidth(2);
  h_syst_bkg->SetMarkerColor(kOrange+1);
  h_syst_bkg->SetMarkerStyle(26);

  h_syst_pdf->SetLineColor(6);
  h_syst_pdf->SetLineWidth(2);
  h_syst_pdf->SetMarkerColor(6);
  h_syst_pdf->SetMarkerStyle(25);

  h_syst_Q2->SetLineColor(kAzure+10);
  h_syst_Q2->SetLineWidth(2);
  h_syst_Q2->SetMarkerColor(kAzure+10);
  h_syst_Q2->SetMarkerStyle(24);
  
  h_syst_PS->SetLineColor(12);
  h_syst_PS->SetLineStyle(7);
  h_syst_PS->SetLineWidth(2);
  h_syst_PS->SetMarkerColor(12);
  h_syst_PS->SetMarkerStyle(32);

  if (doNormalized == false){
    h_lumi->SetLineColor(40);
    h_lumi->SetLineWidth(2);
    h_lumi->SetMarkerColor(40);
    h_lumi->SetMarkerStyle(20);
  }
  
  TLegend* leg2 = new TLegend(0.6,0.54,0.85,0.88);  
  leg2->AddEntry(h_syst_tot,"Total syst. uncertainty","f");
  leg2->AddEntry(h_syst_stat,"Statistical uncertainty","lp");
  if (doNormalized == false) leg2->AddEntry(h_lumi,"Luminosity uncertainty","lp");
  leg2->AddEntry(h_syst_jec,"Jet energy scale","lp");
  leg2->AddEntry(h_syst_jer,"Jet energy resolution","lp");
  leg2->AddEntry(h_syst_toptag,"Top-tagging efficiency","lp");
  if (nobtag == "") leg2->AddEntry(h_syst_btag,"b-tagging efficiency","lp");
  leg2->AddEntry(h_syst_bkg,"Background normalization","lp");
  leg2->AddEntry(h_syst_pdf,"PDF uncertainty","lp");
  if (doQ2) leg2->AddEntry(h_syst_Q2,"Q^{2} scale","lp");
  leg2->AddEntry(h_syst_PS,"Generator+PS","lp");
  leg2->SetFillStyle(0);
  leg2->SetBorderSize(0);
  leg2->SetTextSize(0.032);
  leg2->SetTextFont(42);

  
  h_dummy_r->Draw("hist");
  h_syst_tot->Draw("hist,same");
  h_syst_stat->Draw("ep,same");
  if (doNormalized == false) h_lumi->Draw("ep,same");
  h_syst_jec->Draw("ep,same");
  h_syst_jer->Draw("ep,same");
  h_syst_toptag->Draw("ep,same");
  if (nobtag == "") h_syst_btag->Draw("ep,same");
  h_syst_bkg->Draw("ep,same");
  if (doQ2) h_syst_Q2->Draw("ep,same");
  h_syst_pdf->Draw("ep,same");
  h_syst_PS->Draw("ep,same");
  h_dummy_r->Draw("hist,axis,same");
  leg2->Draw(); 

  drawCMS(0.2,0.84,false,true,forpub);

  c1->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_"+toUnfold+"_"+channel+twoStep+nobtag+".png");
  c1->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_"+toUnfold+"_"+channel+twoStep+nobtag+".pdf");
  c1->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_"+toUnfold+"_"+channel+twoStep+nobtag+".eps");


  // -----------------------------------------------------------
  // Now do particle-level...
  // -----------------------------------------------------------

  if (twoStep == "_2step") {

    // ----------------------------------------------------------------------------------------------------------------
    // systematics for ratio plot
    
    TH1F* h_stat_up_part = (TH1F*) h_true->Clone("stat_part");
    TH1F* h_stat_dn_part = (TH1F*) h_true->Clone("stat_part");
    h_stat_up_part->Reset();
    h_stat_dn_part->Reset();
    
    TH1F* h_systEXP_up_part = (TH1F*) h_true->Clone("syst_up_exp_part");
    TH1F* h_systEXP_dn_part = (TH1F*) h_true->Clone("syst_dn_exp_part");
    h_systEXP_up_part->Reset();
    h_systEXP_dn_part->Reset();
    
    TH1F* h_systTH_up_part = (TH1F*) h_true->Clone("syst_up_th_part");
    TH1F* h_systTH_dn_part = (TH1F*) h_true->Clone("syst_dn_th_part");
    h_systTH_up_part->Reset();
    h_systTH_dn_part->Reset();
    
    TH1F* h_systTOT_up_part = (TH1F*) h_true->Clone("syst_up_tot_part");
    TH1F* h_systTOT_dn_part = (TH1F*) h_true->Clone("syst_dn_tot_part");
    h_systTOT_up_part->Reset();
    h_systTOT_dn_part->Reset();

    
    TH1F* h_syst_jec_part    = (TH1F*) h_true->Clone("syst_jec_part");
    TH1F* h_syst_jer_part    = (TH1F*) h_true->Clone("syst_jer_part");
    TH1F* h_syst_btag_part   = (TH1F*) h_true->Clone("syst_btag_part");
    TH1F* h_syst_toptag_part = (TH1F*) h_true->Clone("syst_toptag_part");
    TH1F* h_syst_bkg_part    = (TH1F*) h_true->Clone("syst_bkg_part");
    TH1F* h_syst_stat_part   = (TH1F*) h_true->Clone("syst_stat_part");
    TH1F* h_syst_pdf_part    = (TH1F*) h_true->Clone("syst_pdf_part");
    TH1F* h_syst_Q2_part     = (TH1F*) h_true->Clone("syst_Q2_part");
    TH1F* h_syst_PS_part     = (TH1F*) h_true->Clone("syst_Q2_part");
    TH1F* h_syst_tot_part    = (TH1F*) h_true->Clone("syst_tot_part");
    
    h_syst_jec_part->Reset();   
    h_syst_jer_part->Reset(); 
    h_syst_btag_part->Reset();   
    h_syst_toptag_part->Reset(); 
    h_syst_bkg_part->Reset(); 
    h_syst_stat_part->Reset(); 
    h_syst_pdf_part->Reset();
    h_syst_Q2_part->Reset(); 
    h_syst_PS_part->Reset(); 
    h_syst_tot_part->Reset(); 
    
    
    float count_part[nSYST] = {0};
    float sig_part[nSYST] = {0};

    float xsec_meas = 0;
    float xsec_true = 0;

    // ----------------------------------------------------------------------------------------------------------------
    // loop over bins
    // ----------------------------------------------------------------------------------------------------------------
    
    cout << endl << "*** unfolding result (particle-level) for " << channel << " channel ***" << endl;

    for (int i=0; i<h_unfolded_part[0]->GetNbinsX(); i++) {
      
      for (int is=0; is<nSYST; is++) {
	count_part[is] = h_unfolded_part[is]->GetBinContent(i+1);
	sig_part[is]   = h_unfolded_part[is]->GetBinError(i+1);
      }
      float truth = h_part->GetBinContent(i+1);
      float this_syst_PS = fabs(count_part[17]-truth)/truth*count_part[0];

      float this_lumi_part = count_part[0]*0.026;
      
      // experimental
      float this_systEXP_up_part = 0;
      this_systEXP_up_part += (count_part[1]-count_part[0])*(count_part[1]-count_part[0]); //jec
      this_systEXP_up_part += (count_part[3]-count_part[0])*(count_part[3]-count_part[0]); //jer
      this_systEXP_up_part += (count_part[5]-count_part[0])*(count_part[5]-count_part[0]); //btag
      this_systEXP_up_part += (count_part[7]-count_part[0])*(count_part[7]-count_part[0]); //toptag
      this_systEXP_up_part += (count_part[9]-count_part[0])*(count_part[9]-count_part[0]); //background normalization
      this_systEXP_up_part += (count_part[15]-count_part[0])*(count_part[15]-count_part[0]); //toptag highpt
      this_systEXP_up_part = sqrt(this_systEXP_up_part);
      
      float this_systEXP_dn_part = 0;
      this_systEXP_dn_part += (count_part[2]-count_part[0])*(count_part[2]-count_part[0]);
      this_systEXP_dn_part += (count_part[4]-count_part[0])*(count_part[4]-count_part[0]);
      this_systEXP_dn_part += (count_part[6]-count_part[0])*(count_part[6]-count_part[0]);
      this_systEXP_dn_part += (count_part[8]-count_part[0])*(count_part[8]-count_part[0]);
      this_systEXP_dn_part += (count_part[10]-count_part[0])*(count_part[10]-count_part[0]);
      this_systEXP_dn_part += (count_part[16]-count_part[0])*(count_part[16]-count_part[0]);
      this_systEXP_dn_part = sqrt(this_systEXP_dn_part);
      
      // theory
      float this_systTH_up_part = 0;
      this_systTH_up_part += (count_part[11]-count_part[0])*(count_part[11]-count_part[0]);
      if (doQ2) this_systTH_up_part += (count_part[13]-count_part[0])*(count_part[13]-count_part[0]);
      this_systTH_up_part += this_syst_PS*this_syst_PS;
      this_systTH_up_part = sqrt(this_systTH_up_part);
      
      float this_systTH_dn_part = 0;
      this_systTH_dn_part += (count_part[12]-count_part[0])*(count_part[12]-count_part[0]);
      if (doQ2) this_systTH_dn_part += (count_part[14]-count_part[0])*(count_part[14]-count_part[0]);
      this_systTH_dn_part += this_syst_PS*this_syst_PS;
      this_systTH_dn_part = sqrt(this_systTH_dn_part);
      
      // theory + experimental + statistical
      float this_systTOT_up_part = this_systEXP_up_part*this_systEXP_up_part + this_systTH_up_part*this_systTH_up_part + sig_part[0]*sig_part[0];
      if (doNormalized == false) this_systTOT_up_part += this_lumi_part*this_lumi_part;
      this_systTOT_up_part = sqrt(this_systTOT_up_part);
      
      float this_systTOT_dn_part = this_systEXP_dn_part*this_systEXP_dn_part + this_systTH_dn_part*this_systTH_dn_part + sig_part[0]*sig_part[0];
      if (doNormalized == false) this_systTOT_dn_part += this_lumi_part*this_lumi_part;
      this_systTOT_dn_part = sqrt(this_systTOT_dn_part);
          
      
      h_stat_up_part->SetBinContent(i+1,count_part[0]+sig_part[0]);
      h_stat_dn_part->SetBinContent(i+1,count_part[0]-sig_part[0]);  
      
      if (doAverageErr) {
	h_systEXP_up_part->SetBinContent(i+1,count_part[0]+(this_systEXP_up_part+this_systEXP_dn_part)/2);
	h_systEXP_dn_part->SetBinContent(i+1,count_part[0]-(this_systEXP_up_part+this_systEXP_dn_part)/2);  
	h_systTH_up_part->SetBinContent(i+1,count_part[0]+(this_systTH_up_part+this_systTH_dn_part)/2);
	h_systTH_dn_part->SetBinContent(i+1,count_part[0]-(this_systTH_up_part+this_systTH_dn_part)/2);  
	h_systTOT_up_part->SetBinContent(i+1,count_part[0]+(this_systTOT_up_part+this_systTOT_dn_part)/2);
	h_systTOT_dn_part->SetBinContent(i+1,count_part[0]-(this_systTOT_up_part+this_systTOT_dn_part)/2);  
      }
      else {
	h_systEXP_up_part->SetBinContent(i+1,count_part[0]+this_systEXP_up_part);
	h_systEXP_dn_part->SetBinContent(i+1,count_part[0]-this_systEXP_dn_part);  
	h_systTH_up_part->SetBinContent(i+1,count_part[0]+this_systTH_up_part);
	h_systTH_dn_part->SetBinContent(i+1,count_part[0]-this_systTH_dn_part);  
	h_systTOT_up_part->SetBinContent(i+1,count_part[0]+this_systTOT_up_part);
	h_systTOT_dn_part->SetBinContent(i+1,count_part[0]-this_systTOT_dn_part);  
      }
    
      // experimental
      double syst_jecup_part   = fabs((count_part[1]-count_part[0])/count_part[0])*100;
      double syst_jecdn_part   = fabs((count_part[2]-count_part[0])/count_part[0])*100;
      double syst_jerup_part   = fabs((count_part[3]-count_part[0])/count_part[0])*100;
      double syst_jerdn_part   = fabs((count_part[4]-count_part[0])/count_part[0])*100;
      double syst_btagup_part   = fabs((count_part[5]-count_part[0])/count_part[0])*100;
      double syst_btagdn_part   = fabs((count_part[6]-count_part[0])/count_part[0])*100;
      double syst_toptagup_part = fabs((count_part[7]-count_part[0])/count_part[0])*100;
      double syst_toptagdn_part = fabs((count_part[8]-count_part[0])/count_part[0])*100;
      double syst_toptagHIGHPTup_part = fabs((count_part[15]-count_part[0])/count_part[0])*100;
      double syst_toptagHIGHPTdn_part = fabs((count_part[16]-count_part[0])/count_part[0])*100;
      double syst_bkgup_part   = fabs((count_part[9]-count_part[0])/count_part[0])*100;
      double syst_bkgdn_part   = fabs((count_part[10]-count_part[0])/count_part[0])*100;
      // statistics
      double syst_stat_part   = sig_part[0]/count_part[0]*100;
      // theoretical
      double syst_pdfup_part   = fabs((count_part[11]-count_part[0])/count_part[0])*100;
      double syst_pdfdn_part   = fabs((count_part[12]-count_part[0])/count_part[0])*100;
      double syst_scaleup_part = fabs((count_part[13]-count_part[0])/count_part[0])*100;
      double syst_scaledn_part = fabs((count_part[14]-count_part[0])/count_part[0])*100;
      // parton shower
      double syst_PS_part = this_syst_PS/count_part[0]*100;

      double max_syst_jec_part = 0;
      double max_syst_jer_part = 0;
      double max_syst_btag_part = 0;
      double max_syst_toptag_part = 0;
      double max_syst_toptagNOM_part = 0;
      double max_syst_toptagHIGHPT_part = 0;
      double max_syst_bkg_part = 0;
      double max_syst_pdf_part = 0;
      double max_syst_Q2_part  = 0;
      
      if (doAverageErr) {
	max_syst_jec_part = (syst_jecup_part+syst_jecdn_part)/2;
	max_syst_jer_part = (syst_jerup_part+syst_jerdn_part)/2;
	max_syst_btag_part = (syst_btagup_part+syst_btagdn_part)/2;
	max_syst_toptagNOM_part = (syst_toptagup_part+syst_toptagdn_part)/2;
	max_syst_toptagHIGHPT_part = (syst_toptagHIGHPTup_part+syst_toptagHIGHPTdn_part)/2;
	max_syst_bkg_part = (syst_bkgup_part+syst_bkgdn_part)/2;
	max_syst_pdf_part = (syst_pdfup_part+syst_pdfdn_part)/2;
	max_syst_Q2_part  = (syst_scaleup_part+syst_scaledn_part)/2;
      }
      else {
	max_syst_jec_part = max(syst_jecup_part,syst_jecdn_part);
	max_syst_jer_part = max(syst_jerup_part,syst_jerdn_part);
	max_syst_btag_part = max(syst_btagup_part,syst_btagdn_part);
	max_syst_toptagNOM_part = max(syst_toptagup_part,syst_toptagdn_part);
	max_syst_toptagHIGHPT_part = max(syst_toptagHIGHPTup_part,syst_toptagHIGHPTdn_part);
	max_syst_bkg_part = max(syst_bkgup_part,syst_bkgdn_part);
	max_syst_pdf_part = max(syst_pdfup_part,syst_pdfdn_part);
	max_syst_Q2_part  = max(syst_scaleup_part,syst_scaledn_part);
      }

      max_syst_toptag_part = sqrt(max_syst_toptagNOM_part*max_syst_toptagNOM_part + max_syst_toptagHIGHPT_part*max_syst_toptagHIGHPT_part);

      if (!doQ2) {
	syst_scaleup_part = 0;
	syst_scaledn_part = 0;
	max_syst_Q2_part = 0;
      }

      double syst_totalEXP_up_part = sqrt(syst_jecup_part*syst_jecup_part + syst_jerup_part*syst_jerup_part + 
					  syst_btagup_part*syst_btagup_part + syst_toptagup_part*syst_toptagup_part + 
					  syst_toptagHIGHPTup_part*syst_toptagHIGHPTup_part + syst_bkgup_part*syst_bkgup_part);
      double syst_totalEXP_dn_part = sqrt(syst_jecdn_part*syst_jecdn_part + syst_jerdn_part*syst_jerdn_part + 
					  syst_btagdn_part*syst_btagdn_part + syst_toptagdn_part*syst_toptagdn_part + 
					  syst_toptagHIGHPTdn_part*syst_toptagHIGHPTdn_part + syst_bkgdn_part*syst_bkgdn_part);
      double syst_totalTH_up_part = sqrt(syst_scaleup_part*syst_scaleup_part + syst_pdfup_part*syst_pdfup_part + syst_PS_part*syst_PS_part);
      double syst_totalTH_dn_part = sqrt(syst_scaledn_part*syst_scaledn_part + syst_pdfdn_part*syst_pdfdn_part + syst_PS_part*syst_PS_part);

      double syst_total_up_part = sqrt(syst_totalEXP_up_part*syst_totalEXP_up_part + syst_totalTH_up_part*syst_totalTH_up_part);
      double syst_total_dn_part = sqrt(syst_totalEXP_dn_part*syst_totalEXP_dn_part + syst_totalTH_dn_part*syst_totalTH_dn_part);
      
      double syst_totaltotal_up_part = sqrt(syst_total_up_part*syst_total_up_part + syst_stat_part*syst_stat_part);
      double syst_totaltotal_dn_part = sqrt(syst_total_dn_part*syst_total_dn_part + syst_stat_part*syst_stat_part);

      // Add lumi uncertainty
      if (doNormalized == false) syst_totaltotal_up_part = sqrt(syst_totaltotal_up_part*syst_totaltotal_up_part + 2.6*2.6);
      if (doNormalized == false) syst_totaltotal_dn_part = sqrt(syst_totaltotal_dn_part*syst_totaltotal_dn_part + 2.6*2.6);
      
      double max_syst_totalEXP_part = 0;
      double max_syst_totalTH_part = 0;
      double max_syst_total_part = 0;
      double max_syst_totaltotal_part = 0;
      
      if (doAverageErr) {
	max_syst_totalEXP_part = (syst_totalEXP_up_part+syst_totalEXP_dn_part)/2;
	max_syst_totalTH_part = (syst_totalTH_up_part+syst_totalTH_dn_part)/2;
	max_syst_total_part = (syst_total_up_part+syst_total_dn_part)/2;
	max_syst_totaltotal_part = (syst_totaltotal_up_part+syst_totaltotal_dn_part)/2;
      }
      else {
	max_syst_totalEXP_part = max(syst_totalEXP_up_part,syst_totalEXP_dn_part);
	max_syst_totalTH_part = max(syst_totalTH_up_part,syst_totalTH_dn_part);
	max_syst_total_part = max(syst_total_up_part,syst_total_dn_part);
	max_syst_totaltotal_part = max(syst_totaltotal_up_part,syst_totaltotal_dn_part);
      }

      h_syst_jec_part->SetBinContent(i+1,max_syst_jec_part);    
      h_syst_jer_part->SetBinContent(i+1,max_syst_jer_part);    
      h_syst_btag_part->SetBinContent(i+1,max_syst_btag_part);   
      h_syst_toptag_part->SetBinContent(i+1,max_syst_toptag_part); 
      h_syst_bkg_part->SetBinContent(i+1,max_syst_bkg_part);  
      h_syst_stat_part->SetBinContent(i+1,syst_stat_part);  
      h_syst_pdf_part->SetBinContent(i+1,max_syst_pdf_part);
      h_syst_Q2_part->SetBinContent(i+1,max_syst_Q2_part);  
      h_syst_PS_part->SetBinContent(i+1,syst_PS_part);  
      h_syst_tot_part->SetBinContent(i+1,max_syst_total_part);
      
      h_syst_jec_part->SetBinError(i+1,0.001);
      h_syst_jer_part->SetBinError(i+1,0.001);
      h_syst_btag_part->SetBinError(i+1,0.001);
      h_syst_toptag_part->SetBinError(i+1,0.001);
      h_syst_bkg_part->SetBinError(i+1,0.001);
      h_syst_stat_part->SetBinError(i+1,0.001);
      h_syst_tot_part->SetBinError(i+1,0.001);
      h_syst_pdf_part->SetBinError(i+1,0.001);
      h_syst_Q2_part->SetBinError(i+1,0.001);  
      h_syst_PS_part->SetBinError(i+1,0.001);  
      
      // ----------------------------------------------------------------------------------------------------------------
      // print outs for cross-section table
      // ----------------------------------------------------------------------------------------------------------------
      
      int ibin1 = h_systEXP_up_part->GetBin(i+1);
      int ibin2 = h_systEXP_up_part->GetBin(i+2);
      int lowedge = h_systEXP_up_part->GetBinLowEdge(ibin1);
      int highedge = h_systEXP_up_part->GetBinLowEdge(ibin2);

      if (toUnfold == "pt"){
      
	if (lowedge > 300 && highedge < 1300) {
	  cout << (float)lowedge << "--" << (float)highedge << " & " << count_part[0] << " & " << syst_stat_part << " & " 
	       << max_syst_totalEXP_part << " & " << max_syst_totalTH_part << " & " << this_lumi_part << " & " << max_syst_totaltotal_part << " & " 
	       << h_part->GetBinContent(i+1) << " & " 
	       << h_partMG->GetBinContent(i+1) << " & " 
	       << h_partMCNLO->GetBinContent(i+1) << endl;
	}
	
	if (lowedge > 300.) {
	  xsec_meas += count_part[0]*h_part->GetBinWidth(i+1);
	  xsec_true += h_part->GetBinContent(i+1)*h_part->GetBinWidth(i+1);
	}
	cout << "TOTAL cross section (particle level), measured = " << xsec_meas << " true = " << xsec_true << endl;
      }
    }

    
    // ----------------------------------------------------------------------------------------------------------------
    // RATIO PLOTS !!!!!!!
    // ----------------------------------------------------------------------------------------------------------------
    
    gStyle->SetPadLeftMargin(0.12);
    gStyle->SetPadRightMargin(0.1);
    gStyle->SetTextSize(f_textSize);
    gStyle->SetLabelSize(f_textSize,"x");
    gStyle->SetTitleSize(f_textSize,"x");
    gStyle->SetLabelSize(f_textSize,"y");
    gStyle->SetTitleSize(f_textSize,"y");
    gStyle->SetOptStat(0);
    
    TH1F* h_fullunc_part = (TH1F*) h_unfolded_part[0]->Clone("fullunc_part");
    
    for (int ib=0; ib<h_fullunc_part->GetNbinsX(); ib++) {
      if (h_fullunc_part->GetBinContent(ib+1) > 0) {
	float up = h_systTOT_up_part->GetBinContent(ib+1);
	float dn = h_systTOT_dn_part->GetBinContent(ib+1);
	h_fullunc_part->SetBinError(ib+1,(up-dn)/2);
      }
    }
    
    gStyle->SetEndErrorSize(5);


    TCanvas *c2 = new TCanvas("c2", "", 700, 625);
    
    TPad* p3 = new TPad("p3","p3",0,ratio_size+0.0,1,1);
    p3->SetBottomMargin(0.01);
    p3->SetTopMargin(0.10);
    p3->SetLeftMargin(0.16);
    p3->SetRightMargin(0.075);
    
    TPad* p4 = new TPad("p4","p4",0,0,1,ratio_size-0.0);
    p4->SetTopMargin(0.06);
    p4->SetBottomMargin(0.34);
    p4->SetLeftMargin(0.16);
    p4->SetRightMargin(0.075);

    p3->Draw();
    p4->Draw();
    
    h_dummy_part->GetYaxis()->SetTitleSize(0.075);    
    if (doLogscale) h_dummy_part->GetYaxis()->SetTitleOffset(0.8);
    else h_dummy_part->GetYaxis()->SetTitleOffset(1.1);
    h_dummy_part->GetYaxis()->SetLabelSize(0.065);
    h_dummy_part->GetXaxis()->SetTitleSize(0);
    h_dummy_part->GetXaxis()->SetLabelSize(0);
    
    p3->cd();
    
    if (doLogscale && doNormalized) {
      h_dummy_part->SetAxisRange(0.00003,0.015,"Y");
      h_part->SetAxisRange(0.00003,0.015,"Y");
      h_partMG->SetAxisRange(0.00003,0.015,"Y");
      h_partMCNLO->SetAxisRange(0.00003,0.015,"Y");
      h_unfolded_part[0]->SetAxisRange(0.00003,0.015,"Y");
      h_fullunc_part->SetAxisRange(0.000015,0.015,"Y");
      gPad->SetLogy();
    }
    else if (doLogscale) {
      if (toUnfold == "y"){
	h_dummy_part->SetAxisRange(300,30000,"Y");
	h_part->SetAxisRange(300,30000,"Y");
	h_partMG->SetAxisRange(300,30000,"Y");
	h_partMCNLO->SetAxisRange(300,30000,"Y");
	h_unfolded_part[0]->SetAxisRange(300,30000,"Y");
	h_fullunc_part->SetAxisRange(300,30000,"Y");
	gPad->SetLogy();
      }
      else {
	h_dummy_part->SetAxisRange(0.03,30,"Y");
	h_part->SetAxisRange(0.03,30,"Y");
	h_partMG->SetAxisRange(0.03,30,"Y");
	h_partMCNLO->SetAxisRange(0.03,30,"Y");
	h_unfolded_part[0]->SetAxisRange(0.03,30,"Y");
	h_fullunc_part->SetAxisRange(0.03,30,"Y");
	gPad->SetLogy();
      }
    }

    h_dummy_part->Draw("hist");
    h_part->Draw("hist,same");
    h_partMG->Draw("hist,same");
    h_partMCNLO->Draw("hist,same");
    TExec *setex1p = new TExec("setex1p","gStyle->SetErrorX(0)");
    setex1p->Draw();
    h_fullunc_part->Draw("hist,ep,same");
    h_unfolded_part[0]->Draw("hist,E1p,same");
    TExec *setex2p = new TExec("setex2p","gStyle->SetErrorX(0.5)");
    setex2p->Draw();
    h_dummy_part->Draw("hist,axis,same"); 
    
    
    
    // ----------------------------------------------------------------------------------------------------------------
    // making ratio part of plot
    // ----------------------------------------------------------------------------------------------------------------
    
    TString baselab = h_unfolded_part[0]->GetName();
    TH1F* h_ratio_part = (TH1F*) h_unfolded_part[0]->Clone(baselab+"_ratio_part");
    
    TH1F* h_ratioSTAT_up_part = (TH1F*) h_stat_up_part->Clone(baselab+"_ratioSTAT_up_part");
    TH1F* h_ratioSTAT_dn_part = (TH1F*) h_stat_dn_part->Clone(baselab+"_ratioSTAT_dn_part");
    
    TH1F* h_ratioEXP_up_part = (TH1F*) h_systEXP_up_part->Clone(baselab+"_ratioEXP_up_part");
    TH1F* h_ratioEXP_dn_part = (TH1F*) h_systEXP_dn_part->Clone(baselab+"_ratioEXP_dn_part");
    
    TH1F* h_ratioTOT_up_part = (TH1F*) h_systTOT_up_part->Clone(baselab+"_ratioTOT_up_part");
    TH1F* h_ratioTOT_dn_part = (TH1F*) h_systTOT_dn_part->Clone(baselab+"_ratioTOT_dn_part");
    
    TH1F* h_ratioTH_up_part = (TH1F*) h_systTH_up_part->Clone(baselab+"_ratioTH_up_part");
    TH1F* h_ratioTH_dn_part = (TH1F*) h_systTH_dn_part->Clone(baselab+"_ratioTH_dn_part");
    
    TH1F* h_ratioGEN_part = (TH1F*) h_part->Clone(baselab+"_ratioGEN_part");
    TH1F* h_ratioMG_part = (TH1F*) h_partMG->Clone(baselab+"_ratioMG_part");
    TH1F* h_ratioMCNLO_part = (TH1F*) h_partMCNLO->Clone(baselab+"_ratioMCNLO_part");
    
    h_ratio_part->Divide(h_unfolded_part[0]);
    h_ratioSTAT_up_part->Divide(h_unfolded_part[0]);
    h_ratioSTAT_dn_part->Divide(h_unfolded_part[0]);
    h_ratioEXP_up_part->Divide(h_unfolded_part[0]);
    h_ratioEXP_dn_part->Divide(h_unfolded_part[0]);
    h_ratioTH_up_part->Divide(h_unfolded_part[0]);
    h_ratioTH_dn_part->Divide(h_unfolded_part[0]);
    h_ratioTOT_up_part->Divide(h_unfolded_part[0]);
    h_ratioTOT_dn_part->Divide(h_unfolded_part[0]);
    h_ratioGEN_part->Divide(h_unfolded_part[0]);
    h_ratioMG_part->Divide(h_unfolded_part[0]);
    h_ratioMCNLO_part->Divide(h_unfolded_part[0]);
    
    
    // ----------------------------------------------------------------------------------------------------------------
    TH1F* blaSTAT_part = (TH1F*) h_ratioSTAT_up_part->Clone("blaSTAT_part");
    blaSTAT_part->Reset();
    for (int i=0; i<blaSTAT_part->GetNbinsX(); i++) {
      float up = h_ratioSTAT_up_part->GetBinContent(i+1);
      float dn = h_ratioSTAT_dn_part->GetBinContent(i+1);
      
      blaSTAT_part->SetBinContent(i+1,(up-dn)/2+dn);
      blaSTAT_part->SetBinError(i+1,(up-dn)/2);
    }
    
    TH1F* blaEXP_part = (TH1F*) h_ratioEXP_up_part->Clone("blaEXP_part");
    blaEXP_part->Reset();
    for (int i=0; i<blaEXP_part->GetNbinsX(); i++) {
      float up = h_ratioEXP_up_part->GetBinContent(i+1);
      float dn = h_ratioEXP_dn_part->GetBinContent(i+1);
      
      blaEXP_part->SetBinContent(i+1,(up-dn)/2+dn);
      blaEXP_part->SetBinError(i+1,(up-dn)/2);
    }
    
    TH1F* blaTH_part = (TH1F*) h_ratioTH_up_part->Clone("blaTH_part");
    blaTH_part->Reset();
    for (int i=0; i<blaTH_part->GetNbinsX(); i++) {
      float up = h_ratioTH_up_part->GetBinContent(i+1);
      float dn = h_ratioTH_dn_part->GetBinContent(i+1);
      
      blaTH_part->SetBinContent(i+1,(up-dn)/2+dn);
      blaTH_part->SetBinError(i+1,(up-dn)/2);
    }
    
    TH1F* blaTOT_part = (TH1F*) h_ratioTOT_up_part->Clone("blaTOT_part");
    blaTOT_part->Reset();
    for (int i=0; i<blaTOT_part->GetNbinsX(); i++) {
      float up = h_ratioTOT_up_part->GetBinContent(i+1);
      float dn = h_ratioTOT_dn_part->GetBinContent(i+1);
      
      blaTOT_part->SetBinContent(i+1,(up-dn)/2+dn);
      blaTOT_part->SetBinError(i+1,(up-dn)/2);
    }
    
    //blaSTAT_part->SetLineColor(1);
    //blaSTAT_part->SetLineWidth(1);
    blaSTAT_part->SetMarkerSize(0);
    blaSTAT_part->SetLineColor(0);
    blaSTAT_part->SetLineWidth(0);
    blaSTAT_part->SetFillColor(18);
    blaSTAT_part->SetFillStyle(1001);

    blaEXP_part->SetMarkerSize(0);
    blaEXP_part->SetLineColor(0);
    blaEXP_part->SetFillColor(kAzure);
    blaEXP_part->SetFillStyle(1001);
    
    blaTH_part->SetMarkerSize(0);
    blaTH_part->SetLineColor(0);
    blaTH_part->SetFillColor(kBlue);
    blaTH_part->SetFillStyle(3453);
    
    blaTOT_part->SetMarkerSize(0);
    blaTOT_part->SetLineColor(0);
    blaTOT_part->SetFillColor(kAzure-9);
    blaTOT_part->SetFillStyle(1001);
    
    
    // ----------------------------------------------------------------------------------------------------------------
    TLegend* leg = new TLegend(legx,legy,legx+0.33,legy+0.35);  
    leg->AddEntry(h_unfolded_part[0],"Data","pe1");
    leg->AddEntry(h_part,"Powheg+Pythia6 t#bar{t}","l");
    leg->AddEntry(h_partMG,"MadGraph+Pythia6 t#bar{t}","l");
    leg->AddEntry(h_partMCNLO,"MC@NLO+Herwig6 t#bar{t}","l");
    //leg->AddEntry(blaEXP_part,"Experimental uncertainty","f");
    //leg->AddEntry(blaTH_part,"Theory uncertainty","f");
    leg->AddEntry(blaSTAT_part,"Stat. Uncertainty","f");
    if (doNormalized) leg->AddEntry(blaTOT_part,"Stat. #oplus Syst.","f");
    else leg->AddEntry(blaTOT_part,"Stat. #oplus Syst. #oplus Lumi","f");
    leg->SetFillStyle(0);
    leg->SetBorderSize(0);
    leg->SetTextSize(0.055);
    leg->SetTextFont(42);
    leg->Draw();

    drawCMS(0.53,0.8,true,true,forpub);

    // ----------------------------------------------------------------------------------------------------------------
        
    p4->cd();
    p4->SetGridy();
    
    h_ratio_part->GetXaxis()->SetTitleSize(0.14);
    h_ratio_part->GetYaxis()->SetTitleSize(0.14);
    h_ratio_part->GetXaxis()->SetLabelSize(0.12);
    h_ratio_part->GetYaxis()->SetLabelSize(0.1);
    h_ratio_part->GetYaxis()->SetTitle("Theory/Data");
    if (toUnfold == "pt") h_ratio_part->GetXaxis()->SetTitle("Particle-level top p_{T} (GeV)");
    else if (toUnfold == "y") h_ratio_part->GetXaxis()->SetTitle("Particle-level top rapidity");
    h_ratio_part->GetYaxis()->SetTitleOffset(0.8);
    h_ratio_part->GetYaxis()->SetNdivisions(505);
    h_ratio_part->GetYaxis()->SetTitleOffset(0.38);
    h_ratio_part->GetXaxis()->SetTitleOffset(1.0);
    
    if (toUnfold == "y") {
      h_ratio_part->SetAxisRange(0.3,1.7,"Y");
      h_ratioGEN_part->SetAxisRange(0.3,1.7,"Y");
      h_ratioMG_part->SetAxisRange(0.3,1.7,"Y");
      h_ratioMCNLO_part->SetAxisRange(0.3,1.7,"Y");
    }
    else if (doNormalized) {
      h_ratio_part->SetAxisRange(0.6,1.4,"Y");
      h_ratioGEN_part->SetAxisRange(0.6,1.4,"Y");
      h_ratioMG_part->SetAxisRange(0.6,1.4,"Y");
      h_ratioMCNLO_part->SetAxisRange(0.6,1.4,"Y");
    }
    else {
      h_ratio_part->SetAxisRange(0.3,1.7,"Y");
      h_ratioGEN_part->SetAxisRange(0.3,1.7,"Y");
      h_ratioMG_part->SetAxisRange(0.3,1.7,"Y");
      h_ratioMCNLO_part->SetAxisRange(0.3,1.7,"Y");
    }
    h_ratio_part->Draw("hist");
    blaTOT_part->Draw("same,e2");
    //blaEXP_part->Draw("same,e2");
    //blaTH_part->Draw("same,e2");
    //blaSTAT_part->Draw("same,ep");
    blaSTAT_part->Draw("same,e2");
    h_ratioGEN_part->Draw("same,hist");
    h_ratioMG_part->Draw("same,hist");
    h_ratioMCNLO_part->Draw("same,hist");
    //blaSTAT_part->Draw("same,ep");
    h_ratio_part->Draw("same,hist");
    h_ratio_part->Draw("same,axis");
    
    p3->cd();
    
    c2->SaveAs("UnfoldingPlots/unfoldWithError_part_"+toUnfold+"_"+channel+twoStep+nobtag+".png");
    c2->SaveAs("UnfoldingPlots/unfoldWithError_part_"+toUnfold+"_"+channel+twoStep+nobtag+".eps");
    c2->SaveAs("UnfoldingPlots/unfoldWithError_part_"+toUnfold+"_"+channel+twoStep+nobtag+".pdf");
    
    
    TCanvas *c3 = new TCanvas("c3", "", 800, 600);
    c3->SetTopMargin(0.08);
    c3->SetRightMargin(0.05);
    c3->SetBottomMargin(0.14);
    c3->SetLeftMargin(0.16);
    
    
    if (toUnfold == "pt") h_dummy_r_part->GetXaxis()->SetTitle("Particle-level top p_{T} (GeV)");
    else if (toUnfold == "y") h_dummy_r_part->GetXaxis()->SetTitle("Particle-level top rapidity");
    h_dummy_r_part->GetYaxis()->SetTitle("Uncertainty [%]");
    if (toUnfold == "pt") h_dummy_r_part->SetAxisRange(400,1150,"X");
    if (toUnfold == "y") h_dummy_r_part->SetAxisRange(0,100,"Y");
    else if (doQ2 && channel == "comb" && doNormalized) h_dummy_r_part->SetAxisRange(0,40,"Y");
    else if (doQ2) h_dummy_r_part->SetAxisRange(0,70,"Y");
    else h_dummy_r_part->SetAxisRange(0,25,"Y");
    
    h_dummy_r_part->GetYaxis()->SetTitleSize(0.055);    
    h_dummy_r_part->GetYaxis()->SetTitleOffset(1.1);
    h_dummy_r_part->GetYaxis()->SetLabelSize(0.045);
    
    h_dummy_r_part->GetXaxis()->SetTitleSize(0.05);
    h_dummy_r_part->GetXaxis()->SetTitleOffset(1.2);
    h_dummy_r_part->GetXaxis()->SetLabelSize(0.0455);
    
    c3->cd();
    
    if (toUnfold == "pt") h_syst_tot_part->SetAxisRange(0,40,"Y");
    if (toUnfold == "y") h_syst_tot_part->SetAxisRange(0,100,"Y");
    h_syst_tot_part->SetFillColor(17);
    h_syst_tot_part->SetFillStyle(3344);
    h_syst_tot_part->SetLineColor(16);
    h_syst_tot_part->SetLineWidth(2);
    
    h_syst_stat_part->SetLineColor(1);
    h_syst_stat_part->SetLineWidth(2);
    h_syst_stat_part->SetMarkerColor(1);
    h_syst_stat_part->SetMarkerStyle(20);
    
    h_syst_jec_part->SetLineColor(4);
    h_syst_jec_part->SetLineWidth(2);
    h_syst_jec_part->SetMarkerColor(4);
    h_syst_jec_part->SetMarkerStyle(21);
    
    h_syst_jer_part->SetLineColor(8);
    h_syst_jer_part->SetLineWidth(2);
    h_syst_jer_part->SetMarkerColor(8);
    h_syst_jer_part->SetMarkerStyle(22);
    
    h_syst_toptag_part->SetLineColor(2);
    h_syst_toptag_part->SetLineWidth(2);
    h_syst_toptag_part->SetMarkerColor(2);
    h_syst_toptag_part->SetMarkerStyle(23);
    
    h_syst_btag_part->SetLineColor(1);
    h_syst_btag_part->SetLineWidth(2);
    h_syst_btag_part->SetMarkerColor(1);
    h_syst_btag_part->SetMarkerStyle(24);  

    h_syst_bkg_part->SetLineColor(kOrange+1);
    h_syst_bkg_part->SetLineWidth(2);
    h_syst_bkg_part->SetMarkerColor(kOrange+1);
    h_syst_bkg_part->SetMarkerStyle(26);
    
    h_syst_pdf_part->SetLineColor(6);
    h_syst_pdf_part->SetLineWidth(2);
    h_syst_pdf_part->SetMarkerColor(6);
    h_syst_pdf_part->SetMarkerStyle(25);
    
    h_syst_Q2_part->SetLineColor(kAzure+10);
    h_syst_Q2_part->SetLineWidth(2);
    h_syst_Q2_part->SetMarkerColor(kAzure+10);
    h_syst_Q2_part->SetMarkerStyle(24);
    
    h_syst_PS_part->SetLineColor(12);
    h_syst_PS_part->SetLineStyle(7);
    h_syst_PS_part->SetLineWidth(2);
    h_syst_PS_part->SetMarkerColor(12);
    h_syst_PS_part->SetMarkerStyle(32);
    
    TLegend* leg4 = new TLegend(0.6,0.54,0.85,0.88);  
    leg4->AddEntry(h_syst_tot_part,"Total syst. uncertainty","f");
    leg4->AddEntry(h_syst_stat_part,"Statistical uncertainty","lp");
    if (doNormalized == false) leg4->AddEntry(h_lumi,"Lumi uncertainty","lp");
    leg4->AddEntry(h_syst_jec_part,"Jet energy scale","lp");
    leg4->AddEntry(h_syst_jer_part,"Jet energy resolution","lp");
    leg4->AddEntry(h_syst_toptag_part,"Top-tagging efficiency","lp");
    if (nobtag == "") leg4->AddEntry(h_syst_btag_part,"b-tagging efficiency","lp");
    leg4->AddEntry(h_syst_bkg_part,"Background normalization","lp");
    leg4->AddEntry(h_syst_pdf_part,"PDF uncertainty","lp");
    if (doQ2) leg4->AddEntry(h_syst_Q2_part,"Q^{2} scale","lp");
    leg4->AddEntry(h_syst_PS_part,"Generator+PS","lp");
    leg4->SetFillStyle(0);
    leg4->SetBorderSize(0);
    leg4->SetTextSize(0.032);
    leg4->SetTextFont(42);
    
    h_dummy_r_part->Draw("hist");
    h_syst_tot_part->Draw("hist,same");
    h_syst_stat_part->Draw("ep,same");
    if (doNormalized == false) h_lumi->Draw("ep,same");
    h_syst_jec_part->Draw("ep,same");
    h_syst_jer_part->Draw("ep,same");
    h_syst_toptag_part->Draw("ep,same");
    if (nobtag == "") h_syst_btag_part->Draw("ep,same");
    h_syst_bkg_part->Draw("ep,same");
    if (doQ2) h_syst_Q2_part->Draw("ep,same");
    h_syst_pdf_part->Draw("ep,same");
    h_syst_PS_part->Draw("ep,same");
    h_dummy_r_part->Draw("hist,axis,same");
    leg4->Draw(); 
    
    drawCMS(0.2,0.84,false,true,forpub);
    
    c3->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_part_"+toUnfold+"_"+channel+twoStep+nobtag+".png");
    c3->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_part_"+toUnfold+"_"+channel+twoStep+nobtag+".pdf");
    c3->SaveAs("UnfoldingPlots/unfold_relative_uncertainties_part_"+toUnfold+"_"+channel+twoStep+nobtag+".eps");
  }

  return;

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

void drawCMS(Double_t x,Double_t y, bool pad, bool prel, bool forPublic) {

  float cmsTextSize = 0.08;
  if (!pad) cmsTextSize = 0.058;
  float extraOverCmsTextSize = 0.76;
  float extraTextSize = extraOverCmsTextSize*cmsTextSize;


  TLatex l;
  l.SetTextSize(cmsTextSize); 
  l.SetTextFont(61); 
  l.SetTextAngle(0);
  l.SetNDC();
  l.SetTextColor(1);
  if (forPublic) l.DrawLatex(x,y,"CMS");

  if (prel && forPublic) {
    TLatex lp;
    lp.SetTextSize(extraTextSize); 
    lp.SetTextFont(52); 
    lp.SetNDC();
    lp.SetTextColor(1);
    float offset = 0.11;
    if (!pad) offset = 0.10;
    lp.DrawLatex(x+offset,y,"Preliminary");
  }

  TLatex ll;
  ll.SetTextSize(extraTextSize); 
  ll.SetTextFont(42); 
  ll.SetTextAngle(0);
  ll.SetNDC();
  ll.SetTextColor(1);
  if (pad) ll.DrawLatex(0.7,0.93,"19.7 fb^{-1} (8 TeV)");
  else ll.DrawLatex(0.72,0.94,"19.7 fb^{-1} (8 TeV)");

}
