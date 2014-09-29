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


void gen_fwlite_plots(string sample = "ttbar")
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


  ofstream tableout("kinematics_output.txt", ios_base::app);
   
  using namespace std;
  using namespace reco;
  


  TH1D * hist_ttbar_mass = new TH1D("hist_ttbar_mass", "t#bar{t} Invariant Mass;Mass (GeV/c^{2});Fraction", 500, 0, 5000);


  TH1D * hist_top_genPt = new TH1D("hist_top_genPt", "Top Quark p_{T};p_{T} (GeV/c);Fraction",     100, 0, 5000 );
  TH1D * hist_w_genPt   = new TH1D("hist_w_genPt",   "W p_{T};p_{T} (GeV/c);Fraction",             100, 0, 5000 );
  TH1D * hist_wDa_genPt = new TH1D("hist_wDa_genPt", "W Daughter p_{T};p_{T} (GeV/c);Fraction",    100, 0, 5000 );
  TH1D * hist_b_genPt   = new TH1D("hist_b_genPt",   "Bottom Quark p_{T};p_{T} (GeV/c);Fraction",  100, 0, 5000 );

  TH1D * hist_top_genY = new TH1D("hist_top_genY", "Top Quark Rapidity;Rapidity;Fraction",     100, -5.0, 5.0 );
  TH1D * hist_w_genY   = new TH1D("hist_w_genY",   "W Rapidity;Rapidity;Fraction",             100, -5.0, 5.0 );
  TH1D * hist_wDa_genY = new TH1D("hist_wDa_genY", "W Daughter Rapidity;Rapidity;Fraction",    100, -5.0, 5.0 );
  TH1D * hist_b_genY   = new TH1D("hist_b_genY",   "Bottom Quark Rapidity;Rapidity;Fraction",  100, -5.0, 5.0 );

  TH1D * hist_minMass  = new TH1D("hist_minMass",  "Min Mass Pairing of All Partons;Mass (GeV/c^{2});Fraction", 100, 0, 200 );
  TH1D * hist_minMass_submu  = new TH1D("hist_minMass_submu",  "Min Mass Pairing of All Partons Minus Muons;Mass (GeV/c^{2});Fraction", 100, 0, 200 );

  TH1D * hist_top_genDeltaPt = new TH1D("hist_top_genDeltaPt", "Top Quark #Delta p_{T};#Delta p_{T} (GeV/c);Fraction", 100, 0, 1000);

  TH1D * hist_top_id = new TH1D("hist_top_id", "Top Quark PdgID", 30, 0, 30);
  TH1D * hist_b_id   = new TH1D("hist_b_id",   "B Quark PdgID", 30, 0, 30);
  TH1D * hist_w_id   = new TH1D("hist_w_id",   "W PdgID", 30, 0, 30);
  TH1D * hist_wDa_id = new TH1D("hist_wDa_id", "W Daughter Quark PdgID", 30, 0, 30);


  cout << "About to make chain event" << endl;
  
  fwlite::ChainEvent ev(files);
  
  cout << "About to loop" << endl;

  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {


    if ( ev.getBranchDescriptions().size() <= 0 ) continue;

//     cout << "Processing event " << count << endl;

    fwlite::Handle<std::vector<reco::GenParticle> > h_gen;

    h_gen   .getByLabel(ev,"prunedGenParticles");

    if ( !h_gen.isValid() ) continue;

    TLorentzVector ttbar;              // Resonance
    TLorentzVector t1, b1, w1, p1, q1; // First top chain
    TLorentzVector t2, b2, w2, p2, q2; // Second top chain
    TLorentzVector mu1_soft, mu2_soft; // Semimuonic b decays
    TLorentzVector num1_soft, num2_soft; // Semimuonic b decays

    reco::Candidate const *pt1=0,  *pb1=0,  *pw1=0,  *pp1=0,  *pq1=0;
    reco::Candidate const *pt2=0,  *pb2=0,  *pw2=0,  *pp2=0,  *pq2=0;
    reco::Candidate const *pmu1_soft = 0, *pmu2_soft = 0;
    reco::Candidate const *pnum1_soft = 0, *pnum2_soft = 0;


    vector<reco::GenParticle> const & gen = *h_gen;

    vector<reco::GenParticle>::const_iterator gen_begin = gen.begin(),
      gen_end = gen.end(), igen = gen_begin;
    for ( ; igen != gen_end; ++igen ) {
      if ( igen->status() != 3 ) continue;
      if ( igen->pdgId() == 6   ) {



	pt1 = &(*igen);
	
	if ( pt1->numberOfDaughters() >= 2 ) {
	  pw1 = igen->daughter(0);
	  pb1 = igen->daughter(1);

	  if ( abs( pw1->pdgId() ) != 24 ) {
	    reco::Candidate const * temp = pw1;
	    pw1 = pb1;
	    pb1 = temp;
	  }

	  if ( pb1->numberOfDaughters() >= 1 ) {
	    for ( int ibda = 0; ibda < pb1->numberOfDaughters(); ++ibda ) {
	      reco::Candidate const * bda = pb1->daughter(ibda);
	      if ( bda != 0 && abs(bda->pdgId()) == 13 ) {
		pmu1_soft = bda;
	      }
	      if ( bda != 0 && abs(bda->pdgId()) == 14 ) {
		pnum1_soft = bda;
	      }
	    }
	  }
	  
	  if ( pw1->numberOfDaughters() >= 2 ) {
	    pp1 = pw1->daughter(0);
	    pq1 = pw1->daughter(1);
	  } else {
	    continue;
	  }
	  
	} else {
	  continue;
	}
	
      
	
      }

      else if ( igen->pdgId() == -6 ) {
	

	pt2 = &(*igen);
	
	if ( pt2->numberOfDaughters() >= 2 ) {
	  pw2 = igen->daughter(0);
	  pb2 = igen->daughter(1);

	  if ( abs( pw2->pdgId() ) != 24 ) {
	    reco::Candidate const * temp = pw2;
	    pw2 = pb2;
	    pb2 = temp;
	  }

	  if ( pb2->numberOfDaughters() >= 1 ) {
	    for ( int ibda = 0; ibda < pb2->numberOfDaughters(); ++ibda ) {
	      reco::Candidate const * bda = pb2->daughter(ibda);
	      if ( bda != 0 && abs(bda->pdgId()) == 13 ) {
		pmu2_soft = bda;
	      }
	      if ( bda != 0 && abs(bda->pdgId()) == 14 ) {
		pnum2_soft = bda;
	      }
	    }
	  }

	  if ( pw2->numberOfDaughters() >= 2 ) {
	    pp2 = pw2->daughter(0);
	    pq2 = pw2->daughter(1);
	  } else {
	    continue;
	  }

	} else {
	  continue;
	}

      }

      
    }

    if ( pt1 == 0 || pb1 == 0 || pw1 == 0 || pp1 == 0 || pq1 == 0 ||
	 pt2 == 0 || pb2 == 0 || pw2 == 0 || pp2 == 0 || pq2 == 0 ) continue;


    t1 = TLorentzVector( pt1->px(), pt1->py(), pt1->pz(), pt1->energy() );
    b1 = TLorentzVector( pb1->px(), pb1->py(), pb1->pz(), pb1->energy() );
    w1 = TLorentzVector( pw1->px(), pw1->py(), pw1->pz(), pw1->energy() );
    p1 = TLorentzVector( pp1->px(), pp1->py(), pp1->pz(), pp1->energy() );
    q1 = TLorentzVector( pq1->px(), pq1->py(), pq1->pz(), pq1->energy() );

    t2 = TLorentzVector( pt2->px(), pt2->py(), pt2->pz(), pt2->energy() );
    b2 = TLorentzVector( pb2->px(), pb2->py(), pb2->pz(), pb2->energy() );
    w2 = TLorentzVector( pw2->px(), pw2->py(), pw2->pz(), pw2->energy() );
    p2 = TLorentzVector( pp2->px(), pp2->py(), pp2->pz(), pp2->energy() );
    q2 = TLorentzVector( pq2->px(), pq2->py(), pq2->pz(), pq2->energy() );

    if ( pmu1_soft != 0 ) mu1_soft = TLorentzVector( pmu1_soft->px(), pmu1_soft->py(), pmu1_soft->pz(), pmu1_soft->energy() );
    if ( pmu2_soft != 0 ) mu2_soft = TLorentzVector( pmu2_soft->px(), pmu2_soft->py(), pmu2_soft->pz(), pmu2_soft->energy() );
    if ( pnum1_soft != 0 ) num1_soft = TLorentzVector( pnum1_soft->px(), pnum1_soft->py(), pnum1_soft->pz(), pnum1_soft->energy() );
    if ( pnum2_soft != 0 ) num2_soft = TLorentzVector( pnum2_soft->px(), pnum2_soft->py(), pnum2_soft->pz(), pnum2_soft->energy() );


    hist_top_id->Fill( pt1->pdgId() );
    hist_top_id->Fill( pt2->pdgId() );

    hist_w_id->Fill( pw1->pdgId() );
    hist_w_id->Fill( pw2->pdgId() );

    hist_b_id->Fill( pb1->pdgId() );
    hist_b_id->Fill( pb2->pdgId() );

    hist_wDa_id->Fill( pq1->pdgId() );
    hist_wDa_id->Fill( pq2->pdgId() );
    hist_wDa_id->Fill( pp1->pdgId() );
    hist_wDa_id->Fill( pp2->pdgId() );

    ttbar = t1 + t2;

    hist_ttbar_mass->Fill( ttbar.M() );

    hist_top_genPt ->Fill( t1.Perp());
    hist_w_genPt   ->Fill( w1.Perp());
    hist_wDa_genPt ->Fill( p1.Perp());
    hist_wDa_genPt ->Fill( q1.Perp());
    hist_b_genPt   ->Fill( b1.Perp());

    hist_top_genPt ->Fill( t2.Perp());
    hist_w_genPt   ->Fill( w2.Perp());
    hist_wDa_genPt ->Fill( p2.Perp());
    hist_wDa_genPt ->Fill( q2.Perp());
    hist_b_genPt   ->Fill( b2.Perp());

    hist_top_genY  ->Fill( t1.Rapidity());
    hist_w_genY    ->Fill( w1.Rapidity());
    hist_wDa_genY  ->Fill( p1.Rapidity());
    hist_wDa_genY  ->Fill( q1.Rapidity());
    hist_b_genY    ->Fill( b1.Rapidity());

    hist_top_genY  ->Fill( t2.Rapidity());
    hist_w_genY    ->Fill( w2.Rapidity());
    hist_wDa_genY  ->Fill( p2.Rapidity());
    hist_wDa_genY  ->Fill( q2.Rapidity());
    hist_b_genY    ->Fill( b2.Rapidity());


    hist_top_genDeltaPt->Fill( fabs(t1.Perp() - t2.Perp() ) );


    vector<TLorentzVector> partons1;
    partons1.push_back( b1 );
    partons1.push_back( p1 );
    partons1.push_back( q1 );

    vector<TLorentzVector> partons2;
    partons2.push_back( b2 );
    partons2.push_back( p2 );
    partons2.push_back( q2 );

    double minMass1 = 999999;
    vector<TLorentzVector>::const_iterator parti = partons1.begin(), partj = parti + 1;

    vector<TLorentzVector>::const_iterator part1Begin = partons1.begin(), part1End = partons1.end();
    for ( parti = part1Begin ; parti != part1End - 1; ++parti ) {
      for ( partj = parti + 1; partj != part1End; ++partj ) {
	TLorentzVector sum = *parti + *partj;
	if ( sum.M() < minMass1 ) {
	  minMass1 = sum.M();
	}
      }
    }

    double minMass2 = 999999;
    vector<TLorentzVector>::const_iterator part2Begin = partons2.begin(), part2End = partons2.end();
    for ( parti = part2Begin ; parti != part2End - 1; ++parti ) {
      for ( partj = parti + 1; partj != part2End; ++partj ) {
	TLorentzVector sum = *parti + *partj;
	if ( sum.M() < minMass2 ) {
	  minMass2 = sum.M();
	}
      }
    }

    hist_minMass   ->Fill( minMass1 );
    hist_minMass   ->Fill( minMass2 );
    

    // Now do it again subtracting out any muons from the b decays

    if ( pmu1_soft != 0 ) {

      partons1.clear();
      TLorentzVector b1_prime = b1 - mu1_soft - num1_soft;
      partons1.push_back( b1_prime );
      partons1.push_back( p1 );
      partons1.push_back( q1 );

      double minMassPrime1 = 999999;
      vector<TLorentzVector>::const_iterator parti = partons1.begin(), partj = parti + 1;

      vector<TLorentzVector>::const_iterator part1Begin = partons1.begin(), part1End = partons1.end();
      for ( parti = part1Begin ; parti != part1End - 1; ++parti ) {
	for ( partj = parti + 1; partj != part1End; ++partj ) {
	  TLorentzVector sum = *parti + *partj;
	  if ( sum.M() < minMassPrime1 ) {
	    minMassPrime1 = sum.M();
	  }
	}
      }


      hist_minMass_submu->Fill( minMassPrime1 );
    }


    
    if ( pmu2_soft != 0 ) {

      partons2.clear();
      TLorentzVector b2_prime = b2 - mu2_soft - num2_soft;
      partons1.push_back( b2_prime );
      partons2.push_back( p2 );
      partons2.push_back( q2 );

      double minMassPrime2 = 999999;
      vector<TLorentzVector>::const_iterator part2Begin = partons2.begin(), part2End = partons2.end();
      for ( parti = part2Begin ; parti != part2End - 1; ++parti ) {
	for ( partj = parti + 1; partj != part2End; ++partj ) {
	  TLorentzVector sum = *parti + *partj;
	  if ( sum.M() < minMassPrime2 ) {
	    minMassPrime2 = sum.M();
	  }
	}
      }

      hist_minMass_submu->Fill( minMassPrime2 );

    }

//     for ( ; igen != gen_end; ++igen ) {
// //       cout << "igen.pdgid = " << igen->pdgId() << endl;
//       if ( abs( igen->pdgId() ) == 6 ) {
// 	hist_top_genPt->Fill( igen->pt() );
//       }
//     }

  }

  cout << "Done with loop, writing" << endl;


  TString fname ("gen_histos_");
  fname += sample;
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();


  hist_ttbar_mass->Write();

  hist_top_genPt ->Write();
  hist_w_genPt   ->Write();
  hist_wDa_genPt ->Write();
  hist_b_genPt   ->Write();

  hist_top_genY  ->Write();
  hist_w_genY    ->Write();
  hist_wDa_genY  ->Write();
  hist_b_genY    ->Write();

  hist_minMass   ->Write();
  hist_minMass_submu->Write();

  hist_top_genDeltaPt->Write();


  hist_top_id->Write();
  hist_w_id->Write  ();
  hist_b_id->Write  ();
  hist_wDa_id->Write();

  f->Close();



  delete hist_ttbar_mass;

  delete hist_top_genPt ;
  delete hist_w_genPt   ;
  delete hist_wDa_genPt ;
  delete hist_b_genPt   ;

  delete hist_top_genY  ;
  delete hist_w_genY    ;
  delete hist_wDa_genY  ;
  delete hist_b_genY    ;

  delete hist_minMass   ;
  delete hist_minMass_submu;

  delete hist_top_genDeltaPt;



  delete hist_top_id;
  delete hist_w_id  ;
  delete hist_b_id  ;
  delete hist_wDa_id;

}



