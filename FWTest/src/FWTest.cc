// -*- C++ -*-
//
// Package:    FWTest
// Class:      FWTest
// 
/**\class FWTest FWTest.cc Analysis/FWTest/src/FWTest.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Thu Jan 14 12:16:08 CST 2010
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

#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"

//
// class declaration
//

class FWTest : public edm::EDProducer {
   public:
      explicit FWTest(const edm::ParameterSet&);
      ~FWTest();

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------
  edm::InputTag caloSrc_;
  edm::InputTag pfSrc_;
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
FWTest::FWTest(const edm::ParameterSet& iConfig) :
  caloSrc_( iConfig.getParameter<edm::InputTag>("caloSrc") ),
  pfSrc_( iConfig.getParameter<edm::InputTag>("pfSrc") )
{
   //register your products
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
*/
   //now do what ever other initialization is needed
  
  produces<std::vector<reco::CaloJet> > ();
  produces<std::vector<reco::PFJet> > ();
}


FWTest::~FWTest()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
FWTest::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   
  std::auto_ptr<std::vector<reco::CaloJet> > p_calo( new std::vector<reco::CaloJet>() );
  std::auto_ptr<std::vector<reco::PFJet> > p_pf( new std::vector<reco::PFJet>() );   


  edm::Handle<std::vector<reco::CaloJet> > h_calo;
  edm::Handle<std::vector<reco::PFJet> > h_pf;

  iEvent.getByLabel( caloSrc_, h_calo );
  iEvent.getByLabel( pfSrc_, h_pf );

  for ( std::vector<reco::CaloJet>::const_iterator caloBegin = h_calo->begin(),
	  caloEnd = h_calo->end(), icalo = caloBegin;
	icalo != caloEnd; ++icalo ) {    
    p_calo->push_back( *icalo );
    p_calo->back().setMass( 175.0 );
  }

  for ( std::vector<reco::PFJet>::const_iterator pfBegin = h_pf->begin(),
	  pfEnd = h_pf->end(), ipf = pfBegin;
	ipf != pfEnd; ++ipf ) {
    p_pf->push_back( *ipf );
    p_pf->back().setMass( 175.0 );
  }

  iEvent.put( p_calo );
  iEvent.put( p_pf );
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
FWTest::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FWTest::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(FWTest);
