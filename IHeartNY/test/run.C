#include "TFile.h"
#include "TH1.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

void run(TString option, bool doElectron, bool combine=true) {
  
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

    /*
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
    */

  }
  // make posterior plots
  else if (option=="post") {

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, "CT10_nom", combine);

    makeTable(doElectron, "CT10_nom", combine);

  }

  else if (option=="allpost") {

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, "CT10_nom", combine);
    makeTable(doElectron, "CT10_nom", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_pdfup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_pdfup", combine);
    makePosteriorPlots("vtxMass7", doElectron, "CT10_pdfup", combine);
    makeTable(doElectron, "CT10_pdfup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "CT10_pdfdown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "CT10_pdfdown", combine);
    makePosteriorPlots("vtxMass7", doElectron, "CT10_pdfdown", combine);
    makeTable(doElectron, "CT10_pdfdown", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "MSTW_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "MSTW_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, "MSTW_nom", combine);
    makeTable(doElectron, "MSTW_nom", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "MSTW_pdfup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "MSTW_pdfup", combine);
    makePosteriorPlots("vtxMass7", doElectron, "MSTW_pdfup", combine);
    makeTable(doElectron, "MSTW_pdfup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "MSTW_pdfdown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "MSTW_pdfdown", combine);
    makePosteriorPlots("vtxMass7", doElectron, "MSTW_pdfdown", combine);
    makeTable(doElectron, "MSTW_pdfdown", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "NNPDF_nom", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "NNPDF_nom", combine);
    makePosteriorPlots("vtxMass7", doElectron, "NNPDF_nom", combine);
    makeTable(doElectron, "NNPDF_nom", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "NNPDF_pdfup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "NNPDF_pdfup", combine);
    makePosteriorPlots("vtxMass7", doElectron, "NNPDF_pdfup", combine);
    makeTable(doElectron, "NNPDF_pdfup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "NNPDF_pdfdown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "NNPDF_pdfdown", combine);
    makePosteriorPlots("vtxMass7", doElectron, "NNPDF_pdfdown", combine);
    makeTable(doElectron, "NNPDF_pdfdown", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "scaleup", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "scaleup", combine);
    makePosteriorPlots("vtxMass7", doElectron, "scaleup", combine);
    makeTable(doElectron, "scaleup", combine);

    makePosteriorPlots("etaAbsLep4", doElectron, "scaledown", combine);
    makePosteriorPlots("etaAbsLep6", doElectron, "scaledown", combine);
    makePosteriorPlots("vtxMass7", doElectron, "scaledown", combine);
    makeTable(doElectron, "scaledown", combine);

  }

  cout << "... DONE! " << endl;

}





