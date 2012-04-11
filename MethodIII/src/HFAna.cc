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
// $Id: HFAna.cc,v 1.1 2009/04/09 18:52:33 guofan Exp $
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
#include "DataFormats/HepMCCandidate/interface/FlavorHistoryEvent.h"
#include "DataFormats/BTauReco/interface/TrackIPData.h"

#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "PhysicsTools/UtilAlgos/interface/TFileDirectory.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <vector>

#include <TH1.h>
#include <TObjArray.h>

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
  bool	       FlavorHistory_;


/*
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
*/
  // Jet itself
  TObjArray *        jetNtrk_;
  TObjArray *        jetMass_;
  TH1F      *        jetNum_;

  // Track counting
  TObjArray *        trk1d0Sig_;
  TObjArray *        trk2d0Sig_;
  TObjArray *        trk3d0Sig_;
  TObjArray *        trk4d0Sig_;
  TObjArray *        trk5d0Sig_;

  // Secondary vertex
  TObjArray *        svLxySig_;
  TObjArray *        svMass_;
  TObjArray *        svCTau_;


  // Flavor history itself
  TObjArray *        bPt1_;
  TObjArray *        bEta1_;
  TObjArray *        bProgId1_;
  TObjArray *        bSisId1_;
  TObjArray *        bPt2_;
  TObjArray *        bEta2_;
  TObjArray *        bDR_;
  TObjArray *        cPt1_;
  TObjArray *        cEta1_;
  TObjArray *        cProgId1_;
  TObjArray *        cSisId1_;
  TObjArray *        cPt2_;
  TObjArray *        cEta2_;
  TObjArray *        cDR_;

  
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
  verbose_( iConfig.getParameter<bool>("verbose") ),
  FlavorHistory_( iConfig.getParameter<bool>("FlavorHistory") )
{
   //now do what ever initialization is needed
  Service<TFileService> fs;
  TFileDirectory plots = TFileDirectory( fs->mkdir("hfana") );

/*
  jetNtrk_   = plots.make<TH1F>("jetNtrk",   "Number of tracks in jet",          100, 0, 100);
  jetMass_   = plots.make<TH1F>("jetMass",   "Jet mass",                         100, 0,  50);
  jetNum_    = plots.make<TH1F>("jetNum",    "Number of jets in event",          50,  0,  50);

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
*/

  jetNum_    = plots.make<TH1F>("jetNum",    "Number of jets in event",          50,  0,  50);
  jetNtrk_   = plots.make<TObjArray>(5, 1);   
//  jetNtrk_   = new TObjArray(5,1);
//  jetMass_   = new TObjArray(5,1);
  jetMass_   = plots.make<TObjArray>(5, 1);    

  trk1d0Sig_ = plots.make<TObjArray>(5, 1);
  trk2d0Sig_ = plots.make<TObjArray>(5, 1);   
  trk3d0Sig_ = plots.make<TObjArray>(5, 1);    
  trk4d0Sig_ = plots.make<TObjArray>(5, 1);
  trk5d0Sig_ = plots.make<TObjArray>(5, 1);  
  svLxySig_  = plots.make<TObjArray>(5, 1);  
  svMass_    = plots.make<TObjArray>(5, 1);
  svCTau_    = plots.make<TObjArray>(5, 1); 
  bPt1_      = plots.make<TObjArray>(5, 1);
  bEta1_     = plots.make<TObjArray>(5, 1);
  bProgId1_  = plots.make<TObjArray>(5, 1);   
  bSisId1_   = plots.make<TObjArray>(5, 1);  
  bPt2_      = plots.make<TObjArray>(5, 1);
  bEta2_     = plots.make<TObjArray>(5, 1); 
  bDR_       = plots.make<TObjArray>(5, 1);  
  cPt1_      = plots.make<TObjArray>(5, 1); 
  cEta1_     = plots.make<TObjArray>(5, 1);  
  cProgId1_  = plots.make<TObjArray>(5, 1);    
  cSisId1_   = plots.make<TObjArray>(5, 1);  
  cPt2_      = plots.make<TObjArray>(5, 1);  
  cEta2_     = plots.make<TObjArray>(5, 1);   
  cDR_       = plots.make<TObjArray>(5, 1);

  char hname[20], htitle[50];
  TH1F * h;

  for(int i=1; i<6; i++){
    sprintf(hname, 	"jetNtrk%i", 	i);
    sprintf(htitle, 	"Number of tracks in jet");
    h = new TH1F(hname,  htitle,  100, 0, 100);
    jetNtrk_->Add(h);

    sprintf(hname,      "jetMass%i",    i);
    sprintf(htitle,     "Jet mass");
    h = new TH1F(hname,  htitle,  100, 0, 50);
    jetMass_->Add(h);


    sprintf(hname,      "trk1d0Sig%i",    i);
    sprintf(htitle,     "IP Significance of First Track");
    h = new TH1F(hname,  htitle,  100, -20, 80);
    trk1d0Sig_ ->Add(h);

    sprintf(hname,      "trk2d0Sig%i",    i);
    sprintf(htitle,     "IP Significance of Second Track");
    h = new TH1F(hname,  htitle,  100, -20, 80);
    trk2d0Sig_ ->Add(h);

    sprintf(hname,      "trk3d0Sig%i",    i);
    sprintf(htitle,     "IP Significance of Third Track");
    h = new TH1F(hname,  htitle,  100, -20, 80);
    trk3d0Sig_ ->Add(h);

    sprintf(hname,      "trk4d0Sig%i",    i);
    sprintf(htitle,     "IP Significance of Fourth Track");
    h = new TH1F(hname,  htitle,  100, -20, 80);
    trk4d0Sig_ ->Add(h);

    sprintf(hname,      "trk5d0Sig%i",    i);
    sprintf(htitle,     "IP Significance of Fifth Track");
    h = new TH1F(hname,  htitle,  100, -20, 80);
    trk5d0Sig_ ->Add(h);

    sprintf(hname,      "svLxySig%i",    i);
    sprintf(htitle,     "Lxy Significance");
    h = new TH1F(hname,  htitle,  100, -20, 80);
    svLxySig_ ->Add(h);

    sprintf(hname,      "svMass%i",    i);
    sprintf(htitle,     "Vertex Mass" );
    h = new TH1F(hname,  htitle,  100, 0, 10);
    svMass_  ->Add(h);

    sprintf(hname,      "svCTau%i",    i);
    sprintf(htitle,     "Vertex Pseudo C-Tau");
    h = new TH1F(hname,  htitle,  100, -0.2, 0.8);
    svCTau_   ->Add(h);

    sprintf(hname,      "bPt1%i",    i);
    sprintf(htitle,     "1st B Parton pt");
    h = new TH1F(hname,  htitle,  100, 0, 100);
    bPt1_  ->Add(h);

    sprintf(hname,      "bEta1%i",    i);
    sprintf(htitle,     "1st B Parton eta");
    h = new TH1F(hname,  htitle,  100, -5.0,  5.0);
    bEta1_   ->Add(h);

    sprintf(hname,      "bProgID1%i",    i);
    sprintf(htitle,     "1st B Parton Progenitor ID");
    h = new TH1F(hname,  htitle,  30,  0,   30);
    bProgId1_ ->Add(h);

    sprintf(hname,      "bSisID1%i",    i);
    sprintf(htitle,     "1st B Parton Sister ID");
    h = new TH1F(hname,  htitle,  30,   0,   30);
    bSisId1_    ->Add(h);

    sprintf(hname,      "bPt2%i",    i);
    sprintf(htitle,     "2nd B Parton pt");
    h = new TH1F(hname,  htitle,  100, 0, 100);
    bPt2_  ->Add(h);

    sprintf(hname,      "bEta2%i",    i);
    sprintf(htitle,     "2nd B Parton eta");
    h = new TH1F(hname,  htitle,  100, -5.0, 5.0 );
    bEta2_   ->Add(h);

    sprintf(hname,      "bDR%i",    i);
    sprintf(htitle,     "#Delta R between two b quarks");
    h = new TH1F(hname,  htitle,  100, 0, TMath::TwoPi() );
    bDR_  ->Add(h);

    sprintf(hname,      "cPt1%i",    i);
    sprintf(htitle,     "1st C Parton pt");
    h = new TH1F(hname,  htitle,  100, 0, 100);
    cPt1_  ->Add(h);

    sprintf(hname,      "cEta1%i",    i);
    sprintf(htitle,     "1st C Parton eta");
    h = new TH1F(hname,  htitle,  100,  -5.0, 5.0 );
    cEta1_   ->Add(h);

    sprintf(hname,      "cProgID1%i",    i);
    sprintf(htitle,     "1st C Parton Progenitor ID");
    h = new TH1F(hname,  htitle,  30,  0, 30 );
    cProgId1_ ->Add(h);

    sprintf(hname,      "cSisID1%i",    i);
    sprintf(htitle,     "1st C Parton Sister ID");
    h = new TH1F(hname,  htitle,  30,  0, 30 );
    cSisId1_    ->Add(h);

    sprintf(hname,      "cPt2%i",    i);
    sprintf(htitle,     "2nd C Parton pt");
    h = new TH1F(hname,  htitle,  100, 0, 100);
    cPt2_  ->Add(h);

    sprintf(hname,      "cEta2%i",    i);
    sprintf(htitle,     "2nd C Parton eta");
    h = new TH1F(hname,  htitle,  100, -5.0, 5.0 );
    cEta2_   ->Add(h);

    sprintf(hname,      "cDR%i",    i);
    sprintf(htitle,     "#Delta R between two c quarks");
    h = new TH1F(hname,  htitle,  100, 0,  TMath::TwoPi() );
    cDR_  ->Add(h);


     

  }


}


