#ifndef Analysis_VPlusJets_interface_VPlusJets_h
#define Analysis_VPlusJets_interface_VPlusJets_h


// -*- C++ -*-
//
// Package:    VPlusJets
// Class:      VPlusJets
// 
/**\class VPlusJets VPlusJets.cc Analysis/VPlusJets/src/VPlusJets.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Thu Apr  9 14:42:23 CDT 2009
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

//
// class declaration
//

class VPlusJets : public edm::EDFilter {
   public:
      explicit VPlusJets(const edm::ParameterSet&);
      ~VPlusJets();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------

      // bools to make or not
      bool makeMuons_;
      bool makeElectrons_;

      // input source
      edm::InputTag muonSrc_;
      edm::InputTag electronSrc_;

      // filter numbers
      unsigned int minMuons_;
      unsigned int maxMuons_;
      unsigned int minElectrons_;
      unsigned int maxElectrons_;

      // muon cuts
      double          chi2CutMuon_;
      double          d0CutMuon_;
      unsigned int    nHitsCutMuon_;
      double          hcalEtCutMuon_;
      double          ecalEtCutMuon_;
      double          relIsoCutMuon_;

      // electron cuts
      double          d0CutElectron_;
      double          relIsoCutElectron_;
      bool            convVetoElectron_;
};


#endif
