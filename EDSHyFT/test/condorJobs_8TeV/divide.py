#!/usr/bin/env python

from __future__ import print_function,division

import itertools
import sys
import math

input = 'SingleEle-Run2012B-13Jul2012'
max_jobs = int(sys.argv[1] if 1 < len(sys.argv) else 10)

def get_num_input_files(filename):
    return sum(1 for line in open(filename, 'r'))

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
