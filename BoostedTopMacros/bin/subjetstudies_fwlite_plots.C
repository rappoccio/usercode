#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
#include <TF1.h>
#include <TRandom.h>
// #include <TDCacheFile.h>
#include <TLorentzVector.h>
#include <TVector2.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

#include <iostream>
#include <fstream>
#include <map>
#include <string>


using namespace std;
using namespace reco;
using namespace edm;

struct GreaterByPt {
  bool operator()( const TLorentzVector & t1, 
		   const TLorentzVector & t2 ) const {
    return t1.Perp() > t2.Perp();
  }
};



ostream & operator<<( ostream & out, TLorentzVector v) {
  out << "(Pt,Y,phi,M) = (" << v.Perp() << ", " << v.Rapidity() << ", " << v.Phi() << ", " << v.M() << ")";
  return out;
}


  class PartonMatcher {
  public:
    typedef std::pair<reco::Candidate const *, reco::Candidate const *>  subjet_pair;
    typedef std::vector<subjet_pair>                                 collection_type;

    PartonMatcher( reco::Jet::Constituents const & subjets, vector<reco::GenParticle> const & genParticles ){

      reco::Jet::Constituents::const_iterator subjets_begin = subjets.begin(),
	subjets_end = subjets.end(), isubjet = subjets_begin;
      for ( ; isubjet != subjets_end; ++isubjet ) {
	TLorentzVector subjet_p4( (*isubjet)->px(), (*isubjet)->py(), (*isubjet)->pz(), (*isubjet)->energy() );
	vector<reco::GenParticle>::const_iterator particles_begin = genParticles.begin(),
	  particles_end = genParticles.end(), iparticle = particles_begin,
	  imatched = particles_end;
	double dr_min = 999;
	for ( ; iparticle != particles_end; ++iparticle ) {
	  if ( iparticle->status() != 3 ||
	       iparticle->pt() < 0.0001 ||
	       abs(iparticle->pdgId()) >= 6)  continue;
	  TLorentzVector parton_p4( iparticle->px(), iparticle->py(), iparticle->pz(), iparticle->energy() );
// 	  cout << "Particle " << iparticle - particles_begin << ", id = " << iparticle->pdgId() << ", p4 = " << parton_p4 << endl;
	  double dr = parton_p4.DeltaR( subjet_p4 );
	  if ( dr < dr_min ) {
	    dr_min = dr;
	    imatched = iparticle;
	  }
	}
// 	cout << "Pushing back pair for subjet " << isubjet - subjets_begin << ", p4 = " << subjet_p4 << ",  id = " << imatched->pdgId() << endl;
	collection_.push_back( subjet_pair( &(**isubjet), &(*imatched)  ) );
      }
    }

    reco::Candidate const *  getSubjet( unsigned int i = 0) const { return collection_[i].first; }
    reco::Candidate const *  getParton( unsigned int i = 0) const { return collection_[i].second; }


  protected:
    collection_type collection_;
  };


struct GreaterByPtCand {
  bool operator()( const reco::Jet::Constituent & t1, 
		   const reco::Jet::Constituent & t2 ) const {
    return t1->pt() > t2->pt();
  }
};

