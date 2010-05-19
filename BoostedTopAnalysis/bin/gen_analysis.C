#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"

#include "PhysicsTools/SelectorUtils/interface/RunLumiSelector.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/ChainEvent.h"

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()

using namespace std;


///-------------------------
/// DRIVER FUNCTION
///-------------------------

// -*- C++ -*-

// CMS includes
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ptr.h"


// Root includes
#include "TROOT.h"
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"


using namespace std;


///////////////////////////
// ///////////////////// //
// // Main Subroutine // //
// ///////////////////// //
///////////////////////////

int main (int argc, char* argv[]) 
{


  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  cout << "Hello from " << argv[0] << "!" << endl;


  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();


  cout << "Getting parameters" << endl;
  // Get the python configuration
  PythonProcessDesc builder(argv[1], argc, argv);
  boost::shared_ptr<edm::ProcessDesc> b = builder.processDesc();
  boost::shared_ptr<edm::ParameterSet> parameters = b->getProcessPSet();
  parameters->registerIt(); 


  edm::ParameterSet inputs              = parameters->getParameter<edm::ParameterSet>("inputs");
  edm::ParameterSet outputs             = parameters->getParameter<edm::ParameterSet>("outputs");

  cout << "setting up TFileService" << endl;
  // book a set of histograms
  fwlite::TFileService fs = fwlite::TFileService( outputs.getParameter<std::string>("outputName") );
  TFileDirectory theDir = fs.mkdir( "histos" ); 
    
  cout << "Setting up chain event" << endl;
  // This object 'event' is used both to get all information from the
  // event as well as to store histograms, etc.
  fwlite::ChainEvent ev ( inputs.getParameter<std::vector<std::string> > ("fileNames") );


  std::cout << "Making hadronic analysis object" << std::endl;

  TH1F * h_dijetMass = theDir.make<TH1F>("h_dijetMass", "Dijet Mass", 500, 0., 5000.);
  TH1F * h_genPt     = theDir.make<TH1F>("h_genPt", "GenJet p_{T}", 500, 0., 5000.);

  cout << "About to begin looping" << endl;

  int nev = 0;
  //loop through each event
  for (ev.toBegin(); ! ev.atEnd(); ++ev, ++nev) {
    edm::EventBase const & event = ev;


    if ( ev.event()->size() == 0 ) continue; // skip trees with no events

    edm::Handle< std::vector<reco::GenJet> > h_genJets;
    event.getByLabel< std::vector<reco::GenJet> > ( edm::InputTag("ca8GenJets"), h_genJets );

    if ( h_genJets->size() >= 2 ) {
      reco::GenJet const & jet0 = h_genJets->at(0);
      reco::GenJet const & jet1 = h_genJets->at(1);

      h_genPt->Fill( jet0.pt() );
      h_genPt->Fill( jet1.pt() );
      reco::Candidate::LorentzVector p4 = jet0.p4() + jet1.p4();
      h_dijetMass->Fill( p4.mass() );
      
    }

  } // end loop over events


  return 0;
}

