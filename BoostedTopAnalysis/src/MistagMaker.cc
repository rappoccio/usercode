#include "Analysis/BoostedTopAnalysis/interface/MistagMaker.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"


MistagMaker::MistagMaker( edm::ParameterSet const & params, TFileDirectory & iDir ) :
  dijetSelector_         (params.getParameter<edm::ParameterSet>("jetIDParams"), 
                          params.getParameter<edm::ParameterSet>("pfJetIDParams"),
                          params.getParameter<edm::ParameterSet>("dijetSelectorParams")),
  theDir(iDir),
  boostedTopWTagFunctor_  (params.getParameter<edm::ParameterSet>("boostedTopWTagParams") ),
  wMassMin_               (params.getParameter<double>("wMassMin") ),
  wMassMax_               (params.getParameter<double>("wMassMax") ),
  ptMin_               (params.getParameter<double>("jetPtMin") )
{
  histograms1d["wTagPt"]      =   theDir.make<TH1F>("wTagPt",   "W Jet Pt",   200,    0,    1000 );
  histograms1d["probePt"]     =   theDir.make<TH1F>("probePt",  "W Jet Pt",   200,    0,    1000 );
  histograms1d["nJets"]       =   theDir.make<TH1F>("nJets",    "N Jets",     20,     0,    20  );

  histograms1d["wTagPt"]        ->  Sumw2();
  histograms1d["probePt"]       ->  Sumw2();

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

  double weight = 1.0;
  edm::Handle<GenEventInfoProduct>    genEvt;
  iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
  if( genEvt.isValid() )  {
    weight = genEvt->weight() ;
  }

  pat::strbitset jetRet = dijetSelector_.getBitTemplate();
  bool passDijet = dijetSelector_( iEvent, jetRet );

  std::vector<edm::Ptr<pat::Jet> > const & pretaggedJets = dijetSelector_.pfJets()  ;
  histograms1d["nJets"]       ->      Fill( pretaggedJets.size() );
  if( pretaggedJets.size() == 2 ) {
    bool dijet = pretaggedJets[0]->pt() > ptMin_  && pretaggedJets[1]->pt() > ptMin_;
    if( dijet ) {
      double x = flatDistribution_->fire();
      int index = x < 0.5 ? 0 : 1;
      const pat::Jet & probe( *pretaggedJets[index] );

      pat::strbitset wRet = boostedTopWTagFunctor_.getBitTemplate();
      bool pass = boostedTopWTagFunctor_ ( probe, wRet );
      bool passMass = probe.mass() > wMassMin_ && probe.mass() < wMassMax_ ;
      histograms1d["probePt"]     ->  Fill( probe.pt() , weight );
      if( pass && passMass )
        histograms1d["wTagPt"]    ->  Fill( probe.pt(), weight );
    }
  }

}

