#include "TFile.h"
#include "TH1.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

void run(TString option, bool doElectron) {
  
  cout << "compile macro..." << endl;
  gSystem->CompileMacro("makeHists.cc");


  // histograms for theta inputs
  if (option=="theta") {

    cout << "make theta histograms..." << endl;

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"scaleup");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"scaleup");
    makeTheta_single("vtxMass",7,doElectron,"scaleup");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"scaledown");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"scaledown");
    makeTheta_single("vtxMass",7,doElectron,"scaledown");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"CT10_nom");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"CT10_nom");
    makeTheta_single("vtxMass",7,doElectron,"CT10_nom");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"CT10_pdfup");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"CT10_pdfup");
    makeTheta_single("vtxMass",7,doElectron,"CT10_pdfup");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"CT10_pdfdown");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"CT10_pdfdown");
    makeTheta_single("vtxMass",7,doElectron,"CT10_pdfdown");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"MSTW_nom");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"MSTW_nom");
    makeTheta_single("vtxMass",7,doElectron,"MSTW_nom");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"MSTW_pdfup");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"MSTW_pdfup");
    makeTheta_single("vtxMass",7,doElectron,"MSTW_pdfup");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"MSTW_pdfdown");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"MSTW_pdfdown");
    makeTheta_single("vtxMass",7,doElectron,"MSTW_pdfdown");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"NNPDF_nom");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"NNPDF_nom");
    makeTheta_single("vtxMass",7,doElectron,"NNPDF_nom");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"NNPDF_pdfup");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"NNPDF_pdfup");
    makeTheta_single("vtxMass",7,doElectron,"NNPDF_pdfup");

    makeTheta_subtract("etaAbsLep",4,6,doElectron,"NNPDF_pdfdown");
    makeTheta_subtract("etaAbsLep",6,7,doElectron,"NNPDF_pdfdown");
    makeTheta_single("vtxMass",7,doElectron,"NNPDF_pdfdown");

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

  }

  else if (option=="allpre") {

    makePlots("vtxMass",7,0,doElectron,"CT10_nom");
    makePlots("etaAbsLep",6,7,doElectron,"CT10_nom");
    makePlots("etaAbsLep",4,6,doElectron,"CT10_nom");

    makePlots("vtxMass",7,0,doElectron,"CT10_pdfup");
    makePlots("etaAbsLep",6,7,doElectron,"CT10_pdfup");
    makePlots("etaAbsLep",4,6,doElectron,"CT10_pdfup");

    makePlots("vtxMass",7,0,doElectron,"CT10_pdfdown");
    makePlots("etaAbsLep",6,7,doElectron,"CT10_pdfdown");
    makePlots("etaAbsLep",4,6,doElectron,"CT10_pdfdown");

    makePlots("vtxMass",7,0,doElectron,"MSTW_nom");
    makePlots("etaAbsLep",6,7,doElectron,"MSTW_nom");
    makePlots("etaAbsLep",4,6,doElectron,"MSTW_nom");

    makePlots("vtxMass",7,0,doElectron,"MSTW_pdfup");
    makePlots("etaAbsLep",6,7,doElectron,"MSTW_pdfup");
    makePlots("etaAbsLep",4,6,doElectron,"MSTW_pdfup");

    makePlots("vtxMass",7,0,doElectron,"MSTW_pdfdown");
    makePlots("etaAbsLep",6,7,doElectron,"MSTW_pdfdown");
    makePlots("etaAbsLep",4,6,doElectron,"MSTW_pdfdown");

    makePlots("vtxMass",7,0,doElectron,"NNPDF_nom");
    makePlots("etaAbsLep",6,7,doElectron,"NNPDF_nom");
    makePlots("etaAbsLep",4,6,doElectron,"NNPDF_nom");

    makePlots("vtxMass",7,0,doElectron,"NNPDF_pdfup");
    makePlots("etaAbsLep",6,7,doElectron,"NNPDF_pdfup");
    makePlots("etaAbsLep",4,6,doElectron,"NNPDF_pdfup");

    makePlots("vtxMass",7,0,doElectron,"NNPDF_pdfdown");
    makePlots("etaAbsLep",6,7,doElectron,"NNPDF_pdfdown");
    makePlots("etaAbsLep",4,6,doElectron,"NNPDF_pdfdown");

    makePlots("vtxMass",7,0,doElectron,"scaleup");
    makePlots("etaAbsLep",6,7,doElectron,"scaleup");
    makePlots("etaAbsLep",4,6,doElectron,"scaleup");

    makePlots("vtxMass",7,0,doElectron,"scaledown");
    makePlots("etaAbsLep",6,7,doElectron,"scaledown");
    makePlots("etaAbsLep",4,6,doElectron,"scaledown");

  }
  // make posterior plots
  else if (option=="post") {

    makePosteriorPlots("etaAbsLep4", doElectron);
    makePosteriorPlots("etaAbsLep6", doElectron);
    makePosteriorPlots("vtxMass7", doElectron);

    makeTable(doElectron);

  }

  else if (option=="allpost") {

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_nom");
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_nom");
    makePosteriorPlots("vtxMass7", doElectron, "CT10_nom");
    makeTable(doElectron, "CT10_nom");

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_pdfup");
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_pdfup");
    makePosteriorPlots("vtxMass7", doElectron, "CT10_pdfup");
    makeTable(doElectron, "CT10_pdfup");

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_pdfdown");
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_pdfdown");
    makePosteriorPlots("vtxMass7", doElectron, "CT10_pdfdown");
    makeTable(doElectron, "CT10_pdfdown");

    makePosteriorPlots("etaAbsLep4", doElectron, "MSTW_nom");
    makePosteriorPlots("etaAbsLep6", doElectron, "MSTW_nom");
    makePosteriorPlots("vtxMass7", doElectron, "MSTW_nom");
    makeTable(doElectron, "MSTW_nom");

    makePosteriorPlots("etaAbsLep4", doElectron, "MSTW_pdfup");
    makePosteriorPlots("etaAbsLep6", doElectron, "MSTW_pdfup");
    makePosteriorPlots("vtxMass7", doElectron, "MSTW_pdfup");
    makeTable(doElectron, "MSTW_pdfup");

    makePosteriorPlots("etaAbsLep4", doElectron, "MSTW_pdfdown");
    makePosteriorPlots("etaAbsLep6", doElectron, "MSTW_pdfdown");
    makePosteriorPlots("vtxMass7", doElectron, "MSTW_pdfdown");
    makeTable(doElectron, "MSTW_pdfdown");

    makePosteriorPlots("etaAbsLep4", doElectron, "NNPDF_nom");
    makePosteriorPlots("etaAbsLep6", doElectron, "NNPDF_nom");
    makePosteriorPlots("vtxMass7", doElectron, "NNPDF_nom");
    makeTable(doElectron, "NNPDF_nom");

    makePosteriorPlots("etaAbsLep4", doElectron, "NNPDF_pdfup");
    makePosteriorPlots("etaAbsLep6", doElectron, "NNPDF_pdfup");
    makePosteriorPlots("vtxMass7", doElectron, "NNPDF_pdfup");
    makeTable(doElectron, "NNPDF_pdfup");

    makePosteriorPlots("etaAbsLep4", doElectron, "NNPDF_pdfdown");
    makePosteriorPlots("etaAbsLep6", doElectron, "NNPDF_pdfdown");
    makePosteriorPlots("vtxMass7", doElectron, "NNPDF_pdfdown");
    makeTable(doElectron, "NNPDF_pdfdown");

    makePosteriorPlots("etaAbsLep4", doElectron, "scaleup");
    makePosteriorPlots("etaAbsLep6", doElectron, "scaleup");
    makePosteriorPlots("vtxMass7", doElectron, "scaleup");
    makeTable(doElectron, "scaleup");

    makePosteriorPlots("etaAbsLep4", doElectron, "scaledown");
    makePosteriorPlots("etaAbsLep6", doElectron, "scaledown");
    makePosteriorPlots("vtxMass7", doElectron, "scaledown");
    makeTable(doElectron, "scaledown");

  }

  cout << "... DONE! " << endl;

}





