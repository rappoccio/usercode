#!/usr/bin/env python

from run_iheartny_unfold import run_threads, Sample

import shlex



samples = [
    
    #------------------------------    
    # Q2 up
    #------------------------------
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_Q2up_inclusive_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --lepType=ele',
           pu='ttbarQ2up', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_Q2up_700to1000_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_Q2up_1000toInf_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),

    #------------------------------    
    # Q2 down
    #------------------------------
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_Q2dn_inclusive_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --lepType=ele',
           pu='ttbarQ2dn', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_Q2dn_700to1000_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_Q2dn_1000toInf_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
           ),

]


run_threads( samples )
# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
