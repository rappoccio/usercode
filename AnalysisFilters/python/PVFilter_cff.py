import FWCore.ParameterSet.Config as cms


from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector as pvSelectorInput

pvFilter = cms.EDFilter("PVFilter",
                        pvSelector = cms.PSet( pvSelectorInput )
                        )
