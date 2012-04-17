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
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "PhysicsTools/Utilities/interface/EventSelector.h"

#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 

// Root includes
#include "TROOT.h"

using namespace std;


class JetIDStudiesSelector : public EventSelector {
public:
  JetIDStudiesSelector( boost::shared_ptr<PVSelector> const & pvSel,
			boost::shared_ptr<JetIDSelectionFunctor> const & jetSel,
			boost::shared_ptr<PFJetIDSelectionFunctor> const & pfJetSel,
			edm::InputTag jetSrc,
			edm::InputTag pfJetSrc,
			bool useCalo ) :
    pvSelector_(pvSel), jetSel_(jetSel), pfJetSel_(pfJetSel),
    jetSrc_(jetSrc), pfJetSrc_(pfJetSrc) {

    push_back("PV");
    push_back("Calo Cuts");
    push_back("Calo Kin Cuts");
    push_back("Calo Delta Phi");
    push_back("Calo Jet ID");
    push_back("PF Cuts");
    push_back("PF Kin Cuts");
    push_back("PF Delta Phi");
    push_back("PF Jet ID");

    set("PV");
    set("Calo Cuts", useCalo);
    set("Calo Kin Cuts", useCalo);
    set("Calo Delta Phi", useCalo);
    set("Calo Jet ID", useCalo);
    set("PF Cuts", !useCalo);
    set("PF Kin Cuts", !useCalo);
    set("PF Delta Phi", !useCalo);    
    set("PF Jet ID", !useCalo);
  }

  virtual ~JetIDStudiesSelector() {}

  virtual bool operator()( edm::EventBase const & event, std::strbitset & ret){

    // Select the PV
    std::strbitset retPV = pvSelector_->getBitTemplate();
    retPV.set(false);
    bool passPV = (*pvSelector_)( event, retPV );
    edm::Handle<vector<reco::Vertex> > const & vertices = pvSelector_->vertices();

    std::strbitset retCaloJet = jetSel_->getBitTemplate();
    std::strbitset retPFJet = pfJetSel_->getBitTemplate();


    if ( passPV || ignoreCut("PV") ) {
      passCut(ret, "PV");

      if ( considerCut("Calo Cuts") ) {
	passCut(ret, "Calo Cuts");
	event.getByLabel( jetSrc_, h_jets_ );
	// Calo Cuts
	if ( h_jets_->size() >= 2 || ignoreCut("Calo Kin Cuts") ) {
	  passCut(ret, "Calo Kin Cuts");
	  pat::Jet const & jet0 = h_jets_->at(0);
	  pat::Jet const & jet1 = h_jets_->at(1);
	  double dphi = fabs(deltaPhi<double>( jet0.phi(),
					       jet1.phi() ) );
	  
	  if ( fabs(dphi - TMath::Pi()) < 1.0 || ignoreCut("Calo Delta Phi") ) {
	    passCut(ret, "Calo Delta Phi");

	    
	    retCaloJet.set(false);
	    bool pass0 = (*jetSel_)( jet0, retCaloJet );
	    retCaloJet.set(false);
	    bool pass1 = (*jetSel_)( jet1, retCaloJet );
	    if ( (pass0 && pass1) || ignoreCut("Calo Jet ID") ) {
	      passCut(ret, "Calo Jet ID");
	      caloJet0_ = edm::Ptr<pat::Jet>( h_jets_, 0);
	      caloJet1_ = edm::Ptr<pat::Jet>( h_jets_, 1);

	      return (bool)ret;
	    }// end if found 2 "loose" jet ID jets
	  }// end if delta phi
	}// end calo kin cuts
      }// end if calo cuts


      if ( considerCut("PF Cuts") ) {
	passCut(ret, "PF Cuts");
	event.getByLabel( pfJetSrc_, h_pfjets_ );
	// PF Cuts
	if ( h_pfjets_->size() >= 2 || ignoreCut("PF Kin Cuts") ) {
	  passCut( ret, "PF Kin Cuts");
	  pat::Jet const & jet0 = h_pfjets_->at(0);
	  pat::Jet const & jet1 = h_pfjets_->at(1);
	  double dphi = fabs(deltaPhi<double>( jet0.phi(),
					       jet1.phi() ) );
	  
	  if ( fabs(dphi - TMath::Pi()) < 1.0 || ignoreCut("PF Delta Phi") ) {
	    passCut(ret, "PF Delta Phi");

	    
	    retPFJet.set(false);
	    bool pass0 = (*pfJetSel_)( jet0, retPFJet );
	    retPFJet.set(false);
	    bool pass1 = (*pfJetSel_)( jet1, retPFJet );
	    if ( (pass0 && pass1) || ignoreCut("PF Jet ID") ) {
	      passCut(ret, "PF Jet ID");
	      pfJet0_ = edm::Ptr<pat::Jet>( h_pfjets_, 0);
	      pfJet1_ = edm::Ptr<pat::Jet>( h_pfjets_, 1);

	      return (bool)ret;
	    }// end if found 2 "loose" jet ID jets
	  }// end if delta phi
	}// end pf kin cuts
      }// end if pf cuts
    }// end if good PV

    setIgnored(ret);

    return false;
  }// end of method


