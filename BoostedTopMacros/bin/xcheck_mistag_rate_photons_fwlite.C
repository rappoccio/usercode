#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
#include <TDCacheFile.h>
#include <TLorentzVector.h>
#include <TRandom.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

#include "PredictedDistribution.h"

#include <iostream>
#include <map>
#include <string>

using namespace std;

// Make a mistag parameterization in et and eta.
// Procedure:
// 1) Loop over odd events (leave even for cross checks).
// 2) Require exactly 2 jets.
// 3) If jet1 is anti-tagged:
//    a) Fill denominator with et,eta of jet 2
//    b) If jet2 is tagged, fill numerator with et, eta of jet 2.
// 4) If jet2 is anti-tagged:
//    a) Fill denominator with et,eta of jet 1
//    b) If jet1 is tagged, fill numerator with et, eta of jet 1.
// 5) Sum up contributions.
// 6) Pass numerator and denominator to the combiner function,
//    which will combine all the separate jet bins, and divide them,
//    taking into account the statistical uncertainty. 

ostream & operator<<( ostream & out, TLorentzVector v )
{
  char buff[1000];
  sprintf(buff, "(%6.2f,%6.2f,%6.2f,%6.2f)",
	  v.Energy(),
	  v.Pt(), v.Eta(), v.Phi() );
  out << buff;
  return out;
}

