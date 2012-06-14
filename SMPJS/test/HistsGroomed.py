import ROOT

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle

#############################
# Histogramming utility to  #
# book each hist for each   #
# jet grooming technique    #
#############################
class HistsGroomed :
    def __init__(self, outname, grooms) :
        self.f = ROOT.TFile(outname + '.root', 'recreate')
        self.grooms = grooms
        self.hists = []

    def get(self, name) :
        return self.f.FindObject(name)

    def write(self) :
        self.f.cd()
        self.f.Write()
        self.f.Close()

    def getFile(self) :
        return self.f

    def makeQuickHists(self) :
        for hist in self.hists :
            setattr(self,hist[0].GetName(), hist[0])
            setattr(self,hist[0].GetName() + '_Groom', [])
            for igroom in range(0,len(hist[1])):
                getattr(self,hist[0].GetName() + '_Groom').append( hist[1][igroom] )

    def book1F(self, *args, **kwargs) :
        name=args[0]
        title=args[1]
        nx=kwargs.get('nx')
        x1=kwargs.get('x1',None)
        x2=kwargs.get('x2',None)
        xbins=kwargs.get('xbins',None)
        bookGrooms=kwargs.get('bookGrooms', True)
        self.f.cd()
        ihists = []
        h1 = None
        if xbins is None :
            h1 = ROOT.TH1F(name,title,nx,x1,x2)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH1F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2)
                    ihists.append(hi)
        else :
            h1 = ROOT.TH1F(name,title,nx,xbins)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH1F(name + '_' + igroom,title + ', ' + igroom,nx,xbins)
                    ihists.append(hi)
        self.hists.append([h1, ihists])


    def book2F(self, *args, **kwargs) :
        name=args[0]
        title=args[1]
        nx=kwargs.get('nx')
        x1=kwargs.get('x1',None)
        x2=kwargs.get('x2',None)
        xbins=kwargs.get('xbins',None)
        ny=kwargs.get('ny')
        y1=kwargs.get('y1',None)
        y2=kwargs.get('y2',None)
        ybins=kwargs.get('ybins',None)
        bookGrooms=kwargs.get('bookGrooms', True)
        self.f.cd()
        ihists = []
        h1 = None
        if x1 is not None and y1 is not None :
            h1 = ROOT.TH2F(name,title,nx,x1,x2,ny,y1,y2)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2,ny,y1,y2)
                    ihists.append(hi)
        elif x1 is not None and y1 is None :
            h1 = ROOT.TH2F(name,title,nx,x1,x2,ny,ybins)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2,ny,ybins)
                    ihists.append(hi)
        elif x1 is None and y1 is not None :
            h1 = ROOT.TH2F(name,title,nx,xbins,ny,y1,y2)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,xbins,ny,y1,y2)
                    ihists.append(hi)
        else :
            h1 = ROOT.TH2F(name,title,nx,xbins,ny,ybins)
            if bookGrooms :
                for igroom in self.grooms :
                    hi = ROOT.TH2F(name + '_' + igroom,title + ', ' + igroom,nx,xbins,ny,ybins)
                    ihists.append(hi)
        self.hists.append([h1, ihists])

    def book3F(self, *args, **kwargs) :
        name=args[0]
        title=args[1]
        nx=kwargs.get('nx')
        x1=kwargs.get('x1')
        x2=kwargs.get('x2')
        ny=kwargs.get('ny')
        y1=kwargs.get('y1')
        y2=kwargs.get('y2')
        nz=kwargs.get('nz')
        z1=kwargs.get('z1')
        z2=kwargs.get('z2')
        bookGrooms=kwargs.get('bookGrooms', True)
        self.f.cd()
        ihists = []
        h1 = ROOT.TH3F(name,title,nx,x1,x2,ny,y1,y2,nz,z1,z2)
        if bookGrooms :
            for igroom in self.grooms :
                hi = ROOT.TH3F(name + '_' + igroom,title + ', ' + igroom,nx,x1,x2,ny,y1,y2,nz,z1,z2)
                ihists.append(hi)
        self.hists.append([h1, ihists])
