#include "Analysis/BoostedTopAnalysis/interface/BoostedTopAnalysis.h"
//using namespace std;
using std::cout;
using std::vector;
using std::endl;
using std::map;
using std::string;

BoostedTopAnalysis::BoostedTopAnalysis(const edm::ParameterSet& iConfig , TFileDirectory & iDir, 
				       SemileptonicSelection& semiLepSel, 
				       CATopJetEventSelector& typeISel,
				       WPlusBJetEventSelector& typeIIandIIISel ) :
  semilepSelector(semiLepSel),
  CATopJetSelector(typeISel),
  WPlusBJetSelector(typeIIandIIISel),
  hadType1_Side1_Ret(CATopJetSelector.getBitTemplate()),
  hadType1_Side2_Ret(CATopJetSelector.getBitTemplate()),
  hadType2_Side1_Ret(WPlusBJetSelector.getBitTemplate()),
  hadType2_Side2_Ret(WPlusBJetSelector.getBitTemplate()),
  semilepRet(semilepSelector.getBitTemplate()),
  evtHypothesis(),
  theDir(iDir)
{
  //Semileptonic histograms
  histograms["lepJetPt"] = theDir.make<TH1F>( "lepJetPt", "Jet p_{T};Jet p_{T} (GeV/c)", 60, 0, 3000);
  histograms["lepJetMass"] = theDir.make<TH1F>( "lepJetMass", "Semileptonic Jet Mass;Jet Mass (GeV/c^{2}", 50, 0, 250 );
  histograms["muPt"] = theDir.make<TH1F>( "muPt", "Muon p_{T};Muon p_{T} (GeV/c)", 50, 0, 500 );
  histograms["muPtRel"] = theDir.make<TH1F>( "muPtRel", "Muon p_{T} Relative to Closest Jet;p_{T} (GeV/c)", 40, 0, 200.0);
  histograms["muDRMin"] = theDir.make<TH1F>( "muDRMin", "Muon #Delta R Relative to Closest Jet;#Delta R", 50, 0, 5.0);
  histograms["semiLepTopMass"] = theDir.make<TH1F>("semiLepTopMass","Semileptonic top mass",100,60.0,350);
  histograms["zPrimeMass"] = theDir.make<TH1F>("zPrimeMass","Z' invariant mass",60,0.0,600);
  histograms["hadronicTopMass"] = theDir.make<TH1F>("hadronicTopMass","Hadronic top mass",100,60.0,350);
  histograms["metDPhiMin"] = theDir.make<TH1F>("metDPhiMin","MET #Delta R to closest Jet;Delta R",50,0,5.0);
  histograms2D["mu2D"] = theDir.make<TH2F>( "mu2D", "Muon 2D Cut;#Delta R_{min};p_{T}^{REL} (GeV/c)", 50, 0, 5.0, 40, 0, 200.0 );
  histograms2D["semiMassVsGenPt"] = theDir.make<TH2F>("semiMassVsGenPt", "Semileptonic Side Mass versus GenJet p_{T}", 50, 0, 1500, 50, 0, 350); 

  //Hadronic histograms 
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

  //SemileptonicSelection ;
  //BoostedTopWTagFunctor boostedTopWTagFunctor(parameters->getParameter<edm::ParameterSet>("hadronicWParams"));
  //pat::strbitset retHad = boostedTopWTagFunctor.getBitTemplate();
}

