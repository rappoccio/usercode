#ifndef makeThetaInputs_h
#define makeThetaInputs_h

#include <TH1.h>
#include <TString.h>
#include <TColor.h>
#include <TFile.h>
#include <TROOT.h>
#include <Rtypes.h>
#include <vector>
#include <iostream>

class SummedHist {
	public : 
	SummedHist( TString const & name, int color ) : name_(name), color_(color) {
		summedHist_ = 0;
	};

	TH1F * hist() { 
		if ( summedHist_ != 0 ) {
			return summedHist_; 
		}
		else if ( hists_.size() == 0 ) {
			return 0; 
		} else {
				summedHist_ = (TH1F*)hists_[0]->Clone();
				summedHist_->SetName( name_ );
				summedHist_->SetFillColor( color_ );
				for ( unsigned int j = 1; j < hists_.size(); ++j ) {
					summedHist_->Add( hists_[j], 1.0 );
				}
		return summedHist_; 
		};
	}

	std::vector<TH1F*> const & hists() const {
	return hists_;
	}

	void push_back( TH1F const * ihist, double norm ) {
		TH1F * clone = (TH1F*)ihist->Clone();
		TString iname(name_);
		iname += hists_.size();
		clone->SetName( iname );
		clone->Scale( norm );
		hists_.push_back( clone );
		norms_.push_back( norm );
	};

	protected : 

	std::vector<TH1F*> hists_;
	std::vector<double> norms_;

	TString name_; 
	int color_;
	TH1F * summedHist_; 
  
};

void adjustThetaName( TString & thetaname, TString name ) {
	if      ( name == "nom" ) return;
	else if ( name == "pdfdn" ) thetaname += "__pdf__down";
	else if ( name == "pdfup" ) thetaname += "__pdf__up";
	else if ( name == "pdfup_CT10" ) thetaname += "__pdf_CT10__up";
	else if ( name == "pdfdn_CT10" ) thetaname += "__pdf_CT10__down";
	else if ( name == "pdfup_MSTW" ) thetaname += "__pdf_MSTW__up";
	else if ( name == "pdfdn_MSTW" ) thetaname += "__pdf_MSTW__down";
	else if ( name == "pdfup_NNPDF" ) thetaname += "__pdf_NNPDF__up";
	else if ( name == "pdfdn_NNPDF" ) thetaname += "__pdf_NNPDF__down";
	else if ( name == "jecdn" ) thetaname += "__jec__down";
	else if ( name == "jecup" ) thetaname += "__jec__up";
	else if ( name == "jerdn" ) thetaname += "__jer__down";
	else if ( name == "jerup" ) thetaname += "__jer__up";
	else if ( name == "scaledown_nom" ) thetaname += "__scale__down";
	else if ( name == "scaleup_nom" ) thetaname += "__scale__up";
	else if ( name == "toptagdn" ) thetaname += "__toptag__down";
	else if ( name == "toptagup" ) thetaname += "__toptag__up";
	else if ( name == "btagdn" ) thetaname += "__btag__down";
	else if ( name == "btagup" ) thetaname += "__btag__up";
	else if ( name == "qcd" ) thetaname += "qcd";
	else {
		std::cerr << "name is " << name << std::endl;
		std::cerr << "Problem in adjusting theta name  " << thetaname << " ! broken!" << std::endl;
	}
	return;
}

const double LUM = 19.7;

SummedHist * getWJets( TString name, TString histname ){
	TString wjets_names[] = {
		"histfiles/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_",
		"histfiles/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_",
		"histfiles/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_",
		"histfiles/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_",
	};
	double wjets_norms[] = {
		5400. * 1.207 * 1000. * LUM / 23141598.,       // W+1 jets
		1750. * 1.207 * 1000. * LUM / 34044921.,       // W+2 jets
		519. * 1.207 * 1000. * LUM  / 15539503.,       // W+3 jets
		214. * 1.207 * 1000. * LUM  / 13382803.        // W+4 jets
	};
	const int nwjets = sizeof( wjets_norms) / sizeof(double);
	TString thetaname = histname + "__WJets";
	adjustThetaName( thetaname, name );
	SummedHist * wjets = new SummedHist( thetaname, kGreen-3 );
	for ( int i = 0 ; i < nwjets; ++i ) {
		TString iname = wjets_names[i] + name + TString(".root");
		TFile * infile = TFile::Open( iname );
		TH1F * hist = (TH1F*) infile->Get(histname);
		wjets->push_back( hist, wjets_norms[i] );
	}
	return wjets;
}



SummedHist * getSingleTop( TString name, TString histname ){
	TString singletop_names[] = {
		"histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
	};
	double singletop_norms[] = {
		3.79 * 1000. * LUM    / 259961.  , // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
		1.76 * 1000. * LUM    / 139974.  , // 
		56.4 * 1000. * LUM    / 3758227. , // 
		30.7 * 1000. * LUM    / 1935072. , // All single-top approx NNLO cross sections from
		11.1 * 1000. * LUM    / 497658.  , // 
		11.1 * 1000. * LUM    / 493460.  , //     
	};
	const int nsingletop = sizeof( singletop_norms) / sizeof(double);
	TString thetaname = histname + "__SingleTop";
	adjustThetaName( thetaname, name );
	SummedHist * singletop = new SummedHist( thetaname, 6 );
	for ( int i = 0 ; i < nsingletop; ++i ) {
		TString iname = singletop_names[i] + name + TString(".root");
		TFile * infile = TFile::Open( iname );
		TH1F * hist = (TH1F*) infile->Get(histname);
		singletop->push_back( hist, singletop_norms[i] );
	}
	return singletop;
}



