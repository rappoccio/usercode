/*   A macro for making a histogram of Jet Pt with cuts
This is a basic way to cut out jets of a certain Pt and Eta using an if statement
This example creates a histogram of Jet Pt, using Jets with Pt above 30 and ETA above -2.1 and below 2.1
*/
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "TFile.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#endif

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>

using namespace std;

int main ( int argc, char ** argv )
{

  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();  

  TFile  * file = new TFile("ttbsm_ca_pat_330.root");
  TH1D * hist_jetPt = new TH1D("hist_jetPt", "Jet p_{T}", 20, 0, 100 );
  fwlite::Event ev(file);

  int count = 0;
  //loop through each event
  for( ev.toBegin();
         ! ev.atEnd();
       ++ev, ++count) {


    fwlite::Handle<std::vector<pat::Jet> > allJets;
    allJets.getByLabel(ev,"selectedLayer1JetsTopTagCalo");
    if (!allJets.isValid() ) continue;

    for ( std::vector<pat::Jet>::const_iterator jetsBegin = allJets->begin(),
	    jetsEnd = allJets->end(),
	    ijet = jetsBegin;
	  ijet != jetsEnd; ++ijet ) {
      const reco::CATopJetTagInfo * catopTag = dynamic_cast<reco::CATopJetTagInfo const *>(ijet->tagInfo("CATopCaloJet"));
      
      if ( catopTag !=0 && catopTag->properties().minMass != 999999.0 ) {
	char buff[1000];
	sprintf(buff, "Jet %6d, pt = %6.2f, mass = %6.2f, minMass = %6.2f, wMass = %6.2f",
		ijet - jetsBegin,
		ijet->pt(), 
		catopTag->properties().topMass,
		catopTag->properties().minMass,
		catopTag->properties().wMass );
	cout << buff << endl;
      }
    }
    
  } //end event loop
  

  file->Close();
  delete file;
  return 0;
}
