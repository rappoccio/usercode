#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "kinematics_fwlite_plots.C"
#include "TSystem.h"


int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_kinematics <sample>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();


  bool useJEC = true;
  if ( argc > 2 ) {
    if ( string(argv[2]) == "false" ) {
      cout << "using uncorrected jets" << endl;
      useJEC = false;
    }
    else
      useJEC = true;
  }

  catop_fwlite(argv[1], useJEC);



  return 0;
}
