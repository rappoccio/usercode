#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "make_mistag_rate_fwlite.C"
#include "TSystem.h"


int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_mistag_parameterization <sample>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();

  make_mistag_rate_fwlite(argv[1],
			  true );

  return 0;
}
