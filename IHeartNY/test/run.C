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
    TString hist[nHIST] = {"etaLep", "etaAbsLep", "ptLep",
			   "hadtop_pt", "hadtop_mass", "hadtop_y", 
			   "leptop_pt", "leptop_mass", "leptop_y",
			   "ht", "ptMET"};
    
    for (int ih=0; ih<nHIST; ih++) {
      for (int ir=0; ir<nREGION; ir++) {
	makePlots_single(hist[ih], region[ir]);
      }
    }  
    makePlots_single("vtxMass",7);

  }
  // debug thing
  else if (option=="debug") {

    makePlots_single("hadtop_pt",7);

  }

  cout << "... DONE! " << endl;

}





