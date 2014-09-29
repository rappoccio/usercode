
import ROOT

ROOT.gROOT.Macro("rootlogon.C")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes

from array import *
import math

class RooUnfoldMjjUnfoldedMeasurement :
    def __init__(self,
                 ibin=None,
                 nominalObj=None,
                 mcNonsymSysObjs=None,
                 mcSymSysObjs=None,
                 trueObj=None) :
        self.ibin=ibin
        self.nominalObj=nominalObj
        self.mcNonsymSysObjs=mcNonsymSysObjs
        self.mcSymSysObjs=mcSymSysObjs
        self.trueObj=trueObj
        self.nominalUnfolded = None
        self.rawHist = None
        self.mcRawHists = []
        self.mcNonsymSysUnfolded = []
        self.mcSymSysUnfolded = []
        self.graphs = []

    def doAllUnfolding(self) :
        self.nominalUnfolded = self.nominalObj.unfold( self.ibin )
        self.rawHist = self.nominalObj.dataHists[self.ibin]
        for isys in xrange(len(self.mcNonsymSysObjs)) :
            iUp = self.mcNonsymSysObjs[isys][0].unfold(self.ibin)
            iDn = self.mcNonsymSysObjs[isys][1].unfold(self.ibin)
            iname=self.mcNonsymSysObjs[isys][2]
            ititle=self.mcNonsymSysObjs[isys][3]
            self.mcNonsymSysUnfolded.append( [iUp, iDn, iname, ititle] )
        for isys in xrange(len(self.mcSymSysObjs)) :
            iSys = self.mcSymSysObjs[isys][0].unfold(self.ibin)
            iname= self.mcSymSysObjs[isys][1]
            self.mcRawHists.append( [self.mcSymSysObjs[isys][0].mcHists[self.ibin], iname] )
            self.mcSymSysUnfolded.append( [iSys, iname] )

    def calcMeasurement(self) :
        xbins = array('d', [])
        ex_stat = array('d', [])
        exlo = array('d', [])
        exhi = array('d', [])

        yraw = array('d', [])     # raw value
        ey_stat_raw = array('d', []) # raw stat errors
        ynom = array('d', [])     # central value
        ey_stat = array('d', [])  # stat only
        eylo = array('d', [])     # stat + sys, lower 
        eyhi = array('d', [])     # stat + sys, upper
        eyloE= []
        eyhiE= []

        ynom_f    = array('d', [])# central value for MC/data
        ey_stat_f = array('d', [])# stat only for MC/data
        eylo_f    = array('d', [])# stat+sys, lower for MC/data
        eyhi_f    = array('d', [])# stat+sys, higher for MC/data
        eyloE_f   = []
        eyhiE_f   = []

        for iexpSys in xrange(len(self.mcNonsymSysObjs)) :
            eyloE.append( array('d', [] ) )
            eyhiE.append( array('d', [] ) )
            eyloE_f.append( array('d', [] ) )
            eyhiE_f.append( array('d', [] ) )

        h = self.nominalUnfolded.Hreco()
        hraw = self.rawHist.Clone()
        hraw.SetName("hraw_" + str(self.ibin) )
        normOfThisBin = h.Integral()
        totalNorm = self.nominalObj.dataNorm
        

        # pythia6 truth :
        hpy6 = self.trueObj.trueHists[self.ibin]['Pythia6'].Clone()
        hpy6.SetName('hpy6_' + str(self.ibin))
        hpy8 = self.trueObj.trueHists[self.ibin]['Pythia8'].Clone()
        hpy8.SetName('hpy8_' + str(self.ibin))
        hhpp = self.trueObj.trueHists[self.ibin]['Herwig++'].Clone()
        hhpp.SetName('hhpp_' + str(self.ibin))


        # pythia6 raw :
        hpy6raw = self.mcRawHists[0][0].Clone()
        hpy6raw.SetName('hpy6raw_' + str(self.ibin))

        #hpy6.Scale( 1.0 / self.trueObj.trueNorms['Pythia6'] )
        #hpy8.Scale( 1.0 / self.trueObj.trueNorms['Pythia8'] )
        #hhpp.Scale( 1.0 / self.trueObj.trueNorms['Herwig++'] )

        #hpy6raw.Scale( 1.0 / self.trueObj.trueNorms['Pythia6'] )

        hpy6.Scale( 1.0 / hpy6.Integral() )
        hpy8.Scale( 1.0 / hpy8.Integral() )
        hhpp.Scale( 1.0 / hhpp.Integral() )

        hpy6raw.Scale( 1.0 / hpy6raw.Integral() )


        hpy6_f = hpy6.Clone()
        hpy6_f.SetName('hpy6_f_' + str(self.ibin))
        hpy8_f = hpy8.Clone()
        hpy8_f.SetName('hpy8_f_' + str(self.ibin))
        hhpp_f = hhpp.Clone()
        hhpp.SetName('hhpp_f_' + str(self.ibin))


        
        for ibin in range(1,h.GetNbinsX()-1):
            #print 'ibin = ' + str(ibin)

            xbins.append( h.GetXaxis().GetBinCenter(ibin) )
            ex_stat.append( h.GetXaxis().GetBinWidth(ibin) * 0.5 )
            exlo.append( h.GetXaxis().GetBinCenter(ibin) - h.GetXaxis().GetBinLowEdge(ibin) )
            exhi.append( h.GetXaxis().GetBinUpEdge(ibin) - h.GetXaxis().GetBinCenter(ibin)  )

            valnom = h.GetBinContent(ibin)
            valraw = hraw.GetBinContent(ibin)
            errnom = h.GetBinError(ibin)
            errraw = hraw.GetBinError(ibin)
            ynom.append( valnom / normOfThisBin )
            ey_stat.append( errnom / normOfThisBin )
            yraw.append( valraw / normOfThisBin )
            ey_stat_raw.append( errraw / normOfThisBin )
            
            
            if valnom > 0.0 :
                ynom_f.append(1.0)
                hpy6_f.SetBinContent( ibin, hpy6.GetBinContent(ibin)  / valnom * normOfThisBin )
                hpy8_f.SetBinContent( ibin, hpy8.GetBinContent(ibin)  / valnom * normOfThisBin )
                hhpp_f.SetBinContent( ibin, hhpp.GetBinContent(ibin)  / valnom * normOfThisBin )
                ey_stat_f.append( errnom/valnom)
            else :
                ynom_f.append(-10.0)
                hpy6_f.SetBinContent( ibin, -10.0 )
                hpy8_f.SetBinContent( ibin, -10.0 )
                hhpp_f.SetBinContent( ibin, -10.0 )
                ey_stat_f.append( 1.0 )

            errlo = (errnom * 0.5)**2
            errhi = (errnom * 0.5)**2
            errloE = [(errnom * 0.5)**2] * len(self.mcNonsymSysObjs)
            errhiE = [(errnom * 0.5)**2] * len(self.mcNonsymSysObjs)

            for isys in xrange(len(self.mcNonsymSysObjs)) :
                vallo = self.mcNonsymSysObjs[isys][0].unfolds[self.ibin].Hreco().GetBinContent(ibin)
                valhi = self.mcNonsymSysObjs[isys][1].unfolds[self.ibin].Hreco().GetBinContent(ibin)
                errnonsymlo = abs(valnom - vallo)
                errnonsymhi = abs(valhi - valnom)
                #print 'asymmetric error {0:15s} = +{1:6.2e} -{2:6.2e}'.format( self.mcNonsymSysUnfolded[isys][2], errnonsymhi, errnonsymlo )
                errlo += errnonsymlo**2
                errhi += errnonsymhi**2
                errloE[isys]+= errnonsymlo**2
                errhiE[isys]+= errnonsymhi**2

            for isys in xrange(len(self.mcSymSysObjs)) :
                valsym = self.mcSymSysObjs[isys][0].unfolds[self.ibin].Hreco().GetBinContent(ibin)
                errsym = abs(valnom - valsym) 
                errlo += (errsym * 0.5)**2
                errhi += (errsym * 0.5)**2

            eylo.append( math.sqrt(errlo) / normOfThisBin )
            eyhi.append( math.sqrt(errhi) / normOfThisBin )


            errloE_toWrite = [0.0] * len(self.mcNonsymSysObjs)
            errhiE_toWrite = [0.0] * len(self.mcNonsymSysObjs)
            for isys in xrange(len(self.mcNonsymSysObjs)) :
                isumlo = 0.0
                isumhi = 0.0
                for jsys in range(0,isys+1) :
                    isumlo += errloE[jsys]
                    isumhi += errhiE[jsys]
                errloE_toWrite[isys] = isumlo
                errhiE_toWrite[isys] = isumhi
            
            for isys in xrange(len(self.mcNonsymSysObjs)) :
                if valnom > 0.0 :
                    eyloE[isys].append( math.sqrt(errloE_toWrite[isys]) / normOfThisBin )
                    eyhiE[isys].append( math.sqrt(errhiE_toWrite[isys]) / normOfThisBin )
                else :
                    eyloE[isys].append( 0.0 )
                    eyhiE[isys].append( 0.0 )

            if valnom > 0.0 :
                eylo_f.append( math.sqrt(errlo)/valnom)
                eyhi_f.append( math.sqrt(errhi)/valnom)

                for isys in xrange(len(self.mcNonsymSysObjs)) :
                    eyloE_f[isys].append( math.sqrt(errloE_toWrite[isys]) / valnom )
                    eyhiE_f[isys].append( math.sqrt(errhiE_toWrite[isys]) / valnom )

            else :
                eylo_f.append( 1.0 )
                eyhi_f.append( 1.0 )
                for isys in xrange(len(self.mcNonsymSysObjs)) :
                    eyloE_f[isys].append( 1.0 )
                    eyhiE_f[isys].append( 1.0 )


        raw = ROOT.TGraphErrors( len(xbins), xbins, yraw, ex_stat, ey_stat_raw )
        raw.SetName('rawgr_' + str(self.ibin))

        statonly = ROOT.TGraphErrors( len(xbins), xbins, ynom, ex_stat, ey_stat )
        statonly.SetName('statonly_' + str(self.ibin))

        statsys = ROOT.TGraphAsymmErrors( len(xbins), xbins, ynom, exlo, exhi, eylo, eyhi )
        statsys.SetName('statsys_' + str(self.ibin))

        statonly_f = ROOT.TGraphErrors( len(xbins), xbins, ynom_f, ex_stat, ey_stat_f )
        statonly_f.SetName('statonlyFrac_' + str(self.ibin))
        
        statsys_f = ROOT.TGraphAsymmErrors( len(xbins), xbins, ynom_f, exlo, exhi, eylo_f, eyhi_f )
        statsys_f.SetName('statsysFrac_' + str(self.ibin))


        statsysE = []
        statsysE_f = []


        syscolors = [ROOT.kOrange+2, ROOT.kOrange-7, ROOT.kOrange-8, ROOT.kGreen]
        for isys in xrange(len(self.mcNonsymSysObjs)) :
            ## print self.mcNonsymSysObjs[isys][3]
            ## for ival in eyloE[isys] :
            ##     print '{0:6.2e}'.format(ival),
            ## print ''

            
            
            istatsysE = ROOT.TGraphAsymmErrors( len(xbins), xbins, ynom, exlo, exhi, eyloE[isys], eyhiE[isys] )
            istatsysE.SetName('statsysE_' + str(self.ibin) + '_' + str(isys))
            istatsysE.SetMarkerStyle( 20 )
            istatsysE.SetFillStyle( 1001 )
            istatsysE.SetFillColor( syscolors[isys] )
            statsysE.append( istatsysE )
        
            istatsysE_f = ROOT.TGraphAsymmErrors( len(xbins), xbins, ynom_f, exlo, exhi, eyloE_f[isys], eyhiE_f[isys] )
            istatsysE_f.SetName('statsysE_f_' + str(self.ibin) + '_' + str(isys))
            istatsysE_f.SetMarkerStyle( 20 )
            istatsysE_f.SetFillStyle( 1001 )
            istatsysE_f.SetFillColor( syscolors[isys] )
            statsysE_f.append( istatsysE_f )

        raw.SetMarkerStyle(24)

        statonly.SetMarkerStyle( 20 )
        statonly.SetFillStyle( 1001 )
        statonly.SetFillColor( ROOT.kYellow)

        statsys.SetMarkerStyle( 20 )
        statsys.SetFillStyle( 1001 )
        statsys.SetFillColor( ROOT.kYellow - 2 )

        statonly_f.SetMarkerStyle( 20 )
        statonly_f.SetFillStyle( 1001 )
        statonly_f.SetFillColor( ROOT.kYellow )
        
        statsys_f.SetMarkerStyle( 20 )
        statsys_f.SetFillStyle( 1001 )
        statsys_f.SetFillColor( ROOT.kYellow - 2 )
        
        hpy6.SetLineStyle(1)
        hpy8.SetLineStyle(2)
        hhpp.SetLineStyle(3)

        hpy6raw.SetLineStyle(1)

        hpy6_f.SetLineStyle(1)
        hpy8_f.SetLineStyle(2)
        hhpp_f.SetLineStyle(3)

        hpy6.SetLineColor(1)
        hpy8.SetLineColor(2)
        hhpp.SetLineColor(4)

        hpy6raw.SetLineColor(2)
        
        hpy6.SetLineWidth(1)
        hpy8.SetLineWidth(1)
        hhpp.SetLineWidth(3)
        hpy6_f.SetLineColor(1)
        hpy8_f.SetLineColor(2)
        hhpp_f.SetLineColor(4)
        hpy6_f.SetLineWidth(1)
        hpy8_f.SetLineWidth(1)
        hhpp_f.SetLineWidth(3)



        #self.graphs = [statonly, statsysE, statsys,hpy6,hpy8,hhpp, statonly_f,statsysE_f, statsys_f, hpy6_f, hpy8_f, hhpp_f, raw, hpy6raw]
        self.graphs = [statonly, statsysE, statsys,hpy6,hpy8,hhpp, statonly_f,statsysE_f, statsys_f, hpy6_f, hpy8_f, hhpp_f, None, None]
        
