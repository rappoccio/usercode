#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
// #include <TDCacheFile.h>
#include <TLorentzVector.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

#include <iostream>
#include <fstream>
#include <map>
#include <string>

using namespace std;

struct results {
  results() {
    n1jet_events = 0;
    n2jet_events = 0;
    n1tagged_events = 0;
    n2tagged_events = 0;
    nfiducial_jets = 0;
    ntopmass_jets = 0; 
    nminmass_jets = 0;
  }
  unsigned int n1jet_events ;    // Number of events that pass the filter (i.e. have >= 1 jet with pt > 300, eta < 2.5)
  unsigned int n2jet_events;  // Number of events that have 2 fiducial jets
  unsigned int n1tagged_events;   // Number of events with >= 1 tag
  unsigned int n2tagged_events;   // Number of events with == 2 tags

  unsigned int nfiducial_jets ;   // Number of jets with pt > 300, eta < 2.5
  unsigned int ntopmass_jets ;    // Number of jets that pass top mass criterion
  unsigned int nminmass_jets ;    // Number of jets that pass min mass criterion AND top mass criterion

  friend ostream & operator<<(ostream & out, results const & iresults) {
    char buff[800];
    sprintf(buff, " & %6d & %6d & %6d & %6d & %6d & %6d & %6d \\\\ \n", 
	    iresults.n1jet_events, iresults.n2jet_events, iresults.n1tagged_events, iresults.n2tagged_events,
	    iresults.nfiducial_jets, iresults.ntopmass_jets, iresults.nminmass_jets );
    out << buff;
    return out;
  }
};

