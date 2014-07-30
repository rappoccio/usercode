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


	TFile * dataFile = TFile::Open("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root");
	TH1F * data = (TH1F*)dataFile->Get( var );
	data->SetName( var + "__DATA" );

	TString outname ("normalized_mujets_");
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

	TFile * dataFile = TFile::Open("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root");
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

	TFile * dataFile_2 = TFile::Open("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root");
	TH1F * data_2 = (TH1F*)dataFile_2->Get( var2 );
	data_2->SetName( var2 + "__DATA_2" );
	
	
	wjets_nom->hist()     ->Add(wjets_nom_2->hist() , -1.0);
	singletop_nom->hist() ->Add(singletop_nom_2->hist() , -1.0);
	ttbar_nom->hist()     ->Add(ttbar_nom_2->hist() , -1.0);
	ttbar_nonSemiLep_nom->hist() ->Add(ttbar_nonSemiLep_nom_2->hist() , -1.0);
	TString name_wjets     (var2); name_wjets +="__subtracted__from__" ; name_wjets+= var1; name_wjets+= "__WJets" ;
	TString name_singletop (var2); name_singletop +="__subtracted__from__" ; name_singletop+= var1; name_singletop+= "__SingleTop" ;
	TString name_ttbar     (var2); name_ttbar +="__subtracted__from__" ; name_ttbar += var1; name_ttbar += "__TTbar" ;
	TString name_ttbar_nonSemiLep (var2); name_ttbar_nonSemiLep +="__subtracted__from__" ; name_ttbar_nonSemiLep += var1; name_ttbar_nonSemiLep += "__TTbar__nonSemiLep" ;
	wjets_nom->hist()     ->SetName( name_wjets );
	singletop_nom->hist() ->SetName( name_singletop );
	ttbar_nom->hist()     ->SetName( name_ttbar );
	ttbar_nonSemiLep_nom->hist() ->SetName( name_ttbar_nonSemiLep );
	
	wjets_btagdn->hist()     ->Add(wjets_btagdn_2->hist() , -1.0);
	singletop_btagdn->hist() ->Add(singletop_btagdn_2->hist() , -1.0);
	ttbar_btagdn->hist()     ->Add(ttbar_btagdn_2->hist() , -1.0);
	ttbar_nonSemiLep_btagdn->hist() ->Add(ttbar_nonSemiLep_btagdn_2->hist() , -1.0);
	TString name_wjets_btagdn     (var2); name_wjets_btagdn+= "__subtracted__from__" ; name_wjets_btagdn+= var1; name_wjets_btagdn+= "__WJets__btag__dn" ;
	TString name_singletop_btagdn (var2); name_singletop_btagdn+= "__subtracted__from__" ; name_singletop_btagdn+= var1; name_singletop_btagdn+= "__SingleTop__btag__dn" ;
	TString name_ttbar_btagdn     (var2); name_ttbar_btagdn+= "__subtracted__from__" ; name_ttbar_btagdn+= var1; name_ttbar_btagdn+= "__TTbar__btag__dn" ;
	TString name_ttbar_nonSemiLep_btagdn (var2); name_ttbar_nonSemiLep_btagdn +="__subtracted__from__" ; name_ttbar_nonSemiLep_btagdn+= var1; name_ttbar_nonSemiLep_btagdn+= "__TTbar__nonSemiLep__btag__dn" ;
	wjets_btagdn->hist()     ->SetName( name_wjets_btagdn );
	singletop_btagdn->hist() ->SetName( name_singletop_btagdn );
	ttbar_btagdn->hist()     ->SetName( name_ttbar_btagdn );
	ttbar_nonSemiLep_btagdn->hist() ->SetName( name_ttbar_nonSemiLep_btagdn );

	wjets_btagup->hist()     ->Add(wjets_btagup_2->hist() , -1.0);
	singletop_btagup->hist() ->Add(singletop_btagup_2->hist() , -1.0);
	ttbar_btagup->hist()     ->Add(ttbar_btagup_2->hist() , -1.0);
	ttbar_nonSemiLep_btagup->hist() ->Add(ttbar_nonSemiLep_btagup_2->hist() , -1.0);
	TString name_wjets_btagup     (var2); name_wjets_btagup+= "__subtracted__from__" ; name_wjets_btagup+= var1; name_wjets_btagup+= "__WJets__btag__dn" ;
	TString name_singletop_btagup (var2); name_singletop_btagup+= "__subtracted__from__" ; name_singletop_btagup+= var1; name_singletop_btagup+= "__SingleTop__btag__dn" ;
	TString name_ttbar_btagup     (var2); name_ttbar_btagup+= "__subtracted__from__" ; name_ttbar_btagup+= var1; name_ttbar_btagup+= "__TTbar__btag__dn" ;
	TString name_ttbar_nonSemiLep_btagup (var2); name_ttbar_nonSemiLep_btagup +="__subtracted__from__" ; name_ttbar_nonSemiLep_btagup+= var1; name_ttbar_nonSemiLep_btagup+= "__TTbar__nonSemiLep__btag__dn" ;
	wjets_btagup->hist()     ->SetName( name_wjets_btagup );
	singletop_btagup->hist() ->SetName( name_singletop_btagup );
	ttbar_btagup->hist()     ->SetName( name_ttbar_btagup );
	ttbar_nonSemiLep_btagup->hist() ->SetName( name_ttbar_nonSemiLep_btagup );

	wjets_jecdn->hist()     ->Add(wjets_jecdn_2->hist() , -1.0);
	singletop_jecdn->hist() ->Add(singletop_jecdn_2->hist() , -1.0);
	ttbar_jecdn->hist()     ->Add(ttbar_jecdn_2->hist() , -1.0);
	ttbar_nonSemiLep_jecdn->hist() ->Add(ttbar_nonSemiLep_jecdn_2->hist() , -1.0);
	TString name_wjets_jecdn     (var2); name_wjets_jecdn+= "__subtracted__from__" ; name_wjets_jecdn+= var1; name_wjets_jecdn+= "__WJets__btag__dn" ;
	TString name_singletop_jecdn (var2); name_singletop_jecdn+= "__subtracted__from__" ; name_singletop_jecdn+= var1; name_singletop_jecdn+= "__SingleTop__btag__dn" ;
	TString name_ttbar_jecdn     (var2); name_ttbar_jecdn+= "__subtracted__from__" ; name_ttbar_jecdn+= var1; name_ttbar_jecdn+= "__TTbar__btag__dn" ;
	TString name_ttbar_nonSemiLep_jecdn (var2); name_ttbar_nonSemiLep_jecdn +="__subtracted__from__" ; name_ttbar_nonSemiLep_jecdn+= var1; name_ttbar_nonSemiLep_jecdn+= "__TTbar__nonSemiLep__btag__dn" ;
	wjets_jecdn->hist()     ->SetName( name_wjets_jecdn );
	singletop_jecdn->hist() ->SetName( name_singletop_jecdn );
	ttbar_jecdn->hist()     ->SetName( name_ttbar_jecdn );
	ttbar_nonSemiLep_jecdn->hist() ->SetName( name_ttbar_nonSemiLep_jecdn );

	wjets_jecup->hist()     ->Add(wjets_jecup_2->hist() , -1.0);
	singletop_jecup->hist() ->Add(singletop_jecup_2->hist() , -1.0);
	ttbar_jecup->hist()     ->Add(ttbar_jecup_2->hist() , -1.0);
	ttbar_nonSemiLep_jecup->hist() ->Add(ttbar_nonSemiLep_jecup_2->hist() , -1.0);
	TString name_wjets_jecup     (var2); name_wjets_jecup+= "__subtracted__from__" ; name_wjets_jecup+= var1; name_wjets_jecup+= "__WJets__btag__dn" ;
	TString name_singletop_jecup (var2); name_singletop_jecup+= "__subtracted__from__" ; name_singletop_jecup+= var1; name_singletop_jecup+= "__SingleTop__btag__dn" ;
	TString name_ttbar_jecup     (var2); name_ttbar_jecup+= "__subtracted__from__" ; name_ttbar_jecup+= var1; name_ttbar_jecup+= "__TTbar__btag__dn" ;
	TString name_ttbar_nonSemiLep_jecup (var2); name_ttbar_nonSemiLep_jecup +="__subtracted__from__" ; name_ttbar_nonSemiLep_jecup+= var1; name_ttbar_nonSemiLep_jecup+= "__TTbar__nonSemiLep__btag__dn" ;
	wjets_jecup->hist()     ->SetName( name_wjets_jecup );
	singletop_jecup->hist() ->SetName( name_singletop_jecup );
	ttbar_jecup->hist()     ->SetName( name_ttbar_jecup );
	ttbar_nonSemiLep_jecup->hist() ->SetName( name_ttbar_nonSemiLep_jecup );


	wjets_jerdn->hist()     ->Add(wjets_jerdn_2->hist() , -1.0);
	singletop_jerdn->hist() ->Add(singletop_jerdn_2->hist() , -1.0);
	ttbar_jerdn->hist()     ->Add(ttbar_jerdn_2->hist() , -1.0);
	ttbar_nonSemiLep_jerdn->hist() ->Add(ttbar_nonSemiLep_jerdn_2->hist() , -1.0);
	TString name_wjets_jerdn     (var2); name_wjets_jerdn+= "__subtracted__from__" ; name_wjets_jerdn+= var1; name_wjets_jerdn+= "__WJets__btag__dn" ;
	TString name_singletop_jerdn (var2); name_singletop_jerdn+= "__subtracted__from__" ; name_singletop_jerdn+= var1; name_singletop_jerdn+= "__SingleTop__btag__dn" ;
	TString name_ttbar_jerdn     (var2); name_ttbar_jerdn+= "__subtracted__from__" ; name_ttbar_jerdn+= var1; name_ttbar_jerdn+= "__TTbar__btag__dn" ;
	TString name_ttbar_nonSemiLep_jerdn (var2); name_ttbar_nonSemiLep_jerdn +="__subtracted__from__" ; name_ttbar_nonSemiLep_jerdn+= var1; name_ttbar_nonSemiLep_jerdn+= "__TTbar__nonSemiLep__btag__dn" ;
	wjets_jerdn->hist()     ->SetName( name_wjets_jerdn );
	singletop_jerdn->hist() ->SetName( name_singletop_jerdn );
	ttbar_jerdn->hist()     ->SetName( name_ttbar_jerdn );
	ttbar_nonSemiLep_jerdn->hist() ->SetName( name_ttbar_nonSemiLep_jerdn );

	wjets_jerup->hist()     ->Add(wjets_jerup_2->hist() , -1.0);
	singletop_jerup->hist() ->Add(singletop_jerup_2->hist() , -1.0);
	ttbar_jerup->hist()     ->Add(ttbar_jerup_2->hist() , -1.0);
	ttbar_nonSemiLep_jerup->hist() ->Add(ttbar_nonSemiLep_jerup_2->hist() , -1.0);
	TString name_wjets_jerup     (var2); name_wjets_jerup+= "__subtracted__from__" ; name_wjets_jerup+= var1; name_wjets_jerup+= "__WJets__btag__dn" ;
	TString name_singletop_jerup (var2); name_singletop_jerup+= "__subtracted__from__" ; name_singletop_jerup+= var1; name_singletop_jerup+= "__SingleTop__btag__dn" ;
	TString name_ttbar_jerup     (var2); name_ttbar_jerup+= "__subtracted__from__" ; name_ttbar_jerup+= var1; name_ttbar_jerup+= "__TTbar__btag__dn" ;
	TString name_ttbar_nonSemiLep_jerup (var2); name_ttbar_nonSemiLep_jerup +="__subtracted__from__" ; name_ttbar_nonSemiLep_jerup+= var1; name_ttbar_nonSemiLep_jerup+= "__TTbar__nonSemiLep__btag__dn" ;
	wjets_jerup->hist()     ->SetName( name_wjets_jerup );
	singletop_jerup->hist() ->SetName( name_singletop_jerup );
	ttbar_jerup->hist()     ->SetName( name_ttbar_jerup );
	ttbar_nonSemiLep_jerup->hist() ->SetName( name_ttbar_nonSemiLep_jerup );

	wjets_toptagdn->hist()     ->Add(wjets_toptagdn_2->hist() , -1.0);
	singletop_toptagdn->hist() ->Add(singletop_toptagdn_2->hist() , -1.0);
	ttbar_toptagdn->hist()     ->Add(ttbar_toptagdn_2->hist() , -1.0);
	ttbar_nonSemiLep_toptagdn->hist() ->Add(ttbar_nonSemiLep_toptagdn_2->hist() , -1.0);
	TString name_wjets_toptagdn     (var2); name_wjets_toptagdn+= "__subtracted__from__" ; name_wjets_toptagdn+= var1; name_wjets_toptagdn+= "__WJets__toptag__dn" ;
	TString name_singletop_toptagdn (var2); name_singletop_toptagdn+= "__subtracted__from__" ; name_singletop_toptagdn+= var1; name_singletop_toptagdn+= "__SingleTop__toptag__dn" ;
	TString name_ttbar_toptagdn     (var2); name_ttbar_toptagdn+= "__subtracted__from__" ; name_ttbar_toptagdn+= var1; name_ttbar_toptagdn+= "__TTbar__toptag__dn" ;
	TString name_ttbar_nonSemiLep_toptagdn (var2); name_ttbar_nonSemiLep_toptagdn +="__subtracted__from__" ; name_ttbar_nonSemiLep_toptagdn+= var1; name_ttbar_nonSemiLep_toptagdn+= "__TTbar__nonSemiLep__toptag__dn" ;
	wjets_toptagdn->hist()     ->SetName( name_wjets_toptagdn );
	singletop_toptagdn->hist() ->SetName( name_singletop_toptagdn );
	ttbar_toptagdn->hist()     ->SetName( name_ttbar_toptagdn );
	ttbar_nonSemiLep_toptagdn->hist() ->SetName( name_ttbar_nonSemiLep_toptagdn );

	wjets_toptagup->hist()     ->Add(wjets_toptagup_2->hist() , -1.0);
	singletop_toptagup->hist() ->Add(singletop_toptagup_2->hist() , -1.0);
	ttbar_toptagup->hist()     ->Add(ttbar_toptagup_2->hist() , -1.0);
	ttbar_nonSemiLep_toptagup->hist() ->Add(ttbar_nonSemiLep_toptagup_2->hist() , -1.0);
	TString name_wjets_toptagup     (var2); name_wjets_toptagup+= "__subtracted__from__" ; name_wjets_toptagup+= var1; name_wjets_toptagup+= "__WJets__toptag__dn" ;
	TString name_singletop_toptagup (var2); name_singletop_toptagup+= "__subtracted__from__" ; name_singletop_toptagup+= var1; name_singletop_toptagup+= "__SingleTop__toptag__dn" ;
	TString name_ttbar_toptagup     (var2); name_ttbar_toptagup+= "__subtracted__from__" ; name_ttbar_toptagup+= var1; name_ttbar_toptagup+= "__TTbar__toptag__dn" ;
	TString name_ttbar_nonSemiLep_toptagup (var2); name_ttbar_nonSemiLep_toptagup +="__subtracted__from__" ; name_ttbar_nonSemiLep_toptagup+= var1; name_ttbar_nonSemiLep_toptagup+= "__TTbar__nonSemiLep__toptag__dn" ;
	wjets_toptagup->hist()     ->SetName( name_wjets_toptagup );
	singletop_toptagup->hist() ->SetName( name_singletop_toptagup );
	ttbar_toptagup->hist()     ->SetName( name_ttbar_toptagup );
	ttbar_nonSemiLep_toptagup->hist() ->SetName( name_ttbar_nonSemiLep_toptagup );

	ttbar_pdfup_CT10->hist() ->Add(ttbar_pdfup_CT10_2->hist() , -1.0);
	ttbar_pdfdn_CT10->hist() ->Add(ttbar_pdfdn_CT10_2->hist() , -1.0);
	TString name_ttbar_pdfup_CT10 (var2); name_ttbar_pdfup_CT10+="__subtracted__from__" ;name_ttbar_pdfup_CT10+=var1 ; name_ttbar_pdfup_CT10+="__TTbar__pdf__up__CT10";
	TString name_ttbar_pdfdn_CT10 (var2); name_ttbar_pdfdn_CT10+="__subtracted__from__" ;name_ttbar_pdfdn_CT10+=var1 ; name_ttbar_pdfdn_CT10+="__TTbar__pdf__dn__CT10";
	ttbar_pdfup_CT10->hist() ->SetName( name_ttbar_pdfup_CT10 );
	ttbar_pdfdn_CT10->hist() ->SetName( name_ttbar_pdfdn_CT10 );
	
	ttbar_pdfup_MSTW->hist() ->Add(ttbar_pdfup_MSTW_2->hist() , -1.0);
	ttbar_pdfdn_MSTW->hist() ->Add(ttbar_pdfdn_MSTW_2->hist() , -1.0);
	TString name_ttbar_pdfup_MSTW (var2); name_ttbar_pdfup_MSTW+="__subtracted__from__" ;name_ttbar_pdfup_MSTW+=var1 ; name_ttbar_pdfup_MSTW+="__TTbar__pdf__up__MSTW";
	TString name_ttbar_pdfdn_MSTW (var2); name_ttbar_pdfdn_MSTW+="__subtracted__from__" ;name_ttbar_pdfdn_MSTW+=var1 ; name_ttbar_pdfdn_MSTW+="__TTbar__pdf__dn__MSTW";
	ttbar_pdfup_MSTW->hist() ->SetName( name_ttbar_pdfup_MSTW );
	ttbar_pdfdn_MSTW->hist() ->SetName( name_ttbar_pdfdn_MSTW );

	ttbar_pdfup_NNPDF->hist() ->Add(ttbar_pdfup_NNPDF_2->hist() , -1.0);
	ttbar_pdfdn_NNPDF->hist() ->Add(ttbar_pdfdn_NNPDF_2->hist() , -1.0);
	TString name_ttbar_pdfup_NNPDF (var2); name_ttbar_pdfup_NNPDF+="__subtracted__from__" ;name_ttbar_pdfup_NNPDF+=var1 ; name_ttbar_pdfup_NNPDF+="__TTbar__pdf__up__NNPDF";
	TString name_ttbar_pdfdn_NNPDF (var2); name_ttbar_pdfdn_NNPDF+="__subtracted__from__" ;name_ttbar_pdfdn_NNPDF+=var1 ; name_ttbar_pdfdn_NNPDF+="__TTbar__pdf__dn__NNPDF";
	ttbar_pdfup_NNPDF->hist() ->SetName( name_ttbar_pdfup_NNPDF );
	ttbar_pdfdn_NNPDF->hist() ->SetName( name_ttbar_pdfdn_NNPDF );
		
	ttbar_scaleup->hist()   ->Add(ttbar_scaleup_2->hist() , -1.0);
	ttbar_scaledown->hist() ->Add(ttbar_scaledown_2->hist() , -1.0);
	TString name_ttbar_scaleup (var2); name_ttbar_scaleup+="__subtracted__from__" ; name_ttbar_scaleup+=var1 ; name_ttbar_scaleup+="__TTbar__Scale__up";
	TString name_ttbar_scaledn (var2); name_ttbar_scaledn+="__subtracted__from__" ; name_ttbar_scaledn+=var1 ; name_ttbar_scaledn+="__TTbar__Scale__dn";
	ttbar_scaleup->hist()   ->SetName( name_ttbar_scaleup );
	ttbar_scaledown->hist() ->SetName( name_ttbar_scaledn );

	qcd->hist() ->Add(qcd_2->hist() , -1.0);
	TString name_qcd (var2); name_qcd+="__subtracted__from__"; name_qcd+=var1 ; name_qcd+="__QCD";
	qcd->hist() ->SetName (name_qcd);

	data ->Add(data_2 , -1.0);
	TString name_data (var2); name_data+="__subtracted__from__" ;name_data+=var1 ; name_data+="__DATA";
	data ->SetName (name_data);

	
	TString outname ("normalized_mujets_");
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

