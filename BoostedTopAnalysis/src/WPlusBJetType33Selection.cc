#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetType33Selection.h"

WPlusBJetType33Selection::WPlusBJetType33Selection ( edm::ParameterSet const & params ) :
  jetTag_               (params.getParameter<edm::InputTag>("jetSrc") ),
  trigSrc_              (params.getParameter<edm::InputTag>("trigSrc") ),
  trig_                 (params.getParameter<std::string>("trig") ),
  leadJetPtCut_         (params.getParameter<double>( "leadJetPtCut" ) ),
  wMassMin_             (params.getParameter<double>("wMassMin") ),
  wMassMax_             (params.getParameter<double>("wMassMax") ),
  topMassMin_           (params.getParameter<double>("topMassMin") ) ,
  topMassMax_           (params.getParameter<double>("topMassMax") ),
  twPlusBJetSelection_  (params.getParameter<edm::ParameterSet>("WPlusBJetSelection") ),
  owPlusBJetSelection_  (twPlusBJetSelection_)
{
  //make the bitset
  push_back("Inclusive");
  push_back("Trigger");
  push_back("Leading Jet Pt");
  push_back(">= 1 bJet");
  push_back(">= 2 bJet");
  push_back("hasMinPair0");
  push_back("hasMinPair1");
  push_back("minPairMassCut");
  push_back("topMassCut");

  //turn on bit
  set("Inclusive");
  set("Trigger");
  set("Leading Jet Pt");
  set(">= 1 bJet");
  set(">= 2 bJet");
  set("hasMinPair0");
  set("hasMinPair1");
  set("minPairMassCut");
  set("topMassCut");

}

bool WPlusBJetType33Selection::operator()( edm::EventBase const & t, pat::strbitset & ret )
{
  //turn off and clear container
  ret.set(false);
  pfJets_.clear();

  p4_top0_ = reco::Candidate::LorentzVector(0,0,0,0);
  p4_top1_ = reco::Candidate::LorentzVector(0,0,0,0);

  passCut( ret, "Inclusive" );

  edm::Handle<vector<pat::Jet>  >   jetHandle;
  t.getByLabel( jetTag_, jetHandle );

  const boost::shared_ptr<PFJetIDSelectionFunctor> & pfJetSel = twPlusBJetSelection_.pfJetSel();
  pat::strbitset retPFJet = pfJetSel->getBitTemplate();

  const pat::Jet * theJet;
  for( vector<pat::Jet>::const_iterator jetBegin=jetHandle->begin(), jetEnd=jetHandle->end(), ijet=jetBegin ;
    ijet!=jetEnd; ijet++ )
  {
    retPFJet.set(false);
    bool passJetID = (*pfJetSel)( *ijet, retPFJet );
    if( passJetID ) {
      pfJets_.push_back( edm::Ptr<pat::Jet>(jetHandle, ijet-jetBegin )  );
    }
  } // end ijet

  if( pfJets_.size() < 1 )   return false;
  theJet = &(*pfJets_.at(0));

  //Get the trigger
  edm::Handle<pat::TriggerEvent>  triggerEvent;
  t.getByLabel( trigSrc_, triggerEvent);
  if( !triggerEvent.isValid() )   return (bool)ret;

  // Check the trigger requirement
  pat::TriggerEvent const * trig = &*triggerEvent;

  bool passTrig = false;
  if( trig->wasRun() && trig->wasAccept() ) {
    pat::TriggerPath const * jetPath = trig->path(trig_);
    if( jetPath != 0 && jetPath->wasAccept() )  {
      passTrig = true;
    }
  }

  if( ignoreCut( "Trigger" ) || passTrig )  {
    passCut( ret, "Trigger" );

    if( ignoreCut( "Leading Jet Pt" ) || theJet->pt() > leadJetPtCut_ ) {
      passCut( ret, "Leading Jet Pt" );

      pat::strbitset tret = twPlusBJetSelection_.getBitTemplate();
      //Analyze the towards direction
      bool tpassWPlusBJet  = twPlusBJetSelection_( t, theJet->p4(), tret, true );

      pat::strbitset oret = owPlusBJetSelection_.getBitTemplate();
      //Analyze the opposite direction
      bool opassWPlusBJet  = owPlusBJetSelection_( t, theJet->p4(), oret, false );

      std::vector<edm::Ptr<pat::Jet> >  const & tbJets = twPlusBJetSelection_.bJets();
      std::vector<edm::Ptr<pat::Jet> >  const & obJets = owPlusBJetSelection_.bJets();
      std::vector<edm::Ptr<pat::Jet> >  const & tMinDrPair = twPlusBJetSelection_.minDrPair();
      std::vector<edm::Ptr<pat::Jet> >  const & oMinDrPair = owPlusBJetSelection_.minDrPair();

      int numBJets = 0;
      if( tbJets.size() >= 1 )  numBJets++;
      if( obJets.size() >= 1 )  numBJets++;

      if( ignoreCut(">= 1 bJet") || numBJets >= 1 ) {
        passCut( ret, ">= 1 bJet" );
        if( ignoreCut(">= 2 bJet") || numBJets >= 2 ) {
          passCut(ret, ">= 2 bJet");
          bool hasMinPair0 = tMinDrPair.size()==2 ;
          bool hasMinPair1 = oMinDrPair.size()==2 ;
          if( ignoreCut("hasMinPair0") || hasMinPair0 ) {
            passCut( ret, "hasMinPair0" );
            if( ignoreCut("hasMinPair1") || hasMinPair1 ) {
              passCut( ret, "hasMinPair1" );

              p4_top0_  = tbJets.at(0)->p4() + tMinDrPair.at(0)->p4() + tMinDrPair.at(1)->p4();
              double minPairMass0 = (tMinDrPair.at(0)->p4() + tMinDrPair.at(1)->p4()).mass();
              p4_top1_  = obJets.at(0)->p4() + oMinDrPair.at(0)->p4() + oMinDrPair.at(1)->p4();
              double minPairMass1 = (oMinDrPair.at(0)->p4() + oMinDrPair.at(1)->p4()).mass();

              bool passMinPairMass = ( minPairMass0 > wMassMin_ && minPairMass0 < wMassMax_ && minPairMass1 > wMassMin_ && minPairMass1 < wMassMax_ );
              if( ignoreCut("minPairMassCut") || passMinPairMass ) {
                passCut( ret, "minPairMassCut" );

                double topMass0 = p4_top0_.mass();
                double topMass1 = p4_top1_.mass();
                double passTopMass = ( topMass0 > topMassMin_ && topMass0 < topMassMax_ && topMass1 > topMassMin_ && topMass1 < topMassMax_ );
                if( ignoreCut("topMassCut") || passTopMass ) {
                  passCut( ret, "topMassCut" );
                  //cout<<"Top Mass 0 "<<topMass0<<endl;
                  //cout<<"Top Mass 1 "<<topMass1<<endl;
                } // topMassCut
              } // minPairMassCut
            } // hasMinPair1
          } // hasMinPair0
        } // >= 2 bJet
      }  // >= 1 bJet
    } // Leading Jet Pt
  }  // pass trigger

  return (bool)ret;


}
