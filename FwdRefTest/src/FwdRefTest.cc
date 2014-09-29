// -*- C++ -*-
//
// Package:    FwdRefTest
// Class:      FwdRefTest
// 
/**\class FwdRefTest FwdRefTest.cc Analysis/FwdRefTest/src/FwdRefTest.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Tue Jan 19 11:55:59 CST 2010
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "DataFormats/Common/interface/FwdRef.h"
#include "DataFormats/JetReco/interface/CaloJet.h"

#include <vector>

//
// class declaration
//

class FwdRefTest : public edm::EDFilter {
   public:
  typedef reco::CaloJet                 value_type;
  typedef std::vector<value_type>       collection_type;
  typedef edm::FwdRef<collection_type>  fwd_type;
  typedef std::vector<fwd_type>         fwd_collection_type;
  typedef edm::Ref<collection_type>     ref_type;
  typedef std::vector<ref_type>         ref_collection_type;

      explicit FwdRefTest(const edm::ParameterSet&);
      ~FwdRefTest();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
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
FwdRefTest::FwdRefTest(const edm::ParameterSet& iConfig)  :
  jetSrc_( iConfig.getParameter<edm::InputTag>("jetSrc") )
{
   //now do what ever initialization is needed

  produces<collection_type> ();
  produces<fwd_collection_type>();
}


FwdRefTest::~FwdRefTest()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
FwdRefTest::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  std::auto_ptr< collection_type > outJets( new collection_type() );
  std::auto_ptr< fwd_collection_type> outFwds( new fwd_collection_type() );

  edm::Handle<collection_type > pJets;
  iEvent.getByLabel(jetSrc_,pJets);

  edm::RefProd<collection_type> outHandle = iEvent.getRefBeforePut<collection_type>();

  for ( collection_type::const_iterator jetsBegin = pJets->begin(),
	  jetsEnd = pJets->end(), ijet = jetsBegin;
	ijet != jetsEnd; ++ijet ) {
    if ( fabs(ijet->eta()) > 1.5 ) {
      outJets->push_back( *ijet );
      ref_type r1 ( outHandle, outJets->size() - 1 );
      ref_type r2 ( pJets, ijet - jetsBegin );
      fwd_type fwdRef ( r1, r2 );
      outFwds->push_back( fwdRef );
    }
  }
  
  bool ret = outJets->size() > 2;
  iEvent.put( outJets );
  iEvent.put( outFwds );

  return ret;
}

// ------------ method called once each job just before starting event loop  ------------
void 
FwdRefTest::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FwdRefTest::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(FwdRefTest);
