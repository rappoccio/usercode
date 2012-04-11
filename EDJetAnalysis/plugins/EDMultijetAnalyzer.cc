#ifndef EDMultijetAnalysis_h
#define EDMultijetAnalysis_h


#include "Analysis/JetAnalysis/interface/MultijetAnalyzer.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"


typedef edm::FWLiteAnalyzerWrapper<MultijetAnalyzer> EDMultijetAnalysis;


DEFINE_FWK_MODULE(EDMultijetAnalysis);


#endif