void subjetstudies_fwlite_plots(std::string sample = "zprime_m1000_w10",
				double ptsmear = 0.0, double etasmear = 0.0, double phismear = 0.0)
{
   

  vector<string> files;

  bool isSignal = false;

  if ( sample == "zprime_m1000_w10" ) {
    isSignal = true;
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_1.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_4.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_5.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_6.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_7.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_8.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m1000_w10_testing/ca_pat_fat_223_9.root");
  }

  else if ( sample == "zprime_m3000_w30" ) {
    isSignal = true;
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_10.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_1.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_2.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_3.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_4.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_5.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_6.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_7.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_8.root");
files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_9.root");
  }

  else if ( sample == "qcd_800" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_testing/ca_pat_fat_223_9.root");

  }

  else if ( sample == "zprime_fullsim_m2000_w20_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/ca_pat_slim_223_9.root");
  }
  else if ( sample == "zprime_fullsim_m2000_w20_v6_fixed_kt" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/kt_pat_slim_223_9.root");

  }
  else if ( sample == "zprime_fullsim_m2000_w20_v6_fixed_antikt" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_fixed/antikt_pat_slim_223_9.root");

  }

  else if ( sample == "zprime_fullsim_m3000_w30_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/ca_pat_slim_223_9.root");
  }
  else if ( sample == "zprime_fullsim_m3000_w30_v6_fixed_kt" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/kt_pat_slim_223_9.root");

  }
  else if ( sample == "zprime_fullsim_m3000_w30_v6_fixed_antikt" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_fixed/antikt_pat_slim_223_9.root");

  }

  else if ( sample == "qcd_600_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/ca_pat_slim_223_9.root");

  }
  else if ( sample == "qcd_600_v6_fixed_kt" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/kt_pat_slim_223_9.root");

  }
  else if ( sample == "qcd_600_v6_fixed_antikt" ) {

files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v6_fixed/antikt_pat_slim_223_9.root");

  }

   
  using namespace std;
  using namespace reco;



  typedef std::vector<reco::GenParticle::const_iterator>::const_iterator key_type;
  typedef reco::Jet::Constituents::const_iterator                        value_type;
  typedef std::pair<key_type, value_type> subjet_pair;
  typedef std::vector<subjet_pair> subjet_vector;




  TString fname( "subjet_studies_" );
  fname += sample.c_str();
  fname += ".root";

  TFile * f = new TFile(fname.Data(), "RECREATE");

  TH1D * hist_n_subjets = new TH1D("hist_n_subjets", "Number of subjets", 5, 0, 5);

  TH1D * hist_subjetPt1 = new TH1D("hist_subjetPt1", "Subjet Pt 1", 100, 0, 1000);
  TH1D * hist_subjetY1 = new TH1D("hist_subjetY1", "Subjet Y 1", 100, 0, 1000);
  TH1D * hist_subjetDR1 = new TH1D("hist_subjetDR1", "#Delta R between Hard Jet and Subjet 1", 100, 0, 1.0);
  TH1D * hist_subjetFlavour1 = new TH1D("hist_subjetFlavour1", "Subjet Flavor 1", 25, 0, 25);

  TH1D * hist_subjetPt2 = new TH1D("hist_subjetPt2", "Subjet Pt 2", 100, 0, 1000);
  TH1D * hist_subjetY2 = new TH1D("hist_subjetY2", "Subjet Y 2", 100, 0, 1000);
  TH1D * hist_subjetDR2 = new TH1D("hist_subjetDR2", "#Delta R between Hard Jet and Subjet 2", 100, 0, 1.0);
  TH1D * hist_subjetFlavour2 = new TH1D("hist_subjetFlavour2", "Subjet Flavor 2", 25, 0, 25);

  TH1D * hist_subjetPt3 = new TH1D("hist_subjetPt3", "Subjet Pt 3", 100, 0, 1000);
  TH1D * hist_subjetY3 = new TH1D("hist_subjetY3", "Subjet Y 3", 100, 0, 1000);
  TH1D * hist_subjetDR3 = new TH1D("hist_subjetDR3", "#Delta R between Hard Jet and Subjet 3", 100, 0, 1.0);
  TH1D * hist_subjetFlavour3 = new TH1D("hist_subjetFlavour3", "Subjet Flavor 3", 25, 0, 25);

  TH1D * hist_subjetPt4 = new TH1D("hist_subjetPt4", "Subjet Pt 4", 100, 0, 1000);
  TH1D * hist_subjetY4 = new TH1D("hist_subjetY4", "Subjet Y 4", 100, 0, 1000);
  TH1D * hist_subjetDR4 = new TH1D("hist_subjetDR4", "#Delta R between Hard Jet and Subjet 4", 100, 0, 1.0);
  TH1D * hist_subjetFlavour4 = new TH1D("hist_subjetFlavour4", "Subjet Flavor 4", 25, 0, 25);



  TH2D * subjet_dr_3subjets = new TH2D("subjet_dr_3subjets", "#Delta R (subjet, parton), 3 subjets;#Delta R", 50, 0, 500, 50, 0, 1.0);
  TH2D * subjet_res_3subjets = new TH2D("subjet_res_3subjets", "p_{T} Residual, 3 subjets;p_{T} of parton;p_{T} Fraction", 50, 0, 500, 50, -1.0, 1.5);
  TH2D * subjet_deta_3subjets = new TH2D("subjet_deta_3subjets", "Rapidity Residual, 3 subjets;p_{T} of parton;Y Fraction", 50, 0, 500, 50, -1.0, 1.0);
  TH2D * subjet_dphi_3subjets = new TH2D("subjet_dphi_3subjets", "#phi Residual, 3 subjets;p_{T} of parton;#phi Fraction", 50, 0, 500, 50, -1.0, 1.0);
  TH1D * min_mass_3subjets = new TH1D("min_mass_3subjets", "Min Mass, 3 subjets;Min Mass (GeV/c^{2})", 50, 0, 100);
  TH1D * pt3_3subjets = new TH1D("pt3_3subjets", "Third Subjet p_{T}, 3 Subjets;Jet p_{T} (GeV/c)", 50, 0, 500);

  TH2D * subjet_dr_4subjets = new TH2D("subjet_dr_4subjets", "#Delta R (subjet, parton), 4 subjets;#Delta R", 50, 0, 500, 50, 0, 1.0);
  TH2D * subjet_res_4subjets = new TH2D("subjet_res_4subjets", "p_{T} Residual, 4 subjets;p_{T} of parton;p_{T} Fraction", 50, 0, 500, 50, -1.0, 1.5);
  TH2D * subjet_deta_4subjets = new TH2D("subjet_deta_4subjets", "Rapidity Residual, 4 subjets;p_{T} of parton;Y Fraction", 50, 0, 500, 50, -1.0, 1.0);
  TH2D * subjet_dphi_4subjets = new TH2D("subjet_dphi_4subjets", "#phi Residual, 4 subjets;p_{T} of parton;#phi Fraction", 50, 0, 500, 50, -1.0, 1.0);

  TH1D * min_mass_4subjets = new TH1D("min_mass_4subjets", "Min Mass, 4 subjets;Min Mass (GeV/c^{2})", 50, 0, 100);
  TH1D * min_3mass_4subjets = new TH1D("min_3mass_4subjets", "Min Mass of top 3 subjets, 4 subjets;Min Mass (GeV/c^{2})", 50, 0, 100);
  TH1D * min_3primemass_4subjets = new TH1D("min_3primemass_4subjets", "Min Mass, Merge lowest subjets, 4 subjets;Min Mass (GeV/c^{2})", 50, 0, 100);
  TH1D * pt3_4subjets = new TH1D("pt3_4subjets", "Third Subjet p_{T}, 4 Subjets;Jet p_{T} (GeV/c)", 50, 0, 500);

  TF1 * resfit3 = new TF1("resfit3", "sqrt( [0]*[0]/(x-[1]) + [2]*[2])", 0, 1000);
  resfit3->SetParameter(0, 0.74);
  resfit3->SetParameter(1, 23.6);
  resfit3->SetParameter(2, 0.146);

  TF1 * resfit4 = new TF1("resfit4", "sqrt( [0]*[0]/(x-[1]) + [2]*[2])", 0, 1000);
  resfit4->SetParameter(0, 0.96);
  resfit4->SetParameter(1, 22.8);
  resfit4->SetParameter(2, 0.177);


  TF1 * etaresfit = new TF1("etaresfit",  "sqrt( [0]*[0]/(x-[1]) + [2]*[2] + [3]*[3]*x*x)", 0, 5000);
  etaresfit->SetParameter(0, 0.41 );
  etaresfit->SetParameter(1, 24.7 );
  etaresfit->SetParameter(2, 0.013);
  etaresfit->SetParameter(3, 6.4e-5);

  TF1 * phiresfit = new TF1("phiresfit",  "sqrt( [0]*[0]/(x-[1]) + [2]*[2] + [3]*[3]*x*x)", 0, 5000);
  phiresfit->SetParameter(0, 0.44 );
  phiresfit->SetParameter(1, 24.7 );
  phiresfit->SetParameter(2, 0.0);
  phiresfit->SetParameter(3, 5.6e-5);

  cout << "About to make chain event" << endl;
  
  fwlite::ChainEvent ev(files);
  
  cout << "About to loop" << endl;

  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {


    if ( ev.getBranchDescriptions().size() <= 0 ) continue;


    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    fwlite::Handle<std::vector<reco::GenParticle> > h_genParticles;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");
    h_genParticles.getByLabel(ev, "prunedGenParticles" );

    if ( !h_jet.isValid() || !h_genParticles.isValid() ) continue;

    vector<pat::Jet>::const_iterator jetsbegin = h_jet->begin(),
      jetsend = h_jet->end(), ijet = jetsbegin;


    for ( ; ijet != jetsend; ++ijet ) {

      if ( isSignal && abs(ijet->partonFlavour()) != 6 ) continue;

      // -------------------------------------------
      // First make some basic plots of the subjets
      // -------------------------------------------

      // This has to be a copy, not a reference. I really should fix this. 
      reco::Jet::Constituents constituents = ijet->getJetConstituents();


      sort( constituents.begin(), constituents.end(), GreaterByPtCand() );


      hist_n_subjets->Fill( constituents.size() );

      PartonMatcher matcher( constituents, *h_genParticles );
      
      TLorentzVector jet_p4( ijet->px(), ijet->py(), ijet->pz(), ijet->energy() );

      int nsubjets = constituents.size();

      if ( nsubjets > 0 ) {

	reco::CandidatePtr & subjet1 = constituents[0];
	TLorentzVector subjet1_p4(subjet1->px(), subjet1->py(), subjet1->pz(), subjet1->energy() );

	hist_subjetPt1->Fill( subjet1_p4.Pt() );
	hist_subjetY1->Fill( subjet1_p4.Rapidity() );
	hist_subjetDR1->Fill( jet_p4.DeltaR(subjet1_p4) );
	hist_subjetFlavour1->Fill( matcher.getParton(0)->pdgId() );

      
	if ( nsubjets > 1 ) {
	  reco::CandidatePtr & subjet2 = constituents[1];
	  TLorentzVector subjet2_p4(subjet2->px(), subjet2->py(), subjet2->pz(), subjet2->energy() );

	  hist_subjetPt2->Fill( subjet2_p4.Pt() );
	  hist_subjetY2->Fill( subjet2_p4.Rapidity() );
	  hist_subjetDR2->Fill( jet_p4.DeltaR(subjet2_p4) );
	  hist_subjetFlavour2->Fill(matcher.getParton(1)->pdgId());


      
	  if ( nsubjets > 2 ) {
	    reco::CandidatePtr & subjet3 = constituents[2];
	    TLorentzVector subjet3_p4(subjet3->px(), subjet3->py(), subjet3->pz(), subjet3->energy() );

	    hist_subjetPt3->Fill( subjet3_p4.Pt() );
	    hist_subjetY3->Fill( subjet3_p4.Rapidity() );
	    hist_subjetDR3->Fill( jet_p4.DeltaR(subjet3_p4) );
	    hist_subjetFlavour3->Fill(matcher.getParton(2)->pdgId());



	    if ( nsubjets > 3 ) {
	      reco::CandidatePtr & subjet4 = constituents[3];
	      TLorentzVector subjet4_p4(subjet4->px(), subjet4->py(), subjet4->pz(), subjet4->energy() );

	      hist_subjetPt4->Fill( subjet4_p4.Pt() );
	      hist_subjetY4->Fill( subjet4_p4.Rapidity() );
	      hist_subjetDR4->Fill( jet_p4.DeltaR(subjet4_p4) );
	      hist_subjetFlavour4->Fill(matcher.getParton(3)->pdgId());

	    }
	  }
	}
      }


	  
      // Now look at the minimum mass 
      double min_mass = 99999;
      reco::Jet::Constituents  subjets = ijet->getJetConstituents();

	  
      // 	  cout << "Jet : pt = " << ijet->pt() << ", Y = " << ijet->rapidity() << endl;
      // 	  cout << "Subjets : " << endl;
      reco::Jet::Constituents::const_iterator isubjetBegin = subjets.begin(),
	isubjetEnd = subjets.end(), isubjet = isubjetBegin;

      // Find closest matching subjet
      if ( subjets.size() >= 3 ) {

	vector<TLorentzVector> subjets_p4;

	


	for ( isubjet = isubjetBegin; isubjet != isubjetEnd ; ++isubjet ) {
	  subjets_p4.push_back(TLorentzVector((*isubjet)->px(), (*isubjet)->py(), (*isubjet)->pz(), (*isubjet)->energy() ) );
	}

	sort( subjets_p4.begin(), subjets_p4.end(), GreaterByPt() );


	for ( isubjet = isubjetBegin; isubjet != isubjetEnd - 1; ++isubjet ) {
	  TLorentzVector & isubjet_p4 = subjets_p4[isubjet - isubjetBegin];

	  reco::Jet::Constituents::const_iterator jsubjet = isubjet + 1;

	  for ( ; jsubjet != isubjetEnd; ++jsubjet ) {
	    TLorentzVector & jsubjet_p4 = subjets_p4[jsubjet - isubjetBegin];
	    		
	    TLorentzVector sum = isubjet_p4 + jsubjet_p4;

	    double m = sum.M();
	    if ( m < min_mass ) {
	      min_mass = m;
	    }
	  }
	    
	}


	if ( subjets.size() == 3 ) {
	  min_mass_3subjets->Fill( min_mass );
	} else if ( subjets.size() == 4 ) {
	  min_mass_4subjets->Fill( min_mass );
	}


	if ( subjets.size() == 4 ) {

	  // get the 3 highest pt  subjets in the case of 4 subjets.


	  double minMass3 = 9999;

		
	  for ( int it1 = 0; it1 < 2; ++it1 ) {
	    for ( int it2 = it1 + 1; it2 < 3; ++it2 ) {
	      TLorentzVector sum = subjets_p4[it1] + subjets_p4[it2];
	      double m = sum.M();
	      if ( m < minMass3 )
		minMass3 = m;
	    }
	  }

	    
	  min_3mass_4subjets->Fill( minMass3 );


	  std::vector<TLorentzVector> subjets_mergedlow_p4( 3 );
	  copy( subjets_p4.begin(), subjets_p4.begin() + 3,
		subjets_mergedlow_p4.begin() );
	  subjets_mergedlow_p4[2] += subjets_p4[3];

	  double minMass3Prime = 9999;
		
	  for ( int it1 = 0; it1 < 2; ++it1 ) {
	    for ( int it2 = it1 + 1; it2 < 3; ++it2 ) {
	      TLorentzVector sum = subjets_mergedlow_p4[it1] + subjets_mergedlow_p4[it2];
	      double m = sum.M();
	      if ( m < minMass3Prime ) {
		minMass3Prime = m;
	      }
	    }
	  }
	  min_3primemass_4subjets->Fill( minMass3Prime ) ;

	}

      }

  
      // -------------------------------------------
      // Next make plots for the subjet resolution studies
      // -------------------------------------------

      
      



      
//       // Make sure we're looking at well-matched ttbar
//       const reco::GenParticle * genParton = ijet->genParton();
//       if ( genParton != 0 && abs(genParton->pdgId()) == 6 ) {
// 	int nda = genParton->numberOfDaughters();

// 	// Get the 3 daughter quarks of the top + W
// 	vector<reco::GenParticle::const_iterator> daughters;
// 	vector<TLorentzVector> subjets_p4;

// 	// Get the top daughter iterators
// 	reco::GenParticle::const_iterator topdaBegin = genParton->begin(),
// 	  topdaEnd = genParton->end(), topda = topdaBegin;

// 	for ( ; topda != topdaEnd; ++topda ) {

// 	  if ( topda->status() != 3 ) continue;


// 	  // Get the b
// 	  if ( fabs(topda->pdgId()) == 5 ) {
// 	    daughters.push_back( topda );
// 	  }
// 	  // And the q+q'
// 	  else if ( fabs(topda->pdgId()) == 24 ) {
	    
// 	    // Get the W daughter iterators
// 	    reco::GenParticle::const_iterator wdaBegin = topda->begin(),
// 	      wdaEnd = topda->end(), wda = wdaBegin;
// 	    for ( ; wda != wdaEnd; ++wda ) {
// 	      if ( fabs(wda->pdgId()) < 21 ) {
// 		daughters.push_back ( wda );
// 	      }
// 	    }
// 	  }
// 	}

// 	// Now we have the 3 daughters. 
// 	if ( daughters.size() == 3 ) {
// // 	  cout << "Top Quark = " << genParton->pdgId() << ", pt = " << genParton->pt() << ", Y = " << genParton->rapidity() << endl;
// // 	  cout << "Daughters: " << endl;
// 	  vector<reco::GenParticle::const_iterator>::const_iterator subjetPartonBegin = daughters.begin(),
// 	    subjetPartonEnd = daughters.end(), isubjetParton = subjetPartonBegin;
// // 	  for ( ; isubjetParton != subjetPartonEnd; ++isubjetParton ) {
// // 	    cout << isubjetParton - subjetPartonBegin << ", id = " << (*isubjetParton)->pdgId() 
// // 		 << ", status = " << (*isubjetParton)->status() 
// // 		 << ", pt = " << (*isubjetParton)->pt() 
// // 		 << ", Y = " << (*isubjetParton)->rapidity()
// // 		 << ", phi = " << (*isubjetParton)->phi() << endl;
// // 	  }


	 
// 	  // Now look at the subjet resolution
// 	  subjet_vector matches;
// 	  // Loop over partons
// 	  for ( isubjetParton = subjetPartonBegin; isubjetParton != subjetPartonEnd; ++isubjetParton ) {
// 	    double minDr = 999;
// 	    value_type dr_min_it = isubjetEnd;
// 	    TLorentzVector parton_p4( (*isubjetParton)->px(),
// 				      (*isubjetParton)->py(),
// 				      (*isubjetParton)->pz(),
// 				      (*isubjetParton)->energy() );
// 	    // Find closest matching subjet
// 	    for ( isubjet = isubjetBegin; isubjet != isubjetEnd; ++isubjet ) {
// 	      TLorentzVector subjet_p4( (*isubjet)->px(),
// 					(*isubjet)->py(),
// 					(*isubjet)->pz(),
// 					(*isubjet)->energy() );
// 	      double dr = parton_p4.DeltaR(subjet_p4);
// 	      if ( dr < minDr ) {
// 		minDr = dr;
// 		dr_min_it = isubjet;
// 	      }
// 	    }
// 	    // If you found a matching subjet, store the pair
// 	    if ( dr_min_it != isubjetEnd ) {
// 	      matches.push_back( subjet_pair( isubjetParton, dr_min_it ) );
// 	      subjets_p4.push_back( TLorentzVector( (*dr_min_it)->px(),
// 						    (*dr_min_it)->py(),
// 						    (*dr_min_it)->pz(),
// 						    (*dr_min_it)->energy()
// 						    ) );
// 	    }
	    
// 	  }

// 	  subjet_vector::const_iterator pairItBegin = matches.begin(),
// 	    pairItEnd = matches.end(), pairIt = pairItBegin;
// 	  for ( ; pairIt != pairItEnd; ++pairIt ) {
// 	    TLorentzVector parton_p4( (* (pairIt->first))->px(),
// 				      (* (pairIt->first))->py(),
// 				      (* (pairIt->first))->pz(),
// 				      (* (pairIt->first))->energy() );
// 	    TLorentzVector subjet_p4 = subjets_p4[ pairIt - pairItBegin];
// // 	    cout << "pair " << pairIt - pairItBegin << " : " << endl;
// // 	    cout << "  parton " << pairIt->first - subjetPartonBegin << " : "
// // 		 << "   pt = " << parton_p4.Perp() 
// // 		 << ",  Y  = " << parton_p4.Rapidity() 
// // 		 << ",  phi= " << parton_p4.Phi() << endl
// // 		 << "  subjet " << pairIt->second - isubjetBegin << " : " 
// // 		 << "   pt = " << subjet_p4.Perp() 
// // 		 << ",  Y  = " << subjet_p4.Rapidity() 
// // 		 << ",  phi= " << subjet_p4.Phi() << endl
// // 		 << "  dR = " << subjet_p4.DeltaR( parton_p4 ) << endl;


// 	    double dR = subjet_p4.DeltaR( parton_p4 );
// 	    double ptfrac = (subjet_p4.Perp() - parton_p4.Perp()) / parton_p4.Perp();
// 	    double deta = (subjet_p4.Rapidity() - parton_p4.Rapidity());
// 	    double dphi = TVector2::Phi_mpi_pi(subjet_p4.Phi() - parton_p4.Phi());
	    
// 	    if ( subjets.size() == 3 ) {
// 	      subjet_dr_3subjets ->Fill( parton_p4.Perp(), dR );
// 	      subjet_deta_3subjets->Fill( parton_p4.Perp(), deta );
// 	      subjet_dphi_3subjets->Fill( parton_p4.Perp(), dphi );
// 	      subjet_res_3subjets ->Fill( parton_p4.Perp(), ptfrac );
// 	      pt3_3subjets->Fill( subjets_p4[2].Perp() );
// 	    }
// 	    else if ( subjets.size() == 4 ) {
// 	      subjet_dr_4subjets ->Fill( parton_p4.Perp(), dR );
// 	      subjet_deta_4subjets->Fill( parton_p4.Perp(), deta );
// 	      subjet_dphi_4subjets->Fill( parton_p4.Perp(), dphi );
// 	      subjet_res_4subjets ->Fill( parton_p4.Perp(), ptfrac );
// 	      pt3_4subjets->Fill( subjets_p4[2].Perp() );
// 	    }
// 	  }


// 	  // Do some smearing if desired
// 	  for ( isubjet = isubjetBegin; isubjet != isubjetEnd; ++isubjet ) {
// 	    TLorentzVector & isubjet_p4 = subjets_p4[isubjet - isubjetBegin];

	  
// 	    // Get the matched parton
// 	    key_type imatched = subjetPartonEnd;
// 	    subjet_vector::const_iterator imatchBegin = matches.begin(),
// 	      imatchEnd = matches.end(), imatchIt = imatchBegin;
// 	    for ( ; imatchIt != imatchEnd; ++imatchIt ) {
// 	      if ( imatchIt->second == isubjet ) imatched = imatchIt->first;
// 	    }


// 	    // Smear the pt of the subjet by some additional amount for studies
// 	    if ( imatched != subjetPartonEnd ) {
// 	      double resolution = resfit3->Eval( (*imatched)->energy() );
// 	      double scalefactor1 = gRandom->Gaus(1, ptsmear*resolution );
// 	      isubjet_p4 *= scalefactor1;
// 	      double resolution_y = etaresfit->Eval( (*imatched)->energy() );
// 	      double scalefactor2 = gRandom->Gaus(1, etasmear * resolution_y );
// 	      double Y = isubjet_p4.Rapidity();
// 	      double dY = Y * scalefactor2;
// 	      double e = isubjet_p4.E();
// 	      double p = isubjet_p4.P();
// 	      double exp2Y = TMath::Exp(2*Y);
// 	      double theta = TMath::ACos( (exp2Y-1)/(exp2Y+1) * e/p);
// 	      isubjet_p4.SetTheta( theta );
// 	      double resolution_phi = phiresfit->Eval( (*imatched)->energy() );
// 	      double scalefactor3 = gRandom->Gaus(1, phismear * resolution_phi );
// 	      isubjet_p4.SetPhi( isubjet_p4.Phi() * scalefactor3 );
// 	    }
// 	  }
	  
// 	}
	
//       }
    }
    

  }

  f->cd();

  hist_n_subjets->Write();

  hist_subjetPt1->Write();
  hist_subjetY1->Write();
  hist_subjetDR1->Write();
  hist_subjetFlavour1->Write();


  hist_subjetPt2->Write();
  hist_subjetY2->Write(); 
  hist_subjetDR2->Write(); 
  hist_subjetFlavour2->Write(); 


  hist_subjetPt3->Write(); 
  hist_subjetY3->Write(); 
  hist_subjetDR3->Write(); 
  hist_subjetFlavour3->Write(); 



  hist_subjetPt4->Write(); 
  hist_subjetY4->Write();
  hist_subjetDR4->Write();
  hist_subjetFlavour4->Write();


  subjet_dr_3subjets ->Write();
  subjet_deta_3subjets ->Write();
  subjet_dphi_3subjets ->Write();
  subjet_res_3subjets ->Write();
  min_mass_3subjets-> Write();
  pt3_3subjets->Write();

  subjet_dr_4subjets ->Write();
  subjet_deta_4subjets ->Write();
  subjet_dphi_4subjets ->Write();
  subjet_res_4subjets ->Write();
  min_mass_4subjets-> Write();
  min_3mass_4subjets->Write();
  min_3primemass_4subjets->Write();
  pt3_4subjets->Write();

  f->Close();
  
}

