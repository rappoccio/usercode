#include "TFile.h"
#include "TH1.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

void run(TString option, bool doElectron, bool combine=true, TString pdfdir = "CT10_nom", TString ptbin = "") {
  
  cout << "compile macro..." << endl;
  gSystem->CompileMacro("makeHists.cc");


  // histograms for theta inputs
  if (option=="theta") {

    cout << "make theta histograms..." << endl;

    makeTheta_subtract("etaAbsLep",4,6,ptbin,doElectron,pdfdir,false);
    makeTheta_subtract("etaAbsLep",6,7,ptbin,doElectron,pdfdir,false);
    makeTheta_single("vtxMass",7,ptbin,doElectron,pdfdir,false);

  } 
  else if (option=="thetaHalf") {

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

    //makePlots("etaAbsLep", 4, 6, doElectron, "", "CT10_nom", true, combine);
    //makePlots("etaAbsLep", 6, 7, doElectron, "", "CT10_nom", true, combine);
    makePlots("etaAbsLep", 7, 0, doElectron, "", "CT10_nom", true, combine);

    //makePlots("vtxMass", 4, 6, doElectron, "", "CT10_nom", true, combine);
    //makePlots("vtxMass", 6, 7, doElectron, "", "CT10_nom", true, combine);
    //makePlots("vtxMass", 7, 0, doElectron, "", "CT10_nom", true, combine);

    makePlots("hadtop_pt", 4, 6, doElectron, "", "CT10_nom", true, combine);
    makePlots("hadtop_pt", 6, 7, doElectron, "", "CT10_nom", true, combine);
    makePlots("hadtop_pt", 7, 0, doElectron, "", "CT10_nom", true, combine);

    makePlots("hadtop_y", 4, 6, doElectron, "", "CT10_nom", true, combine);
    makePlots("hadtop_y", 6, 7, doElectron, "", "CT10_nom", true, combine);
    makePlots("hadtop_y", 7, 0, doElectron, "", "CT10_nom", true, combine);

    //makePlots("ptLep", 4, 6, doElectron, "", "CT10_nom", true, combine);
    makePlots("ptLep", 6, 7, doElectron, "", "CT10_nom", true, combine);
    makePlots("ptLep", 7, 0, doElectron, "", "CT10_nom", true, combine);

    //makePlots("ptMET", 4, 6, doElectron, "", "CT10_nom", true, combine);
    //makePlots("ptMET", 6, 7, doElectron, "", "CT10_nom", true, combine);
    //makePlots("ptMET", 7, 0, doElectron, "", "CT10_nom", true, combine);

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
    /*
    makePlots("hadtop_pt",7,0, doElectron);
    makePlots("hadtop_pt",6,7, doElectron);
    makePlots("hadtop_pt",4,6, doElectron);
    */

    makePlots("vtxMass",7,0, doElectron,"",pdfdir);
    makePlots("etaAbsLep",6,7, doElectron,"",pdfdir);
    makePlots("etaAbsLep",4,6, doElectron,"",pdfdir);
  }
  // debug thing
  else if (option=="debug") {
    makePlots("ptLep",5,7, doElectron,"",pdfdir);
    makePlots("ptMET",5,7, doElectron,"",pdfdir);
    makePlots("hadtop_pt",5,7, doElectron,"",pdfdir);
    makePlots("etaAbsLep",5,7, doElectron,"",pdfdir);
    makePlots("vtxMass",5,7, doElectron,"",pdfdir);
  }

  else if (option=="table") {
    setExtName();
    makeTable(doElectron, "", "CT10_nom", combine);
  }

  // make posterior plots
  else if (option=="post") {

    setExtName();

    if (fittype == "htlep6" || fittype == "flatQCD"){
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
    else {
      makePosteriorPlots("etaAbsLep4", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("etaAbsLep6", doElectron, ptbin, "CT10_nom", combine, false, false);
      makePosteriorPlots("vtxMass7", doElectron, ptbin, "CT10_nom", combine, false, false);
    }
    
    makeTable(doElectron, ptbin, "CT10_nom", combine, false, false);

  }

  cout << "... DONE! " << endl;

}





