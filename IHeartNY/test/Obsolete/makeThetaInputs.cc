#include "makeThetaInputs.h"

#include "TStyle.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "THStack.h"

#include <iostream>

void setStyle() {
	gStyle->SetOptTitle(0);
	gStyle->SetOptStat(0);
	gStyle->SetOptFit(0);

	gStyle->SetOptStat(000000);

	gStyle->SetTitleFont(43);
	//gStyle->SetTitleFontSize(0.05);
	gStyle->SetTitleFont(43, "XYZ");
	gStyle->SetTitleSize(30, "XYZ");
	gStyle->SetTitleOffset(2.0, "X");
	gStyle->SetTitleOffset(1.25, "Y");
	gStyle->SetLabelFont(43, "XYZ");
	gStyle->SetLabelSize(20, "XYZ");
}

void makeThetaInputs_Singlestage() {

  TH1::AddDirectory(kFALSE); 

	setStyle();

	double nqcd; TString var;
	cout << "hist1 = "; cin >> var;
	cout << "NQCD = "; cin >> nqcd;

	SummedHist * wjets_nom     = getWJets( "nom", var );
	SummedHist * singletop_nom = getSingleTop( "nom", var );
	SummedHist * ttbar_nom     = getTTbar("nom", var );
	SummedHist * ttbar_nonSemiLep_nom     = getTTbarNonSemiLep("nom", var );

	SummedHist * wjets_btagdn     = getWJets( "btagdn", var );
	SummedHist * singletop_btagdn = getSingleTop( "btagdn", var );
	SummedHist * ttbar_btagdn     = getTTbar("btagdn", var );  
	SummedHist * ttbar_nonSemiLep_btagdn     = getTTbarNonSemiLep("btagdn", var );

	SummedHist * wjets_btagup     = getWJets( "btagup", var );
	SummedHist * singletop_btagup = getSingleTop( "btagup", var );
	SummedHist * ttbar_btagup     = getTTbar("btagup", var );  
	SummedHist * ttbar_nonSemiLep_btagup     = getTTbarNonSemiLep("btagup", var );

	SummedHist * wjets_jecdn     = getWJets( "jecdn", var );
	SummedHist * singletop_jecdn = getSingleTop( "jecdn", var );
	SummedHist * ttbar_jecdn     = getTTbar("jecdn", var );  
	SummedHist * ttbar_nonSemiLep_jecdn     = getTTbarNonSemiLep("jecdn", var );

	SummedHist * wjets_jecup     = getWJets( "jecup", var );
	SummedHist * singletop_jecup = getSingleTop( "jecup", var );
	SummedHist * ttbar_jecup     = getTTbar("jecup", var );  
	SummedHist * ttbar_nonSemiLep_jecup     = getTTbarNonSemiLep("jecup", var );

	SummedHist * wjets_jerdn     = getWJets( "jerdn", var );
	SummedHist * singletop_jerdn = getSingleTop( "jerdn", var );
	SummedHist * ttbar_jerdn     = getTTbar("jerdn", var );  
	SummedHist * ttbar_nonSemiLep_jerdn     = getTTbarNonSemiLep("jerdn", var );

	SummedHist * wjets_jerup     = getWJets( "jerup", var );
	SummedHist * singletop_jerup = getSingleTop( "jerup", var );
	SummedHist * ttbar_jerup     = getTTbar("jerup", var );  
	SummedHist * ttbar_nonSemiLep_jerup     = getTTbarNonSemiLep("jerup", var );

	SummedHist * wjets_toptagdn     = getWJets( "toptagdn", var );
	SummedHist * singletop_toptagdn = getSingleTop( "toptagdn", var );
	SummedHist * ttbar_toptagdn     = getTTbar("toptagdn", var );  
	SummedHist * ttbar_nonSemiLep_toptagdn     = getTTbarNonSemiLep("toptagdn", var );

	SummedHist * wjets_toptagup     = getWJets( "toptagup", var );
	SummedHist * singletop_toptagup = getSingleTop( "toptagup", var );
	SummedHist * ttbar_toptagup     = getTTbar("toptagup", var );  
	SummedHist * ttbar_nonSemiLep_toptagup     = getTTbarNonSemiLep("toptagup", var );

	SummedHist * ttbar_pdfup_CT10     = getTTbar("pdfup_CT10", var );  
	SummedHist * ttbar_pdfdn_CT10     = getTTbar("pdfdn_CT10", var );  

	SummedHist * ttbar_pdfup_MSTW     = getTTbar("pdfup_MSTW", var );  
	SummedHist * ttbar_pdfdn_MSTW     = getTTbar("pdfdn_MSTW", var );  

	SummedHist * ttbar_pdfup_NNPDF     = getTTbar("pdfup_NNPDF", var );  
	SummedHist * ttbar_pdfdn_NNPDF     = getTTbar("pdfdn_NNPDF", var );  


	SummedHist * ttbar_scaleup     = getTTbar("scaleup_nom", var );  
	SummedHist * ttbar_scaledown     = getTTbar("scaledown_nom", var );  

	SummedHist * qcd = getQCD( var, nqcd );


	TFile * dataFile = TFile::Open("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root");
	TH1F * data = (TH1F*)dataFile->Get( var );
	data->SetName( var + "__DATA" );

	TString outname ("normalized2d_mujets_");
	outname += var; outname += ".root";
	TFile * fout = new TFile( outname.Data() , "RECREATE");

	fout->cd();

	wjets_nom->hist()->Write();
	singletop_nom->hist()->Write();
	ttbar_nom->hist()->Write();
	ttbar_nonSemiLep_nom->hist()->Write();

	wjets_btagdn->hist()->Write();
	singletop_btagdn->hist()->Write();
	ttbar_btagdn->hist()->Write();
	ttbar_nonSemiLep_btagdn->hist()->Write();

	wjets_btagup->hist()->Write();
	singletop_btagup->hist()->Write();
	ttbar_btagup->hist()->Write();
	ttbar_nonSemiLep_btagup->hist()->Write();

	wjets_toptagdn->hist()->Write();
	singletop_toptagdn->hist()->Write();
	ttbar_toptagdn->hist()->Write();
	ttbar_nonSemiLep_toptagdn->hist()->Write();

	wjets_toptagup->hist()->Write();
	singletop_toptagup->hist()->Write();
	ttbar_toptagup->hist()->Write();
	ttbar_nonSemiLep_toptagup->hist()->Write();


	wjets_jecdn->hist()->Write();
	singletop_jecdn->hist()->Write();
	ttbar_jecdn->hist()->Write();
	ttbar_nonSemiLep_jecdn->hist()->Write();

	wjets_jecup->hist()->Write();
	singletop_jecup->hist()->Write();
	ttbar_jecup->hist()->Write();
	ttbar_nonSemiLep_jecup->hist()->Write();

	wjets_jerdn->hist()->Write();
	singletop_jerdn->hist()->Write();
	ttbar_jerdn->hist()->Write();
	ttbar_nonSemiLep_jerdn->hist()->Write();

	wjets_jerup->hist()->Write();
	singletop_jerup->hist()->Write();
	ttbar_jerup->hist()->Write();
	ttbar_nonSemiLep_jerup->hist()->Write();



	ttbar_pdfup_CT10->hist()->Write();
	ttbar_pdfdn_CT10->hist()->Write();

	ttbar_pdfup_MSTW->hist()->Write();
	ttbar_pdfdn_MSTW->hist()->Write();

	ttbar_pdfup_NNPDF->hist()->Write();
	ttbar_pdfdn_NNPDF->hist()->Write();


	ttbar_scaleup->hist()->Write();
	ttbar_scaledown->hist()->Write();

	qcd->hist()->Write();

	data->Write();

	fout->Close();

}

