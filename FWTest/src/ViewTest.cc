// -*- C++ -*-
//
// Package:    ViewTest
// Class:      ViewTest
// 
/**\class ViewTest ViewTest.cc Analysis/ViewTest/src/ViewTest.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Thu Jan 14 12:51:09 CST 2010
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

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/Jet.h"
//
// class declaration
//

class ViewTest : public edm::EDAnalyzer {
   public:
      explicit ViewTest(const edm::ParameterSet&);
      ~ViewTest();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------
  edm::InputTag jetSrc_;
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
ViewTest::ViewTest(const edm::ParameterSet& iConfig) :
  jetSrc_( iConfig.getParameter<edm::InputTag>("jetSrc") )
{
   //now do what ever initialization is needed

}


ViewTest::~ViewTest()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
ViewTest::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{



  edm::Handle<edm::View<reco::Jet> > pIn;
  iEvent.getByLabel( jetSrc_, pIn);

  
  for ( edm::View<reco::Jet>::const_iterator ibegin = pIn->begin(),
	  iend = pIn->end(), i = ibegin; 
	i != iend; ++i ) {
    std::cout << "i = " << i - iend << ", pt = " << i->pt() << std::endl;
  }
}


// ------------ method called once each job just before starting event loop  ------------
void 
ViewTest::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ViewTest::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(ViewTest);
