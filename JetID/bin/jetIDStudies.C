/*   A macro for making a histogram of Jet Pt with cuts
This is a basic way to cut out jets of a certain Pt and Eta using an if statement
This example creates a histogram of Jet Pt, using Jets with Pt above 30 and ETA above -2.1 and below 2.1
*/

#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"
#include "TLorentzVector.h"

#include "PhysicsTools/Utilities/interface/strbitset.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "PhysicsTools/Utilities/interface/Selector.h"
#include "PhysicsTools/PatUtils/interface/JetIDSelectionFunctor.h"

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()

using namespace std;


// make a selector for this selection
class PVSelector : public Selector<edm::EventBase> {
public:
  PVSelector( int minPVTracks = 2,
	      double maxPVZ = 20) 
  {
    push_back("PV NTrk", minPVTracks);
    push_back("PV Z", maxPVZ);
    set("PV NTrk");
    set("PV Z");
  }

  bool operator() ( edm::EventBase const & event,  std::strbitset & ret ) {
    event.getByLabel(edm::InputTag("offlinePrimaryVertices"), h_primVtx);

    // check if there is a good primary vertex
    if ( (h_primVtx->size() > 0 && h_primVtx->at(0).tracksSize() >= cut("PV NTrk", int()) ) 
	 || ignoreCut("PV NTrk")    ) {
      passCut(ret, "PV NTrk" );
      if ( (h_primVtx->size() > 0 && fabs(h_primVtx->at(0).z()) <= cut("PV Z", double()) ) 
	   || ignoreCut("PV Z")    ) 
	passCut(ret, "PV Z" );
      
    }
    return (bool)ret;
  }

  edm::Handle<vector<reco::Vertex> > const & vertices() const { return h_primVtx; }

private:
  edm::Handle<vector<reco::Vertex> > h_primVtx;
};





///-------------------------
/// DRIVER FUNCTION
///-------------------------

// -*- C++ -*-

// CMS includes
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 