void xcheck_mistag_rate_fwlite(TH1D * parameterization,
			       string sample = "ttbar",
			       bool processAll = false,
			       bool pseudoExp = true,
			       double Lum = 1.0,
			       int njets = 2,
			       double topMassCut1 = 100, double topMassCut2 = 250,
			       double wMassCut1 = 0, double wMassCut2 = 99999.0,
			       double minMassCut1 = 50.0, double minMassCut2 = 99999.0)
{
  
  cout << "Processing sample = " << sample << endl;
  vector<string> files;

  int iweight = -1;


 if ( sample == "photonjet_300") {
   iweight = 0;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_35.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_44.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_45.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_46.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt300/ca_pat_slim_fastsim_220_9.root");
 }

 else if ( sample == "photonjet_470" ) {

   iweight = 1;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_35.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_44.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_45.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_46.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt470/ca_pat_slim_fastsim_220_9.root");
 }

 else if ( sample == "photonjet_800") {

   iweight = 2;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_35.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_44.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_45.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_46.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt800/ca_pat_slim_fastsim_220_9.root");

 }




  else if ( sample == "photonjet_1400" ) {
    iweight = 3;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_101.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_44.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_45.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_46.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt1400/ca_pat_slim_fastsim_220_9.root");
 }

 else if ( sample == "photonjet_2200" ) {
   iweight = 4;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_35.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt2200/ca_pat_slim_fastsim_220_9.root");
 }

 else if ( sample == "photonjet_3000" ) {
   iweight = 5;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_35.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_44.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_45.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_46.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PhotonJetPt3000/ca_pat_slim_fastsim_220_9.root");
 }

 else if ( sample == "photonjet_300_v6" ) {
   iweight = 0;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_300_v6/ca_pat_slim_fastsim_223_9.root");
 }
 else if ( sample == "photonjet_470_v6" ) {
   iweight = 1;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_470_v6/ca_pat_slim_fastsim_223_9.root");
 }
 else if ( sample == "photonjet_800_v6" ) {
   iweight = 2;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_800_v6/ca_pat_slim_fastsim_223_9.root");
 }
 else if ( sample == "photonjet_1400_v6" ) {
   iweight = 3;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_21.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_1400_v6/ca_pat_slim_fastsim_223_9.root");
 }
 else if ( sample == "photonjet_2200_v6" ) {
   iweight = 4;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_2200_v6/ca_pat_slim_fastsim_223_9.root");
 }
 else if ( sample == "photonjet_3000_v6" ) {
   iweight = 5;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/photonjet_3000_v6/ca_pat_slim_fastsim_223_9.root");
 }

  double weights[] = {
    4.193   ,
    4.515e-1,
    2.003e-2 ,
    2.686e-4 ,
    1.522e-6 ,
    5.332e-9
  };

  int nevents[] = {
    1104000,
    1092000,
    1104000,
    1100000,
    1100000,
    1100000
  };

  unsigned int seeds[] = {
    282618,
    947201,
    231657,
    484974,
    957477,
    744305,
    540044,
    739953,
    759944,
    658637,
    315638,
    804403,
    519672,
    168572
  };


  double weight = weights[iweight];
  int nevent = nevents[iweight];

  // Calculate the effective luminosity generated
  double lum_eff = (double)nevent / weight; 

  // Note! For an ensemble test, need to reweight the distributions
  // to account for the luminosity discrepancy.
  // To do a proper statistical treatment, we need to "throw"
  // pseudo experiments via which to make a prediction. 

  double pe_factor = Lum / lum_eff;

  // Make sure the pseudoexperiments always choose the same seed
  // for reproducability. 
  if ( pseudoExp ) {
    gRandom->SetSeed( seeds[iweight] );

    cout << "Effective lum = " << lum_eff << endl;
    cout << "Desired lum   = " << Lum << endl;
    cout << "Skipping every " << 1.0 / pe_factor << " events" << endl;
  }
  
  using namespace std;
  using namespace reco;
  using namespace edm;
  
  using namespace std;
  using namespace reco;
  using namespace edm;


  PredictedDistribution * total_pred     = new PredictedDistribution(parameterization, "total",  "Total Rate", 2, 0, 2 );
  PredictedDistribution * jet_et_pred    = new PredictedDistribution(parameterization,  "jet_pt", "Predicted Jet p_{T}", 50, 0, 5000 );
  PredictedDistribution * jet_eta_pred   = new PredictedDistribution(parameterization,  "jet_eta", "Predicted Jet #eta", 30, -3.0, 3.0 );
  PredictedDistribution * jet_phi_pred   = new PredictedDistribution(parameterization,  "jet_phi", "Predicted Jet #phi", 30, -3.14159, 3.14159 );
  
  
  cout << "About to create chain event" << endl;
  
  fwlite::ChainEvent ev(files);
  
  cout << "About to loop" << endl;
  
  // Loop over events
  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {

//     cout << "About to get pseudoexp value" << endl;
    // Select a subset of the events for a pseudoexperiment
    // based on the desired luminosity. 
    if ( pseudoExp && pe_factor < 1.0 ) {
      double fi = gRandom->Uniform();
      if ( fi >= pe_factor ) continue;
    } 


    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    unsigned int eventNumber = ev.id().event();

//     cout << "About to get jets" << endl;
    // get the jets
    fwlite::Handle<std::vector<pat::Jet> > h_jet;
//     cout << "About to get handle" << endl;
    h_jet   .getByLabel(ev,"selectedLayer1Jets");
    if ( !h_jet.isValid() ) continue;     // Make sure we have a handle

    // get the photons
    fwlite::Handle<std::vector<pat::Photon> > h_photon;
//     cout << "About to get handle" << endl;
    h_photon   .getByLabel(ev,"selectedLayer1Photons");
    if ( !h_photon.isValid() ) continue;     // Make sure we have a handle

//     cout << "Have a valid handle" << endl;

//     cout << "Done getting handle" << endl;
    if ( (eventNumber % 2 == 1) && !processAll ) continue; // Take even events, odd were used to make this matrix

//     cout << "Got handle, dereferencing" << endl;
    vector<pat::Jet> const & jets = *h_jet;
    vector<pat::Photon> const & photons = *h_photon;

//      cout << "Jets size = " << jets.size() << endl;
//      cout << "Photons size = " << photons.size() << endl;

    // require gamma+jet events
    if ( jets.size() >= 1 && photons.size() >= 1 ) {

//       cout << "Have a jet and a photon" << endl;

      // get the highest pt photon
      pat::Photon const & photon = photons[0];
      TLorentzVector v(photon.px(), photon.py(), photon.pz(),  photon.energy() );

//       cout << "Photon p4 = " << v << endl;
      
      // get the jet opposite to the photon
      double dphi_max = TMath::Pi()/2.0; // Don't take jets within a 1.0 cone of the photon
      vector<pat::Jet>::const_iterator ibegin = jets.begin(), iend = jets.end(), i = ibegin,
	ret = iend;
      for ( ; i != iend; ++i ) {
	TLorentzVector w(i->px(), i->py(), i->pz(), i->energy() );
	double dphi = fabs(w.DeltaPhi( v ));
//  	cout << "Examining jet " << i - ibegin << ", p4 = " << w <<  ", dphi = " << dphi * 180.0/TMath::Pi() << endl;
	if ( dphi > dphi_max) {
	  dphi_max = fabs(dphi);
	  ret = i;
	}
      }

      if ( ret == iend ) continue;

//        cout << "Got retvalues" << endl;

      pat::Jet const & jet1 = *ret;

      const reco::CATopJetTagInfo * catopTag1 = dynamic_cast<CATopJetTagInfo const *> (jet1.tagInfo("CATopJetTagger"));

      double topMass1 = catopTag1->properties().topMass;
      double wMass1 = catopTag1->properties().wMass;
      double minMass1 = catopTag1->properties().minMass;


      // get the tag quantities
      bool tagged1 = 
	(topMass1 >= topMassCut1 && topMass1 <= topMassCut2) &&
	(wMass1   >= wMassCut1   && wMass1   <= wMassCut2  ) &&
	(minMass1 >= minMassCut1 && minMass1 <= minMassCut2);

//       cout << "minMass = " << minMass1 << endl;

      total_pred->Accumulate( 1.0, jet1.pt(), tagged1 );
      jet_et_pred->Accumulate( jet1.pt(), jet1.pt(), tagged1  );
      jet_eta_pred->Accumulate( jet1.eta(), jet1.pt(), tagged1  );
      jet_phi_pred->Accumulate( jet1.phi(), jet1.pt(), tagged1  );

    }


  }

  cout << "Done with the loop" << endl;

  total_pred->SetCalculatedErrors();
//   total_pred->Normalize();

  jet_et_pred->SetCalculatedErrors();
//   jet_et_pred->Normalize();
  
  jet_eta_pred->SetCalculatedErrors();
//   jet_eta_pred->Normalize();
  
  jet_phi_pred->SetCalculatedErrors();
//   jet_phi_pred->Normalize();

  cout << "About to draw" << endl;
  
  TString fname ("xchecks_gammaplusjet_pe_");
  fname += sample;
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();

  total_pred->GetPredictedHist()->Write();
  total_pred->GetObservedHist()->Write();
  total_pred->GetTaggableHist()->Write();

  jet_et_pred->GetPredictedHist()->Write();
  jet_et_pred->GetObservedHist()->Write();
  jet_et_pred->GetTaggableHist()->Write();

  jet_eta_pred->GetPredictedHist()->Write();
  jet_eta_pred->GetObservedHist()->Write();
  jet_eta_pred->GetTaggableHist()->Write();

  jet_phi_pred->GetPredictedHist()->Write();
  jet_phi_pred->GetObservedHist()->Write();
  jet_phi_pred->GetTaggableHist()->Write();

  f->Close();

  delete total_pred;
  delete jet_et_pred;
  delete jet_eta_pred;
  delete jet_phi_pred;

  delete f;

}