  boost::shared_ptr<PVSelector> const &              pvSelector() const { return pvSelector_;}
  boost::shared_ptr<JetIDSelectionFunctor> const &   jetSel()     const { return jetSel_;}
  boost::shared_ptr<PFJetIDSelectionFunctor> const & pfJetSel()   const { return pfJetSel_;}

  vector<pat::Jet>            const &   allCaloJets () const { return *h_jets_; }
  vector<pat::Jet>            const &   allPFJets   () const { return *h_pfjets_; }

  pat::Jet                    const &   caloJet0() const { return *caloJet0_; }
  pat::Jet                    const &   caloJet1() const { return *caloJet1_; }

  pat::Jet                    const &   pfJet0() const { return *pfJet0_; }
  pat::Jet                    const &   pfJet1() const { return *pfJet1_; }


protected:
  boost::shared_ptr<PVSelector>              pvSelector_;
  boost::shared_ptr<JetIDSelectionFunctor>   jetSel_;
  boost::shared_ptr<PFJetIDSelectionFunctor> pfJetSel_;
  edm::InputTag                              jetSrc_;
  edm::InputTag                              pfJetSrc_;
  
  edm::Handle<vector<pat::Jet> >             h_jets_;
  edm::Handle<vector<pat::Jet> >             h_pfjets_;

  edm::Ptr<pat::Jet>                         caloJet0_;
  edm::Ptr<pat::Jet>                         caloJet1_;

