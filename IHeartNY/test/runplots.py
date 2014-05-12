import subprocess

class Plot :
    def __init__( self, outname, hist1, maxy ) :
        self.outname = outname
        self.hist1 = hist1
        self.maxy = maxy
    def draw(self) :
        s = 'python makeBarePlots.py --outname=' + self.outname + \
            ' --hist1=' + self.hist1 + \
            ' --maxy=' + str(self.maxy) + ' --plotNom' 
        print 'executing ' + s
        subprocess.call( [s], shell=True )



def main() :
    outname = 'mujets'
    plots = [
        Plot( outname=outname, hist1='ht1' , maxy=160000),
        Plot( outname=outname, hist1='ht2' , maxy=160000),
        Plot( outname=outname, hist1='ht3' , maxy=2800),
        Plot( outname=outname, hist1='ht4' , maxy=400),
        Plot( outname=outname, hist1='ht5' , maxy=300),
        Plot( outname=outname, hist1='ht6' , maxy=35),
        Plot( outname=outname, hist1='ht7' , maxy=15),
        
        Plot( outname=outname, hist1='htLep1' , maxy=160000),
        Plot( outname=outname, hist1='htLep2' , maxy=160000),
        Plot( outname=outname, hist1='htLep3' , maxy=2500),
        Plot( outname=outname, hist1='htLep4' , maxy=300),
        Plot( outname=outname, hist1='htLep5' , maxy=250),
        Plot( outname=outname, hist1='htLep6' , maxy=35),
        Plot( outname=outname, hist1='htLep7' , maxy=17),
        
        Plot( outname=outname, hist1='lepMET1' , maxy=65000),
        Plot( outname=outname, hist1='lepMET2' , maxy=65000),
        Plot( outname=outname, hist1='lepMET3' , maxy=1200),
        Plot( outname=outname, hist1='lepMET4' , maxy=150),
        Plot( outname=outname, hist1='lepMET5' , maxy=150),
        Plot( outname=outname, hist1='lepMET6' , maxy=40),
        Plot( outname=outname, hist1='lepMET7' , maxy=9),
        
        Plot( outname=outname, hist1='pfIso0' , maxy=7500000),
        Plot( outname=outname, hist1='pfIso1' , maxy=2000000),
        Plot( outname=outname, hist1='pfIso2' , maxy=2000000),
        Plot( outname=outname, hist1='pfIso3' , maxy=85000),
        
        Plot( outname=outname, hist1='ptLep0' , maxy=2000000),
        Plot( outname=outname, hist1='ptLep1' , maxy=450000),
        Plot( outname=outname, hist1='ptLep2' , maxy=450000),
        Plot( outname=outname, hist1='ptLep3' , maxy=6000),
        Plot( outname=outname, hist1='ptLep4' , maxy=600),
        Plot( outname=outname, hist1='ptLep5' , maxy=600),
        Plot( outname=outname, hist1='ptLep6' , maxy=90),
        
        Plot( outname=outname, hist1='etaLep0' , maxy=280000),
        Plot( outname=outname, hist1='etaLep1' , maxy=85000),
        Plot( outname=outname, hist1='etaLep2' , maxy=85000),
        Plot( outname=outname, hist1='etaLep3' , maxy=3500),
        Plot( outname=outname, hist1='etaLep4' , maxy=600),
        Plot( outname=outname, hist1='etaLep5' , maxy=600),
        Plot( outname=outname, hist1='etaLep6' , maxy=80),
        
        Plot( outname=outname, hist1='nJets0' , maxy=7000000),
        Plot( outname=outname, hist1='nJets1' , maxy=1800000),
        Plot( outname=outname, hist1='nJets2' , maxy=1800000),
        Plot( outname=outname, hist1='nJets3' , maxy=30000),
        Plot( outname=outname, hist1='nJets4' , maxy=4000),
        Plot( outname=outname, hist1='nJets5' , maxy=2600),
        Plot( outname=outname, hist1='nJets6' , maxy=400),
        
        Plot( outname=outname, hist1='nBJets0' , maxy=8000000),
        Plot( outname=outname, hist1='nBJets1' , maxy=2000000),
        Plot( outname=outname, hist1='nBJets2' , maxy=2000000),
        Plot( outname=outname, hist1='nBJets3' , maxy=56000),
        Plot( outname=outname, hist1='nBJets4' , maxy=5000),
        Plot( outname=outname, hist1='nBJets5' , maxy=5500),
        Plot( outname=outname, hist1='nBJets6' , maxy=350),
        
        Plot( outname=outname, hist1='wboson_pt1' , maxy=260000),
        Plot( outname=outname, hist1='wboson_pt2' , maxy=260000),
        Plot( outname=outname, hist1='wboson_pt3' , maxy=4500),
        Plot( outname=outname, hist1='wboson_pt4' , maxy=500),
        Plot( outname=outname, hist1='wboson_pt5' , maxy=400),
        Plot( outname=outname, hist1='wboson_pt6' , maxy=40),
        Plot( outname=outname, hist1='wboson_pt7' , maxy=25),
        
        Plot( outname=outname, hist1='wboson_mt1' , maxy=260000),
        Plot( outname=outname, hist1='wboson_mt2' , maxy=260000),
        Plot( outname=outname, hist1='wboson_mt3' , maxy=4400),
        Plot( outname=outname, hist1='wboson_mt4' , maxy=500),
        Plot( outname=outname, hist1='wboson_mt5' , maxy=350),
        Plot( outname=outname, hist1='wboson_mt6' , maxy=40),
        Plot( outname=outname, hist1='wboson_mt7' , maxy=25),
        
        Plot( outname=outname, hist1='pt1LepJet2' , maxy=125000),
        Plot( outname=outname, hist1='pt1LepJet3' , maxy=4300),
        Plot( outname=outname, hist1='pt1LepJet4' , maxy=500),
        Plot( outname=outname, hist1='pt1LepJet5' , maxy=300),
        Plot( outname=outname, hist1='pt1LepJet6' , maxy=50),
        Plot( outname=outname, hist1='pt1LepJet7' , maxy=20),
        
        Plot( outname=outname, hist1='eta1LepJet2' , maxy=26000),
        Plot( outname=outname, hist1='eta1LepJet3' , maxy=3500),
        Plot( outname=outname, hist1='eta1LepJet4' , maxy=600),
        Plot( outname=outname, hist1='eta1LepJet5' , maxy=600),
        Plot( outname=outname, hist1='eta1LepJet6' , maxy=80),
        Plot( outname=outname, hist1='eta1LepJet7' , maxy=25),
        
        Plot( outname=outname, hist1='csv1LepJet2' , maxy=60000),
        Plot( outname=outname, hist1='csv1LepJet3' , maxy=8500),
        Plot( outname=outname, hist1='csv1LepJet4' , maxy=1300),
        Plot( outname=outname, hist1='csv1LepJet5' , maxy=1300),
        Plot( outname=outname, hist1='csv1LepJet6' , maxy=160),
        Plot( outname=outname, hist1='csv1LepJet7' , maxy=110),
        
        Plot( outname=outname, hist1='vtxMass1LepJet2' , maxy=63000),
        Plot( outname=outname, hist1='vtxMass1LepJet3' , maxy=63000),
        Plot( outname=outname, hist1='vtxMass1LepJet4' , maxy=6000),
        Plot( outname=outname, hist1='vtxMass1LepJet5' , maxy=6000),
        Plot( outname=outname, hist1='vtxMass1LepJet6' , maxy=500),
        Plot( outname=outname, hist1='vtxMass1LepJet7' , maxy=60),
        
        Plot( outname=outname, hist1='pt2LepJet2' , maxy=17000),
        Plot( outname=outname, hist1='pt2LepJet3' , maxy=2600),
        Plot( outname=outname, hist1='pt2LepJet4' , maxy=300),
        Plot( outname=outname, hist1='pt2LepJet5' , maxy=300),
        Plot( outname=outname, hist1='pt2LepJet6' , maxy=50),
        Plot( outname=outname, hist1='pt2LepJet7' , maxy=25),
        
        Plot( outname=outname, hist1='eta2LepJet2' , maxy=2400),
        Plot( outname=outname, hist1='eta2LepJet3' , maxy=800),
        Plot( outname=outname, hist1='eta2LepJet4' , maxy=160),
        Plot( outname=outname, hist1='eta2LepJet5' , maxy=160),
        Plot( outname=outname, hist1='eta2LepJet6' , maxy=20),
        Plot( outname=outname, hist1='eta2LepJet7' , maxy=14),
        
        Plot( outname=outname, hist1='csv2LepJet2' , maxy=4500),
        Plot( outname=outname, hist1='csv2LepJet3' , maxy=1500),
        Plot( outname=outname, hist1='csv2LepJet4' , maxy=250),
        Plot( outname=outname, hist1='csv2LepJet5' , maxy=250),
        Plot( outname=outname, hist1='csv2LepJet6' , maxy=25),
        Plot( outname=outname, hist1='csv2LepJet7' , maxy=25),
        
        Plot( outname=outname, hist1='vtxMass2LepJet2' , maxy=50000),
        Plot( outname=outname, hist1='vtxMass2LepJet3' , maxy=12000),
        Plot( outname=outname, hist1='vtxMass2LepJet4' , maxy=1600),
        Plot( outname=outname, hist1='vtxMass2LepJet5' , maxy=1600),
        Plot( outname=outname, hist1='vtxMass2LepJet6' , maxy=200),
        Plot( outname=outname, hist1='vtxMass2LepJet7' , maxy=80),
        
        Plot( outname=outname, hist1='leptop_pt3' , maxy=3000),
        Plot( outname=outname, hist1='leptop_pt4' , maxy=400),
        Plot( outname=outname, hist1='leptop_pt5' , maxy=400),
        Plot( outname=outname, hist1='leptop_pt6' , maxy=60),
        Plot( outname=outname, hist1='leptop_pt7' , maxy=20),
        
        Plot( outname=outname, hist1='leptop_y3' , maxy=4700),
        Plot( outname=outname, hist1='leptop_y4' , maxy=700),
        Plot( outname=outname, hist1='leptop_y5' , maxy=700),
        Plot( outname=outname, hist1='leptop_y6' , maxy=70),
        Plot( outname=outname, hist1='leptop_y7' , maxy=35),
        
        Plot( outname=outname, hist1='leptop_mass3' , maxy=2800),
        Plot( outname=outname, hist1='leptop_mass4' , maxy=300),
        Plot( outname=outname, hist1='leptop_mass5' , maxy=350),
        Plot( outname=outname, hist1='leptop_mass6' , maxy=45),
        Plot( outname=outname, hist1='leptop_mass7' , maxy=25),
        
        Plot( outname=outname, hist1='hadtop_pt3' , maxy=5000),
        Plot( outname=outname, hist1='hadtop_pt4' , maxy=700),
        Plot( outname=outname, hist1='hadtop_pt5' , maxy=550),
        Plot( outname=outname, hist1='hadtop_pt6' , maxy=60),
        Plot( outname=outname, hist1='hadtop_pt7' , maxy=30),
        
        Plot( outname=outname, hist1='hadtop_y3' , maxy=3500),
        Plot( outname=outname, hist1='hadtop_y4' , maxy=600),
        Plot( outname=outname, hist1='hadtop_y5' , maxy=500),
        Plot( outname=outname, hist1='hadtop_y6' , maxy=80),
        Plot( outname=outname, hist1='hadtop_y7' , maxy=30),
        
        Plot( outname=outname, hist1='hadtop_mass3' , maxy=7000),
        Plot( outname=outname, hist1='hadtop_mass4' , maxy=800),
        Plot( outname=outname, hist1='hadtop_mass5' , maxy=500),
        Plot( outname=outname, hist1='hadtop_mass6' , maxy=100),
        Plot( outname=outname, hist1='hadtop_mass7' , maxy=60),
        
        Plot( outname=outname, hist1='hadtop_precut_tau32' , maxy=100),
        
        
        
        
        
        ]

    for plot in plots :
        plot.draw()


if __name__ == "__main__":
    main()