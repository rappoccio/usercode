import ROOT

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

import math
from DataFormats.FWLite import Events, Handle


#############################
# Matching one jet to another in some other collection
# Uses DR < 0.5 matching
#############################
def findJetInColl( jet0, jets ) :
    minDR = 0.2
    ijet = 0
    for jet in jets :
        dR = jet0.DeltaR( jet )
        if dR < minDR :
            return [jet,ijet]
        ijet += 1
    return [None,None]



def printRawColl( coll, name, altindex=None ) :
    for ijet in xrange(len(coll)) :
        if coll[ijet] is not None :
            if altindex is None :
                print '{0:20s} : {1:4.0f}, pt,eta,phi,m = {2:6.2f},{3:6.2f},{4:6.2f},{5:6.2f}'.format(
                    name,
                    ijet,
                    coll[ijet].Perp(),
                    coll[ijet].Eta(),
                    coll[ijet].Phi(),
                    coll[ijet].M()
                    )
            else :
                print '{0:16s} ({1:2.0f}) : {2:4.0f}, pt,eta,phi,m = {3:6.2f},{4:6.2f},{5:6.2f},{6:6.2f}'.format(
                    name,
                    ijet,
                    altindex[ijet],
                    coll[ijet].Perp(),
                    coll[ijet].Eta(),
                    coll[ijet].Phi(),
                    coll[ijet].M()
                    )
        else :
            print '{0:20s} : None'.format( name )



