#include "TH1.h"
#include "THStack.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLegend.h"
#include <iostream>

#include "palette.C"

THStack * add_plots( TLegend * leg, const char * basename, const char * varname, const char * vartitle )
{


  cout << "basename = " << basename << endl;
  cout << "varname  = " << varname << endl;
  cout << "vartitle = " << vartitle << endl;
  
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
    0.00000018146
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
    34320
  };

  const char * filenames[] = {
    "qcd_230",
    "qcd_300",
    "qcd_380",
    "qcd_470",
    "qcd_600",
    "qcd_800",
    "qcd_1000",
    "qcd_1400",
    "qcd_1800",
    "qcd_2200",
    "qcd_2600",
    "qcd_3000",
    "qcd_3500"
  };
  const char * filetitles[] = {
    "QCD Dijets, #hat{pt} = 230-300",
    "QCD Dijets, #hat{pt} = 300-380",
    "QCD Dijets, #hat{pt} = 380-470",
    "QCD Dijets, #hat{pt} = 470-600",
    "QCD Dijets, #hat{pt} = 600-800",
    "QCD Dijets, #hat{pt} = 800-1000",
    "QCD Dijets, #hat{pt} = 1000-1400",
    "QCD Dijets, #hat{pt} = 1400-1800",
    "QCD Dijets, #hat{pt} = 1800-2200",
    "QCD Dijets, #hat{pt} = 2200-2600",
    "QCD Dijets, #hat{pt} = 2600-3000",
    "QCD Dijets, #hat{pt} = 3000-3500",
    "QCD Dijets, #hat{pt} = 3500-Inf"
  };

  const Int_t N = sizeof ( weights ) / sizeof( double );


  palette(N);
  

  THStack * stack = new THStack(varname, vartitle);
  
  // do the QCD samples
  for ( int i = 0; i < N; ++i ) {
    cout << "Processing i = " << i << endl;
    TString filename(basename);
    filename += "_";
    filename += filenames[i];
    filename += ".root";
    cout << "filename = " << filename.Data() << endl;

    TFile * f = new TFile(filename.Data());
    
    TH1 * h = (TH1*)f->Get(varname);

    if ( h->GetEntries() <= 0 ) {
      cout << "Skipping " << filetitles[i] << ", no entries" << endl;
      continue;
    } else {
      cout << "Number of entries = " << h->GetEntries() << endl;
    }

    h->Scale( weights[i] / (float) nevents[i] );

    h->SetFillColor(251 + i);
    stack->Add( h );
    leg->AddEntry( h, filetitles[i], "f");
  }


  return stack;
}
