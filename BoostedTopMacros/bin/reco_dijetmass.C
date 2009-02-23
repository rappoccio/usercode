#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include <TH1.h>
#include <TFile.h>


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#endif

#include <iostream>
#include <map>
#include <string>

using namespace std;

void reco_dijetmass(int sample = 0)
{
  using namespace std;
  using namespace reco;
   
   
  vector<string> files0;
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/patlayer1_kt_dijetsamples_qcd_470_600_1.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/patlayer1_kt_dijetsamples_qcd_470_600_2.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/patlayer1_kt_dijetsamples_qcd_470_600_3.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/patlayer1_kt_dijetsamples_qcd_470_600_4.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/patlayer1_kt_dijetsamples_qcd_470_600_5.root");
  files0.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_470/patlayer1_kt_dijetsamples_qcd_470_600_6.root");


  vector<string> files1;
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/patlayer1_kt_dijetsamples_qcd_600_800_1.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/patlayer1_kt_dijetsamples_qcd_600_800_2.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/patlayer1_kt_dijetsamples_qcd_600_800_3.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/patlayer1_kt_dijetsamples_qcd_600_800_4.root");
  files1.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_600/patlayer1_kt_dijetsamples_qcd_600_800_5.root");


  vector<string> files2;
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_1.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_2.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_3.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_4.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_5.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_6.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_7.root");
  files2.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_800/patlayer1_kt_dijetsamples_qcd_800_1000_8.root");

  vector<string> files3;
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_1.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_2.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_3.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_4.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_5.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_6.root");
  files3.push_back("dcap:///pnfs/cms/WAX/11/store/user/rappocc/qcd_1000/patlayer1_kt_dijetsamples_qcd_1000_1400_7.root");

  vector< vector<string> * > files;
  files.push_back(&files0);
  files.push_back(&files1);
  files.push_back(&files2);
  files.push_back(&files3);

  double xs[] = {  // pb
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

  int nevents[] = {  // number of events generated
    27648,
    28620,
    20880,
    24640
  };

  double lum = 100; // pb-1

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

  double nexp = xs[sample] * lum;

  const char * plots [] = {
    "jjMass",
    "leadJetPt"
  };
  const int nplots = sizeof ( plots ) / sizeof( const char * );
  double bounds [nplots][3] = {
    {100, 0, 4000},
    {100, 0, 2000}
  };

  TH1D * histograms[nplots][2];

  for ( int i = 0; i < nplots; ++i ) {


      TString name1("hist_nontop_");
      TString name2("hist_top_");

      name1 += plots[i];

      histograms[i][0] = new TH1D (name1.Data(), name1.Data(), (int)bounds[i][0], bounds[i][1], bounds[i][2] );

      name2 += plots[i];

      histograms[i][1] = new TH1D (name2.Data(), name2.Data(), (int)bounds[i][0], bounds[i][1], bounds[i][2] );


  }
  


  fwlite::ChainEvent ev(file);

  int icount = 0;
  for( ev.toBegin();
          ! ev.atEnd();
       ++ev, ++icount) {

    if ( icount % 1000  == 0 ) cout << "Processing icount = " << icount << endl;

    fwlite::Handle<std::vector<pat::Jet> > h_jet;

    h_jet   .getByLabel(ev,"selectedLayer1Jets");

    vector<pat::Jet> const & jets = *h_jet;

    if ( jets.size() < 2 ) continue;


    reco::Particle::LorentzVector p4_1 = jets[0].p4();
	 
    reco::Particle::LorentzVector p4_2 = jets[1].p4();


    // See if we have signal (from MC truth)
    int signal = 0;
    if ( abs(jets[0].partonFlavour()) == 6 && abs(jets[1].partonFlavour()) == 6 ) {
      signal = 1;
    }


    reco::Particle::LorentzVector p4 = p4_1 + p4_2;
    double mass = p4.mass();
	 
    // Now fill the dijet mass for various cuts
    histograms[0][signal]->Fill( mass );
  }

  cout << "------------" << endl;
  cout << "Sample   = " << filetitles[sample] << endl;
  cout << "xs       = " << xs[sample] << endl;
  cout << "Lum      = " << lum << endl;
  cout << "Nexp     = " << nexp << endl;
  cout << "Nevents  = " << nevents[sample] << endl;
  cout << "Nentries = " << histograms[0][0]->GetEntries() << endl;
  cout << "Scale    = " << nexp / (float)histograms[0][0]->GetEntries() << endl;
  cout << "Integral1= " << histograms[0][0]->Integral() << endl;
  if ( nevents[sample] > 0 ) {
    histograms[0][0]->Sumw2();
    histograms[0][0]->Scale( nexp / (float)nevents[sample] );
  } 
  if ( nevents[sample] > 0 ) {
    histograms[0][1]->Sumw2();
    histograms[0][1]->Scale( nexp / (float)nevents[sample] );
  }
  cout << "Integral2= " << histograms[0][0]->Integral() << endl;
  cout << "------------" << endl;

  TString outname("histograms_reco_mjj_analysis_fwlite_twojetmass");
  outname += filename;
  outname += ".root";
  TFile * f = new TFile(outname.Data(), "RECREATE" );
  f->cd();
  

  for ( int i = 0; i < nplots; ++i ) {
	histograms[i][0] -> Write();
	histograms[i][1] -> Write();
  }

  
  
}
