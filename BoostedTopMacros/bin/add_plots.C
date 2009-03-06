#include "TH1.h"
#include "THStack.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLegend.h"
#include <iostream>

#include "palette.C"

THStack * add_plots( double Lum, TLegend * leg, const char * basename, const char * varname, const char * vartitle )
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
    "qcd_230_v5",
    "qcd_300_v5",
    "qcd_380_v5",
    "qcd_470_v5",
    "qcd_600_v5",
    "qcd_800_v5",
    "qcd_1000_v5",
    "qcd_1400_v5",
    "qcd_1800_v5",
    "qcd_2200_v5",
    "qcd_2600_v5",
    "qcd_3000_v5",
    "qcd_3500_v5"
  };
  const char * filetitles[] = {
    "#hat{pt} = 230-300",
    "#hat{pt} = 300-380",
    "#hat{pt} = 380-470",
    "#hat{pt} = 470-600",
    "#hat{pt} = 600-800",
    "#hat{pt} = 800-1000",
    "#hat{pt} = 1000-1400",
    "#hat{pt} = 1400-1800",
    "#hat{pt} = 1800-2200",
    "#hat{pt} = 2200-2600",
    "#hat{pt} = 2600-3000",
    "#hat{pt} = 3000-3500",
    "#hat{pt} = 3500-Inf"
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

    h->Scale( weights[i] / (float) nevents[i] * Lum );

    h->SetFillColor(251 + i);
    stack->Add( h );
    leg->AddEntry( h, filetitles[i], "f");
  }


  return stack;
}
