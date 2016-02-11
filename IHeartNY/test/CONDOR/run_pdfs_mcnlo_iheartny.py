#!/usr/bin/env python

from run_iheartny_unfold import run_threads, Sample

import shlex

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--postfit', metavar='F', type='string', action='store',
                  default=None,
                  dest='postfit',
                  help='Use posterior top-tagging SF? Options are \'comb\' (combined fit) or \'emu\' (separate e/mu fit result). Default is None (that means to use prior value).')
(options, args) = parser.parse_args()
argv = []


samples = [
    
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_mu',
           title='TT_mcatnlo_iheartNY_V1_mu',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
    ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_el',
           title='TT_mcatnlo_iheartNY_V1_el',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
    ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_mu',
           title='TT_nonSemiLep_mcatnlo_iheartNY_V1_mu',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
    ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_el',
           title='TT_nonSemiLep_mcatnlo_iheartNY_V1_el',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
    ),
    
]

samplesMini = [
    
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_mu',
           title='TT_mcatnlo_iheartNY_V1_mu',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_el',
           title='TT_mcatnlo_iheartNY_V1_el',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    
]


if options.postfit != None:
    run_threads( samplesMini )
else:
    run_threads( samples )

# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
