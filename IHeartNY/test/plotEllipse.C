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

void plotEllipse(TString fitter="mle") {
  
  SetPlotStyle();
  TString channels[] = {"mu","el","comb"};
  //TString channels[] = {"comb"};

  TString fitstring = "";
  if (fitter == "mle") fitstring = "_mle";

  TGraph* curves[3][2][5];
  int ncurves[3][2];

  for (int ii = 0; ii < 3; ii++){
    for (int jj = 0; jj < 2; jj++){
      TString zoomstring = "";
      if (jj == 1) zoomstring = "_zoom";
      
      TFile* f = new TFile("run_theta/nll_2d"+fitstring+"_"+channels[ii]+zoomstring+".root");
    
      TH2F* h_ellipse;
      if (fitter == "mle") {
	h_ellipse = (TH2F*) f->Get("nll_2d");
      }
      
      if (fitter == "pl") {
	h_ellipse = (TH2F*) f->Get("nll_2d_toptag");
	TH2F* h_temp = (TH2F*) f->Get("nll_2d_beta_signal");
	h_ellipse->Add(h_temp);
	h_ellipse->Scale(-1.0);
      }
    
      TCanvas c;
      h_ellipse->GetYaxis()->SetTitleSize(0.052);
      h_ellipse->GetXaxis()->SetTitleSize(0.052);
      h_ellipse->GetYaxis()->SetLabelSize(0.045);
      h_ellipse->GetXaxis()->SetLabelSize(0.045);
      h_ellipse->GetYaxis()->SetTitleOffset(1.0);
      h_ellipse->GetYaxis()->SetTitle("#beta_{signal}");
      h_ellipse->GetXaxis()->SetTitle("Toptag SF");
      h_ellipse->Draw("COLZ");
      
      c.SaveAs("ellipse"+fitstring+"_"+channels[ii]+zoomstring+".png");
      c.SaveAs("ellipse"+fitstring+"_"+channels[ii]+zoomstring+".pdf");

      TH2F* h_full = (TH2F*) h_ellipse->Clone();
      
      // Now plot ellipse for (min, min+2)
      float maxll = h_ellipse->GetMaximum();
      if (fitter == "mle") printf("Maximum log(L) = %.2f\n",maxll);
      
      h_ellipse->SetMinimum(maxll - 2.0);
            
      h_ellipse->Draw("COLZ");
      int binx, biny, binz;

      h_ellipse->GetMaximumBin(binx, biny, binz);
      double xwidth = h_ellipse->GetXaxis()->GetBinWidth(binx);
      double ywidth = h_ellipse->GetYaxis()->GetBinWidth(biny);
      double xpos = h_ellipse->GetXaxis()->GetBinLowEdge(1) + binx * xwidth - xwidth / 2.;
      double ypos = h_ellipse->GetYaxis()->GetBinLowEdge(1) + biny * ywidth - ywidth / 2.;
      printf("Location of maximum (bin): (%.2f,%.2f)\n",binx,biny);
      printf("Location of maximum (position): (%.2f, %.2f)\n",xpos,ypos);
      
      c.SaveAs("ellipse"+fitstring+"_"+channels[ii]+zoomstring+"_2sig.png");
      c.SaveAs("ellipse"+fitstring+"_"+channels[ii]+zoomstring+"_2sig.pdf");
      
      // Now try actually plotting *contours*
      h_ellipse->SetContour(2, [(maxll - 1.0),(maxll - 2.0)]);
      h_ellipse->Draw("CONT Z LIST");
      c.Update();
      
      TH2D* h_empty = new TH2D("","",h_ellipse->GetXaxis()->GetNbins(),h_ellipse->GetXaxis()->GetXmin(),h_ellipse->GetXaxis()->GetXmax(),h_ellipse->GetYaxis()->GetNbins(), h_ellipse->GetYaxis()->GetXmin(),h_ellipse->GetYaxis()->GetXmax());
      h_empty->Draw();

      h_full->Draw("COLZ");
      
      TObjArray *conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
      int TotalConts = conts->GetSize();
      TList* contLevel = NULL;
      TGraph* curv = NULL;

      printf("TotalConts = %i\n",TotalConts);
      
      for(int aa = 0; aa < TotalConts; aa++){
	contLevel = (TList*)conts->At(aa);
	curv = (TGraph*)contLevel->First();
	int ncurv = 0;
	for(int bb = 0; bb < contLevel->GetSize(); bb++){
	  ncurv += 1;
	  TGraph* gc = (TGraph*)curv->Clone();	  
	  if ((aa == 0 && fitter == "mle") || (aa == 1 && fitter == "pl")) gc->SetLineStyle(1);
	  if ((aa == 1 && fitter == "mle") || (aa == 0 && fitter == "pl")) gc->SetLineStyle(2);
	  gc->Draw("C");
	  if (jj == 0) curves[ii][aa][bb] = gc;
	  curv = (TGraph*)contLevel->After(curv); // Get Next graph
	}
	printf("Total # curves in contour %i : %i\n",aa,ncurv);
	if (jj == 0) ncurves[ii][aa] = ncurv;
      }
      c.Update();
      
      c.SaveAs("ellipse"+fitstring+"_"+channels[ii]+zoomstring+"_cont.png");
      c.SaveAs("ellipse"+fitstring+"_"+channels[ii]+zoomstring+"_cont.pdf");
      c.Close();
    }
  }

  // Now plot all contours on same graph
  TCanvas c2;
  int colors[] = {2,4,1};
  TH2D* h_empty_all = new TH2D("","",100, -2.0, 2.0, 100, 0.0, 2.0);
  h_empty_all->GetYaxis()->SetTitleSize(0.052);
  h_empty_all->GetXaxis()->SetTitleSize(0.052);
  h_empty_all->GetYaxis()->SetLabelSize(0.045);
  h_empty_all->GetXaxis()->SetLabelSize(0.045);
  h_empty_all->GetYaxis()->SetTitleOffset(1.0);
  h_empty_all->GetYaxis()->SetTitle("#beta_{signal}");
  h_empty_all->GetXaxis()->SetTitle("Toptag SF");
  h_empty_all->Draw();
  
  for (int ii = 0; ii < 3; ii++){
    for (int aa = 0; aa < 2; aa++){
      printf("There will be %i curves in contour %i\n",ncurves[ii][aa],aa);
      for (int bb = 0; bb < ncurves[ii][aa]; bb++){
	curves[ii][aa][bb]->SetLineColor(colors[ii]);
	if (aa == 1) curves[ii][aa][bb]->SetLineStyle(2);
	curves[ii][aa][bb]->Draw("C");
      }
    }
  }

  c2.SaveAs("ellipse"+fitstring+"_allCont.png");
  c2.SaveAs("ellipse"+fitstring+"_allCont.pdf");
  c2.Close();
      
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
  //gStyle->SetHistLineColor(1);
  
  gStyle->SetPalette(1);
  
  // set the paper & margin sizes
  //gStyle->SetPaperSize(20,26);
  gStyle->SetPadTopMargin(0.07);
  gStyle->SetPadRightMargin(0.15);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.12);
  
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

