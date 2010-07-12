#ifndef Analysis_BoostedTopEventHypothesis_h
#define Analysis_BoostedTopEventHypothesis_h


#include <vector>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Candidate/interface/CompositePtrCandidate.h"


/**
   \class   BoostedTopEventHypothesis BoostedTopEventHypothesis.h "Analysis/BoostedTopObjects/interface/BoostedTopEventHypothesis.h"

   \brief   Class to hold event hypothesis information for boosted top events

   This class provides an interface for boosted top event hypotheses. The possible options are:
      - Leptonic decay  on  hadronic decay
          * Hadronic decay = 
	    - Type I
	    - Type II
	    - Type III
      - Hadronic decay  on  hadronic decay
          * Hadronic decay =
	    - Type I
	    - Type II
	    - Type III
**/

class BoostedTopEventHypothesis : public reco::CompositePtrCandidate {

 public:
  typedef reco::CompositeCandidate base_type;

  enum Decay_t {
    SEMI_TYPE1,
    SEMI_TYPE2,
    SEMI_TYPE3,
    HAD_TYPE1_TYPE1,
    HAD_TYPE1_TYPE2,
    HAD_TYPE1_TYPE3,
    HAD_TYPE2_TYPE2,
    HAD_TYPE2_TYPE3,
    HAD_TYPE3_TYPE3,
    N_DECAY_TYPES
  };

 public:
  BoostedTopEventHypothesis() {decay_ = N_DECAY_TYPES; } 

  // Various ways to set up the candidates.
  // Possibilities are:
  //   - Semilep on Type 1, 2, 3
  //   - All hadronic, all Type1,2,3 combinations

  // Signatures are in order as "top candidate 1 constituents, top candidate 2 constituents",
  //     and the constituents are ordered as "b jet, W candidate constituents"

  void setSemiLepType1( reco::CandidatePtr const & bJet,
			reco::CandidatePtr const & muon,
			reco::CandidatePtr const & met,			
			reco::CandidatePtr const & topJet );

  void setSemiLepType2( reco::CandidatePtr const & bJet1,
			reco::CandidatePtr const & muon,
			reco::CandidatePtr const & met,
			reco::CandidatePtr const & bJet2,
			reco::CandidatePtr const & wJet );

  void setSemiLepType3( reco::CandidatePtr const & bJet1,
			reco::CandidatePtr const & muon,
			reco::CandidatePtr const & met,
			reco::CandidatePtr const & bJet2,
			reco::CandidatePtr const & qJet,
			reco::CandidatePtr const & pJet );

  void setHadType1Type1( reco::CandidatePtr const & topJet1,
			 reco::CandidatePtr const & topJet2 );
 

  void setHadType1Type2( reco::CandidatePtr const & topJet1,
			 reco::CandidatePtr const & bJet2,
			 reco::CandidatePtr const & wJet2 ); 
  
  void setHadType1Type3( reco::CandidatePtr const & topJet1,
			 reco::CandidatePtr const & bJet2,
			 reco::CandidatePtr const & qJet2,
			 reco::CandidatePtr const & pJet2 ); 


  void setHadType2Type2( reco::CandidatePtr const & bJet1,
			 reco::CandidatePtr const & wJet1,
			 reco::CandidatePtr const & bJet2,
			 reco::CandidatePtr const & wJet2 ); 
  
  void setHadType2Type3( reco::CandidatePtr const & bJet1,
			 reco::CandidatePtr const & wJet1,
			 reco::CandidatePtr const & bJet2,
			 reco::CandidatePtr const & qJet2,
			 reco::CandidatePtr const & pJet2 ); 

  void setHadType3Type3( reco::CandidatePtr const & bJet1,
			 reco::CandidatePtr const & qJet1,
			 reco::CandidatePtr const & pJet1,
			 reco::CandidatePtr const & bJet2,
			 reco::CandidatePtr const & qJet2,
			 reco::CandidatePtr const & pJet2 ); 

  reco::Candidate const * getT1()   const;  // first top candidate
  reco::Candidate const * getT2()   const;  // second top candidate


  reco::Candidate const * getB1()   const;  // first b candidate
  reco::Candidate const * getB2()   const;  // second b candidate
  reco::Candidate const * getW1()   const;  // first W candidate
  reco::Candidate const * getW2()   const;  // second W candidate

  reco::Candidate const * getMu()   const;  // muon 
  reco::Candidate const * getNu()   const;  // neutrino 

  reco::Candidate const * getQ1()   const;  // first W's first daughter 
  reco::Candidate const * getP1()   const;  // first W's second daughter 
  reco::Candidate const * getQ2()   const;  // second W's first daughter 
  reco::Candidate const * getP2()   const;  // second W's second daughter 

  // Decay type return
  Decay_t  decay() const { return decay_; }


 protected:
  Decay_t       decay_;      // Decay type 
  std::vector<reco::CompositePtrCandidate> wVector_;
  std::vector<reco::CompositePtrCandidate> tVector_;
};


#endif