#############################
#  Get a collection from    #
#  the event record, and    #
#  correct them. Return     #
#  list of corrected p4's   #
#############################
class PyFWLiteJetColl :
    def __init__ ( self,
		  coll,                               # collection name to use
		  jec=None,                           # JEC to use
		  jecUnc=None, upOrDown=True,         # JEC uncertainty, up or down
		  useGen = False,                     # use gen-jet info only
		  jerSmear=None,                      # jet energy smearing
		  jarSmear=None,                      # jet angular smearing
		  jetPtMin = 20.0, jetEtaMax = 2.5) : # kinematic cuts):
        self.jetCollPxHandle         = Handle( "std::vector<float>" )
        self.jetCollPxLabel          = ( coll ,   "px" )
        self.jetCollPyHandle         = Handle( "std::vector<float>" )
        self.jetCollPyLabel          = ( coll ,   "py" )
        self.jetCollPzHandle         = Handle( "std::vector<float>" )
        self.jetCollPzLabel          = ( coll ,   "pz" )
        self.jetCollEnergyHandle     = Handle( "std::vector<float>" )
        self.jetCollEnergyLabel      = ( coll ,   "energy" )
        self.jetCollJetAreaHandle    = Handle( "std::vector<float>" )
        self.jetCollJetAreaLabel     = ( coll ,   "jetArea" )
        self.jetCollJecFactorHandle  = Handle( "std::vector<float>" )
        self.jetCollJecFactorLabel   = ( coll ,   "jecFactor" )
        self.jetColl = []
	self.matchedRecoColl = []
        self.matchedRecoIndices = []
	self.matchedGenColl = []
        self.matchedGenIndices = []
	self.jec = jec
        self.jecUnc = jecUnc
        self.upOrDown = upOrDown
        self.useGen = useGen
	self.jerSmearVal=jerSmear
	self.jarSmearVal=jarSmear
        self.jetPtMin = jetPtMin
        self.jetEtaMax = jetEtaMax


    def printJetColl( self ) :
	print 'Jet collection : '
        printRawColl( self.jetColl, '-ijet')
        if self.matchedRecoColl is not None:
            print 'Matched RECO collection : '
            printRawColl( self.matchedRecoColl, '-matched reco', self.matchedRecoIndices)
        else :
            print '  -- no matched reco'

        if self.matchedGenColl is not None:
            print 'Matched GEN collection : '
            printRawColl( self.matchedGenColl, '-matched gen', self.matchedGenIndices)
        else :
            print '  -- no matched gen'


    def getMatchedGen(self) :
            return self.matchedGenColl

    def getMatchedReco(self) :
	    return self.matchedRecoColl

    def getMatchedGenIndices(self) :
            return self.matchedGenIndices

    def getMatchedRecoIndices(self) :
	    return self.matchedRecoIndices

    def getJets( self, event, rho=None, genToMatch=None, recoToMatch=None ) :
	# Get a collection of jets. There are three optional parameters:
	#  rho: mean-pt-per-unit-area
	#  genToMatch : any matched gen-jet to use for smearing, etc.
	#  recoToMatch : any matched reco-jet to use for matching groomed to ungroomed, etc.
	# If the JEC is defined (self.jec), then the jets are corrected.
	# If the JEC uncertainty is defined (self.jecunc) then the jets are scaled up or down
	#    according to the user's choice for systematic studies. 
        self.jetColl = []
	self.matchedRecoColl = []
	self.matchedGenColl = []
	self.matchedRecoIndices = []
	self.matchedGenIndices = []
	# Always get "this" collection. 
        event.getByLabel( self.jetCollPxLabel, self.jetCollPxHandle )
        self.jetCollPxs = self.jetCollPxHandle.product()
        event.getByLabel( self.jetCollPyLabel, self.jetCollPyHandle )
        self.jetCollPys = self.jetCollPyHandle.product()
        event.getByLabel( self.jetCollPzLabel, self.jetCollPzHandle )
        self.jetCollPzs = self.jetCollPzHandle.product()
        event.getByLabel( self.jetCollEnergyLabel, self.jetCollEnergyHandle )
        self.jetCollEnergys = self.jetCollEnergyHandle.product()
        if not self.useGen :
	    # If we're using the reco jets, get the jet area and JEC factors. 
            event.getByLabel( self.jetCollJetAreaLabel, self.jetCollJetAreaHandle )
            self.jetCollJetAreas = self.jetCollJetAreaHandle.product()
            event.getByLabel( self.jetCollJecFactorLabel, self.jetCollJecFactorHandle )
            self.jetCollJecFactors = self.jetCollJecFactorHandle.product()

            for idef in range(0,len(self.jetCollPxs)):
		# Uncorrect the jets first, to get the raw jet
                jdefRaw = ROOT.TLorentzVector(
                    self.jetCollPxs[idef] * self.jetCollJecFactors[idef],
                    self.jetCollPys[idef] * self.jetCollJecFactors[idef],
                    self.jetCollPzs[idef] * self.jetCollJecFactors[idef],
                    self.jetCollEnergys[idef] * self.jetCollJecFactors[idef]
                    )

                if self.jec is not None :
		    # if JEC is there, correct the raw jets. 
                    self.jec.setJetEta(jdefRaw.Eta())
                    self.jec.setJetPt(jdefRaw.Perp())
                    self.jec.setJetA(self.jetCollJetAreas[idef])
                    self.jec.setRho(rho)
                    factor = self.jec.getCorrection()

                    if self.jecUnc is not None:
                        self.jecUnc.setJetEta( jdefRaw.Eta() )
                        self.jecUnc.setJetPt( jdefRaw.Perp() * factor ) 
                        unc1 = self.jecUnc.getUncertainty( self.upOrDown )
                        unc2 = 0.05
                        unc = math.sqrt(unc1*unc1 + unc2*unc2)
                        if self.upOrDown :
                            factor *= (1 + unc)
                        else :
                            factor *= (1 - unc)

                                                  
                else :
		    factor = 1.0
                    

		# Get the corrected jets. 
		jdef = ROOT.TLorentzVector(
			jdefRaw.Px() * factor,
			jdefRaw.Py() * factor,
			jdefRaw.Pz() * factor,
			jdefRaw.Energy() * factor
			)

		# Now see if there are any matched RECO jets.
		# This is used for groomed jet collections.
                [jreco,jRecoIndex] = [None,None]
		if recoToMatch is not None:
                    [jreco,jRecoIndex] = findJetInColl( jdef, recoToMatch )

		# Now see if there are any matched GEN jets.
		# This is used for smearing and to check
		# responses.
                [jgen,jGenIndex] = [None,None]
		if genToMatch is not None:
                    [jgen,jGenIndex] = findJetInColl( jdef, genToMatch )


		# Now do the smearing to the gen matched collection if desired.
		# Change the jet energy and angular resolution based on the
		# matched genjet
		if self.jarSmearVal is not None and jgen is not None:
		    recoeta = jdef.Eta()
		    geneta = jgen.Eta()
		    deltaeta = (recoeta-geneta)*self.jarSmearVal
		    etaSmear = max(0.0,(recoeta+deltaeta)/recoeta)
		    recophi = jdef.Phi()
		    genphi = jgen.Phi()
		    deltaphi = (recophi-genphi)*self.jarSmearVal 
		    phiSmear = max(0.0,(recophi+deltaphi)/recophi)

		    jdef.SetPhi( jdef.Phi()*phiSmear )
		    etanew = jdef.Eta()*etaSmear
		    # Stupid root doesn't have SetEta for TLorentzVector... grrrr
		    thetanew = 2.0*ROOT.TMath.ATan(ROOT.TMath.Exp(-etanew))
		    jdef.SetTheta( thetanew )

		if self.jerSmearVal is not None and jgen is not None:
		    recopt = jdef.Perp()
		    genpt = jgen.Perp()
		    deltapt = (recopt-genpt)*self.jerSmearVal
		    ptSmear = max(0.0, (recopt+deltapt)/recopt)
		    jdef *= ptSmear


                if jdef.Perp() > self.jetPtMin and abs(jdef.Rapidity()) < self.jetEtaMax :
                    self.jetColl.append( jdef )
                    self.matchedRecoColl.append( jreco )
                    self.matchedRecoIndices.append( jRecoIndex)
                    self.matchedGenColl.append( jgen )
                    self.matchedGenIndices.append( jGenIndex)
        else :
	    # Otherwise, this is for GenJets only, so no need to do corrections.
	    # Just grab the jets. 
            for idef in range(0,len(self.jetCollPxs)):
                jdefRaw = ROOT.TLorentzVector(
                    self.jetCollPxs[idef] ,
                    self.jetCollPys[idef] ,
                    self.jetCollPzs[idef] ,
                    self.jetCollEnergys[idef] 
                    )
                self.jetColl.append(jdefRaw)
        return self.jetColl

