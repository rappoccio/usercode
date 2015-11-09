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
    
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_odd',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=1 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_odd',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=1 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_odd',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=1 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_even',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=2 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_even',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=2 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom_even',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=2 --lepType=ele',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),

    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_odd',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=1',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_odd',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=1',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_odd',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=1',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_even',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=2',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_even',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=2',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_nom_even',
           flags='--makeResponse  --semilep=1.0 --pdfSys=0.0 --pdfSet=0.0 --oddeven=2',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, postfit=options.postfit
    ),

    ]


run_threads( samples )
# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
