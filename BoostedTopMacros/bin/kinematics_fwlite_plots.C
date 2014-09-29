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
		  bool useJEC = true,
		  double topMassCut1 = 100, double topMassCut2 = 250,
		  double wMassCut1 = 0, double wMassCut2 = 99999.0,
		  double minMassCut1 = 50.0, double minMassCut2 = 99999.0)
{
   

  cout << "Processing sample = " << sample << endl;
  vector<string> files;



  if ( sample == "ttbar_v6_fixed" ) {
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


  else if ( sample == "rs_1000_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1000_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_heavyfrag_down_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_heavyfrag_down__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_heavyfrag_up_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_heavyfrag_up__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_isrfsr_down_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_isrfsr_down__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_isrfsr_up_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_isrfsr_up__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_lightfrag_down_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_lightfrag_down__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_lightfrag_up_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_lightfrag_up__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_renorm_down_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_renorm_down__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }


  else if ( sample == "rs_1250_renorm_up_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET_renorm_up__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_1250_v6_fixed") {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1250_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }


  else if ( sample == "rs_1500_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS1500_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_2000_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS2000_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }
  else if ( sample == "rs_2000_v6_local" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS2000_tt_jetMET_v6_local/ca_pat_slim_fastsim_223.root");
  }

  else if ( sample == "rs_2500_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS2500_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_3000_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS3000_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
  }

  else if ( sample == "rs_750_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/RS750_tt_jetMET__FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
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



  else if ( sample == "zprime_fullsim_m1000_w10_v6_widecone" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_widecone/ca_pat_slim_widecone_223_9.root");
  }



  else if ( sample == "zprime_fullsim_m2000_w20_v6_widecone" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w20_v6_widecone/ca_pat_slim_widecone_223_9.root");
  }



  else if ( sample == "zprime_fullsim_m3000_w30_v6_widecone" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w30_v6_widecone/ca_pat_slim_widecone_223_9.root");
  }



  else if ( sample == "zprime_fullsim_m4000_w40_v6_widecone" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_widecone/ca_pat_slim_widecone_223_9.root");
  }

  else if ( sample == "qcd_230_v6_fixed" ) {
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

  else if ( sample == "TTbar_800_1000" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_9.root");
  }

  else if ( sample == "TTbar_800_1000_isrfsr_up" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_up_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_9.root");

  }

  else if ( sample == "TTbar_800_1000_isrfsr_down" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_11.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_12.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_13.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_14.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_15.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_16.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_17.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_18.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_19.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_20.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/PYTHIA6_Tauola_TTbar_800_1000_isrfsr_down_FastSim_PAT_v6_fixed/ca_pat_slim_fastsim_223_9.root");

  }


  else if ( sample == "zprime_fullsim_m1000_w10_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w10_v6_fixed/ca_pat_slim_223_9.root");
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


  else if ( sample == "zprime_fullsim_m4000_w40_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w40_v6_fixed/ca_pat_slim_223_9.root");
  }

  else if ( sample == "zprime_fullsim_m1000_w100_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m1000_w100_v6_fixed/ca_pat_slim_223_9.root");
  }


  else if ( sample == "zprime_fullsim_m2000_w200_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m2000_w200_v6_fixed/ca_pat_slim_223_9.root");
  }

  else if ( sample == "zprime_fullsim_m3000_w300_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m3000_w300_v6_fixed/ca_pat_slim_223_9.root");
  }


  else if ( sample == "zprime_fullsim_m4000_w400_v6_fixed" ) {
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_10.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_1.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_2.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_3.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_4.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_5.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_6.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_7.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_8.root");
files.push_back("/uscms/home/rappocc/nobackup/TopTaggingV2/zprime_fullsim_m4000_w400_v6_fixed/ca_pat_slim_223_9.root");
  }


  else if ( sample == "wjets_inclusive_200_v6_fixed2" ) {
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



  ofstream tableout("kinematics_output.txt", ios_base::app);
   
  using namespace std;
  using namespace reco;
  



  TH1D * hist_top_jetPt = new TH1D("hist_top_jetPt", "Jet p_{T}", 100, 0, 5000 );
  TH1D * hist_nontop_jetPt = new TH1D("hist_nontop_jetPt", "Jet p_{T}", 100, 0, 5000 );

  TH1D * hist_top_jetY = new TH1D("hist_top_jetY", "Jet Rapidity", 100, -3.0, 3.0 );
  TH1D * hist_nontop_jetY = new TH1D("hist_nontop_jetY", "Jet Rapidity", 100, -3.0, 3.0);

  TH1D * hist_top_nSubjet = new TH1D("hist_top_nSubjet", "Number of Subjets", 5, 0, 5);
  TH1D * hist_nontop_nSubjet = new TH1D("hist_nontop_nSubjet", "Number of Subjets", 5, 0, 5);

  TH2D * hist_top_jetPt_vs_jetY = new TH2D("hist_top_jetPt_vs_jetY", "Jet p_{T} Versus Jet Rapidity", 25, 0, 5000, 25, -3.0, 3.0);
  TH2D * hist_nontop_jetPt_vs_jetY = new TH2D("hist_nontop_jetPt_vs_jetY", "Jet p_{T} Versus Jet Rapidity", 25, 0, 5000, 25, -3.0, 3.0);

  TH1D * hist_tagged_top_jetPt = new TH1D("hist_tagged_top_jetPt", "Tagged Jet p_{T}", 100, 0, 5000 );
  TH1D * hist_tagged_nontop_jetPt = new TH1D("hist_tagged_nontop_jetPt", "Tagged Jet p_{T}", 100, 0, 5000 );

  TH1D * hist_tagged_top_jetY = new TH1D("hist_tagged_top_jetY", "Tagged Jet Rapidity", 100, -3.0, 3.0 );
  TH1D * hist_tagged_nontop_jetY = new TH1D("hist_tagged_nontop_jetY", "Tagged Jet Rapidity", 100, -3.0, 3.0);

  TH2D * hist_tagged_top_jetPt_vs_jetY = new TH2D("hist_tagged_top_jetPt_vs_jetY", "Jet p_{T} Versus Jet Rapidity", 25, 0, 5000, 25, -3.0, 3.0);
  TH2D * hist_tagged_nontop_jetPt_vs_jetY = new TH2D("hist_tagged_nontop_jetPt_vs_jetY", "Jet p_{T} Versus Jet Rapidity", 25, 0, 5000, 25, -3.0, 3.0);

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

  TH1D * hist_top_deltaPt = new TH1D("hist_top_deltaPt", "#Delta p_{T}, Untagged", 100, 0, 1000 );
  TH1D * hist_nontop_deltaPt = new TH1D("hist_nontop_deltaPt", "#Delta p_{T}, Untagged", 100, 0, 1000 );

  TH1D * hist_top_jetMinMass_semilep_b = new TH1D("hist_top_jetMinMass_semilep_b", "Jet Min Mass, Events with Semileptonic B Decay", 100, 0, 200);
  TH1D * hist_nontop_jetMinMass_semilep_b = new TH1D("hist_nontop_jetMinMass_semilep_b", "Jet Min Mass, Events with Semileptonic B Decay", 100, 0, 200);

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
//     cout << "Processing event " << count << endl;

    fwlite::Handle<std::vector<pat::Jet> > h_jet;
    fwlite::Handle<std::vector<pat::Muon> > h_muon;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    if ( !h_jet.isValid() ) continue;

    vector<pat::Jet> const & jets = *h_jet;


    h_muon   .getByLabel(ev,"selectedLayer1Muons");

    bool isSemiLep = (h_muon.isValid() && h_muon->size() > 0 );

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


      double corrF1 = 1.0;
      double corrF2 = 1.0;
      if ( !useJEC ) {
        corrF1 = jet1.corrFactor( jet1.corrStep() );
	corrF2 = jet2.corrFactor( jet2.corrStep() );
      }


      bool tagged = tagged1 && tagged2; 
      
      TLorentzVector v1(jet1.px()/corrF1, jet1.py()/corrF1, jet1.pz()/corrF1, jet1.energy()/corrF1 );
      TLorentzVector v2(jet2.px()/corrF2, jet2.py()/corrF2, jet2.pz()/corrF2, jet2.energy()/corrF2 );

      TLorentzVector v = v1 + v2;

      double mass = v.Mag();
      if ( abs(jet1.partonFlavour()) == 6 && abs(jet2.partonFlavour() == 6) ) {
	hist_top_dijetmass->Fill( mass );
	hist_top_deltaPt->Fill( fabs(jet1.pt() - jet2.pt()) );
	if ( tagged ) {
	  hist_tagged_top_dijetmass->Fill( mass );
	} 
	if ( tagged1 || tagged2 ) {
	  hist_onetagged_top_dijetmass->Fill( mass );
	}
      }
      else {
	hist_nontop_dijetmass->Fill( mass );
	hist_nontop_deltaPt->Fill( fabs(jet1.pt() - jet2.pt()) );
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



      std::string corrname = jets[i].corrStep();
      double corrF = 1.0;



      if ( useJEC ) {
	corrF = jets[i].corrFactor( corrname );
      }

      
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

	hist_top_jetPt_vs_jetY->Fill( jets[i].pt()/corrF, jets[i].rapidity() );
	hist_top_jetPt->Fill( jets[i].pt()/corrF );
	hist_top_jetY->Fill( jets[i].rapidity() );
	hist_top_jetMass->Fill( topMass );
	hist_top_jetMinMass->Fill( minMass );
	hist_top_jetWMass->Fill( wMass );
	hist_top_nSubjet->Fill( jets[i].nConstituents() );
	if ( isSemiLep ) 
	  hist_top_jetMinMass_semilep_b->Fill( minMass );
	hist_top_jetMass_Vs_jetMinMass->Fill( topMass, minMass );

	if ( tagged ){
	  hist_tagged_top_jetPt_vs_jetY->Fill( jets[i].pt()/corrF, jets[i].rapidity() );
	  hist_tagged_top_jetPt->Fill( jets[i].pt()/corrF );
	  hist_tagged_top_jetY->Fill( jets[i].rapidity() );
	}

      }
      else {

	hist_nontop_jetPt_vs_jetY->Fill( jets[i].pt()/corrF, jets[i].rapidity() );
	hist_nontop_jetPt->Fill( jets[i].pt()/corrF );
	hist_nontop_jetY->Fill( jets[i].rapidity() );
	hist_nontop_jetMass->Fill( catopTag->properties().topMass );
	hist_nontop_jetMinMass->Fill( catopTag->properties().minMass );
	hist_nontop_jetWMass->Fill( catopTag->properties().wMass );
	hist_nontop_nSubjet->Fill( jets[i].nConstituents() );
	if ( isSemiLep ) 
	  hist_nontop_jetMinMass_semilep_b->Fill( minMass );

	hist_nontop_jetMass_Vs_jetMinMass->Fill( topMass, minMass );

	if ( tagged ){
	  hist_tagged_nontop_jetPt_vs_jetY->Fill( jets[i].pt()/corrF, jets[i].rapidity() );
	  hist_tagged_nontop_jetPt->Fill( jets[i].pt()/corrF );
	  hist_tagged_nontop_jetY->Fill( jets[i].rapidity() );
	}
      }
    }

  }

  TString fname ("kinematic_histos_");
  fname += sample;
  if ( !useJEC )
    fname += "_uncorr";
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();

  hist_nontop_jetPt_vs_jetY->Write();
  hist_top_jetPt_vs_jetY->Write();

  hist_nontop_jetPt->Write();
  hist_top_jetPt->Write();

  hist_nontop_jetY->Write();
  hist_top_jetY->Write();

  hist_nontop_nSubjet->Write();
  hist_top_nSubjet->Write();

  hist_tagged_nontop_jetPt_vs_jetY->Write();
  hist_tagged_top_jetPt_vs_jetY->Write();

  hist_tagged_nontop_jetPt->Write();
  hist_tagged_top_jetPt->Write();

  hist_tagged_nontop_jetY->Write();
  hist_tagged_top_jetY->Write();

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

  hist_nontop_deltaPt->Write();
  hist_top_deltaPt->Write();

  hist_nontop_jetMinMass_semilep_b->Write();
  hist_top_jetMinMass_semilep_b->Write();

  hist_top_jetMass_Vs_jetMinMass->Write();
  hist_nontop_jetMass_Vs_jetMinMass->Write();

  f->Close();



  delete hist_nontop_jetPt_vs_jetY;
  delete hist_top_jetPt_vs_jetY;

  delete hist_nontop_jetPt;
  delete hist_top_jetPt;

  delete hist_nontop_jetY;
  delete hist_top_jetY;
  
  delete hist_nontop_nSubjet;
  delete hist_top_nSubjet;

  delete hist_tagged_nontop_jetPt_vs_jetY;
  delete hist_tagged_top_jetPt_vs_jetY;

  delete hist_tagged_nontop_jetPt;
  delete hist_tagged_top_jetPt;

  delete hist_tagged_nontop_jetY;
  delete hist_tagged_top_jetY;

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

  delete hist_nontop_deltaPt;
  delete hist_top_deltaPt;

  delete hist_nontop_jetMinMass_semilep_b;
  delete hist_top_jetMinMass_semilep_b;

  delete hist_top_jetMass_Vs_jetMinMass;
  delete hist_nontop_jetMass_Vs_jetMinMass;

  tableout << sample << " " << iresults;

}


