// system include files
#include <memory>
#include <iostream>
#include <string>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "Analysis/EDSHyFT/plugins/BTagSFUtil_tprime.h"
#include "RecoBTag/Records/interface/BTagPerformanceRecord.h"
#include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h"
#include "RecoBTag/PerformanceDB/interface/BtagPerformance.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TF1.h"

class BTaggingSFProducer : public edm::EDProducer {
public:
  explicit BTaggingSFProducer(const edm::ParameterSet&);
  ~BTaggingSFProducer();
  
private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  // ----------member data --------------------------
  edm::InputTag jetSource_;
  std::string discriminatorTag_;
  double discriminatorValue_;
  std::string btagger_;
  double heavySFUncInflateBy_;
  std::string lightSFCorrFunction_;
  std::string effMapB_;
  std::string effMapC_;
  std::string effMapUDSG_;

  TF1 lightSFCorr_;

  TFile *f_EffMapB_;
  TFile *f_EffMapC_;
  TFile *f_EffMapUDSG_;

  TH2D *h2_EffMapB_;
  TH2D *h2_EffMapC_;
  TH2D *h2_EffMapUDSG_;
};

BTaggingSFProducer::BTaggingSFProducer(const edm::ParameterSet& iConfig)
{
  jetSource_= iConfig.getParameter<edm::InputTag>("JetSource");
  discriminatorTag_ = iConfig.getParameter<std::string>("DiscriminatorTag");
  discriminatorValue_ = iConfig.getParameter<double>("DiscriminatorValue");
  btagger_ = iConfig.getParameter<std::string>("BTagger");
  heavySFUncInflateBy_ = iConfig.getParameter<double>("HeavySFUncInflateBy");
  lightSFCorrFunction_ = iConfig.getParameter<std::string>("LightSFCorrFunction");
  effMapB_ = iConfig.getParameter<std::string>("EffMapB");
  effMapC_ = iConfig.getParameter<std::string>("EffMapC");
  effMapUDSG_ = iConfig.getParameter<std::string>("EffMapUDSG");
  
  lightSFCorr_ = TF1("lightSFCorr",lightSFCorrFunction_.c_str(), 0.,670.);

  edm::FileInPath fipEffMapB(effMapB_);
  edm::FileInPath fipEffMapC(effMapC_);
  edm::FileInPath fipEffMapUDSG(effMapUDSG_);

  f_EffMapB_ = new TFile(fipEffMapB.fullPath().c_str());
  f_EffMapC_ = new TFile(fipEffMapC.fullPath().c_str());
  f_EffMapUDSG_ = new TFile(fipEffMapUDSG.fullPath().c_str());

  h2_EffMapB_ = (TH2D*)f_EffMapB_->Get("efficiency");
  h2_EffMapC_ = (TH2D*)f_EffMapC_->Get("efficiency");
  h2_EffMapUDSG_ = (TH2D*)f_EffMapUDSG_->Get("efficiency");

  produces< std::vector< pat::Jet > >();
}

BTaggingSFProducer::~BTaggingSFProducer()
{
  delete f_EffMapB_;
  delete f_EffMapC_;
  delete f_EffMapUDSG_;
}

