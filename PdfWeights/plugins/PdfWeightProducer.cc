// -*- C++ -*-
//
// Package:    PdfWeightProducer
// Class:      PdfWeightProducer
// 
/**\class PdfWeightProducer PdfWeightProducer.cc Analysis/PdfWeightProducer/src/PdfWeightProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Mon Jan 17 21:44:07 CST 2011
// $Id: PdfWeightProducer.cc,v 1.1 2011/08/11 14:21:22 srappocc Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

namespace LHAPDF {
      void initPDFSet(int nset, const std::string& filename, int member=0);
      int numberPDF(int nset);
      void usePDFMember(int nset, int member);
      double xfx(int nset, double x, double Q, int fl);
      double getXmin(int nset, int member);
      double getXmax(int nset, int member);
      double getQ2min(int nset, int member);
      double getQ2max(int nset, int member);
      void extrapolate(bool extrapolate=true);
}

//
// class declaration
//

class PdfWeightProducer : public edm::EDProducer {
   public:
      explicit PdfWeightProducer(const edm::ParameterSet&);
      ~PdfWeightProducer();

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

  std::vector<std::string> pdfSet_;  // lhapdf string
  std::vector<std::string> pdfName_; // short name for output collection identifier
  std::vector<int> nMembers_;        // number of eigenvector variations for the given PDF set  

};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
PdfWeightProducer::PdfWeightProducer(const edm::ParameterSet& iConfig) :
  pdfSet_   (iConfig.getParameter<std::vector<std::string> > ("pdfSet") ),
  pdfName_  (iConfig.getParameter<std::vector<std::string> > ("pdfName") ),
  nMembers_ (iConfig.getParameter<std::vector<int> > ("nMembers") )
{

  if (pdfSet_.size()>3) {
    std::cout << "WARNING! Can handle max 3 PDF sets!";
    pdfSet_.erase(pdfSet_.begin()+3,pdfSet_.end());
    pdfName_.erase(pdfName_.begin()+3,pdfName_.end());
    nMembers_.erase(nMembers_.begin()+3,nMembers_.end());
  }


  for (unsigned int ipdf=0; ipdf<pdfSet_.size(); ipdf++) {
    // output collection
    produces<std::vector<double> > (pdfName_.at(ipdf)+"weights");

    // initialize LHAPDF
    if (pdfSet_.at(ipdf) != "") LHAPDF::initPDFSet(ipdf+1, pdfSet_.at(ipdf).c_str());
  }

}


PdfWeightProducer::~PdfWeightProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
PdfWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  if (iEvent.isRealData()) return;

  edm::Handle<GenEventInfoProduct> pdfstuff;
  if (!iEvent.getByLabel("generator", pdfstuff)) {
    std::cout << "WARNING: GenEventInfoProduct collection not found!" << std::endl;
    return;
  }

  // nominal PDF set
  LHAPDF::usePDFMember(1,0);
  
  float q = pdfstuff->pdf()->scalePDF;
  
  int id1 = pdfstuff->pdf()->id.first;
  double x1 = pdfstuff->pdf()->x.first;      
  int id2 = pdfstuff->pdf()->id.second;
  double x2 = pdfstuff->pdf()->x.second;
  
  double xpdf1 = LHAPDF::xfx(1, x1, q, id1);
  double xpdf2 = LHAPDF::xfx(1, x2, q, id2);
  double w0 = xpdf1 * xpdf2;

  // loop over the PDF sets
  for (unsigned int ipdf=0; ipdf<pdfSet_.size(); ipdf++) {

    std::auto_ptr<std::vector<double> > pdf_weights( new std::vector<double>() );

    if (pdfSet_.at(ipdf) == "") continue;
    if (nMembers_.at(ipdf) < 1) {
      std::cout << "WARNING: nMembers == 0 for PDF set, can't get eigenvector variations..." << std::endl;
      continue;
    }

    // need this to get the central value for other PDF sets, i.e. rescaling it from CT10 to a different pdf set
    // for the nominal PDF, this first weight will be == 1

    LHAPDF::usePDFMember(ipdf+1,0);
    double central_xpdf1 = LHAPDF::xfx(1, x1, q, id1);
    double central_xpdf2 = LHAPDF::xfx(1, x2, q, id2);
    double central_weight = central_xpdf1 * central_xpdf2 / w0;
    pdf_weights->push_back(central_weight); 
    

    // PDF eigenvector variations for the different PDF sets

    for(int i=1; i <=nMembers_.at(ipdf); ++i){
      LHAPDF::usePDFMember(ipdf+1,i);
      double xpdf1_new = LHAPDF::xfx(ipdf+1, x1, q, id1);
      double xpdf2_new = LHAPDF::xfx(ipdf+1, x2, q, id2);
      double weight = xpdf1_new * xpdf2_new / w0;
      pdf_weights->push_back(weight);
    }
    
    iEvent.put( pdf_weights, pdfName_.at(ipdf)+"weights");

  }//end loop over PDF sets

  
}

// ------------ method called once each job just before starting event loop  ------------
void 
PdfWeightProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PdfWeightProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(PdfWeightProducer);
