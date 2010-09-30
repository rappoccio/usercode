#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetType22Selection.h"

WPlusBJetType22Selection::WPlusBJetType22Selection ( edm::ParameterSet const & params ) :
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
  push_back(">= 1 WJet");
  push_back(">= 2 WJet");
  push_back("wMassCut");
  push_back("has Tight Top");
  push_back("hasTwoTops");
  push_back("topMassCut");

  //turn on bit
  set("Inclusive");
  set("Trigger");
  set("Leading Jet Pt");
  set(">= 1 WJet");
  set(">= 2 WJet");
  set("wMassCut");
  set("has Tight Top");
  set("hasTwoTops");
  set("topMassCut");

}

bool WPlusBJetType22Selection::operator()( edm::EventBase const & t, pat::strbitset & ret )
{
  //turn off and clear container
  ret.set(false);
  tightTop0_ = false;
  tightTop1_ = false;
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

  pat::strbitset tret = twPlusBJetSelection_.getBitTemplate();
  //Analyze the towards direction
  bool tpassWPlusBJet  = twPlusBJetSelection_( t, theJet->p4(), tret, true );

  pat::strbitset oret = owPlusBJetSelection_.getBitTemplate();
  //Analyze the opposite direction
  bool opassWPlusBJet  = owPlusBJetSelection_( t, theJet->p4(), oret, false );


  std::vector<edm::Ptr<pat::Jet> >  const & tWJets = twPlusBJetSelection_.wJets();
  std::vector<edm::Ptr<pat::Jet> >  const & oWJets = owPlusBJetSelection_.wJets();
  std::vector<edm::Ptr<pat::Jet> >  const & tbJets = twPlusBJetSelection_.bJets();
  std::vector<edm::Ptr<pat::Jet> >  const & obJets = owPlusBJetSelection_.bJets();
  edm::Ptr<pat::Jet> const & taJet = twPlusBJetSelection_.aJet();
  edm::Ptr<pat::Jet> const & oaJet = owPlusBJetSelection_.aJet();

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

      int numWJets = 0;
      int numBJets = 0;
      if( tWJets.size() >= 1 )  numWJets++;
      if( oWJets.size() >= 1 )  numWJets++;
      if( tbJets.size() >= 1 )  numBJets++;
      if( obJets.size() >= 1 )  numBJets++;

      if( ignoreCut(">= 1 WJet") || numWJets >= 1 ) {
        passCut( ret, ">= 1 WJet" );
        if( ignoreCut(">= 2 WJet") || numWJets >= 2 ) {
          passCut( ret, ">= 2 WJet" );
          
          //Get W mass
          double wMass0 = tWJets.at(0)->mass();
          double wMass1 = oWJets.at(0)->mass();
          bool passWMass = ( wMass0 > wMassMin_ && wMass0 < wMassMax_ && wMass1 > wMassMin_ && wMass1 < wMassMax_ );
          if( ignoreCut("wMassCut") || passWMass ) {
            passCut( ret, "wMassCut" );
            if( ignoreCut("has Tight Top") || numBJets >= 1 ) {
              passCut( ret, "has Tight Top" );

              bool hasTop0 = false, hasTop1 = false;
              if( tbJets.size() >= 1 ) {
                p4_top0_ = tWJets.at(0)->p4() + tbJets.at(0)->p4()  ;
                tightTop0_ = true;
                hasTop0 = true;
              }
              else if( twPlusBJetSelection_.aJetFound() )  {
                p4_top0_ = tWJets.at(0)->p4() + taJet->p4();
                tightTop0_ = false;
                hasTop0 = true;
              }
              if( obJets.size() >= 1 ) {
                p4_top1_ = oWJets.at(0)->p4() + obJets.at(0)->p4()  ;
                tightTop1_ = true;
                hasTop1 = true;
              }
              else if( owPlusBJetSelection_.aJetFound() ) {
                p4_top1_ = oWJets.at(0)->p4() + oaJet->p4();
                tightTop1_ = false;
                hasTop1 = true;
              }

              bool hasTwoTops = hasTop0 && hasTop1 ;
              if( ignoreCut("hasTwoTops") || hasTwoTops ) {
                passCut( ret, "hasTwoTops" );

                double topMass0 = p4_top0_.mass();
                double topMass1 = p4_top1_.mass();
                double passTopMass = ( topMass0 > topMassMin_ && topMass0 < topMassMax_ && topMass1 > topMassMin_ && topMass1 < topMassMax_ );
                if( ignoreCut("topMassCut") || passTopMass ) {
                  passCut( ret, "topMassCut" );
                  //cout<<"Top Mass 0 "<<topMass0<<endl;
                  //cout<<"Top Mass 1 "<<topMass1<<endl;
                } // topMassCut
              }// hasTwoTops
            } // has Tight Top
          } // wMassCut
        }  // >= 2 WJet
      }  // >= 1 WJet
    } // Leading Jet Pt
  }  // pass trigger

  return (bool)ret;


}
