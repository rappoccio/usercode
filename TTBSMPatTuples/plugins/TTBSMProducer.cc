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
// $Id: TTBSMProducer.cc,v 1.4 2011/05/30 19:53:51 srappocc Exp $
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
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerPath.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#include "Analysis/BoostedTopAnalysis/interface/CATopTagFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
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
  edm::InputTag             trigSrc_;
  std::vector<std::string>  trigs_;
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
  trigSrc_      (iConfig.getParameter<edm::InputTag>("trigSrc") ),
  trigs_        (iConfig.getParameter<std::vector<std::string> > ("trigs") ),
  topTagName_   (iConfig.getParameter<edm::ParameterSet>("topTagParams").getParameter<std::string>("tagName") ),
  topTagFunctor_(iConfig.getParameter<edm::ParameterSet>("topTagParams")),
  wTagFunctor_  (iConfig.getParameter<edm::ParameterSet>("wTagParams"))
{
  //register your products
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4");  
  produces<std::vector<double> > ("topTagBDisc");
  produces<std::vector<double> > ("wTagBDisc");
  produces<std::vector<double> > ("wTagMu");
  produces<std::vector<int> >    ("wTagPass");
  produces<std::vector<double> > ("topTagMinMass");
  produces<std::vector<double> > ("topTagTopMass");
  produces<std::vector<double> > ("topTagNSubjets");
  produces<std::vector<int> >    ("topTagPass");
  produces<std::vector<int> >    ("prescales");
  produces<std::vector<int> >    ("trigs");
  produces<std::vector<std::string> > ("trigNames");
  produces<double> ("rho");
  produces<double> ("weight");

  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4Hemis0");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4Hemis1");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4Hemis0");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4Hemis1");
  produces<std::vector<double> > ("wTagBDiscHemis0");
  produces<std::vector<double> > ("wTagMuHemis0");
  produces<std::vector<double> > ("topTagMinMassHemis0");
  produces<std::vector<double> > ("topTagTopMassHemis0");
  produces<std::vector<double> > ("topTagNSubjetsHemis0");
  produces<std::vector<int> >    ("topTagPassHemis0");
  produces<std::vector<double> > ("wTagBDiscHemis1");
  produces<std::vector<double> > ("wTagMuHemis1");
  produces<std::vector<double> > ("topTagMinMassHemis1");
  produces<std::vector<double> > ("topTagTopMassHemis1");
  produces<std::vector<double> > ("topTagNSubjetsHemis1");
  produces<std::vector<int> >    ("topTagPassHemis1");
  produces<int>                  ("jet3Hemis0");
  produces<int>                  ("jet3Hemis1");

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
  typedef reco::Candidate::PolarLorentzVector LorentzV;

  std::auto_ptr<p4_vector> wTagP4( new p4_vector() );
  std::auto_ptr<p4_vector> topTagP4( new p4_vector() );
  std::auto_ptr<std::vector<double> > wTagBDisc ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagBDisc ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMu ( new std::vector<double>() );
  std::auto_ptr<std::vector<int> >    wTagPass ( new std::vector<int>() );
  std::auto_ptr<std::vector<double> > topTagMinMass ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMass ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjets ( new std::vector<double>() );
  std::auto_ptr<std::vector<int> >    topTagPass ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> >    prescales ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> >    trigs ( new std::vector<int>() );
  std::auto_ptr<std::vector<std::string> >    trigNames ( new std::vector<std::string>() );
  std::auto_ptr<double>               rho( new double(-1.0) );
  std::auto_ptr<double>               weight( new double(1.0) );

  //The duplicate quantities by hemisphere
  std::auto_ptr<p4_vector> topTagP4Hemis0 ( new p4_vector() );
  std::auto_ptr<p4_vector> topTagP4Hemis1 ( new p4_vector() );
  std::auto_ptr<p4_vector> wTagP4Hemis0 ( new p4_vector() );
  std::auto_ptr<p4_vector> wTagP4Hemis1 ( new p4_vector() );
  std::auto_ptr<int> jet3Hemis0   ( new int(-1) );
  std::auto_ptr<int> jet3Hemis1   ( new int(-1) );
  std::auto_ptr<std::vector<double> > wTagBDiscHemis0( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagBDiscHemis1( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMuHemis0( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMuHemis1( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagMinMassHemis0 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagMinMassHemis1 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMassHemis0 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMassHemis1 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjetsHemis0( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjetsHemis1( new std::vector<double>() );
  std::auto_ptr<std::vector<int> > topTagPassHemis0  ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> > topTagPassHemis1  ( new std::vector<int>() );




  edm::Handle<std::vector<pat::Jet> > h_wTag;
  edm::Handle<std::vector<pat::Jet> > h_topTag;
  edm::Handle<pat::TriggerEvent>      h_trig;

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
    topTagBDisc->push_back( ijet->bDiscriminator("trackCountingHighEffBJetTags") );

  }

  // For real data, get trigger path
  if ( iEvent.isRealData() ) {
    iEvent.getByLabel( trigSrc_,h_trig );
    for ( std::vector<std::string>::const_iterator itrigBegin = trigs_.begin(),
	    itrigEnd = trigs_.end(), itrig = itrigBegin;
	  itrig != itrigEnd; ++itrig ) {
      if ( h_trig->wasRun() && h_trig->wasAccept() && h_trig->paths() > 0 ) {
	int indexPath = h_trig->indexPath( *itrig );
	if ( indexPath > 0 ) {
	  pat::TriggerPath const * path = h_trig->path( *itrig );
	  if ( path != 0 && path->wasRun() && path->wasAccept() ) {
	    trigs->push_back( path->index() );
	    prescales->push_back( path->prescale() );
	    trigNames->push_back( path->name() );
	  }
	}
      }
    }
  }

  //Make hemisphere
  if( topTagP4->size() > 0 ) {
    LorentzV  leadJet = topTagP4->at(0);
    for( size_t i=0; i<topTagP4->size(); i++ ) {
      double dPhi = fabs( reco::deltaPhi<double>( leadJet.phi(), topTagP4->at(i).phi() ) );
      if( dPhi < TMath::Pi()/2 )  {
        topTagP4Hemis0->push_back( topTagP4->at(i) );
        topTagMinMassHemis0->push_back( topTagMinMass->at(i) );
        topTagTopMassHemis0->push_back( topTagTopMass->at(i) );
        topTagNSubjetsHemis0->push_back( topTagNSubjets->at(i) );
        topTagPassHemis0->push_back( topTagPass->at(i) );
      }
      else  {
        topTagP4Hemis1->push_back( topTagP4->at(i) );
        topTagMinMassHemis1->push_back( topTagMinMass->at(i) );
        topTagTopMassHemis1->push_back( topTagTopMass->at(i) );
        topTagNSubjetsHemis1->push_back( topTagNSubjets->at(i) );
        topTagPassHemis1->push_back( topTagPass->at(i) );
      }
    }
    for( size_t i=0; i<wTagP4->size(); i++ )  {
      double dPhi = fabs( reco::deltaPhi<double>( leadJet.phi(), wTagP4->at(i).phi() )  );
      if( dPhi < TMath::Pi()/2 )  {
        wTagP4Hemis0->push_back( wTagP4->at(i) );
        wTagBDiscHemis0->push_back( wTagBDisc->at(i) );
        wTagMuHemis0->push_back( wTagMu->at(i) );
      }
      else  {
        wTagP4Hemis1->push_back( wTagP4->at(i) );
        wTagBDiscHemis1->push_back( wTagBDisc->at(i) );
        wTagMuHemis1->push_back( wTagMu->at(i) );
      }
    }
  }

  if( wTagP4Hemis0->size() > 0 )  {
    LorentzV   leadJetHemis0 = wTagP4Hemis0->at(0) ;
    double minDr = 99999. ;
    for( size_t i=1 ; i<wTagP4Hemis0->size() ; i++ )  {
      double deltaR = reco::deltaR<double>( leadJetHemis0.eta(), leadJetHemis0.phi(),
                                            wTagP4Hemis0->at(i).eta(), wTagP4Hemis0->at(i).phi() );
      if( deltaR < minDr )  {
        *jet3Hemis0 = i;
        minDr = deltaR;
      }
    }
  }
  if( wTagP4Hemis1->size() > 0 )  {
    LorentzV   leadJetHemis1 = wTagP4Hemis1->at(0) ;
    double minDr = 99999. ;
    for( size_t i=1 ; i<wTagP4Hemis1->size() ; i++ )  {
      double deltaR = reco::deltaR<double>( leadJetHemis1.eta(), leadJetHemis1.phi(),
                                            wTagP4Hemis1->at(i).eta(), wTagP4Hemis1->at(i).phi() );
      if( deltaR < minDr )  {
        *jet3Hemis1 = i;
        minDr = deltaR;
      }
    }
  }

  edm::Handle<double>        caTopJetRho;
  iEvent.getByLabel( edm::InputTag("kt6PFJetsPFlow", "rho"),    caTopJetRho );
  *rho = *caTopJetRho ;
  edm::Handle<GenEventInfoProduct>    genEvt;
  iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
  if( genEvt.isValid() )  {
    *weight = genEvt->weight() ;
  }


  iEvent.put(wTagP4        ,"wTagP4");
  iEvent.put(topTagP4      ,"topTagP4");  
  iEvent.put(wTagBDisc     ,"wTagBDisc");
  iEvent.put(topTagBDisc   ,"topTagBDisc");
  iEvent.put(wTagMu        ,"wTagMu");
  iEvent.put(wTagPass      ,"wTagPass");
  iEvent.put(topTagMinMass ,"topTagMinMass");
  iEvent.put(topTagTopMass ,"topTagTopMass");
  iEvent.put(topTagNSubjets,"topTagNSubjets");
  iEvent.put(topTagPass    ,"topTagPass");    
  iEvent.put(prescales     ,"prescales");
  iEvent.put(trigs         ,"trigs");
  iEvent.put(trigNames     ,"trigNames");
  iEvent.put(wTagP4Hemis0        ,"wTagP4Hemis0");
  iEvent.put(topTagP4Hemis0      ,"topTagP4Hemis0");
  iEvent.put(wTagBDiscHemis0     ,"wTagBDiscHemis0");
  iEvent.put(wTagMuHemis0        ,"wTagMuHemis0");
  iEvent.put(topTagMinMassHemis0 ,"topTagMinMassHemis0");
  iEvent.put(topTagTopMassHemis0 ,"topTagTopMassHemis0");
  iEvent.put(topTagNSubjetsHemis0,"topTagNSubjetsHemis0");
  iEvent.put(topTagPassHemis0    ,"topTagPassHemis0");
  iEvent.put(jet3Hemis0,          "jet3Hemis0" );
  iEvent.put(wTagP4Hemis1        ,"wTagP4Hemis1");
  iEvent.put(topTagP4Hemis1      ,"topTagP4Hemis1");
  iEvent.put(wTagBDiscHemis1     ,"wTagBDiscHemis1");
  iEvent.put(wTagMuHemis1        ,"wTagMuHemis1");
  iEvent.put(topTagMinMassHemis1 ,"topTagMinMassHemis1");
  iEvent.put(topTagTopMassHemis1 ,"topTagTopMassHemis1");
  iEvent.put(topTagNSubjetsHemis1,"topTagNSubjetsHemis1");
  iEvent.put(topTagPassHemis1    ,"topTagPassHemis1");
  iEvent.put(jet3Hemis1,          "jet3Hemis1"  );
  iEvent.put( rho,                "rho" );
  iEvent.put( weight,             "weight");

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
