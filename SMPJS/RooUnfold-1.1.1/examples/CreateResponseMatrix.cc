#include "TNamed.h"
#include "TRandom.h"
#include "TFile.h"
#include "TF1.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TPaveText.h"
#include "TCanvas.h"
#include "RooUnfold.h"
#include "RooUnfoldResponse.h"
#include "../interface/CommandLine.h"
#include "TSystem.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <fstream>
#include <string>
using namespace std;

    

void CreateResponseMatrix(int argc, char** argv)
{
  ///////////////////  Read parameters  /////////////////////
  CommandLine c1;
  
  c1.parse(argc,argv);
  
  const int BIN           = c1.getValue<int>     ("NBINS");
  int NEVENTS             = c1.getValue<int>     ("NEVENTS");
  string InputFileName    = c1.getValue<string>  ("INPUTNAME");
  string OutputFileName   = c1.getValue<string>  ("OUTPUTNAME");
  string InputSpectrum    = c1.getValue<string>  ("INPUTSPECTRUM");
  string hInputSpectrum   = c1.getValue<string>  ("INPUTSPECTRUMHISTO");
  string fInputSpectrum   = c1.getValue<string>  ("INPUTSPECTRUMFUNC");
  string Resolution       = c1.getValue<string>  ("RESOLUTION");
  vector<double> PtHatBnd = c1.getVector<double> ("Boundaries");
  c1.print();

  /// example config:
  // NBINS              = 6
  // NEVENTS            = 1000
  // INPUTNAME          = "PtSpectra_ak7pf.root" 
  // INPUTSPECTRUM      = "InclusiveHistos_pythia.root"
  // INPUTSPECTRUMHISTO = "GenPt_Ybin"
  // OUTPUTNAME         = "ResponseMatrix_2.root"
  // RESOLUTION         = "TMath::Sqrt(([0]*[0])/pow(x,2)+([1]*[1])/x+[2]*[2])"
  // INPUTSPECTRUMFUNC  = "[0]*pow(2*x/7000,-[1])*pow(1-x/7000,[2])"

  // Boundaries    = 40., 53., 67., 81., 97., 114., 133., 153., 174., 196., 220., 245., 272., 300., 330., 362., 395., 430., 468., 507., 548., 592., 638., 686., 737., 
  // 790., 846., 905., 967., 1032., 1101., 1172., 1248., 1327., 1410., 1497., 1588., 1684., 1784., 1890., 2000., 2116., 2238., 2366., 2500., 2640., 2787., 2941., 
  // 3103., 3273., 3500.

  
  for(int i=0;i<PtHatBnd.size();i++){cout<<i<<" "<<PtHatBnd.at(i)<<" "<<PtHatBnd.size()<<endl;}
  
  const int npTBins = PtHatBnd.size()-1;
 
  double pTBnd[npTBins+1];

  for(int i=0;i<npTBins+1;i++)
    {
      pTBnd[i]=PtHatBnd.at(i)/1000.;
      cout<<"i="<<i<<" "<<pTBnd[i]<<endl;
    }
  double FitRange[]={2800,2800,2000,1400,900,550};
  char name[1000];
  double PARAM[][3] =
    {{0.005162,0.0284,0.03607},{0.006166,0.02428,0.03886},{0.008006,0.02335,0.04418},{0.009145,0.01232,0.03314},
     {0.007821,0.01298,0.0271},{0.008735,0.00719,0.03176}};
 
  //------------------------------------------ 
  TRandom *rnd = new TRandom();
  rnd->SetSeed(0);
  TFile *outf = new TFile(OutputFileName.c_str(),"RECREATE");
  TFile *infGen  = new TFile(InputSpectrum.c_str());
  TFile *dataf = new TFile(InputFileName.c_str());
  TH1F *hData[BIN];
  TH1F *hTrue_Toy_MC[BIN];
  TH1F *hTrue_Toy_MC_Smeared[BIN];
  TCanvas *c[BIN];
  gDirectory->pwd();
  TH1F *hMCGen[BIN];
  TF1 *fSpectrum_aux[BIN];
  TF1 *fSigma[BIN];
  TCanvas *can[BIN];
  TH1F *hist_aux = new TH1F("aux","aux",npTBins,pTBnd);
  RooUnfoldResponse *RESP_MATRIX[BIN];
  TH2D *ResponseMatrix[BIN];
  TString YBIN[] = {"Ybin0","Ybin1","Ybin2","Ybin3","Ybin4","Ybin5"};
  
  std::vector<RooUnfoldResponse> Response[BIN];
  std::vector<TF1> fSpectrum[BIN];
  
  TH1F *ForwardSmearing_gen[9];
  TH1F *ForwardSmearing_smeared[9];
  
  for(int iy=0;iy<BIN;iy++) {
    sprintf(name,"True from Toy MC_Ybin%d",iy);
    hTrue_Toy_MC[iy]         = new TH1F(name,name,npTBins,pTBnd);
    hTrue_Toy_MC[iy]->Sumw2();
    
    sprintf(name,"True from Toy MC_Smeared_Ybin%d",iy);
    hTrue_Toy_MC_Smeared[iy] = new TH1F(name,name,npTBins,pTBnd);
    hTrue_Toy_MC_Smeared[iy]->Sumw2();
    
    
    sprintf(name,"%d",iy);
    hInputSpectrum +=name;
    cout<<hInputSpectrum.c_str()<<endl;
    hMCGen[iy]  = (TH1F*)infGen->FindObjectAny(hInputSpectrum.c_str());
    hInputSpectrum.erase(hInputSpectrum.size()-1,hInputSpectrum.size());
    
    for(int variation=0;variation<9;variation++)
    
      {
	// fSpectrum are the spectra from reco-level MC ??? 
        sprintf(name,"fSpectrum_%d_Ybin%d",variation,iy);
        fSpectrum_aux[iy] = new TF1(name,fInputSpectrum.c_str(),0,2800);
        fSpectrum[iy].assign(variation,*(TF1*)fSpectrum_aux[iy]->Clone());
        
        sprintf(name,"ForwardSmearing_gen_%d_Ybin%d",variation,iy);
        ForwardSmearing_gen[variation] = new TH1F(name,name,npTBins,pTBnd);
        ForwardSmearing_gen[variation]->Sumw2();
        
        sprintf(name,"ForwardSmearing_smeared_%d_Ybin%d",variation,iy);
        ForwardSmearing_smeared[variation] = new TH1F(name,name,npTBins,pTBnd);
        ForwardSmearing_smeared[variation]->Sumw2();
      }
    

    sprintf(name,"YBin%d",iy);;
    can[iy]= new TCanvas(name);
    hMCGen[iy]->Draw();
    fSpectrum_aux[iy]->SetParameters(1e-7,4.5,9);
    hMCGen[iy]->Fit(fSpectrum_aux[iy],"RQN");
    hMCGen[iy]->GetXaxis()->SetTitle("p_{T} (TeV)");
    hMCGen[iy]->GetYaxis()->SetTitle("d^{2}#sigma/p_{T}d|y| (pb/TeV)");
    TPaveText *pave3 = new TPaveText(0.25,0.84,0.39,0.93,"NDC");
    pave3->AddText(name);
    pave3->SetFillColor(0);
    pave3->SetLineColor(0);
    pave3->SetBorderSize(0);
    pave3->SetFillStyle(0);
    pave3->SetTextFont(42);
    pave3->SetTextSize(0.05);
    pave3->SetTextAlign(12);
    pave3->Draw("same");
    
    c[iy]= new TCanvas(name);
    gPad->SetLogx();
    gPad->SetLogy();
    hMCGen[iy]->Fit(fSpectrum_aux[iy],"RQ");
    fSpectrum[iy].at(0).SetRange(0,3500);
    
    sprintf(name,"Resolution_Ybin%d",iy);
    fSigma[iy]= new TF1(name,Resolution.c_str(),0.,5.);
    
    for(int variation=0;variation<9;variation++)
    
      {
        sprintf(name,"ResponseMatrix_%d_Ybin%d",variation,iy);
        RESP_MATRIX[iy]= new RooUnfoldResponse(hist_aux,hist_aux,name);
        
        Response[iy].push_back(*RESP_MATRIX[iy]);      
      }

    
    for(int i=0;i<3;i++)
      {
	fSigma[iy]     ->SetParameter(i,PARAM[iy][i]);
     
	if(i==1 || i==2)
	  {
	    fSpectrum[iy].at(0).SetParameter(i,1.00*fSpectrum_aux[iy]->GetParameter(i));
	    fSpectrum[iy].at(1).SetParameter(i,1.05*fSpectrum_aux[iy]->GetParameter(i));
	    fSpectrum[iy].at(2).SetParameter(i,0.95*fSpectrum_aux[iy]->GetParameter(i));
	  }
	else
	  { 
	    fSpectrum[iy].at(0).SetParameter(i,fSpectrum_aux[iy]->GetParameter(i));
	    fSpectrum[iy].at(1).SetParameter(i,fSpectrum_aux[iy]->GetParameter(i));
	    fSpectrum[iy].at(2).SetParameter(i,fSpectrum_aux[iy]->GetParameter(i));
	  }
      }
 
    for(int i=0;i<NEVENTS;i++) {
      if (i!=0 && i%(NEVENTS/10)==0)
	{
	  cout<<10*i/NEVENTS<<" M"<<endl;
	}

      // m is the x-axis value
      double m      = rnd->Uniform(0.,3500.);

      // d is the width of the bin corresponding to mass m
      double d      = hist_aux->GetBinWidth(hist_aux->FindBin(m/1000.));
      
      // fSigma[i] is the resolution function for ith rapidity bin
      // x_i are the smeared deviates
      double x_1 = rnd->Gaus(m,m*fSigma[iy]->Eval(m/1000.));
      double x_2 = rnd->Gaus(m,1.10*m*fSigma[iy]->Eval(m/1000.));
      double x_3 = rnd->Gaus(m,0.95*m*fSigma[iy]->Eval(m/1000.));
      
      // fSpectrum is the observed spectrum in MC (reconstructed? or gen? Dunno yet). 
      // w_i is the weight for that histogram bin
      double w_1 = fSpectrum[iy].at(0).Eval(m);
      double w_2 = fSpectrum[iy].at(1).Eval(m);
      double w_3 = fSpectrum[iy].at(2).Eval(m);
      
      if(m>0. && m<4000.)
        {
          hTrue_Toy_MC[iy]        ->Fill(m/1000.,w_1/d);
          hTrue_Toy_MC_Smeared[iy]->Fill(x_1/1000.,w_1/d);
          
          Response[iy].at(0).Fill(x_1/1000.,m/1000.,w_1/d);
          Response[iy].at(1).Fill(x_2/1000.,m/1000.,w_1/d);
          Response[iy].at(2).Fill(x_3/1000.,m/1000.,w_1/d);
          
          Response[iy].at(3).Fill(x_1/1000.,m/1000.,w_2/d);
          Response[iy].at(4).Fill(x_2/1000.,m/1000.,w_2/d);
          Response[iy].at(5).Fill(x_3/1000.,m/1000.,w_2/d);
          
          Response[iy].at(6).Fill(x_1/1000.,m/1000.,w_3/d);
          Response[iy].at(7).Fill(x_2/1000.,m/1000.,w_3/d);
          Response[iy].at(8).Fill(x_3/1000.,m/1000.,w_3/d);
          
          ForwardSmearing_gen[0]->Fill(m/1000.,w_1/d);
          ForwardSmearing_gen[1]->Fill(m/1000.,w_1/d);
          ForwardSmearing_gen[2]->Fill(m/1000.,w_1/d);
          
          ForwardSmearing_gen[3]->Fill(m/1000.,w_2/d);
          ForwardSmearing_gen[4]->Fill(m/1000.,w_2/d);
          ForwardSmearing_gen[5]->Fill(m/1000.,w_2/d);
          
          ForwardSmearing_gen[6]->Fill(m/1000.,w_3/d);
          ForwardSmearing_gen[7]->Fill(m/1000.,w_3/d);
          ForwardSmearing_gen[8]->Fill(m/1000.,w_3/d);
          
          ForwardSmearing_smeared[0]->Fill(x_1/1000.,w_1/d);
          ForwardSmearing_smeared[1]->Fill(x_2/1000.,w_1/d);
          ForwardSmearing_smeared[2]->Fill(x_3/1000.,w_1/d);
          
          ForwardSmearing_smeared[3]->Fill(x_1/1000.,w_2/d);
          ForwardSmearing_smeared[4]->Fill(x_2/1000.,w_2/d);
          ForwardSmearing_smeared[5]->Fill(x_3/1000.,w_2/d);
          
          ForwardSmearing_smeared[6]->Fill(x_1/1000.,w_3/d);
          ForwardSmearing_smeared[7]->Fill(x_2/1000.,w_3/d);
          ForwardSmearing_smeared[8]->Fill(x_3/1000.,w_3/d);
          
          
        }
      
    }    
    
    outf->cd();
    fSpectrum[iy].at(0).Write();
    fSpectrum[iy].at(1).Write();
    fSpectrum[iy].at(2).Write();
    
    for(int i=0;i<9;i++)
      {
	ForwardSmearing_gen[i]-> Divide(ForwardSmearing_smeared[i]);
	ForwardSmearing_gen[i]->Write();
      }

    hTrue_Toy_MC[iy]        ->Write();
    hTrue_Toy_MC_Smeared[iy]->Write();
    
    for(int i=0;i<9;i++)
      {
	Response[iy].at(i).Write();
                
      }

  }// y loop

  outf->Close();
}

TH2D* Normalize(TH2D* h, TString type){

  int Nx=h->GetNbinsX();
  int Ny=h->GetNbinsY();
  double check_sum;
  double row_sum;
  double content;
  if(type=="row")
    {
      for(int _column=0;_column<Ny;_column++)
	{
	  row_sum=0;
	  check_sum=0;
                   
	  for(int _row=0;_row<Nx;_row++)
	    {
	      row_sum+=h->GetBinContent(_row,_column);
	    }
                        
	  for(int _row=0;_row<Nx;_row++)
	    {
	      content=h->GetBinContent(_row,_column);
                           
                        
	      if(row_sum!=0) h->SetBinContent(_row,_column,content/row_sum);
	      check_sum+=h->GetBinContent(_row,_column);
                                
	    }
	  cout<<check_sum<<endl;
	}
      cout<<"check is done!"<<endl;
    }

  return h;
}
  
int main(int argc, char**argv)
{

  CreateResponseMatrix(argc, argv);
  return 0;
        
}
