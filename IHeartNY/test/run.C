#include "TFile.h"
#include "TH1.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

void run(TString option) {
  
  cout << "compile macro..." << endl;
  gSystem->CompileMacro("makeHists.cc");


  // histograms for theta inputs
  if (option=="theta") {

    cout << "make theta histograms..." << endl;

    makeTheta_subtract("etaAbsLep",4,6,"scaleup");
    makeTheta_subtract("etaAbsLep",6,7,"scaleup");
    makeTheta_single("vtxMass",7,"scaleup");

    makeTheta_subtract("etaAbsLep",4,6,"scaledown");
    makeTheta_subtract("etaAbsLep",6,7,"scaledown");
    makeTheta_single("vtxMass",7,"scaledown");

    makeTheta_subtract("etaAbsLep",4,6,"CT10_nom");
    makeTheta_subtract("etaAbsLep",6,7,"CT10_nom");
    makeTheta_single("vtxMass",7,"CT10_nom");

    makeTheta_subtract("etaAbsLep",4,6,"CT10_pdfup");
    makeTheta_subtract("etaAbsLep",6,7,"CT10_pdfup");
    makeTheta_single("vtxMass",7,"CT10_pdfup");

    makeTheta_subtract("etaAbsLep",4,6,"CT10_pdfdown");
    makeTheta_subtract("etaAbsLep",6,7,"CT10_pdfdown");
    makeTheta_single("vtxMass",7,"CT10_pdfdown");

    makeTheta_subtract("etaAbsLep",4,6,"MSTW_nom");
    makeTheta_subtract("etaAbsLep",6,7,"MSTW_nom");
    makeTheta_single("vtxMass",7,"MSTW_nom");

    makeTheta_subtract("etaAbsLep",4,6,"MSTW_pdfup");
    makeTheta_subtract("etaAbsLep",6,7,"MSTW_pdfup");
    makeTheta_single("vtxMass",7,"MSTW_pdfup");

    makeTheta_subtract("etaAbsLep",4,6,"MSTW_pdfdown");
    makeTheta_subtract("etaAbsLep",6,7,"MSTW_pdfdown");
    makeTheta_single("vtxMass",7,"MSTW_pdfdown");

    makeTheta_subtract("etaAbsLep",4,6,"NNPDF_nom");
    makeTheta_subtract("etaAbsLep",6,7,"NNPDF_nom");
    makeTheta_single("vtxMass",7,"NNPDF_nom");

    makeTheta_subtract("etaAbsLep",4,6,"NNPDF_pdfup");
    makeTheta_subtract("etaAbsLep",6,7,"NNPDF_pdfup");
    makeTheta_single("vtxMass",7,"NNPDF_pdfup");

    makeTheta_subtract("etaAbsLep",4,6,"NNPDF_pdfdown");
    makeTheta_subtract("etaAbsLep",6,7,"NNPDF_pdfdown");
    makeTheta_single("vtxMass",7,"NNPDF_pdfdown");

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
	makePlots(hist[ih], region[ir], region2[ir]);
      }
    }  
    makePlots("vtxMass",7);

  }
  // debug thing
  else if (option=="plotmini") {

    makePlots("hadtop_pt",7);
    makePlots("hadtop_pt",6,7);
    makePlots("hadtop_pt",4,6);

    makePlots("vtxMass",7);
    makePlots("etaAbsLep",6,7);
    makePlots("etaAbsLep",4,6);

  }

  else if (option=="allpre") {

    makePlots("vtxMass",7,0,"CT10_nom");
    makePlots("etaAbsLep",6,7,"CT10_nom");
    makePlots("etaAbsLep",4,6,"CT10_nom");

    makePlots("vtxMass",7,0,"CT10_pdfup");
    makePlots("etaAbsLep",6,7,"CT10_pdfup");
    makePlots("etaAbsLep",4,6,"CT10_pdfup");

    makePlots("vtxMass",7,0,"CT10_pdfdown");
    makePlots("etaAbsLep",6,7,"CT10_pdfdown");
    makePlots("etaAbsLep",4,6,"CT10_pdfdown");

    makePlots("vtxMass",7,0,"MSTW_nom");
    makePlots("etaAbsLep",6,7,"MSTW_nom");
    makePlots("etaAbsLep",4,6,"MSTW_nom");

    makePlots("vtxMass",7,0,"MSTW_pdfup");
    makePlots("etaAbsLep",6,7,"MSTW_pdfup");
    makePlots("etaAbsLep",4,6,"MSTW_pdfup");

    makePlots("vtxMass",7,0,"MSTW_pdfdown");
    makePlots("etaAbsLep",6,7,"MSTW_pdfdown");
    makePlots("etaAbsLep",4,6,"MSTW_pdfdown");

    makePlots("vtxMass",7,0,"NNPDF_nom");
    makePlots("etaAbsLep",6,7,"NNPDF_nom");
    makePlots("etaAbsLep",4,6,"NNPDF_nom");

    makePlots("vtxMass",7,0,"NNPDF_pdfup");
    makePlots("etaAbsLep",6,7,"NNPDF_pdfup");
    makePlots("etaAbsLep",4,6,"NNPDF_pdfup");

    makePlots("vtxMass",7,0,"NNPDF_pdfdown");
    makePlots("etaAbsLep",6,7,"NNPDF_pdfdown");
    makePlots("etaAbsLep",4,6,"NNPDF_pdfdown");

    makePlots("vtxMass",7,0,"scaleup");
    makePlots("etaAbsLep",6,7,"scaleup");
    makePlots("etaAbsLep",4,6,"scaleup");

    makePlots("vtxMass",7,0,"scaledown");
    makePlots("etaAbsLep",6,7,"scaledown");
    makePlots("etaAbsLep",4,6,"scaledown");

  }
  // make posterior plots
  else if (option=="post") {

    makePosteriorPlots("etaAbsLep4");
    makePosteriorPlots("etaAbsLep6");
    makePosteriorPlots("vtxMass7");

    makeTable();

  }

  else if (option=="allpost") {

    makePosteriorPlots("etaAbsLep4", "CT10_nom");
    makePosteriorPlots("etaAbsLep6", "CT10_nom");
    makePosteriorPlots("vtxMass7", "CT10_nom");
    makeTable("CT10_nom");

    makePosteriorPlots("etaAbsLep4", "CT10_pdfup");
    makePosteriorPlots("etaAbsLep6", "CT10_pdfup");
    makePosteriorPlots("vtxMass7", "CT10_pdfup");
    makeTable("CT10_pdfup");

    makePosteriorPlots("etaAbsLep4", "CT10_pdfdown");
    makePosteriorPlots("etaAbsLep6", "CT10_pdfdown");
    makePosteriorPlots("vtxMass7", "CT10_pdfdown");
    makeTable("CT10_pdfdown");

    makePosteriorPlots("etaAbsLep4", "MSTW_nom");
    makePosteriorPlots("etaAbsLep6", "MSTW_nom");
    makePosteriorPlots("vtxMass7", "MSTW_nom");
    makeTable("MSTW_nom");

    makePosteriorPlots("etaAbsLep4", "MSTW_pdfup");
    makePosteriorPlots("etaAbsLep6", "MSTW_pdfup");
    makePosteriorPlots("vtxMass7", "MSTW_pdfup");
    makeTable("MSTW_pdfup");

    makePosteriorPlots("etaAbsLep4", "MSTW_pdfdown");
    makePosteriorPlots("etaAbsLep6", "MSTW_pdfdown");
    makePosteriorPlots("vtxMass7", "MSTW_pdfdown");
    makeTable("MSTW_pdfdown");

    makePosteriorPlots("etaAbsLep4", "NNPDF_nom");
    makePosteriorPlots("etaAbsLep6", "NNPDF_nom");
    makePosteriorPlots("vtxMass7", "NNPDF_nom");
    makeTable("NNPDF_nom");

    makePosteriorPlots("etaAbsLep4", "NNPDF_pdfup");
    makePosteriorPlots("etaAbsLep6", "NNPDF_pdfup");
    makePosteriorPlots("vtxMass7", "NNPDF_pdfup");
    makeTable("NNPDF_pdfup");

    makePosteriorPlots("etaAbsLep4", "NNPDF_pdfdown");
    makePosteriorPlots("etaAbsLep6", "NNPDF_pdfdown");
    makePosteriorPlots("vtxMass7", "NNPDF_pdfdown");
    makeTable("NNPDF_pdfdown");

    makePosteriorPlots("etaAbsLep4", "scaleup");
    makePosteriorPlots("etaAbsLep6", "scaleup");
    makePosteriorPlots("vtxMass7", "scaleup");
    makeTable("scaleup");

    makePosteriorPlots("etaAbsLep4", "scaledown");
    makePosteriorPlots("etaAbsLep6", "scaledown");
    makePosteriorPlots("vtxMass7", "scaledown");
    makeTable("scaledown");

  }

  cout << "... DONE! " << endl;

}





