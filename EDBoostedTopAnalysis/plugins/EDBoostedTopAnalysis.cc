#ifndef EDHadronicAnalysis_h
#define EDHadronicAnalysis_h


#include "Analysis/BoostedTopAnalysis/interface/HadronicAnalysis.h"
#include "Analysis/BoostedTopAnalysis/interface/SemileptonicAnalysis.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetAnalysis.h"
#include "Analysis/BoostedTopAnalysis/interface/CombinedQCDEstimation.h"
#include "Analysis/BoostedTopAnalysis/interface/Type22QCDEstimation.h"
#include "Analysis/BoostedTopAnalysis/interface/MistagMaker.h"


typedef edm::AnalyzerWrapper<HadronicAnalysis> EDHadronicAnalysis;
typedef edm::AnalyzerWrapper<SemileptonicAnalysis> EDSemileptonicAnalysis;
typedef edm::AnalyzerWrapper<WPlusBJetAnalysis>   EDWPlusBJetAnalysis;
typedef edm::AnalyzerWrapper<CombinedQCDEstimation>  EDCombinedQCDEstimation;
typedef edm::AnalyzerWrapper<Type22QCDEstimation>  EDType22QCDEstimation;
typedef edm::AnalyzerWrapper<MistagMaker>       EDMistagMaker;

DEFINE_FWK_MODULE(EDHadronicAnalysis);
DEFINE_FWK_MODULE(EDSemileptonicAnalysis);
DEFINE_FWK_MODULE(EDWPlusBJetAnalysis);
DEFINE_FWK_MODULE(EDCombinedQCDEstimation);
DEFINE_FWK_MODULE(EDType22QCDEstimation);
DEFINE_FWK_MODULE(EDMistagMaker);

#endif
