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
    
    #------------------------------    
    # Q2 up
    #------------------------------
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_Q2up_inclusive_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --lepType=ele',
           pu='ttbarQ2up', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
           ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_Q2up_700to1000_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
           ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_Q2up_1000toInf_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
           ),

    #------------------------------    
    # Q2 down
    #------------------------------
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_Q2dn_inclusive_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --lepType=ele',
           pu='ttbarQ2dn', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
           ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_Q2dn_700to1000_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
           ),
    Sample(directory='/store/user/skinnari/Unfold_24feb2015/TT_Q2dn_1000toInf_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, postfit=options.postfit
           ),

]


run_threads( samples )
# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
