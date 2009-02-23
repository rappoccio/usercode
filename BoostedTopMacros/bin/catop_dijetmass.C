#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TFile.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

#include <iostream>
#include <map>
#include <string>

using namespace std;

void catop_fwlite(int sample = 0)
{
  using namespace std;
  using namespace reco;
   
   
  vector<string> files0;
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/qcd_470_ca_pat_default_2110_uniformDR08_1.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/qcd_470_ca_pat_default_2110_uniformDR08_2.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/qcd_470_ca_pat_default_2110_uniformDR08_3.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/qcd_470_ca_pat_default_2110_uniformDR08_4.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/qcd_470_ca_pat_default_2110_uniformDR08_5.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/qcd_470_ca_pat_default_2110_uniformDR08_6.root");


  vector<string> files1;
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/qcd_600_ca_pat_default_2110_uniformDR08_1.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/qcd_600_ca_pat_default_2110_uniformDR08_2.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/qcd_600_ca_pat_default_2110_uniformDR08_3.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/qcd_600_ca_pat_default_2110_uniformDR08_4.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/qcd_600_ca_pat_default_2110_uniformDR08_5.root");


  vector<string> files2;
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_1.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_2.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_3.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_4.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_5.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_6.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_7.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/qcd_800_ca_pat_default_2110_uniformDR08_8.root");

  vector<string> files3;
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_1.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_2.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_3.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_4.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_5.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_6.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/qcd_1000_ca_pat_default_2110_uniformDR08_7.root");

  vector< vector<string> * > files;
  files.push_back(&files0);
  files.push_back(&files1);
  files.push_back(&files2);
  files.push_back(&files3);

  double weights[] = {
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

  const char * filenames[] = {
    "QCD_470_600",
    "QCD_600_800",
    "QCD_800_1000",
    "QCD_1000_1400",
  };
  const char * filetitles[] = {
    "QCD 470-600",
    "QCD 600-800",
    "QCD 800-1000",
    "QCD 1000-1400",
  };

  const int nfiles = sizeof( files ) / sizeof( TFile *);
  if ( sample < 0 || sample > nfiles ) return;
  vector<string> const & file = *(files[sample]);
  const char * title = filetitles[sample];
  const char * filename = filenames[sample];
  double weight = weights[sample] / weights[0];

  const char * cutnames [] = {
    "Jet Pt Cuts" ,
    ">= 3 Subjets",
    "Jet Mass Cut",
    "W Mass Cut"  ,
    "Min Mass Cut"
  };

  const int ncuts = sizeof( cutnames ) / sizeof( const char * );

  const char * plots [] = {
    "jjMass",
    "leadJetPt"
  };
  const int nplots = sizeof ( plots ) / sizeof( const char * );
  double bounds [nplots][3] = {
    {100, 0, 4000},
    {100, 0, 2000}
  };

  TH1D * histograms[nplots][ncuts][2];

  for ( int i = 0; i < nplots; ++i ) {
    for ( int j = 0; j < ncuts; ++j ) {

      TString name1("hist_nontop_");
      TString name2("hist_top_");

      name1 += plots[i];
      name1 += "_cut";
      name1 += j;

      histograms[i][j][0] = new TH1D (name1.Data(), name1.Data(), (int)bounds[i][0], bounds[i][1], bounds[i][2] );

      name2 += plots[i];
      name2 += "_cut";
      name2 += j;

      histograms[i][j][1] = new TH1D (name2.Data(), name2.Data(), (int)bounds[i][0], bounds[i][1], bounds[i][2] );

    }
  }
  


  fwlite::ChainEvent ev(file);
  
  for( ev.toBegin();
          ! ev.atEnd();
          ++ev) {


    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    vector<pat::Jet> const & jets = *h_jet;

    int jetSignal = (abs(jets[0].partonFlavour()) == 6) ? 1 : 0;
    // Now fill the dijet mass for various cuts
    histograms[1][0][jetSignal]->Fill( jets[0].pt(), weight );

    if ( jets.size() < 2 ) continue;

    // Get the top tag info and 4-vector for the first jet
    const reco::CATopJetTagInfo * catopTag1 = dynamic_cast<CATopJetTagInfo const *>(jets[0].tagInfo("CATopJetTagger"));
    reco::Particle::LorentzVector p4_1 = jets[0].p4();
       
	 
    // Get the top tag info and 4-vector for the second jet
    const reco::CATopJetTagInfo * catopTag2 = dynamic_cast<CATopJetTagInfo const *>(jets[1].tagInfo("CATopJetTagger"));
    reco::Particle::LorentzVector p4_2 = jets[1].p4();


    // See if we have signal (from MC truth)
    int signal = 0;
    if ( abs(jets[0].partonFlavour()) == 6 && abs(jets[1].partonFlavour()) == 6 ) {
      signal = 1;
    }


    reco::Particle::LorentzVector p4 = p4_1 + p4_2;
    double mass = p4.mass();
	 
    // Now fill the dijet mass for various cuts
    histograms[0][0][signal]->Fill( mass, weight );
    
    if  ( jets[0].getJetConstituents().size() < 3 ||
	  jets[1].getJetConstituents().size() < 3 )  continue;
    histograms[0][1][signal]->Fill( mass, weight );
    
    if ( (catopTag1->properties().topMass < 100 || catopTag1->properties().topMass > 250) ||
	 (catopTag2->properties().topMass < 100 || catopTag2->properties().topMass > 250) ) continue;
    histograms[0][2][signal]->Fill( mass, weight );
    
    if ( catopTag1->properties().wMass < 0 ||
	 catopTag2->properties().wMass < 0) continue;
    histograms[0][3][signal]->Fill( mass, weight );
    
    if ( catopTag1->properties().minMass < 50 ||
	 catopTag2->properties().minMass < 50 ) continue;
    histograms[0][4][signal]->Fill( mass, weight );

  }


  TString outname("histograms_catop_mjj_analysis_fwlite_twojetmass");
  outname += filename;
  outname += ".root";
  TFile * f = new TFile(outname.Data(), "RECREATE" );
  f->cd();
  

  for ( int i = 0; i < nplots; ++i ) {
    for ( int j = 0; j < ncuts; ++j ) {
	histograms[i][j][0] -> Write();
	histograms[i][j][1] -> Write();
    }
  }

  
  
}
