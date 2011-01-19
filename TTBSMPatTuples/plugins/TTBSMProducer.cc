// -*- C++ -*-
//
// Package:    TTBSMProducer
// Class:      TTBSMProducer
// 
/**\class TTBSMProducer TTBSMProducer.cc Analysis/TTBSMProducer/src/TTBSMProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Mon Jan 17 21:44:07 CST 2011
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
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#include "Analysis/BoostedTopAnalysis/interface/CATopTagFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
//
// class declaration
//

class TTBSMProducer : public edm::EDFilter {
   public:
      explicit TTBSMProducer(const edm::ParameterSet&);
      ~TTBSMProducer();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------
  edm::InputTag             wTagSrc_; 
  edm::InputTag             topTagSrc_;
  PFJetIDSelectionFunctor   pfJetId_;
  CATopTagFunctor           topTagFunctor_;
  BoostedTopWTagFunctor     wTagFunctor_;
  std::string               topTagName_;
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
TTBSMProducer::TTBSMProducer(const edm::ParameterSet& iConfig) :
  wTagSrc_      (iConfig.getParameter<edm::InputTag>("wTagSrc") ),
  topTagSrc_    (iConfig.getParameter<edm::InputTag>("topTagSrc") ),
  pfJetId_      (iConfig.getParameter<edm::ParameterSet>("pfJetIdParams") ),
  topTagFunctor_(iConfig.getParameter<edm::ParameterSet>("topTagParams") ),
  wTagFunctor_  (iConfig.getParameter<edm::ParameterSet>("wTagParams") ),
  topTagName_   (iConfig.getParameter<edm::ParameterSet>("topTagParams").getParameter<std::string>("tagName") )
{
  //register your products
  produces<std::vector<pat::Jet> > ("wTag");
  produces<std::vector<pat::Jet> > ("topTag");  
}


TTBSMProducer::~TTBSMProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
bool
TTBSMProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  std::auto_ptr<std::vector<pat::Jet> >  selectedWTag( new std::vector<pat::Jet> );
  std::auto_ptr<std::vector<pat::Jet> >  selectedTopTag( new std::vector<pat::Jet> );

  edm::Handle<std::vector<pat::Jet> > h_wTag;
  edm::Handle<std::vector<pat::Jet> > h_topTag;

  iEvent.getByLabel( wTagSrc_, h_wTag );
  iEvent.getByLabel( topTagSrc_, h_topTag );

  pat::strbitset jetIdRet = pfJetId_.getBitTemplate();
  pat::strbitset wTagRet = wTagFunctor_.getBitTemplate();
  pat::strbitset topTagRet = topTagFunctor_.getBitTemplate();
  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_wTag->begin(),
	  jetEnd = h_wTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {
    bool passJetId = pfJetId_( *ijet, jetIdRet );
    if ( passJetId ) {
      selectedWTag->push_back( *ijet );
      double y = -1.0, mu = -1.0, dR = -1.0;
      pat::subjetHelper( selectedWTag->back(), y, mu, dR );
      selectedWTag->back().addUserFloat( "y", y );
      selectedWTag->back().addUserFloat( "mu", mu );
      selectedWTag->back().addUserFloat( "dR", dR );
      bool passedWTag = wTagFunctor_(*ijet, wTagRet);
      selectedWTag->back().addUserInt( "wTagPass", (int)passedWTag );
    }
  }

  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_topTag->begin(),
	  jetEnd = h_topTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {
    bool passJetId = pfJetId_( *ijet, jetIdRet );
    if ( passJetId ) {
      selectedTopTag->push_back( *ijet );
      const reco::CATopJetTagInfo * catopTag = 
	dynamic_cast<reco::CATopJetTagInfo const *>(selectedTopTag->back().tagInfo(topTagName_));
      selectedTopTag->back().addUserFloat( "minMass", catopTag->properties().minMass );
      selectedTopTag->back().addUserFloat( "topMass", catopTag->properties().topMass );
      selectedTopTag->back().addUserFloat( "nSubjets", ijet->numberOfDaughters() );
      bool passedTopTag = topTagFunctor_( *ijet, topTagRet );
      selectedTopTag->back().addUserInt( "topTagPass", (int)passedTopTag );
    }
  }

  iEvent.put( selectedWTag, "wTag");  
  iEvent.put( selectedTopTag, "topTag");   

  return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
TTBSMProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TTBSMProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(TTBSMProducer);