HFAna::~HFAna()
{
 
}


//
// member functions
//

// ------------ method called to for each event  ------------
void
HFAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  TH1F * h;
  if ( verbose_ ) cout << "Hello from HFAna::analyze" << endl;

  Handle<vector<Jet> > h_jets;
  iEvent.getByLabel( src_, h_jets );
  if ( h_jets->size() == 0 ) return;
  int njet = ( h_jets->size() > 5 ) ? 5 : h_jets->size(); 
  if ( verbose_ )  cout<<"The number of jets is "<<njet<<endl;

  // First analyze the flavor history

  // b first
  if(FlavorHistory_){
  Handle<reco::FlavorHistoryEvent > h_bflav;
  iEvent.getByLabel( bFlavorHistorySrc_, h_bflav );
  if ( h_bflav.isValid() && h_bflav->size() > 0 ) {

    int nb                        = h_bflav->nb();
    int nc                        = h_bflav->nc();
    double dR                     = h_bflav->deltaR();

    reco::FlavorHistoryEvent::const_iterator ib_begin = h_bflav->begin(),
      ib_end = h_bflav->end(),
      ib = ib_begin;

    for (; ib != ib_end; ++ib ) {
      reco::CandidatePtr parton     = ib->parton();
      reco::CandidatePtr progenitor = ib->progenitor();
      reco::CandidatePtr sister     = ib->sister();
      reco::ShallowClonePtrCandidate matched1 = ib->matchedJet();
      reco::ShallowClonePtrCandidate sister1  = ib->sisterJet();

      if ( !parton.isNull() ) {
      
	double parton_pt = parton.isNonnull() ? parton->pt() : -1.0;
	double sister_pt = sister.isNonnull() ? sister->pt() : -1.0;
	double matched_pt = matched1.masterClonePtr().isNonnull() ? matched1.pt() : -1.0;
	double matched_eta = matched1.masterClonePtr().isNonnull() ? matched1.eta() : -1.0;
	double sister_matched_pt = sister1.masterClonePtr().isNonnull() ? sister1.pt() : -1.0;
	double sister_matched_eta = sister1.masterClonePtr().isNonnull() ? sister1.eta() : -1.0;

	if ( verbose_ ) {
	  cout << "------------------------" << endl;
	  cout << "highest flavor = " << h_bflav->highestFlavor() << endl;
	  cout << "flavor source  = " << h_bflav->flavorSource() << endl;
	  cout << "size           = " << h_bflav->size() << endl;
	  cout << "nb             = " << nb << endl;
	  cout << "nc             = " << nc << endl;
	  cout << "dR             = " << dR << endl;
	  cout << "parton pt      = " << parton_pt << endl;
	  cout << "sister pt      = " << sister_pt << endl;
	  cout << "matched pt     = " << matched_pt << endl;
	  cout << "matched eta    = " << matched_eta << endl;
	}

	(  h =(TH1F *) bPt1_->At(njet) )->Fill( matched_pt );
	(  h =(TH1F *) bEta1_->At(njet) )->Fill( matched_eta );
	
	if ( !progenitor.isNull() ) {
	  (  h =(TH1F *) bProgId1_->At(njet) )->Fill( abs(progenitor->pdgId()) );
	}
	if ( !sister.isNull() ) {
	  (  h =(TH1F *) bPt2_->At(njet) )->Fill( sister_matched_pt );
	  (  h =(TH1F *) bEta2_->At(njet) )->Fill( sister_matched_eta );
	  (  h =(TH1F *) bDR_->At(njet) )->Fill( dR );
	  (  h =(TH1F *) bSisId1_->At(njet) )->Fill( abs(sister->pdgId()) );
	}
      }
    }
  }
  

  // c next

  Handle<reco::FlavorHistoryEvent > h_cflav;
  iEvent.getByLabel( cFlavorHistorySrc_, h_cflav );
  if ( h_cflav.isValid() && h_cflav->size() > 0 ) {

    int nb                        = h_cflav->nb();
    int nc                        = h_cflav->nc();
    double dR                     = h_cflav->deltaR();

    reco::FlavorHistoryEvent::const_iterator ic_begin = h_cflav->begin(),
      ic_end = h_cflav->end(),
      ic = ic_begin;

    for (; ic != ic_end; ++ic ) {
      reco::CandidatePtr parton     = ic->parton();
      reco::CandidatePtr progenitor = ic->progenitor();
      reco::CandidatePtr sister     = ic->sister();
      reco::ShallowClonePtrCandidate matched1 = ic->matchedJet();
      reco::ShallowClonePtrCandidate sister1  = ic->sisterJet();

      if ( !parton.isNull() ) {
      
	double parton_pt = parton.isNonnull() ? parton->pt() : -1.0;
	double sister_pt = sister.isNonnull() ? sister->pt() : -1.0;
	double matched_pt = matched1.masterClonePtr().isNonnull() ? matched1.pt() : -1.0;
	double matched_eta = matched1.masterClonePtr().isNonnull() ? matched1.eta() : -1.0;
	double sister_matched_pt = sister1.masterClonePtr().isNonnull() ? sister1.pt() : -1.0;
	double sister_matched_eta = sister1.masterClonePtr().isNonnull() ? sister1.eta() : -1.0;

	if ( verbose_ ) {
	  cout << "------------------------" << endl;
	  cout << "highest flavor = " << h_cflav->highestFlavor() << endl;
	  cout << "flavor source  = " << h_cflav->flavorSource() << endl;
	  cout << "size           = " << h_cflav->size() << endl;
	  cout << "nb             = " << nb << endl;
	  cout << "nc             = " << nc << endl;
	  cout << "dR             = " << dR << endl;
	  cout << "parton pt      = " << parton_pt << endl;
	  cout << "sister pt      = " << sister_pt << endl;
	  cout << "matched pt     = " << matched_pt << endl;
	  cout << "matched eta    = " << matched_eta << endl;
	}

	(  h =(TH1F *) cPt1_->At(njet) )->Fill( matched_pt );
	(  h =(TH1F *) cEta1_->At(njet) )->Fill( matched_eta );
	
	if ( !progenitor.isNull() ) {
	  (  h =(TH1F *) cProgId1_->At(njet) )->Fill( abs(progenitor->pdgId()) );
	}
	if ( !sister.isNull() ) {
	  (  h =(TH1F *) cPt2_->At(njet) )->Fill( sister_matched_pt );
	  (  h =(TH1F *) cEta2_->At(njet) )->Fill( sister_matched_eta );
	  (  h =(TH1F *) cDR_->At(njet) )->Fill( dR );
	  (  h =(TH1F *) cSisId1_->At(njet) )->Fill( abs(sister->pdgId()) );
	}
      }
    }
  }
  }   // end if(FlavorHistory_)


  // Then fill heavy flavor analysis part
