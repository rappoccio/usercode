#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileData', metavar='F', type='string', action='store',
                  default='Jet_plots_nominal.root',
                  dest='inputFileData',
                  help='Input file for data')

parser.add_option('--inputFileMC', metavar='F', type='string', action='append',
                  default=[ 'QCD_pythia6_z2_plots_nominal',
                            'QCD_pythia8_4c_plots_nominal',
                            'QCD_herwigpp_23_plots_nominal'
                            ],
                  dest='inputFileMC',
                  help='Input file for MC')




parser.add_option('--grooms', metavar='F', type='string', action='append',
                  default=[ '', 'Filtered', 'Trimmed', 'Pruned'
                            ],
                  dest='grooms',
                  help='Grooms to run')




(options, args) = parser.parse_args()

argv = []

from ROOT import *

gROOT.Macro("rootlogon.C")
gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
gStyle.SetTitleFontSize(0.04)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")

ptBins =  [0., 50., 125., 150., 220., 300., 450., 500., 600., 800., 1000., 1500., 7000.]


with open('texTemplateResponse.tex', 'r') as ftex :
    texStr = ftex.read()
ftex.closed

ftexout = open('responseFigures.tex', 'a')

ifile = TFile('response_full.root')
hists2D = []

canv = TCanvas('c', 'c', 500, 500)
canv.SetLogz()
canv.SetLeftMargin(0.2)
canv.SetBottomMargin(0.2)
canv.Print('response_full.pdf[')

for inputFileStr in options.inputFileMC :
    if inputFileStr.find('pythia6') >= 0 :
        generator = '\PYTHIA'
    elif inputFileStr.find('pythia8') >= 0 :
        generator = '\PYTHIAEIGHT'
    elif inputFileStr.find('herwig') >= 0 :
        generator = '\HERWIG'
    
    for igroom in options.grooms :
        if igroom != '' :
            jgroom = '_' + igroom
            kgroom = igroom + '_'
        else :
            jgroom = ''
            kgroom = ''



        texStrOut = texStr.replace( 'SAMPLE', inputFileStr )
        texStrOut = texStrOut.replace( 'GROOMSTRING', ' ' + igroom )
        texStrOut = texStrOut.replace( 'GROOMAPPEND', kgroom )
        texStrOut = texStrOut.replace( 'GENERATOR', generator )
        ftexout.write(texStrOut + '\n\n')

        for ipt in range(0,len(ptBins)-1) :




            responseStr = 'response_' + inputFileStr + jgroom + '_pt' + str(ipt)
            responseTitle = inputFileStr + ', ' + igroom + ' ' + str(ptBins[ipt]) + ' < p_{T}^{AVG} < ' + str(ptBins[ipt+1])
            print 'getting ' + responseStr
            response = ifile.Get(responseStr)
            hist2d = response.Hresponse()
            hists2D.append( hist2d )
            hist2d.SetTitle( responseTitle + ';m_{jet}^{GEN} (GeV);m_{jet}^{RECO} (GeV)')
            hist2d.Draw('colz')
            canv.Print('response_full.pdf')
            canv.Print( responseStr + '.pdf', 'pdf')
            canv.Print( responseStr + '.png', 'png')



canv.Print('response_full.pdf]')
