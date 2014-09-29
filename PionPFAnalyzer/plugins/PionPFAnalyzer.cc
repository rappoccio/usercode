// -*- C++ -*-
//
///1;3402;0c/ Package:    PionPFAnalyzer
// Class:      PionPFAnalyzer
// 
/**\class PionPFAnalyzer PionPFAnalyzer.cc Analyzer/PionPFAnalyzer/src/PionPFAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/

// $Id$
//
//

// system include files
#include <memory>
#include <map>
#include <utility>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstring>
#include <cmath>

#include <TLorentzVector.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TFile.h>
#include <TTree.h>
//New Include files
#include "DataFormats/ParticleFlowReco/interface/PFRecHit.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"

#include "DataFormats/Math/interface/deltaR.h"


// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerFilter.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
//#include "DataFormats/ParticleFlowReco/interface/PFSuperCluster.h"


#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/ParticleFlowReco/interface/PFLayer.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


//
// class declaration
//

class PionPFAnalyzer : public edm::EDAnalyzer {
public:
  explicit PionPFAnalyzer(const edm::ParameterSet&);
  ~PionPFAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  //virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  //virtual void endRun(edm::Run const&, edm::EventSetup const&);
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  // ----------member data ---------------------------

  double dRMin_;
  edm::InputTag jetSrc_;
  edm::InputTag genSrc_;


  TTree * mytree;


  float reco_pt;
  float reco_eta;
  float reco_phi;
  float reco_m;
  float gen_pt;
  float gen_eta;
  float gen_phi;
  float gen_m;
  

  static const int MAXRECHIT = 10000;
  Int_t layer[MAXRECHIT];
  float energy[MAXRECHIT];
  float time[MAXRECHIT];

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//
using namespace std;
using namespace reco;
//
// constructors and destructor
//
PionPFAnalyzer::PionPFAnalyzer(const edm::ParameterSet& iConfig) :
  dRMin_( iConfig.getParameter<double>( "dRMin") ),
  jetSrc_( iConfig.getParameter<edm::InputTag>( "jetSrc") ),
  genSrc_( iConfig.getParameter<edm::InputTag>( "genSrc") )
{
   //now do what ever initialization is needed


  edm::Service<TFileService> fs;


  reco_pt = reco_eta = reco_phi = reco_m = gen_pt = gen_eta = gen_phi = gen_m = 0.0;
  for ( auto & i : layer ) i = 0.0;
  for ( auto & i : energy ) i = 0.0;
  for ( auto & i : time ) i = 0.0;

  mytree = fs->make<TTree>("pfRecHitTree", "pfRecHitTree");
  mytree->Branch("reco_pt",&reco_pt,"reco_pt/F");
  mytree->Branch("reco_eta",&reco_eta,"reco_eta/F");
  mytree->Branch("reco_phi",&reco_phi,"reco_phi/F");
  mytree->Branch("reco_m",&reco_m,"reco_m/F");
  mytree->Branch("gen_pt",&gen_pt,"gen_pt/F");
  mytree->Branch("gen_eta",&gen_eta,"gen_eta/F");
  mytree->Branch("gen_phi",&gen_phi,"gen_phi/F");
  mytree->Branch("gen_m",&gen_m,"gen_m/F");  
  mytree->Branch("layer",layer,"layer[10000]/I");
  mytree->Branch("energy",energy,"energy[10000]/F");
  mytree->Branch("time",time,"time[10000]/F");

 }


PionPFAnalyzer::~PionPFAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void PionPFAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
   using namespace edm;



   reco_pt = reco_eta = reco_phi = reco_m = gen_pt = gen_eta = gen_phi = gen_m = 0.0;
   for ( auto & i : layer ) i = 0.0;
   for ( auto & i : energy ) i = 0.0;
   for ( auto & i : time ) i = 0.0;
   

   Handle<reco::PFJetCollection> pfjets;
   iEvent.getByLabel(jetSrc_, pfjets);

   Handle<reco::GenParticleCollection> genParticles;
   iEvent.getByLabel(genSrc_, genParticles);

   for ( auto const & PFJet : *pfjets) {
	bool gotit = false;
	reco::GenParticle const * matchedGen = 0;
	for ( auto const & genParticle : *genParticles) {
	  if ( gotit ) break;
	  auto deltaR = reco::deltaR( genParticle.p4(), PFJet.p4() );
	  if ( deltaR < dRMin_ ) {
	    gotit = true;
	    matchedGen = &genParticle;
	  }
	  if ( matchedGen != 0 ){

	    reco_pt = PFJet.pt();
	    reco_eta = PFJet.eta();
	    reco_phi = PFJet.phi();
	    reco_m = PFJet.mass();
	    gen_pt = matchedGen->pt();
	    gen_eta = matchedGen->eta();
	    gen_phi = matchedGen->phi();
	    gen_m = matchedGen->mass();

	    auto pfcands = PFJet.getPFConstituents();

	    int irechit = 0;
	    // Get the PF cands in the jets
	    for ( auto const & pfcand : pfcands ) {
	      // Check if available
	      if ( pfcand.isNonnull() && pfcand.isAvailable() ) {
		// Get the elements in each block
		auto const & elementsInBlocks = pfcand->elementsInBlocks() ;
		// Loop over the elements
		for ( auto const & ielementInBlock : elementsInBlocks) {
		  // Get the reference to the actual elements
		  auto const & elementsRef = ielementInBlock.first;
		  // Check if available
		  if ( elementsRef.isNonnull() && elementsRef.isAvailable() ) {
		    // If available, get the elements
		    auto const & elements = elementsRef->elements();
		    // Loop over elements
		    for ( auto const & element : elements ) {
		      // Get ref to cluster
		      auto const & clusterRef = element.clusterRef();
		      // Check if available
		      if ( clusterRef.isNonnull() && clusterRef.isAvailable() ) {
			reco::PFCluster const * cluster = &*clusterRef;
			if ( cluster != 0 ) {

			  auto const & recHitFractions = cluster->recHitFractions();

			  for ( auto const & recHitFraction : recHitFractions ) {
			    //auto const & fraction = recHitFraction.fraction();
			    auto const & recHitRef = recHitFraction.recHitRef();
			    if ( recHitRef.isNonnull() && recHitRef.isAvailable() ) {

			      if ( irechit >= MAXRECHIT ) {
				break;
			      }

			      layer[irechit] = recHitRef->layer();
			      energy[irechit] = recHitRef->energy();
			      time[irechit] = recHitRef->time();

			      ++irechit;

			    }
			  }
			}
		      }
		    }
		  }
		}
	      }
	    }
	  }
	}
   }

   mytree->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void 
PionPFAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PionPFAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
PionPFAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
PionPFAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
PionPFAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
PionPFAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PionPFAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PionPFAnalyzer);
