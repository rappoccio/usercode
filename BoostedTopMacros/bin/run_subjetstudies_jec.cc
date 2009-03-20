

#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "TSystem.h"
#include "subjetstudies_fwlite_plots_jec.C"

int main (int argc, char ** argv)
{

  double ptsmear = 0., etasmear = 0., phismear = 0.;
  if ( argc < 2 ) {
    cout << "usage: run_subjetstudies [sample]" << endl;
    return 0;
  }

  std::string sample(argv[1]);

  if ( argc >= 3 ) ptsmear = atof( argv[2] );
  if ( argc >= 4 ) etasmear = atof( argv[3] );
  if ( argc >= 5 ) phismear = atof( argv[4] );

  cout << "ptsmear  = " << ptsmear  << endl;
  cout << "etasmear = " << etasmear << endl;
  cout << "phismear = " << phismear << endl;

  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();


  subjetstudies_fwlite_plots( sample, ptsmear, etasmear, phismear );


  return 0;
}
