/*   A macro for making a histogram of Jet Pt with cuts
This is a basic way to cut out jets of a certain Pt and Eta using an if statement
This example creates a histogram of Jet Pt, using Jets with Pt above 30 and ETA above -2.1 and below 2.1
*/

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"
#include "TLorentzVector.h"

#include "PhysicsTools/SelectorUtils/interface/strbitset.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/PVSelector.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/ChainEvent.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"


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
#include "PhysicsTools/SelectorUtils/interface/EventSelector.h"

#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 

// Root includes
#include "TROOT.h"

using namespace std;


class JetIDStudiesSelector : public EventSelector {
public:
  JetIDStudiesSelector( edm::ParameterSet const & pvParams,
			edm::ParameterSet const & caloJetIdParams,
			edm::ParameterSet const & pfJetIdParams,
			edm::ParameterSet const & params ) :
    pvSelector_(new PVSelector(pvParams)), 
    jetSel_    (new JetIDSelectionFunctor(caloJetIdParams)), 
    pfJetSel_  (new PFJetIDSelectionFunctor(pfJetIdParams)),
    jetSrc_    (params.getParameter<edm::InputTag>("jetSrc")), 
    pfJetSrc_  (params.getParameter<edm::InputTag>("pfJetSrc")) 
  {
    bool useCalo = params.getParameter<bool>("useCalo");
	       
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

    if ( params.exists("doPV") && ! params.getParameter<bool>("doPV") ) 
      set("PV", false);
    
  }

  virtual ~JetIDStudiesSelector() {}