// ------------ method called to produce the data  ------------
void
BTaggingSFProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace reco;

  edm::ESHandle<BtagPerformance> perfH_Btag;
  edm::ESHandle<BtagPerformance> perfH_Mistag;

  iSetup.get<BTagPerformanceRecord>().get(("MUJETSWPBTAG" + btagger_), perfH_Btag);
  iSetup.get<BTagPerformanceRecord>().get(("MISTAG" + btagger_), perfH_Mistag);

  edm::Handle<std::vector<pat::Jet > > jetsH;
  iEvent.getByLabel(jetSource_, jetsH);

  std::auto_ptr< std::vector<pat::Jet> > jetsBtags( new std::vector<pat::Jet> (*jetsH) );

  int runNumber = iEvent.id().run();
  int eventNumber = iEvent.id().event();

  BTagSFUtil btaggingUtility( runNumber+eventNumber);
  BinningPointByMap measurePoint;

  for ( std::vector<pat::Jet>::iterator jetIt = jetsBtags->begin(); jetIt != jetsBtags->end(); ++jetIt )
  {
    // Get the mistag efficiency and the light and heavy flavour tagging scale factors
    double ScaleFactor;
    double ScaleFactor_up;
    double ScaleFactor_down;
    double ScaleFactor_unc;
    double tagEfficiency;

    measurePoint.reset();

    int parton = jetIt->partonFlavour();

    bool btag = false;
    bool btagNominal = false;
    bool btagUp = false;
    bool btagDown = false;

    if ( jetIt->bDiscriminator(discriminatorTag_.c_str()) >= discriminatorValue_ ) btag = true;

    // if b jet
    if ( abs(parton) == 5 )
    {
      double jetPt = jetIt->pt();
      if ( jetPt>670. ) jetPt = 670.;
      else if ( jetPt<30. ) jetPt = 30.;
      double jetAbsEta = fabs(jetIt->eta());
      if ( jetAbsEta>2.4 ) jetAbsEta = 2.4;

      measurePoint.insert( BinningVariables::JetEt, jetPt);
      measurePoint.insert( BinningVariables::JetEta, jetAbsEta);

      ScaleFactor     = perfH_Btag->getResult(PerformanceResult::BTAGBEFFCORR, measurePoint);
      ScaleFactor_unc = perfH_Btag->getResult(PerformanceResult::BTAGBERRCORR, measurePoint);
      if ( jetIt->pt()>670. )     ScaleFactor_unc = 2*ScaleFactor_unc;
      else if ( jetIt->pt()<30. ) ScaleFactor_unc = 0.12;

      ScaleFactor_up   = ScaleFactor + heavySFUncInflateBy_*ScaleFactor_unc;
      ScaleFactor_down = ScaleFactor - heavySFUncInflateBy_*ScaleFactor_unc;

      tagEfficiency = h2_EffMapB_->GetBinContent( h2_EffMapB_->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapB_->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }
    // if c jet
    else if ( abs(parton) == 4 )
    {
      double jetPt = jetIt->pt();
      if ( jetPt>670. ) jetPt = 670.;
      else if ( jetPt<30. ) jetPt = 30.;
      double jetAbsEta = fabs(jetIt->eta());
      if ( jetAbsEta>2.4 ) jetAbsEta = 2.4;

      measurePoint.insert( BinningVariables::JetEt, jetPt);
      measurePoint.insert( BinningVariables::JetEta, jetAbsEta);

      ScaleFactor     = perfH_Btag->getResult(PerformanceResult::BTAGBEFFCORR, measurePoint);
      ScaleFactor_unc = perfH_Btag->getResult(PerformanceResult::BTAGBERRCORR, measurePoint);
      if ( jetIt->pt()>670. )     ScaleFactor_unc = 2*ScaleFactor_unc;
      else if ( jetIt->pt()<30. ) ScaleFactor_unc = 0.12;

      ScaleFactor_up   = ScaleFactor + 2*heavySFUncInflateBy_*ScaleFactor_unc;
      ScaleFactor_down = ScaleFactor - 2*heavySFUncInflateBy_*ScaleFactor_unc;

      tagEfficiency = h2_EffMapC_->GetBinContent( h2_EffMapC_->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapC_->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }
    else
    {
      double jetPt = jetIt->pt();
      if ( jetPt>670. ) jetPt = 670.;
      double jetAbsEta = fabs(jetIt->eta());
      if ( jetAbsEta>2.4 ) jetAbsEta = 2.4;

      measurePoint.insert( BinningVariables::JetEt, jetPt);
      measurePoint.insert( BinningVariables::JetEta, jetAbsEta);

      ScaleFactor = lightSFCorr_.Eval(jetPt)*perfH_Mistag->getResult(PerformanceResult::BTAGLEFFCORR, measurePoint);
      // here, we need to keep the relative uncertainties unchanged
      ScaleFactor_unc = (perfH_Mistag->getResult(PerformanceResult::BTAGLERRCORR, measurePoint))/(perfH_Mistag->getResult(PerformanceResult::BTAGLEFFCORR, measurePoint));
      if ( jetIt->pt()>670. ) ScaleFactor_unc = 2*ScaleFactor_unc;

      ScaleFactor_up   = ScaleFactor + ScaleFactor_unc*ScaleFactor;
      ScaleFactor_down = ScaleFactor - ScaleFactor_unc*ScaleFactor;

      tagEfficiency = h2_EffMapUDSG_->GetBinContent( h2_EffMapUDSG_->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapUDSG_->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }

    btagNominal = btaggingUtility.applySF( btag, ScaleFactor, tagEfficiency);
    btagUp = btaggingUtility.applySF( btag, ScaleFactor_up, tagEfficiency);
    btagDown = btaggingUtility.applySF( btag, ScaleFactor_down, tagEfficiency);

    int btaggingSummary = 1*btag + 2*btagNominal + 4*btagUp + 8*btagDown;

    jetIt->addUserInt("btagRegular", btaggingSummary);
  }

  // put jets into event
  iEvent.put(jetsBtags);
}

// ------------ method called once each job just before starting event loop  ------------
void
BTaggingSFProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
BTaggingSFProducer::endJob() {
  

}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingSFProducer);
