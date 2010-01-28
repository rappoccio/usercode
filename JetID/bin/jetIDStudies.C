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
#include "PhysicsTools/PatUtils/interface/PFJetIDSelectionFunctor.h"
#include "Analysis/AnalysisFilters/interface/PVSelector.h"

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

   parser.addOption( "pfjetSrc", optutl::CommandLineParser::kString, 
		     "PFJet source",
		     "selectedLayer1JetsPF" );

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
   


   ///-------- PF JETS
   

   eventCont.add( new TH1D("hist_pf_nJet", "Number of Jets", 10, 0, 10 ) );
   eventCont.add( new TH1D("hist_pf_jetPt", "PFJet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_pf_jetEtaVsPhi", "PFJet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_pf_jetNTracks", "PFJet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_pf_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}", 20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_pf_jetEMF", "PFJet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_jetCHF", "PFJet CHF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_jetNHF", "PFJet NHF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_jetCEF", "PFJet CEF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_jetNEF", "PFJet NEF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_pf_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_pf_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_pf_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_pf_jetCorr", "PFJet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_pf_nConstituents", "PFJet nConstituents", 20, 0, 20 ) );



   eventCont.add( new TH1D("hist_pf_good_jetPt", "PFJet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_pf_good_jetEtaVsPhi", "PFJet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_pf_good_jetNTracks", "PFJet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_pf_good_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}",20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_pf_good_jetEMF", "PFJet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_jetCHF", "PFJet CHF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_jetNHF", "PFJet NHF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_jetCEF", "PFJet CEF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_jetNEF", "PFJet NEF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_pf_good_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_pf_good_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_pf_good_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_pf_good_jetCorr", "PFJet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_pf_good_nConstituents", "PFJet nConstituents", 20, 0, 20 ) );

   eventCont.add( new TH1D("hist_pf_good_dijets_jetPt", "PFJet p_{T}", 400, 0, 400 ) );
   eventCont.add( new TH2D("hist_pf_good_dijets_jetEtaVsPhi", "PFJet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetNTracks", "PFJet N_{TRACKS}", 20, 0, 20 ) );
   eventCont.add( new TH2D("hist_pf_good_dijets_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) );N_{Tracks}",20, 0, 200, 20, 0, 20 ) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetEMF", "PFJet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetCHF", "PFJet CHF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetNHF", "PFJet NHF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetCEF", "PFJet CEF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetNEF", "PFJet NEF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetPdgID", "PDG Id of Jet Constituents", 10000, 0, 10000 ) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetGenEmE", "Gen Jet EM Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetGenHadE", "Gen Jet HAD Energy", 200, 0, 200 ) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetGenEMF", "Gen Jet EMF", 200, 0, 1) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetEoverGenE", "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) );
   eventCont.add( new TH1D("hist_pf_good_dijets_jetCorr", "PFJet Correction Factor", 200, 0, 1.0 ) );
   eventCont.add( new TH1D("hist_pf_good_dijets_nConstituents", "PFJet nConstituents", 20, 0, 20 ) );




   /// Event quantities

   eventCont.add( new TH1D("hist_nGeneralTracks", "Number of General Tracks", 100, 0, 100) );
   eventCont.add( new TH1D("hist_primVtxNTracks", "Number of Tracks in Primary Vertex", 100, 0, 100) );
   eventCont.add( new TH1D("hist_primVtxNDof", "Number of Degrees of Freedom in Primary Vertex", 100, 0, 100) );
   eventCont.add( new TH1D("hist_primVtxChi2", "Primary Vertex #chi^{2}", 100, 0, 20 ) );

   eventCont.add( new TH1D("hist_mjj", "Dijet mass", 300, 0, 300 ) );
   eventCont.add( new TH1D("hist_dR_jj", "#Delta R_{JJ}", 200, 0, TMath::TwoPi() ) );
   eventCont.add( new TH1D("hist_imbalance_jj", "Dijet imbalance", 200, -1.0, 1.0 )  );

   eventCont.add( new TH1D("hist_pf_mjj", "Dijet mass", 300, 0, 300 ) );
   eventCont.add( new TH1D("hist_pf_dR_jj", "#Delta R_{JJ}", 200, 0, TMath::TwoPi() ) );
   eventCont.add( new TH1D("hist_pf_imbalance_jj", "Dijet imbalance", 200, -1.0, 1.0 )  );


   //////////////////////
   // //////////////// //
   // // Event Loop // //
   // //////////////// //
   //////////////////////
   PVSelector pvSelector( edm::InputTag("offlinePrimaryVertices"), 5., 15. );
   JetIDSelectionFunctor jetSelector( JetIDSelectionFunctor::CRAFT08, 
				      JetIDSelectionFunctor::TIGHT );

   PFJetIDSelectionFunctor pfjetSelector( PFJetIDSelectionFunctor::FIRSTDATA, 
					  PFJetIDSelectionFunctor::TIGHT,
					  0.0,
					  0.9,
					  0.9 );

  

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

//     edm::Handle<vector<reco::CaloJet> > h_calojets;
//     event.getByLabel( edm::InputTag("ak5CaloJets"), h_calojets );
//     edm::Handle<vector<pat::Jet> > h_patjets;
//     event.getByLabel( edm::InputTag("selectedLayer1Jets"), h_patjets );

//     for ( vector<reco::CaloJet>::const_iterator caloBegin = h_calojets->begin(),
// 	    caloEnd = h_calojets->end(), icalo = caloBegin;
// 	  icalo != caloEnd; ++icalo ) {
//       cout << "Calo jet " << icalo - caloBegin << ", pt = " << icalo->pt() << endl;
//     }
    

//     for ( vector<pat::Jet>::const_iterator patBegin = h_patjets->begin(),
// 	    patEnd = h_patjets->end(), ipat = patBegin;
// 	  ipat != patEnd; ++ipat ) {
//       cout << "Pat jet  " << ipat - patBegin << ", pt = " << ipat->correctedJet("raw").pt() << endl;
//     }
  

    // Plot some PV info
    eventCont.hist("hist_primVtxNTracks")->Fill( vertices->at(0).tracksSize() );
    eventCont.hist("hist_primVtxNDof")->Fill( vertices->at(0).ndof() );
    eventCont.hist("hist_primVtxChi2")->Fill( vertices->at(0).normalizedChi2() );
    eventCont.hist("hist_nGeneralTracks")->Fill( h_tracks->size() );


    ///------------------
    /// CALO JETS
    ///------------------

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
      bool selected = jetSelector( jet, retJet );

      bool minimal = retJet.test(string("MINIMAL_EMF") );
      bool loose_n90hits = retJet.test(string("LOOSE_N90Hits"));


      if ( minimal &&
	   loose_n90hits ) {
	const reco::TrackRefVector & jetTracks = jet.associatedTracks();
	
	if ( static_cast<int>(jet.jetID().n90Hits) == 1 ) { 
	  cout << endl << endl << endl << "---------------------------------->>>>> THIS ONE IS BUGGED! <<<<<<======" << endl;
	  retJet.print(std::cout);
	  cout << endl << endl;
	}
	  
	if ( fabs(jet.eta()) < 2.6 ) {

	  
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

    }



    ///------------------
    /// PF JETS
    ///------------------

    edm::Handle<vector<pat::Jet> > h_pfjets;
    event.getByLabel( edm::InputTag( parser.stringValue("pfJetSrc")), h_pfjets );

    std::strbitset retPFJet = pfjetSelector.getBitTemplate();

    std::vector<unsigned int> goodPFJetIndices;

    for ( std::vector<pat::Jet>::const_iterator jetBegin = h_pfjets->begin(),
	    jetEnd = h_pfjets->end(), ijet = jetBegin;
	  ijet != jetEnd; ++ijet ) {
	
      const pat::Jet & jet = *ijet;
	
      double pt = jet.pt();
      
      retPFJet.set(false);
      bool selected = pfjetSelector( jet, retPFJet );



      if ( selected ) {

	  
	if ( fabs(jet.eta()) < 3.0 ) {

	  
	  // get "uncleaned" jets
	  eventCont.hist("hist_pf_jetPt")->Fill( pt );
	  eventCont.hist("hist_pf_jetEtaVsPhi")->Fill( jet.eta(), jet.phi() );
	  eventCont.hist("hist_pf_nConstituents")->Fill( jet.nConstituents() );



	  if ( parser.boolValue("doGen") && jet.genJet() != 0 ) {
	    eventCont.hist("hist_pf_jetGenEmE")->Fill( jet.genJet()->emEnergy() );
	    eventCont.hist("hist_pf_jetGenHadE")->Fill( jet.genJet()->hadEnergy() );
	    eventCont.hist("hist_pf_jetEoverGenE")->Fill( jet.energy() / jet.genJet()->energy() );

	    eventCont.hist("hist_pf_jetGenEMF")->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	  }

	  if ( retPV ) {
	    goodJetIndices.push_back( ijet - jetBegin );
	    eventCont.hist("hist_pf_good_jetPt")->Fill( pt );
	    eventCont.hist("hist_pf_good_jetEtaVsPhi")->Fill( jet.eta(), jet.phi() );
	    eventCont.hist("hist_pf_good_nConstituents")->Fill( jet.nConstituents() );

	    if ( parser.boolValue("doGen") && jet.genJet() != 0 ) {
	      eventCont.hist("hist_pf_good_jetGenEmE")->Fill( jet.genJet()->emEnergy() );
	      eventCont.hist("hist_pf_good_jetGenHadE")->Fill( jet.genJet()->hadEnergy() );
	      eventCont.hist("hist_pf_good_jetEoverGenE")->Fill( jet.energy() / jet.genJet()->energy() );

	      eventCont.hist("hist_pf_good_jetGenEMF")->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	    }
	  } // end if good PV

	} // end if |eta| < 2.1
	
      } // end if good jet
      
    } // end loop over jets

    

    if ( goodPFJetIndices.size() >= 2 ) {
      pat::Jet const & jet0 = h_jets->at( goodPFJetIndices[0] );
      pat::Jet const & jet1 = h_jets->at( goodPFJetIndices[1] );

      TLorentzVector p4_j0( jet0.px(), jet0.py(), jet0.pz(), jet0.energy() );
      TLorentzVector p4_j1( jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );

      TLorentzVector p4_jj = p4_j0 + p4_j1;

      eventCont.hist("hist_pf_mjj")->Fill( p4_jj.M() );
      eventCont.hist("hist_pf_dR_jj")->Fill( p4_j0.DeltaR( p4_j1 ) );
      eventCont.hist("hist_pf_imbalance_jj")->Fill( (p4_j0.Perp() - p4_j1.Perp() ) /
						    (p4_j0.Perp() + p4_j1.Perp() ) );

      eventCont.hist("hist_pf_good_dijets_jetPt")->Fill( jet0.pt() );
      eventCont.hist("hist_pf_good_dijets_jetEtaVsPhi")->Fill( jet0.eta(), jet0.phi() );
      eventCont.hist("hist_pf_good_dijets_jetEMF")->Fill( jet0.emEnergyFraction() );	
      eventCont.hist("hist_pf_good_dijets_jetCorr")->Fill( jet0.corrFactor("raw") );
      eventCont.hist("hist_pf_good_dijets_nConstituents")->Fill( jet0.nConstituents() );


      eventCont.hist("hist_pf_good_dijets_jetPt")->Fill( jet1.pt() );
      eventCont.hist("hist_pf_good_dijets_jetEtaVsPhi")->Fill( jet1.eta(), jet1.phi() );
      eventCont.hist("hist_pf_good_dijets_jetEMF")->Fill( jet1.emEnergyFraction() );	
      eventCont.hist("hist_pf_good_dijets_jetCorr")->Fill( jet1.corrFactor("raw") );
      eventCont.hist("hist_pf_good_dijets_nConstituents")->Fill( jet1.nConstituents() );

      
      
   
      
    } // end if 2 good PF jets
    
  
    
  } // end loop over events
    
    // print PV selection
  cout << "PV Selection: "<< endl;
  pvSelector.print(std::cout);

  cout << "Calo Jet selection (NOTE: Only minimal_emf cuts applied to plots): " << endl;
  jetSelector.print(std::cout);
  cout << "PF Jet selection: " << endl;
  pfjetSelector.print(std::cout);


      
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

