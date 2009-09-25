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
#include <fstream>

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
			     bool processAll = false,
			     bool useJEC = true,
			     double topMassCut1 = 100, double topMassCut2 = 250,
			     double wMassCut1 = 0, double wMassCut2 = 99999.0,
			     double minMassCut1 = 50.0, double minMassCut2 = 99999.0)
{
   

  cout << "Processing sample = " << sample << endl;
  vector<string> files;
  int isample = -1;



  if ( sample == "ttbar_v6_fixed" ) {
    isample = 13;
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v6_fixed/ca_pat_slim_223_9.root");
  }

  else if ( sample == "qcd_230_v6_fixed" ) {
    isample = 0;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v6_fixed/ca_pat_slim_223_9.root");
  }

  else if ( sample == "qcd_300_v6_fixed") {
    isample = 1;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v6_fixed/ca_pat_slim_223_9.root");
  }

  else if ( sample == "qcd_380_v6_fixed" ) {
    isample = 2;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_470_v6_fixed" ) {
    isample = 3;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_600_v6_fixed" ) {
    isample = 4;
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

  else if ( sample == "qcd_800_v6_fixed" ) {
    isample = 5;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_1000_v6_fixed" ) {
    isample = 6;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_1400_v6_fixed" ) {
    isample = 7;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_1800_v6_fixed" ) {
    isample = 8;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_2200_v6_fixed" ) {
    isample = 9;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_2600_v6_fixed" ) {
    isample = 10;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_3000_v6_fixed" ) {
    isample = 11;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v6_fixed/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_3500_v6_fixed" ) {
    isample = 12;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v6_fixed/ca_pat_slim_223_9.root");
      }



  else if ( sample == "wjets_inclusive_200_v6_fixed2" ) {
    isample = 14;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_10.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/PYTHIA6_Winclusive_200_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_9.root");



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
    0.00000018146,
    317. * 1.4,
    74.68,
    3700
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
    1028322,
    100000,
    1287404    
  };

  double weight = weights[isample];
  int nevent = nevents[isample];
  

  const char * output_name = ( processAll ? "mistag_rate_output.txt" : "mistag_rate_output_odd.txt" );
  ofstream output(output_name, ios_base::app);

//   TH2D * numerator   = new TH2D("numerator",   "Fake Tag Parameterization Numerator",   50, 0, 5000, 30, -3.0, 3.0 );
//   TH2D * denominator = new TH2D("denominator", "Fake Tag Parameterization Denominator", 50, 0, 5000, 30, -3.0, 3.0 );


  Double_t PtBins[] = {
    0,
    250,
    275,
    300,
    325,
    350,
    375,
    400,
    450,
    500,
    550,
    600,
    650,
    700,
    750,
    800,
    900,
    1000,
    1200,
    1600,
    2000
  };


  static const int nPtBins = sizeof( PtBins ) / sizeof( Double_t );

  
  Double_t ptMax = PtBins[nPtBins - 1];

  TH1D * numerator   = new TH1D("numerator",   "Fake Tag Parameterization Numerator",   nPtBins-1, PtBins );
  TH1D * denominator = new TH1D("denominator", "Fake Tag Parameterization Denominator", nPtBins-1, PtBins );
  TH2D * numerator2d   = new TH2D("numerator2d",   "Fake Tag Parameterization Numerator",   nPtBins-1, PtBins, 20, -3.0, 3.0 );
  TH2D * denominator2d = new TH2D("denominator2d", "Fake Tag Parameterization Denominator", nPtBins-1, PtBins, 20, -3.0, 3.0 );

  numerator->Sumw2();
  denominator->Sumw2();
  numerator2d->Sumw2();
  denominator2d->Sumw2();
  
  fwlite::ChainEvent ev(files);

  unsigned int ntotal = 0;
  unsigned int n1jet = 0;
  unsigned int n2jet = 0;
  unsigned int ntopmass = 0;
  unsigned int nminmass = 0;

  
  // Loop over events
  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {
    

    unsigned int eventNumber = ev.id().event();

    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    if ( eventNumber % 2 == 0 && !processAll ) continue; // Leave even events for closure tests

    // get the jets
    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    if ( !h_jet.isValid() ) continue;     // Make sure we have a handle

    ++ntotal;

    vector<pat::Jet> const & jets = *h_jet;

    if ( jets.size() >= 1 )
      ++n1jet;


    // require dijet events
    if ( jets.size() == 2 ) {
      ++n2jet;
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


      double corrF1 = 1.0;
      double corrF2 = 1.0;


      if ( !useJEC ) {
	corrF1 = jet1.corrFactor( jet1.corrStep() );
	corrF2 = jet2.corrFactor( jet1.corrStep() );
      }

      // If jet 1 is antitagged, fill jet 2
      if ( !tagged1 ) {
	double jet2pt = jet2.pt() / corrF2;
	denominator->Fill( jet2pt,  weight / (double)nevent );
	denominator2d->Fill( jet2pt, jet2.rapidity(), weight / (double)nevent);
	if ( tagged2 ) {
	  numerator->Fill( jet2pt,  weight / (double)nevent );
	  numerator2d->Fill( jet2pt, jet2.rapidity(), weight / (double)nevent);
	}
      } 
      // If jet 2 is antitagged, fill jet 1
      if ( !tagged2 ) {
	double jet1pt = jet1.pt() / corrF1;
	denominator->Fill( jet1pt,  weight / (double)nevent );
	denominator2d->Fill( jet1pt, jet1.rapidity(), weight / (double)nevent);
	if ( tagged1 ) {
	  numerator->Fill( jet1pt,  weight / (double)nevent );
	  numerator2d->Fill( jet1pt, jet1.rapidity(), weight / (double)nevent);
	}
      } 


      // get the tag quantities
      
      if (topMass1 >= topMassCut1 && topMass1 <= topMassCut2 &&
	  topMass2 >= topMassCut1 && topMass2 <= topMassCut2 ) {
	++ntopmass;

	if (minMass1 >= minMassCut1 && minMass1 <= minMassCut2 &&
	    minMass2 >= minMassCut1 && minMass2 <= minMassCut2 ) 
	  ++nminmass;
      }

    }
  }
  
  char buff[2000];
  sprintf(buff, " %30s & %6d & %6d & %6d & %6d & %6.0f & %6.0f",
	  sample.c_str(), n1jet, n2jet, ntopmass, nminmass, denominator->GetEntries(), numerator->GetEntries() );
  output << buff << endl;
  cout << buff << endl;

  cout << "Number of events considered = " << ntotal << endl;
  cout << "Number of >= 1-jet events   = " << n1jet << endl;
  cout << "Number of == 2-jet events   = " << n2jet << endl;
  cout << "Number of events with 2 jets that pass top mass cut = " << ntopmass << endl;
  cout << "Number of events with 2 jets that pass top mass cut and min mass cut = " << nminmass << endl;

  cout << "Number of events in anti-tagged + X sample = " << denominator->GetEntries() << endl;
  cout << "Number of events in anti-tagged + tagged sample = " << numerator->GetEntries() << endl;


  cout << "About to book output file" << endl;
  TString fname ("mistag_parameterization_");
  fname += sample;
  if ( !processAll ) {
    fname += "_odd";
  }
  if ( !useJEC ) {
    fname += "_uncorr";
  }
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();


  cout << "About to write" << endl;
  numerator->Write();
  denominator->Write();
  numerator2d->Write();
  denominator2d->Write();

  cout << "About to close, and delete" << endl;
  f->Close();

  delete numerator;
  delete denominator;
  delete numerator2d;
  delete denominator2d;
  delete f;


  cout << "Exiting" << endl;
}
