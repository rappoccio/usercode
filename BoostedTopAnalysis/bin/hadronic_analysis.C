// -*- C++ -*-

// CMS includes
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#include "Analysis/BoostedTopAnalysis/interface/HadronicSelection.h"

#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 


#include <iostream>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>

// Root includes
#include "TROOT.h"
#include "TLorentzVector.h"

using namespace std;


///////////////////////////
// ///////////////////// //
// // Main Subroutine // //
// ///////////////////// //
///////////////////////////

int main (int argc, char* argv[]) 
{
   ////////////////////////////////
   // ////////////////////////// //
   // // Command Line Options // //
   // ////////////////////////// //
   ////////////////////////////////

   // Tell people what this analysis code does and setup default options.
   optutl::CommandLineParser parser ("Boosted Top All Hadronic Example");

   ////////////////////////////////////////////////
   // Change any defaults or add any new command //
   //      line options you would like here.     //
   ////////////////////////////////////////////////
   parser.stringValue ("outputFile") = "ttbsm_had"; // .root added automatically

   // Parse the command line arguments
   parser.parseArguments (argc, argv);

   //////////////////////////////////
   // //////////////////////////// //
   // // Create Event Container // //
   // //////////////////////////// //
   //////////////////////////////////

   // This object 'event' is used both to get all information from the
   // event as well as to store histograms, etc.
   fwlite::EventContainer eventCont (parser);

   ////////////////////////////////////////
   // ////////////////////////////////// //
   // //         Begin Run            // //
   // // (e.g., book histograms, etc) // //
   // ////////////////////////////////// //
   ////////////////////////////////////////

   std::string tagName = "CATopCaloJet";

  // Tight jet id
  boost::shared_ptr<JetIDSelectionFunctor> jetIdTight      
    ( new JetIDSelectionFunctor( JetIDSelectionFunctor::CRAFT08, 
				 JetIDSelectionFunctor::TIGHT) );

   boost::shared_ptr<CATopTagFunctor> caTopTagFunctor
     ( new CATopTagFunctor( CATopTagFunctor::CALO, 
			    CATopTagFunctor::TIGHT,
			    tagName ) );

   HadronicSelection caTopHadronic(
     edm::InputTag("selectedLayer1JetsTopTagCalo"),
     edm::InputTag("patTriggerEvent"),
     jetIdTight,caTopTagFunctor,
     2,
     2,
     250,
     2.5,
     100., 250.,
     50.,
     0., 1000000.
     );

   // Setup a style
   gROOT->SetStyle ("Plain");

   // Book those histograms!
   eventCont.add( new TH1F( "jetPt", "Jet p_{T};Jet p_{T} (GeV/c)", 60, 0, 3000) );
   eventCont.add( new TH1F( "topMass", "Top Mass;Top Mass (GeV/c^{2}", 100, 0, 500 ) );
   eventCont.add( new TH1F( "minMass", "Jet Min Mass;Min Mass (GeV/c^{2})", 100, 0, 200 ) );
   eventCont.add( new TH1F( "wMass",   "W Mass;W Mass (GeV/c^{2})", 100, 0, 200 ) );

   eventCont.add( new TH1F( "dijetMassGen", "Dijet Mass, Generator Level;Mass (GeV/c^{2})", 500, 0, 5000 ) );
   eventCont.add( new TH1F( "dijetMassPre", "Dijet Mass Before Tagging;Mass (GeV/c^{2})", 500, 0, 5000 ) );
   eventCont.add( new TH1F( "dijetMassTag", "Dijet Mass, 2 Tags;Mass (GeV/c^{2})", 500, 0, 5000 ) );

   //////////////////////
   // //////////////// //
   // // Event Loop // //
   // //////////////// //
   //////////////////////

   for (eventCont.toBegin(); ! eventCont.atEnd(); ++eventCont) {
     

    edm::Handle<vector<reco::GenJet> > h_genJets;
    eventCont.getByLabel( edm::InputTag("ca8GenJets"), h_genJets);

    if ( !h_genJets.isValid() || h_genJets->size() < 2 ) continue;
    vector<reco::GenJet> const & genJets   = *h_genJets;

    TLorentzVector genJ0( genJets[0].px(),
			  genJets[0].py(),
			  genJets[0].pz(),
			  genJets[0].energy());
    TLorentzVector genJ1( genJets[1].px(),
			  genJets[1].py(),
			  genJets[1].pz(),
			  genJets[1].energy());
    TLorentzVector genJ = genJ0 + genJ1;
    eventCont.hist("dijetMassGen")->Fill( genJ.M() );
			  
    std::strbitset ret = caTopHadronic.getBitTemplate();
     
    bool passed = caTopHadronic(eventCont, ret);
    vector<pat::Jet>      const & jets      = caTopHadronic.selectedJets();
    vector<pat::Jet>      const & tags      = caTopHadronic.taggedJets();


    if ( ret[std::string(">= 1 Tight Jet")] ) {
      for ( vector<pat::Jet>::const_iterator jetsBegin = jets.begin(),
	      jetsEnd = jets.end(),
	      ijet = jetsBegin;
	    ijet != jetsEnd;
	    ++ijet ) {
	
	
	const reco::CATopJetTagInfo * catopTag = 
	  dynamic_cast<reco::CATopJetTagInfo const *>(ijet->tagInfo(tagName));
	eventCont.hist("jetPt")->Fill( ijet->pt() );
	if ( catopTag != 0 && catopTag->properties().minMass < 999999.) {
	  eventCont.hist("topMass")->Fill( catopTag->properties().topMass );
	  eventCont.hist("minMass")->Fill( catopTag->properties().minMass );
	  eventCont.hist("wMass")  ->Fill( catopTag->properties().wMass );
	}
      }

      if ( ret[std::string(">= N Tight Jets")] ) {
	TLorentzVector j0 ( jets[0].px(),
			    jets[0].py(),
			    jets[0].pz(),
			    jets[0].energy() );
	TLorentzVector j1 ( jets[1].px(),
			    jets[1].py(),
			    jets[1].pz(),
			    jets[1].energy() );
	TLorentzVector j = j0 + j1;
	eventCont.hist("dijetMassPre")->Fill( j.M() );
	if ( passed ) {
	  eventCont.hist("dijetMassTag")->Fill( j.M() );
	}
      }
    }


   } // for eventCont

      
   ////////////////////////
   // ////////////////// //
   // // Clean Up Job // //
   // ////////////////// //
   ////////////////////////

   caTopHadronic.print(cout);

   // Histograms will be automatically written to the root file
   // specificed by command line options.

   // All done!  Bye bye.
   return 0;
}


