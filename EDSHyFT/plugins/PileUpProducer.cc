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
// $Id: TTBSMProducer.cc,v 1.13 2012/02/03 17:11:54 guofan Exp $
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

#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"

#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "DataFormats/PatCandidates/interface/MET.h"

using namespace std;

class PileUpProducer : public edm::EDFilter {
   public:
      explicit PileUpProducer(const edm::ParameterSet&);
      ~PileUpProducer();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
  edm::InputTag   pvSrc_;           /// primary vertex


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
PileUpProducer::PileUpProducer(const edm::ParameterSet& iConfig) :
  pvSrc_        ( iConfig.getParameter<edm::InputTag>("pvSrc"))
{
  produces<unsigned int>    ("npv");
  produces<int>    ("npvTrue");
  produces<int>    ("npvRealTrue");
}


PileUpProducer::~PileUpProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
bool
PileUpProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle< std::vector<reco::Vertex> > h_pv;
  iEvent.getByLabel( pvSrc_, h_pv );

  std::auto_ptr<unsigned int> npv( new unsigned int() );
  std::auto_ptr<int> npvTrue( new int() );
  std::auto_ptr<int> npvRealTrue( new int() );

  // Number of reconstructed PV's
  *npv = h_pv->size();

  // Pileup reweighting in the MC
  *npvTrue = -1;
  *npvRealTrue = -1;
  if ( ! iEvent.isRealData() ) {
    edm::InputTag PileupSrc_ ("addPileupInfo");
    edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    iEvent.getByLabel(PileupSrc_, PupInfo);
    std::vector<PileupSummaryInfo>::const_iterator PVI;
    // (then, for example, you can do)
    for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
      int BX = PVI->getBunchCrossing();
      if(BX == 0) { 
	*npvTrue = PVI->getPU_NumInteractions();
        *npvRealTrue = PVI->getTrueNumInteractions();
	break;
      }
    }
  }


  iEvent.put( npv,     "npv");
  iEvent.put( npvTrue, "npvTrue");
  iEvent.put( npvRealTrue, "npvRealTrue");
  return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
PileUpProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PileUpProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(PileUpProducer);
