// -*- C++ -*-
//
// Package:    EDSingleJetTriggerAna
// Class:      EDSingleJetTriggerAna
// 
/**\class EDSingleJetTriggerAna EDSingleJetTriggerAna.cc Analysis/EDSingleJetTriggerAna/src/EDSingleJetTriggerAna.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Benedikt Hegner
//         Created:  Sat July 15 11:39:14 CDT 2011
// $Id: EDSingleJetTriggerAna.cc,v 1.1 2012/06/14 14:41:28 srappocc Exp $
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

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH2F.h"
#include "TH1F.h"
//
// class declaration
//

using namespace std;
using trigger::Keys;
using trigger::TriggerObject;
using edm::InputTag;



class EDSingleJetTriggerAna : public edm::EDAnalyzer {
   public:
      explicit EDSingleJetTriggerAna(const edm::ParameterSet&);
      ~EDSingleJetTriggerAna();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      virtual void getAodTriggerObjectsForModule (edm::InputTag collectionTag,
                                                  edm::Handle<trigger::TriggerEvent> aodTriggerEvent,
                                                  trigger::TriggerObjectCollection trigObjs,
                                                  std::vector<TriggerObject> & foundObjects  );

      // ----------member data ---------------------------

      std::string targetTrigger;
      double threshold_;
      std::string theHltProcessName; 
      bool verbose_;
      InputTag nameOfHLTFinalFilterModule;
      std::string jetTag_;
      bool inTable_;

  TH1D * jetPtNum;
  TH1D * jetPtDen;

  int nPassed_;
  int nTotal_;
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
EDSingleJetTriggerAna::EDSingleJetTriggerAna(const edm::ParameterSet& iConfig)

{
  verbose_ = iConfig.getUntrackedParameter<bool>("Verbose", false);
  theHltProcessName = iConfig.getUntrackedParameter<std::string>("HltProcessName", "HLT");
  targetTrigger = iConfig.getUntrackedParameter<std::string>("TargetTrigger", "HLT_Jet60_v");
  threshold_ = iConfig.getUntrackedParameter<double>("threshold", 100.0);
  jetTag_ = iConfig.getUntrackedParameter<std::string>("jetTag", "ak7Lite");

  edm::Service<TFileService> fs;
  nPassed_ = nTotal_ = 0;


  jetPtNum = fs->make<TH1D>("jetPtNum",  "Jet p_{T}, Numerator",   150, 0., 1500.);
  jetPtDen = fs->make<TH1D>("jetPtDen",  "Jet p_{T}, Denominator", 150, 0., 1500.);

  inTable_ = false;
}



EDSingleJetTriggerAna::~EDSingleJetTriggerAna()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
EDSingleJetTriggerAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  if ( !inTable_ )
    return;

   using namespace edm;

   if ( verbose_ )
     cout << "Passed event, analyzing the triggers" << endl;

   edm::Handle<trigger::TriggerEvent>         aodTriggerEvent;
   InputTag HltAodInputTag("hltTriggerSummaryAOD","","");
   iEvent.getByLabel(HltAodInputTag, aodTriggerEvent);

   edm::Handle<vector<float>  >   jetHandlePx;
   edm::Handle<vector<float>  >   jetHandlePy;
   edm::Handle<vector<float>  >   jetHandlePz;
   edm::Handle<vector<float>  >   jetHandleE;

   if ( verbose_ )
     cout << "Getting lite jet collection" << endl;

   iEvent.getByLabel( edm::InputTag(jetTag_, "px", "PAT"),  jetHandlePx );
   iEvent.getByLabel( edm::InputTag(jetTag_, "py", "PAT"),  jetHandlePy );
   iEvent.getByLabel( edm::InputTag(jetTag_, "pz", "PAT"),  jetHandlePz );
   iEvent.getByLabel( edm::InputTag(jetTag_, "energy", "PAT"),  jetHandleE );


   vector<reco::Candidate::LorentzVector> jets;

   for ( unsigned int index = 0; index < jetHandlePx->size(); ++index ) {
     jets.push_back(  reco::Candidate::LorentzVector(
						     (*jetHandlePx)[index],
						     (*jetHandlePy)[index],
						     (*jetHandlePz)[index],
						     (*jetHandleE)[index]
						     ) );

     if ( verbose_ ) {
       cout << "Added jet : (px,py,pz,e) = " <<
	 (*jetHandlePx)[index] << ", " <<
	 (*jetHandlePy)[index] << ", " <<
	 (*jetHandlePz)[index] << ", " <<
	 (*jetHandleE)[index] << endl;
     }
   }


   const trigger::TriggerObjectCollection trigObjs = aodTriggerEvent->getObjects();
   std::vector<TriggerObject> foundHLTTrigObjs; 

   getAodTriggerObjectsForModule ( nameOfHLTFinalFilterModule,
				   aodTriggerEvent,
				   trigObjs,
				   foundHLTTrigObjs );
   bool pass = false;
   if ( jets.size() < 2 ) {
     if ( verbose_ ) {
       cout << "Event has less than two jets, skipping" << endl;
     }
   }
   if ( jets.size() >= 2 ) {

     if ( verbose_ ) 
       cout << "Event has two jets" << endl;

     reco::Candidate::LorentzVector const & jet0 = jets[0];
     reco::Candidate::LorentzVector const & jet1 = jets[1];
     double ptJet = jet0.pt();


     double ptThreshold = std::max( ptJet * 0.1, 30.0 );
     int njetsAboveThreshold = 0;
     for ( unsigned int ijet = 0; ijet < jets.size(); ++ijet )
       if ( jets[ijet].pt() > ptThreshold ) 
	 ++njetsAboveThreshold;

     if ( jet0.pt() > 50 &&
	  fabs(jet0.eta()) < 2.4 &&
	  njetsAboveThreshold == 2
	  ) {
       if ( verbose_ ) {
	 cout << "Event passes preselection" << endl;
	 cout << "pt0 = " << jet0.pt() << ", pt1 = " << jet1.pt() << ", ptJet = " << ptJet << endl;
       }
       jetPtDen->Fill( ptJet );
       pass = true;
       ++nTotal_;
       
       bool passedTrig = false;
       if ( foundHLTTrigObjs.size() != 0 ){
	 double trigPt = foundHLTTrigObjs[0].pt();
	 if ( verbose_ ) {
	   cout << "trigPt = " << trigPt << ", threshold = " << threshold_ << endl;
	 }
	 if ( trigPt > threshold_ ) {
	   passedTrig = true;
	 }
       }
       if ( passedTrig ) {
	 if ( verbose_ ) {
	   cout << "Passed trigger!" << endl;
	 }
	 jetPtNum->Fill( ptJet );
	 ++nPassed_;
       }
     }
   }
}



// ------------ method called once each job just before starting event loop  ------------
void 
EDSingleJetTriggerAna::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EDSingleJetTriggerAna::endJob() 
{
  std::cout << " -------------- Efficiency --------------" << std::endl;
  char buff[1000];
  sprintf(buff, "Efficiency = %8d / %8d = %6.2f", nPassed_, nTotal_, (double)nPassed_/(double(nTotal_) ) );
  std::cout << buff << std::endl;
}

// ------------ method called when starting to processes a run  ------------
void 
EDSingleJetTriggerAna::beginRun(edm::Run const& run , edm::EventSetup const& eventSetup)
{

  HLTConfigProvider hltConfig;
    
  bool hltConfigChanged;
  bool hltConfigInitSuccess = hltConfig.init(run, eventSetup, theHltProcessName, hltConfigChanged);

  std::vector<std::string> validTriggerNames;

  if (hltConfigInitSuccess)
    validTriggerNames = hltConfig.triggerNames();

  if (validTriggerNames.size() < 1) {
    cout  << endl << endl << endl
          << "---> WARNING: The HLT Config Provider gave you an empty list of valid trigger names" << endl
          << "Could be a problem with the HLT Process Name (you provided  " << theHltProcessName <<")" << endl
          << "W/o valid triggers we can't produce plots, exiting..."
          << endl << endl << endl;

    int noValidHLTConfig = 0;
    assert (noValidHLTConfig);
    
  }

  vector<string>::const_iterator iDumpName;
  unsigned int numTriggers = 0;
  
  bool foundMatchingTrigger = false;
  
  for ( iDumpName = validTriggerNames.begin();
        iDumpName != validTriggerNames.end();
        iDumpName++) {

    if (verbose_) 
      cout << "Trigger   "  << numTriggers << "   =   "
           << (*iDumpName)
           << endl;
    size_t found;
    found= (*iDumpName).find(targetTrigger);

    if ( found!=string::npos ) {
      foundMatchingTrigger = true;
      targetTrigger = (*iDumpName);
      inTable_ = true;
      if (verbose_)
        cout << "---------> Trigger " << (*iDumpName)
             << " matches your TargetTrigger ( "
             << targetTrigger
             << ") " << endl;
    }

        
    ++numTriggers;
  }


  if (!foundMatchingTrigger) {
    cout << "Oops, the trigger you want to study "
         << "is not in this table :( "
         << endl;
    inTable_ = false;
    return;
  }


  ////////////////////////////////////////////////////////
  //
  //  Parse the list of modules for your trigger
  //  Look for
  //    1. The L1 Seed 
  //    2. The Final Filter
  /////////////////////////////////////////////////////////

  std::vector<std::string> moduleNames = hltConfig.moduleLabels (targetTrigger);

  string finalFilterString;
  for ( size_t i = 0; i < moduleNames.size(); i++ ) {
    string module = moduleNames[i];

    if ( TString(module).Contains ("Regional") ) {
      finalFilterString = module;
    }
                                  
    
  }

  nameOfHLTFinalFilterModule = InputTag(finalFilterString, "", theHltProcessName);
  //  cout << "Name is" << nameOfHLTFinalFilterModule << endl;  


}

// ------------ method called when ending the processing of a run  ------------
void 
EDSingleJetTriggerAna::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
EDSingleJetTriggerAna::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
EDSingleJetTriggerAna::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EDSingleJetTriggerAna::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

void 
EDSingleJetTriggerAna::getAodTriggerObjectsForModule (edm::InputTag collectionTag,
                                                  edm::Handle<trigger::TriggerEvent> aodTriggerEvent,
                                                  trigger::TriggerObjectCollection trigObjs,
                                                  std::vector<TriggerObject> & foundObjects  ) {


  if (verbose_)
    cout  << "Getting trigger objects for module label = " << collectionTag << endl;
  
  size_t filterIndex   = aodTriggerEvent->filterIndex( collectionTag );
    
  if (verbose_)
    cout << "\n\n filterIndex is "
         << filterIndex << "\n\n";
    
  if ( filterIndex < aodTriggerEvent->sizeFilters() ) {
    const Keys & keys = aodTriggerEvent->filterKeys( filterIndex );

    if (verbose_)
      cout << "\n\nGot keys"
           << "Key size is " << keys.size() << std::endl;;
                              
    // The keys are apparently pointers into the trigger
    // trigObjs collections
    // Use the key's to look up the particles for the
    // filter module that you're using 
      
    for ( size_t j = 0; j < keys.size(); j++ ){
      TriggerObject foundObject = trigObjs[keys[j]];

      // This is the trigger object. Apply your filter to it!
      if (verbose_)
        cout << "Found an objects with pt = "
             << foundObject.pt()
             << ", eta = " << foundObject.eta()
             << endl ;
        

      foundObjects.push_back( foundObject );
     
    }
  }

  
  
}


//define this as a plug-in
DEFINE_FWK_MODULE(EDSingleJetTriggerAna);
