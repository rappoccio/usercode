#include "TFile.h"
#include "TH1.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

void run(TString option, bool doElectron, bool combine=true, TString ptbin = "") {
  
  cout << "compile macro..." << endl;
  gSystem->CompileMacro("makeHists.cc");


  // histograms for theta inputs
  if (option=="theta") {

    cout << "make theta histograms..." << endl;

    makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"CT10_nom");
    makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"CT10_nom");
    makeTheta_single("vtxMass",7,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");
    //makeTheta_single("htLep",7,ptbin,doElectron,"CT10_nom");
    
    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"CT10_pdfup");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"CT10_pdfup");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"CT10_pdfup");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_pdfup");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_pdfup");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"CT10_pdfdown");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"CT10_pdfdown");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"CT10_pdfdown");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_pdfdown");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_pdfdown");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"MSTW_nom");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"MSTW_nom");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"MSTW_nom");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"MSTW_pdfup");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"MSTW_pdfup");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"MSTW_pdfup");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"MSTW_pdfdown");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"MSTW_pdfdown");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"MSTW_pdfdown");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"NNPDF_nom");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"NNPDF_nom");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"NNPDF_nom");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"NNPDF_pdfup");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"NNPDF_pdfup");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"NNPDF_pdfup");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"NNPDF_pdfdown");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"NNPDF_pdfdown");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"NNPDF_pdfdown");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"CT10_nom");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"CT10_nom");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"scaleup");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"scaleup");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"scaleup");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"scaleup");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"scaleup");

    //makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,"scaledown");
    //makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,"scaledown");
    //makeTheta_single("vtxMass",7,ptbin,doElectron,"scaledown");
    //makeTheta_subtract("htLep",4,6,ptbin,doElectron,"scaledown");
    //makeTheta_subtract("htLep",6,7,ptbin,doElectron,"scaledown");

  } 

  if (option=="thetaHalf") {

    cout << "make theta histograms using 1/2 QCD..." << endl;

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"CT10_nom",true);
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"CT10_nom",true);
    makeTheta_single("vtxMass",7,doElectron,"CT10_nom",true);

  } 

  // various plots for kinematic checks
  else if (option=="plot") {

    cout << "make pretty histograms..." << endl;

    const int nREGION = 3;
    const int nHIST = 11;
    int region[nREGION] = {4,6,7};
    int region2[nREGION] = {6,7,0};
    TString hist[nHIST] = {"etaLep", "etaAbsLep", "ptLep",
			   "hadtop_pt", "hadtop_mass", "hadtop_y", 
			   "leptop_pt", "leptop_mass", "leptop_y",
			   "ht", "ptMET"};
    
    for (int ih=0; ih<nHIST; ih++) {
      for (int ir=0; ir<nREGION; ir++) {
	makePlots(hist[ih], region[ir], region2[ir], doElectron);
      }
    }  
    makePlots("vtxMass",7,0,doElectron);

  }

  // various plots for kinematic checks
  else if (option=="plotPost") {

    cout << "Make various post-fit histograms..." << endl;

    setExtName();

    const int nREGION = 4;
    const int nHIST = 11;
    int region[nREGION] = {4,6,6,7};
    int region2[nREGION] = {6,7,0,0};
    TString hist[nHIST] = {"etaLep", "etaAbsLep", "ptLep",
			   "hadtop_pt", "hadtop_mass", "hadtop_y", 
			   "leptop_pt", "leptop_mass", "leptop_y",
			   "ht", "ptMET"};
    
    for (int ih=0; ih<nHIST; ih++) {
      for (int ir=0; ir<nREGION; ir++) {
	makePlots(hist[ih], region[ir], region2[ir], doElectron, "", "CT10_nom", true, combine);
      }
    }  
    makePlots("vtxMass", 7, 0, doElectron, "", "CT10_nom", true, combine);

  }


  // various plots for kinematic checks
  else if (option=="plotex") {

    cout << "make exclusive pretty histograms..." << endl;

    const int nHIST = 11;
    TString hist[nHIST] = {"etaLep", "etaAbsLep", "ptLep",
			   "hadtop_pt", "hadtop_mass", "hadtop_y", 
			   "leptop_pt", "leptop_mass", "leptop_y",
			   "ht", "ptMET"};
    
    for (int ih=0; ih<nHIST; ih++) {
      makePlots(hist[ih], 4,6, doElectron);
      makePlots(hist[ih], 6,7, doElectron);
      makePlots(hist[ih], 7,0, doElectron);      
    }  
    makePlots("vtxMass",7,0, doElectron);

  }

  // debug thing
  else if (option=="plotmini") {
    makePlots("hadtop_pt",7,0, doElectron);
    makePlots("hadtop_pt",6,7, doElectron);
    makePlots("hadtop_pt",4,6, doElectron);

    makePlots("vtxMass",7,0, doElectron);
    makePlots("etaAbsLep",6,7, doElectron);
    makePlots("etaAbsLep",4,6, doElectron);
    
    makePlots("htLep",7,0, doElectron);
    makePlots("htLep",6,7, doElectron);
    makePlots("htLep",4,6, doElectron);
  }

  else if (option=="allpre") {

    makePlots("vtxMass",7,0,doElectron,ptbin,"CT10_nom");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"CT10_nom");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"CT10_nom");

    makePlots("vtxMass",7,0,doElectron,ptbin,"CT10_pdfup");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"CT10_pdfup");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"CT10_pdfup");

    makePlots("vtxMass",7,0,doElectron,ptbin,"CT10_pdfdown");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"CT10_pdfdown");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"CT10_pdfdown");

    makePlots("vtxMass",7,0,doElectron,ptbin,"MSTW_nom");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"MSTW_nom");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"MSTW_nom");

    makePlots("vtxMass",7,0,doElectron,ptbin,"MSTW_pdfup");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"MSTW_pdfup");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"MSTW_pdfup");

    makePlots("vtxMass",7,0,doElectron,ptbin,"MSTW_pdfdown");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"MSTW_pdfdown");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"MSTW_pdfdown");

    makePlots("vtxMass",7,0,doElectron,ptbin,"NNPDF_nom");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"NNPDF_nom");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"NNPDF_nom");

    makePlots("vtxMass",7,0,doElectron,ptbin,"NNPDF_pdfup");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"NNPDF_pdfup");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"NNPDF_pdfup");

    makePlots("vtxMass",7,0,doElectron,ptbin,"NNPDF_pdfdown");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"NNPDF_pdfdown");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"NNPDF_pdfdown");

    makePlots("vtxMass",7,0,doElectron,ptbin,"scaleup");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"scaleup");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"scaleup");

    makePlots("vtxMass",7,0,doElectron,ptbin,"scaledown");
    makePlots("etaAbsLep",6,7,doElectron,ptbin,"scaledown");
    makePlots("etaAbsLep",4,6,doElectron,ptbin,"scaledown");

  }

  else if (option=="table") {
    setExtName();
    makeTable(doElectron, "", "CT10_nom", combine);
  }

  // make posterior plots
  else if (option=="post") {

    setExtName();

    if (fittype == ""){
      makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    else if (fittype == "htlep6"){
      makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    else if (fittype == "htlep46"){
      makePosteriorPlots("htLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    else if (fittype == "htlep467"){
      makePosteriorPlots("htLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    else if (fittype == "2temp0t"){
      makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    else if (fittype == "2temp46"){
      makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("htLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    

    makeTable(doElectron, ptbin, "CT10_nom", combine, false, false);

  }

  else if (option=="allpost") {

    setExtName();
    
    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "CT10_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine);
    makeTable(doElectron, ptbin, "CT10_nom", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_pdfup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "CT10_pdfup", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_pdfup", combine);
    makeTable(doElectron, ptbin, "CT10_pdfup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_pdfdown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "CT10_pdfdown", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_pdfdown", combine);
    makeTable(doElectron, ptbin, "CT10_pdfdown", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "MSTW_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "MSTW_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "MSTW_nom", combine);
    makeTable(doElectron, ptbin, "MSTW_nom", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "MSTW_pdfup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "MSTW_pdfup", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "MSTW_pdfup", combine);
    makeTable(doElectron, ptbin, "MSTW_pdfup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "MSTW_pdfdown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "MSTW_pdfdown", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "MSTW_pdfdown", combine);
    makeTable(doElectron, ptbin, "MSTW_pdfdown", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "NNPDF_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "NNPDF_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "NNPDF_nom", combine);
    makeTable(doElectron, ptbin, "NNPDF_nom", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "NNPDF_pdfup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "NNPDF_pdfup", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "NNPDF_pdfup", combine);
    makeTable(doElectron, ptbin, "NNPDF_pdfup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "NNPDF_pdfdown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "NNPDF_pdfdown", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "NNPDF_pdfdown", combine);
    makeTable(doElectron, ptbin, "NNPDF_pdfdown", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "scaleup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "scaleup", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "scaleup", combine);
    makeTable(doElectron, ptbin, "scaleup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "scaledown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "scaledown", combine);
    makePosteriorPlots("vtxMass7", doElectron, ptbin, "scaledown", combine);
    makeTable(doElectron, ptbin, "scaledown", combine);

  }

  cout << "... DONE! " << endl;

}





