#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
#include <TDCacheFile.h>
#include <TLorentzVector.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

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

void make_mistag_rate_fwlite(string sample = "ttbar",
			     double topMassCut1 = 100, double topMassCut2 = 250,
			     double wMassCut1 = 0, double wMassCut2 = 99999.0,
			     double minMassCut1 = 50.0, double minMassCut2 = 99999.0)
{
   

  cout << "Processing sample = " << sample << endl;
  vector<string> files;
  int isample = -1;

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
    isample = 0;
    files.push_back("/uscms_data/d1/rappocc/qcd_230/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_230/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_230/ca_pat_slim_220_3.root");
  }
  else if ( sample == "qcd_300" ) {
    isample = 1;
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
    isample = 2;
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
    isample = 3;
    files.push_back("/uscms_data/d1/rappocc/qcd_470/ca_pat_slim_220_1.root");
  }
  else if ( sample == "qcd_600" ) {
    isample = 4;
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
    isample = 5;
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_800/ca_pat_slim_220_6.root");
  }
  else if ( sample == "qcd_1000" ) {
    isample = 6;
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
    isample = 7;
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_1800" ) {
    isample = 8;
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_1800/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_2200" ) {
    isample = 9;
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
    isample = 10;
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d1/rappocc/qcd_2600/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_3000" ) {
    isample = 11;
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
    isample = 12;
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
  }

  
  using namespace std;
  using namespace reco;
  using namespace edm;



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
    0.00000018146
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
    34320
  };

  double weight = weights[isample];
  int nevent = nevents[isample];
  

//   TH2D * numerator   = new TH2D("numerator",   "Fake Tag Parameterization Numerator",   50, 0, 5000, 30, -3.0, 3.0 );
//   TH2D * denominator = new TH2D("denominator", "Fake Tag Parameterization Denominator", 50, 0, 5000, 30, -3.0, 3.0 );

  TH1D * numerator   = new TH1D("numerator",   "Fake Tag Parameterization Numerator",   50, 0, 5000 );
  TH1D * denominator = new TH1D("denominator", "Fake Tag Parameterization Denominator", 50, 0, 5000 );

  numerator->Sumw2();
  denominator->Sumw2();
  
  fwlite::ChainEvent ev(files);
  
  // Loop over events
  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {

    unsigned int eventNumber = ev.id().event();

    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    // get the jets
    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    if ( eventNumber % 2 == 0 ) continue; // Leave even events for closure tests
    if ( !h_jet.isValid() ) continue;     // Make sure we have a handle


    vector<pat::Jet> const & jets = *h_jet;

    // require dijet events
    if ( jets.size() == 2 ) {
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

      // get the tag quantities
      bool tagged1 = 
	(topMass1 >= topMassCut1 && topMass1 <= topMassCut2) &&
	(wMass1   >= wMassCut1   && wMass1   <= wMassCut2  ) &&
	(minMass1 >= minMassCut1 && minMass1 <= minMassCut2);

      bool tagged2 = 
	(topMass2 >= topMassCut1 && topMass2 <= topMassCut2) &&
	(wMass2   >= wMassCut1   && wMass2   <= wMassCut2  ) &&
	(minMass2 >= minMassCut1 && minMass2 <= minMassCut2);

      // If jet 1 is antitagged, fill jet 2
      if ( !tagged1 ) {
	denominator->Fill( jet2.et(), 0.5 );
	if ( tagged2 ) {
	  numerator->Fill( jet2.et(), 0.5 );
	}
      } 
      // If jet 2 is antitagged, fill jet 1
      if ( !tagged2 ) {
	denominator->Fill( jet1.et(), 0.5 );
	if ( tagged1 ) {
	  numerator->Fill( jet1.et(), 0.5 );
	}
      } 

    }
  }
  

  
  TString fname ("mistag_parameterization_");
  fname += sample;
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();

  numerator->Write();
  denominator->Write();

  f->Close();

  delete numerator;
  delete denominator;
  delete f;

}
