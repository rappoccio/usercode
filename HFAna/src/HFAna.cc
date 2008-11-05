// -*- C++ -*-
//
// Package:    HFAna
// Class:      HFAna
// 
/**\class HFAna HFAna.cc Analysis/HFAna/src/HFAna.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Tue Jul 29 10:04:34 CDT 2008
// $Id: HFAna.cc,v 1.2 2008/08/03 16:29:59 bazterra Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "PhysicsTools/CandUtils/interface/AddFourMomenta.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/HepMCCandidate/interface/FlavorHistory.h"
#include "DataFormats/BTauReco/interface/TrackIPData.h"

#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "PhysicsTools/UtilAlgos/interface/TFileDirectory.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <vector>

#include <TH1.h>

#include <TMath.h>

//
// class decleration
//

using namespace edm;
using namespace pat;
using namespace std;

class HFAna : public edm::EDAnalyzer {
   public:
      explicit HFAna(const edm::ParameterSet&);
      ~HFAna();


   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------

  InputTag     src_;
  InputTag     bFlavorHistorySrc_;
  InputTag     cFlavorHistorySrc_;
  InputTag     genJetsSrc_;
  bool         verbose_;

  // Jet itself
  TH1F *        jetNtrk_;
  TH1F *        jetMass_;

  // Track counting
  TH1F *        trk1d0Sig_;
  TH1F *        trk2d0Sig_;
  TH1F *        trk3d0Sig_;
  TH1F *        trk4d0Sig_;
  TH1F *        trk5d0Sig_;

  // Secondary vertex
  TH1F *        svLxySig_;
  TH1F *        svMass_;
  TH1F *        svCTau_;


  // Flavor history itself
  TH1F *        bPt1_;
  TH1F *        bEta1_;
  TH1F *        bProgId1_;
  TH1F *        bSisId1_;
  TH1F *        bPt2_;
  TH1F *        bEta2_;
  TH1F *        bDR_;
  TH1F *        cPt1_;
  TH1F *        cEta1_;
  TH1F *        cProgId1_;
  TH1F *        cSisId1_;
  TH1F *        cPt2_;
  TH1F *        cEta2_;
  TH1F *        cDR_;



  reco::GenJetCollection::const_iterator 
  getClosestJet( Handle<reco::GenJetCollection> const & pJets,
		 reco::CandidatePtr const & parton ) const 
  {
    double dr = 0.5;
    reco::GenJetCollection::const_iterator j = pJets->begin(),
      jend = pJets->end();
    reco::GenJetCollection::const_iterator bestJet = pJets->end();
    for ( ; j != jend; ++j ) {
      double dri = deltaR( parton->p4(), j->p4() );
      if ( dri < dr ) {
	dr = dri;
	bestJet = j;
      }
    }
    return bestJet;
  }
  
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
HFAna::HFAna(const edm::ParameterSet& iConfig) :
  src_( iConfig.getParameter<InputTag>("src") ),
  bFlavorHistorySrc_( iConfig.getParameter<InputTag>("bFlavorHistory") ),
  cFlavorHistorySrc_( iConfig.getParameter<InputTag>("cFlavorHistory") ),
  genJetsSrc_       ( iConfig.getParameter<InputTag>("genJetsSrc") ),
  verbose_( iConfig.getParameter<bool>("verbose") )
{
   //now do what ever initialization is needed
  Service<TFileService> fs;
  TFileDirectory plots = TFileDirectory( fs->mkdir("hfana") );

  

  jetNtrk_   = plots.make<TH1F>("jetNtrk",   "Number of tracks in jet",          100, 0, 100);
  jetMass_   = plots.make<TH1F>("jetMass",   "Jet mass",                         100, 0,  50);
  trk1d0Sig_ = plots.make<TH1F>("trk1d0Sig", "IP Significance of First Track",   100, -20, 80);
  trk2d0Sig_ = plots.make<TH1F>("trk2d0Sig", "IP Significance of Second Track",  100, -20, 80);
  trk3d0Sig_ = plots.make<TH1F>("trk3d0Sig", "IP Significance of Third Track",   100, -20, 80);
  trk4d0Sig_ = plots.make<TH1F>("trk4d0Sig", "IP Significance of Fourth Track",  100, -20, 80);
  trk5d0Sig_ = plots.make<TH1F>("trk5d0Sig", "IP Significance of Fifth Track",   100, -20, 80);
  svLxySig_  = plots.make<TH1F>("svLxySig",  "Lxy Significance",                 100, -20, 80);
  svMass_    = plots.make<TH1F>("svMass",    "Vertex Mass",                      100, 0, 10);
  svCTau_    = plots.make<TH1F>("svCTau",    "Vertex Pseudo C-Tau",              100, -0.2, 0.8);
  

  bPt1_      = plots.make<TH1F>("bPt1",      "1st B Parton pt",                  100, 0, 100 );
  bEta1_     = plots.make<TH1F>("bEta1",     "1st B Parton eta",                 100, -5.0, 5.0 );
  bProgId1_  = plots.make<TH1F>("bProgID1",  "1st B Parton Progenitor ID",       30,  0, 30 );
  bSisId1_   = plots.make<TH1F>("bSisID1",   "1st B Parton Sister ID",           30,  0, 30 );

  bPt2_      = plots.make<TH1F>("bPt2",      "2nd B Parton pt",                  100, 0, 100 );
  bEta2_     = plots.make<TH1F>("bEta2",     "2nd B Parton eta",                 100, -5.0, 5.0 );

  bDR_       = plots.make<TH1F>("bDR",       "#Delta R between two b quarks",    100, 0, TMath::TwoPi() );

  cPt1_      = plots.make<TH1F>("cPt1",      "1st C Parton pt",                  100, 0, 100 );
  cEta1_     = plots.make<TH1F>("cEta1",     "1st C Parton eta",                 100, -5.0, 5.0 );
  cProgId1_  = plots.make<TH1F>("cProgID1",  "1st C Parton Progenitor ID",       30,  0, 30 );
  cSisId1_   = plots.make<TH1F>("cSisID1",   "1st C Parton Sister ID",           30,  0, 30 );

  cPt2_      = plots.make<TH1F>("cPt2",      "2nd C Parton pt",                  100, 0, 100 );
  cEta2_     = plots.make<TH1F>("cEta2",     "2nd C Parton eta",                 100, -5.0, 5.0 );

  cDR_       = plots.make<TH1F>("cDR",       "#Delta R between two c quarks",    100, 0, TMath::TwoPi() );

}


HFAna::~HFAna()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

//   if ( jetNtrk_   ) delete  jetNtrk_      ; 
//   if ( jetMass_   ) delete  jetMass_      ; 
//   if ( trk1d0Sig_ ) delete  trk1d0Sig_    ; 
//   if ( trk2d0Sig_ ) delete  trk2d0Sig_    ; 
//   if ( trk3d0Sig_ ) delete  trk3d0Sig_    ; 
//   if ( trk4d0Sig_ ) delete  trk4d0Sig_    ; 
//   if ( trk5d0Sig_ ) delete  trk5d0Sig_    ; 
//   if ( svLxySig_  ) delete  svLxySig_     ; 
//   if ( svMass_    ) delete  svMass_       ; 
//   if ( svCTau_    ) delete  svCTau_       ; 



}


//
// member functions
//

// ------------ method called to for each event  ------------
void
HFAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

//   if ( verbose_ ) cout << "Hello from HFAna::analyze" << endl;

//   Handle<vector<Jet> > h_jets;
//   iEvent.getByLabel( src_, h_jets );

//   if ( ! (h_jets.isValid()) ) return;

//   if ( verbose_ ) cout << "Got a valid handle" << endl;

//   if ( h_jets->size() == 0 ) return;

//   if ( verbose_ ) cout << "Have some jets" << endl;


//   vector<Jet>::const_iterator jetBegin = h_jets->begin(),
//     jetEnd = h_jets->end(), ijet = jetBegin;

//   for ( ; ijet != jetEnd; ++ijet ) {

//     if ( verbose_ ) cout << "Processing jet " << ijet - jetBegin << " with pt = " << ijet->pt() << endl;

//     // Fill basic jet mass
//     jetMass_->Fill( ijet->mass() );

//     // Get the associated tag infos
//     reco::TrackIPTagInfo const * ipTagInfos = ijet->tagInfoTrackIP("impactParameter");
//     reco::SecondaryVertexTagInfo const * svTagInfos = ijet->tagInfoSecondaryVertex("secondaryVertex");

//     if ( ipTagInfos == 0 || svTagInfos == 0 ) continue;

//     if ( verbose_ ) cout << "Got valid tag infos" << endl;

//     // Fill the number of tracks
//     vector<reco::TrackIPTagInfo::TrackIPData> const & trackIPData =  ipTagInfos->impactParameterData();
//     // Collect the indexes sorted IP2DSig
//     std::vector<size_t> trackIndexes( ipTagInfos->sortedIndexes(reco::TrackIPTagInfo::IP2DSig) );

//     jetNtrk_->Fill( trackIPData.size() );

//     if ( verbose_ ) cout << "About to fill track IP stuff" << endl;
//     // Fill the track IP significances wrt jet axis
//     if ( trackIPData.size() > 0 ) {
//       trk1d0Sig_->Fill( trackIPData[trackIndexes[0]].ip2d.significance() );
//     }
//     if ( trackIPData.size() > 1 ) {
//       trk2d0Sig_->Fill( trackIPData[trackIndexes[1]].ip2d.significance() );
//     }
//     if ( trackIPData.size() > 2 ) {
//       trk3d0Sig_->Fill( trackIPData[trackIndexes[2]].ip2d.significance() );
//     }
//     if ( trackIPData.size() > 3 ) {
//       trk4d0Sig_->Fill( trackIPData[trackIndexes[3]].ip2d.significance() );
//     }
//     if ( trackIPData.size() > 4 ) {
//       trk5d0Sig_->Fill( trackIPData[trackIndexes[4]].ip2d.significance() );
//     }
    
//     if ( verbose_ ) cout << "About to fill Lxy sig stuff" << endl;
//     // Fill lxy
//     if ( svTagInfos->nVertices() <= 0 ) continue;
    
//     svLxySig_->Fill( svTagInfos->flightDistance(0).significance() );

//     if ( verbose_ ) cout << "About to get tracks" << endl;
//     // Get and fill vertex mass and pseudo ctau
//     reco::TrackRefVector const & tracks = svTagInfos->vertexTracks(0);

//     if ( verbose_ ) cout << "About to make candidate" << endl;
//     reco::TrackRefVector::const_iterator tracksBegin = tracks.begin(),
//       tracksEnd = tracks.end(), itrack = tracksBegin;

//     reco::CompositeCandidate vertexCand;
//     for ( ; itrack != tracksEnd; ++itrack ) {
     
//       const double M_PION = 0.13957018;
//       ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > p4_1;
//       p4_1.SetPt  ( (*itrack)->pt() );
//       p4_1.SetEta ( (*itrack)->eta() );
//       p4_1.SetPhi ( (*itrack)->phi() );
//       p4_1.SetM   ( M_PION ) ;
//       reco::RecoChargedCandidate::LorentzVector p4( p4_1.x(), p4_1.y(), p4_1.z(), p4_1.t() );
//       reco::RecoChargedCandidate cand ( (*itrack)->charge(),
// 					p4
// 					);
      
//       cand.setTrack( *itrack );

//       vertexCand.addDaughter( cand );

//     }

//     if ( verbose_ ) cout << "Done making candidate" << endl;

//     AddFourMomenta addFourMomenta;
//     addFourMomenta.set( vertexCand );

//     double vtxMass = vertexCand.mass();
//     double lxy = svTagInfos->flightDistance(0).value();
//     double vtxPt = vertexCand.pt();

//     double ctau = (vtxPt > 0 ) ?  vtxMass / vtxPt * lxy : 0;

//     svMass_  ->Fill( vtxMass );
//     svCTau_  ->Fill( ctau );

//     if ( verbose_ ) cout << "Done filling jet" << endl;
//   }

  Handle<reco::GenJetCollection> h_jets;
  iEvent.getByLabel( genJetsSrc_, h_jets );

  reco::GenJetCollection::const_iterator jetsEnd = h_jets->end();

  Handle<vector<reco::FlavorHistory> > h_bflav;
  iEvent.getByLabel( bFlavorHistorySrc_, h_bflav );
  if ( h_bflav.isValid() && h_bflav->size() > 0 ) {
    reco::CandidatePtr parton     = h_bflav->at(0).parton();
    reco::CandidatePtr progenitor = h_bflav->at(0).progenitor();
    reco::CandidatePtr sister     = h_bflav->at(0).sister();

    if ( !parton.isNull() ) {
      reco::GenJetCollection::const_iterator matched1 = getClosestJet( h_jets, parton );
      if ( matched1 != jetsEnd ) {
	bPt1_->Fill( matched1->pt() );
	bEta1_->Fill( matched1->pt() );
	
	if ( !progenitor.isNull() ) {
	  bProgId1_->Fill( abs(progenitor->pdgId()) );
	}
	if ( !sister.isNull() ) {
	  reco::GenJetCollection::const_iterator matched2 = getClosestJet( h_jets, sister );
	  if ( matched2 != jetsEnd ) {
	    bPt2_->Fill( matched2->pt() );
	    bEta2_->Fill( matched2->pt() );
	    bDR_->Fill( deltaR<reco::GenJet,reco::GenJet>( *matched1, *matched2 ) );
	  }
	  bSisId1_->Fill( abs(sister->pdgId()) );
	}
      }
    }
  }




  Handle<vector<reco::FlavorHistory> > h_cflav;
  iEvent.getByLabel( cFlavorHistorySrc_, h_cflav );
  if ( h_cflav.isValid() && h_cflav->size() > 0 ) {
    reco::CandidatePtr parton     = h_cflav->at(0).parton();
    reco::CandidatePtr progenitor = h_cflav->at(0).progenitor();
    reco::CandidatePtr sister     = h_cflav->at(0).sister();

    if ( !parton.isNull() ) {
      reco::GenJetCollection::const_iterator matched1 = getClosestJet( h_jets, parton );
      if ( matched1 != jetsEnd ) {
	cPt1_->Fill( matched1->pt() );
	cEta1_->Fill( matched1->pt() );
	
	if ( !progenitor.isNull() ) {
	  cProgId1_->Fill( abs(progenitor->pdgId()) );
	}
	if ( !sister.isNull() ) {
	  reco::GenJetCollection::const_iterator matched2 = getClosestJet( h_jets, sister );
	  if ( matched2 != jetsEnd ) {
	    cPt2_->Fill( matched2->pt() );
	    cEta2_->Fill( matched2->pt() );
	    cDR_->Fill( deltaR<reco::GenJet,reco::GenJet>( *matched1, *matched2 ) );
	  }
	  cSisId1_->Fill( abs(sister->pdgId()) );
	}
      }
    }
  }

  

  if ( verbose_ ) cout << "Finished" << endl;

}


// ------------ method called once each job just before starting event loop  ------------
void 
HFAna::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HFAna::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HFAna);
