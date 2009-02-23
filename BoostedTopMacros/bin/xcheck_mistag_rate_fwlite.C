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

  if ( sample == "ttbar" ) {
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_20.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_21.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_22.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_23.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_9.root");
  }
  else if ( sample == "qcd_15" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_15/ca_pat_slim_220_1.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_15/ca_pat_slim_220_2.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_15/ca_pat_slim_220_3.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_15/ca_pat_slim_220_4.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_15/ca_pat_slim_220_5.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_15/ca_pat_slim_220_6.root");
  }
  else if ( sample == "qcd_20" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_20/ca_pat_slim_220_1.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_20/ca_pat_slim_220_2.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_20/ca_pat_slim_220_3.root");
  }
  else if ( sample == "qcd_30" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_30/ca_pat_slim_220_1.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_30/ca_pat_slim_220_2.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_30/ca_pat_slim_220_3.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_30/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_50" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_50/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_80" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_80/ca_pat_slim_220_1.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_80/ca_pat_slim_220_2.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_80/ca_pat_slim_220_3.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_80/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_120" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_120/ca_pat_slim_220_1.root");
  }
  else if ( sample == "qcd_170" ) {
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_170/ca_pat_slim_220_1.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_170/ca_pat_slim_220_2.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_170/ca_pat_slim_220_3.root");
    files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_170/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_230" ) {
    iweight = 0;
    files.push_back("/uscms_data/d1/rappocc/qcd_230/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_230/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_230/ca_pat_slim_220_3.root");
  }
  else if ( sample == "qcd_300" ) {
    iweight = 1;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_11.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_12.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_13.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_300/ca_pat_slim_220_9.root");
  }
  else if ( sample == "qcd_380" ) {
    iweight = 2;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_9.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_380/ca_pat_slim_220_11.root");
  }
  else if ( sample == "qcd_470" ) {
    iweight = 3;
    files.push_back("/uscms_data/d1/rappocc/qcd_470/ca_pat_slim_220_1.root");
  }
  else if ( sample == "qcd_600" ) {
    iweight = 4;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_600/ca_pat_slim_220_9.root");
  }
  else if ( sample == "qcd_800" ) {
    iweight = 5;
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_6.root");
  }
  else if ( sample == "qcd_1000" ) {
    iweight = 6;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_11.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_12.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1000/ca_pat_slim_220_9.root");
  }
  else if ( sample == "qcd_1400" ) {
    iweight = 7;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_1800" ) {
    iweight = 8;
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_2200" ) {
    iweight = 9;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_11.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_12.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_2200/ca_pat_slim_220_9.root");

    //     files.push_back("/uscms_data/d1/rappocc/qcd_2200/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_2200/ca_pat_slim_220_4.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_2200/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_2600" ) {
    iweight = 10;
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_3000" ) {
    iweight = 11;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_11.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_12.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3000/ca_pat_slim_220_9.root");

    //     files.push_back("/uscms_data/d1/rappocc/qcd_3000/ca_pat_slim_220_2.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3000/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3000/ca_pat_slim_220_4.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3000/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_3500" ) {
    iweight = 12;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_11.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_12.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_8.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_3500/ca_pat_slim_220_9.root");


    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_1.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_2.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_4.root");
  }else if ( sample == "zjets" ) {
    iweight = 13;

    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_10.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_11.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_12.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_13.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_14.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_15.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_16.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_17.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_18.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_19.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_20.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_21.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_23.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_24.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_4.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_5.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_6.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_7.root");
    files.push_back("/uscms/home/rappocc/nobackup/TopTagging/zjets/ca_pat_slim_220_9.root");


    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_1.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_2.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d1/rappocc/qcd_3500/ca_pat_slim_220_4.root");
  }


  double weights[] = {
    10623.2,
    2634.94,
    722.099,
    240.983,
    62.4923,
    9.42062,
    2.34357,
    0.1568550,
    0.013811,
    0.00129608,
    0.00011404,
    0.0000084318,
    0.00000018146,
    3700.0
  };


  int nevents[] = {
    54000,
    54000,
    51840,
    27648,
    28620,
    20880,
    24640,
    27744,
    22848,
    22560,
    22800,
    20880,
    34320,
    1287404
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


  PredictedDistribution * total_pred     = new PredictedDistribution("total",  "Total Rate", 2, 0, 2 );
  PredictedDistribution * jet_et_pred    = new PredictedDistribution( "jet_et", "Predicted Jet E_{T}", 50, 0, 5000 );
  PredictedDistribution * jet_eta_pred   = new PredictedDistribution( "jet_eta", "Predicted Jet #eta", 30, -3.0, 3.0 );
  PredictedDistribution * jet_phi_pred   = new PredictedDistribution( "jet_phi", "Predicted Jet #phi", 30, -3.14159, 3.14159 );
  PredictedDistribution * dijetmass_pred = new PredictedDistribution("dijetmass", "Predicted Dijet Mass", 50, 0, 5000);
  
  total_pred->SetRateMatrix( parameterization );
  jet_et_pred->SetRateMatrix( parameterization );
  jet_eta_pred->SetRateMatrix( parameterization );
  jet_phi_pred->SetRateMatrix( parameterization );
  dijetmass_pred->SetRateMatrix( parameterization );
  
  cout << "About to loop" << endl;
  
  fwlite::ChainEvent ev(files);
  
  // Loop over events
  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {


    if ( ev.getBranchDescriptions().size() <= 0 ) continue;

    // Select a subset of the events for a pseudoexperiment
    // based on the desired luminosity. 
    if ( pseudoExp ) {
      double fi = gRandom->Uniform();
      if ( fi >= pe_factor ) continue;
    }


    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    unsigned int eventNumber = ev.id().event();


    // get the jets
    fwlite::Handle<std::vector<pat::Jet> > h_jet;

//     cout << "About to get handle" << endl;
    h_jet   .getByLabel(ev,"selectedLayer1Jets");

//     cout << "Done getting handle" << endl;
    if ( (eventNumber % 2 == 1) || processAll ) continue; // Take even events, odd were used to make this matrix
    if ( !h_jet.isValid() ) continue;     // Make sure we have a handle

//     cout << "Got handle, dereferencing" << endl;
    vector<pat::Jet> const & jets = *h_jet;

    // require dijet events
    if ( jets.size() == 2 && njets == 2 ) {
//       cout << "Have 2 jets" << endl;
      pat::Jet const & jet1 = jets[0];
      pat::Jet const & jet2 = jets[1];

      const reco::CATopJetTagInfo * catopTag1 = dynamic_cast<CATopJetTagInfo const *> (jet1.tagInfo("CATopJetTagger"));
      const reco::CATopJetTagInfo * catopTag2 = dynamic_cast<CATopJetTagInfo const *> (jet2.tagInfo("CATopJetTagger"));

      double topMass1 = catopTag1->properties().topMass;
      double wMass1 = catopTag1->properties().wMass;
      double minMass1 = catopTag1->properties().minMass;

      double topMass2 = catopTag2->properties().topMass;
      double wMass2 = catopTag2->properties().wMass;
      double minMass2 = catopTag2->properties().minMass;

      TLorentzVector v1(jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );
      TLorentzVector v2(jet2.px(), jet2.py(), jet2.pz(), jet2.energy() );

      TLorentzVector v = v1 + v2;

      // get the tag quantities
      bool tagged1 = 
	(topMass1 >= topMassCut1 && topMass1 <= topMassCut2) &&
	(wMass1   >= wMassCut1   && wMass1   <= wMassCut2  ) &&
	(minMass1 >= minMassCut1 && minMass1 <= minMassCut2);

      bool tagged2 = 
	(topMass2 >= topMassCut1 && topMass2 <= topMassCut2) &&
	(wMass2   >= wMassCut1   && wMass2   <= wMassCut2  ) &&
	(minMass2 >= minMassCut1 && minMass2 <= minMassCut2);

      if ( v.Mag() > 2000 ) {
	int bin1 = parameterization->FindBin(jet1.et() );
	int bin2 = parameterization->FindBin(jet2.et() );
	cout << "v.Mag() = " << v.Mag() << endl;
	cout << "jet1.p4 = " << v1 << endl;
	cout << "bin1    = " << bin1 << endl;
	cout << "rate1   = " << parameterization->GetBinContent(bin1) << " +- " << parameterization->GetBinError(bin1) << endl;
	cout << "jet2.p4 = " << v2 << endl;
	cout << "bin2    = " << bin2 << endl;
	cout << "rate2   = " << parameterization->GetBinContent(bin2) << " +- " << parameterization->GetBinError(bin2) << endl;
	
      }

      if ( !tagged1 ) {
	total_pred->Accumulate( 1.0, jet2.et(), tagged2 );
	jet_et_pred->Accumulate( jet2.et(), jet2.et(), tagged2  );
	jet_eta_pred->Accumulate( jet2.eta(), jet2.et(), tagged2  );
	jet_phi_pred->Accumulate( jet2.phi(), jet2.et(), tagged2  );
	dijetmass_pred->Accumulate( v.Mag(), jet2.et(), tagged2  );
      }
      
      if ( !tagged2 ) {
	total_pred->Accumulate( 1.0, jet1.et(), tagged1 );
	jet_et_pred->Accumulate( jet1.et(), jet1.et(), tagged1  );
	jet_eta_pred->Accumulate( jet1.eta(), jet1.et(), tagged1  );
	jet_phi_pred->Accumulate( jet1.phi(), jet1.et(), tagged1  );
	dijetmass_pred->Accumulate( v.Mag(), jet1.et(), tagged1  );
      }



    }

//     else if ( jets.size() == 1 && njets == 1 ) {

// //       cout << "Have 1 jet" << endl;
//       pat::Jet const & jet1 = jets[0];

//       const reco::CATopJetTagInfo * catopTag1 = dynamic_cast<CATopJetTagInfo const *> (jet1.tagInfo("CATopJetTagger"));

//       double topMass1 = catopTag1->properties().topMass;
//       double wMass1 = catopTag1->properties().wMass;
//       double minMass1 = catopTag1->properties().minMass;

//       TLorentzVector v1(jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );

//       // get the tag quantities
//       bool tagged1 = 
// 	(topMass1 >= topMassCut1 && topMass1 <= topMassCut2) &&
// 	(wMass1   >= wMassCut1   && wMass1   <= wMassCut2  ) &&
// 	(minMass1 >= minMassCut1 && minMass1 <= minMassCut2);

//       total_pred->Accumulate( 1.0, jet1.et(), tagged1 );
//       jet_et_pred->Accumulate( jet1.et(), jet1.et(), tagged1  );
//       jet_eta_pred->Accumulate( jet1.eta(), jet1.et(), tagged1  );
//       jet_phi_pred->Accumulate( jet1.phi(), jet1.et(), tagged1  );

//     }
    


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
  
  dijetmass_pred->SetCalculatedErrors();
//   dijetmass_pred->Normalize();

  cout << "About to draw" << endl;
  
  TString fname ("xchecks_");
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

  dijetmass_pred->GetPredictedHist()->Write();
  dijetmass_pred->GetObservedHist()->Write();
  dijetmass_pred->GetTaggableHist()->Write();


  f->Close();

  delete total_pred;
  delete jet_et_pred;
  delete jet_eta_pred;
  delete jet_phi_pred;
  delete dijetmass_pred;

  delete f;

}
