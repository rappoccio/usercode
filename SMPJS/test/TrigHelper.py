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
        self.trigThresholds = [ 50., 150., 220., 300., 450., 7000.]
        self.trigsToKeep = [
            'HLT_Jet60',
            'HLT_Jet110',
            'HLT_Jet190',
            'HLT_Jet240',
            'HLT_Jet370',
        ]

    def passEventMC( self, event, ptAvg ) :

        for ibin in range(0, len(self.trigThresholds)) :
            if ptAvg >= self.trigThresholds[ibin] and ptAvg < self.trigThresholds[ibin+1] :
                return True

    def passEventData( self, event, ptAvg ) :
        iTrigHist = None
        event.getByLabel( self.trigLabel, self.trigHandle )
        trigs = self.trigHandle.product()

        acceptedPaths = []
        trigPassedName = None
        passPtAvgTrig = False


        # If there are any accepted paths, cache them. Then match to the lookup table "trigThresholds" to see if
        # the event is in the correct mjj bin for the trigger in question.
        if len( trigs ) > 0 :
            for ipath in xrange( len(trigs)-1, -1, -1) :
                path = trigs[ipath]
                for ikeep in xrange(len(self.trigsToKeep)-1, -1, -1) :
                    if self.verbose :
                        print '   ----- checking trigger ' + self.trigsToKeep[ikeep] + ' : ptAvgThreshold = ' + str(self.trigThresholds[ikeep])
                    if path.find( self.trigsToKeep[ikeep] ) >= 0 and ptAvg >= self.trigThresholds[ikeep] and ptAvg < self.trigThresholds[ikeep + 1]:
                        trigPassedName = path
                        iTrigHist = ikeep
                        passPtAvgTrig = True
                        if self.verbose :
                            print '    -----------> Joy and elation, it worked! trigger = ' + self.trigsToKeep[iTrigHist]
                        break
                if passPtAvgTrig == True :
                    break

        passEvent = passPtAvgTrig
        return [passEvent,iTrigHist]
