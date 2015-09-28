#!/usr/bin/env python

from run_iheartny_unfold import run_threads, Sample

import shlex



samples = [
    
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_mu',
           title='TT_mcatnlo_iheartNY_V1_mu',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_el',
           title='TT_mcatnlo_iheartNY_V1_el',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_mu',
           title='TT_nonSemiLep_mcatnlo_iheartNY_V1_mu',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_mcatnlo_el',
           title='TT_nonSemiLep_mcatnlo_iheartNY_V1_el',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    
]

run_threads( samples )
# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
