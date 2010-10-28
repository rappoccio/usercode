#!/bin/python

from ROOT import *
from array import *

def addSimple( lum, idir, templatedir, histname, k_tot, sample, verbose = False ) :
    prepend = sample[0]
    ifile = sample[1]
    xs = sample[2]
    nevt = sample[3]
    sampleIsData = sample[4]

    if templatedir is not None and sampleIsData is False :
        h = ifile.Get( templatedir + prepend + histname ).Clone()
        h2 = ifile.Get( idir + prepend + histname ).Clone()
    else :
        h = ifile.Get( idir + prepend + histname ).Clone()

    h.SetName( prepend + histname )
    h.SetTitle( prepend + histname )    
    if sampleIsData is False :
        h.Scale( k_tot * xs * lum * h2.Integral() / (nevt * h.Integral() ) )
    return h
