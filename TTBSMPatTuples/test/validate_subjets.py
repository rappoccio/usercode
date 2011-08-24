#! /usr/bin/env python

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

files = ["ttbsm_386.root"]
events = Events (files)
handle  = Handle ("std::vector<pat::Jet>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("selectedPatJetsCA8PrunedPUSubPF")

# loop over events
i = 0
for event in events:
    i = i + 1
    # use getByLabel, just like in cmsRun
    event.getByLabel (label, handle)
    # get the product
    jets = handle.product()

    for ijet in range(0,len(jets)):
        print 'Jet {0:6d} : pt = {1:6.2f}, m = {2:6.2f}, nsubjets    = {3:6d} :'.format( ijet,
                                                                                      jets[ijet].pt(),
                                                                                      jets[ijet].mass(),
                                                                                      jets[ijet].numberOfDaughters())
        for ida in range(0,jets[ijet].numberOfDaughters()) :
            print '+ Da{0:6d} : pt = {1:6.2f}, m = {2:6.2f}, nconstituents = {3:6d} :'.format( ida,
                                                                                               jets[ijet].daughterPtr(ida).pt(),
                                                                                               jets[ijet].daughterPtr(ida).mass(),
                                                                                               jets[ijet].daughterPtr(ida).numberOfDaughters())

            print '----'
            for jda in range(0,jets[ijet].daughterPtr(ida).numberOfDaughters()) :
                print '++Da{0:6d} : pt = {1:6.2f}, m = {2:6.2f}, nconstituents = {3:6d} :'.format( jda,
                                                                                                   jets[ijet].daughterPtr(ida).daughterPtr(jda).pt(),
                                                                                                   jets[ijet].daughterPtr(ida).daughterPtr(jda).mass(),
                                                                                                   jets[ijet].daughterPtr(ida).daughterPtr(jda).numberOfDaughters())

            
            print '----'
            
        print '--------------'
        
