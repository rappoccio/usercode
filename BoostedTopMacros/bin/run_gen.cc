#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "gen_fwlite_plots.C"
#include "TSystem.h"


int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_gen <sample>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();


  gen_fwlite_plots(argv[1]);


  return 0;
}
