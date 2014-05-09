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
                ' --NQCD=' + str(self.NQCD) + ' --maxy=' + str(self.maxy) + ' --rebin=' + str(self.rebin)
        else : 
            s = 'python makeBarePlots.py --outname=' + self.outname + \
                ' --hist1=' + self.hist1 + \
                ' --NQCD=' + str(self.NQCD) + ' --maxy=' + str(self.maxy) + ' --rebin=' + str(self.rebin)
        print 'executing ' + s
        subprocess.call( [s], shell=True )



def main() :
    outname = 'mujets'
    plots = [
        Plot( outname=outname, hist1='etaLep4', hist2=None, NQCD=0.0, maxy=3000, rebin=5),
        Plot( outname=outname, hist1='etaLep4', hist2='etaLep6', NQCD=0.0, maxy=3000, rebin=5),
        Plot( outname=outname, hist1='etaLep6', hist2=None, NQCD=0.0, maxy=300, rebin=5),
        Plot( outname=outname, hist1='vtxMass7', hist2=None, NQCD=0.0, maxy=30, rebin=1),
        ]

    for plot in plots :
        plot.draw()


if __name__ == "__main__":
    main()
