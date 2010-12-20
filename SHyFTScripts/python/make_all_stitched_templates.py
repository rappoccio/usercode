#!/bin/python

import subprocess


options = [
    ['pfShyftAna',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaJES095', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaJES105', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ['pfShyftAnaMETRES090', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaMETRES110', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],


    ['pfShyftAnaJER000', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaJER020', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],


    ['pfShyftAna',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_d0vsiso_metcut_normalized_qcd_templates.root', 'pfShyftAnaMC', None],    
#    ['pfShyftAnaNoMET',  'pfShyftAnaNoMET', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_d0vsiso_nometcut_normalized_qcd_templates.root',  'pfShyftAnaMC', None],

#    ['pfShyftAnaReweightedUnity', 'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ['pfShyftAnaReweightedBTag080',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedBTag090',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag090',      'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedBTag110',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedBTag120',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ['pfShyftAnaReweightedLFTag070',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag080',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag090',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedUnity',          'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ['pfShyftAnaReweightedLFTag110',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ['pfShyftAna',       'pfShyftAna', '35pb_fhmore_387v1data_387v1mc_pretag', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'pf_metvsiso_pretag_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --makePretagPlots'],

    ## ['jptShyftAna',      'jptShyftAna', '35pb_fhmore_387v1data_387v1mc_pretag', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'jpt_metvsiso_pretag_normalized_qcd_templates.root', 'pfShyftAnaMC', ' --makePretagPlots'],

    ## ['jptShyftAna',       'jptShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'jpt_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ## ['jptShyftAnaJES095', 'jptShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'jpt_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],
    ## ['jptShyftAnaJES105', 'jptShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'jpt_metvsiso_normalized_qcd_templates.root', 'pfShyftAnaMC', None],

    ## ['jptShyftAna',       'jptShyftAna', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'jpt_d0vsiso_metcut_normalized_qcd_templates.root', 'pfShyftAnaMC', None],    
    ## ['jptShyftAnaNoMET',  'jptShyftAnaNoMET', '35pb_fhmore_387v1data_387v1mc', 'Mu_Nov4ReReco_shyft_387_v1_shyftana_v1.root', 'jpt_d0vsiso_nometcut_normalized_qcd_templates.root',  'pfShyftAnaMC', None],

    ]

command = 'python combineBackgroundPlots.py --input=shyftana_387_v3 --mcDir={0:s} --dataDir={1:s} --outputLabel={2:s}  --useData --dataFile={3:s} --useDataQCD --dataQCDFile={4:s} --templateDir={5:s} {6:s}'

for option in options :
    if option[6] is None :
        s = command.format(
            option[0], option[1], option[2], option[3], option[4], option[5], ''
            )
    else :
        s = command.format(
            option[0], option[1], option[2], option[3], option[4], option[5], option[6]
            )
    print '--------------------------------------------------------------------------'    
    print '--------------------------------------------------------------------------'
    print s
    print '--------------------------------------------------------------------------'
    print '--------------------------------------------------------------------------'
    subprocess.call( [s, ""], shell=True )    