  virtual bool operator()( edm::EventBase const & event, std::strbitset & ret){

    // Select the PV
    std::strbitset retPV = pvSelector_->getBitTemplate();
    retPV.set(false);
    bool passPV = false;
    if ( ignoreCut("PV") ) passPV = true;
    else passPV = (*pvSelector_)( event, retPV );
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
  PythonProcessDesc builder(argv[1]);
  edm::ParameterSet const& jetStudiesParams = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("jetStudies");
  edm::ParameterSet const& pfJetStudiesParams = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("pfJetStudies");
  edm::ParameterSet const& caloJetIDParameters = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("jetIDSelector");
  edm::ParameterSet const& pfJetIDParameters = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("pfJetIDSelector");
  edm::ParameterSet const& pvSelector = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("pvSelector");
  edm::ParameterSet const& plotParameters = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("plotParameters");
  edm::ParameterSet const& inputs = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("inputs");
  edm::ParameterSet const& outputs = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("outputs");
  
  cout << "setting up TFileService" << endl;
  // book a set of histograms
  fwlite::TFileService fs = fwlite::TFileService( outputs.getParameter<std::string>("outputName") );
  TFileDirectory theDir = fs.mkdir( "histos" ); 
    
  cout << "Setting up chain event" << endl;
  // This object 'event' is used both to get all information from the
  // event as well as to store histograms, etc.
  fwlite::ChainEvent ev ( inputs.getParameter<std::vector<std::string> > ("fileNames") );


  cout << "Booking histograms" << endl;
   // Book histograms

  std::map<std::string, TH1*> hists;

   hists["hist_nJet"                     ] = theDir.make<TH1D>( "hist_nJet"                    ,"Number of Calo Jets", 10, 0, 10 ) ;
   hists["hist_nPFJet"                   ] = theDir.make<TH1D>( "hist_nPFJet"                  ,"Number of PF Jets", 10, 0, 10 ) ;

   hists["hist_jetPt"                    ] = theDir.make<TH1D>( "hist_jetPt"                   , "Jet p_{T}", 400, 0, 400 ) ;
   hists["hist_jetEtaVsPhi"              ] = theDir.make<TH2D>( "hist_jetEtaVsPhi"             , "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) ;
   hists["hist_jetNTracks"               ] = theDir.make<TH1D>( "hist_jetNTracks"              , "Jet N_{TRACKS}", 20, 0, 20 ) ;
   hists["hist_jetNTracksVsPt"           ] = theDir.make<TH2D>( "hist_jetNTracksVsPt"          , "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) ;N_{Tracks}",20, 0, 200, 20, 0, 20 ) ;
   hists["hist_jetEMF"                   ] = theDir.make<TH1D>( "hist_jetEMF"                  , "Jet EMF", 200, 0, 1) ;
   hists["hist_jetPdgID"                 ] = theDir.make<TH1D>( "hist_jetPdgID"                , "PDG Id of Jet Constituents", 10000, 0, 10000 ) ;
   hists["hist_jetGenEmE"                ] = theDir.make<TH1D>( "hist_jetGenEmE"               , "Gen Jet EM Energy", 200, 0, 200 ) ;
   hists["hist_jetGenHadE"               ] = theDir.make<TH1D>( "hist_jetGenHadE"              , "Gen Jet HAD Energy", 200, 0, 200 ) ;
   hists["hist_jetGenEMF"                ] = theDir.make<TH1D>( "hist_jetGenEMF"               , "Gen Jet EMF", 200, 0, 1) ;
   hists["hist_jetEoverGenE"             ] = theDir.make<TH1D>( "hist_jetEoverGenE"            , "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) ;
   hists["hist_jetCorr"                  ] = theDir.make<TH1D>( "hist_jetCorr"                 , "Jet Correction Factor", 200, 0, 1.0 ) ;
   hists["hist_n90Hits"                  ] = theDir.make<TH1D>( "hist_n90Hits"                 , "Jet n90Hits", 20, 0, 20) ;
   hists["hist_fHPD"                     ] = theDir.make<TH1D>( "hist_fHPD"                    , "Jet fHPD", 200, 0, 1) ;
   hists["hist_nConstituents"            ] = theDir.make<TH1D>( "hist_nConstituents"           , "Jet nConstituents", 20, 0, 20 ) ;
   hists["hist_jetCHF"                   ] = theDir.make<TH1D>( "hist_jetCHF"                  , "Jet Charged Hadron Fraction", 200, 0, 1.0) ;
	                                      
   hists["hist_dijets_jetPt"             ] = theDir.make<TH1D>( "hist_dijets_jetPt"            , "Jet p_{T}", 400, 0, 400 ) ;
   hists["hist_dijets_jetEtaVsPhi"       ] = theDir.make<TH2D>( "hist_dijets_jetEtaVsPhi"      , "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) ;
   hists["hist_dijets_jetNTracks"        ] = theDir.make<TH1D>( "hist_dijets_jetNTracks"       , "Jet N_{TRACKS}", 20, 0, 20 ) ;
   hists["hist_dijets_jetNTracksVsPt"    ] = theDir.make<TH2D>( "hist_dijets_jetNTracksVsPt"   , "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) ;N_{Tracks}",20, 0, 200, 20, 0, 20 ) ;
   hists["hist_dijets_jetEMF"            ] = theDir.make<TH1D>( "hist_dijets_jetEMF"           , "Jet EMF", 200, 0, 1) ;
   hists["hist_dijets_jetPdgID"          ] = theDir.make<TH1D>( "hist_dijets_jetPdgID"         , "PDG Id of Jet Constituents", 10000, 0, 10000 ) ;
   hists["hist_dijets_jetGenEmE"         ] = theDir.make<TH1D>( "hist_dijets_jetGenEmE"        , "Gen Jet EM Energy", 200, 0, 200 ) ;
   hists["hist_dijets_jetGenHadE"        ] = theDir.make<TH1D>( "hist_dijets_jetGenHadE"       , "Gen Jet HAD Energy", 200, 0, 200 ) ;
   hists["hist_dijets_jetGenEMF"         ] = theDir.make<TH1D>( "hist_dijets_jetGenEMF"        , "Gen Jet EMF", 200, 0, 1) ;
   hists["hist_dijets_jetEoverGenE"      ] = theDir.make<TH1D>( "hist_dijets_jetEoverGenE"     , "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) ;
   hists["hist_dijets_jetCorr"           ] = theDir.make<TH1D>( "hist_dijets_jetCorr"          , "Jet Correction Factor", 200, 0, 1.0 ) ;
   hists["hist_dijets_n90Hits"           ] = theDir.make<TH1D>( "hist_dijets_n90Hits"          , "Jet n90Hits", 20, 0, 20) ;
   hists["hist_dijets_fHPD"              ] = theDir.make<TH1D>( "hist_dijets_fHPD"             , "Jet fHPD", 200, 0, 1) ;
   hists["hist_dijets_nConstituents"     ] = theDir.make<TH1D>( "hist_dijets_nConstituents"    , "Jet nConstituents", 20, 0, 20 ) ;
   hists["hist_dijets_jetCHF"            ] = theDir.make<TH1D>( "hist_dijets_jetCHF"           , "Jet Charged Hadron Fraction", 200, 0, 1.0) ;
   	                                                  
	                                      
   hists["hist_pf_jetPt"                 ] = theDir.make<TH1D>( "hist_pf_jetPt"                , "PFJet p_{T}", 400, 0, 400 ) ;
   hists["hist_pf_jetEtaVsPhi"           ] = theDir.make<TH2D>( "hist_pf_jetEtaVsPhi"          , "PFJet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) ;
   hists["hist_pf_jetNTracks"            ] = theDir.make<TH1D>( "hist_pf_jetNTracks"           , "PFJet N_{TRACKS}", 20, 0, 20 ) ;
   hists["hist_pf_jetNTracksVsPt"        ] = theDir.make<TH2D>( "hist_pf_jetNTracksVsPt"       , "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) ;N_{Tracks}",20, 0, 200, 20, 0, 20 ) ;
   hists["hist_pf_jetEMF"                ] = theDir.make<TH1D>( "hist_pf_jetEMF"               , "PFJet EMF", 200, 0, 1) ;
   hists["hist_pf_jetCHF"                ] = theDir.make<TH1D>( "hist_pf_jetCHF"               , "PFJet CHF", 200, 0, 1) ;
   hists["hist_pf_jetNHF"                ] = theDir.make<TH1D>( "hist_pf_jetNHF"               , "PFJet NHF", 200, 0, 1) ;
   hists["hist_pf_jetCEF"                ] = theDir.make<TH1D>( "hist_pf_jetCEF"               , "PFJet CEF", 200, 0, 1) ;
   hists["hist_pf_jetNEF"                ] = theDir.make<TH1D>( "hist_pf_jetNEF"               , "PFJet NEF", 200, 0, 1) ;
   hists["hist_pf_jetPdgID"              ] = theDir.make<TH1D>( "hist_pf_jetPdgID"             , "PDG Id of Jet Constituents", 10000, 0, 10000 ) ;
   hists["hist_pf_jetGenEmE"             ] = theDir.make<TH1D>( "hist_pf_jetGenEmE"            , "Gen Jet EM Energy", 200, 0, 200 ) ;
   hists["hist_pf_jetGenHadE"            ] = theDir.make<TH1D>( "hist_pf_jetGenHadE"           , "Gen Jet HAD Energy", 200, 0, 200 ) ;
   hists["hist_pf_jetGenEMF"             ] = theDir.make<TH1D>( "hist_pf_jetGenEMF"            , "Gen Jet EMF", 200, 0, 1) ;
   hists["hist_pf_jetEoverGenE"          ] = theDir.make<TH1D>( "hist_pf_jetEoverGenE"         , "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) ;
   hists["hist_pf_jetCorr"               ] = theDir.make<TH1D>( "hist_pf_jetCorr"              , "PFJet Correction Factor", 200, 0, 1.0 ) ;
   hists["hist_pf_nConstituents"         ] = theDir.make<TH1D>( "hist_pf_nConstituents"        , "PFJet nConstituents", 20, 0, 20 ) ;
	                                      
   hists["hist_pf_dijets_jetPt"          ] = theDir.make<TH1D>( "hist_pf_dijets_jetPt"         , "PFJet p_{T}", 400, 0, 400 ) ;
   hists["hist_pf_dijets_jetEtaVsPhi"    ] = theDir.make<TH2D>( "hist_pf_dijets_jetEtaVsPhi"   , "PFJet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() ) ;
   hists["hist_pf_dijets_jetNTracks"     ] = theDir.make<TH1D>( "hist_pf_dijets_jetNTracks"    , "PFJet N_{TRACKS}", 20, 0, 20 ) ;
   hists["hist_pf_dijets_jetNTracksVsPt" ] = theDir.make<TH2D>( "hist_pf_dijets_jetNTracksVsPt", "Number of Tracks versus Jet p_{T};Jet p_{T}(GeV/c) ;N_{Tracks}",20, 0, 200, 20, 0, 20 ) ;
   hists["hist_pf_dijets_jetEMF"         ] = theDir.make<TH1D>( "hist_pf_dijets_jetEMF"        , "PFJet EMF", 200, 0, 1) ;
   hists["hist_pf_dijets_jetCHF"         ] = theDir.make<TH1D>( "hist_pf_dijets_jetCHF"        , "PFJet CHF", 200, 0, 1) ;
   hists["hist_pf_dijets_jetNHF"         ] = theDir.make<TH1D>( "hist_pf_dijets_jetNHF"        , "PFJet NHF", 200, 0, 1) ;
   hists["hist_pf_dijets_jetCEF"         ] = theDir.make<TH1D>( "hist_pf_dijets_jetCEF"        , "PFJet CEF", 200, 0, 1) ;
   hists["hist_pf_dijets_jetNEF"         ] = theDir.make<TH1D>( "hist_pf_dijets_jetNEF"        , "PFJet NEF", 200, 0, 1) ;
   hists["hist_pf_dijets_jetPdgID"       ] = theDir.make<TH1D>( "hist_pf_dijets_jetPdgID"      , "PDG Id of Jet Constituents", 10000, 0, 10000 ) ;
   hists["hist_pf_dijets_jetGenEmE"      ] = theDir.make<TH1D>( "hist_pf_dijets_jetGenEmE"     , "Gen Jet EM Energy", 200, 0, 200 ) ;
   hists["hist_pf_dijets_jetGenHadE"     ] = theDir.make<TH1D>( "hist_pf_dijets_jetGenHadE"    , "Gen Jet HAD Energy", 200, 0, 200 ) ;
   hists["hist_pf_dijets_jetGenEMF"      ] = theDir.make<TH1D>( "hist_pf_dijets_jetGenEMF"     , "Gen Jet EMF", 200, 0, 1) ;
   hists["hist_pf_dijets_jetEoverGenE"   ] = theDir.make<TH1D>( "hist_pf_dijets_jetEoverGenE"  , "Energy of reco Jet / Energy of gen Jet", 200, 0, 2.0) ;
   hists["hist_pf_dijets_jetCorr"        ] = theDir.make<TH1D>( "hist_pf_dijets_jetCorr"       , "PFJet Correction Factor", 200, 0, 1.0 ) ;
   hists["hist_pf_dijets_nConstituents"  ] = theDir.make<TH1D>( "hist_pf_dijets_nConstituents" , "PFJet nConstituents", 20, 0, 20 ) ;
	                                      
   hists["hist_nGeneralTracks"                ] = theDir.make<TH1D>( "hist_nGeneralTracks"               , "Number of General Tracks", 100, 0, 100) ;
   hists["hist_primVtxNTracks"                ] = theDir.make<TH1D>( "hist_primVtxNTracks"               , "Number of Tracks in Primary Vertex", 100, 0, 100) ;
   hists["hist_primVtxNDof"                   ] = theDir.make<TH1D>( "hist_primVtxNDof"                  , "Number of Degrees of Freedom in Primary Vertex", 100, 0, 100) ;
   hists["hist_primVtxChi2"                   ] = theDir.make<TH1D>( "hist_primVtxChi2"                  , "Primary Vertex #chi^{2}", 100, 0, 20 ) ;
   hists["hist_primVtxZ"                      ] = theDir.make<TH1D>( "hist_primVtxZ"                     , "Primary Vertex z", 100, -20, 20 ) ;
	                                      
   hists["hist_mjj"                           ] = theDir.make<TH1D>( "hist_mjj"                          , "Dijet mass", 300, 0, 300 ) ;
   hists["hist_dR_jj"                         ] = theDir.make<TH1D>( "hist_dR_jj"                        , "#Delta R_{JJ}", 200, 0, TMath::TwoPi() ) ;
   hists["hist_imbalance_jj"                  ] = theDir.make<TH1D>( "hist_imbalance_jj"                 , "Dijet imbalance", 200, -1.0, 1.0 )  ;
	                                      
   hists["hist_pf_mjj"                        ] = theDir.make<TH1D>( "hist_pf_mjj"                       , "Dijet mass", 300, 0, 300 ) ;
   hists["hist_pf_dR_jj"                      ] = theDir.make<TH1D>( "hist_pf_dR_jj"                     , "#Delta R_{JJ}", 200, 0, TMath::TwoPi() ) ;
   hists["hist_pf_imbalance_jj"               ] = theDir.make<TH1D>( "hist_pf_imbalance_jj"              , "Dijet imbalance", 200, -1.0, 1.0 )  ;


   
   cout << "Making functors" << endl;
   JetIDStudiesSelector caloSelector( pvSelector,
				      caloJetIDParameters,
				      pfJetIDParameters,
				      jetStudiesParams );

   JetIDStudiesSelector pfSelector( pvSelector,
				    caloJetIDParameters,
				    pfJetIDParameters,
				    pfJetStudiesParams );

   vector<int> const & runs = plotParameters.getParameter<std::vector<int> >("runs");
   bool doTracks = plotParameters.getParameter<bool>("doTracks");
   bool doGen    = plotParameters.getParameter<bool>("doGen");

   cout << "About to begin looping" << endl;

  int nev = 0;
  //loop through each event
  for (ev.toBegin(); ! ev.atEnd(); ++ev, ++nev) {


    edm::EventBase const & event = ev;

    int run = event.id().run();
    if ( runs.size() > 0 && find( runs.begin(), runs.end(), run ) == runs.end() ) continue;

    if ( nev % 10000 == 0 ) cout << "Processing run " << event.id().run() << ", event " << event.id().event() << endl;

    std::strbitset retCalo = caloSelector.getBitTemplate();
    bool passedCalo = caloSelector( event, retCalo );

    std::strbitset retPF = pfSelector.getBitTemplate();
    bool passedPF = pfSelector( event, retPF );

    if ( retCalo.test("PV") == false ) continue;

    edm::Handle<vector<reco::Vertex> > const & vertices = caloSelector.pvSelector()->vertices();

    // Plot some PV info
    if ( doTracks ) {
      hists["hist_primVtxNTracks"]->Fill( vertices->at(0).tracksSize() );
      hists["hist_primVtxNDof"]->Fill( vertices->at(0).ndof() );
      hists["hist_primVtxChi2"]->Fill( vertices->at(0).normalizedChi2() );
      hists["hist_primVtxZ"]->Fill( vertices->at(0).z() );
    }


    ///------------------
    /// CALO JETS
    ///------------------
    if ( retCalo.test("Calo Kin Cuts") ) {
      if ( retCalo.test("Calo Delta Phi") ) {
	vector<pat::Jet>  const & allCaloJets = caloSelector.allCaloJets();
// 	char buff[1000];
// 	sprintf(buff, "Run %12d, Lumi %6d, Event %12d  : Pt0 = %6.2f, Eta0 = %6.2f, Pt1 = %6.2f, Eta1 = %6.2f",
// 		eventCont.id().run(),
// 		eventCont.id().luminosityBlock(),
// 		eventCont.id().event(),
// 		allCaloJets[0].pt(),
// 		allCaloJets[0].eta(),
// 		allCaloJets[1].pt(),
// 		allCaloJets[1].eta()
// 		);
// 	cout << buff << endl;


	for ( std::vector<pat::Jet>::const_iterator jetBegin = allCaloJets.begin(),
		jetEnd = jetBegin + 2, ijet = jetBegin;
	      ijet != jetEnd; ++ijet ) {
	
	  const pat::Jet & jet = *ijet;

	  double pt = jet.pt();

	  const reco::TrackRefVector & jetTracks = jet.associatedTracks();

	  hists["hist_jetPt"]->Fill( pt );
	  hists["hist_jetEtaVsPhi"]->Fill( jet.eta(), jet.phi() );
	  hists["hist_jetNTracks"]->Fill( jetTracks.size() );
	  hists["hist_jetNTracksVsPt"]->Fill( pt, jetTracks.size() );
	  hists["hist_jetEMF"]->Fill( jet.emEnergyFraction() );	
	  hists["hist_jetCorr"]->Fill( jet.corrFactor("raw") );
	  hists["hist_n90Hits"]->Fill( static_cast<int>(jet.jetID().n90Hits) );
	  hists["hist_fHPD"]->Fill( jet.jetID().fHPD );
	  hists["hist_nConstituents"]->Fill( jet.nConstituents() );

	  if ( doGen && jet.genJet() != 0 ) {
	    hists["hist_jetGenEmE"]->Fill( jet.genJet()->emEnergy() );
	    hists["hist_jetGenHadE"]->Fill( jet.genJet()->hadEnergy() );
	    hists["hist_jetEoverGenE"]->Fill( jet.energy() / jet.genJet()->energy() );
	    hists["hist_jetGenEMF"]->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	  }
	  if ( doTracks ) {
	    TLorentzVector p4_tracks(0,0,0,0);
	    for ( reco::TrackRefVector::const_iterator itrk = jetTracks.begin(),
		    itrkBegin = jetTracks.begin(), itrkEnd = jetTracks.end();
		  itrk != itrkEnd; ++itrk ) {
	      TLorentzVector p4_trk;
	      double M_PION = 0.140;
	      p4_trk.SetPtEtaPhiM( (*itrk)->pt(), (*itrk)->eta(), (*itrk)->phi(), M_PION );
	      p4_tracks += p4_trk;
	    }
	    hists["hist_jetCHF"]->Fill( p4_tracks.Energy() / jet.energy() );
	  }

      
	} // end loop over jets

    

	if ( retCalo.test("Calo Jet ID") ) {
	  pat::Jet const & jet0 = caloSelector.caloJet0();
	  pat::Jet const & jet1 = caloSelector.caloJet1();

	  TLorentzVector p4_j0( jet0.px(), jet0.py(), jet0.pz(), jet0.energy() );
	  TLorentzVector p4_j1( jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );

	  TLorentzVector p4_jj = p4_j0 + p4_j1;

	  hists["hist_mjj"]->Fill( p4_jj.M() );
	  hists["hist_dR_jj"]->Fill( p4_j0.DeltaR( p4_j1 ) );
	  hists["hist_imbalance_jj"]->Fill( (p4_j0.Perp() - p4_j1.Perp() ) /
						     (p4_j0.Perp() + p4_j1.Perp() ) );

	  hists["hist_dijets_jetPt"]->Fill( jet0.pt() );
	  hists["hist_dijets_jetEtaVsPhi"]->Fill( jet0.eta(), jet0.phi() );
	  hists["hist_dijets_jetNTracks"]->Fill( jet0.associatedTracks().size() );
	  hists["hist_dijets_jetNTracksVsPt"]->Fill( jet0.pt(), jet0.associatedTracks().size() );
	  hists["hist_dijets_jetEMF"]->Fill( jet0.emEnergyFraction() );	
	  hists["hist_dijets_jetCorr"]->Fill( jet0.corrFactor("raw") );
	  hists["hist_dijets_n90Hits"]->Fill( static_cast<int>(jet0.jetID().n90Hits) );
	  hists["hist_dijets_fHPD"]->Fill( jet0.jetID().fHPD );
	  hists["hist_dijets_nConstituents"]->Fill( jet0.nConstituents() );


	  hists["hist_dijets_jetPt"]->Fill( jet1.pt() );
	  hists["hist_dijets_jetEtaVsPhi"]->Fill( jet1.eta(), jet1.phi() );
	  hists["hist_dijets_jetNTracks"]->Fill( jet1.associatedTracks().size() );
	  hists["hist_dijets_jetNTracksVsPt"]->Fill( jet1.pt(), jet1.associatedTracks().size() );
	  hists["hist_dijets_jetEMF"]->Fill( jet1.emEnergyFraction() );	
	  hists["hist_dijets_jetCorr"]->Fill( jet1.corrFactor("raw") );
	  hists["hist_dijets_n90Hits"]->Fill( static_cast<int>(jet1.jetID().n90Hits) );
	  hists["hist_dijets_fHPD"]->Fill( jet1.jetID().fHPD );
	  hists["hist_dijets_nConstituents"]->Fill( jet1.nConstituents() );

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
      
	hists["hist_pf_jetPt"]->Fill( pt );
	hists["hist_pf_jetEtaVsPhi"]->Fill( jet.eta(), jet.phi() );
	hists["hist_pf_nConstituents"]->Fill( jet.nConstituents() );
	hists["hist_pf_jetCEF"]->Fill( jet.chargedEmEnergyFraction()  );
	hists["hist_pf_jetNEF"]->Fill( jet.neutralEmEnergyFraction()  );
	hists["hist_pf_jetCHF"]->Fill( jet.chargedHadronEnergyFraction()  );
	hists["hist_pf_jetNHF"]->Fill( jet.neutralHadronEnergyFraction()  );


	if ( doGen && jet.genJet() != 0 ) {
	  hists["hist_pf_jetGenEmE"]->Fill( jet.genJet()->emEnergy() );
	  hists["hist_pf_jetGenHadE"]->Fill( jet.genJet()->hadEnergy() );
	  hists["hist_pf_jetEoverGenE"]->Fill( jet.energy() / jet.genJet()->energy() );

	  hists["hist_pf_jetGenEMF"]->Fill( jet.genJet()->emEnergy() / jet.genJet()->energy() );
	}
 
      } // end loop over jets

    

      if ( retPF.test("PF Jet ID") ) {
	pat::Jet const & jet0 = pfSelector.pfJet0();
	pat::Jet const & jet1 = pfSelector.pfJet1();

	TLorentzVector p4_j0( jet0.px(), jet0.py(), jet0.pz(), jet0.energy() );
	TLorentzVector p4_j1( jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );

	TLorentzVector p4_jj = p4_j0 + p4_j1;

	hists["hist_pf_mjj"]->Fill( p4_jj.M() );
	hists["hist_pf_dR_jj"]->Fill( p4_j0.DeltaR( p4_j1 ) );
	hists["hist_pf_imbalance_jj"]->Fill( (p4_j0.Perp() - p4_j1.Perp() ) /
						      (p4_j0.Perp() + p4_j1.Perp() ) );

	hists["hist_pf_dijets_jetPt"]->Fill( jet0.pt() );
	hists["hist_pf_dijets_jetEtaVsPhi"]->Fill( jet0.eta(), jet0.phi() );
	hists["hist_pf_dijets_nConstituents"]->Fill( jet0.nConstituents() );
	hists["hist_pf_dijets_jetCEF"]->Fill( jet0.chargedEmEnergyFraction()  );
	hists["hist_pf_dijets_jetNEF"]->Fill( jet0.neutralEmEnergyFraction()  );
	hists["hist_pf_dijets_jetCHF"]->Fill( jet0.chargedHadronEnergyFraction()  );
	hists["hist_pf_dijets_jetNHF"]->Fill( jet0.neutralHadronEnergyFraction()  );


	hists["hist_pf_dijets_jetPt"]->Fill( jet1.pt() );
	hists["hist_pf_dijets_jetEtaVsPhi"]->Fill( jet1.eta(), jet1.phi() );
	hists["hist_pf_dijets_nConstituents"]->Fill( jet1.nConstituents() );
	hists["hist_pf_dijets_jetCEF"]->Fill( jet1.chargedEmEnergyFraction()  );
	hists["hist_pf_dijets_jetNEF"]->Fill( jet1.neutralEmEnergyFraction()  );
	hists["hist_pf_dijets_jetCHF"]->Fill( jet1.chargedHadronEnergyFraction()  );
	hists["hist_pf_dijets_jetNHF"]->Fill( jet1.neutralHadronEnergyFraction()  );

      
      
   
      
      } // end if 2 good PF jets
    
    }// end if delta phi pf cuts
    
  } // end loop over events
    
  cout << "Calo jet selection" << endl;
  caloSelector.print(std::cout);
  cout << "PF jet selection" << endl;
  pfSelector.print(std::cout);




  return 0;
}

