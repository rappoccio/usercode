#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"


using namespace std;


HadronicAnalysis::HadronicAnalysis(const edm::ParameterSet& iConfig, TFileDirectory& iDir) :
  hadronicSelection_(iConfig.getParameter<edm::ParameterSet>("hadronicAnalysis")),
  theDir(iDir)
{
  std::cout << "Instantiated HadronicAnalysis" << std::endl;
  histograms1d["dijetMass"] = theDir.make<TH1F>("dijetMass", "Dijet Mass", 500, 0, 5000);
  histograms1d["dijetMassSingleTagged"] = theDir.make<TH1F>("dijetMassSingleTagged", "Dijet Mass, Single Tagged", 500, 0, 5000);
  histograms1d["dijetMassDoubleTagged"] = theDir.make<TH1F>("dijetMassDoubleTagged", "Dijet Mass, Double Tagged", 500, 0, 5000);

  histograms1d["jetMass0"] = theDir.make<TH1F>("jetMass0", "Jet Mass of First Jet", 500, 0, 250 );
  histograms1d["jetMass1"] = theDir.make<TH1F>("jetMass1", "Jet Mass of Second Jet", 500, 0, 250 );
  histograms1d["mu0"]     = theDir.make<TH1F>("mu0", "Mass Drop of First Jet", 500, 0.0, 1.0 );
  histograms1d["mu1"]     = theDir.make<TH1F>("mu1", "Mass Drop of Second Jet", 500, 0.0, 1.0 );
  histograms1d["y0"]     = theDir.make<TH1F>("y0", "Asymmetry of First Jet", 500, 0.0, 1.0 );
  histograms1d["y1"]     = theDir.make<TH1F>("y1", "Asymmetry of Second Jet", 500, 0.0, 1.0 );
  histograms1d["dR0"]     = theDir.make<TH1F>("dR0", "#Delta R of First Jet", 500, 0.0, 1.0 );
  histograms1d["dR1"]     = theDir.make<TH1F>("dR1", "#Delta R of Second Jet", 500, 0.0, 1.0 );

  histograms2d["jetMassVsPt0"] = theDir.make<TH2F>("jetMassVsPt0", "First Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["jetMassVsPt1"] = theDir.make<TH2F>("jetMassVsPt1", "Second Jet Mass Versus Jet Pt", 50, 0, 500, 50, 0, 250 );
  histograms2d["muVsPt0"]     = theDir.make<TH2F>("muVsPt0", "Mass Drop of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["muVsPt1"]     = theDir.make<TH2F>("muVsPt1", "Mass Drop of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["yVsPt0"]     = theDir.make<TH2F>("yVsPt0", "Asymmetry of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["yVsPt1"]     = theDir.make<TH2F>("yVsPt1", "Asymmetry of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt0"]     = theDir.make<TH2F>("dRVsPt0", "#Delta R of First Jet", 50, 0, 500, 50, 0.0, 1.0 );
  histograms2d["dRVsPt1"]     = theDir.make<TH2F>("dRVsPt1", "#Delta R of Second Jet", 50, 0, 500, 50, 0.0, 1.0 );
}

void HadronicAnalysis::analyze(const edm::EventBase& iEvent)
{
  pat::strbitset ret = hadronicSelection_.getBitTemplate();
  bool pass = hadronicSelection_(iEvent, ret);

  if ( ret[std::string("Jet Preselection")] ) {
    std::vector<edm::Ptr<pat::Jet> > const & pretaggedJets = hadronicSelection_.pretaggedJets();

    if ( pretaggedJets.size() >= 2 ) {
      reco::Candidate::LorentzVector p4_0( pretaggedJets[0]->p4() );
      reco::Candidate::LorentzVector p4_1( pretaggedJets[1]->p4() );

      reco::Candidate::LorentzVector p4 = p4_0 + p4_1;

      double mu0 = 0.0, y0 = 0.0, dR0 = 0.0;
      pat::subjetHelper( *pretaggedJets[0], y0, mu0, dR0);
      double mu1 = 0.0, y1 = 0.0, dR1 = 0.0;
      pat::subjetHelper( *pretaggedJets[1], y1, mu1, dR1);	  


      histograms1d["dijetMass"]->Fill( p4.mass() );
      histograms1d["jetMass0"]->Fill( pretaggedJets[0]->mass() );
      histograms1d["mu0"]->Fill(mu0);
      histograms1d["y0"]->Fill(y0);
      histograms1d["dR0"]->Fill(dR0);
      histograms2d["jetMassVsPt0"]->Fill( pretaggedJets[0]->pt(), pretaggedJets[0]->mass() );
      histograms2d["muVsPt0"]->Fill(pretaggedJets[0]->pt(), mu0);
      histograms2d["yVsPt0"]->Fill(pretaggedJets[0]->pt(), y0);
      histograms2d["dRVsPt0"]->Fill(pretaggedJets[0]->pt(), dR0);

      histograms1d["jetMass1"]->Fill( pretaggedJets[1]->mass() );
      histograms1d["mu1"]->Fill(mu1);
      histograms1d["y1"]->Fill(y1);
      histograms1d["dR1"]->Fill(dR1);
      histograms2d["jetMassVsPt1"]->Fill( pretaggedJets[1]->pt(), pretaggedJets[1]->mass() );
      histograms2d["muVsPt1"]->Fill(pretaggedJets[1]->pt(), mu1);
      histograms2d["yVsPt1"]->Fill(pretaggedJets[1]->pt(), y1);
      histograms2d["dRVsPt1"]->Fill(pretaggedJets[1]->pt(), dR1);
    
      if ( ret ) {
	std::vector<edm::Ptr<pat::Jet> > const & taggedJets = hadronicSelection_.taggedJets();

	if ( taggedJets.size() >= 1 ) {
	  histograms1d["dijetMassSingleTagged"]->Fill( p4.mass() );

	  if ( taggedJets.size() >= 2 ) {	    
	    histograms1d["dijetMassDoubleTagged"]->Fill( p4.mass() );
	  }
	}
      }
    }
  }
}
