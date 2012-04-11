import ROOT

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle

class TriggerAndEventSelectionObject :
    """Class to select triggers and ensure rho is sane"""
    def __init__(self, inputTrigs):
        self.rhoHandle           = Handle("double")
        self.rhoLabel            = ( "ttbsmAna", "rho" )
        self.myTrigIndexHandle   = Handle( "std::vector<int>")
        self.myTrigIndexLabel    = ( "ttbsmAna",  "myTrigIndex" )
        self.prescalesHandle     = Handle( "std::vector<int>")
        self.prescalesLabel      = ( "ttbsmAna",  "prescales" )
        self.trigNamesHandle     = Handle( "std::vector<string>")
        self.trigNamesLabel      = ( "ttbsmAna",  "trigNames" )
        self.trigs               = inputTrigs

    def select(self, event) :

        if not event.object().isValid():
            return False

        event.getByLabel (self.myTrigIndexLabel, self.myTrigIndexHandle)
        if not self.myTrigIndexHandle.isValid():
            print 'myTrigIndex is invalid'
            return False
        myTrigIndices = self.myTrigIndexHandle.product()
    
        event.getByLabel (self.prescalesLabel, self.prescalesHandle)
        if not self.prescalesHandle.isValid():
            print 'prescales is invalid'
            return False
        prescales = self.prescalesHandle.product()

        event.getByLabel (self.rhoLabel, self.rhoHandle)
        if not self.rhoHandle.isValid():
            print 'rho is invalid'
            return False
        rho = self.rhoHandle.product()[0]
        if abs(rho) > 100 or rho < 0.0 :
            print 'AAAACCCKK!!! rho = ' + str(rho)
            return False
    
        found = False
        firedTrig = -1
        for mytrig in self.trigs :
            if mytrig in myTrigIndices :
                found = True
                firedTrig = mytrig
                break
            
            
        return found
                