// Root includes
#include "TROOT.h"

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
   optutl::CommandLineParser parser ("Jet ID studies");

   ////////////////////////////////////////////////
   // Change any defaults or add any new command //
   //      line options you would like here.     //
   ////////////////////////////////////////////////
   parser.stringValue ("outputFile") = "jetIDStudies"; // .root added automatically


   parser.addOption( "jetSrc", optutl::CommandLineParser::kString, 
		     "Jet source",
		     "selectedLayer1Jets" );

   parser.addOption( "doGen", optutl::CommandLineParser::kBool, 
		     "Match generator level stuff",
		     false );

   parser.addOption( "isData", optutl::CommandLineParser::kBool,
		     "Is this data?",
		     true );

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

   // Book those histograms!


   eventCont.add( new TH1D("hist_nJet", "Number of Jets", 10, 0, 10 ) );
   eventCont.add( new TH1D("hist_jetPt", "Jet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_jetEtaVsPhi", "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_jetNTracks", "Jet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}", 20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_jetEMF", "Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_jetCorr", "Jet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_n90Hits", "Jet n90Hits", 20, 0, 20) );
   eventCont.add( new TH1D("hist_fHPD", "Jet fHPD", 200, 0, 1) );
   eventCont.add( new TH1D("hist_nConstituents", "Jet nConstituents", 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_jetCHF", "Jet Charged Hadron Fraction", 200, 0, 1.0) );


   eventCont.add( new TH1D("hist_good_jetPt", "Jet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_good_jetEtaVsPhi", "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_good_jetNTracks", "Jet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_good_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}",20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_good_jetEMF", "Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_good_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_good_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_good_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_good_jetCorr", "Jet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_good_n90Hits", "Jet n90Hits", 20, 0, 20) );
   eventCont.add( new TH1D("hist_good_fHPD", "Jet fHPD", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_nConstituents", "Jet nConstituents", 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_good_jetCHF", "Jet Charged Hadron Fraction", 200, 0, 1.0) );

   eventCont.add( new TH1D("hist_good_dijets_jetPt", "Jet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_good_dijets_jetEtaVsPhi", "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_good_dijets_jetNTracks", "Jet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_good_dijets_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}",20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_good_dijets_jetEMF", "Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_dijets_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_good_dijets_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_good_dijets_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_good_dijets_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_dijets_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_good_dijets_jetCorr", "Jet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_good_dijets_n90Hits", "Jet n90Hits", 20, 0, 20) );
   eventCont.add( new TH1D("hist_good_dijets_fHPD", "Jet fHPD", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_dijets_nConstituents", "Jet nConstituents", 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_good_dijets_jetCHF", "Jet Charged Hadron Fraction", 200, 0, 1.0) );
   

   eventCont.add( new TH1D("hist_good_notracks_jetPt", "Jet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_good_notracks_jetEtaVsPhi", "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_good_notracks_jetNTracks", "Jet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_good_notracks_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}",20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_good_notracks_jetEMF", "Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_notracks_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_good_notracks_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_good_notracks_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_good_notracks_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_notracks_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_good_notracks_jetCorr", "Jet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_good_notracks_n90Hits", "Jet n90Hits", 20, 0, 20) );
   eventCont.add( new TH1D("hist_good_notracks_fHPD", "Jet fHPD", 200, 0, 1) );
   eventCont.add( new TH1D("hist_good_notracks_nConstituents", "Jet nConstituents", 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_good_notracks_jetCHF", "Jet Charged Hadron Fraction", 200, 0, 1.0) );
   

   eventCont.add( new TH1D("hist_nGeneralTracks", "Number of General Tracks", 100, 0, 100) );
   eventCont.add( new TH1D("hist_primVtxNTracks", "Number of Tracks in Primary Vertex", 100, 0, 100) );
   eventCont.add( new TH1D("hist_primVtxChi2", "Primary Vertex #chi^{2}", 100, 0, 20 ) );

   eventCont.add( new TH1D("hist_mjj", "Dijet mass", 300, 0, 300 ) );
   eventCont.add( new TH1D("hist_dR_jj", "#Delta R_{JJ}", 200, 0, TMath::TwoPi() ) );
   eventCont.add( new TH1D("hist_imbalance_jj", "Dijet imbalance", 200, -1.0, 1.0 )  );



   //////////////////////
   // //////////////// //
   // // Event Loop // //
   // //////////////// //
   //////////////////////
  PVSelector pvSelector;
  JetIDSelectionFunctor jetSelector( JetIDSelectionFunctor::CRAFT08, 
				     JetIDSelectionFunctor::TIGHT );
  

  int nev = 0;
  //loop through each event
  for (eventCont.toBegin(); ! eventCont.atEnd(); ++eventCont) {


    edm::EventBase const & event = eventCont;

    // Select the PV
    std::strbitset retPV = pvSelector.getBitTemplate();
    retPV.set(false);
    pvSelector( event, retPV );
    edm::Handle<vector<reco::Vertex> > const & vertices = pvSelector.vertices();

    edm::Handle<vector<reco::Track> > h_tracks;
    event.getByLabel( edm::InputTag("generalTracks"), h_tracks );

    // Plot some PV info
    eventCont.hist("hist_primVtxNTracks")->Fill( vertices->at(0).tracksSize() );
    eventCont.hist("hist_primVtxChi2")->Fill( vertices->at(0).normalizedChi2() );
    eventCont.hist("hist_nGeneralTracks")->Fill( h_tracks->size() );

    edm::Handle<vector<pat::Jet> > h_jets;
    event.getByLabel( edm::InputTag( parser.stringValue("jetSrc")), h_jets );

    std::strbitset retJet = jetSelector.getBitTemplate();

    std::vector<unsigned int> goodJetIndices;

    for ( std::vector<pat::Jet>::const_iterator jetBegin = h_jets->begin(),
	    jetEnd = h_jets->end(), ijet = jetBegin;
	  ijet != jetEnd; ++ijet ) {
	
      const pat::Jet & jet = *ijet;
	
      double pt = jet.pt();
      
      retJet.set(false);
      jetSelector( jet, retJet );
      if ( retJet.test(string("MINIMAL_EMF")) &&
	   retJet.test(string("LOOSE_N90Hits"))) {
	const reco::TrackRefVector & jetTracks = jet.associatedTracks();
	
	if ( static_cast<int>(jet.jetID().n90Hits) == 1 ) { 
	  cout << endl << endl << endl << "---------------------------------->>>>> THIS ONE IS BUGGED! <<<<<<======" << endl;
	  retJet.print(std::cout);
	  cout << endl << endl;
	}
	  
	if ( fabs(jet.eta()) < 2.6 ) {
	  if ( parser.boolValue("isData") ) {
	    char buffjet[1000];
	    sprintf (buffjet, "Good jet pt = %6.2f, eta = %6.2f, phi = %6.2f, emf = %6.2f, n90hits = %6d",
		     jet.pt(), jet.eta(), jet.phi(), jet.emEnergyFraction(), static_cast<int>(jet.jetID().n90Hits) );
	    cout << buffjet << endl;
	  }
	  
	  // get "uncleaned" jets
	  eventCont.hist("hist_jetPt")->Fill( pt );
	  eventCont.hist("hist_jetEtaVsPhi")->Fill( jet.eta(), jet.phi() );
	  eventCont.hist("hist_jetNTracks")->Fill( jetTracks.size() );
	  eventCont.hist("hist_jetNTracksVsPt")->Fill( pt, jetTracks.size() );
	  eventCont.hist("hist_jetEMF")->Fill( jet.emEnergyFraction() );
	  eventCont.hist("hist_jetCorr")->Fill( jet.corrFactor("raw") );
	  eventCont.hist("hist_n90Hits")->Fill( static_cast<int>(jet.jetID().n90Hits) );
	  eventCont.hist("hist_fHPD")->Fill( jet.jetID().fHPD );
	  eventCont.hist("hist_nConstituents")->Fill( jet.nConstituents() );



	  if ( parser.boolValue("doGen") && jet.genJet() != 0 ) {
	    eventCont.hist("hist_jetGenEmE")->Fill( jet.genJet()->emEnergy() );
	    eventCont.hist("hist_jetGenHadE")->Fill( jet.genJet()->hadEnergy() );
	    eventCont.hist("hist_jetEoverGenE")->Fill( jet.energy() / jet.genJet()->energy() );

	    eventCont.hist("hist_jetGenEMF")->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	  }

	  if ( retPV ) {
	    goodJetIndices.push_back( ijet - jetBegin );
	    eventCont.hist("hist_good_jetPt")->Fill( pt );
	    eventCont.hist("hist_good_jetEtaVsPhi")->Fill( jet.eta(), jet.phi() );
	    eventCont.hist("hist_good_jetNTracks")->Fill( jetTracks.size() );
	    eventCont.hist("hist_good_jetNTracksVsPt")->Fill( pt, jetTracks.size() );
	    eventCont.hist("hist_good_jetEMF")->Fill( jet.emEnergyFraction() );	
	    eventCont.hist("hist_good_jetCorr")->Fill( jet.corrFactor("raw") );
	    eventCont.hist("hist_good_n90Hits")->Fill( static_cast<int>(jet.jetID().n90Hits) );
	    eventCont.hist("hist_good_fHPD")->Fill( jet.jetID().fHPD );
	    eventCont.hist("hist_good_nConstituents")->Fill( jet.nConstituents() );

	    if ( parser.boolValue("doGen") && jet.genJet() != 0 ) {
	      eventCont.hist("hist_good_jetGenEmE")->Fill( jet.genJet()->emEnergy() );
	      eventCont.hist("hist_good_jetGenHadE")->Fill( jet.genJet()->hadEnergy() );
	      eventCont.hist("hist_good_jetEoverGenE")->Fill( jet.energy() / jet.genJet()->energy() );

	      eventCont.hist("hist_good_jetGenEMF")->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	    }

	    TLorentzVector p4_tracks(0,0,0,0);
	    for ( reco::TrackRefVector::const_iterator itrk = jetTracks.begin(),
		    itrkBegin = jetTracks.begin(), itrkEnd = jetTracks.end();
		itrk != itrkEnd; ++itrk ) {
	      TLorentzVector p4_trk;
	      double M_PION = 0.140;
	      p4_trk.SetPtEtaPhiM( (*itrk)->pt(), (*itrk)->eta(), (*itrk)->phi(), M_PION );
	      p4_tracks += p4_trk;
	    }
	    eventCont.hist("hist_good_jetCHF")->Fill( p4_tracks.Energy() / jet.energy() );

	    if ( jetTracks.size() == 0 ) {
	      eventCont.hist("hist_good_notracks_jetPt")->Fill( pt );
	      eventCont.hist("hist_good_notracks_jetEtaVsPhi")->Fill( jet.eta(), jet.phi() );
	      eventCont.hist("hist_good_notracks_jetNTracks")->Fill( jetTracks.size() );
	      eventCont.hist("hist_good_notracks_jetNTracksVsPt")->Fill( pt, jetTracks.size() );
	      eventCont.hist("hist_good_notracks_jetEMF")->Fill( jet.emEnergyFraction() );	  
	      eventCont.hist("hist_good_notracks_jetCorr")->Fill( jet.corrFactor("raw") );
	      eventCont.hist("hist_good_notracks_n90Hits")->Fill( static_cast<int>(jet.jetID().n90Hits) );
	      eventCont.hist("hist_good_notracks_fHPD")->Fill( jet.jetID().fHPD );
	      eventCont.hist("hist_good_notracks_nConstituents")->Fill( jet.nConstituents() );

	      if ( parser.boolValue("doGen") && jet.genJet() != 0 ) {
		eventCont.hist("hist_good_notracks_jetGenEmE")->Fill( jet.genJet()->emEnergy() );
		eventCont.hist("hist_good_notracks_jetGenHadE")->Fill( jet.genJet()->hadEnergy() );
		eventCont.hist("hist_good_notracks_jetEoverGenE")->Fill( jet.energy() / jet.genJet()->energy() );

		eventCont.hist("hist_good_notracks_jetGenEMF")->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	      }

	    } // end if no tracks

	  } // end if good PV

	} // end if |eta| < 2.1
	
      } // end if good jet
      
    } // end loop over jets

    

    if ( goodJetIndices.size() >= 2 ) {
      pat::Jet const & jet0 = h_jets->at( goodJetIndices[0] );
      pat::Jet const & jet1 = h_jets->at( goodJetIndices[1] );

      TLorentzVector p4_j0( jet0.px(), jet0.py(), jet0.pz(), jet0.energy() );
      TLorentzVector p4_j1( jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );

      TLorentzVector p4_jj = p4_j0 + p4_j1;

      eventCont.hist("hist_mjj")->Fill( p4_jj.M() );
      eventCont.hist("hist_dR_jj")->Fill( p4_j0.DeltaR( p4_j1 ) );
      eventCont.hist("hist_imbalance_jj")->Fill( (p4_j0.Perp() - p4_j1.Perp() ) /
						 (p4_j0.Perp() + p4_j1.Perp() ) );

      eventCont.hist("hist_good_dijets_jetPt")->Fill( jet0.pt() );
      eventCont.hist("hist_good_dijets_jetEtaVsPhi")->Fill( jet0.eta(), jet0.phi() );
      eventCont.hist("hist_good_dijets_jetNTracks")->Fill( jet0.associatedTracks().size() );
      eventCont.hist("hist_good_dijets_jetNTracksVsPt")->Fill( jet0.pt(), jet0.associatedTracks().size() );
      eventCont.hist("hist_good_dijets_jetEMF")->Fill( jet0.emEnergyFraction() );	
      eventCont.hist("hist_good_dijets_jetCorr")->Fill( jet0.corrFactor("raw") );
      eventCont.hist("hist_good_dijets_n90Hits")->Fill( static_cast<int>(jet0.jetID().n90Hits) );
      eventCont.hist("hist_good_dijets_fHPD")->Fill( jet0.jetID().fHPD );
      eventCont.hist("hist_good_dijets_nConstituents")->Fill( jet0.nConstituents() );


      eventCont.hist("hist_good_dijets_jetPt")->Fill( jet1.pt() );
      eventCont.hist("hist_good_dijets_jetEtaVsPhi")->Fill( jet1.eta(), jet1.phi() );
      eventCont.hist("hist_good_dijets_jetNTracks")->Fill( jet1.associatedTracks().size() );
      eventCont.hist("hist_good_dijets_jetNTracksVsPt")->Fill( jet1.pt(), jet1.associatedTracks().size() );
      eventCont.hist("hist_good_dijets_jetEMF")->Fill( jet1.emEnergyFraction() );	
      eventCont.hist("hist_good_dijets_jetCorr")->Fill( jet1.corrFactor("raw") );
      eventCont.hist("hist_good_dijets_n90Hits")->Fill( static_cast<int>(jet1.jetID().n90Hits) );
      eventCont.hist("hist_good_dijets_fHPD")->Fill( jet1.jetID().fHPD );
      eventCont.hist("hist_good_dijets_nConstituents")->Fill( jet1.nConstituents() );

      
      if ( parser.boolValue("isData") ) {
	char mjjbuff[1000];
	sprintf(mjjbuff, "Dijet candidate : Run %12d, Event %16d, mjj = %6.2f",
		event.id().run(),  event.id().event(),  p4_jj.M());
	cout << mjjbuff << endl;
      }
      
    }
    
  } // end loop over events
    
  // print PV selection
  cout << "PV Selection: "<< endl;
  pvSelector.print(std::cout);

  cout << "Jet selection (NOTE: Only minimal_emf cuts applied to plots): " << endl;
  jetSelector.print(std::cout);


      
   ////////////////////////
   // ////////////////// //
   // // Clean Up Job // //
   // ////////////////// //
   ////////////////////////

   // Histograms will be automatically written to the root file
   // specificed by command line options.

   // All done!  Bye bye.
   return 0;
}

