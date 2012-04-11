/* 
Example W+Jets selection
*/
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "TFile.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"
#include "TROOT.h"


#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 

#include "PhysicsTools/PatExamples/interface/WPlusJetsEventSelector.h"

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>

using namespace std;

int main ( int argc, char ** argv )
{


   ////////////////////////////////
   // ////////////////////////// //
   // // Command Line Options // //
   // ////////////////////////// //
   ////////////////////////////////

   // Tell people what this analysis code does and setup default options.
   optutl::CommandLineParser parser ("W+Jets Example");

   ////////////////////////////////////////////////
   // Change any defaults or add any new command //
   //      line options you would like here.     //
   ////////////////////////////////////////////////
   parser.stringValue ("storeprepend")="dcap:////pnfs/cms/WAX/11";
   parser.integerValue("outputevery" ) = 1000;
   parser.stringValue ("outputFile")    = "wPlusJets"; // .root added automatically


   parser.addOption ("muPlusJets",   optutl::CommandLineParser::kBool,
		     "Run mu+Jets",
                     true );
   parser.addOption ("ePlusJets",   optutl::CommandLineParser::kBool,
		     "Run e+Jets",
                     false );
   parser.addOption ("minNJets",   optutl::CommandLineParser::kInteger,
		     "Min number of tight jets",
                     4 );
   parser.addOption ("tightMuMinPt",   optutl::CommandLineParser::kDouble,
		     "Min tight mu pt",
                     20.0 );
   parser.addOption ("tightMuMaxEta",   optutl::CommandLineParser::kDouble,
		     "Max tight mu eta",
                     2.1 );
   parser.addOption ("tightEleMinPt",   optutl::CommandLineParser::kDouble,
		     "Min tight e pt",
		     30.0 );
   parser.addOption ("tightEleMaxEta",   optutl::CommandLineParser::kDouble,
		     "Max tight e eta",
                     2.4 );
   parser.addOption ("looseMuMinPt",   optutl::CommandLineParser::kDouble,
		     "Min loose mu pt",
                     10.0 );
   parser.addOption ("looseMuMaxEta",   optutl::CommandLineParser::kDouble,
		     "Max loose mu eta",
                     2.5 );
   parser.addOption ("looseEleMinPt",   optutl::CommandLineParser::kDouble,
		     "Min loose e pt",
		     15.0 );
   parser.addOption ("looseEleMaxEta",   optutl::CommandLineParser::kDouble,
		     "Max loose e eta",
                     2.5 );
   parser.addOption ("jetMinPt",   optutl::CommandLineParser::kDouble,
		     "Min jet pt",
		     30.0 );
   parser.addOption ("jetMaxEta",   optutl::CommandLineParser::kDouble,
		     "Max jet eta",
                     2.4 );
   

   // Parse the command line arguments
   parser.parseArguments (argc, argv);

   //////////////////////////////////
   // //////////////////////////// //
   // // Create Event Container // //
   // //////////////////////////// //
   //////////////////////////////////

   // This object 'event' is used both to get all information from the
   // event as well as to store histograms, etc.
   fwlite::EventContainer ev (parser);

   ////////////////////////////////////////
   // ////////////////////////////////// //
   // //         Begin Run            // //
   // // (e.g., book histograms, etc) // //
   // ////////////////////////////////// //
   ////////////////////////////////////////

   // Setup a style
   gROOT->SetStyle ("Plain");

  
  cout << "About to allocate functors" << endl;

  // Tight muon id
  boost::shared_ptr<MuonVPlusJetsIDSelectionFunctor>      muonIdTight     
    (new MuonVPlusJetsIDSelectionFunctor( MuonVPlusJetsIDSelectionFunctor::SUMMER08 ) );
  muonIdTight->set( "D0", 0.02 );
  // Tight electron id
  boost::shared_ptr<ElectronVPlusJetsIDSelectionFunctor>  electronIdTight     
    (new ElectronVPlusJetsIDSelectionFunctor( ElectronVPlusJetsIDSelectionFunctor::SUMMER08 ) );
  electronIdTight->set( "D0", 0.02 );

  // Tight jet id
  boost::shared_ptr<JetIDSelectionFunctor>                jetIdTight      
    ( new JetIDSelectionFunctor( JetIDSelectionFunctor::CRAFT08, JetIDSelectionFunctor::TIGHT) );

  
  // Loose muon id
  boost::shared_ptr<MuonVPlusJetsIDSelectionFunctor>      muonIdLoose     
    (new MuonVPlusJetsIDSelectionFunctor( MuonVPlusJetsIDSelectionFunctor::SUMMER08 ) );
  muonIdLoose->set( "Chi2",    false);
  muonIdLoose->set( "D0",      false);
  muonIdLoose->set( "NHits",   false);
  muonIdLoose->set( "ECalVeto",false);
  muonIdLoose->set( "HCalVeto",false);
  muonIdLoose->set( "RelIso", 0.2 );

  // Loose electron id
  boost::shared_ptr<ElectronVPlusJetsIDSelectionFunctor>  electronIdLoose     
    (new ElectronVPlusJetsIDSelectionFunctor( ElectronVPlusJetsIDSelectionFunctor::SUMMER08) );
  electronIdLoose->set( "D0",  false);
  electronIdLoose->set( "RelIso", 0.2 );
  // Loose jet id
  boost::shared_ptr<JetIDSelectionFunctor>                jetIdLoose      
    ( new JetIDSelectionFunctor( JetIDSelectionFunctor::CRAFT08, JetIDSelectionFunctor::LOOSE) );

  cout << "Making event selector" << endl;
  WPlusJetsEventSelector wPlusJets(
     edm::InputTag("selectedLayer1Muons"),
     edm::InputTag("selectedLayer1Electrons"),
     edm::InputTag("selectedLayer1Jets"),
     edm::InputTag("layer1METs"),
     edm::InputTag("triggerEvent"),
     muonIdTight,
     electronIdTight,
     jetIdTight,
     muonIdLoose,
     electronIdLoose,
     jetIdLoose,
     parser.integerValue ("minNJets")      ,
     parser.boolValue    ("muPlusJets")    ,
     parser.boolValue    ("ePlusJets")     ,
     parser.doubleValue  ("tightMuMinPt")  ,
     parser.doubleValue  ("tightMuMaxEta") ,
     parser.doubleValue  ("tightEleMinPt") ,
     parser.doubleValue  ("tightEleMaxEta"),
     parser.doubleValue  ("looseMuMinPt")  ,
     parser.doubleValue  ("looseMuMaxEta") ,
     parser.doubleValue  ("looseEleMinPt") ,
     parser.doubleValue  ("looseEleMaxEta"),
     parser.doubleValue  ("jetMinPt")      ,
     parser.doubleValue  ("jetMaxEta")
     );

  
  bool muPlusJets_ = parser.boolValue    ("muPlusJets");
  bool ePlusJets_  = parser.boolValue    ("ePlusJets");
  
  if( muPlusJets_ ) {
      ev.add ( new TH1F( "muPt",  "Muon p_{T} (GeV/c) ",     200,  0,  200 ) );
      ev.add ( new TH1F( "muEta", "Muon eta",			50,   -3.0,  3.0) );
      ev.add ( new TH1F( "nHits", "Muon N Hits",		50,	0,	50) );
      ev.add ( new TH1F( "d0",	  "Muon D0",			100,	-0.3,	0.3) );
      ev.add ( new TH1F( "Chi2",  "Muon Chi2",			50,	0,	25)  );
      ev.add ( new TH1F( "hCalVeto", "Muon hCalVeto",		100,	0,	100)  );
      ev.add ( new TH1F( "eCalVeto", "Muon eCalVeto",		100,	0,	100)  );
      ev.add ( new TH1F( "trackIso", "Muon trackIso",		200,	0,	200) );
      ev.add ( new TH1F( "eCalIso",  "Muon eCalIso",		100,	0,	100) );
      ev.add ( new TH1F( "hCalIso",  "Muon hCalIso",		100,	0,	100) );
      ev.add ( new TH1F( "relIso",   "Muon RelIso",		110,	-1.0,	10.0) );
      ev.add ( new TH1F( "nJets",    "N Jets, pt>30, eta<2.4",	30,	0,	30)  );
      ev.add ( new TH1F( "jet1Pt",   "1st leading jet pt",	300,	0,	300) );
      ev.add ( new TH1F( "jet2Pt",   "2nd leading jet pt",      300,    0,      300) );
      ev.add ( new TH1F( "jet3Pt",   "3rd leading jet pt",      300,    0,      300) );
      ev.add ( new TH1F( "jet4Pt",   "4th leading jet pt",      300,    0,      300) );
      ev.add ( new TH1F( "jet1Eta",  "1st leading jet eta",	50,     -3.0,   3.0) );
      ev.add ( new TH1F( "jet2Eta",  "2nd leading jet eta",     50,     -3.0,   3.0) );
      ev.add ( new TH1F( "jet3Eta",  "3rd leading jet eta",     50,     -3.0,   3.0) );
      ev.add ( new TH1F( "jet4Eta",  "4th leading jet eta",     50,     -3.0,   3.0) );
  }

  if ( ePlusJets_ ) {
      ev.add( new TH1F( "ePt",		"Electron p_{T} (GeV/c) ",	200,  0,  	200 ) );
      ev.add( new TH1F( "eEta",		"Electron eta",			50,   -3.0,  	3.0) );
      ev.add( new TH1F( "ePhi",		"Electron Phi",			50,	-3.2,	3.2) );
      ev.add( new TH1F( "eD0",		"Electron D0",			100,    -0.3,   0.3) );
      ev.add( new TH1F( "trackIso",	"Electron TrackIso",		200,    0,      200) );
      ev.add( new TH1F( "eCalIso",	"Electron ECalIso",		100,    0,      100) );
      ev.add( new TH1F( "hCalIso",	"Electron HCalIso",		100,    0,      100) );
      ev.add( new TH1F( "relIso",	"Electron RelIso",		110,    -1.0,   10.0) );
      ev.add( new TH1F( "nJets",	"Number of Jets before Clean",	30,     0,      30)  );
      ev.add( new TH1F( "nCleanedJets",	"Number of Jets after Clean",	30,     0,      30)  );
      ev.add( new TH1F( "jet1Pt",	"1st leading jet pt",		300,    0,      300) );
      ev.add( new TH1F( "jet2Pt",       "2nd leading jet pt",           300,    0,      300) );
      ev.add( new TH1F( "jet3Pt",       "3rd leading jet pt",           300,    0,      300) );
      ev.add( new TH1F( "jet4Pt",       "4th leading jet pt",           300,    0,      300) );
      ev.add( new TH1F( "jet1Eta",	"1st leading jet eta",		50,     -3.0,   3.0) );
      ev.add( new TH1F( "jet2Eta",      "2nd leading jet eta",          50,     -3.0,   3.0) );
      ev.add( new TH1F( "jet3Eta",      "3rd leading jet eta",          50,     -3.0,   3.0) );
      ev.add( new TH1F( "jet4Eta",      "4th leading jet eta",          50,     -3.0,   3.0) );
  }  // end  ePlusJets_




  //loop through each event
  for( ev.toBegin();
         ! ev.atEnd();
       ++ev) {

 
    std::strbitset ret = wPlusJets.getBitTemplate();


    bool passed = wPlusJets(ev, ret);
    vector<pat::Electron> const & electrons = wPlusJets.selectedElectrons();
    vector<pat::Muon>     const & muons     = wPlusJets.selectedMuons();
    vector<pat::Jet>      const & jets      = wPlusJets.cleanedJets();
    vector<pat::Jet>      const & jetsBeforeClean = wPlusJets.selectedJets();

    string bit_;
    if ( muPlusJets_ ){
        edm::Handle< vector< pat::Muon > > muonHandle_;
	ev.getByLabel ( edm::InputTag("selectedLayer1Muons") , muonHandle_);
	assert( muonHandle_.isValid() );
	//if pass muon trigger, plot the leading muon
	bit_ = "Trigger" ;
	bool passTrigger = ret[ bit_ ];
	bit_ = "== 1 Lepton";
	bool passOneMuon = ret[ bit_ ];
	// if not passed trigger, next event
	if ( !passTrigger )  continue;
	const pat::Muon * globalMuon = NULL;
	//find the first global muon
	for ( std::vector<pat::Muon>::const_iterator muonBegin = muonHandle_->begin(),
	        muonEnd = muonHandle_->end(), imuon = muonBegin;
	      imuon != muonEnd; ++imuon ) {
	      if ( imuon->isGlobalMuon() ) {
	         globalMuon = &(*imuon);
		 break;
	      }
	}
	if ( globalMuon == NULL )   {  cout<<"No Global Muon is found"<<endl; continue; }
	double muPt_ 		= globalMuon->pt();
	double muEta_		= globalMuon->eta();
	int	nhits_		= static_cast<int>( globalMuon->numberOfValidHits() );
	double	d0_		= globalMuon->dB();
	double	norm_chi2_	= globalMuon->normChi2();
	double	hCalVeto_	= globalMuon->isolationR03().hadVetoEt;
	double	eCalVeto_	= globalMuon->isolationR03().emVetoEt;
	double	trackIso_	= globalMuon->trackIso();
	double	eCalIso_	= globalMuon->ecalIso();
	double  hCalIso_	= globalMuon->hcalIso();
	double	relIso_		= ( trackIso_ + eCalIso_ + hCalIso_ )/muPt_ ;
	
	ev.hist( "muPt" )	->Fill(muPt_);
	ev.hist( "muEta" )	->Fill(muEta_ );
	ev.hist( "nHits" )	->Fill( nhits_ );
	ev.hist( "d0" )		->Fill( d0_ );
	ev.hist( "Chi2" )	->Fill( norm_chi2_ );
	ev.hist( "hCalVeto" )	->Fill( hCalVeto_  );
	ev.hist( "eCalVeto" )	->Fill( eCalVeto_  );
	ev.hist( "trackIso" )	->Fill( trackIso_  );
	ev.hist( "eCalIso" )	->Fill( eCalIso_   );
	ev.hist( "hCalIso" )	->Fill( hCalIso_   );
	ev.hist( "relIso"  )	->Fill( relIso_	   );

	//if pass One Muon, plot jets
	if ( !passOneMuon )   continue;
	ev.hist( "nJets" )	->Fill( jets.size() );
	if ( jets.size() >= 4 ) {
	   ev.hist( "jet1Pt" )	->Fill( jets[0].pt() 	);
	   ev.hist( "jet2Pt" )  ->Fill( jets[1].pt()    );
	   ev.hist( "jet3Pt" )  ->Fill( jets[2].pt()    );
	   ev.hist( "jet4Pt" )  ->Fill( jets[3].pt()    );
	   ev.hist( "jet1Eta")	->Fill( jets[0].eta()	);
	   ev.hist( "jet2Eta")  ->Fill( jets[1].eta()   );
	   ev.hist( "jet3Eta")  ->Fill( jets[2].eta()   );
	   ev.hist( "jet4Eta")  ->Fill( jets[3].eta()   );
	} // end jet size
	
    } // end muonPlusJets_

    if ( ePlusJets_ ) {
       //if pass electron trigger, plot the leading electron
       bit_ = "Trigger" ;
       bool passTrigger = ret[ bit_ ];
       bit_ = "== 1 Lepton";
       bool passOneElectron = ret[ bit_ ];
       // if not passed trigger, next event
       if ( !passTrigger )  continue;
       if ( electrons.size() == 0 )  continue;
       const pat::Electron * electron_ = NULL;
       electron_ = &( electrons[0] );
       if( electron_ == NULL )  {  cout<<"No electron Found"<<endl;   continue;  }
       double ePt_ 	= electron_ ->pt();
       double eEta_	= electron_ ->eta();
       double ePhi_	= electron_ ->phi();
       double eD0_	= electron_ ->dB();
       double trackIso_	= electron_ ->trackIso();
       double eCalIso_	= electron_ ->ecalIso();
       double hCalIso_	= electron_ ->hcalIso();
       double relIso_	= ( trackIso_ + eCalIso_ + hCalIso_ )/ePt_ ;

       ev.hist( "ePt" )		->Fill( ePt_	 );
       ev.hist( "eEta" )	->Fill( eEta_	);
       ev.hist( "ePhi" )	->Fill( ePhi_	);
       ev.hist( "eD0"  )	->Fill( eD0_	);
       ev.hist( "trackIso" )	->Fill( trackIso_);
       ev.hist( "eCalIso" )	->Fill( eCalIso_ );
       ev.hist( "hCalIso" )	->Fill( hCalIso_ );
       ev.hist( "relIso" )	->Fill( relIso_ );
       
       if( !passOneElectron )   continue;
       ev.hist( "nJets" )	->Fill( jetsBeforeClean.size() );
       ev.hist( "nCleanedJets" )->Fill( jets.size() );
       if ( jets.size() >= 4 ) {
           ev.hist( "jet1Pt" )  ->Fill( jets[0].pt()    );
           ev.hist( "jet2Pt" )  ->Fill( jets[1].pt()    );
           ev.hist( "jet3Pt" )  ->Fill( jets[2].pt()    );
           ev.hist( "jet4Pt" )  ->Fill( jets[3].pt()    );
           ev.hist( "jet1Eta")  ->Fill( jets[0].eta()   );
           ev.hist( "jet2Eta")  ->Fill( jets[1].eta()   );
           ev.hist( "jet3Eta")  ->Fill( jets[2].eta()   );
           ev.hist( "jet4Eta")  ->Fill( jets[3].eta()   );
        } // end jet size


       
    }// end ePlusJets_
 

    if ( passed ) {
      for ( vector<pat::Jet>::const_iterator jetsBegin = jets.begin(),
	      jetsEnd = jets.end(), ijet = jetsBegin; 
	    ijet != jetsEnd; ++ijet) {
	//	cout << "Looking at each jet, pt,eta = " << ijet->pt() << ", " << ijet->eta() << endl;
      } //end Jet loop   
    } // end if passes event selection
  } //end event loop
  
  cout << "Printing" << endl;
  wPlusJets.print(std::cout);

  cout << "We're done!" << endl;

  return 0;
}
