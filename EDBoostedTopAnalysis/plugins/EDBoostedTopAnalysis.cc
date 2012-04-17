#ifndef EDHadronicAnalysis_h
#define EDHadronicAnalysis_h


#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "Analysis/BoostedTopAnalysis/interface/SemileptonicAnalysis.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"


typedef edm::FWLiteAnalyzerWrapper<HadronicAnalysis> EDHadronicAnalysis;
typedef edm::FWLiteAnalyzerWrapper<SemileptonicAnalysis> EDSemileptonicAnalysis;


DEFINE_FWK_MODULE(EDHadronicAnalysis);
DEFINE_FWK_MODULE(EDSemileptonicAnalysis);

#endif
