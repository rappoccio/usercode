import subprocess

class Plot :
    def __init__( self, outname, hist1, hist2, NQCD, rebin, newYlabel ) :
        self.outname = outname
        self.hist1 = hist1
        self.hist2 = hist2
        self.NQCD = NQCD
        self.rebin = rebin
        self.newYlabel = newYlabel
    def draw(self) :
        if self.hist2 != None : 
            s = 'python makeBarePlots.py --outname=' + self.outname + \
                ' --hist1=' + self.hist1 + ' --hist2=' + self.hist2 + \
                ' --NQCD=' + str(self.NQCD) + \
                ' --rebin=' + str(self.rebin) + ' --newYlabel=' + self.newYlabel + ' --plotNom'
        else : 
            s = 'python makeBarePlots.py --outname=' + self.outname + \
                ' --hist1=' + self.hist1 + \
                ' --NQCD=' + str(self.NQCD) + \
                ' --rebin=' + str(self.rebin) + ' --newYlabel=' + self.newYlabel + ' --plotNom'
        print 'executing ' + s
        subprocess.call( [s], shell=True )



def main() :
    outname = 'mujets'
    plots = [
        Plot( outname=outname, hist1='csv1LepJet2', hist2=None, NQCD=143202.7, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='csv1LepJet3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='csv1LepJet4', hist2=None, NQCD=384.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='csv1LepJet6', hist2=None, NQCD=91.3    , rebin=2, newYlabel='Jets\ /\ 0.04'),
        Plot( outname=outname, hist1='csv1LepJet7', hist2=None, NQCD=2       , rebin=2, newYlabel='Jets\ /\ 0.04'),
        
        Plot( outname=outname, hist1='csv2LepJet2', hist2=None, NQCD=143202.7*0.12, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='csv2LepJet3', hist2=None, NQCD=3321.1*0.30  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='csv2LepJet4', hist2=None, NQCD=384.1*0.48   , rebin=2, newYlabel='Jets\ /\ 0.04'),
        Plot( outname=outname, hist1='csv2LepJet6', hist2=None, NQCD=91.3*0.52    , rebin=2, newYlabel='Jets\ /\ 0.04'),
        Plot( outname=outname, hist1='csv2LepJet7', hist2=None, NQCD=2*0.62       , rebin=2, newYlabel='Jets\ /\ 0.04'),
        
        Plot( outname=outname, hist1='eta1LepJet2', hist2=None, NQCD=143202.7, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='eta1LepJet3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='eta1LepJet4', hist2=None, NQCD=384.1   , rebin=2, newYlabel='Jets\ /\ 0.2'),
        Plot( outname=outname, hist1='eta1LepJet6', hist2=None, NQCD=91.3    , rebin=2, newYlabel='Jets\ /\ 0.2'),
        Plot( outname=outname, hist1='eta1LepJet7', hist2=None, NQCD=2       , rebin=2, newYlabel='Jets\ /\ 0.2'),
        
        Plot( outname=outname, hist1='eta2LepJet2', hist2=None, NQCD=143202.7*0.12, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='eta2LepJet3', hist2=None, NQCD=3321.1*0.30  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='eta2LepJet4', hist2=None, NQCD=384.1*0.48   , rebin=2, newYlabel='Jets\ /\ 0.2'),
        Plot( outname=outname, hist1='eta2LepJet6', hist2=None, NQCD=91.3*0.52    , rebin=2, newYlabel='Jets\ /\ 0.2'),
        Plot( outname=outname, hist1='eta2LepJet7', hist2=None, NQCD=2*0.62       , rebin=2, newYlabel='Jets\ /\ 0.2'),
        
        Plot( outname=outname, hist1='etaLep0', hist2=None, NQCD=1520239.0, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='etaLep2', hist2=None, NQCD=143202.7 , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='etaLep3', hist2=None, NQCD=3321.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='etaLep4', hist2=None, NQCD=384.1    , rebin=2, newYlabel='Muons\ /\ 0.2'),
        Plot( outname=outname, hist1='etaLep6', hist2=None, NQCD=91.3     , rebin=2, newYlabel='Muons\ /\ 0.2'),
        
        Plot( outname=outname, hist1='hadtop_mass3', hist2=None, NQCD=3321.1, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='hadtop_mass4', hist2=None, NQCD=384.1 , rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='hadtop_mass6', hist2=None, NQCD=91.3  , rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='hadtop_mass7', hist2=None, NQCD=2     , rebin=2, newYlabel='Events\ /\ 10\ GeV'),
                
        Plot( outname=outname, hist1='hadtop_pt3', hist2=None, NQCD=3321.1, rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='hadtop_pt4', hist2=None, NQCD=384.1 , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='hadtop_pt6', hist2=None, NQCD=91.3  , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='hadtop_pt7', hist2=None, NQCD=2     , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='hadtop_y3', hist2=None, NQCD=3321.1, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='hadtop_y4', hist2=None, NQCD=384.1 , rebin=2, newYlabel='Events\ /\ 0.2'),
        Plot( outname=outname, hist1='hadtop_y6', hist2=None, NQCD=91.3  , rebin=2, newYlabel='Events\ /\ 0.2'),
        Plot( outname=outname, hist1='hadtop_y7', hist2=None, NQCD=2     , rebin=2, newYlabel='Events\ /\ 0.2'),
        
        Plot( outname=outname, hist1='ht2', hist2=None, NQCD=143202.7, rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='ht3', hist2=None, NQCD=3321.1  , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='ht4', hist2=None, NQCD=384.1   , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        Plot( outname=outname, hist1='ht6', hist2=None, NQCD=91.3    , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        Plot( outname=outname, hist1='ht7', hist2=None, NQCD=2       , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        
        Plot( outname=outname, hist1='htLep2', hist2=None, NQCD=143202.7, rebin=5, newYlabel='Events\ /\ 50\ GeV'),
    	Plot( outname=outname, hist1='htLep3', hist2=None, NQCD=3321.1  , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        Plot( outname=outname, hist1='htLep4', hist2=None, NQCD=384.1   , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        Plot( outname=outname, hist1='htLep6', hist2=None, NQCD=91.3    , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        Plot( outname=outname, hist1='htLep7', hist2=None, NQCD=2       , rebin=5, newYlabel='Events\ /\ 50\ GeV'),
        
        Plot( outname=outname, hist1='lepMET2', hist2=None, NQCD=143202.7, rebin=5, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='lepMET3', hist2=None, NQCD=3321.1  , rebin=5, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='lepMET4', hist2=None, NQCD=384.1   , rebin=10, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='lepMET6', hist2=None, NQCD=91.3    , rebin=10, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='lepMET7', hist2=None, NQCD=2       , rebin=10, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='leptop_mass3', hist2=None, NQCD=3321.1, rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='leptop_mass4', hist2=None, NQCD=384.1 , rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='leptop_mass6', hist2=None, NQCD=91.3  , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='leptop_mass7', hist2=None, NQCD=2     , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='leptop_pt3', hist2=None, NQCD=3321.1, rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='leptop_pt4', hist2=None, NQCD=384.1 , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='leptop_pt6', hist2=None, NQCD=91.3  , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='leptop_pt7', hist2=None, NQCD=2     , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='leptop_y3', hist2=None, NQCD=3321.1, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='leptop_y4', hist2=None, NQCD=384.1 , rebin=2, newYlabel='Events\ /\ 0.2'),
        Plot( outname=outname, hist1='leptop_y6', hist2=None, NQCD=91.3  , rebin=2, newYlabel='Events\ /\ 0.2'),
        Plot( outname=outname, hist1='leptop_y7', hist2=None, NQCD=2     , rebin=2, newYlabel='Events\ /\ 0.2'),
        
        Plot( outname=outname, hist1='nBJets0', hist2=None, NQCD=1520239.0, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nBJets2', hist2=None, NQCD=143202.7 , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nBJets3', hist2=None, NQCD=3321.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nBJets4', hist2=None, NQCD=384.1    , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nBJets6', hist2=None, NQCD=91.3     , rebin=1, newYlabel=''),
        
        Plot( outname=outname, hist1='nJets0', hist2=None, NQCD=1520239.0, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nJets2', hist2=None, NQCD=143202.7 , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nJets3', hist2=None, NQCD=3321.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nJets4', hist2=None, NQCD=384.1    , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='nJets6', hist2=None, NQCD=91.3     , rebin=1, newYlabel=''),
        
        #Plot( outname=outname, hist1='pfIso0', hist2=None, NQCD=1520239.0, rebin=5),
        #Plot( outname=outname, hist1='pfIso2', hist2=None, NQCD=143202.7 , rebin=5),
        #Plot( outname=outname, hist1='pfIso3', hist2=None, NQCD=3321.1   , rebin=5),
        
        Plot( outname=outname, hist1='pt1LepJet2', hist2=None, NQCD=143202.7, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='pt1LepJet3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='pt1LepJet4', hist2=None, NQCD=384.1   , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='pt1LepJet6', hist2=None, NQCD=91.3    , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='pt1LepJet7', hist2=None, NQCD=2       , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='pt2LepJet2', hist2=None, NQCD=143202.7*0.12, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='pt2LepJet3', hist2=None, NQCD=3321.1*0.30  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='pt2LepJet4', hist2=None, NQCD=384.1*0.48   , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='pt2LepJet6', hist2=None, NQCD=91.3*0.52    , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='pt2LepJet7', hist2=None, NQCD=2*0.62       , rebin=4, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='ptLep0', hist2=None, NQCD=1520239.0, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptLep2', hist2=None, NQCD=143202.7 , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptLep3', hist2=None, NQCD=3321.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptLep4', hist2=None, NQCD=384.1    , rebin=2, newYlabel='Events\ /\ 10\ GeV'),
        Plot( outname=outname, hist1='ptLep6', hist2=None, NQCD=91.3     , rebin=2, newYlabel='Events\ /\ 10\ GeV'),

        Plot( outname=outname, hist1='ptMET0', hist2=None, NQCD=1520239.0, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptMET2', hist2=None, NQCD=143202.7 , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptMET3', hist2=None, NQCD=3321.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptMET4', hist2=None, NQCD=384.1    , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='ptMET6', hist2=None, NQCD=91.3     , rebin=1, newYlabel=''),

        Plot( outname=outname, hist1='vtxMass3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='vtxMass4', hist2=None, NQCD=384.1   , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='vtxMass6', hist2=None, NQCD=91.3    , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='vtxMass7', hist2=None, NQCD=2       , rebin=2, newYlabel='Events\ /\ 0.2\ GeV'),

        Plot( outname=outname, hist1='etaAbsLep0', hist2=None, NQCD=1520239.0, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='etaAbsLep2', hist2=None, NQCD=143202.7 , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='etaAbsLep3', hist2=None, NQCD=3321.1   , rebin=2, newYlabel='Events'),
        Plot( outname=outname, hist1='etaAbsLep4', hist2=None, NQCD=384.1    , rebin=5, newYlabel='Events'),
        Plot( outname=outname, hist1='etaAbsLep6', hist2=None, NQCD=91.3     , rebin=5, newYlabel='Events'),
        Plot( outname=outname, hist1='etaAbsLep7', hist2=None, NQCD=2        , rebin=10, newYlabel='Events'),


        Plot( outname=outname, hist1='etaAbsLep4', hist2='etaAbsLep6', NQCD=384.1-91.3   , rebin=5, newYlabel='Events'),
        Plot( outname=outname, hist1='etaAbsLep6', hist2='etaAbsLep7', NQCD=91.3-2.0     , rebin=5, newYlabel='Events'),

        
        #Plot( outname=outname, hist1='vtxMass1LepJet2', hist2=None, NQCD=143202.7, rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass1LepJet3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass1LepJet4', hist2=None, NQCD=384.1   , rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass1LepJet6', hist2=None, NQCD=91.3    , rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass1LepJet7', hist2=None, NQCD=2       , rebin=1, newYlabel=''),
        
        #Plot( outname=outname, hist1='vtxMass2LepJet2', hist2=None, NQCD=143202.7*0.12, rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass2LepJet3', hist2=None, NQCD=3321.1*0.30  , rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass2LepJet4', hist2=None, NQCD=384.1*0.48   , rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass2LepJet6', hist2=None, NQCD=91.3*0.52    , rebin=1, newYlabel=''),
        #Plot( outname=outname, hist1='vtxMass2LepJet7', hist2=None, NQCD=2*0.62       , rebin=1, newYlabel=''),
        
        Plot( outname=outname, hist1='wboson_mt2', hist2=None, NQCD=143202.7, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='wboson_mt3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='wboson_mt4', hist2=None, NQCD=384.1   , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='wboson_mt6', hist2=None, NQCD=91.3    , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='wboson_mt7', hist2=None, NQCD=2       , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        
        Plot( outname=outname, hist1='wboson_pt2', hist2=None, NQCD=143202.7, rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='wboson_pt3', hist2=None, NQCD=3321.1  , rebin=1, newYlabel=''),
        Plot( outname=outname, hist1='wboson_pt4', hist2=None, NQCD=384.1   , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='wboson_pt6', hist2=None, NQCD=91.3    , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        Plot( outname=outname, hist1='wboson_pt7', hist2=None, NQCD=2       , rebin=2, newYlabel='Events\ /\ 20\ GeV'),
        
        ]

    for plot in plots :
        plot.draw()


if __name__ == "__main__":
    main()
