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
  std::string effMapFile_;

  TF1  *CSVM_SFb_0to2p4;
  TH1D *CSVM_SFb_errors;

  TF1 *CSVM_SFl_0to2p4;
  TF1 *CSVM_SFl_0to0p8;
  TF1 *CSVM_SFl_0p8to1p6;
  TF1 *CSVM_SFl_1p6to2p4;

  TF1 *CSVM_SFl_0to2p4_min;
  TF1 *CSVM_SFl_0to0p8_min;
  TF1 *CSVM_SFl_0p8to1p6_min;
  TF1 *CSVM_SFl_1p6to2p4_min;

  TF1 *CSVM_SFl_0to2p4_max;
  TF1 *CSVM_SFl_0to0p8_max;
  TF1 *CSVM_SFl_0p8to1p6_max;
  TF1 *CSVM_SFl_1p6to2p4_max;

  TFile *f_EffMap;

  TH2D *h2_EffMapB;
  TH2D *h2_EffMapC;
  TH2D *h2_EffMapUDSG;
};

BTaggingSFProducer::BTaggingSFProducer(const edm::ParameterSet& iConfig)
{
  jetSource_= iConfig.getParameter<edm::InputTag>("JetSource");
  discriminatorTag_ = iConfig.getParameter<std::string>("DiscriminatorTag");
  discriminatorValue_ = iConfig.getParameter<double>("DiscriminatorValue");
  effMapFile_ = iConfig.getParameter<std::string>("EffMapFile");

  double PtBins[] = {20, 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 600, 800};

  CSVM_SFb_0to2p4 = new TF1("CSVM_SFb_0to2p4","0.726981*((1.+(0.253238*x))/(1.+(0.188389*x)))", 20.,800.);

  CSVM_SFb_errors = new TH1D("CSVM_SFb_errors", "CSVM_SFb_errors", 16, PtBins);
  CSVM_SFb_errors->SetBinContent( 0,(2*0.0554504));
  CSVM_SFb_errors->SetBinContent( 1,0.0554504);
  CSVM_SFb_errors->SetBinContent( 2,0.0209663);
  CSVM_SFb_errors->SetBinContent( 3,0.0207019);
  CSVM_SFb_errors->SetBinContent( 4,0.0230073);
  CSVM_SFb_errors->SetBinContent( 5,0.0208719);
  CSVM_SFb_errors->SetBinContent( 6,0.0200453);
  CSVM_SFb_errors->SetBinContent( 7,0.0264232);
  CSVM_SFb_errors->SetBinContent( 8,0.0240102);
  CSVM_SFb_errors->SetBinContent( 9,0.0229375);
  CSVM_SFb_errors->SetBinContent(10,0.0184615);
  CSVM_SFb_errors->SetBinContent(11,0.0216242);
  CSVM_SFb_errors->SetBinContent(12,0.0248119);
  CSVM_SFb_errors->SetBinContent(13,0.0465748);
  CSVM_SFb_errors->SetBinContent(14,0.0474666);
  CSVM_SFb_errors->SetBinContent(15,0.0718173);
  CSVM_SFb_errors->SetBinContent(16,0.0717567);
  CSVM_SFb_errors->SetBinContent(17,(2*0.0717567));

  // light flavor SFs are provided separately for 2012 data taking periods AB, C, and D as well as full ABCD. Values used here correspond to the full period ABCD
  CSVM_SFl_0to0p8 =   new TF1("CSVM_SFl_0to0p8","((1.06238+(0.00198635*x))+(-4.89082e-06*(x*x)))+(3.29312e-09*(x*(x*x)))", 20.,800.);
  CSVM_SFl_0p8to1p6 = new TF1("CSVM_SFl_0p8to1p6","((1.08048+(0.00110831*x))+(-2.96189e-06*(x*x)))+(2.16266e-09*(x*(x*x)))", 20.,800.);
  CSVM_SFl_1p6to2p4 = new TF1("CSVM_SFl_1p6to2p4","((1.09145+(0.000687171*x))+(-2.45054e-06*(x*x)))+(1.7844e-09*(x*(x*x)))", 20.,700.);

  CSVM_SFl_0to0p8_min =   new TF1("CSVM_SFl_0to0p8_min","((0.972746+(0.00104424*x))+(-2.36081e-06*(x*x)))+(1.53438e-09*(x*(x*x)))", 20.,800.);
  CSVM_SFl_0p8to1p6_min = new TF1("CSVM_SFl_0p8to1p6_min","((0.9836+(0.000649761*x))+(-1.59773e-06*(x*x)))+(1.14324e-09*(x*(x*x)))", 20.,800.);
  CSVM_SFl_1p6to2p4_min = new TF1("CSVM_SFl_1p6to2p4_min","((1.00616+(0.000358884*x))+(-1.23768e-06*(x*x)))+(6.86678e-10*(x*(x*x)))", 20.,700.);

  CSVM_SFl_0to0p8_max =   new TF1("CSVM_SFl_0to0p8_max","((1.15201+(0.00292575*x))+(-7.41497e-06*(x*x)))+(5.0512e-09*(x*(x*x)))", 20.,800.);
  CSVM_SFl_0p8to1p6_max = new TF1("CSVM_SFl_0p8to1p6_max","((1.17735+(0.00156533*x))+(-4.32257e-06*(x*x)))+(3.18197e-09*(x*(x*x)))", 20.,800.);
  CSVM_SFl_1p6to2p4_max = new TF1("CSVM_SFl_1p6to2p4_max","((1.17671+(0.0010147*x))+(-3.66269e-06*(x*x)))+(2.88425e-09*(x*(x*x)))", 20.,700.);

  edm::FileInPath fipEffMap(effMapFile_);

  f_EffMap = new TFile(fipEffMap.fullPath().c_str());

  h2_EffMapB    = (TH2D*)f_EffMap->Get("efficiency_b");
  h2_EffMapC    = (TH2D*)f_EffMap->Get("efficiency_c");
  h2_EffMapUDSG = (TH2D*)f_EffMap->Get("efficiency_udsg");

  produces< std::vector< pat::Jet > >();
}

