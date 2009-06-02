#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "TFile.h"
#include "subjet_event_display_fwlite.C"
#include "TSystem.h"


int main (int argc, char ** argv)
{


  if ( argc < 2 ) {
    cout << "usage: run_subjet_event_display <sample> <event>" << endl;
    return 0;
  }


  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();


  bool useJEC = true;
  int event = 0;
  if ( argc > 2 ) {
    event = atoi(argv[2]);
  }

  subjet_event_display_fwlite(argv[1], event);



  return 0;
}
