#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "PhysicsTools/FWLite/interface/CommandLineParser.h" 
#include "PhysicsTools/PatExamples/interface/WPlusJetsEventSelector.h"
#include "Math/GenVector/PxPyPzM4D.h"

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>
#include <boost/lexical_cast.hpp>

//Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"

using namespace std;

enum
{
   kNormalMode,
   kVqqMode,
   kLFMode,
   kWcMode
};

// Global Variables - maybe should be done differently
double muPt_, muEta_, d0_, norm_chi2_;
double hCalVeto_, eCalVeto_, trackIso_;
double eCalIso_, hCalIso_, relIso_;
double ePt_, eEta_, ePhi_, eD0_;
int    nhits_, HFcat_;
unsigned int nJetsCut;
bool   muPlusJets_, ePlusJets_;
bool   passTrigger, passOneLepton;
string sampleNameInput;

edm::Handle< vector< pat::Muon     > > muonHandle_;
edm::Handle< vector< pat::Electron > > electronHandle_;
edm::Handle< vector< pat::Jet      > > jetHandle_;
//edm::Handle< vector< pat::Muon > > muonHandle_;


// Function which takes in the collections and fills the histograms
bool make_plots(fwlite::EventContainer & ev, vector<pat::Electron> electrons, vector<pat::Muon> muons, vector<pat::Jet> jets, vector<pat::Jet> jetsBeforeClean, std::string prename, std::string secvtxname);

// Calculate the name that should be used for this event based on the
// mode, the HF word, and (if necessary), whether or not it's a W or
// Z.  Returns false if the event should not be processed.
bool calcSampleName (fwlite::EventContainer &eventCont, string &sampleName);


