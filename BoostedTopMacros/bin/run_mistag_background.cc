#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "dijet_analysis_mistag_prediction_fwlite.C"
#include "TSystem.h"

#include <string>

using namespace std;

int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_mistag_background <sample> <useJEC>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();

  string sample(argv[1]);

  bool processAll = true;
  bool pseudoExp = true;
  bool useJEC = true;
  double Lum = 100.0;

  if ( argc > 2 ) {
    if ( string(argv[2]) == "false")
      useJEC = false;
    else
      useJEC = true;
  }



  TFile * parameterizationFile = 0;
  if ( useJEC ) 
    parameterizationFile = new TFile("mistag_parameterization_100pb.root");
  else 
    parameterizationFile = new TFile("mistag_parameterization_100pb_uncorr.root");    

  TH1D * parameterization = (TH1D*)parameterizationFile->Get("mistag_rate");

  dijet_analysis_mistag_prediction_fwlite( parameterization,
					   sample,
					   processAll,
					   pseudoExp,
					   useJEC,
					   Lum);


  return 0;
}
