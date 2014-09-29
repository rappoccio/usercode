// -*- C++ -*-
//
// Package:    EDJetMassPDFUncertainty
// Class:      EDJetMassPDFUncertainty
// 
/**\class EDJetMassPDFUncertainty EDJetMassPDFUncertainty.cc Analysis/EDJetMassPDFUncertainty/src/EDJetMassPDFUncertainty.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Sal Rappoccio
//         Created:  Sat July 15 11:39:14 CDT 2011
// $Id: EDJetMassPDFUncertainty.cc,v 1.1 2012/06/14 14:41:28 srappocc Exp $
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
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "TPRegexp.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH2F.h"
#include "TH1F.h"
#include <sstream>

//
// class declaration
//


class EDJetMassPDFUncertainty : public edm::EDAnalyzer {
   public:
      explicit EDJetMassPDFUncertainty(const edm::ParameterSet&);
      ~EDJetMassPDFUncertainty();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------

      std::string jetTag_;
      edm::InputTag generatorTag_;
      edm::InputTag pdfTag_;

  TH1D * jetPtNum;
  TH1D * jetPtDen;

  std::vector<TH1F*> massHists;
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
EDJetMassPDFUncertainty::EDJetMassPDFUncertainty(const edm::ParameterSet& iConfig)

{
  jetTag_ = iConfig.getParameter<std::string>("jetTag");
  generatorTag_ = iConfig.getParameter<edm::InputTag>("generatorTag");
  pdfTag_ = iConfig.getParameter<edm::InputTag>("pdfTag");

  edm::Service<TFileService> fs;


  for ( unsigned i = 0; i < 44; ++i ) {

    std::stringstream s;
    // s << "jetPt" << i;
    // fs->make<TH1D>(s.str().c_str(), s.str().c_str(),   30, 0., 3000.);
    s << "jetMass" << i;
    TH1F * imassHist = fs->make<TH1F>(s.str().c_str(), s.str().c_str(),   30, 0., 300.);
    massHists.push_back( imassHist );
  }
}



EDJetMassPDFUncertainty::~EDJetMassPDFUncertainty()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
EDJetMassPDFUncertainty::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   using namespace edm;

   edm::Handle<std::vector<float>  >   jetHandlePx;
   edm::Handle<std::vector<float>  >   jetHandlePy;
   edm::Handle<std::vector<float>  >   jetHandlePz;
   edm::Handle<std::vector<float>  >   jetHandleE;

   edm::Handle<std::vector<double>  >   pdfWeightsHandle;
   edm::Handle<GenEventInfoProduct >    genHandle;


   iEvent.getByLabel( edm::InputTag(jetTag_, "px", "PAT"),  jetHandlePx );
   iEvent.getByLabel( edm::InputTag(jetTag_, "py", "PAT"),  jetHandlePy );
   iEvent.getByLabel( edm::InputTag(jetTag_, "pz", "PAT"),  jetHandlePz );
   iEvent.getByLabel( edm::InputTag(jetTag_, "energy", "PAT"),  jetHandleE );

   iEvent.getByLabel( pdfTag_,  pdfWeightsHandle );
   iEvent.getByLabel( generatorTag_,  genHandle );


   std::vector<reco::Candidate::LorentzVector> jets;

   for ( unsigned int index = 0; index < jetHandlePx->size(); ++index ) {
     jets.push_back(  reco::Candidate::LorentzVector(
						     (*jetHandlePx)[index],
						     (*jetHandlePy)[index],
						     (*jetHandlePz)[index],
						     (*jetHandleE)[index]
						     ) );
   }

   if ( jets.size() < 2 )
     return;


   double genWeight = 1.0;
   if ( genHandle.isValid() ) {
     genWeight *= genHandle->weight();
   }


   float jetMass = (jets[0] + jets[1]).mass();

   for ( unsigned i = 0; i < 44; ++i ) {
     float weight = pdfWeightsHandle->at(i) * genWeight;
     massHists[i]->Fill( jetMass, weight );
   }

}



// ------------ method called once each job just before starting event loop  ------------
void 
EDJetMassPDFUncertainty::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EDJetMassPDFUncertainty::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
EDJetMassPDFUncertainty::beginRun(edm::Run const& run , edm::EventSetup const& eventSetup)
{

}

// ------------ method called when ending the processing of a run  ------------
void 
EDJetMassPDFUncertainty::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
EDJetMassPDFUncertainty::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
EDJetMassPDFUncertainty::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EDJetMassPDFUncertainty::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}



//define this as a plug-in
DEFINE_FWK_MODULE(EDJetMassPDFUncertainty);
