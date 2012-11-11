import subprocess, os, ConfigParser


dummy_config_name = 'crab_dummy_anashyft_ele.cfg'

dummy_config = ConfigParser.RawConfigParser()
dummy_config.read(dummy_config_name)

pset = 'edmNtupleMaker.py'
working_dir = os.environ['HOME'] + '/nobackup/BPrimeEDM_8TeV/Nov9/'
dir_suffix = '_tlbsm_53x_v2'

# one pset for all jobs
dummy_config.set('CMSSW','pset',pset)

joblist = [
   # ==========  MC ==========
## Those marked with ## needs b-tag maps from Dinko.
    
##        {'datasetpath':'/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath':'/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath': '/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath': '/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath': '/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath': '/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

#    {'datasetpath': '/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
    
##   {'datasetpath': '/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },    

##   {'datasetpath': '/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
        
##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },
        
##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##   {'datasetpath': '/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },    
                      
    ]

for job in joblist:
    config = dummy_config

    # common input files
    config.set('USER', 'additional_input_files', 'Jec12_V2_L1FastJet_AK5PFchs.txt,Jec12_V2_L2Relative_AK5PFchs.txt,Jec12_V2_L3Absolute_AK5PFchs.txt,Jec12_V2_L2L3Residual_AK5PFchs.txt,Jec12_V2_Uncertainty_AK5PFchs.txt,PUMC_dist_flat10.root,PUData_finebin_dist.root')
 
    # for MC we don't need this
    config.remove_option('CMSSW','runselection')
    config.remove_option('CMSSW','lumi_mask')

    # plug for data
    if 'Data' in job['#sample_name']:
        config.remove_option('CMSSW','total_number_of_events')
        config.set('CMSSW','total_number_of_lumis','-1')

    # set the CMSSW parameters   
    for p in job:
        config.set('CMSSW', p, job[p])
 

    if 'Data' not in job['#sample_name']:
        dataset =  job['datasetpath'].split('/')[1]
        
        # set the b-tag maps for mass 750 for all the bprime samples
        if 'BprimeBprimeToTWTWinc' in dataset:
            mass = dataset.split('_')[1]    
            m = mass.split('-')[1]          
            if eval(m) >= 600 :
                dataset = dataset.replace(mass, 'M-750')
            else:
                dataset = dataset.replace(mass, 'M-450')
        elif 'BprimeBprimeToBZTWinc' in dataset:
            mass = dataset.split('_')[1]
            m = mass.split('-')[1]
            if eval(m) >= 600 :
                dataset = dataset.replace(mass, 'M-750')
            else:
                dataset = dataset.replace(mass, 'M-450')
        elif 'BprimeBprimeToBHBHinc' in dataset:
            mass = dataset.split('_')[1]
            m = mass.split('-')[1]
            if eval(m) >= 600 :
                dataset = dataset.replace(mass, 'M-600')
            else:
                dataset = dataset.replace(mass, 'M-450')        
            
        btagFile_ak5 = dataset + "_AK5PF_CSVM_bTaggingEfficiencyMap.root"
        btagFile_ca8 = dataset + "_CA8PrunedPF_CSVM_bTaggingEfficiencyMap.root"
        #print 'btagFile_ak5', btagFile_ak5
        #print 'btagFile_ca8', btagFile_ca8
        
        config.set('USER', 'additional_input_files', config.get('USER', 'additional_input_files')+','+btagFile_ak5+','+btagFile_ca8)
        
        c1 = 'cp ../data/'+btagFile_ak5+' .'
        c2 = 'cp ../data/'+btagFile_ca8+' .'
        subprocess.call( [c1], shell=True)
        subprocess.call( [c2], shell=True)
        config.set('CMSSW', 'pycfg_params', config.get('CMSSW', 'pycfg_params')+" btagMap="+dataset)  
        
        
    # specify the name in case of data and signal
    if 'Data' in job['#sample_name'] or 'Bprime' in job['#sample_name']:
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + '_' + job['#sample_name'] + dir_suffix
    else:    
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + dir_suffix
    config.set('USER','ui_working_dir',ui_working_dir)
    
    # write cfg file and run crab
    cfgname = 'crab_'+job['#sample_name']+'.cfg'
    with open(cfgname, 'wb') as configfile:
        config.write(configfile)
       
    s = 'crab -create -cfg ' + cfgname
    print s
    subprocess.call( [s], shell=True )

    s = 'crab -submit -c ' + ui_working_dir
    print s
    subprocess.call( [s], shell=True )

    
    r1 = 'rm '+btagFile_ak5
    r2 = 'rm '+btagFile_ca8
    subprocess.call( [r1], shell=True)
    subprocess.call( [r2], shell=True)


