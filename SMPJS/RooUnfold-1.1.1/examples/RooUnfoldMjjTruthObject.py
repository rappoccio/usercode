
import ROOT

ROOT.gROOT.Macro("rootlogon.C")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes

class RooUnfoldMjjTruthObject :
    def __init__( self,
                 nbins=10,
                 ptBins=None,
                 trueFileName=None,
                 trueNames=None
                 ) :
        self.trueFile = ROOT.TFile(trueFileName)
        self.trueNames = trueNames
        self.responses = []
        self.trueHists = []
        self.nbins=nbins
        self.ptBins=ptBins
        self.trueNorms = dict( {None:None} )
        for ientry in self.trueNames.iteritems() :
            self.trueNorms.update( {ientry[0]:0.0} )
        for ibin in xrange(nbins) :
            self.trueHists.append( dict({None:None}) )
            ptWidth = self.ptBins[ibin+1] - self.ptBins[ibin]
            for ientry in self.trueNames.iteritems() :
                ikey = ientry[0]
                hTrue = self.trueFile.Get( ientry[1] + '_pt' + str(ibin) )
                hTrue.Scale(1.0 / ptWidth )
                for imbin in range(1,hTrue.GetNbinsX() + 1) :
                    val = hTrue.GetBinContent( imbin )
                    err = hTrue.GetBinError( imbin )
                    dmjet = hTrue.GetXaxis().GetBinUpEdge(imbin) - hTrue.GetXaxis().GetBinLowEdge(imbin)
                    hTrue.SetBinContent( imbin, val / dmjet )
                    hTrue.SetBinError  ( imbin, err / dmjet )
                self.trueNorms[ikey] += hTrue.Integral()
                self.trueHists[ibin].update( {ikey:hTrue} )
                

    def clear(self) :
        self.trueHists = []
