
import ROOT

ROOT.gROOT.Macro("rootlogon.C")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes

from array import array

class RooUnfoldMjjObject :
    def __init__( self,
                 nbins=11,
                 ptBins=None,
                 responseFileName=None,
                 obsFileName=None,
                 responseName='response',
                 dataHistName='jetdata',
                 mcHistName='QCD_pythia6_z2_plots_nominal'
                 ) :
        self.ptBins=ptBins
        self.nbins=nbins
        self.responseFile = ROOT.TFile(responseFileName)
        self.obsFile = ROOT.TFile(obsFileName)
        self.responseName=responseName
        self.dataHistName=dataHistName
        self.mcHistName=mcHistName
        self.dataHists = []
        self.mcHists = []
        self.responses = []
        self.unfolds = {None:None}
        self.dataNorm = 0.0
        self.mcNorm = 0.0
        for ibin in xrange(nbins) :
            ptWidth = self.ptBins[ibin+1] - self.ptBins[ibin]
            #print 'getting ' + self.mcHistName + '_pt' + str(ibin)
            hMC   = self.obsFile.Get( self.mcHistName + '_pt' + str(ibin) )
            hData = self.obsFile.Get( self.dataHistName + '_pt' + str(ibin) )
            hMC.Sumw2()
            hData.Sumw2()
            hMC.Scale( 1.0 / ptWidth )
            hData.Scale( 1.0 / ptWidth )
            resp  = self.responseFile.Get( self.responseName + '_pt' + str(ibin) )
            for hist in [hMC, hData] :
                for imbin in range(1,hist.GetNbinsX() + 1) :
                    val = hist.GetBinContent( imbin )
                    err = hist.GetBinError( imbin )
                    dmjet = hist.GetXaxis().GetBinUpEdge(imbin) - hist.GetXaxis().GetBinLowEdge(imbin)
                    hist.SetBinContent( imbin, val / dmjet )
                    hist.SetBinError  ( imbin, err / dmjet )
            self.mcHists.append(hMC)
            self.dataHists.append(hData)
            self.responses.append(resp)
            self.dataNorm += hData.Integral()
            self.mcNorm += hMC.Integral()


    def clear(self) :
        self.unfolds = {None:None}

    def unfold( self, ibin=None, closureTest=False ) :
        if ibin is None :
            return None
        if self.unfolds.has_key(ibin) :
            print 'Unfolding for bin ' + str(ibin) + ' already computed, returning it. If you do not want this, call clear() before this call.'
            return self.unfolds[ibin]
        else :
            unfold=None
            if not closureTest :
                print self.responses[ibin]
                unfold= RooUnfoldBayes     (self.responses[ibin], self.dataHists[ibin], 4)
            else :
                unfold= RooUnfoldBayes     (self.responses[ibin], self.mcHists[ibin], 4)
            self.unfolds.update( {ibin:unfold} )
            return unfold
        
