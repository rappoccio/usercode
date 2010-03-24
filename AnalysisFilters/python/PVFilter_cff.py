import FWCore.ParameterSet.Config as cms


from Analysis.AnalysisFilters.pvSelector_cfi import pvSelector

pvFilter = cms.EDFilter("PVFilter",
                        pvSelector
                        )
