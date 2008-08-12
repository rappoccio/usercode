#include "DataFormats/FWLite/interface/Handle.h"


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/FlavorHistory.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "Math/VectorUtil.h"
#include "TH1.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLorentzVector.h"
#endif

#include <iostream>

using namespace std;

void plot_deltaR()
{
   
   
  TFile  * file = new TFile("/uscms_data/d1/rappocc/wbb_patLayer1.root");

  using namespace std;

  TH1D * hist_nbb = new TH1D("hist_nbb", "Number of b #bar{b} pairs", 5, 0, 5);
  TH1D * hist_dr_bb = new TH1D("hist_dr_bb", "#Delta R between b #bar{b} pair", 50, 0, 5 );
  TH1D * hist_m_bb = new TH1D("hist_m_bb", "Invariant mass of b #bar{b} pair", 50, 0, 50 );

  fwlite::Event ev(file);
  
  for( ev.toBegin();
          ! ev.atEnd();
          ++ev) {


    fwlite::Handle<vector<reco::FlavorHistory> > h_bfh;

    h_bfh   .getByLabel(ev,"bFlavorHistoryProducer", "bPartonFlavorHistory");

    hist_nbb->Fill( h_bfh.ptr()->size() );
    
    
    if ( h_bfh.ptr()->size() == 2 ) {
      reco::CandidatePtr parton = h_bfh.ptr()->at(0).parton();
      reco::CandidatePtr sister = h_bfh.ptr()->at(0).sister();
    

      ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > p4_1 = parton->p4();
      ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > p4_2 = sister->p4();

      TLorentzVector ip4_1(p4_1.px(), p4_1.py(), p4_1.pz(), p4_1.e() );
      TLorentzVector ip4_2(p4_2.px(), p4_2.py(), p4_2.pz(), p4_2.e() );

      TLorentzVector p4 = ip4_1 + ip4_2;


      hist_dr_bb->Fill( ROOT::Math::VectorUtil::DeltaR(p4_1, p4_2 ) );
      hist_m_bb->Fill( p4.M() );
    }

  }

  TCanvas *c1 = new TCanvas();
  hist_nbb->Draw();

  TCanvas *c2 = new TCanvas();
  hist_dr_bb->Draw();

  TCanvas *c3 = new TCanvas();
  hist_m_bb->Draw();
}
