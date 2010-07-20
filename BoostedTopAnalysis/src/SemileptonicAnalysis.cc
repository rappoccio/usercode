#include "Analysis/BoostedTopAnalysis/interface/SemileptonicAnalysis.h"
#include "TLorentzVector.h"

using namespace std;


SemileptonicAnalysis::SemileptonicAnalysis(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  semileptonicSelection_(iConfig.getParameter<edm::ParameterSet>("semileptonicSelection")),
  boostedTopWTagFunctor_(iConfig.getParameter<edm::ParameterSet>("hadronicWParams")),
  theDir(iDir)
{


  histograms1d["lepJetPt"] = theDir.make<TH1F>( "lepJetPt", "Jet p_{T};Jet p_{T} (GeV/c)", 60, 0, 3000);
  histograms1d["lepJetMass"] = theDir.make<TH1F>( "lepJetMass", "Semileptonic Jet Mass;Jet Mass (GeV/c^{2}", 50, 0, 250 );
  histograms1d["muPt"] = theDir.make<TH1F>( "muPt", "Muon p_{T};Muon p_{T} (GeV/c)", 50, 0, 500 );
  histograms1d["muPtRel"] = theDir.make<TH1F>( "muPtRel", "Muon p_{T} Relative to Closest Jet;p_{T} (GeV/c)", 40, 0, 200.0);
  histograms1d["muDRMin"] = theDir.make<TH1F>( "muDRMin", "Muon #Delta R Relative to Closest Jet;#Delta R", 50, 0, 5.0);
  histograms1d["semiLepTopMass"] = theDir.make<TH1F>("semiLepTopMass","Semileptonic top mass",100,60.0,350);
  histograms1d["zPrimeMass"] = theDir.make<TH1F>("zPrimeMass","Z' invariant mass",60,0.0,600);
  histograms1d["hadronicTopMass"] = theDir.make<TH1F>("hadronicTopMass","Hadronic top mass",100,60.0,350);
  histograms1d["metDPhiMin"] = theDir.make<TH1F>("metDPhiMin","MET #Delta R to closest Jet;Delta R",50,0,5.0);
  histograms2d["mu2DBefore"] = theDir.make<TH2F>( "mu2DBefore", "Muon 2D Cut;#Delta R_{min};p_{T}^{REL} (GeV/c)", 50, 0, 5.0, 40, 0, 200.0 );
  histograms2d["mu2DAfter"] = theDir.make<TH2F>( "mu2DAfter", "Muon 2D Cut;#Delta R_{min};p_{T}^{REL} (GeV/c)", 50, 0, 5.0, 40, 0, 200.0 );
  histograms2d["semiMassVsGenPt"] = theDir.make<TH2F>("semiMassVsGenPt", "Semileptonic Side Mass versus GenJet p_{T}", 50, 0, 1500, 50, 0, 350); 

  histograms1d["muHtBefore"] = theDir.make<TH1F>( "muHtBefore", "Muon H_{T} no Jets;Muon H_{T} (GeV/c)", 50, 0, 500 );
  histograms1d["muHtAfter"] = theDir.make<TH1F>( "muHtAfter", "Muon H_{T} >2 Jets;Muon H_{T} (GeV/c)", 50, 0, 500 );
  histograms1d["muHtFinal"] = theDir.make<TH1F>( "muHtFinal", "Muon H_{T}, Full Selection;Muon H_{T} (GeV/c)", 50, 0, 500 );
  histograms1d["nJetsSemi"] = theDir.make<TH1F>( "nJetsSemi", "Number of Semilep Jets; #Jets", 5, 0, 5 );

  histograms1d["had_w_deltaPhi"] = theDir.make<TH1F>( "had_w_deltaPhi", "#Delta #phi", 50, 0, TMath::Pi());
  histograms1d["had_w_m"] = theDir.make<TH1F>( "had_w_m", "m", 50, 0, 250 );
  histograms1d["had_w_pt"] = theDir.make<TH1F>( "had_w_pt", "pt", 150, 0, 1500 );
  histograms1d["had_w_m0"] = theDir.make<TH1F>( "had_w_m0", "m0", 50, 0, 200);
  histograms1d["had_w_m1"] = theDir.make<TH1F>( "had_w_m1", "m1", 50, 0, 200);
  histograms1d["had_w_pt0"] = theDir.make<TH1F>( "had_w_pt0", "pt0", 50, 0, 200);
  histograms1d["had_w_pt1"] = theDir.make<TH1F>( "had_w_pt1", "pt1", 50, 0, 200);
  histograms1d["had_w_deltaR"] = theDir.make<TH1F>( "had_w_deltaR", "#Delta R", 50, 0, 1.0 );
  histograms1d["had_w_y"]= theDir.make<TH1F>( "had_w_y", "Subjet Asymmetry", 50, 0, 1 );
  histograms1d["had_w_mu"] = theDir.make<TH1F>( "had_w_mu", "m_{0} / m", 50, 0, 1 );
  histograms2d["hadMassVsGenPt"] = theDir.make<TH2F>("hadMassVsGenPt", "Hadronic Side Mass versus GenJet p_{T}", 50, 0, 1500, 50, 0, 350); 

  histograms1d["nJetsA"] = theDir.make<TH1F>("nJetsA", "Number of jets in region A",5,0,5); 
  histograms1d["nJetsB"] = theDir.make<TH1F>("nJetsB", "Number of jets in region B",5,0,5);
  histograms1d["nJetsC"] = theDir.make<TH1F>("nJetsC", "Number of jets in region C",5,0,5);

  histograms1d["diffPtb1b2"] = theDir.make<TH1F>("diffPtb1b2", "p_{T} b1-b2", 50, -300,300);
  histograms1d["diffEb1b2"] = theDir.make<TH1F>("diffEb1b2", "E b1-b2", 50, -300,300);

  histograms2d["Mb1VsMb2"] = theDir.make<TH2F> ("Mb1VsMb2", "Mass of b1 vs mass of b2",50,0,300,50,0,300);
  histograms2d["Ptb1VsPtb2"] = theDir.make<TH2F> ("Ptb1VsPtb2", "p_{T} of b1 vs p_{T} of b2",50,0,1500,50,0,1500);


}

void SemileptonicAnalysis::analyze(const edm::EventBase& iEvent)
{

  pat::strbitset semilepRet = semileptonicSelection_.getBitTemplate();
  semileptonicSelection_(iEvent, semilepRet);
  string bitString;
  //SemileptonicSelection::candidate_collection::const_iterator wJet = semileptonicSelection_.getWJet();
  SemileptonicSelection::candidate_collection::const_iterator closestJet = semileptonicSelection_.getClosestJet();
  SemileptonicSelection::candidate const & met = semileptonicSelection_.taggedMETs();
  SemileptonicSelection::candidate_collection const & taggedMuons = semileptonicSelection_.taggedMuons();
  SemileptonicSelection::candidate_collection const & taggedJets  = semileptonicSelection_.taggedJets();
  pat::strbitset wPlusJetsRet (semileptonicSelection_.getWPlusJetsBitSet());

  if(taggedMuons.size() > 0)
    {
      TLorentzVector muP ( taggedMuons[0].px(),
			   taggedMuons[0].py(),
			   taggedMuons[0].pz(),
			   taggedMuons[0].energy() );
      if(semilepRet[string("Lepton")])
	{
	  histograms1d["nJetsSemi"]->Fill(taggedJets.size());
	  histograms1d["muHtBefore"]->Fill(taggedMuons[0].pt() + met.et());


	  if(semilepRet[string("Lepton has close jet")])
	    {
	      pat::strbitset retHad = boostedTopWTagFunctor_.getBitTemplate();
	      retHad.set(false);

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
	      double dRMin = semileptonicSelection_.getdRMin();
	      histograms2d["mu2DBefore"]->Fill( dRMin, ptRel );

	      if ( semilepRet[string("Relative Pt and Min Delta R")] ) {

		histograms1d["muHtAfter"]->Fill(taggedMuons[0].pt() + met.et());

		if(semilepRet[string("Opposite leadJetPt")])
		  {

		    histograms2d["mu2DAfter"]->Fill( dRMin, ptRel );
		    histograms1d["muHtFinal"]->Fill(taggedMuons[0].pt() + met.et());
		    TLorentzVector MET ( met.px(), 
					 met.py(), 
					 met.pz(), //filling with zero, should have an estimate of this to get it right
					 met.energy() );

		    double metDPhiMin = reco::deltaPhi<double>( closestJet->phi(), met.phi() );
		    //semileptonic histograms
		    histograms1d["muPt"]->Fill( muP.Perp() );
		    histograms1d["muPtRel"]->Fill( ptRel );
		    histograms1d["muDRMin"]->Fill( dRMin );
		    histograms1d["metDPhiMin"]->Fill(metDPhiMin);
		    histograms1d["semiLepTopMass"]->Fill((muP + bjetP + MET).M());


		    if( semilepRet[string("Hemispheric")]) {
		      pat::Jet const * closestJetPat = dynamic_cast<pat::Jet const *>(closestJet->masterClonePtr().get());
		      if (closestJetPat != NULL && closestJetPat->genJet() != 0 )
			histograms2d["semiMassVsGenPt"]->Fill( closestJetPat->genJet()->pt(), closestJet->mass() );
		      else
			edm::LogWarning("AnomalousTopology") << "No GenJet!" << std::endl;
		      //double yMax=0.0, muMax=0.0, dRMax=0.0;
		      //pat::Jet const * jet = dynamic_cast<pat::Jet const *>(wJet->masterClonePtr().get());
		      //if (jet == NULL) cout << "ERROR, crashing!\n";
		      //pat::subjetHelper(*jet, yMax, muMax, dRMax);
		      //hadronic histograms
		      SemileptonicSelection::candidate_collection::const_iterator wJet = semileptonicSelection_.getWJet();
		      if ( wJet != semileptonicSelection_.taggedJets().end() ) {
			pat::Jet const * wJetPat = dynamic_cast<pat::Jet const *>(wJet->masterClonePtr().get());
			if ( wJetPat != 0 ) {
			  boostedTopWTagFunctor_( *wJetPat, retHad);
			  double y = 0.0, mu = 0.0, dR = 0.0;
			  pat::subjetHelper( *wJetPat, y, mu, dR );
		
			  histograms1d["diffPtb1b2"]->Fill(closestJet->pt() - wJet->pt() );
			  histograms1d["diffEb1b2"]->Fill(closestJet->energy() - wJet->energy() );
			  histograms2d["Mb1VsMb2"]->Fill(closestJet->mass(), wJet->mass() );
			  histograms2d["Ptb1VsPtb2"]->Fill(closestJet->pt(), wJet->pt() );
			  histograms1d["had_w_m"]->Fill( wJet->mass() );
			  histograms1d["had_w_pt"]->Fill( wJet->pt() );
			  if ( wJet->daughter(0) != 0 ) {
			    histograms1d["had_w_m0"]->Fill( wJet->daughter(0)->mass() );
			    histograms1d["had_w_pt0"]->Fill( wJet->daughter(0)->pt() );
			  } else {
			    edm::LogWarning("AnomalousTopology") << "W0 has no daughters" << std::endl;
			    histograms1d["had_w_m0"]->Fill( -1.0 );
			    histograms1d["had_w_pt0"]->Fill( -1.0 );
			  }

			  if ( wJet->daughter(1) != 0 ) {
			    histograms1d["had_w_m1"]->Fill( wJet->daughter(1)->mass() );
			    histograms1d["had_w_pt1"]->Fill( wJet->daughter(1)->pt() );
			  } else {
			    edm::LogWarning("AnomalousTopology") << "W1 has no daughters" << std::endl;
			    histograms1d["had_w_m1"]->Fill( -1.0 );
			    histograms1d["had_w_pt1"]->Fill( -1.0 );
			  }

			  histograms1d["had_w_mu"]->Fill( mu );
			  histograms1d["had_w_y"]->Fill( y );
			  histograms1d["had_w_deltaR"]->Fill( dR );	

			  if ( wJetPat->genJet() != 0 ) 
			    histograms2d["hadMassVsGenPt"]->Fill(  wJetPat->genJet()->pt(), wJet->mass() );
			  else
			    edm::LogWarning("AnomalousTopology") << "GenJet is zero for W candidates!" << std::endl;
			} else {
			  edm::LogWarning("BadCast") << "This isn't a pat jet!" << std::endl;
			} // end if pat jet
		      }// end if valid wjet
		    }// end if hemispheric event
		  }// end if opposite leading jet pt
	      }// end if 2d cut
	    }// end if lepton has close jet
	}// end if lepton passes
    }// end if there are any muons
}// end of function
