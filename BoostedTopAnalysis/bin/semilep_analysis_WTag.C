//#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "TSystem.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "PhysicsTools/FWLite/interface/EventContainer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "PhysicsTools/SelectorUtils/interface/WPlusJetsEventSelector.h"
#include "Analysis/BoostedTopAnalysis/interface/CATopTagFunctor.h"
//#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/SemileptonicSelection.h"
#include "TLorentzVector.h"
#include "TH2F.h"

#include "PhysicsTools/SelectorUtils/interface/RunLumiSelector.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/ChainEvent.h"

#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"

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

using namespace std;


///////////////////////////
// ///////////////////// //
// // Main Subroutine // //
// ///////////////////// //
///////////////////////////


int main (int argc, char* argv[]) 
{

  if ( argc != 2)
    {
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
  edm::ParameterSet initParams          = parameters->getParameter<edm::ParameterSet>("initParams");

  cout << "setting up TFileService" << endl;
  // book a set of histograms
  string outName = outputs.getParameter<std::string>("outputName");
  string dirName = "histos";
  fwlite::TFileService fs = fwlite::TFileService(outName);
  TFileDirectory theDir = fs.mkdir( dirName.c_str() ); 
    
  cout << "Setting up chain event... ";
  // This object 'event' is used both to get all information from the
  // event as well as to store histograms, etc.
  fwlite::ChainEvent ev ( inputs.getParameter<std::vector<std::string> > ("fileNames") );
  cout <<"Done!\n";

   cout <<" Creating Functors... hold still...";
  SemileptonicSelection semilepSelector(*parameters);
  BoostedTopWTagFunctor boostedTopWTagFunctor(parameters->getParameter<edm::ParameterSet>("hadronicWParams"));
  pat::strbitset retHad = boostedTopWTagFunctor.getBitTemplate();
  
  // turn these off in the python config...
  //semilepSelector.set("Trigger", false);
  //if SemileptonicSelection's trigger is off, so is wPlusJets
  //semilepSelector.set("",false);

  cout <<"Done!\n";
 
  cout <<"Booking histograms...";
  std::map<std::string, TH1F*> histograms; //sal's "histogram registry,"  slick trick to manage the pointers :)
  std::map<std::string, TH2F*> histograms2D;
  histograms["lepJetPt"] = theDir.make<TH1F>( "lepJetPt", "Jet p_{T};Jet p_{T} (GeV/c)", 60, 0, 3000);
  histograms["lepJetMass"] = theDir.make<TH1F>( "lepJetMass", "Semileptonic Jet Mass;Jet Mass (GeV/c^{2}", 50, 0, 250 );
  histograms["muPt"] = theDir.make<TH1F>( "muPt", "Muon p_{T};Muon p_{T} (GeV/c)", 50, 0, 500 );
  histograms["muPtRel"] = theDir.make<TH1F>( "muPtRel", "Muon p_{T} Relative to Closest Jet;p_{T} (GeV/c)", 40, 0, 200.0);
  histograms["muDRMin"] = theDir.make<TH1F>( "muDRMin", "Muon #Delta R Relative to Closest Jet;#Delta R", 50, 0, 5.0);
  histograms["semiLepTopMass"] = theDir.make<TH1F>("semiLepTopMass","Semileptonic top mass",100,60.0,350);
  histograms["zPrimeMass"] = theDir.make<TH1F>("zPrimeMass","Z' invariant mass",60,0.0,600);
  histograms["hadronicTopMass"] = theDir.make<TH1F>("hadronicTopMass","Hadronic top mass",100,60.0,350);
  histograms["metDPhiMin"] = theDir.make<TH1F>("metDPhiMin","MET #Delta R to closest Jet;Delta R",50,0,5.0);
  histograms2D["mu2DBefore"] = theDir.make<TH2F>( "mu2DBefore", "Muon 2D Cut 1 Jet;#Delta R_{min};p_{T}^{REL} (GeV/c)", 50, 0, 5.0, 40, 0, 200.0 );
  histograms2D["mu2DAfter"] = theDir.make<TH2F>( "mu2DAfter", "Muon 2D Cut >2 Jets;#Delta R_{min};p_{T}^{REL} (GeV/c)", 50, 0, 5.0, 40, 0, 200.0 );
  histograms2D["semiMassVsGenPt"] = theDir.make<TH2F>("semiMassVsGenPt", "Semileptonic Side Mass versus GenJet p_{T}", 50, 0, 1500, 50, 0, 350); 

  histograms["muHtBefore"] = theDir.make<TH1F>( "muHtBefore", "Muon H_{T} no Jets;Muon H_{T} (GeV/c)", 50, 0, 500 );
  histograms["muHtAfter"] = theDir.make<TH1F>( "muHtAfter", "Muon H_{T} >2 Jets;Muon H_{T} (GeV/c)", 50, 0, 500 );

  histograms["nJetsSemi"] = theDir.make<TH1F>( "nJetsSemi", "Number of Semilep Jets; #Jets", 5, 0, 5 );
  

  histograms["had_w_deltaPhi"] = theDir.make<TH1F>( "had_w_deltaPhi", "#Delta #phi", 50, 0, TMath::Pi());
  histograms["had_w_m"] = theDir.make<TH1F>( "had_w_m", "m", 50, 0, 250 );
  histograms["had_w_pt"] = theDir.make<TH1F>( "had_w_pt", "pt", 150, 0, 1500 );
  histograms["had_w_m0"] = theDir.make<TH1F>( "had_w_m0", "m0", 50, 0, 200);
  histograms["had_w_m1"] = theDir.make<TH1F>( "had_w_m1", "m1", 50, 0, 200);
  histograms["had_w_pt0"] = theDir.make<TH1F>( "had_w_pt0", "pt0", 50, 0, 200);
  histograms["had_w_pt1"] = theDir.make<TH1F>( "had_w_pt1", "pt1", 50, 0, 200);
  histograms["had_w_deltaR"] = theDir.make<TH1F>( "had_w_deltaR", "#Delta R", 50, 0, 1.0 );
  histograms["had_w_y"]= theDir.make<TH1F>( "had_w_y", "Subjet Asymmetry", 50, 0, 1 );
  histograms["had_w_mu"] = theDir.make<TH1F>( "had_w_mu", "m_{0} / m", 50, 0, 1 );
  histograms2D["hadMassVsGenPt"] = theDir.make<TH2F>("hadMassVsGenPt", "Hadronic Side Mass versus GenJet p_{T}", 50, 0, 1500, 50, 0, 350); 

  histograms["nJetsA"] = theDir.make<TH1F>("nJetsA", "Number of jets in region A",5,0,5); 
  histograms["nJetsB"] = theDir.make<TH1F>("nJetsB", "Number of jets in region B",5,0,5);
  histograms["nJetsC"] = theDir.make<TH1F>("nJetsC", "Number of jets in region C",5,0,5);

  histograms["diffPtb1b2"] = theDir.make<TH1F>("diffPtb1b2", "p_{T} b1-b2", 50, -300,300);
  histograms["diffEb1b2"] = theDir.make<TH1F>("diffEb1b2", "E b1-b2", 50, -300,300);

  histograms2D["Mb1VsMb2"] = theDir.make<TH2F> ("Mb1VsMb2", "Mass of b1 vs mass of b2",50,0,300,50,0,300);
  histograms2D["Ptb1VsPtb2"] = theDir.make<TH2F> ("Ptb1VsPtb2", "p_{T} of b1 vs p_{T} of b2",50,0,1500,50,0,1500);

  cout<<"Done!\n";

  cout << "About to begin looping" << endl;

  int nev = 0;
  //loop through each event
  for (ev.toBegin(); ! ev.atEnd(); ++ev, ++nev) 
   {
      //if( nev == 150000) break;
     //if(nev==10000) break;

      edm::EventBase const & event = ev;
      if ( ev.event()->size() == 0 ) continue; // skip trees with no events
      if ( nev % 10000 == 0 ) cout << "Entry " << nev << ", Processing run " << event.id().run() << ", event " << event.id().event() << endl;
      pat::strbitset semilepRet (semilepSelector.getBitTemplate());
      semilepSelector(event, semilepRet);
      pat::strbitset wPlusJetsRet (semilepSelector.getWPlusJetsBitSet());
      string bitString;
      //SemileptonicSelection::candidate_collection::const_iterator wJet = semilepSelector.getWJet();
      SemileptonicSelection::candidate_collection::const_iterator closestJet = semilepSelector.getClosestJet();
      SemileptonicSelection::candidate met = semilepSelector.taggedMETs();
      SemileptonicSelection::candidate_collection taggedMuons = semilepSelector.taggedMuons();
      SemileptonicSelection::candidate_collection taggedJets  = semilepSelector.taggedJets();

      edm::Handle<std::vector<reco::GenParticle> > h_gens;
      event.getByLabel( edm::InputTag("decaySubset"), h_gens);

      typedef std::vector<reco::GenParticle> genparticle_collection;
      if(taggedMuons.size() > 0)
	{
	  TLorentzVector muP ( taggedMuons[0].px(),
			       taggedMuons[0].py(),
			       taggedMuons[0].pz(),
			       taggedMuons[0].energy() );
	  if(wPlusJetsRet[string("== 1 Lepton")])
	    {
	      histograms["nJetsSemi"]->Fill(taggedJets.size());
	      histograms["muHtBefore"]->Fill(taggedMuons[0].pt() + met.et());
	      if(taggedJets.size() > 0)
		{
		  TLorentzVector bjetP ( taggedJets[0].px(),
					 taggedJets[0].py(),
					 taggedJets[0].pz(),
					 taggedJets[0].energy() );
		  double ptRel = TMath::Abs(muP.Perp(bjetP.Vect()));
		  double dRMin = semilepSelector.getdRMin();
		  if(!(ptRel < 35 && dRMin < 0.4))
		    {
		      histograms2D["mu2DBefore"]->Fill( dRMin, ptRel );
		    }
		}
	    }
	  else if (wPlusJetsRet[string(">=2 Jets")])
	    {
	      histograms["muHtAfter"]->Fill(taggedMuons[0].pt() + met.et());
	      if(closestJet != taggedJets.end() )
		{
		  TLorentzVector bjetP( closestJet->px(),
					closestJet->py(),
					closestJet->pz(),
					closestJet->energy() );
		  double ptRel = TMath::Abs(muP.Perp(bjetP.Vect()));
		  double dRMin = semilepSelector.getdRMin();
		  if(!(ptRel < 35 && dRMin < 0.4))
		    {
		      histograms2D["mu2DAfter"]->Fill( dRMin, ptRel );
		    }
		}
	    }
	}	  
      if(semilepRet[string("Lepton has close jet")])
	{
	  TLorentzVector MET ( met.px(), 
			       met.py(), 
			       met.pz(), //filling with zero, should have an estimate of this to get it right
			       met.energy() );
	  TLorentzVector muP ( taggedMuons[0].px(),
			       taggedMuons[0].py(),
			       taggedMuons[0].pz(),
			       taggedMuons[0].energy() );
	  TLorentzVector bjetP ( closestJet->px(),
				 closestJet->py(),
				 closestJet->pz(),
				 closestJet->energy() );

	  double ptRel = TMath::Abs(muP.Perp(bjetP.Vect()));
	  double dRMin = semilepSelector.getdRMin();
	  if(semilepRet[string("Passed Semileptonic Side")])
	    {
	      double mMax = 0.0;
	      double yMax = 0.0;
	      double muMax = 0.0;
	      double dRMax = 0.0;
	      SemileptonicSelection::candidate_collection::const_iterator wJet = taggedJets.end();
	      for ( SemileptonicSelection::candidate_collection::const_iterator ijet = taggedJets.begin(),
		      taggedJetsBegin = taggedJets.begin(), taggedJetsEnd = taggedJets.end();
		    ijet != taggedJetsEnd; ++ijet ) 
		{
		  if ( ijet != closestJet && reco::deltaPhi<double>(ijet->phi(),taggedMuons[0].phi()) > 2*TMath::Pi()/3.0 ) 
		    {
		      retHad.set(false);
		      pat::Jet const * jet = dynamic_cast<pat::Jet const *>(ijet->masterClonePtr().get());
		      if ( jet != 0 && jet->numberOfDaughters() >= 2 ) 
			{
			  if ( ijet->mass() > mMax ) 
			    {
			      boostedTopWTagFunctor( *jet, retHad);
			      double y = 0.0, mu = 0.0, dR = 0.0;
			      pat::subjetHelper( *jet, y, mu, dR );
			      wJet = ijet;
			      mMax = ijet->mass();
			      yMax = y;
			      muMax = mu;
			      dRMax = dR;
			    }
			}
		    }
		}

	      TLorentzVector MET ( met.px(), 
				   met.py(), 
				   met.pz(), //filling with zero, should have an estimate of this to get it right
				   met.energy() );

	      double metDPhiMin = reco::deltaPhi<double>( closestJet->phi(), met.phi() );
	      if(wJet==taggedJets.end()) continue;
	      //semileptonic histograms		
	      histograms["muPtRel"]->Fill( ptRel );
	      histograms["muDRMin"]->Fill( dRMin );
	      histograms["metDPhiMin"]->Fill(metDPhiMin);
	      histograms["semiLepTopMass"]->Fill((muP + bjetP + MET).M());
	      pat::Jet const * closestJetPat = dynamic_cast<pat::Jet const *>(closestJet->masterClonePtr().get());
	      if (closestJetPat != NULL && closestJetPat->genJet() != 0 )
		histograms2D["semiMassVsGenPt"]->Fill( closestJetPat->genJet()->pt(), closestJet->mass() );
	      else
		std::cout << "Gen jet is zero!" << std::endl;
	      //double yMax=0.0, muMax=0.0, dRMax=0.0;
	      //pat::Jet const * jet = dynamic_cast<pat::Jet const *>(wJet->masterClonePtr().get());
	      //if (jet == NULL) cout << "ERROR, crashing!\n";
	      //pat::subjetHelper(*jet, yMax, muMax, dRMax);
	      //hadronic histograms
	      histograms["diffPtb1b2"]->Fill(closestJet->pt() - wJet->pt() );
	      histograms["diffEb1b2"]->Fill(closestJet->energy() - wJet->energy() );
	      histograms2D["Mb1VsMb2"]->Fill(closestJet->mass(), wJet->mass() );
	      histograms2D["Ptb1VsPtb2"]->Fill(closestJet->pt(), wJet->pt() );
	      histograms["had_w_m"]->Fill( wJet->mass() );
	      histograms["had_w_pt"]->Fill( wJet->pt() );
	      histograms["had_w_m0"]->Fill( wJet->daughter(0)->mass() );
	      histograms["had_w_m1"]->Fill( wJet->daughter(1)->mass() );
	      histograms["had_w_pt0"]->Fill( wJet->daughter(0)->pt() );
	      histograms["had_w_pt1"]->Fill( wJet->daughter(1)->pt() );
	      histograms["had_w_mu"]->Fill( muMax );
	      histograms["had_w_y"]->Fill( yMax );
	      histograms["had_w_deltaR"]->Fill( dRMax );	
	      pat::Jet const * wJetPat = dynamic_cast<pat::Jet const *>(wJet->masterClonePtr().get());
	      if ( wJetPat->genJet() != 0 ) 
		histograms2D["hadMassVsGenPt"]->Fill(  wJetPat->genJet()->pt(), wJet->mass() );
	      else
		std::cout << "Gen Jet is zero for w jet" << std::endl;
	    }
	}
   }// for (events)
  semilepSelector.print(cout);
  cout <<"----- boosted w top tagger ----\n";
  boostedTopWTagFunctor.print(cout);

  return 0;
}