int main ( int argc, char ** argv )
{
  ///// Command Line Options /////
  
  // Tell people what this analysis code does and setup default options.
  optutl::CommandLineParser parser ("SHyFT tagged analysis");
  
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
		    1 );
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
  parser.addOption ("mode",        optutl::CommandLineParser::kInteger, 
		    "Normal(0), VQQ(1), LF(2), Wc(3)", 
		    0);   
  parser.addOption ("sampleName",   optutl::CommandLineParser::kString, 
		    "Sample name (e.g., top, Wqq, etc.)");

  parser.addOption ("jetScale", optutl::CommandLineParser::kDouble,
                    "Scale factor to apply to jet energies",
                    1.0);
  
  // Parse the command line arguments
  parser.parseArguments (argc, argv);
  
  ///// Create Event Container /////
    
  // This object 'event' is used both to get all information from the
  // event as well as to store histograms, etc.
  fwlite::EventContainer ev (parser);
  
  // Setup a style
  gROOT->SetStyle ("Plain");
  
  //cout << "About to allocate functors" << endl;
  
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
  muonIdLoose->set( "RelIso",   0.2 );

  // Loose electron id
  boost::shared_ptr<ElectronVPlusJetsIDSelectionFunctor>  electronIdLoose     
    (new ElectronVPlusJetsIDSelectionFunctor( ElectronVPlusJetsIDSelectionFunctor::SUMMER08) );
  electronIdLoose->set( "D0",  false);
  electronIdLoose->set( "RelIso", 0.2 );
  // Loose jet id
  boost::shared_ptr<JetIDSelectionFunctor>                jetIdLoose      
    ( new JetIDSelectionFunctor( JetIDSelectionFunctor::CRAFT08, JetIDSelectionFunctor::LOOSE) );

  //cout << "Making event selector" << endl;
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

  //Shift the jet energy scale, if desired.
  wPlusJets.scaleJets(parser.doubleValue("jetScale"));

  muPlusJets_ = parser.boolValue    ("muPlusJets");
  ePlusJets_  = parser.boolValue    ("ePlusJets" );
  nJetsCut    = parser.integerValue ("minNJets"  );

  
  // Trying to smartly create the histograms. There must be a better way, but this removes many lines of code
  string prename;
  sampleNameInput = parser.stringValue  ("sampleName");
  std::vector<std::string> sampleNameBase;
  std::vector<std::string> sampleName;
  std::vector<std::string> secvtxName(5,"_secvtxMass_");
  secvtxName[0]+="1j_"; secvtxName[1]+="2j_"; secvtxName[2]+="3j_"; secvtxName[3]+="4j_"; secvtxName[4]+="5j_";
  
  std::vector<std::string> secvtxEnd;
  secvtxEnd.push_back("1t_b");  secvtxEnd.push_back("1t_c");  secvtxEnd.push_back("1t_q");
  secvtxEnd.push_back("1t_x");  secvtxEnd.push_back("1t");    secvtxEnd.push_back("2t_bb");
  secvtxEnd.push_back("2t_bc"); secvtxEnd.push_back("2t_bq"); secvtxEnd.push_back("2t_cc");
  secvtxEnd.push_back("2t_cq"); secvtxEnd.push_back("2t_qq"); secvtxEnd.push_back("2t");
  secvtxEnd.push_back("2t_xx");

  if(sampleNameInput=="Vqq") {
    sampleNameBase.push_back(sampleNameInput+"W");
    sampleNameBase.push_back(sampleNameInput+"Z");
    sampleNameBase.push_back(sampleNameInput+"X");
    for(int i=0;i<3;++i) {
      sampleName.push_back(sampleNameBase[i]+"bb");
      sampleName.push_back(sampleNameBase[i]+"b2");
      sampleName.push_back(sampleNameBase[i]+"cc");
      sampleName.push_back(sampleNameBase[i]+"c2");
     }
  }
  else if (sampleNameInput=="WJets") {
    sampleName.push_back("WJets");
    sampleName.push_back("WJetsb3");
    sampleName.push_back("WJetsc3");
  }
  else sampleName.push_back(sampleNameInput);

  for(int i=0;i<2;++i) {
    if(i==0) prename = "noSelection_";
    else prename = "";
    if( muPlusJets_ ) {
      ev.add ( new TH1F( prename+TString("muPt"),     "Muon p_{T} (GeV/c) ", 100,    0, 200) );
      ev.add ( new TH1F( prename+TString("muEta"),    "Muon eta",	      50, -3.0, 3.0) );
      ev.add ( new TH1F( prename+TString("nHits"),    "Muon N Hits",	      35,    0,	 35) );
      ev.add ( new TH1F( prename+TString("d0"),	      "Muon D0",              60, -0.2,	0.2) );
      ev.add ( new TH1F( prename+TString("Chi2"),     "Muon Chi2",	      20,    0,   5) );
      ev.add ( new TH1F( prename+TString("hCalVeto"), "Muon hCalVeto",	      30,    0,	 30) );
      ev.add ( new TH1F( prename+TString("eCalVeto"), "Muon eCalVeto",	      30,    0,	 30) );
  
    }
    
    if ( ePlusJets_ ) {
      ev.add( new TH1F( prename+TString("ePt"),	      "Electron p_{T} (GeV/c) ", 100,    0, 200) );
      ev.add( new TH1F( prename+TString("eEta"),      "Electron eta",		  50, -3.0, 3.0) );
      ev.add( new TH1F( prename+TString("ePhi"),      "Electron Phi",		  50, -3.2, 3.2) );
      ev.add( new TH1F( prename+TString("eD0"),	      "Electron D0",	          60, -0.2, 0.2) );
    }  // end  ePlusJets_
    
    ev.add( new TH1F( prename+TString("trackIso"), "TrackIso",		      50,    0,	  50) );
    ev.add( new TH1F( prename+TString("eCalIso"),  "eCalIso",		      80,    0,   40) );
    ev.add( new TH1F( prename+TString("hCalIso"),  "hCalIso",		      60,    0,   30) );
    ev.add( new TH1F( prename+TString("relIso"),   "RelIso",		      50,    0,    5) );
    ev.add( new TH1F( prename+TString("nJets"),    "N Jets, pt>30, eta<2.4",  15,    0,	  15) );
    ev.add( new TH1F( prename+TString("jet1Pt"),   "1st leading jet pt",     150,    0,  300) );
    ev.add( new TH1F( prename+TString("jet2Pt"),   "2nd leading jet pt",     150,    0,  300) );
    ev.add( new TH1F( prename+TString("jet3Pt"),   "3rd leading jet pt",     150,    0,  300) );
    ev.add( new TH1F( prename+TString("jet4Pt"),   "4th leading jet pt",     150,    0,  300) );
    ev.add( new TH1F( prename+TString("jet1Eta"),  "1st leading jet eta",     50, -3.0,  3.0) );
    ev.add( new TH1F( prename+TString("jet2Eta"),  "2nd leading jet eta",     50, -3.0,  3.0) );
    ev.add( new TH1F( prename+TString("jet3Eta"),  "3rd leading jet eta",     50, -3.0,  3.0) );
    ev.add( new TH1F( prename+TString("jet4Eta"),  "4th leading jet eta",     50, -3.0,  3.0) );
    ev.add( new TH1F( prename+TString("bmass"),    "B Sec Vtx Mass",          28,    0,    7) );
    ev.add( new TH1F( prename+TString("cmass"),    "C Sec Vtx Mass",          28,    0,    7) );
    ev.add( new TH1F( prename+TString("lfmass"),   "LF Sec Vtx Mass",         28,    0,    7) );
    ev.add( new TH1F( prename+TString("flavorhistory"), "Flavor History",     12,    0,   12) );
    ev.add( new TH1F( prename+TString("discriminator"), "BTag Discriminator", 30,    2,    8) );
    ev.add( new TH1F( prename+TString("nVertices"), "num sec Vertices",        5,    0,    5) );
    ev.add ( new TH1F( prename+TString("jet1Mass"),   "1st leading jet mass",	    50,	   0,	   150) );
    ev.add ( new TH1F( prename+TString("jet2Mass"),   "2nd leading jet mass",      50,    0,      150) );
    ev.add ( new TH1F( prename+TString("jet3Mass"),   "3rd leading jet mass",      50,    0,      150) );
    ev.add ( new TH1F( prename+TString("jet4Mass"),   "4th leading jet mass",      50,    0,      150) );
  
    for (unsigned int j=0;j<sampleName.size();++j) {
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT"), "HT using Et is the sum of Jet Et plus Muon Pt", 50, 0, 1200) );
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hTUsingPt"), "HT s is Sum of Jet Pt", 50, 0, 1200) );
      ev.add ( new TH2F( prename+sampleName[j]+TString("_hTvsNJet"), "HT as a function of NJets", 5, 0.5, 5.5, 50, 0, 1200));
      
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_3jet"), "HT using Et is the sum of Jet Et plus Muon Pt", 50, 0, 1200) );
      ev.add ( new TH2F( prename+sampleName[j]+TString("_hTvsNJet_3jet"), "HT as a function of NJets", 5, 0.5, 5.5, 50, 0, 1200));
      //----- Use separate HT histograms
      
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_1j"), "HT using Pt is the sum of Jet Et plus Muon Pt", 10, 50, 300) );
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_2j"), "HT using Pt is the sum of Jet Et plus Muon Pt", 10, 80, 500) );
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_3j"), "HT using Pt is the sum of Jet Et plus Muon Pt", 10, 110, 600) );
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_4j"), "HT using Pt is the sum of Jet Et plus Muon Pt", 5, 140, 600) );
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_5j"), "HT using Pt is the sum of Jet Et plus Muon Pt", 5, 170, 600) );
      ev.add ( new TH1F( prename+sampleName[j]+TString("_hT_345j"), "HT using Pt is the sum of Jet Et plus Muon Pt", 10, 110, 600) );


      for(unsigned int k=0;k<secvtxName.size();++k) {
	for(unsigned int l=0;l<secvtxEnd.size();++l) {
	  std::string temp = prename+sampleName[j]+secvtxName[k]+secvtxEnd[l];
	  ev.add( new TH1F( temp.c_str(), "secvtxmass", 40,    0,   10) );
	  if(k==0 && l==4) break;
	}
      }
      ev.add( new TH2F( prename+sampleName[j]+TString("_jettag"), "N-Jets vs N-tags", 6, -0.5, 5.5, 3, -0.5, 2.5));
    }
  }  
  
  
  //loop through each event
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev) {
    
    //////////////////////////////////
    // Take What We Need From Event //
    //////////////////////////////////
    fwlite::Handle< vector< pat::Jet > > jetCollection;
    jetCollection.getByLabel (ev, "selectedLayer1Jets");
    assert ( jetCollection.isValid() );
    
    std::strbitset ret = wPlusJets.getBitTemplate();

    bool passed = wPlusJets(ev, ret);
    vector<pat::Electron> const & electrons = wPlusJets.selectedElectrons();
    vector<pat::Muon>     const & muons     = wPlusJets.selectedMuons();
    vector<pat::Jet>      const & jets      = wPlusJets.cleanedJets();
    vector<pat::Jet>      const & jetsBeforeClean = wPlusJets.selectedJets();

    string bit_;
    
    bit_ = "Trigger" ;
    passTrigger = ret[ bit_ ];
    bit_ = "== 1 Lepton";
    passOneLepton = ret[ bit_ ];
    // if not passed trigger, next event
    if ( !passTrigger )  continue;
   
    ev.getByLabel ( edm::InputTag("selectedLayer1Muons") , muonHandle_);
    assert( muonHandle_.isValid() );
    
    ev.getByLabel ( edm::InputTag("selectedLayer1Electrons") , electronHandle_);
    assert( electronHandle_.isValid() );
        
    ev.getByLabel ( edm::InputTag("selectedLayer1Jets") , jetHandle_);
    assert( jetHandle_.isValid() );
   
    std::string prename = "noSelection_";
    std::string secvtxname = "";

    //find the sample name
    if(!calcSampleName(ev, secvtxname) ) continue;
   
    // Make the plots for the pre-event selection sample;
    if(!make_plots(ev, *electronHandle_, *muonHandle_, jets, jetsBeforeClean, prename, secvtxname) ) continue;
    
    // Make the plots for the post-event selection sample;
    if ( passed ) {
      prename = "";
      if(!make_plots(ev, electrons, muons, jets, jetsBeforeClean, prename, secvtxname)) continue;
    }
  } //end event loop
  
  //cout << "Printing" << endl;
  wPlusJets.print(std::cout);
  //cout << "We're done!" << endl;
  
  return 0;
}