void BoostedTopAnalysis::analyze(const edm::EventBase& iEvent)
{
  //Classify the event topology
  //Run event selectors and decide how the event decayed
  semilepSelector(iEvent, semilepRet);
  reco::Candidate::LorentzVector dummy(0,0,0,0);
  //string bitString="Passed Semileptonic Side";

  if(semilepRet[string("Passed Semileptonic Side")])
    {
      //bitString = ">= 1 TopJet";
      reco::Candidate::LorentzVector muP = semilepSelector.taggedMuons()[0].p4();
      CATopJetSelector(iEvent, muP, hadType1_Side2_Ret, true, false);
      WPlusBJetSelector(iEvent, muP, hadType2_Side2_Ret, true, false);
      reco::ShallowClonePtrCandidate closestJet(*semilepSelector.getClosestJet());
      reco::ShallowClonePtrCandidate muon(semilepSelector.taggedMuons().at(0));
      reco::ShallowClonePtrCandidate met(semilepSelector.taggedMETs());
      
      if(hadType1_Side2_Ret[string(">= 1 TopJet")] /*|| hadTypeIRet[string(">= 2 TopJet")]*/)
	{
	  reco::ShallowClonePtrCandidate topJet     = CATopJetSelector.topJets().at(0);
	  evtHypothesis.setSemiLepType1(closestJet.masterClonePtr(),
					muon.masterClonePtr(),
					met.masterClonePtr(),
					topJet.masterClonePtr());
	  //fill histos here
	}
      else if(hadType2_Side2_Ret[string(">= 1 WJet")] && hadType2_Side2_Ret[string(">= 1 bJet")])
	{
	  //reco::ShallowClonePtrCandidate bJet = 
	  evtHypothesis.setSemiLepType2(closestJet.masterClonePtr(),
					muon.masterClonePtr(),
					met.masterClonePtr(),
					WPlusBJetSelector.bJets()[0].masterClonePtr(),
					WPlusBJetSelector.wJets()[0].masterClonePtr() );
	  
	  //fill histos here
	}
      else if( !WPlusBJetSelector.hasWJets() && WPlusBJetSelector.hasBJets() )
	{
	  evtHypothesis.setSemiLepType3(closestJet.masterClonePtr(),
					muon.masterClonePtr(),
					met.masterClonePtr(),
					WPlusBJetSelector.bJets()[0].masterClonePtr(),
					WPlusBJetSelector.minDrPair()[0].masterClonePtr(),
					WPlusBJetSelector.minDrPair()[1].masterClonePtr() );
	  //fill histos
	}
      else
	{
	  cerr <<" ERROR: Could not classify hadronic side of semileptonic event!\n";
	}
    }
  else //all hadronic from here on out!
    {
      CATopJetSelector(iEvent, dummy, hadType1_Side1_Ret, true, true);
      WPlusBJetSelector(iEvent, dummy, hadType2_Side1_Ret, true, true);
      if(hadType1_Side1_Ret[string(">= 1 TopJet")])
	{
	  vector<reco::ShallowClonePtrCandidate> const topJetsSide1 = CATopJetSelector.topJets();
	  vector<reco::ShallowClonePtrCandidate> const wJetsSide1 = WPlusBJetSelector.wJets();
	  vector<reco::ShallowClonePtrCandidate> const bJetsSide1 = WPlusBJetSelector.bJets();

	  CATopJetSelector(iEvent, topJetsSide1[0].p4() ,hadType1_Side2_Ret, true, false);
	  WPlusBJetSelector(iEvent, CATopJetSelector.topJets()[0].p4() ,hadType2_Side2_Ret, true, false);
	  if(hadType1_Side2_Ret[string(">= 1 TopJet")] /*|| hadTypeIRet[string(">= 2 TopJet")]*/)
	    {
	      evtHypothesis.setHadType1Type1( topJetsSide1[0].masterClonePtr(),
					      CATopJetSelector.topJets()[0].masterClonePtr());
	      //fill histos here
	    }
	  else if(hadType2_Side2_Ret[string(">= 1 WJet")] && hadType2_Side2_Ret[string(">= 1 bJet")])
	    {
	      evtHypothesis.setHadType1Type2( topJetsSide1[0].masterClonePtr(),
					      WPlusBJetSelector.bJets()[0].masterClonePtr(),
					      WPlusBJetSelector.wJets()[0].masterClonePtr());
	      //fill histos here
	    }
	  else if( !WPlusBJetSelector.hasWJets() && WPlusBJetSelector.hasBJets() )
	    {
	      evtHypothesis.setHadType1Type3(topJetsSide1[0].masterClonePtr(),
					     WPlusBJetSelector.bJets()[0].masterClonePtr(),
					     WPlusBJetSelector.minDrPair()[0].masterClonePtr(),
					     WPlusBJetSelector.minDrPair()[1].masterClonePtr() );
	      //fill histos
	    }
	  else
	    {
	      cerr <<" ERROR: Could not classify second side of hadronic Type 1 event!\n";
	    }
	}
      else if(hadType2_Side1_Ret[string(">= WJet")] && hadType2_Side1_Ret[string(">= 1 bJet")])
	{
	  vector<reco::ShallowClonePtrCandidate> const wJetsSide1 = WPlusBJetSelector.wJets();
	  vector<reco::ShallowClonePtrCandidate> const bJetsSide1 = WPlusBJetSelector.bJets();
	  if(WPlusBJetSelector.hasWJets())
	    WPlusBJetSelector(iEvent, wJetsSide1[0].p4() ,hadType2_Side2_Ret, true, false);
	  else
	    WPlusBJetSelector(iEvent, bJetsSide1[0].p4() ,hadType2_Side2_Ret, true, false);
	    
	  if(hadType2_Side2_Ret[string(">= 1 WJet")] && hadType2_Side2_Ret[string(">= 1 bJet")])
	    {
	      evtHypothesis.setHadType2Type2( wJetsSide1[0].masterClonePtr(),
					      bJetsSide1[0].masterClonePtr(),
					      WPlusBJetSelector.bJets()[0].masterClonePtr(),
					      WPlusBJetSelector.wJets()[0].masterClonePtr());
	      //fill histos here
	    }
	  else if( !WPlusBJetSelector.hasWJets() && WPlusBJetSelector.hasBJets() )
	    {
	      evtHypothesis.setHadType2Type3( wJetsSide1[0].masterClonePtr(),
					      bJetsSide1[0].masterClonePtr(),
					      WPlusBJetSelector.bJets()[0].masterClonePtr(),
					      WPlusBJetSelector.minDrPair()[0].masterClonePtr(),
					      WPlusBJetSelector.minDrPair()[1].masterClonePtr() );
	      //fill histos
	    }
	  else
	    {
	      cerr <<" ERROR: Could not classify second side of hadronic Type 2 event!\n";
	    }
	}
      else if(!WPlusBJetSelector.hasWJets() && WPlusBJetSelector.hasBJets() )
	{
	  //vector<reco::ShallowClonePtrCandidate> const wJetsSide1 = WPlusBJetSelector.wJets();
	  vector<reco::ShallowClonePtrCandidate> const bJetsSide1 = WPlusBJetSelector.bJets();
	  vector<reco::ShallowClonePtrCandidate> const minDrPairSide1  = WPlusBJetSelector.minDrPair();
	  WPlusBJetSelector(iEvent, bJetsSide1[0].p4() ,hadType2_Side2_Ret, true, false);

	  if( !WPlusBJetSelector.hasWJets() && WPlusBJetSelector.hasBJets() )
	    {
	      evtHypothesis.setHadType3Type3( bJetsSide1[0].masterClonePtr(),
					      minDrPairSide1[0].masterClonePtr(),
					      minDrPairSide1[1].masterClonePtr(),
					      WPlusBJetSelector.bJets()[0].masterClonePtr(),
					      WPlusBJetSelector.minDrPair()[0].masterClonePtr(),
					      WPlusBJetSelector.minDrPair()[1].masterClonePtr() );
	      //fill histos
	    }
	  else
	    {
	      cerr <<" ERROR: Could not classify second side of hadronic Type 3 event!\n";
	    }
	}
    }
  return;
}