void catop_fwlite(string sample = "ttbar",
		  double topMassCut1 = 100, double topMassCut2 = 250,
		  double wMassCut1 = 0, double wMassCut2 = 99999.0,
		  double minMassCut1 = 50.0, double minMassCut2 = 99999.0)
{
   

  cout << "Processing sample = " << sample << endl;
  vector<string> files;

  if ( sample == "ttbar" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_20.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_21.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_22.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_23.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_9.root");
  } else if ( sample == "rs_750" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_20.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_21.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_22.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_750/ca_pat_slim_220_9.root");
  } 
  else if ( sample == "rs_1000" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_20.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_21.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1000/ca_pat_slim_220_9.root");
  }
  else if ( sample == "rs_1250" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_20.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_21.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_22.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/rs_1250/ca_pat_slim_220_9.root");
  }
  else if ( sample == "rs_750_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS750_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1000_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1000_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }

  else if ( sample == "rs_1250_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1500_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1500_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  } 
  else if ( sample == "rs_2000_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS2000_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_2500_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS2500_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_3000_fastsim" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS3000_tt_jetMET_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_heavyfrag_up" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_heavyfrag_down_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_heavyfrag_down" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_heavyfrag_up_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_isrfsr_down" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_isrfsr_down_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_isrfsr_up" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_isrfsr_up_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_lightfrag_down" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_lightfrag_down_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_lightfrag_up" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_lightfrag_up_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_renorm_down" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_renorm_down_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "rs_1250_fastsim_renorm_up" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/RS1250_tt_jetMET_renorm_up_FastSim_PAT/ca_pat_slim_fastsim_220_1.root");
  }
  else if ( sample == "qcd_15" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_15/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_15/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_15/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_15/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_15/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_15/ca_pat_slim_220_6.root");
  }
  else if ( sample == "qcd_20" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_20/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_20/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_20/ca_pat_slim_220_3.root");
  }
  else if ( sample == "qcd_30" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_30/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_30/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_30/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_30/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_50" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_50/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_80" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_80/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_80/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_80/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_80/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_120" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_120/ca_pat_slim_220_1.root");
  }
  else if ( sample == "qcd_170" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_170/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_170/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_170/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_170/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_230" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_230/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_230/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_230/ca_pat_slim_220_3.root");
  }
  else if ( sample == "qcd_300" ) {
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
    files.push_back("/uscms_data/d2/rappocc/qcd_470/ca_pat_slim_220_1.root");
  }
  else if ( sample == "qcd_600" ) {
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
    files.push_back("/uscms_data/d2/rappocc/qcd_800/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_800/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_800/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_800/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_800/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_800/ca_pat_slim_220_6.root");
  }
  else if ( sample == "qcd_1000" ) {
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
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_1.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_2.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_3.root");
    files.push_back("/uscms/home/rappocc/nobackup/qcd_1400/ca_pat_slim_220_4.root");
  }
  else if ( sample == "qcd_1800" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_1800/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_1800/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_1800/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_1800/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_1800/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_2200" ) {
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

    //     files.push_back("/uscms_data/d2/rappocc/TopTagging/qcd_2200/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d2/rappocc/TopTagging/qcd_2200/ca_pat_slim_220_4.root");
    //     files.push_back("/uscms_data/d2/rappocc/TopTagging/qcd_2200/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_2600" ) {
    files.push_back("/uscms_data/d2/rappocc/qcd_2600/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_2600/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_2600/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_2600/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/qcd_2600/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_3000" ) {

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

    //     files.push_back("/uscms_data/d2/rappocc/qcd_3000/ca_pat_slim_220_2.root");
    //     files.push_back("/uscms_data/d2/rappocc/qcd_3000/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d2/rappocc/qcd_3000/ca_pat_slim_220_4.root");
    //     files.push_back("/uscms_data/d2/rappocc/qcd_3000/ca_pat_slim_220_5.root");
  } else if ( sample == "qcd_3500" ) {
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


    //     files.push_back("/uscms_data/d2/rappocc/qcd_3500/ca_pat_slim_220_1.root");
    //     files.push_back("/uscms_data/d2/rappocc/qcd_3500/ca_pat_slim_220_2.root");
    //     files.push_back("/uscms_data/d2/rappocc/qcd_3500/ca_pat_slim_220_3.root");
    //     files.push_back("/uscms_data/d2/rappocc/qcd_3500/ca_pat_slim_220_4.root");
  } else if ( sample == "zprime_m1000_w10" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w10/ca_pat_slim_220_20.root");
  } else if ( sample == "zprime_m2000_w20" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w20/ca_pat_slim_220_20.root");
  } else if ( sample == "zprime_m3000_w30" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w30/ca_pat_slim_220_20.root");
  } else if ( sample == "zprime_m4000_w40" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w40/ca_pat_slim_220_20.root");  
  } else if ( sample == "zprime_m1000_w100" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m1000_w100/ca_pat_slim_220_20.root");
  } else if ( sample == "zprime_m2000_w200" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m2000_w200/ca_pat_slim_220_20.root");
  } else if ( sample == "zprime_m3000_w300" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m3000_w300/ca_pat_slim_220_20.root");
  } else if ( sample == "zprime_m4000_w400" ) {
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_1.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_2.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_3.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_4.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_5.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_6.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_7.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_8.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_9.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_10.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_11.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_12.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_13.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_14.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_15.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_16.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_17.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_18.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_19.root");
    files.push_back("/uscms_data/d2/rappocc/TopTagging/zprime_m4000_w400/ca_pat_slim_220_20.root");
  }





  ofstream tableout("kinematics_output.txt", ios_base::app);
   
  using namespace std;
  using namespace reco;

  TH1D * hist_top_jetEt = new TH1D("hist_top_jetEt", "Jet E_{T}", 100, 0, 5000 );
  TH1D * hist_nontop_jetEt = new TH1D("hist_nontop_jetEt", "Jet E_{T}", 100, 0, 5000 );

  TH1D * hist_top_jetEta = new TH1D("hist_top_jetEta", "Jet #eta", 100, -3.0, 3.0 );
  TH1D * hist_nontop_jetEta = new TH1D("hist_nontop_jetEta", "Jet #eta", 100, -3.0, 3.0);

  TH1D * hist_tagged_top_jetEt = new TH1D("hist_tagged_top_jetEt", "Tagged Jet E_{T}", 100, 0, 5000 );
  TH1D * hist_tagged_nontop_jetEt = new TH1D("hist_tagged_nontop_jetEt", "Tagged Jet E_{T}", 100, 0, 5000 );

  TH1D * hist_tagged_top_jetEta = new TH1D("hist_tagged_top_jetEta", "Tagged Jet #eta", 100, -3.0, 3.0 );
  TH1D * hist_tagged_nontop_jetEta = new TH1D("hist_tagged_nontop_jetEta", "Tagged Jet #eta", 100, -3.0, 3.0);

  TH1D * hist_top_jetMass = new TH1D("hist_top_jetMass", "Jet Mass", 100, 0, 500 );
  TH1D * hist_nontop_jetMass = new TH1D("hist_nontop_jetMass", "Jet Mass", 100, 0, 500 );

  TH1D * hist_top_jetMinMass = new TH1D("hist_top_jetMinMass", "Jet Min Mass", 100, 0, 200 );
  TH1D * hist_nontop_jetMinMass = new TH1D("hist_nontop_jetMinMass", "Jet Min Mass", 100, 0, 200 );

  TH1D * hist_top_jetWMass = new TH1D("hist_top_jetWMass", "Jet W Mass", 100, 0, 200 );
  TH1D * hist_nontop_jetWMass = new TH1D("hist_nontop_jetWMass", "Jet W Mass", 100, 0, 200 );

  TH1D * hist_top_dijetmass = new TH1D("hist_top_dijetmass", "Dijet mass, Untagged", 100, 0, 5000 );
  TH1D * hist_nontop_dijetmass = new TH1D("hist_nontop_dijetmass", "Dijet mass, Untagged", 100, 0, 5000 );

  TH1D * hist_onetagged_top_dijetmass = new TH1D("hist_onetagged_top_dijetmass", "Dijet mass, Single Tagged Events", 100, 0, 5000 );
  TH1D * hist_onetagged_nontop_dijetmass = new TH1D("hist_onetagged_nontop_dijetmass", "Dijet mass, Single Tagged Events", 100, 0, 5000 );

  TH1D * hist_tagged_top_dijetmass = new TH1D("hist_tagged_top_dijetmass", "Dijet mass, Double Tagged Events", 100, 0, 5000 );
  TH1D * hist_tagged_nontop_dijetmass = new TH1D("hist_tagged_nontop_dijetmass", "Dijet mass, Double Tagged Events", 100, 0, 5000 );

  TH2D * hist_top_jetMass_Vs_jetMinMass = new TH2D("hist_top_jetMass_Vs_jetMinMass", 
						"Jet Mass Versus Jet Min Mass, Top Jets",
						100, 0, 500, 100, 0, 200 );

  TH2D * hist_nontop_jetMass_Vs_jetMinMass = new TH2D("hist_nontop_jetMass_Vs_jetMinMass", 
						"Jet Mass Versus Jet Min Mass, Non-Top Jets",
						100, 0, 500, 100, 0, 200 );
  
  results iresults;

  cout << "About to make chain event" << endl;
  
  fwlite::ChainEvent ev(files);
  
  cout << "About to loop" << endl;

  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {


    if ( ev.getBranchDescriptions().size() <= 0 ) continue;

    ++iresults.n1jet_events;

    if ( count % 1000 == 0 ) cout << "Processing event " << count << endl;

    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    if ( !h_jet.isValid() ) continue;


    vector<pat::Jet> const & jets = *h_jet;

    if ( jets.size() >= 2 ) {

      pat::Jet const & jet1 = jets[0];
      pat::Jet const & jet2 = jets[1];
      
      const reco::CATopJetTagInfo * catopTag1 = dynamic_cast<CATopJetTagInfo const *>(jet1.tagInfo("CATopJetTagger"));
      const reco::CATopJetTagInfo * catopTag2 = dynamic_cast<CATopJetTagInfo const *>(jet2.tagInfo("CATopJetTagger"));

      double topMass1 = catopTag1->properties().topMass;
      double wMass1 = catopTag1->properties().wMass;
      double minMass1 = catopTag1->properties().minMass;

      double topMass2 = catopTag2->properties().topMass;
      double wMass2 = catopTag2->properties().wMass;
      double minMass2 = catopTag2->properties().minMass;

      bool tagged1 = 
	(topMass1 >= topMassCut1 && topMass1 <= topMassCut2) &&
	(wMass1   >= wMassCut1   && wMass1   <= wMassCut2  ) &&
	(minMass1 >= minMassCut1 && minMass1 <= minMassCut2);

      bool tagged2 = 
	(topMass2 >= topMassCut1 && topMass2 <= topMassCut2) &&
	(wMass2   >= wMassCut1   && wMass2   <= wMassCut2  ) &&
	(minMass2 >= minMassCut1 && minMass2 <= minMassCut2);

      bool tagged = tagged1 && tagged2; 
      
      TLorentzVector v1(jet1.px(), jet1.py(), jet1.pz(), jet1.energy() );
      TLorentzVector v2(jet2.px(), jet2.py(), jet2.pz(), jet2.energy() );

      TLorentzVector v = v1 + v2;

      double mass = v.Mag();
      if ( abs(jet1.partonFlavour()) == 6 && abs(jet2.partonFlavour() == 6) ) {
	hist_top_dijetmass->Fill( mass );
	if ( tagged ) {
	  hist_tagged_top_dijetmass->Fill( mass );
	} 
	if ( tagged1 || tagged2 ) {
	  hist_onetagged_top_dijetmass->Fill( mass );
	}
      }
      else {
	hist_nontop_dijetmass->Fill( mass );
	if ( tagged ) {
	  hist_tagged_nontop_dijetmass->Fill( mass );
	}
	if ( tagged1 || tagged2 ) {
	  hist_onetagged_nontop_dijetmass->Fill( mass );
	}
      }

      ++iresults.n2jet_events;
      if ( tagged1 || tagged2 ) ++iresults.n1tagged_events;
      if ( tagged1 && tagged2 ) ++iresults.n2tagged_events;
    }

    for ( int i = 0; i < jets.size();  ++i ) {

      ++iresults.nfiducial_jets;

      const reco::CATopJetTagInfo * catopTag = dynamic_cast<CATopJetTagInfo const *>(jets[i].tagInfo("CATopJetTagger"));

      double topMass = catopTag->properties().topMass;
      double wMass = catopTag->properties().wMass;
      double minMass = catopTag->properties().minMass;
      
      if ( topMass >= topMassCut1 && topMass <= topMassCut2 ) {
	++iresults.ntopmass_jets;
	if ( minMass >= minMassCut1 && minMass <= minMassCut2 ) {
	  ++iresults.nminmass_jets;
	}
      }

      bool tagged = 
	(topMass >= topMassCut1 && topMass <= topMassCut2) &&
	(wMass   >= wMassCut1   && wMass   <= wMassCut2  ) &&
	(minMass >= minMassCut1 && minMass <= minMassCut2);
       
      if ( abs(jets[i].partonFlavour()) == 6) {

	hist_top_jetEt->Fill( jets[i].et() );
	hist_top_jetEta->Fill( jets[i].eta() );
	hist_top_jetMass->Fill( topMass );
	hist_top_jetMinMass->Fill( minMass );
	hist_top_jetWMass->Fill( wMass );

	hist_top_jetMass_Vs_jetMinMass->Fill( topMass, minMass );

	if ( tagged ){
	  hist_tagged_top_jetEt->Fill( jets[i].et() );
	  hist_tagged_top_jetEta->Fill( jets[i].eta() );
	}

      }
      else {

	hist_nontop_jetEt->Fill( jets[i].et() );
	hist_nontop_jetEta->Fill( jets[i].eta() );
	hist_nontop_jetMass->Fill( catopTag->properties().topMass );
	hist_nontop_jetMinMass->Fill( catopTag->properties().minMass );
	hist_nontop_jetWMass->Fill( catopTag->properties().wMass );


	hist_nontop_jetMass_Vs_jetMinMass->Fill( topMass, minMass );

	if ( tagged ){
	  hist_tagged_nontop_jetEt->Fill( jets[i].et() );
	  hist_tagged_nontop_jetEta->Fill( jets[i].eta() );
	}
      }
    }

  }

  TString fname ("kinematic_histos_");
  fname += sample;
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();

  hist_nontop_jetEt->Write();
  hist_top_jetEt->Write();

  hist_nontop_jetEta->Write();
  hist_top_jetEta->Write();

  hist_tagged_nontop_jetEt->Write();
  hist_tagged_top_jetEt->Write();

  hist_tagged_nontop_jetEta->Write();
  hist_tagged_top_jetEta->Write();

  hist_nontop_jetMinMass->Write();
  hist_top_jetMinMass->Write();

  hist_nontop_jetMass->Write();
  hist_top_jetMass->Write();

  hist_nontop_jetWMass->Write();
  hist_top_jetWMass->Write();  

  hist_nontop_dijetmass->Write();
  hist_top_dijetmass->Write();

  hist_tagged_nontop_dijetmass->Write();
  hist_tagged_top_dijetmass->Write();

  hist_onetagged_nontop_dijetmass->Write();
  hist_onetagged_top_dijetmass->Write();

  hist_top_jetMass_Vs_jetMinMass->Write();
  hist_nontop_jetMass_Vs_jetMinMass->Write();

  f->Close();



  delete hist_nontop_jetEt;
  delete hist_top_jetEt;

  delete hist_nontop_jetEta;
  delete hist_top_jetEta;

  delete hist_tagged_nontop_jetEt;
  delete hist_tagged_top_jetEt;

  delete hist_tagged_nontop_jetEta;
  delete hist_tagged_top_jetEta;

  delete hist_nontop_jetMinMass;
  delete hist_top_jetMinMass;

  delete hist_nontop_jetMass;
  delete hist_top_jetMass;

  delete hist_nontop_jetWMass;
  delete hist_top_jetWMass;  

  delete hist_nontop_dijetmass;
  delete hist_top_dijetmass;

  delete hist_tagged_nontop_dijetmass;
  delete hist_tagged_top_dijetmass;

  delete hist_onetagged_nontop_dijetmass;
  delete hist_onetagged_top_dijetmass;

  delete hist_top_jetMass_Vs_jetMinMass;
  delete hist_nontop_jetMass_Vs_jetMinMass;

  tableout << sample << " " << iresults;

}