bool make_plots(fwlite::EventContainer & ev, vector<pat::Electron> electrons, vector<pat::Muon> muons, vector<pat::Jet> jets, vector<pat::Jet> jetsBeforeClean, std::string prename, std::string secvtxname) {
  
  //SecVtxMass and b-tagging related quantities
  int numBottom=0,numCharm=0,numLight=0;
  int numTags=0, numJets=0;
  double sumVertexMass=0, vertexMass=0;
  for ( std::vector< pat::Jet >::const_iterator jetBegin = jets.begin(),
	  jetEnd = jets.end(), jetIter = jetBegin;
	jetIter != jetEnd; ++jetIter)
    {
      // Is this jet tagged and does it have a good secondary vertex
      if( jetIter->bDiscriminator("simpleSecondaryVertexBJetTags") < 2.05 )
	// This jet is not tagged, so we skip it
	continue;
      
      reco::SecondaryVertexTagInfo const * svTagInfos
	= jetIter->tagInfoSecondaryVertex("secondaryVertex");
      if ( svTagInfos->nVertices() <= 0 )  continue;
      else ev.hist( prename+TString("nVertices") ) -> Fill( svTagInfos->nVertices() );
     
      // Calculate SecVtx Mass //
      ROOT::Math::LorentzVector< ROOT::Math::PxPyPzM4D<double> > sumVec;
      
      reco::Vertex::trackRef_iterator
	kEndTracks = svTagInfos->secondaryVertex(0).tracks_end();
      for (reco::Vertex::trackRef_iterator trackIter =
	     svTagInfos->secondaryVertex(0).tracks_begin();
	   trackIter != kEndTracks;
	   ++trackIter )
	{
	  const double kPionMass = 0.13957018;
	  ROOT::Math::LorentzVector< ROOT::Math::PxPyPzM4D<double> >  p4_1;
	  p4_1.SetPx( (*trackIter)->px() );
	  p4_1.SetPy( (*trackIter)->py() );
	  p4_1.SetPz( (*trackIter)->pz() );
	  p4_1.SetM (kPionMass);
	  sumVec += p4_1;
	  
	}  // for trackIter
      
      vertexMass = sumVec.M();
      sumVertexMass += vertexMass;

      int jetFlavor = std::abs( jetIter->partonFlavour() );
    
      //Here we determine what kind of flavor we have in this jet
      ev.hist( prename+TString("flavorhistory") ) -> Fill ( HFcat_ );
      if (5 == jetFlavor)
	{
	  ev.hist( prename+TString("bmass") ) -> Fill( vertexMass );
	  ++numBottom;
	} // if bottom
      else if ( 4 == jetFlavor )
	{
	  ev.hist( prename+TString("cmass") ) -> Fill( vertexMass );
	  ++numCharm;
	} // if charm
      else
	{
	  ev.hist( prename+TString("lfmass") ) -> Fill( vertexMass );
	  ++numLight;
	} // if light flavor
      
      ++numTags;
      ev.hist( prename+TString("discriminator") ) -> Fill ( jetIter->bDiscriminator("simpleSecondaryVertexBJetTags") );
      
      // For now, we only care if we have 2 tags...any more are treated the same - maybe we should look at 3 tags?
      if(numTags==2) break;
      
    }//jets

  // Calculate average SecVtx mass and //
  // fill appropriate histograms.      //
  numJets = std::min( (int) jets.size(), 5 );
  ev.hist( prename+secvtxname + "_jettag")->Fill (numJets, numTags);
      
  // If we don't have any tags, don't bother going on
  if ( ! numTags) {
    double hTUsingPt = muPt_;
    double hTUsingEt = muPt_;
    
    
    for (unsigned ijet = 0; ijet < jets.size(); ijet++) {
      hTUsingPt += jets[ijet].pt();
      hTUsingEt += jets[ijet].et();
      if (ijet == 0) {
	ev.hist(prename+TString("jet1Pt" ))	->Fill( jets[ijet].pt() 	);
	ev.hist(prename+TString("jet1Mass" ))	->Fill( jets[ijet].mass() 	);
	ev.hist(prename+TString("jet1Eta" ))	->Fill( jets[ijet].eta()	);
      }
      if (ijet == 1) {
	ev.hist(prename+TString("jet2Pt" )) ->Fill( jets[ijet].pt()    );
	ev.hist(prename+TString("jet2Mass" ))  ->Fill( jets[ijet].mass()    );
	ev.hist(prename+TString("jet2Eta" )) ->Fill( jets[ijet].eta()   );
      }
      if (ijet == 2) {
	ev.hist(prename+TString("jet3Pt" )) ->Fill( jets[ijet].pt()    );
	ev.hist(prename+TString("jet3Mass" ))  ->Fill( jets[ijet].mass()    );
	ev.hist(prename+TString("jet3Eta" )) ->Fill( jets[ijet].eta()   );
      }
      
      if (ijet == 3) {
	ev.hist(prename+TString("jet4Pt" )) ->Fill( jets[ijet].pt()    );
	ev.hist(prename+TString("jet4Mass" ))  ->Fill( jets[ijet].mass()    );
	ev.hist(prename+TString("jet4Eta" )) ->Fill( jets[ijet].eta()   );
      }
      
    }
     
    if (numJets == 1 ) ev.hist(prename+sampleNameInput+TString("_hT_1j"))->Fill(hTUsingEt);
    if (numJets == 2 ) ev.hist(prename+sampleNameInput+TString("_hT_2j"))->Fill(hTUsingEt);
    if (numJets == 3 ) ev.hist(prename+sampleNameInput+TString("_hT_3j"))->Fill(hTUsingEt);
    if (numJets == 4 ) ev.hist(prename+sampleNameInput+TString("_hT_4j"))->Fill(hTUsingEt);
    if (numJets == 5 ) ev.hist(prename+sampleNameInput+TString("_hT_5j"))->Fill(hTUsingEt);

        

    ev.hist(prename+sampleNameInput+TString("_hT"))  ->Fill( hTUsingEt   );
    ev.hist(prename+sampleNameInput+TString("_hTUsingPt"))->Fill (hTUsingPt);
    ev.hist(prename+sampleNameInput+TString("_hTvsNJet"))-> Fill (numJets, hTUsingEt);

      return true;
  }

  sumVertexMass /= numTags;
    
  string whichtag = "";
  if (1 == numTags)
    {
      // single tag
      if      (numBottom)              whichtag = "_b";
      else if (numCharm)               whichtag = "_c";
      else if (numLight)               whichtag = "_q";
      else                             whichtag = "_x";
    }
  else {
    // double tags
    if      (2 == numBottom)         whichtag = "_bb";
    else if (2 == numCharm)          whichtag = "_cc";
    else if (2 == numLight)          whichtag = "_qq";
    else if (numBottom && numCharm)  whichtag = "_bc";
    else if (numBottom && numLight)  whichtag = "_bq";
    else if (numCharm  && numLight)  whichtag = "_cq";
    else                             whichtag = "_xx";
  } // if two tags
  string massName = secvtxname
   + Form("_secvtxMass_%dj_%dt", numJets, numTags);

  ev.hist( prename + massName           ) -> Fill (sumVertexMass);
  ev.hist( prename + massName + whichtag) -> Fill (sumVertexMass);

  
  // Muons Only //
  if ( muPlusJets_ ){
    const pat::Muon * globalMuon = NULL;
    //find the first global muon
    for ( std::vector<pat::Muon>::const_iterator muonBegin = muons.begin(),
	    muonEnd = muons.end(), imuon = muonBegin;
	  imuon != muonEnd; ++imuon ) {
      if ( imuon->isGlobalMuon() ) {
	globalMuon = &(*imuon);
	break;
      }
    }
    if ( globalMuon == NULL )   {  cout<<"No Global Muon is found"<<endl; return false; }
    muPt_ 	= globalMuon->pt();
    muEta_	= globalMuon->eta();
    nhits_	= static_cast<int>( globalMuon->numberOfValidHits() );
    d0_		= globalMuon->dB();
    norm_chi2_	= globalMuon->normChi2();
    hCalVeto_	= globalMuon->isolationR03().hadVetoEt;
    eCalVeto_	= globalMuon->isolationR03().emVetoEt;
    trackIso_	= globalMuon->trackIso();
    eCalIso_	= globalMuon->ecalIso();
    hCalIso_	= globalMuon->hcalIso();
    relIso_	= ( trackIso_ + eCalIso_ + hCalIso_ )/muPt_ ;

    ev.hist( prename+TString("muPt") )	  ->Fill( muPt_      );
    ev.hist( prename+TString("muEta") )   ->Fill( muEta_     );
    ev.hist( prename+TString("nHits") )   ->Fill( nhits_     );
    ev.hist( prename+TString("d0") )	  ->Fill( d0_        );
    ev.hist( prename+TString("Chi2") )	  ->Fill( norm_chi2_ );
    ev.hist( prename+TString("hCalVeto") )->Fill( hCalVeto_  );
    ev.hist( prename+TString("eCalVeto") )->Fill( eCalVeto_  );
  } // end muonPlusJets_
  // Electrons Only //
  if ( ePlusJets_ ) {
    if ( electrons.size() == 0 )  return false;
    const pat::Electron * electron_ = NULL;
    electron_ = &( electrons[0] );
    if( electron_ == NULL )  {  cout<<"No electron Found"<<endl;   return false;  }
    ePt_      = electron_ ->pt();
    eEta_     = electron_ ->eta();
    ePhi_     = electron_ ->phi();
    eD0_      = electron_ ->dB();
    trackIso_ = electron_ ->trackIso();
    eCalIso_  = electron_ ->ecalIso();
    hCalIso_  = electron_ ->hcalIso();
    relIso_   = ( trackIso_ + eCalIso_ + hCalIso_ )/ePt_ ;

    ev.hist( prename+TString("ePt"  ) )	   ->Fill( ePt_	     );
    ev.hist( prename+TString("eEta" ) )	   ->Fill( eEta_     );
    ev.hist( prename+TString("ePhi" ) )	   ->Fill( ePhi_     );
    ev.hist( prename+TString("eD0"  ) )    ->Fill( eD0_	     );
    
  }// end ePlusJets_

  ev.hist( prename+TString("trackIso" ) )->Fill( trackIso_ );
  ev.hist( prename+TString("eCalIso"  ) )->Fill( eCalIso_  );
  ev.hist( prename+TString("hCalIso"  ) )->Fill( hCalIso_  );
  ev.hist( prename+TString("relIso"   ) )->Fill( relIso_   );
  
  if( !passOneLepton ) return false;
  ev.hist( prename+TString("nJets" ) )->Fill( jets.size() );
    
  unsigned int maxJets = jets.size();
  if ( maxJets >= nJetsCut ) {
    if ( maxJets > 4 ) maxJets = 4;
    for ( unsigned int i=0; i<maxJets; ++i) {
      ev.hist( prename+TString("jet" + boost::lexical_cast<std::string>(i+1) + "Pt") ) ->Fill( jets[i].pt()  );
      ev.hist( prename+TString("jet" + boost::lexical_cast<std::string>(i+1) + "Eta") )->Fill( jets[i].eta() );
    }
  }
  return true;
}

