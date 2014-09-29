import ROOT

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle

############################################
#     Trigger information                  #
############################################
# Use the same trigger thresholds as QCD-11-004 in AN-364-v4 Table 8

class TrigHelper :
    def __init__ ( self, verbose=False ) :
        self.verbose=verbose
        self.trigLabel = ( "dijetTriggerFilter", 'jetPaths')
        self.trigHandle = Handle("std::vector<std::string>")
        # Here are the trigger thresholds for the various eta bins.
        # In the following, each entry is an eta bin. The
        # two fields are then [etamin,etamax], and the
        # list of mjj thresholds for HLT_Jet60,110,190,240,370.
        self.trigThresholds = [
            [[0.0, 0.5], [ 178.,  324.,  533.,  663.,  970., 7000.] ],
            [[0.5, 1.0], [ 240.,  390.,  645.,  820., 1218., 7000.] ],
            [[1.0, 1.5], [ 369.,  615.,  998., 1261., 1904., 7000.] ],
            [[1.5, 2.0], [ 530.,  920., 1590., 1985., 3107., 7000.] ],
            [[2.0, 2.5], [ 913., 1549., 2665., 3700., 4000., 7000.] ]
            ]
        self.trigsToKeep = [
            'HLT_Jet60',
            'HLT_Jet110',
            'HLT_Jet190',
            'HLT_Jet240',
            'HLT_Jet370',
        ]

    def passEventMC( self, event, mjjReco, etaMax ) :

        for ibin in range(0, len(self.trigThresholds)) :
            if etaMax >= self.trigThresholds[ibin][0][0] and etaMax < self.trigThresholds[ibin][0][1] :
                break
        mjjThresholds = self.trigThresholds[ibin][1]

        passMjjTrig = False
        if self.verbose :
            print 'testing MC mjjReco = ' + str(mjjReco) + ', etamax = ' + str(etaMax) + ', threshold = ' + str(mjjThresholds[0])
        if mjjReco >= mjjThresholds[0] :
            if self.verbose :
                print '  ----> passed!'
            passMjjTrig = True
        return passMjjTrig

    def passEventData( self, event, mjjReco, etaMax ) :
        iTrigHist = None
        event.getByLabel( self.trigLabel, self.trigHandle )
        trigs = self.trigHandle.product()

        for ibin in range(0, len(self.trigThresholds)) :
            if etaMax >= self.trigThresholds[ibin][0][0] and etaMax < self.trigThresholds[ibin][0][1] :
                break
        mjjThresholds = self.trigThresholds[ibin][1]

        acceptedPaths = []
        trigPassedName = None
        passMjjTrig = False


        # If there are any accepted paths, cache them. Then match to the lookup table "trigThresholds" to see if
        # the event is in the correct mjj bin for the trigger in question.
        if len( trigs ) > 0 :
            for ipath in xrange( len(trigs)-1, -1, -1) :
                path = trigs[ipath]
                for ikeep in xrange(len(self.trigsToKeep)-1, -1, -1) :
                    if self.verbose :
                        print '   ----- checking trigger ' + self.trigsToKeep[ikeep] + ' : mjjThreshold = ' + str(mjjThresholds[ikeep])
                    if path.find( self.trigsToKeep[ikeep] ) >= 0 and mjjReco >= mjjThresholds[ikeep] and mjjReco < mjjThresholds[ikeep + 1]:
                        trigPassedName = path
                        iTrigHist = ikeep
                        passMjjTrig = True
                        if self.verbose :
                            print '    -----------> Joy and elation, it worked! trigger = ' + self.trigsToKeep[iTrigHist]
                        break
                if passMjjTrig == True :
                    break

        passEvent = passMjjTrig
        return [passEvent,iTrigHist]