void makeThetaInputs_subhist() {

TH1::AddDirectory(kFALSE); 

	setStyle();

	double nqcd1 ; double nqcd2 ; 
	TString var1 ; TString var2;
	cout << "hist1 = "; cin >> var1;
	cout << "hist2 = "; cin >> var2;
	cout << "NQCD1 = "; cin >> nqcd1;
	cout << "NQCD2 = "; cin >> nqcd2;
	

	SummedHist * wjets_nom     = getWJets( "nom", var1 );
	SummedHist * singletop_nom = getSingleTop( "nom", var1 );
	SummedHist * ttbar_nom     = getTTbar("nom", var1 );
	SummedHist * ttbar_nonSemiLep_nom     = getTTbarNonSemiLep("nom", var1 );

	SummedHist * wjets_btagdn     = getWJets( "btagdn", var1 );
	SummedHist * singletop_btagdn = getSingleTop( "btagdn", var1 );
	SummedHist * ttbar_btagdn     = getTTbar("btagdn", var1 );  
	SummedHist * ttbar_nonSemiLep_btagdn     = getTTbarNonSemiLep("btagdn", var1 );

	SummedHist * wjets_btagup     = getWJets( "btagup", var1 );
	SummedHist * singletop_btagup = getSingleTop( "btagup", var1 );
	SummedHist * ttbar_btagup     = getTTbar("btagup", var1 );  
	SummedHist * ttbar_nonSemiLep_btagup     = getTTbarNonSemiLep("btagup", var1 );

	SummedHist * wjets_jecdn     = getWJets( "jecdn", var1  );
	SummedHist * singletop_jecdn = getSingleTop( "jecdn", var1  );
	SummedHist * ttbar_jecdn     = getTTbar("jecdn", var1  );  
	SummedHist * ttbar_nonSemiLep_jecdn     = getTTbarNonSemiLep("jecdn" , var1  );

	SummedHist * wjets_jecup     = getWJets( "jecup", var1  );
	SummedHist * singletop_jecup = getSingleTop( "jecup", var1  );
	SummedHist * ttbar_jecup     = getTTbar("jecup", var1  );  
	SummedHist * ttbar_nonSemiLep_jecup     = getTTbarNonSemiLep("jecup", var1  );

	SummedHist * wjets_jerdn     = getWJets( "jerdn", var1  );
	SummedHist * singletop_jerdn = getSingleTop( "jerdn", var1  );
	SummedHist * ttbar_jerdn     = getTTbar("jerdn", var1  );  
	SummedHist * ttbar_nonSemiLep_jerdn     = getTTbarNonSemiLep("jerdn", var1  );

	SummedHist * wjets_jerup     = getWJets( "jerup", var1  );
	SummedHist * singletop_jerup = getSingleTop( "jerup", var1  );
	SummedHist * ttbar_jerup     = getTTbar("jerup", var1  );  
	SummedHist * ttbar_nonSemiLep_jerup     = getTTbarNonSemiLep("jerup", var1  );

	SummedHist * wjets_toptagdn     = getWJets( "toptagdn", var1  );
	SummedHist * singletop_toptagdn = getSingleTop( "toptagdn", var1  );
	SummedHist * ttbar_toptagdn     = getTTbar("toptagdn", var1  );  
	SummedHist * ttbar_nonSemiLep_toptagdn     = getTTbarNonSemiLep("toptagdn", var1  );

	SummedHist * wjets_toptagup     = getWJets( "toptagup", var1  );
	SummedHist * singletop_toptagup = getSingleTop( "toptagup", var1  );
	SummedHist * ttbar_toptagup     = getTTbar("toptagup", var1  );  
	SummedHist * ttbar_nonSemiLep_toptagup     = getTTbarNonSemiLep("toptagup", var1  );

	SummedHist * ttbar_pdfup_CT10     = getTTbar("pdfup_CT10", var1  );  
	SummedHist * ttbar_pdfdn_CT10     = getTTbar("pdfdn_CT10", var1  );  

	SummedHist * ttbar_pdfup_MSTW     = getTTbar("pdfup_MSTW", var1  );  
	SummedHist * ttbar_pdfdn_MSTW     = getTTbar("pdfdn_MSTW", var1  );  

	SummedHist * ttbar_pdfup_NNPDF     = getTTbar("pdfup_NNPDF", var1  );  
	SummedHist * ttbar_pdfdn_NNPDF     = getTTbar("pdfdn_NNPDF", var1  );  


	SummedHist * ttbar_scaleup     = getTTbar("scaleup_nom", var1  );  
	SummedHist * ttbar_scaledown     = getTTbar("scaledown_nom", var1  );  

	SummedHist * qcd = getQCD( var1 , nqcd1 );

	TFile * dataFile = TFile::Open("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root");
	TH1F * data = (TH1F*)dataFile->Get( var1 );
	data->SetName( var1 + "__DATA" );
	
	SummedHist * wjets_nom_2     = getWJets( "nom", var2 );
	SummedHist * singletop_nom_2 = getSingleTop( "nom", var2 );
	SummedHist * ttbar_nom_2     = getTTbar("nom", var2 );
	SummedHist * ttbar_nonSemiLep_nom_2     = getTTbarNonSemiLep("nom", var2 );

	SummedHist * wjets_btagdn_2     = getWJets( "btagdn", var2 );
	SummedHist * singletop_btagdn_2 = getSingleTop( "btagdn", var2 );
	SummedHist * ttbar_btagdn_2     = getTTbar("btagdn", var2 );  
	SummedHist * ttbar_nonSemiLep_btagdn_2     = getTTbarNonSemiLep("btagdn", var2 );

	SummedHist * wjets_btagup_2     = getWJets( "btagup", var2 );
	SummedHist * singletop_btagup_2 = getSingleTop( "btagup", var2 );
	SummedHist * ttbar_btagup_2     = getTTbar("btagup", var2 );  
	SummedHist * ttbar_nonSemiLep_btagup_2     = getTTbarNonSemiLep("btagup", var2 );

	SummedHist * wjets_jecdn_2     = getWJets( "jecdn", var2  );
	SummedHist * singletop_jecdn_2 = getSingleTop( "jecdn", var2  );
	SummedHist * ttbar_jecdn_2     = getTTbar("jecdn", var2  );  
	SummedHist * ttbar_nonSemiLep_jecdn_2     = getTTbarNonSemiLep("jecdn", var2  );

	SummedHist * wjets_jecup_2     = getWJets( "jecup", var2  );
	SummedHist * singletop_jecup_2 = getSingleTop( "jecup", var2  );
	SummedHist * ttbar_jecup_2     = getTTbar("jecup", var2  );  
	SummedHist * ttbar_nonSemiLep_jecup_2     = getTTbarNonSemiLep("jecup", var2  );

	SummedHist * wjets_jerdn_2     = getWJets( "jerdn", var2  );
	SummedHist * singletop_jerdn_2 = getSingleTop( "jerdn", var2  );
	SummedHist * ttbar_jerdn_2     = getTTbar("jerdn", var2  );  
	SummedHist * ttbar_nonSemiLep_jerdn_2     = getTTbarNonSemiLep("jerdn", var2  );

	SummedHist * wjets_jerup_2     = getWJets( "jerup", var2  );
	SummedHist * singletop_jerup_2 = getSingleTop( "jerup", var2  );
	SummedHist * ttbar_jerup_2     = getTTbar("jerup", var2  );  
	SummedHist * ttbar_nonSemiLep_jerup_2     = getTTbarNonSemiLep("jerup", var2  );

	SummedHist * wjets_toptagdn_2     = getWJets( "toptagdn", var2  );
	SummedHist * singletop_toptagdn_2 = getSingleTop( "toptagdn", var2  );
	SummedHist * ttbar_toptagdn_2     = getTTbar("toptagdn", var2  );  
	SummedHist * ttbar_nonSemiLep_toptagdn_2     = getTTbarNonSemiLep("toptagdn", var2  );

	SummedHist * wjets_toptagup_2     = getWJets( "toptagup", var2  );
	SummedHist * singletop_toptagup_2 = getSingleTop( "toptagup", var2  );
	SummedHist * ttbar_toptagup_2     = getTTbar("toptagup", var2  );  
	SummedHist * ttbar_nonSemiLep_toptagup_2     = getTTbarNonSemiLep("toptagup", var2  );

	SummedHist * ttbar_pdfup_CT10_2     = getTTbar("pdfup_CT10", var2  );  
	SummedHist * ttbar_pdfdn_CT10_2     = getTTbar("pdfdn_CT10", var2  );  

	SummedHist * ttbar_pdfup_MSTW_2     = getTTbar("pdfup_MSTW", var2  );  
	SummedHist * ttbar_pdfdn_MSTW_2     = getTTbar("pdfdn_MSTW", var2  );  

	SummedHist * ttbar_pdfup_NNPDF_2     = getTTbar("pdfup_NNPDF", var2  );  
	SummedHist * ttbar_pdfdn_NNPDF_2     = getTTbar("pdfdn_NNPDF", var2  );  


	SummedHist * ttbar_scaleup_2     = getTTbar("scaleup_nom", var2  );  
	SummedHist * ttbar_scaledown_2     = getTTbar("scaledown_nom", var2  );  

	SummedHist * qcd_2 = getQCD( var2 , nqcd2 );

	TFile * dataFile_2 = TFile::Open("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root");
	TH1F * data_2 = (TH1F*)dataFile_2->Get( var2 );
	data_2->SetName( var2 + "__DATA_2" );
	
	
	wjets_nom->hist()     ->Add(wjets_nom_2->hist() , -1.0);
	singletop_nom->hist() ->Add(singletop_nom_2->hist() , -1.0);
	ttbar_nom->hist()     ->Add(ttbar_nom_2->hist() , -1.0);
	ttbar_nonSemiLep_nom->hist() ->Add(ttbar_nonSemiLep_nom_2->hist() , -1.0);
	
	wjets_btagdn->hist()     ->Add(wjets_btagdn_2->hist() , -1.0);
	singletop_btagdn->hist() ->Add(singletop_btagdn_2->hist() , -1.0);
	ttbar_btagdn->hist()     ->Add(ttbar_btagdn_2->hist() , -1.0);
	ttbar_nonSemiLep_btagdn->hist() ->Add(ttbar_nonSemiLep_btagdn_2->hist() , -1.0);

	wjets_btagup->hist()     ->Add(wjets_btagup_2->hist() , -1.0);
	singletop_btagup->hist() ->Add(singletop_btagup_2->hist() , -1.0);
	ttbar_btagup->hist()     ->Add(ttbar_btagup_2->hist() , -1.0);
	ttbar_nonSemiLep_btagup->hist() ->Add(ttbar_nonSemiLep_btagup_2->hist() , -1.0);

	wjets_jecdn->hist()     ->Add(wjets_jecdn_2->hist() , -1.0);
	singletop_jecdn->hist() ->Add(singletop_jecdn_2->hist() , -1.0);
	ttbar_jecdn->hist()     ->Add(ttbar_jecdn_2->hist() , -1.0);
	ttbar_nonSemiLep_jecdn->hist() ->Add(ttbar_nonSemiLep_jecdn_2->hist() , -1.0);

	wjets_jecup->hist()     ->Add(wjets_jecup_2->hist() , -1.0);
	singletop_jecup->hist() ->Add(singletop_jecup_2->hist() , -1.0);
	ttbar_jecup->hist()     ->Add(ttbar_jecup_2->hist() , -1.0);
	ttbar_nonSemiLep_jecup->hist() ->Add(ttbar_nonSemiLep_jecup_2->hist() , -1.0);


	wjets_jerdn->hist()     ->Add(wjets_jerdn_2->hist() , -1.0);
	singletop_jerdn->hist() ->Add(singletop_jerdn_2->hist() , -1.0);
	ttbar_jerdn->hist()     ->Add(ttbar_jerdn_2->hist() , -1.0);
	ttbar_nonSemiLep_jerdn->hist() ->Add(ttbar_nonSemiLep_jerdn_2->hist() , -1.0);

	wjets_jerup->hist()     ->Add(wjets_jerup_2->hist() , -1.0);
	singletop_jerup->hist() ->Add(singletop_jerup_2->hist() , -1.0);
	ttbar_jerup->hist()     ->Add(ttbar_jerup_2->hist() , -1.0);
	ttbar_nonSemiLep_jerup->hist() ->Add(ttbar_nonSemiLep_jerup_2->hist() , -1.0);

	wjets_toptagdn->hist()     ->Add(wjets_toptagdn_2->hist() , -1.0);
	singletop_toptagdn->hist() ->Add(singletop_toptagdn_2->hist() , -1.0);
	ttbar_toptagdn->hist()     ->Add(ttbar_toptagdn_2->hist() , -1.0);
	ttbar_nonSemiLep_toptagdn->hist() ->Add(ttbar_nonSemiLep_toptagdn_2->hist() , -1.0);

	wjets_toptagup->hist()     ->Add(wjets_toptagup_2->hist() , -1.0);
	singletop_toptagup->hist() ->Add(singletop_toptagup_2->hist() , -1.0);
	ttbar_toptagup->hist()     ->Add(ttbar_toptagup_2->hist() , -1.0);
	ttbar_nonSemiLep_toptagup->hist() ->Add(ttbar_nonSemiLep_toptagup_2->hist() , -1.0);

	ttbar_pdfup_CT10->hist() ->Add(ttbar_pdfup_CT10_2->hist() , -1.0);
	ttbar_pdfdn_CT10->hist() ->Add(ttbar_pdfdn_CT10_2->hist() , -1.0);
	
	ttbar_pdfup_MSTW->hist() ->Add(ttbar_pdfup_MSTW_2->hist() , -1.0);
	ttbar_pdfdn_MSTW->hist() ->Add(ttbar_pdfdn_MSTW_2->hist() , -1.0);

	ttbar_pdfup_NNPDF->hist() ->Add(ttbar_pdfup_NNPDF_2->hist() , -1.0);
	ttbar_pdfdn_NNPDF->hist() ->Add(ttbar_pdfdn_NNPDF_2->hist() , -1.0);
		
	ttbar_scaleup->hist()   ->Add(ttbar_scaleup_2->hist() , -1.0);
	ttbar_scaledown->hist() ->Add(ttbar_scaledown_2->hist() , -1.0);

	qcd->hist() ->Add(qcd_2->hist() , -1.0);
	TString name_qcd (var2); name_qcd+="__subtracted__from__"; name_qcd+=var1 ; name_qcd+="__QCD";

	data ->Add(data_2 , -1.0);
	TString name_data (var2); name_data+="__subtracted__from__" ;name_data+=var1 ; name_data+="__DATA";

	
	TString outname ("normalized2d_mujets_");
	outname += var2; outname +="_subtracted_from_" ;outname += var1 ;outname += ".root";
	TFile * fout = new TFile( outname.Data() , "RECREATE");

	fout->cd();

	wjets_nom->hist()->Write();
	singletop_nom->hist()->Write();
	ttbar_nom->hist()->Write();
	ttbar_nonSemiLep_nom->hist()->Write();

	wjets_btagdn->hist()->Write();
	singletop_btagdn->hist()->Write();
	ttbar_btagdn->hist()->Write();
	ttbar_nonSemiLep_btagdn->hist()->Write();

	wjets_btagup->hist()->Write();
	singletop_btagup->hist()->Write();
	ttbar_btagup->hist()->Write();
	ttbar_nonSemiLep_btagup->hist()->Write();

	wjets_toptagdn->hist()->Write();
	singletop_toptagdn->hist()->Write();
	ttbar_toptagdn->hist()->Write();
	ttbar_nonSemiLep_toptagdn->hist()->Write();

	wjets_toptagup->hist()->Write();
	singletop_toptagup->hist()->Write();
	ttbar_toptagup->hist()->Write();
	ttbar_nonSemiLep_toptagup->hist()->Write();

	wjets_jecdn->hist()->Write();
	singletop_jecdn->hist()->Write();
	ttbar_jecdn->hist()->Write();
	ttbar_nonSemiLep_jecdn->hist()->Write();

	wjets_jecup->hist()->Write();
	singletop_jecup->hist()->Write();
	ttbar_jecup->hist()->Write();
	ttbar_nonSemiLep_jecup->hist()->Write();

	wjets_jerdn->hist()->Write();
	singletop_jerdn->hist()->Write();
	ttbar_jerdn->hist()->Write();
	ttbar_nonSemiLep_jerdn->hist()->Write();

	wjets_jerup->hist()->Write();
	singletop_jerup->hist()->Write();
	ttbar_jerup->hist()->Write();
	ttbar_nonSemiLep_jerup->hist()->Write();

	ttbar_pdfup_CT10->hist()->Write();
	ttbar_pdfdn_CT10->hist()->Write();

	ttbar_pdfup_MSTW->hist()->Write();
	ttbar_pdfdn_MSTW->hist()->Write();

	ttbar_pdfup_NNPDF->hist()->Write();
	ttbar_pdfdn_NNPDF->hist()->Write();

	ttbar_scaleup->hist()->Write();
	ttbar_scaledown->hist()->Write();

	qcd->hist()->Write();

	data->Write();


	fout->Close();

}

