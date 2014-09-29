from ROOT import *

f = TFile.Open("allJet_data.root")

idir = "wPlusBJetAna/"
output = TFile("mistag.root", "recreate")

btag = f.Get( idir + "bTag_M")
wtag = f.Get( idir + "wTag")

bJetTotal = f.Get( idir + "jetTotal")
wJetTotal = f.Get( idir + "jetPt" )

tag1 = btag.Clone("bMistag") 
tag2 = wtag.Clone("wMistag")
bTotal = bJetTotal.Clone()
wTotal = wJetTotal.Clone()


#tag1.Sumw2()
tag1.Divide( bTotal )

#tag2.Sumw2()
tag2.Divide( wTotal )

output.Write()
output.Close()
f.Close()
