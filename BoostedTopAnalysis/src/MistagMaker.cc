#include "Analysis/BoostedTopAnalysis/interface/MistagMaker.h"

MistagMaker::MistagMaker( edm::ParameterSet const & params, TFileDirectory & iDir ) :
  dijetSelector_         (params.getParameter<edm::ParameterSet>("jetIDParams"), 
                          params.getParameter<edm::ParameterSet>("pfJetIDParams"),
                          params.getParameter<edm::ParameterSet>("dijetSelectorParams")),
  theDir(iDir)
{
  histograms1d["wTagPt"]      =   theDir.make<TH1F>("wTagPt",   "W Jet Pt",   200,    0,    1000 );
  histograms1d["probePt"]     =   theDir.make<TH1F>("probePt",  "W Jet Pt",   200,    0,    1000 );

  edm::Service<edm::RandomNumberGenerator> rng;
  if ( ! rng.isAvailable()) {
    throw cms::Exception("Configuration")
      << "Module requires the RandomNumberGeneratorService\n";
  }

  CLHEP::HepRandomEngine& engine = rng->getEngine();
  flatDistribution_ = new CLHEP::RandFlat(engine, 0., 1.);


}

void MistagMaker::analyze( const edm::EventBase & iEvent )
{

  pat::strbitset jetRet = dijetSelector_.getBitTemplate();
  bool passDijet = dijetSelector_( iEvent, jetRet );

  std::vector<edm::Ptr<pat::Jet> > const & pretaggedJets = dijetSelector_.pfJets()  ;
  cout<<pretaggedJets.size()<<endl;

}

