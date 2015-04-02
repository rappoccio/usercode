#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
        
    #------------------------------    
    # Q2 Scale up and down samples
    #------------------------------
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --lepType=ele',
           pu='ttbarQ2dn', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --lepType=ele',
           pu='ttbarQ2up', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),            
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--makeResponse --semilep=1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--mttGenMax=700. --semilep=-1.0 --lepType=ele',
           pu='ttbarQ2dn', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_Feb15/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--mttGenMax=700. --semilep=-1.0 --lepType=ele',
           pu='ttbarQ2up', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaledown',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),            
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola_iheartNY_el',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_scaleup',
           flags='--semilep=-1.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    )
    ]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
