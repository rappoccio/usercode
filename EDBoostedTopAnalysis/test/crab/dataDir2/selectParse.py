#! /usr/bin/env python

import re
import sys
import os.path
import commands
import array

p = re.compile(r'\s\s+')

datasets = []
infile = open( sys.argv[1], 'r' )

for line in infile :
  datasets.append( line.rstrip() )

tokens = [ 'Type 2 + Type 2 selection:', 'Type 2 + Type 3 selection:', 'Type 3 + Type 3 selection:' ]
selectSteps = [ 18, 13, 11 ]
nMax = 1

for dataset in datasets :
  names = dataset.split('/')
  toks = names[2].split('-')
  files = commands.getoutput( 'ls ' + names[1] + "_" + toks[1] + '/res/*.stdout' ).split('\n')
  #print files
  print '-------------------' + names[1] + '--------------------------'
  for s in range(0,len(tokens) ) :
    selectCounts = []
    stepNames    = []
    for n in range(0,nMax) :
      selectCounts.append([])
      stepNames.append([])
    firstFile = True
    for i in files :
        infile = open(i, 'r')
        n = -1
        for line in infile :
            if ( line.find(tokens[s]) >= 0 ) :
              n+=1
              if firstFile  :
                for step in range(0,selectSteps[s])  :
                  selectline = infile.next()
                  selectline = selectline.rstrip('\n')
                  stepNames[n].append( p.split(selectline)[2] )
                  if step==1 :
                    selectCounts[n].append(0)
                  else :
                    selectCounts[n].append( int(p.split(selectline)[3] ) )
              else :
                for step in range(0,selectSteps[s]) : 
                  selectline = infile.next()
                  selectline = selectline.rstrip('\n')
                  if step==1 :
                    selectCounts[n][step] += 0
                  else :
                    selectCounts[n][step] += (int(p.split(selectline)[3]))
        firstFile = False

    print '%20s' % tokens[s]
    for n in range(0, nMax)  :
      print "\tCut %5d" % n
      for step in range(0,selectSteps[s])  :
        print "%10d" % step, " : %30s" % stepNames[n][step], "%10d" % selectCounts[n][step]


