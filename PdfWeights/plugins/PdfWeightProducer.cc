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
// $Id: PdfWeightProducer.cc,v 1.8 2011/07/01 17:53:07 srappocc Exp $
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
      virtual bool produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

  std::string               pdfSet_; /// lhapdf string


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
  pdfSet_       (iConfig.getParameter<std::string> ("pdfSet") )
{

  produces<std::vector<double> > ("pdfWeights");


  if ( pdfSet_ != "" )
    LHAPDF::initPDFSet(1, pdfSet_.c_str());
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

  std::auto_ptr<std::vector<double> > pdf_weights( new std::vector<double>() );

  if ( ! iEvent.isRealData() && pdfSet_ != "" ) {

    edm::Handle<GenEventInfoProduct> pdfstuff;
    if (iEvent.getByLabel("generator", pdfstuff)) {


      LHAPDF::usePDFMember(1,0);

      float q = pdfstuff->pdf()->scalePDF;
 
      int id1 = pdfstuff->pdf()->id.first;
      double x1 = pdfstuff->pdf()->x.first;
      // double pdf1 = pdfstuff->pdf()->xPDF.first;
      
      int id2 = pdfstuff->pdf()->id.second;
      double x2 = pdfstuff->pdf()->x.second;
      // double pdf2 = pdfstuff->pdf()->xPDF.second; 

      double xpdf1 = LHAPDF::xfx(1, x1, q, id1);
      double xpdf2 = LHAPDF::xfx(1, x2, q, id2);
      double w0 = xpdf1 * xpdf2;
      for(int i=1; i <=44; ++i){
	LHAPDF::usePDFMember(1,i);
	double xpdf1_new = LHAPDF::xfx(1, x1, q, id1);
	double xpdf2_new = LHAPDF::xfx(1, x2, q, id2);
	double weight = xpdf1_new * xpdf2_new / w0;
	pdf_weights->push_back(weight);
      }
    }
  }

  iEvent.put( pdf_weights, "pdfWeights");

  return true;
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
