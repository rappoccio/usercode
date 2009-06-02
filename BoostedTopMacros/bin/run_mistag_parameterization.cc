#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "make_mistag_rate_fwlite.C"
#include "TSystem.h"


int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_mistag_parameterization <sample> <processAll> <use_jec>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();

  bool processAll = true;
  bool useJEC = true;
  if ( argc > 2 ) {
    cout << "Setting processAll = " << string(argv[2]) << endl;
    if ( string(argv[2]) == "false" )
      processAll = false;
    else
      processAll = true;
  }
  if ( argc > 3 ) {
    cout << "Setting useJEC = " << string(argv[3]) << endl;
    if ( string(argv[3]) == "false" )
      useJEC = false;
    else
      useJEC = true;
  }

  make_mistag_rate_fwlite(argv[1],
			  processAll,
			  useJEC );

  return 0;
}