BTaggingSFProducer::~BTaggingSFProducer()
{
}

// ------------ method called to produce the data  ------------
void
BTaggingSFProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace reco;

  edm::Handle<std::vector<pat::Jet > > jetsH;
  iEvent.getByLabel(jetSource_, jetsH);

  std::auto_ptr< std::vector<pat::Jet> > jetsBtags( new std::vector<pat::Jet> (*jetsH) );

  int runNumber = iEvent.id().run();
  int eventNumber = iEvent.id().event();

  BTagSFUtil btaggingUtility( runNumber+eventNumber );

  // b-tagging scale factors are applied following the BTV POG recommendations (https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagPOG)
  for ( std::vector<pat::Jet>::iterator jetIt = jetsBtags->begin(); jetIt != jetsBtags->end(); ++jetIt )
  {
    double ScaleFactor;
    double ScaleFactor_up;
    double ScaleFactor_down;
    double ScaleFactor_unc;
    double tagEfficiency;

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
      if ( jetPt>800. ) jetPt = 800.;
      else if ( jetPt<20. ) jetPt = 20.;

      ScaleFactor     = CSVM_SFb_0to2p4->Eval(jetPt);
      ScaleFactor_unc = CSVM_SFb_errors->GetBinContent(CSVM_SFb_errors->GetXaxis()->FindBin(jetIt->pt()));

      ScaleFactor_up   = ScaleFactor + ScaleFactor_unc;
      ScaleFactor_down = ScaleFactor - ScaleFactor_unc;

      tagEfficiency = h2_EffMapB->GetBinContent( h2_EffMapB->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapB->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }
    // if c jet
    else if ( abs(parton) == 4 )
    {
      double jetPt = jetIt->pt();
      if ( jetPt>800. ) jetPt = 800.;
      else if ( jetPt<20. ) jetPt = 20.;

      ScaleFactor     = CSVM_SFb_0to2p4->Eval(jetPt);
      ScaleFactor_unc = CSVM_SFb_errors->GetBinContent(CSVM_SFb_errors->GetXaxis()->FindBin(jetIt->pt()));

      ScaleFactor_up   = ScaleFactor + 2*ScaleFactor_unc;
      ScaleFactor_down = ScaleFactor - 2*ScaleFactor_unc;

      tagEfficiency = h2_EffMapC->GetBinContent( h2_EffMapC->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapC->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }
    // if light flavor
    else
    {
      double jetPt = jetIt->pt();
      double jetAbsEta = fabs(jetIt->eta());
      if ( jetAbsEta<1.6 && jetPt>800. ) jetPt = 800.;
      else if ( jetAbsEta>=1.6 && jetPt>700. ) jetPt = 700.;
      else if ( jetPt<20. ) jetPt = 20.;

      if(jetAbsEta<0.8)
      {
        ScaleFactor      = CSVM_SFl_0to0p8->Eval(jetPt);
        ScaleFactor_up   = ScaleFactor + ( jetIt->pt()>800. ? 2. : 1. )*(CSVM_SFl_0to0p8_max->Eval(jetPt) - CSVM_SFl_0to0p8->Eval(jetPt));
        ScaleFactor_down = ScaleFactor + ( jetIt->pt()>800. ? 2. : 1. )*(CSVM_SFl_0to0p8_min->Eval(jetPt) - CSVM_SFl_0to0p8->Eval(jetPt));
      }
      else if(jetAbsEta>=0.8 && jetAbsEta<1.6)
      {
        ScaleFactor      = CSVM_SFl_0p8to1p6->Eval(jetPt);
        ScaleFactor_up   = ScaleFactor + ( jetIt->pt()>800. ? 2. : 1. )*(CSVM_SFl_0p8to1p6_max->Eval(jetPt) - CSVM_SFl_0p8to1p6->Eval(jetPt));
        ScaleFactor_down = ScaleFactor + ( jetIt->pt()>800. ? 2. : 1. )*(CSVM_SFl_0p8to1p6_min->Eval(jetPt) - CSVM_SFl_0p8to1p6->Eval(jetPt));
      }
      else
      {
        ScaleFactor      = CSVM_SFl_1p6to2p4->Eval(jetPt);
        ScaleFactor_up   = ScaleFactor + ( jetIt->pt()>700. ? 2. : 1. )*(CSVM_SFl_1p6to2p4_max->Eval(jetPt) - CSVM_SFl_1p6to2p4->Eval(jetPt));
        ScaleFactor_down = ScaleFactor + ( jetIt->pt()>700. ? 2. : 1. )*(CSVM_SFl_1p6to2p4_min->Eval(jetPt) - CSVM_SFl_1p6to2p4->Eval(jetPt));
      }

      tagEfficiency = h2_EffMapUDSG->GetBinContent( h2_EffMapUDSG->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapUDSG->GetYaxis()->FindBin(fabs(jetIt->eta())) );
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
BTaggingSFProducer::endJob()
{
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingSFProducer);
