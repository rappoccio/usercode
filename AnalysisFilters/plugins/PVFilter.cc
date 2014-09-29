// -*- C++ -*-
//
// Package:    AnalysisFilters
// Class:      AnalysisFilters
// 
/**\class AnalysisFilters AnalysisFilters.cc Analysis/AnalysisFilters/src/AnalysisFilters.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Sun Jan 24 22:48:12 CST 2010
// $Id: PVFilter.cc,v 1.2 2010/01/27 17:39:04 srappocc Exp $
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

#include "Analysis/AnalysisFilters/interface/PVSelector.h"

//
// class declaration
//

class PVFilter : public edm::EDFilter {
   public:
      explicit PVFilter(const edm::ParameterSet&);
      ~PVFilter();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------

  boost::shared_ptr<PVSelector>  pvSelector_;
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
PVFilter::PVFilter(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed

  pvSelector_ = 
    boost::shared_ptr<PVSelector> ( new PVSelector (  
      iConfig.getParameter<edm::InputTag>("pvSrc"), 
      iConfig.getParameter<double>("minPVNdof"), 
      iConfig.getParameter<double>("maxPVZ") 
    ) );

}


PVFilter::~PVFilter()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
PVFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::strbitset ret = pvSelector_->getBitTemplate();
  
  bool passPV = (*pvSelector_)( iEvent, ret );
  return passPV;
}

// ------------ method called once each job just before starting event loop  ------------
void 
PVFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PVFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(PVFilter);
