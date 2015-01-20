#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
    
    #------------------------------    
    # PDF Up samples, CT10
    #------------------------------
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--makeResponse  --semilep=1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/sdittmer/CMSSW_5_3_22_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_CT10_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),


]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
