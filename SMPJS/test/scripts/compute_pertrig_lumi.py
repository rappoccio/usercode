#!/bin/python

import subprocess
from string import *


triggers = []

tot = 3.375e9

f = open('lumicomputation.txt', 'r')
instrings = f.readlines()
f.close()
trigslines = []
for instring in instrings :
    s = instring.rstrip()
    toks = s.split(',')
    sumval = 0
    for itok in range(1,len(toks)) :
        sumval += float( toks[itok] )
    trigslines.append( [toks[0], sumval]  )
    

for itrig in trigslines :
    effprescale = tot / itrig[1]
    print '{0:10s} : {1:6.2e}, {2:6.2f}'.format( itrig[0], itrig[1], effprescale)