bool calcSampleName (fwlite::EventContainer &eventCont, string &sampleName)
{
  // calculate sample name
  optutl::CommandLineParser &parser = eventCont.parser();
  sampleName += parser.stringValue  ("sampleName");
  int mode   = parser.integerValue ("mode");
  
  // Get the heavy flavor category
  fwlite::Handle< unsigned int > heavyFlavorCategory;
  heavyFlavorCategory.getByLabel (eventCont, "flavorHistoryFilter");
  assert ( heavyFlavorCategory.isValid() );
  HFcat_ = (*heavyFlavorCategory);
  
  // Normal Mode //
  if (kNormalMode == mode)
    {
      // all we want is the sample name, so in this case we're done.
      return true;
    }
  
  // Light Flavor Mode //
  if (kLFMode == mode)
    {
      // Wqq
      if (5 == HFcat_)
	{
	  sampleName += "b3";
	} else if (6 == HFcat_)
	{
	  sampleName += "c3";
	} else if (11 != HFcat_)
	{
	  // skip this event
	  return false;
	} // else if ! 11
      return true;
    }
  
  // Wc Mode //
  if (kWcMode == mode)
    {
      // Wc
      if (4 != HFcat_)
	{
	  // skip this event
	  return false;
	} // if not Wc
      return true;
    } // else if Wc
  
  // Vqq Mode //
  
  // MadGraph (at least as CMS has implemented it) has this _lovely_
  // feature that if the W or Z is far enough off-shell, it erases
  // the W or Z from the event record.  This means that in some
  // number of cases, we won't be able to tell whether this is a W or
  // Z event by looking for a W or Z in the GenParticle collection.
  // (We'll eventually have to be more clever).
  //   sampleName = "X";
  fwlite::Handle< vector< reco::GenParticle > > genParticleCollection;
  genParticleCollection.getByLabel (eventCont, "prunedGenParticles");
  assert ( genParticleCollection.isValid() );
  // We don't know if it is a W, a Z, or neither
  // Iterate over genParticles
  const vector< reco::GenParticle>::const_iterator 
    kGenPartEnd = genParticleCollection->end();
  for (vector< reco::GenParticle>::const_iterator gpIter =
	 genParticleCollection->begin(); 
       gpIter != kGenPartEnd; ++gpIter ) 
    {
      if (gpIter->status() == 3 && std::abs(gpIter->pdgId()) == 23)
	{
	  sampleName += "Z";
	  break;
	}
      else if (gpIter->status() == 3 && std::abs(gpIter->pdgId()) == 24)
	{
	  sampleName += "W";
	  break;
	}
      else if (gpIter==kGenPartEnd-1) 
	{
	  sampleName += "X";
	  break;
	}
    } // for  gpIter
  switch (HFcat_)
    {
      // from:
      // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideFlavorHistory
      //  1. W+bb with >= 2 jets from the ME (dr > 0.5)
      //  2. W+b or W+bb with 1 jet from the ME
      //  3. W+cc from the ME (dr > 0.5)
      //  4. W+c or W+cc with 1 jet from the ME
      //  5. W+bb with 1 jet from the parton shower (dr == 0.0)
      //  6. W+cc with 1 jet from the parton shower (dr == 0.0)
      //  7. W+bb with >= 2 partons but 1 jet from the ME (dr == 0.0)
      //  8. W+cc with >= 2 partons but 1 jet from the ME (dr == 0.0)
      //  9. W+bb with >= 2 partons but 2 jets from the PS (dr > 0.5)
      // 10. W+cc with >= 2 partons but 2 jets from the PS (dr > 0.5)
      // 11. Veto of all the previous (W+ light jets)
    case 1:
      sampleName += "bb";
      break;
    case 2:
      // Sometimes this is referred to as 'b' (e.g., 'Wb'), but I
      // am using the suffix '2' to keep this case clear for when
      // we have charm (see below).
      sampleName += "b2";
      break; 
    case 3:
      sampleName += "cc";
      break;
    case 4:
      // We want to keep this case clear from real W + single charm
      // produced (as opposed to two charm quarks produced and one
      // goes down the beampipe), so we use 'c2' instead of 'c'.
      sampleName += "c2";
      break;
    default:
      // we don't want the rest of the cases.  Return an empty
      // string so we know.
      return false;
    } // switch HFcat_
  return true;
}

