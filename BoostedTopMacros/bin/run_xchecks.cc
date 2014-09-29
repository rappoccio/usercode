#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "xcheck_mistag_rate_fwlite.C"
#include "TSystem.h"


int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_xchecks <sample>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();

  string sample(argv[1]);

  TFile * parameterizationFile = new TFile("mistag_parameterization_odd_100pb.root");

  TH1D * parameterization = (TH1D*)parameterizationFile->Get("mistag_rate");

  bool processAll = false;
  bool pseudoExp = false;
  double Lum = 100.0;

  xcheck_mistag_rate_fwlite( parameterization,
			     sample,
			     processAll,
			     pseudoExp,
			     Lum);


  return 0;
}