  edm::Ptr<pat::Jet>                         pfJet0_;
  edm::Ptr<pat::Jet>                         pfJet1_;

};

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
   eventCont.add( new TH1D("hist_primVtxZ", "Primary Vertex z", 100, -20, 20 ) );

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
   boost::shared_ptr<PVSelector>
     pvSelector ( new PVSelector ( edm::InputTag("offlinePrimaryVertices"), 5., 15. ) );

   boost::shared_ptr<JetIDSelectionFunctor>
     jetSelector( new JetIDSelectionFunctor( JetIDSelectionFunctor::CRAFT08, 
					     JetIDSelectionFunctor::LOOSE )
		  );
   
   boost::shared_ptr<PFJetIDSelectionFunctor> 
     pfJetSelector( new PFJetIDSelectionFunctor( PFJetIDSelectionFunctor::FIRSTDATA, 
						 PFJetIDSelectionFunctor::LOOSE,
						 0.0,
						 0.9,
						 0.9 )
		    );

   
   JetIDStudiesSelector caloSelector( pvSelector,
				      jetSelector,
				      pfJetSelector,
				      parser.stringValue("jetSrc"),
				      parser.stringValue("pfJetSrc"),
				      true
				      );

   JetIDStudiesSelector pfSelector( pvSelector,
				    jetSelector,
				    pfJetSelector,
				    parser.stringValue("jetSrc"),
				    parser.stringValue("pfJetSrc"),
				    false
				    );

  int nev = 0;
  //loop through each event
  for (eventCont.toBegin(); ! eventCont.atEnd(); ++eventCont) {


    edm::EventBase const & event = eventCont;

    std::strbitset retCalo = caloSelector.getBitTemplate();
    bool passedCalo = caloSelector( event, retCalo );

    std::strbitset retPF = pfSelector.getBitTemplate();
    bool passedPF = pfSelector( event, retPF );


    if ( retCalo.test("PV") == false ) continue;

    edm::Handle<vector<reco::Vertex> > const & vertices = caloSelector.pvSelector()->vertices();

    // Plot some PV info
    eventCont.hist("hist_primVtxNTracks")->Fill( vertices->at(0).tracksSize() );
    eventCont.hist("hist_primVtxNDof")->Fill( vertices->at(0).ndof() );
    eventCont.hist("hist_primVtxChi2")->Fill( vertices->at(0).normalizedChi2() );
    eventCont.hist("hist_primVtxZ")->Fill( vertices->at(0).z() );



    ///------------------
    /// CALO JETS
    ///------------------
    if ( retCalo.test("Calo Kin Cuts") ) {
      if ( retCalo.test("Calo Delta Phi") ) {
	vector<pat::Jet>  const & allCaloJets = caloSelector.allCaloJets();
	char buff[1000];
	sprintf(buff, "Run %12d, Lumi %6d, Event %12d  : Pt0 = %6.2f, Eta0 = %6.2f, Pt1 = %6.2f, Eta1 = %6.2f",
		eventCont.id().run(),
		eventCont.id().luminosityBlock(),
		eventCont.id().event(),
		allCaloJets[0].pt(),
		allCaloJets[0].eta(),
		allCaloJets[1].pt(),
		allCaloJets[1].eta()
		);
	cout << buff << endl;


	for ( std::vector<pat::Jet>::const_iterator jetBegin = allCaloJets.begin(),
		jetEnd = jetBegin + 2, ijet = jetBegin;
	      ijet != jetEnd; ++ijet ) {
	
	  const pat::Jet & jet = *ijet;

	  double pt = jet.pt();

	  const reco::TrackRefVector & jetTracks = jet.associatedTracks();
      

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

      
	} // end loop over jets

    

	if ( retCalo.test("Calo Jet ID") ) {
	  pat::Jet const & jet0 = caloSelector.caloJet0();
	  pat::Jet const & jet1 = caloSelector.caloJet1();

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

	}// end if passed calo jet id
      }// end if passed dphi cuts
    }// end if passed kin cuts


    ///------------------
    /// PF JETS
    ///------------------
    if ( retPF.test("PF Delta Phi") ) {

      vector<pat::Jet> const & allPFJets = pfSelector.allPFJets();

      for ( std::vector<pat::Jet>::const_iterator jetBegin = allPFJets.begin(),
	      jetEnd = jetBegin + 2, ijet = jetBegin;
	    ijet != jetEnd; ++ijet ) {
	
	const pat::Jet & jet = *ijet;
	
	double pt = jet.pt();
      
	eventCont.hist("hist_pf_good_jetPt")->Fill( pt );
	eventCont.hist("hist_pf_good_jetEtaVsPhi")->Fill( jet.eta(), jet.phi() );
	eventCont.hist("hist_pf_good_nConstituents")->Fill( jet.nConstituents() );
	eventCont.hist("hist_pf_good_jetCEF")->Fill( jet.chargedEmEnergyFraction()  );
	eventCont.hist("hist_pf_good_jetNEF")->Fill( jet.neutralEmEnergyFraction()  );
	eventCont.hist("hist_pf_good_jetCHF")->Fill( jet.chargedHadronEnergyFraction()  );
	eventCont.hist("hist_pf_good_jetNHF")->Fill( jet.neutralHadronEnergyFraction()  );


	if ( parser.boolValue("doGen") && jet.genJet() != 0 ) {
	  eventCont.hist("hist_pf_good_jetGenEmE")->Fill( jet.genJet()->emEnergy() );
	  eventCont.hist("hist_pf_good_jetGenHadE")->Fill( jet.genJet()->hadEnergy() );
	  eventCont.hist("hist_pf_good_jetEoverGenE")->Fill( jet.energy() / jet.genJet()->energy() );

	  eventCont.hist("hist_pf_good_jetGenEMF")->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	}
 
      } // end loop over jets

    

      if ( retPF.test("PF Jet ID") ) {
	pat::Jet const & jet0 = pfSelector.pfJet0();
	pat::Jet const & jet1 = pfSelector.pfJet1();

	TLorentzVector p4_j0( jet0.px(), jet0.py(), jet0.pz(), jet0.energy() );
	TLorentzVector p4_j1( jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );

	TLorentzVector p4_jj = p4_j0 + p4_j1;

	eventCont.hist("hist_pf_mjj")->Fill( p4_jj.M() );
	eventCont.hist("hist_pf_dR_jj")->Fill( p4_j0.DeltaR( p4_j1 ) );
	eventCont.hist("hist_pf_imbalance_jj")->Fill( (p4_j0.Perp() - p4_j1.Perp() ) /
						      (p4_j0.Perp() + p4_j1.Perp() ) );

	eventCont.hist("hist_pf_good_dijets_jetPt")->Fill( jet0.pt() );
	eventCont.hist("hist_pf_good_dijets_jetEtaVsPhi")->Fill( jet0.eta(), jet0.phi() );
	eventCont.hist("hist_pf_good_dijets_nConstituents")->Fill( jet0.nConstituents() );
	eventCont.hist("hist_pf_good_dijets_jetCEF")->Fill( jet0.chargedEmEnergyFraction()  );
	eventCont.hist("hist_pf_good_dijets_jetNEF")->Fill( jet0.neutralEmEnergyFraction()  );
	eventCont.hist("hist_pf_good_dijets_jetCHF")->Fill( jet0.chargedHadronEnergyFraction()  );
	eventCont.hist("hist_pf_good_dijets_jetNHF")->Fill( jet0.neutralHadronEnergyFraction()  );


	eventCont.hist("hist_pf_good_dijets_jetPt")->Fill( jet1.pt() );
	eventCont.hist("hist_pf_good_dijets_jetEtaVsPhi")->Fill( jet1.eta(), jet1.phi() );
	eventCont.hist("hist_pf_good_dijets_nConstituents")->Fill( jet1.nConstituents() );
	eventCont.hist("hist_pf_good_dijets_jetCEF")->Fill( jet1.chargedEmEnergyFraction()  );
	eventCont.hist("hist_pf_good_dijets_jetNEF")->Fill( jet1.neutralEmEnergyFraction()  );
	eventCont.hist("hist_pf_good_dijets_jetCHF")->Fill( jet1.chargedHadronEnergyFraction()  );
	eventCont.hist("hist_pf_good_dijets_jetNHF")->Fill( jet1.neutralHadronEnergyFraction()  );

      
      
   
      
      } // end if 2 good PF jets
    
    }// end if delta phi pf cuts
    
  } // end loop over events
    
  cout << "Calo jet selection" << endl;
  caloSelector.print(std::cout);
  cout << "PF jet selection" << endl;
  pfSelector.print(std::cout);

      
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

