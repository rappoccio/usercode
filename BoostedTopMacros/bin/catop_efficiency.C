#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
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

void catop_fwlite()
{
   
  vector<string> files;

  //  files.push_back("ca_pat_slim_220.root");

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


//   files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR_1.root");
//   files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR_2.root");
//   files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR_3.root");
//   files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR_4.root");
//   files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR_5.root");
//   files.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR_6.root");
  
  using namespace std;
  using namespace reco;


  TH1D * hist_muonPt = new TH1D("hist_muonPt", "Muon p_{T}", 50, 0, 2000);
  TH1D * hist_muonEta = new TH1D("hist_muonEta", "Muon #eta", 50, -3.0, 3.0 );
  TH1D * hist_muonIso = new TH1D("hist_muonIso", "Muon pt / (pt + iso)", 55, 0., 1.1);
  TH1D * hist_true_muonPt = new TH1D("hist_true_muonPt", "True Muon p_{T}", 50, 0, 2000);
  TH1D * hist_muon_genid = new TH1D("hist_muon_genid", "Muon GenParticle PDGID", 20, 0, 20);
  TH1D * hist_metPt = new TH1D("hist_metPt", "Met p_{T}", 50, 0, 2000);
  TH1D * hist_drMuonJet = new TH1D("hist_drMuonJet", "#Delta R, Muon-Jet", 50, 0, 10.0);


  TH1D * hist_njets = new TH1D("hist_njet", "Number of jets", 5, 0, 5);

  map<string, int> top_counts;
  map<string, int> nontop_counts;

  const char * cutnames [] = {
    "Jet Pt Cuts" ,
    ">= 3 Subjets",
    "Jet Mass Cut",
    "W Mass Cut"  ,
    "Min Mass Cut"
  };

  top_counts[cutnames[0]] = 0;
  top_counts[cutnames[1]] = 0;
  top_counts[cutnames[2]] = 0;
  top_counts[cutnames[3]] = 0;
  top_counts[cutnames[4]] = 0;
  

  nontop_counts[cutnames[0]] = 0;
  nontop_counts[cutnames[1]] = 0;
  nontop_counts[cutnames[2]] = 0;
  nontop_counts[cutnames[3]] = 0;
  nontop_counts[cutnames[4]] = 0;
  
  
  fwlite::ChainEvent ev(files);

  int nevents_total = 0;
  int nevents_passed = 0;
 
  for( ev.toBegin();
       ! ev.atEnd();
       ++ev) {

    ++nevents_total;

    bool passed = false;

    fwlite::Handle<std::vector<pat::Jet> > h_jet;
    fwlite::Handle<std::vector<pat::Muon> > h_muon;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");
    h_muon  .getByLabel(ev,"selectedLayer1Muons");

    vector<pat::Jet> const & jets = *h_jet;
    vector<pat::Muon> const & muons = *h_muon;


    // Require 1 muon
    if ( muons.size() < 1 ) continue;


    // Take the highest pt muon
    pat::Muon const & muon = muons[0];
    TLorentzVector p4_muon( muon.px(), muon.py(), muon.pz(), muon.energy() );

    // Fill reco muon stuff
    hist_muonPt->Fill( muon.pt() );
    hist_muonEta->Fill( muon.eta() );
    double relIso = (muon.pt() > 0 ) ? (muon.pt() / (muon.pt() + muon.caloIso() + muon.trackIso()) ) : 0.0;
    hist_muonIso->Fill( relIso );


    // Fill jet stuff
    hist_njets->Fill( jets.size() );

    // Fill matching stuff
    vector<pat::Jet>::const_iterator ijet = jets.begin(),
      ijetBegin = jets.begin(), ijetEnd = jets.end(),
      probejet = ijetEnd;

    double dr_max = 0.0;
    

    for ( ; ijet != ijetEnd; ++ijet ) {
      TLorentzVector p4_jet( ijet->px(), ijet->py(), ijet->pz(), ijet->energy() );
      
      double dr = p4_jet.DeltaR( p4_muon );
      
      if ( dr > dr_max ) {
	dr_max = dr;
	probejet = ijet;
      }
    }

    hist_drMuonJet->Fill( dr_max );
  }

  TFile * f = new TFile("histograms_catop_efficiency_fwlite.root", "RECREATE");
  f->cd();


  hist_muonPt ->Write();
  hist_muonEta ->Write();
  hist_muonIso ->Write();
  hist_true_muonPt ->Write();
  hist_muon_genid ->Write();
  hist_metPt ->Write();
  hist_drMuonJet ->Write();

  hist_njets ->Write();
 
}
