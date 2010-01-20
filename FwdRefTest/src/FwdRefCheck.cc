// -*- C++ -*-
//
// Package:    FwdRefCheck
// Class:      FwdRefCheck
// 
/**\class FwdRefCheck FwdRefCheck.cc Analysis/FwdRefCheck/src/FwdRefCheck.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Wed Jan 20 09:00:40 CST 2010
// $Id$
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

#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/Common/interface/FwdRef.h"
//
// class declaration
//

class FwdRefCheck : public edm::EDAnalyzer {
   public:
      explicit FwdRefCheck(const edm::ParameterSet&);
      ~FwdRefCheck();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------

  edm::InputTag jetSrc1_;
  edm::InputTag jetSrc2_;  
  edm::InputTag refVecSrc_;
  edm::InputTag jetIDSrc_;
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
FwdRefCheck::FwdRefCheck(const edm::ParameterSet& iConfig) :
  jetSrc1_(iConfig.getParameter<edm::InputTag>("jetSrc1") ),
  jetSrc2_(iConfig.getParameter<edm::InputTag>("jetSrc2") ),  
  refVecSrc_ (iConfig.getParameter<edm::InputTag>("refVecSrc") ),
  jetIDSrc_ (iConfig.getParameter<edm::InputTag>("jetIDSrc") )
{
   //now do what ever initialization is needed

}


FwdRefCheck::~FwdRefCheck()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
FwdRefCheck::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<reco::CaloJetFwdRefVector> h_refs;
  edm::Handle<reco::JetIDValueMap> h_JetIDMap;
  
    iEvent.getByLabel( refVecSrc_, h_refs );
  iEvent.getByLabel( jetIDSrc_, h_JetIDMap );
  
  for ( reco::CaloJetFwdRefVector::const_iterator refsBegin = h_refs->begin(),
	  refsEnd = h_refs->end(), iref = refsBegin;
	iref != refsEnd; ++iref ) {
    reco::CaloJetFwdRef const & ref = *iref;
    reco::JetID jetId = (*h_JetIDMap)[ ref.backRef() ];

    std::cout << "Processing ref " << iref - refsBegin << ", ref idx = " << ref.key() << ", backref idx = " << ref.backRef().key() 
	      << ", jet pt = " << ref->pt() << ", n90Hits = " << jetId.n90Hits << std::endl;
  }
    
}


// ------------ method called once each job just before starting event loop  ------------
void 
FwdRefCheck::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FwdRefCheck::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(FwdRefCheck);
