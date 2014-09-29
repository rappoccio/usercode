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

void dijet_analysis_mistag_prediction_fwlite(TH1D * parameterization,
					     string sample = "qcd_230_v5",
					     bool processAll = false,
					     bool pseudoExp = true,
					     double Lum = 1.0,
					     int njets = 2,
					     double topMassCut1 = 100, double topMassCut2 = 250,
					     double wMassCut1 = 0, double wMassCut2 = 99999.0,
					     double minMassCut1 = 50.0, double minMassCut2 = 99999.0)
{
  
using namespace std;
using namespace reco;
using namespace edm;

  cout << "Processing sample = " << sample << endl;
  vector<string> files;

  int isample = -1;





   if ( sample == "qcd_230_v5" ) {
    isample = 0;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_230_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_300_v5" ) {
    isample = 1;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_300_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_380_v5" ) {
    isample = 2;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_380_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_470_v5" ) {
    isample = 3;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_470_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_600_v5" ) {
    isample = 4;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_600_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_800_v5" ) {
    isample = 5;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_800_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_1000_v5" ) {
    isample = 6;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1000_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_1400_v5" ) {
    isample = 7;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1400_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_1800_v5" ) {
    isample = 8;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_1800_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_2200_v5" ) {
    isample = 9;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2200_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_2600_v5" ) {
    isample = 10;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_2600_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_3000_v5" ) {
    isample = 11;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3000_v5/ca_pat_slim_223_9.root");
      }

  else if ( sample == "qcd_3500_v5" ) {
    isample = 12;
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/qcd_3500_v5/ca_pat_slim_223_9.root");
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

  double weight = weights[isample];
  int nevent = nevents[isample];

  // Weight to the desired luminosity. Sometimes this scales up,
  // and sometimes it scales down.
  double predicted_weight = weight * Lum / (double)nevent;

  // Calculate the effective luminosity generated
  double lum_eff = (double)nevent / weight; 

  // Note! For an ensemble test, need to reweight the distributions
  // to account for the luminosity discrepancy.
  // To do a proper statistical treatment, we need to "throw"
  // pseudo experiments via which to make a prediction. 

  double pe_factor = Lum / lum_eff;

  // Make sure the pseudoexperiments always choose the same seed
  // for reproducability. 
  if ( pseudoExp && pe_factor < 1.0 ) {
    // Set the weight for the summation to be 1.0 if we're doing
    // pseudoexperiments.
    predicted_weight = 1.0;
    gRandom->SetSeed( seeds[isample] );

    cout << "Skipping to every " << 1.0 / pe_factor << " event" << endl;
  }

  cout << "Desired lum   = " << Lum << endl;
  cout << "Generated lum = " << lum_eff << endl;
  cout << "Ratio         = " << pe_factor << endl;
  cout << "Scaling predictions by " << predicted_weight << endl;
  


  PredictedDistribution * total_pred     = new PredictedDistribution("total",  "Total Rate", 2, 0, 2 );
  PredictedDistribution * jet_et_pred    = new PredictedDistribution( "jet_et", "Predicted Jet E_{T}", 50, 0, 5000 );
  PredictedDistribution * jet_eta_pred   = new PredictedDistribution( "jet_eta", "Predicted Jet #eta", 30, -3.0, 3.0 );
  PredictedDistribution * jet_phi_pred   = new PredictedDistribution( "jet_phi", "Predicted Jet #phi", 30, -3.14159, 3.14159 );
  PredictedDistribution * dijetmass_pred = new PredictedDistribution("dijetmass", "Predicted Dijet Mass", 100, 0, 5000);
  
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

    // Select a subset of the events for a pseudoexperiment
    // based on the desired luminosity. 
    if ( pseudoExp && pe_factor < 1.0 ) {
      double fi = gRandom->Uniform();
      if ( fi >= pe_factor ) continue;
    }


    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    unsigned int eventNumber = ev.id().event();

//     cout << "Getting the handle" << endl;
    // get the jets
    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    if ( !h_jet.isValid() ) continue;     // Make sure we have a handle

//     cout << "Dereferencing jets" << endl;
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

//       cout << "Tagged 1 = " << tagged1 << ", tagged2 = " << tagged2 << ", predicted_weight = " << predicted_weight << endl;
//       cout << "Jet1 Et = " << jet1.et() << ", Jet2 Et = " << jet2.et() << endl;

      if ( tagged1 ) {
	total_pred->Accumulate( 1.0, jet2.et(), tagged2 , predicted_weight );
	jet_et_pred->Accumulate( jet2.et(), jet2.et(), tagged2  , predicted_weight );
	jet_eta_pred->Accumulate( jet2.eta(), jet2.et(), tagged2  , predicted_weight );
	jet_phi_pred->Accumulate( jet2.phi(), jet2.et(), tagged2  , predicted_weight );
	dijetmass_pred->Accumulate( v.Mag(), jet2.et(), tagged2  , predicted_weight );
      }
      
      if ( tagged2 ) {
	total_pred->Accumulate( 1.0, jet1.et(), tagged1 , predicted_weight );
	jet_et_pred->Accumulate( jet1.et(), jet1.et(), tagged1  , predicted_weight );
	jet_eta_pred->Accumulate( jet1.eta(), jet1.et(), tagged1  , predicted_weight );
	jet_phi_pred->Accumulate( jet1.phi(), jet1.et(), tagged1  , predicted_weight );
	dijetmass_pred->Accumulate( v.Mag(), jet1.et(), tagged1  , predicted_weight );
      }

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
  
  dijetmass_pred->SetCalculatedErrors();
//   dijetmass_pred->Normalize();

  cout << "About to draw" << endl;
  
  TString fname ("mistag_background_");
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