SummedHist * getTTbarNonSemiLep( TString name, TString histname ){
	TString ttbar_names[] = {
		"histfiles/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"
	};
	double ttbar_xs[] = {
		245.8 * 1000. * LUM,  // nominal
		252.0 * 1000. * LUM,  // q2 up
		237.4 * 1000. * LUM   // q2 down
	};
	double ttbar_nevents[][3] = {
		{21675970.,3082812.,1249111.},  // nominal
		{14998720.,2243672.,1241650.},  // q2 up
		{14998606.,2170074.,1308090.},  // q2 down
	};
	double ttbar_eff[][3] = {
		{1.0, 0.074, 0.015},  // nominal
		{1.0, 0.074, 0.014},  // q2 up
		{1.0, 0.081, 0.016},  // q2 down
	};
	unsigned int iq2 = 0;
	if ( name == "scaleup_nom" ) iq2 = 1;
	if ( name == "scaledown_nom")iq2 = 2;

	const int nttbar = 3;
	double ttbar_norms[nttbar] = {
		ttbar_xs[iq2] * ttbar_eff[iq2][0] / ttbar_nevents[iq2][0],
		ttbar_xs[iq2] * ttbar_eff[iq2][1] / ttbar_nevents[iq2][1],
		ttbar_xs[iq2] * ttbar_eff[iq2][2] / ttbar_nevents[iq2][2],
	};
	TString thetaname = histname + "__TTbar_nonSemiLep";
	adjustThetaName( thetaname, name );
	SummedHist * ttbar = new SummedHist( thetaname, kRed +1);
	for ( int i = 0 ; i < nttbar; ++i ) {
		TString iname = ttbar_names[i] + name + TString(".root");
		TFile * infile = TFile::Open( iname );
		TH1F * hist = (TH1F*) infile->Get(histname);
		ttbar->push_back( hist, ttbar_norms[i] );
	}
	return ttbar;
}


SummedHist * getTTbar( TString name, TString histname ){
	TString ttbar_names[] = {
		"histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_",
		"histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"
	};
	double ttbar_xs[] = {
		245.8 * 1000. * LUM,  // nominal
		252.0 * 1000. * LUM,  // q2 up
		237.4 * 1000. * LUM   // q2 down
	};
	double ttbar_nevents[][3] = {
		{21675970.,3082812.,1249111.},  // nominal
		{14998720.,2243672.,1241650.},  // q2 up
		{14998606.,2170074.,1308090.},  // q2 down
	};
	double ttbar_eff[][3] = {
		{1.0, 0.074, 0.015},  // nominal
		{1.0, 0.074, 0.014},  // q2 up
		{1.0, 0.081, 0.016},  // q2 down
	};
	unsigned int iq2 = 0;
	if ( name == "scaleup_nom" ) iq2 = 1;
	if ( name == "scaledown_nom")iq2 = 2;

	const int nttbar = 3;
	double ttbar_norms[nttbar] = {
		ttbar_xs[iq2] * ttbar_eff[iq2][0] / ttbar_nevents[iq2][0],
		ttbar_xs[iq2] * ttbar_eff[iq2][1] / ttbar_nevents[iq2][1],
		ttbar_xs[iq2] * ttbar_eff[iq2][2] / ttbar_nevents[iq2][2],
	};
	TString thetaname = histname + "__TTbar";
	adjustThetaName( thetaname, name );
	SummedHist * ttbar = new SummedHist( thetaname, kRed +1);
	for ( int i = 0 ; i < nttbar; ++i ) {
		TString iname = ttbar_names[i] + name + TString(".root");
		TFile * infile = TFile::Open( iname );
		TH1F * hist = (TH1F*) infile->Get(histname);
		ttbar->push_back( hist, ttbar_norms[i] );
	}
	return ttbar;
}

SummedHist * getQCD( TString var, double norm ){
	SummedHist * wjets_qcd = getWJets( "qcd", var );
	SummedHist * singletop_qcd = getSingleTop( "qcd", var );
	SummedHist * ttbar_qcd = getTTbar( "qcd", var );

	SummedHist * qcd = new SummedHist( var + "__QCD", 5 );

	TFile * qcdFile = TFile::Open("histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd.root");
	TH1F * qcdHistRaw = (TH1F*)qcdFile->Get(var);

	qcdHistRaw->Add( wjets_qcd->hist(), -1.0 );
	qcdHistRaw->Add( singletop_qcd->hist(), -1.0 );
	qcdHistRaw->Add( ttbar_qcd->hist(), -1.0 );

	for ( int ibin = 0; ibin < qcdHistRaw->GetNbinsX(); ++ibin ) {
		if ( qcdHistRaw->GetBinContent(ibin) < 0.0 ) qcdHistRaw->SetBinContent(ibin, 0.0);    
	}
  
	qcd->push_back( qcdHistRaw, norm / qcdHistRaw->GetSum() );


	return qcd;

}



#endif
