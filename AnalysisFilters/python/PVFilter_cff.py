import FWCore.ParameterSet.Config as cms


from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

pvFilter = cms.EDFilter("PVFilter",
                        pvSelector
                        )
