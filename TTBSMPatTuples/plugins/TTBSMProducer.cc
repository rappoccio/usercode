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
// $Id: TTBSMProducer.cc,v 1.1 2011/01/19 15:52:05 srappocc Exp $
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
  std::string               topTagName_;
  CATopTagFunctor           topTagFunctor_;
  BoostedTopWTagFunctor     wTagFunctor_;
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
  topTagName_   (iConfig.getParameter<edm::ParameterSet>("topTagParams").getParameter<std::string>("tagName") ),
  topTagFunctor_(iConfig.getParameter<edm::ParameterSet>("topTagParams")),
  wTagFunctor_  (iConfig.getParameter<edm::ParameterSet>("wTagParams"))
{
  //register your products
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4");  
  produces<std::vector<double> > ("wTagBDisc");
  produces<std::vector<double> > ("wTagMu");
  produces<std::vector<int> >    ("wTagPass");
  produces<std::vector<double> > ("topTagMinMass");
  produces<std::vector<double> > ("topTagTopMass");
  produces<std::vector<double> > ("topTagNSubjets");
  produces<std::vector<int> >    ("topTagPass");
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

  typedef std::vector<reco::Candidate::PolarLorentzVector> p4_vector;

  std::auto_ptr<p4_vector> wTagP4( new p4_vector() );
  std::auto_ptr<p4_vector> topTagP4( new p4_vector() );
  std::auto_ptr<std::vector<double> > wTagBDisc ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMu ( new std::vector<double>() );
  std::auto_ptr<std::vector<int> >    wTagPass ( new std::vector<int>() );
  std::auto_ptr<std::vector<double> > topTagMinMass ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMass ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjets ( new std::vector<double>() );
  std::auto_ptr<std::vector<int> >    topTagPass ( new std::vector<int>() );

  edm::Handle<std::vector<pat::Jet> > h_wTag;
  edm::Handle<std::vector<pat::Jet> > h_topTag;

  iEvent.getByLabel( wTagSrc_, h_wTag );
  iEvent.getByLabel( topTagSrc_, h_topTag );

  pat::strbitset wTagRet = wTagFunctor_.getBitTemplate();
  pat::strbitset topTagRet = topTagFunctor_.getBitTemplate();
  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_wTag->begin(),
	  jetEnd = h_wTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {
    wTagP4->push_back( ijet->polarP4() );
    bool passedWTag = wTagFunctor_(*ijet, wTagRet);
    double y = -1.0, mu = -1.0, dR = -1.0;
    pat::subjetHelper( *ijet, y, mu, dR );
    wTagMu->push_back( mu );
    wTagPass->push_back( passedWTag );
    wTagBDisc->push_back( ijet->bDiscriminator("trackCountingHighEffBJetTags") );
  }

  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_topTag->begin(),
	  jetEnd = h_topTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {
    const reco::CATopJetTagInfo * catopTag = 
      dynamic_cast<reco::CATopJetTagInfo const *>(ijet->tagInfo(topTagName_));
    bool passedTopTag = topTagFunctor_( *ijet, topTagRet );
    topTagP4->push_back( ijet->polarP4() );
    topTagPass->push_back( passedTopTag );
    topTagMinMass->push_back( catopTag->properties().minMass );
    topTagTopMass->push_back( catopTag->properties().topMass );
    topTagNSubjets->push_back( ijet->numberOfDaughters() );

  }

  iEvent.put(wTagP4        ,"wTagP4");
  iEvent.put(topTagP4      ,"topTagP4");  
  iEvent.put(wTagBDisc     ,"wTagBDisc");
  iEvent.put(wTagMu        ,"wTagMu");
  iEvent.put(wTagPass      ,"wTagPass");
  iEvent.put(topTagMinMass ,"topTagMinMass");
  iEvent.put(topTagTopMass ,"topTagTopMass");
  iEvent.put(topTagNSubjets,"topTagNSubjets");
  iEvent.put(topTagPass    ,"topTagPass");    


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
