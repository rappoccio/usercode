#ifndef EDHadronicAnalysis_h
#define EDHadronicAnalysis_h


#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "Analysis/BoostedTopAnalysis/interface/SemileptonicAnalysis.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetAnalysis.h"

typedef edm::AnalyzerWrapper<HadronicAnalysis> EDHadronicAnalysis;
typedef edm::AnalyzerWrapper<SemileptonicAnalysis> EDSemileptonicAnalysis;
typedef edm::AnalyzerWrapper<WPlusBJetAnalysis>   EDWPlusBJetAnalysis;

DEFINE_FWK_MODULE(EDHadronicAnalysis);
DEFINE_FWK_MODULE(EDSemileptonicAnalysis);
DEFINE_FWK_MODULE(EDWPlusBJetAnalysis);

#endif
