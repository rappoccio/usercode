#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
#include <TLorentzVector.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

#include <iostream>
#include <fstream>
#include <map>
#include <string>


using namespace std;
using namespace reco;
using namespace edm;

ostream & operator<<( ostream & out, TLorentzVector const & v ) {
  char buff[1000];
  sprintf(buff, "(%8.2f, %8.2f, %8.2f, %8.2f)", v.Perp(), v.Rapidity(), v.Phi(), v.Mag() );
  out << buff;

  return out;
}

void subjet_event_display_fwlite(string sample = "ttbar", int event = 0)
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


  Int_t N_ETA = 41;
  Int_t N_PHI = 36;
  Double_t DETAPHI = 0.087;

  TH2D * hist_subjets1    = new TH2D("hist_subjets1",    "Subjets",     N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI );
  TH2D * hist_jets1       = new TH2D("hist_jets1",       "Jets",        N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI ); 
  TH2D * hist_b1          = new TH2D("hist_b1",          "B Quarks",    N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI );
  TH2D * hist_q1          = new TH2D("hist_q1",          "Q Quarks",    N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI );


  TH2D * hist_subjets2    = new TH2D("hist_subjets2",    "Subjets",     N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI );
  TH2D * hist_jets2       = new TH2D("hist_jets2",       "Jets",        N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI ); 
  TH2D * hist_b2          = new TH2D("hist_b2",          "B Quarks",    N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI );
  TH2D * hist_q2          = new TH2D("hist_q2",          "Q Quarks",    N_ETA*2, -DETAPHI*N_ETA, DETAPHI*N_ETA, N_PHI*2, -DETAPHI*N_PHI, DETAPHI*N_PHI );

  cout << "About to make chain event" << endl;
  
  fwlite::ChainEvent ev(files);
  
  cout << "About to loop" << endl;

  int count = 0;
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev, ++count) {

    if ( count == event ) {


      if ( ev.getBranchDescriptions().size() <= 0 ) continue;

      fwlite::Handle<std::vector<pat::Jet> > h_jet;
      fwlite::Handle<std::vector<reco::GenParticle> > h_gen;

      h_jet   .getByLabel(ev,"selectedLayer1Jets");
      h_gen   .getByLabel(ev, "prunedGenParticles" );



    
    
      if ( !h_jet.isValid() || !h_gen.isValid() ) continue;



      TLorentzVector ttbar;              // Resonance
      TLorentzVector t1, b1, w1, p1, q1; // First top chain
      TLorentzVector t2, b2, w2, p2, q2; // Second top chain
      TLorentzVector mu1_soft, mu2_soft; // Semimuonic b decays
      TLorentzVector num1_soft, num2_soft; // Semimuonic b decays

      reco::Candidate const *pt1=0,  *pb1=0,  *pw1=0,  *pp1=0,  *pq1=0;
      reco::Candidate const *pt2=0,  *pb2=0,  *pw2=0,  *pp2=0,  *pq2=0;


      vector<reco::GenParticle> const & gen = *h_gen;

      // First get the generator level particles: top, bottom, and W daughters (p + q)
      vector<reco::GenParticle>::const_iterator gen_begin = gen.begin(),
	gen_end = gen.end(), igen = gen_begin;
      for ( ; igen != gen_end; ++igen ) {
	if ( igen->status() != 3 ) continue;

	// First get the top
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

	    if ( pw1->numberOfDaughters() >= 2 ) {
	      pp1 = pw1->daughter(0);
	      pq1 = pw1->daughter(1);
	    } else {
	      continue;
	    }
	  
	  } else {
	    continue;
	  }
	
      
	
	} // end of pdg id == 6

	// Then get the other
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

	    if ( pw2->numberOfDaughters() >= 2 ) {
	      pp2 = pw2->daughter(0);
	      pq2 = pw2->daughter(1);
	    } else {
	      continue;
	    }

	  } else {
	    continue;
	  }

	} // end of pdg id = -6

      
      }

      // Now make sure we got them all
      if ( pt1 == 0 || pb1 == 0 || pw1 == 0 || pp1 == 0 || pq1 == 0 ||
	   pt2 == 0 || pb2 == 0 || pw2 == 0 || pp2 == 0 || pq2 == 0 ) continue;




      // Get TLorentzVectors for all of them
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






      // Now fill the results of the generator level info
      hist_b1->Fill( b1.Rapidity(), b1.Phi() ,  b1.Energy());
      hist_q1->Fill( q1.Rapidity(), q1.Phi() ,  q1.Energy());
      hist_q1->Fill( p1.Rapidity(), p1.Phi() ,  p1.Energy());

      hist_b2->Fill( b2.Rapidity(), b2.Phi() ,  b2.Energy());
      hist_q2->Fill( q2.Rapidity(), q2.Phi() ,  q2.Energy());
      hist_q2->Fill( p2.Rapidity(), p2.Phi() ,  p2.Energy());


      vector<pat::Jet> const & jets = *h_jet;


      vector<pat::Jet>::const_iterator jetsbegin = h_jet->begin(),
	jetsend = h_jet->end(), ijet = jetsbegin;

      pat::Jet const * pt1_jet = &jets[0];
      pat::Jet const * pt2_jet = &jets[1];

      TLorentzVector temp1( pt1_jet->px(), pt1_jet->py(), pt1_jet->pz(), pt1_jet->energy() );
      TLorentzVector temp2( pt2_jet->px(), pt2_jet->py(), pt2_jet->pz(), pt2_jet->energy() );
      
      // If the first jet is closer to the second top, switch them
      if ( temp1.DeltaR( t1 ) > temp1.DeltaR( t2 ) ) {
	pt1_jet = &jets[1];
	pt2_jet = &jets[0];
      } 

      TLorentzVector subjets1[4];
      TLorentzVector subjets2[4];

      
      // Get the tag infos

      const reco::CATopJetTagInfo * catopTag1 = dynamic_cast<CATopJetTagInfo const *>(pt1_jet->tagInfo("CATopJetTagger"));
      const reco::CATopJetTagInfo * catopTag2 = dynamic_cast<CATopJetTagInfo const *>(pt2_jet->tagInfo("CATopJetTagger"));

      // and the cut variables
      double topMass1 = catopTag1->properties().topMass;
      double wMass1 = catopTag1->properties().wMass;
      double minMass1 = catopTag1->properties().minMass;

      double topMass2 = catopTag2->properties().topMass;
      double wMass2 = catopTag2->properties().wMass;
      double minMass2 = catopTag2->properties().minMass;

      // These are the top jets corrected to the true top direction
      TLorentzVector t1_jet ( pt1_jet->px(), pt1_jet->py(), pt1_jet->pz(), pt1_jet->energy() );
      TLorentzVector t2_jet ( pt2_jet->px(), pt2_jet->py(), pt2_jet->pz(), pt2_jet->energy() );




      // Now get the subjets. They are also corrected to the true top direction
      reco::Jet::Constituents constituents1 = pt1_jet->getJetConstituents();
      reco::Jet::Constituents constituents2 = pt2_jet->getJetConstituents();



      cout << "------------" << endl;
      cout << "Event = " << count << endl;
      char buff[1000];

      cout << "t1 = " << t1 << endl;
      cout << "   - b1 = " << b1 << endl;
      cout << "   - q1 = " << q1 << endl;
      cout << "   - p1 = " << p1 << endl;
      sprintf(buff, " MinMass = %6.2f, Jet Mass = %6.2f", minMass1, topMass1 );
      cout << "j1 = " << t1_jet << " : " << buff << endl;
      for ( int isub1 = 0; isub1 < constituents1.size(); ++isub1 ) {
	TLorentzVector subjets1_raw( constituents1[isub1]->px(), 
				     constituents1[isub1]->py(), 
				     constituents1[isub1]->pz(), 
				     constituents1[isub1]->energy() );
	subjets1[isub1] = subjets1_raw;
	cout << "   - s" << isub1 << " = " << subjets1[isub1] << endl;
      }


      cout << "t2 = " << t2 << endl;
      cout << "   - b2 = " << b2 << endl;
      cout << "   - q2 = " << q2 << endl;
      cout << "   - p2 = " << p2 << endl;
      sprintf(buff, " MinMass = %6.2f, Jet Mass = %6.2f", minMass2, topMass2 );
      cout << "j2 = " << t2_jet << buff << endl;
      for ( int isub2 = 0; isub2 < constituents2.size(); ++isub2 ) {
	TLorentzVector subjets2_raw( constituents2[isub2]->px(), 
				     constituents2[isub2]->py(), 
				     constituents2[isub2]->pz(), 
				     constituents2[isub2]->energy() );
	subjets2[isub2] = subjets2_raw;
	cout << "   - s" << isub2 << " = " << subjets2[isub2] << endl;
      }


      // Fill the distributions
    
      hist_jets1->Fill( t1_jet.Rapidity(), t1_jet.Phi(), t1_jet.Energy() );
      for ( int isub1 = 0; isub1 < constituents1.size(); ++isub1 ) {
	hist_subjets1->Fill( subjets1[isub1].Rapidity(), subjets1[isub1].Phi(), subjets1[isub1].Energy() );
      }
      hist_jets2->Fill( t2_jet.Rapidity(), t2_jet.Phi(), t2_jet.Energy() );
      for ( int isub2 = 0; isub2 < constituents2.size(); ++isub2 ) {
	hist_subjets2->Fill( subjets2[isub2].Rapidity(), subjets2[isub2].Phi(), subjets2[isub2].Energy() );
      }
    

    } // end if this is the selected event
  } // end of event loop

  TString fname ("subjet_event_display_");
  fname += sample;
  fname += "_";
  fname += event;
  fname += ".root";
  TFile * f = new TFile(fname.Data(), "RECREATE");
  f->cd();


  hist_subjets1    ->Write(); 
  hist_jets1       ->Write();  
  hist_b1          ->Write(); 
  hist_q1          ->Write(); 
  hist_subjets2    ->Write(); 
  hist_jets2       ->Write();  
  hist_b2          ->Write(); 
  hist_q2          ->Write(); 


  f->Close();


  delete hist_subjets1    ;
  delete hist_jets1       ; 
  delete hist_b1          ;
  delete hist_q1          ;
  delete hist_subjets2    ;
  delete hist_jets2       ; 
  delete hist_b2          ;
  delete hist_q2          ;



}


