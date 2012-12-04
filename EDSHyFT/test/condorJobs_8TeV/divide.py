#!/usr/bin/env python

from __future__ import print_function,division

import itertools
import sys
import math

def get_num_input_files(filename):
    return sum(1 for line in open(filename, 'r'))

path='Unsplit/'

textFiles = [
    #[path+'SingleEle-Run2012A-13Jul2012', 4],
    #[path+'SingleEle-Run2012B-13Jul2012', 16],
    #[path+'SingleEle-Run2012A-06Aug2012', 4],
    #[path+'SingleEle-Run2012C-24Aug2012', 4],
    [path+'TTJets_matchingdown', 10],
    [path+'TTJets_matchingup', 10],
    [path+'TTJets_scaleup', 5],
    [path+'TTJets_scaledown', 10],
    ]

for file in textFiles:
    input = file[0]
    max_jobs = file[1]
    
    num_input_files = get_num_input_files(input+'.txt')
    inputs_per_job = math.ceil(num_input_files / max_jobs)
    
    print('inputs_per_jobs', inputs_per_job)


    for job in range(0, max_jobs):
        lines = []
        for line in itertools.islice(open(input+'.txt', 'r'),
                                     job * inputs_per_job,
                                     (job + 1) * inputs_per_job):
            lines.append(line.strip())
            
        if lines:
            with open(input+'_v'+str(job)+'.txt', 'w') as output_:
                for line in lines:
                    print(line, file=output_)