//  Handle<vector<Jet> > h_jets;
//  iEvent.getByLabel( src_, h_jets );

  if ( ! (h_jets.isValid()) ) return;

  if ( verbose_ ) cout << "Got a valid handle" << endl;

  if ( h_jets->size() == 0 ) return;

  if ( verbose_ ) cout << "Have some jets" << endl;

  jetNum_->Fill(h_jets->size() );

  vector<Jet>::const_iterator jetBegin = h_jets->begin(),
    jetEnd = h_jets->end(), ijet = jetBegin;

  for ( ; ijet != jetEnd; ++ijet ) {

    if ( verbose_ ) cout << "Processing jet " << ijet - jetBegin << " with pt = " << ijet->pt() << endl;

    // Fill basic jet mass
    (  h = ( TH1F *) jetMass_->At(njet)  )->Fill( ijet->mass() );

    // Get the associated tag infos
    reco::TrackIPTagInfo const * ipTagInfos = ijet->tagInfoTrackIP("impactParameter");
    reco::SecondaryVertexTagInfo const * svTagInfos = ijet->tagInfoSecondaryVertex("secondaryVertex");

    if ( ipTagInfos == 0 || svTagInfos == 0 ) continue;

    if ( verbose_ ) cout << "Got valid tag infos" << endl;

    // Fill the number of tracks
    vector<reco::TrackIPTagInfo::TrackIPData> const & trackIPData =  ipTagInfos->impactParameterData();
    // Collect the indexes sorted IP2DSig
    std::vector<size_t> trackIndexes( ipTagInfos->sortedIndexes(reco::TrackIPTagInfo::IP2DSig) );

    (  h =(TH1F *) jetNtrk_->At(njet)  )->Fill( trackIPData.size() );

    if ( verbose_ ) cout << "About to fill track IP stuff" << endl;
    // Fill the track IP significances wrt jet axis
    if ( trackIPData.size() > 0 ) {
      (  h =(TH1F *) trk1d0Sig_->At(njet) )->Fill( trackIPData[trackIndexes[0]].ip2d.significance() );
    }
    if ( trackIPData.size() > 1 ) {
      (  h =(TH1F *) trk2d0Sig_->At(njet) )->Fill( trackIPData[trackIndexes[1]].ip2d.significance() );
    }
    if ( trackIPData.size() > 2 ) {
      (  h =(TH1F *) trk3d0Sig_->At(njet) )->Fill( trackIPData[trackIndexes[2]].ip2d.significance() );
    }
    if ( trackIPData.size() > 3 ) {
      (  h =(TH1F *) trk4d0Sig_->At(njet) )->Fill( trackIPData[trackIndexes[3]].ip2d.significance() );
    }
    if ( trackIPData.size() > 4 ) {
      (  h =(TH1F *) trk5d0Sig_->At(njet) )->Fill( trackIPData[trackIndexes[4]].ip2d.significance() );
    }
    
    if ( verbose_ ) cout << "About to fill Lxy sig stuff" << endl;
    // Fill lxy
    if ( svTagInfos->nVertices() > 0 ) {
      ( h =(TH1F *) svLxySig_->At(njet)  )->Fill( svTagInfos->flightDistance(0).significance() );
    }

    if ( verbose_ ) cout << "About to fill vertex mass " << endl;
    if ( svTagInfos->nVertices() > 0 ) {
      reco::Vertex::trackRef_iterator tracksBegin = svTagInfos->secondaryVertex(0).tracks_begin(),
	tracksEnd = svTagInfos->secondaryVertex(0).tracks_end(),
	itrack = tracksBegin;

      if ( verbose_ ) cout << "There are " << tracksEnd - tracksBegin << " tracks in the vertex" << endl;
    
      reco::CompositeCandidate vertexCand;
      for ( ; itrack != tracksEnd; ++itrack ) {
     
	const double M_PION = 0.13957018;
	ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > p4_1;
	p4_1.SetPt  ( (*itrack)->pt() );
	p4_1.SetEta ( (*itrack)->eta() );
	p4_1.SetPhi ( (*itrack)->phi() );
	p4_1.SetM   ( M_PION ) ;
	reco::RecoChargedCandidate::LorentzVector p4( p4_1.x(), p4_1.y(), p4_1.z(), p4_1.t() );
	reco::RecoChargedCandidate cand ( (*itrack)->charge(),
					  p4
					  );
      
	//       cand.setTrack( *itrack );

	vertexCand.addDaughter( cand );

      }

      if ( verbose_ ) cout << "Done making candidate" << endl;

      AddFourMomenta addFourMomenta;
      addFourMomenta.set( vertexCand );

      double vtxMass = vertexCand.mass();
      double lxy = svTagInfos->flightDistance(0).value();
      double vtxPt = vertexCand.pt();

      double ctau = (vtxPt > 0 ) ?  vtxMass / vtxPt * lxy : 0;

      ( h =(TH1F *)svMass_->At(njet) )->Fill( vtxMass );
      ( h =(TH1F *)svCTau_->At(njet) )->Fill( ctau );
      if ( verbose_ ) cout << "Filling vertex mass and cta = " << vtxMass << ", " << ctau << endl;
    }

    if ( verbose_ ) cout << "Done filling jet" << endl;
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


  Service<TFileService> fs;
  fs->mkdir("dir");

  jetNtrk_->Write();
  jetMass_->Write();

  trk1d0Sig_ ->Write();
  trk2d0Sig_ ->Write();
  trk3d0Sig_ ->Write();
  trk4d0Sig_ ->Write();
  trk5d0Sig_ ->Write();

  svLxySig_ ->Write();
  svMass_ ->Write();
  svCTau_ ->Write();

  if(FlavorHistory_){
  bPt1_ ->Write();
  bEta1_ ->Write();
  bProgId1_ ->Write();
  bSisId1_ ->Write();
  bPt2_ ->Write();
  bEta2_ ->Write();
  bDR_ ->Write();
  cPt1_ ->Write();
  cEta1_ ->Write();
  cProgId1_ ->Write();
  cSisId1_ ->Write();
  cPt2_ ->Write();
  cEta2_ ->Write();
  cDR_ ->Write();
  }

}

//define this as a plug-in
DEFINE_FWK_MODULE(HFAna);
