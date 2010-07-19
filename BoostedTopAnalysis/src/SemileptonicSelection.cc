#include "Analysis/BoostedTopAnalysis/interface/SemileptonicSelection.h"
#include "TLorentzVector.h"
#include <iostream>

//using namespace std;
using std::vector;
using std::cout;
using std::map;
using std::endl;
using std::string;

SemileptonicSelection::SemileptonicSelection( edm::ParameterSet const & params ) :
  wPlusJets_(params.getParameter<edm::ParameterSet>("WPlusJetsParams")),
  taggedMuons_(),
  taggedJets_(),
  taggedMETs_(),
  wJet(),
  closestJet(),
  dRMin(TMath::Pi()/3),
  nJetsA(0),
  nJetsB(0),
  nJetsC(0),
  jetSrc(params.getParameter<edm::InputTag>("jetSrc")),
  ptRelMin(params.getParameter<double>("ptRelMin")),
  dRMinCut(params.getParameter<double>("dRMin")),
  oppLeadJetPt(params.getParameter<double>("oppLeadJetPt")),
  leadJetPt(params.getParameter<double>("leadJetPt"))
{
  // std::cout << "Instantiated SemileptonicSelection" << std::endl;
  // make the bitset
  push_back("Inclusive");
  push_back("Trigger");
  push_back("Lepton + Jets");
  push_back("Lepton has close jet");
  push_back("Relative Pt and Min Delta R");
  push_back("Opposite leadJetPt");
  push_back("Passed Semileptonic Side");
  // all on by default
  set("Inclusive");
  set("Trigger");
  set("Lepton + Jets");
  set("Opposite leadJetPt");
  set("Lepton has close jet");
  set("Relative Pt and Min Delta R");
  set("Passed Semileptonic Side");

  if ( params.exists("cutsToIgnore") )
    setIgnoredCuts( params.getParameter<vector<string> >("cutsToIgnore") );

  // initialize bitsets for later
  retSemi = wPlusJets_.getBitTemplate();
  //retHad  = boostedTopWTagFunctor_.getBitTemplate();
  retInt = getBitTemplate();
}

bool SemileptonicSelection::operator() ( edm::EventBase const & event, pat::strbitset & ret)
{
  static int nev = 0;
  nev++;
  // fail everything by default
  ret.set(false);
  retSemi.set(false);
  //retHad.set(false);
  // tagged objects are const references, so they're handled by the
  // selector that owns them

  taggedMuons_.clear();
  taggedJets_.clear();
  //  taggedMETs_.clear();

  passCut(ret,"Inclusive");
  if(ignoreCut("Trigger")) 
    wPlusJets_.set("Trigger", false);

  /*bool passedSemi = */wPlusJets_(event, retSemi);
  // ignoreCut isn't needed here, but it doesn't hurt to be pedantic
  if( ignoreCut("Trigger") || retSemi[string("Trigger")]) passCut(ret, "Trigger");

  //not sure if this is the way to handle this, but we need more than
  //one lepton to continue, otherwise we'll get memory problems.  Is
  //there a way to enforce that a cut is turned on??
  if(ignoreCut("Lepton + Jets")) passCut(ret, "Lepton + Jets");

  if ( retSemi[string("== 1 Lepton")] && retSemi[string(">=2 Jets")]  ) 
    {
      taggedMuons_     = wPlusJets_.selectedMuons();
      taggedJets_      = wPlusJets_.selectedJets();
      taggedMETs_      = wPlusJets_.selectedMET();
      if(taggedMuons_.size()*taggedJets_.size() != 0)
	{
	  passCut(ret, string("Lepton + Jets"));
	  dRMin = TMath::Pi() / 3.0;
	  closestJet = taggedJets_.end();
	  bool leadJetCut = false;
	  bool oppLeadJetCut = false;
	  for ( vector<reco::ShallowClonePtrCandidate>::const_iterator ijet = taggedJets_.begin(),
		  taggedJets_Begin = taggedJets_.begin(), taggedJets_End = taggedJets_.end();
		ijet != taggedJets_End; ++ijet ) 
	    {
	      if( fabs(reco::deltaPhi<double>(ijet->phi(), taggedMuons_[0].phi()) < TMath::Pi()/3 ))
		nJetsA++;
	      else if (fabs(reco::deltaPhi<double>(ijet->phi(), taggedMuons_[0].phi())) > 2*TMath::Pi()/3 )
		{
		  oppLeadJetCut = (ijet->pt() > leadJetPt );
		  nJetsB++;
		}
	      else 
		nJetsC++;
	      double dR = reco::deltaR<double>(ijet->eta(), ijet->phi(),
					       taggedMuons_[0].eta(), taggedMuons_[0].phi() );
	      if ( dR < dRMin ) 
		{
		  dRMin = dR;
		  closestJet = ijet;
		}
	    }
	  if ( closestJet != taggedJets_.end() || ignoreCut("Lepton has close jet"))  
	    {
	      passCut(ret, "Lepton has close jet");
	      TLorentzVector muP ( taggedMuons_[0].px(),
				   taggedMuons_[0].py(),
				   taggedMuons_[0].pz(),
				   taggedMuons_[0].energy() );

	      TLorentzVector bjetP ( closestJet->px(),
				     closestJet->py(),
				     closestJet->pz(),
				     closestJet->energy() );


	      double ptRel = TMath::Abs( muP.Perp( bjetP.Vect() ) );
	      bool dRandPtCut = !(ptRel < ptRelMin && dRMin < dRMinCut);
	      if(dRandPtCut ||  ignoreCut("Relative Pt and Min Delta R") )
		{
		  passCut(ret, "Relative Pt and Min Delta R");
		  if( oppLeadJetCut || ignoreCut("Opposite leadJetPt") || ignoreCut("Passed Semileptonic Side"))
		    {
		      passCut(ret, "Opposite leadJetPt");
		      passCut(ret, "Passed Semileptonic Side");
		    }//if(!oppLeadJetCut)
		} // dRandPtCut 
	    } //if ( closestJet != taggedJets_.end() )  
	}//if(taggedMuons_.size()*taggedJets_.size() == 0)

    } //if passed semileptonic

  return (bool)ret;
}

