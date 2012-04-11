#ifndef EDHadronicAnalysis_h
#define EDHadronicAnalysis_h


#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"


typedef edm::FWLiteAnalyzerWrapper<HadronicAnalysis> EDHadronicAnalysis;


DEFINE_FWK_MODULE(EDHadronicAnalysis);


#endif
