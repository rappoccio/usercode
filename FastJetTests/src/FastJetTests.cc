// -*- C++ -*-
//
// Package:    FastJetTests
// Class:      FastJetTests
// 
/**\class FastJetTests FastJetTests.cc Analysis/FastJetTests/src/FastJetTests.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Tue Mar 24 13:26:36 CDT 2009
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/JetReco/interface/BasicJet.h"
#include "RecoJets/JetAlgorithms/interface/JetRecoTypes.h"
#include "RecoJets/JetAlgorithms/interface/ProtoJet.h"

#include "RecoJets/JetAlgorithms/interface/CMSIterativeConeAlgorithm.h"

#include <valarray>

#include <fstream>
//
// class decleration
//

class FastJetTests : public edm::EDProducer {
   public:
      explicit FastJetTests(const edm::ParameterSet&);
      ~FastJetTests();

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------

  CMSIterativeConeAlgorithm alg_;
  std::ifstream fastjet_inputs;

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
FastJetTests::FastJetTests(const edm::ParameterSet& iConfig) :
  alg_(iConfig.getParameter<double>("seedThreshold"),
       iConfig.getParameter<double>("coneRadius")),
  fastjet_inputs("Pythia-PtMin50-LHC-1000ev.dat")
{
  produces<std::vector<reco::BasicJet> >();        // jets
  produces<std::vector<reco::LeafCandidate> >();   // constituents
}


FastJetTests::~FastJetTests()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
FastJetTests::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace std;

  std::auto_ptr<vector<reco::BasicJet> >      jets( new vector<reco::BasicJet> );
  vector<reco::LeafCandidate>  cand_particles;

  JetReco::InputCollection input_particles;
  
 //...


 std::string line;
//  cout << "About to loop" << endl;
 while (getline(fastjet_inputs, line)) {
//    cout << "Processing " << line << endl;
   istringstream linestream(line);
   if (line == "#END") break;
   if (line.substr(0,1) == "#") {continue;}

   valarray<double> fourvec(4);
   linestream >> fourvec[0] >> fourvec[1] >> fourvec[2] >> fourvec[3];
//    particles.push_back(PseudoJet(fourvec));
   cand_particles.push_back( reco::LeafCandidate( 0, reco::Candidate::LorentzVector( fourvec[0], fourvec[1], fourvec[2], fourvec[3] )) );
   
 }

 vector<reco::LeafCandidate>::const_iterator candbegin = cand_particles.begin(),
   candend = cand_particles.end(), icand = candbegin;
 for ( ; icand != candend; ++icand ) {
   input_particles.push_back( JetReco::CorrectedIndexedCandidate(&(cand_particles[icand - candbegin]), icand - candbegin ) );
 }

 
//  JetReco::InputCollection::const_iterator ipbegin = input_particles.begin(),
//    ipend = input_particles.end(), ipit = ipbegin;
//  for ( ; ipit != ipend; ++ipit ) {
//    cout << "index = " << ipit->index() << ", address = " << ipit->get()  << endl;
//  }

 JetReco::OutputCollection output_collection;

//  cout << "Running algorithm" << endl;
 alg_.run( input_particles, &output_collection );

//  cout << "reconstructing stuff" << endl;
 JetReco::OutputCollection::const_iterator jetsBegin = output_collection.begin(),
   jetsEnd = output_collection.end(), ijet = jetsBegin;

 for ( ; ijet != jetsEnd; ++ijet ) {
   jets->push_back( reco::BasicJet( ijet->p4(), reco::Candidate::Point() ) );
 }

//  cout << "Putting to the event" << endl;
 auto_ptr<vector<reco::LeafCandidate> > toPut( new vector<reco::LeafCandidate>( cand_particles ) );
 iEvent.put( toPut );
 iEvent.put( jets );

 
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
FastJetTests::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FastJetTests::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(FastJetTests);
