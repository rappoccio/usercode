import subprocess

class Plot :
    def __init__( self, outname, hist1, hist2, NQCD, maxy, rebin ) :
        self.outname = outname
        self.hist1 = hist1
        self.hist2 = hist2
        self.NQCD = NQCD
        self.maxy = maxy
        self.rebin = rebin
    def draw(self) :
        if self.hist2 != None : 
            s = 'python makeBarePlots.py --outname=' + self.outname + \
                ' --hist1=' + self.hist1 + ' --hist2=' + self.hist2 + \
                ' --NQCD=' + str(self.NQCD) + ' --maxy=' + str(self.maxy) + ' --rebin=' + str(self.rebin) + ' --plotNom'
        else : 
            s = 'python makeBarePlots.py --outname=' + self.outname + \
                ' --hist1=' + self.hist1 + \
                ' --NQCD=' + str(self.NQCD) + ' --maxy=' + str(self.maxy) + ' --rebin=' + str(self.rebin) + ' --plotNom'
        print 'executing ' + s
        subprocess.call( [s], shell=True )



def main() :
    outname = 'mujets'
    plots = [
        #Plot( outname=outname, hist1='csv1LepJet2' , hist2=None, NQCD=0.0 , maxy=60000 , rebin=1),
        #Plot( outname=outname, hist1='csv1LepJet3' , hist2=None, NQCD=0.0 , maxy=8500 , rebin=1),
        #Plot( outname=outname, hist1='csv1LepJet4' , hist2=None, NQCD=0.0 , maxy=4000 , rebin=5),
        #Plot( outname=outname, hist1='csv1LepJet5' , hist2=None, NQCD=0.0 , maxy=4000 , rebin=5),
        #Plot( outname=outname, hist1='csv1LepJet6' , hist2=None, NQCD=0.0 , maxy=300 , rebin=5),
        #Plot( outname=outname, hist1='csv1LepJet7' , hist2=None, NQCD=0.0 , maxy=220 , rebin=5),
        
        #Plot( outname=outname, hist1='csv2LepJet2' , hist2=None, NQCD=0.0 , maxy=4500 , rebin=1),
        #Plot( outname=outname, hist1='csv2LepJet3' , hist2=None, NQCD=0.0 , maxy=1500 , rebin=1),
        #Plot( outname=outname, hist1='csv2LepJet4' , hist2=None, NQCD=0.0 , maxy=800 , rebin=5),
        #Plot( outname=outname, hist1='csv2LepJet5' , hist2=None, NQCD=0.0 , maxy=800 , rebin=5),
        #Plot( outname=outname, hist1='csv2LepJet6' , hist2=None, NQCD=0.0 , maxy=100 , rebin=5),
        #Plot( outname=outname, hist1='csv2LepJet7' , hist2=None, NQCD=0.0 , maxy=60 , rebin=5),
        
        #Plot( outname=outname, hist1='eta1LepJet2' , hist2=None, NQCD=0.0 , maxy=26000 , rebin=1),
        #Plot( outname=outname, hist1='eta1LepJet3' , hist2=None, NQCD=0.0 , maxy=3500 , rebin=1),
        #Plot( outname=outname, hist1='eta1LepJet4' , hist2=None, NQCD=0.0 , maxy=600 , rebin=1),
        #Plot( outname=outname, hist1='eta1LepJet5' , hist2=None, NQCD=0.0 , maxy=600 , rebin=1),
        #Plot( outname=outname, hist1='eta1LepJet6' , hist2=None, NQCD=0.0 , maxy=250 , rebin=5),
        #Plot( outname=outname, hist1='eta1LepJet7' , hist2=None, NQCD=0.0 , maxy=100 , rebin=5),
        
        #Plot( outname=outname, hist1='eta2LepJet2' , hist2=None, NQCD=0.0 , maxy=2400 , rebin=1),
        #Plot( outname=outname, hist1='eta2LepJet3' , hist2=None, NQCD=0.0 , maxy=800 , rebin=1),
        #Plot( outname=outname, hist1='eta2LepJet4' , hist2=None, NQCD=0.0 , maxy=600 , rebin=5),
        #Plot( outname=outname, hist1='eta2LepJet5' , hist2=None, NQCD=0.0 , maxy=600 , rebin=5),
        #Plot( outname=outname, hist1='eta2LepJet6' , hist2=None, NQCD=0.0 , maxy=80 , rebin=5),
        #Plot( outname=outname, hist1='eta2LepJet7' , hist2=None, NQCD=0.0 , maxy=40 , rebin=5),
        
        #Plot( outname=outname, hist1='etaLep0' , hist2=None, NQCD=0.0 , maxy=280000 , rebin=1),
        #Plot( outname=outname, hist1='etaLep1' , hist2=None, NQCD=0.0 , maxy=85000 , rebin=1),
        #Plot( outname=outname, hist1='etaLep2' , hist2=None, NQCD=0.0 , maxy=85000 , rebin=1),
        #Plot( outname=outname, hist1='etaLep3' , hist2=None, NQCD=0.0 , maxy=3500 , rebin=1),
        #Plot( outname=outname, hist1='etaLep4' , hist2=None, NQCD=0.0 , maxy=2000 , rebin=5),
        #Plot( outname=outname, hist1='etaLep5' , hist2=None, NQCD=0.0 , maxy=2000 , rebin=5),
        #Plot( outname=outname, hist1='etaLep6' , hist2=None, NQCD=0.0 , maxy=250 , rebin=5),
        
        #Plot( outname=outname, hist1='hadtop_mass3' , hist2=None, NQCD=0.0 , maxy=7000 , rebin=1),
        #Plot( outname=outname, hist1='hadtop_mass4' , hist2=None, NQCD=0.0 , maxy=2300 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_mass5' , hist2=None, NQCD=0.0 , maxy=2300 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_mass6' , hist2=None, NQCD=0.0 , maxy=400 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_mass7' , hist2=None, NQCD=0.0 , maxy=200 , rebin=5),
        
        #Plot( outname=outname, hist1='hadtop_precut_tau32' , hist2=None, NQCD=0.0 , maxy=250 , rebin=5),
        
        #Plot( outname=outname, hist1='hadtop_pt3' , hist2=None, NQCD=0.0 , maxy=5000 , rebin=1),
        #Plot( outname=outname, hist1='hadtop_pt4' , hist2=None, NQCD=0.0 , maxy=1800 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_pt5' , hist2=None, NQCD=0.0 , maxy=1800 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_pt6' , hist2=None, NQCD=0.0 , maxy=200 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_pt7' , hist2=None, NQCD=0.0 , maxy=80 , rebin=5),
        
        #Plot( outname=outname, hist1='hadtop_y3' , hist2=None, NQCD=0.0 , maxy=3500 , rebin=1),
        #Plot( outname=outname, hist1='hadtop_y4' , hist2=None, NQCD=0.0 , maxy=1600 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_y5' , hist2=None, NQCD=0.0 , maxy=1500 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_y6' , hist2=None, NQCD=0.0 , maxy=250 , rebin=5),
        #Plot( outname=outname, hist1='hadtop_y7' , hist2=None, NQCD=0.0 , maxy=30 , rebin=1),
        
        #Plot( outname=outname, hist1='ht1' , hist2=None, NQCD=0.0 , maxy=160000 , rebin=1),
        #Plot( outname=outname, hist1='ht2' , hist2=None, NQCD=0.0 , maxy=160000 , rebin=1),
        #Plot( outname=outname, hist1='ht3' , hist2=None, NQCD=0.0 , maxy=2800 , rebin=1),
        #Plot( outname=outname, hist1='ht4' , hist2=None, NQCD=0.0 , maxy=1000 , rebin=5),
        #Plot( outname=outname, hist1='ht5' , hist2=None, NQCD=0.0 , maxy=1000 , rebin=5),
        #Plot( outname=outname, hist1='ht6' , hist2=None, NQCD=0.0 , maxy=140 , rebin=5),
        #Plot( outname=outname, hist1='ht7' , hist2=None, NQCD=0.0 , maxy=60 , rebin=5),
        
        #Plot( outname=outname, hist1='htLep1' , hist2=None, NQCD=0.0 , maxy=160000 , rebin=1),
        #Plot( outname=outname, hist1='htLep2' , hist2=None, NQCD=0.0 , maxy=160000 , rebin=1),
        #Plot( outname=outname, hist1='htLep3' , hist2=None, NQCD=0.0 , maxy=2500 , rebin=1),
        #Plot( outname=outname, hist1='htLep4' , hist2=None, NQCD=0.0 , maxy=1200 , rebin=5),
        #Plot( outname=outname, hist1='htLep5' , hist2=None, NQCD=0.0 , maxy=1000 , rebin=5),
        #Plot( outname=outname, hist1='htLep6' , hist2=None, NQCD=0.0 , maxy=120 , rebin=5),
        #Plot( outname=outname, hist1='htLep7' , hist2=None, NQCD=0.0 , maxy=50 , rebin=5),
        
        #Plot( outname=outname, hist1='lepMET1' , hist2=None, NQCD=0.0 , maxy=65000 , rebin=1),
        #Plot( outname=outname, hist1='lepMET2' , hist2=None, NQCD=0.0 , maxy=65000 , rebin=1),
        #Plot( outname=outname, hist1='lepMET3' , hist2=None, NQCD=0.0 , maxy=1200 , rebin=1),
        #Plot( outname=outname, hist1='lepMET4' , hist2=None, NQCD=0.0 , maxy=400 , rebin=5),
        #Plot( outname=outname, hist1='lepMET5' , hist2=None, NQCD=0.0 , maxy=400 , rebin=5),
        #Plot( outname=outname, hist1='lepMET6' , hist2=None, NQCD=0.0 , maxy=80 , rebin=10),
        #Plot( outname=outname, hist1='lepMET7' , hist2=None, NQCD=0.0 , maxy=40 , rebin=10),
        
        #Plot( outname=outname, hist1='leptop_mass3' , hist2=None, NQCD=0.0 , maxy=2800 , rebin=1),
        #Plot( outname=outname, hist1='leptop_mass4' , hist2=None, NQCD=0.0 , maxy=1300 , rebin=5),
        #Plot( outname=outname, hist1='leptop_mass5' , hist2=None, NQCD=0.0 , maxy=1100 , rebin=5),
        #Plot( outname=outname, hist1='leptop_mass6' , hist2=None, NQCD=0.0 , maxy=160 , rebin=5),
        #Plot( outname=outname, hist1='leptop_mass7' , hist2=None, NQCD=0.0 , maxy=70 , rebin=5),
        
        #Plot( outname=outname, hist1='leptop_pt3' , hist2=None, NQCD=0.0 , maxy=3000 , rebin=1),
        #Plot( outname=outname, hist1='leptop_pt4' , hist2=None, NQCD=0.0 , maxy=1200 , rebin=5),
        #Plot( outname=outname, hist1='leptop_pt5' , hist2=None, NQCD=0.0 , maxy=1100 , rebin=5),
        #Plot( outname=outname, hist1='leptop_pt6' , hist2=None, NQCD=0.0 , maxy=300 , rebin=10),
        #Plot( outname=outname, hist1='leptop_pt7' , hist2=None, NQCD=0.0 , maxy=90 , rebin=10),
        
        #Plot( outname=outname, hist1='leptop_y3' , hist2=None, NQCD=0.0 , maxy=4700 , rebin=1),
        #Plot( outname=outname, hist1='leptop_y4' , hist2=None, NQCD=0.0 , maxy=700 , rebin=1),
        #Plot( outname=outname, hist1='leptop_y5' , hist2=None, NQCD=0.0 , maxy=700 , rebin=1),
        #Plot( outname=outname, hist1='leptop_y6' , hist2=None, NQCD=0.0 , maxy=300 , rebin=5),
        #Plot( outname=outname, hist1='leptop_y7' , hist2=None, NQCD=0.0 , maxy=35 , rebin=1),
        
        Plot( outname=outname, hist1='nBJets0' , hist2=None, NQCD=1520239.0 , maxy=8000000 , rebin=1),
        Plot( outname=outname, hist1='nBJets1' , hist2=None, NQCD=143202.7  , maxy=2000000 , rebin=1),
        Plot( outname=outname, hist1='nBJets2' , hist2=None, NQCD=143202.7  , maxy=2000000 , rebin=1),
        Plot( outname=outname, hist1='nBJets3' , hist2=None, NQCD=3321.1    , maxy=56000 , rebin=1),
        Plot( outname=outname, hist1='nBJets4' , hist2=None, NQCD=384.1     , maxy=5000 , rebin=1),
        Plot( outname=outname, hist1='nBJets5' , hist2=None, NQCD=384.1     , maxy=5500 , rebin=1),
        Plot( outname=outname, hist1='nBJets6' , hist2=None, NQCD=91.3      , maxy=350 , rebin=5),
        
        Plot( outname=outname, hist1='nJets0' , hist2=None, NQCD=1520239.0  , maxy=7000000 , rebin=1),
        Plot( outname=outname, hist1='nJets1' , hist2=None, NQCD=143202.7   , maxy=1800000 , rebin=1),
        Plot( outname=outname, hist1='nJets2' , hist2=None, NQCD=143202.7   , maxy=1800000 , rebin=1),
        Plot( outname=outname, hist1='nJets3' , hist2=None, NQCD=3321.1     , maxy=30000 , rebin=1),
        Plot( outname=outname, hist1='nJets4' , hist2=None, NQCD=384.1      , maxy=4000 , rebin=1),
        Plot( outname=outname, hist1='nJets5' , hist2=None, NQCD=384.1      , maxy=2600 , rebin=1),
        Plot( outname=outname, hist1='nJets6' , hist2=None, NQCD=91.3       , maxy=400 , rebin=5),
        
        Plot( outname=outname, hist1='pfIso0' , hist2=None, NQCD=1520239.0 , maxy=7500000 , rebin=1),
        Plot( outname=outname, hist1='pfIso1' , hist2=None, NQCD=143202.7  , maxy=2000000 , rebin=1),
        Plot( outname=outname, hist1='pfIso2' , hist2=None, NQCD=143202.7  , maxy=2000000 , rebin=1),
        Plot( outname=outname, hist1='pfIso3' , hist2=None, NQCD=03321.1   , maxy=85000 , rebin=1),
        
        Plot( outname=outname, hist1='pt1LepJet2' , hist2=None, NQCD=143202.7  , maxy=125000 , rebin=1),
        Plot( outname=outname, hist1='pt1LepJet3' , hist2=None, NQCD=3321.1    , maxy=4300 , rebin=1),
        Plot( outname=outname, hist1='pt1LepJet4' , hist2=None, NQCD=384.1     , maxy=1000 , rebin=5),
        Plot( outname=outname, hist1='pt1LepJet5' , hist2=None, NQCD=384.1     , maxy=1000 , rebin=5),
        Plot( outname=outname, hist1='pt1LepJet6' , hist2=None, NQCD=91.3      , maxy=150 , rebin=5),
        Plot( outname=outname, hist1='pt1LepJet7' , hist2=None, NQCD=2.0       , maxy=60 , rebin=5),
        
        Plot( outname=outname, hist1='pt2LepJet2' , hist2=None, NQCD=143202.7   , maxy=17000 , rebin=1),
        Plot( outname=outname, hist1='pt2LepJet3' , hist2=None, NQCD=3321.1     , maxy=2600 , rebin=1),
        Plot( outname=outname, hist1='pt2LepJet4' , hist2=None, NQCD=384.1      , maxy=1000 , rebin=5),
        Plot( outname=outname, hist1='pt2LepJet5' , hist2=None, NQCD=384.1      , maxy=1000 , rebin=5),
        Plot( outname=outname, hist1='pt2LepJet6' , hist2=None, NQCD=91.3       , maxy=150 , rebin=5),
        Plot( outname=outname, hist1='pt2LepJet7' , hist2=None, NQCD=2.0        , maxy=60 , rebin=5),
        
        Plot( outname=outname, hist1='ptLep0' , hist2=None, NQCD=1520239.0  , maxy=2000000 , rebin=1),
        Plot( outname=outname, hist1='ptLep1' , hist2=None, NQCD=143202.7   , maxy=450000 , rebin=1),
        Plot( outname=outname, hist1='ptLep2' , hist2=None, NQCD=143202.7   , maxy=450000 , rebin=1),
        Plot( outname=outname, hist1='ptLep3' , hist2=None, NQCD=3321.1     , maxy=6000 , rebin=1),
        Plot( outname=outname, hist1='ptLep4' , hist2=None, NQCD=384.1      , maxy=600 , rebin=1),
        Plot( outname=outname, hist1='ptLep5' , hist2=None, NQCD=384.1      , maxy=600 , rebin=1),
        Plot( outname=outname, hist1='ptLep6' , hist2=None, NQCD=91.3       , maxy=170 , rebin=5),
        
        Plot( outname=outname, hist1='vtxMass1LepJet2' , hist2=None, NQCD=143202.7   , maxy=600000 , rebin=5),
        Plot( outname=outname, hist1='vtxMass1LepJet3' , hist2=None, NQCD=3321.1     , maxy=70000 , rebin=5),
        Plot( outname=outname, hist1='vtxMass1LepJet4' , hist2=None, NQCD=384.1      , maxy=6500 , rebin=5),
        Plot( outname=outname, hist1='vtxMass1LepJet5' , hist2=None, NQCD=384.1      , maxy=6500 , rebin=5),
        Plot( outname=outname, hist1='vtxMass1LepJet6' , hist2=None, NQCD=91.3       , maxy=600 , rebin=5),
        Plot( outname=outname, hist1='vtxMass1LepJet7' , hist2=None, NQCD=2.0        , maxy=80 , rebin=5),
        
        Plot( outname=outname, hist1='vtxMass2LepJet2' , hist2=None, NQCD=143202.7   , maxy=50000 , rebin=5),
        Plot( outname=outname, hist1='vtxMass2LepJet3' , hist2=None, NQCD=3321.1     , maxy=11000 , rebin=5),
        Plot( outname=outname, hist1='vtxMass2LepJet4' , hist2=None, NQCD=384.1      , maxy=1700 , rebin=5),
        Plot( outname=outname, hist1='vtxMass2LepJet5' , hist2=None, NQCD=384.1      , maxy=1700 , rebin=5),
        Plot( outname=outname, hist1='vtxMass2LepJet6' , hist2=None, NQCD=91.3       , maxy=200 , rebin=5),
        Plot( outname=outname, hist1='vtxMass2LepJet7' , hist2=None, NQCD=2.0        , maxy=80 , rebin=5),
        
        Plot( outname=outname, hist1='wboson_mt1' , hist2=None, NQCD=143202.7   , maxy=260000 , rebin=1),
        Plot( outname=outname, hist1='wboson_mt2' , hist2=None, NQCD=143202.7   , maxy=260000 , rebin=1),
        Plot( outname=outname, hist1='wboson_mt3' , hist2=None, NQCD=3321.1     , maxy=4400 , rebin=1),
        Plot( outname=outname, hist1='wboson_mt4' , hist2=None, NQCD=384.1      , maxy=1500 , rebin=5),
        Plot( outname=outname, hist1='wboson_mt5' , hist2=None, NQCD=384.1      , maxy=1500 , rebin=5),
        Plot( outname=outname, hist1='wboson_mt6' , hist2=None, NQCD=91.3       , maxy=200 , rebin=5),
        Plot( outname=outname, hist1='wboson_mt7' , hist2=None, NQCD=2.0        , maxy=25 , rebin=1),
        
        Plot( outname=outname, hist1='wboson_pt1' , hist2=None, NQCD=143202.7   , maxy=260000 , rebin=1),
        Plot( outname=outname, hist1='wboson_pt2' , hist2=None, NQCD=143202.7   , maxy=260000 , rebin=1),
        Plot( outname=outname, hist1='wboson_pt3' , hist2=None, NQCD=3321.1     , maxy=4500 , rebin=1),
        Plot( outname=outname, hist1='wboson_pt4' , hist2=None, NQCD=384.1      , maxy=1600 , rebin=5),
        Plot( outname=outname, hist1='wboson_pt5' , hist2=None, NQCD=384.1      , maxy=1600 , rebin=5),
        Plot( outname=outname, hist1='wboson_pt6' , hist2=None, NQCD=91.3       , maxy=200 , rebin=5),
        Plot( outname=outname, hist1='wboson_pt7' , hist2=None, NQCD=2.0        , maxy=25 , rebin=1),
        
        ]

    for plot in plots :
        plot.draw()


if __name__ == "__main__":
    main()
