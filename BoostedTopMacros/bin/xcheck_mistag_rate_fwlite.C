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

  int isample = -1;



  if ( sample == "qcd_230_v6_fixed" ) {
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


  else if ( sample == "wjets_v6_fixed2" ) {
    isample = 14;
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_100.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_101.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_102.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_103.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_104.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_105.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_106.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_107.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_108.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_109.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_110.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_11.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_12.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_13.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_14.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_15.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_16.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_17.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_18.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_19.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_1.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_20.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_21.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_22.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_23.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_24.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_25.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_26.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_27.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_28.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_29.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_2.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_30.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_31.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_32.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_33.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_34.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_35.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_36.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_37.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_38.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_39.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_3.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_40.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_41.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_42.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_43.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_44.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_45.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_46.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_47.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_48.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_49.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_4.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_50.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_51.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_52.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_53.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_54.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_55.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_56.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_57.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_58.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_59.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_5.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_60.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_61.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_62.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_63.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_64.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_65.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_66.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_67.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_68.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_69.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_6.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_70.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_71.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_72.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_73.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_74.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_75.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_76.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_77.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_78.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_79.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_7.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_80.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_81.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_82.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_83.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_84.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_85.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_86.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_87.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_88.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_89.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_8.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_90.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_91.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_92.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_93.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_94.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_95.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_96.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_97.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_98.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_99.root");
files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/wjets_fullsim_v6_fixed2/ca_pat_slim_223_9.root");


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
    3700.0,
    40e3
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
    1287404,
    10307094
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
    168572,
    592834
  };

  double weight = weights[isample];
  int nevent = nevents[isample];

  // Calculate the effective luminosity generated
  double lum_eff = (double)nevent / weight; 

  // Note! For an ensemble test, need to reweight the distributions
  // to account for the luminosity discrepancy.
  // To do a proper statistical treatment, we need to "throw"
  // pseudo experiments via which to make a prediction. 

  double pe_factor = Lum / lum_eff;

  double fillWeight = weight / (double)nevent * Lum;

  cout << "Fill weight 1 = " << fillWeight << endl;
  // Make sure the pseudoexperiments always choose the same seed
  // for reproducability. 
  if ( pseudoExp ) {
    gRandom->SetSeed( seeds[isample] );
    if ( fillWeight < 1.0 )
      fillWeight = 1.0; 

    cout << "Effective lum = " << lum_eff << endl;
    cout << "Desired lum   = " << Lum << endl;
    cout << "Skipping every " << 1.0 / pe_factor << " events" << endl;
  } else {
    fillWeight = 1.0;
  }
  cout << "Fill weight 2 = " << fillWeight << endl;
  
  using namespace std;
  using namespace reco;
  using namespace edm;


  PredictedDistribution * total_pred     = new PredictedDistribution( parameterization, "total",  "Total Rate", 2, 0, 2 );
  PredictedDistribution * jet_pt_pred    = new PredictedDistribution( parameterization, "jet_pt", "Predicted Jet p_{T}", 50, 0, 5000 );
  PredictedDistribution * jet_eta_pred   = new PredictedDistribution( parameterization, "jet_eta", "Predicted Jet #eta", 30, -3.0, 3.0 );
  PredictedDistribution * jet_phi_pred   = new PredictedDistribution( parameterization, "jet_phi", "Predicted Jet #phi", 30, -3.14159, 3.14159 );
  PredictedDistribution * dijetmass_pred = new PredictedDistribution( parameterization, "dijetmass", "Predicted Dijet Mass", 50, 0, 5000);
  
  PredictedDistribution * subjet_pt1 = new PredictedDistribution( parameterization, "subjet_pt1", "Subjet 1 p_{T}", 50, 0, 5000);
  PredictedDistribution * subjet_pt2 = new PredictedDistribution( parameterization, "subjet_pt2", "Subjet 2 p_{T}", 50, 0, 5000);
  PredictedDistribution * subjet_pt3 = new PredictedDistribution( parameterization, "subjet_pt3", "Subjet 3 p_{T}", 50, 0, 5000);

  PredictedDistribution * subjet_dr1 = new PredictedDistribution( parameterization, "subjet_dr1", "Subjet 1 #Delta R", 50, 0, 1.0);
  PredictedDistribution * subjet_dr2 = new PredictedDistribution( parameterization, "subjet_dr2", "Subjet 2 #Delta R", 50, 0, 1.0);
  PredictedDistribution * subjet_dr3 = new PredictedDistribution( parameterization, "subjet_dr3", "Subjet 3 #Delta R", 50, 0, 1.0);
  
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



      reco::Jet::Constituents constituents1 = jet1.getJetConstituents();
      reco::Jet::Constituents constituents2 = jet2.getJetConstituents();


      vector<TLorentzVector> subjets1_p4s;

      if ( constituents1.size() > 0 ) 
	subjets1_p4s.push_back( TLorentzVector( constituents1[0]->px(),constituents1[0]->py(),constituents1[0]->pz(),constituents1[0]->energy() ) );
      if ( constituents1.size() > 1 ) 
	subjets1_p4s.push_back( TLorentzVector( constituents1[1]->px(),constituents1[1]->py(),constituents1[1]->pz(),constituents1[1]->energy() ) );
      if ( constituents1.size() > 2 ) 
	subjets1_p4s.push_back( TLorentzVector( constituents1[2]->px(),constituents1[2]->py(),constituents1[2]->pz(),constituents1[2]->energy() ) );

      vector<TLorentzVector> subjets2_p4s;

      if ( constituents2.size() > 0 ) 
	subjets2_p4s.push_back( TLorentzVector( constituents2[0]->px(),constituents2[0]->py(),constituents2[0]->pz(),constituents2[0]->energy() ) );
      if ( constituents2.size() > 1 ) 
	subjets2_p4s.push_back( TLorentzVector( constituents2[1]->px(),constituents2[1]->py(),constituents2[1]->pz(),constituents2[1]->energy() ) );
      if ( constituents2.size() > 2 ) 
	subjets2_p4s.push_back( TLorentzVector( constituents2[2]->px(),constituents2[2]->py(),constituents2[2]->pz(),constituents2[2]->energy() ) );

//       if ( true ) {
// 	int bin1 = parameterization->FindBin(jet1.pt() );
// 	int bin2 = parameterization->FindBin(jet2.pt() );
// 	cout << "v.Mag() = " << v.Mag() << endl;
// 	cout << "jet1.p4 = " << v1 << endl;
// 	cout << "bin1    = " << bin1 << endl;
// 	cout << "rate1   = " << parameterization->GetBinContent(bin1) << " +- " << parameterization->GetBinError(bin1) << endl;
// 	cout << "jet2.p4 = " << v2 << endl;
// 	cout << "bin2    = " << bin2 << endl;
// 	cout << "rate2   = " << parameterization->GetBinContent(bin2) << " +- " << parameterization->GetBinError(bin2) << endl;
	
//       }

      if ( !tagged1 ) {
	total_pred->Accumulate( 1.0, jet2.pt(), tagged2, fillWeight );
	jet_pt_pred->Accumulate( jet2.pt(), jet2.pt(), tagged2 , fillWeight );
	jet_eta_pred->Accumulate( jet2.eta(), jet2.pt(), tagged2 , fillWeight );
	jet_phi_pred->Accumulate( jet2.phi(), jet2.pt(), tagged2 , fillWeight );
	dijetmass_pred->Accumulate( v.Mag(), jet2.pt(), tagged2 , fillWeight );

	if ( subjets2_p4s.size() > 0 ) {
	  subjet_pt1->Accumulate( subjets2_p4s[0].Perp(), jet2.pt(), tagged2, fillWeight );
	  subjet_dr1->Accumulate( subjets2_p4s[0].DeltaR(v2) , jet2.pt(), tagged2, fillWeight );
	}
	if ( subjets2_p4s.size() > 1 ) {
	  subjet_pt2->Accumulate( subjets2_p4s[1].Perp(), jet2.pt(), tagged2, fillWeight );
	  subjet_dr2->Accumulate( subjets2_p4s[1].DeltaR(v2) , jet2.pt(), tagged2, fillWeight );
	}
	if ( subjets2_p4s.size() > 2 ) {
	  subjet_pt3->Accumulate( subjets2_p4s[2].Perp(), jet2.pt(), tagged2, fillWeight );
	  subjet_dr3->Accumulate( subjets2_p4s[2].DeltaR(v2) , jet2.pt(), tagged2, fillWeight );
	}

      }
      
      if ( !tagged2 ) {
	total_pred->Accumulate( 1.0, jet1.pt(), tagged1 , fillWeight);
	jet_pt_pred->Accumulate( jet1.pt(), jet1.pt(), tagged1  , fillWeight);
	jet_eta_pred->Accumulate( jet1.eta(), jet1.pt(), tagged1  , fillWeight);
	jet_phi_pred->Accumulate( jet1.phi(), jet1.pt(), tagged1  , fillWeight);
	dijetmass_pred->Accumulate( v.Mag(), jet1.pt(), tagged1  , fillWeight);

	if ( subjets1_p4s.size() > 0 ) {
	  subjet_pt1->Accumulate( subjets1_p4s[0].Perp(), jet1.pt(), tagged1, fillWeight );
	  subjet_dr1->Accumulate( subjets1_p4s[0].DeltaR(v1) , jet1.pt(), tagged1, fillWeight );
	}
	if ( subjets1_p4s.size() > 1 ) {
	  subjet_pt2->Accumulate( subjets1_p4s[1].Perp(), jet1.pt(), tagged1, fillWeight );
	  subjet_dr2->Accumulate( subjets1_p4s[1].DeltaR(v1) , jet1.pt(), tagged1, fillWeight );
	}
	if ( subjets1_p4s.size() > 2 ) {
	  subjet_pt3->Accumulate( subjets1_p4s[2].Perp(), jet1.pt(), tagged1, fillWeight );
	  subjet_dr3->Accumulate( subjets1_p4s[2].DeltaR(v1) , jet1.pt(), tagged1, fillWeight );
	}



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

  jet_pt_pred->SetCalculatedErrors();
//   jet_et_pred->Normalize();
  
  jet_eta_pred->SetCalculatedErrors();
//   jet_eta_pred->Normalize();
  
  jet_phi_pred->SetCalculatedErrors();
//   jet_phi_pred->Normalize();
  
  dijetmass_pred->SetCalculatedErrors();
//   dijetmass_pred->Normalize();

  subjet_pt1->SetCalculatedErrors();
  subjet_pt2->SetCalculatedErrors();
  subjet_pt3->SetCalculatedErrors();

  subjet_dr1->SetCalculatedErrors();
  subjet_dr2->SetCalculatedErrors();
  subjet_dr3->SetCalculatedErrors();

  cout << "About to draw" << endl;
  
  TString fname ("xchecks_");
  fname += sample;
  if ( pseudoExp == false ) 
    fname += "_noPE";
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();

  total_pred->GetPredictedHist()->Write();
  total_pred->GetObservedHist()->Write();
  total_pred->GetTaggableHist()->Write();

  jet_pt_pred->GetPredictedHist()->Write();
  jet_pt_pred->GetObservedHist()->Write();
  jet_pt_pred->GetTaggableHist()->Write();

  jet_eta_pred->GetPredictedHist()->Write();
  jet_eta_pred->GetObservedHist()->Write();
  jet_eta_pred->GetTaggableHist()->Write();

  jet_phi_pred->GetPredictedHist()->Write();
  jet_phi_pred->GetObservedHist()->Write();
  jet_phi_pred->GetTaggableHist()->Write();

  dijetmass_pred->GetPredictedHist()->Write();
  dijetmass_pred->GetObservedHist()->Write();
  dijetmass_pred->GetTaggableHist()->Write();

  subjet_pt1->GetPredictedHist()->Write();
  subjet_pt1->GetObservedHist()->Write();
  subjet_pt1->GetTaggableHist()->Write();

  subjet_pt2->GetPredictedHist()->Write();
  subjet_pt2->GetObservedHist()->Write();
  subjet_pt2->GetTaggableHist()->Write();

  subjet_pt3->GetPredictedHist()->Write();
  subjet_pt3->GetObservedHist()->Write();
  subjet_pt3->GetTaggableHist()->Write();

  subjet_dr1->GetPredictedHist()->Write();
  subjet_dr1->GetObservedHist()->Write();
  subjet_dr1->GetTaggableHist()->Write();

  subjet_dr2->GetPredictedHist()->Write();
  subjet_dr2->GetObservedHist()->Write();
  subjet_dr2->GetTaggableHist()->Write();

  subjet_dr3->GetPredictedHist()->Write();
  subjet_dr3->GetObservedHist()->Write();
  subjet_dr3->GetTaggableHist()->Write();

  f->Close();

  delete total_pred;
  delete jet_pt_pred;
  delete jet_eta_pred;
  delete jet_phi_pred;
  delete dijetmass_pred;
  
  delete subjet_pt1;
  delete subjet_pt2;
  delete subjet_pt3;

  delete subjet_dr1;
  delete subjet_dr2;
  delete subjet_dr3;

  delete f;

}
