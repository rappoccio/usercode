#include "DataFormats/FWLite/interface/Handle.h"


#include "Math/VectorUtil.h"
#include "TH1.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLorentzVector.h"

#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/FlavorHistory.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#endif

#include <iostream>

using namespace std;

void plot_deltaR_fe()
{
   
   
  TFile  * file = new TFile("/uscms_data/d1/rappocc/wjets_patLayer1.root");

  using namespace std;

  TH1D * hist_n_c   = new TH1D("hist_n_c",   "Number of c quarks", 5, 0, 5);
  TH1D * hist_dr_cj = new TH1D("hist_dr_cj", "#Delta R between b #bar{b} pair", 50, 0, 5 );

  fwlite::Event ev(file);
  
  for( ev.toBegin();
          ! ev.atEnd();
          ++ev) {


    fwlite::Handle<vector<reco::FlavorHistory> > h_cfh;
    fwlite::Handle<vector<reco::GenJet> > h_genjets;

    h_cfh    .getByLabel(ev,"cFlavorHistoryProducer", "cPartonFlavorHistory");
    h_genjets.getByLabel(ev,"iterativeCone5GenJets");

    hist_n_c->Fill( h_cfh->size() );
    
    
    if ( h_cfh.ptr()->size() > 0 ) {
      reco::CandidatePtr parton = h_cfh.ptr()->at(0).parton();

      ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > p4_1 = parton->p4();

      double minDR = 999.0;
      for ( int ijet = 0; ijet < h_genjets->size(); ++ijet ) {
	
	ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > p4_2 = h_genjets->at(ijet).p4();
	
	double dr = ROOT::Math::VectorUtil::DeltaR(p4_1, p4_2 );
	if ( dr < minDR ) {
	  minDR = dr;
	}
      }
      hist_dr_cj->Fill( minDR );
    }
  }

  TCanvas *c1 = new TCanvas();
  hist_n_c->Draw();

  TCanvas *c2 = new TCanvas();
  hist_dr_cj->Draw();

}
