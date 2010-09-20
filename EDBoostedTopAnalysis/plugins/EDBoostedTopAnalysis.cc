#ifndef EDHadronicAnalysis_h
#define EDHadronicAnalysis_h


#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "Analysis/BoostedTopAnalysis/interface/SemileptonicAnalysis.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetAnalysis.h"

typedef edm::FWLiteAnalyzerWrapper<HadronicAnalysis> EDHadronicAnalysis;
typedef edm::FWLiteAnalyzerWrapper<SemileptonicAnalysis> EDSemileptonicAnalysis;
typedef edm::FWLiteAnalyzerWrapper<WPlusBJetAnalysis>   EDWPlusBJetAnalysis;

DEFINE_FWK_MODULE(EDHadronicAnalysis);
DEFINE_FWK_MODULE(EDSemileptonicAnalysis);
DEFINE_FWK_MODULE(EDWPlusBJetAnalysis);

#endif
