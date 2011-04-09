import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

import FWCore.PythonUtilities.LumiList as LumiList

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.parseArguments()

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# get JSON file correctly parced
JSONfile = 'Cert_161079-161352_7TeV_PromptReco_Collisions11_JSON_noESpbl_v2.txt'
myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


if options.useData :
    histFileName = 'jetStudiesJet2011A.root'
    
    ## Source
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(  
 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/SingleMu/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_17_1_ACA.root'                 
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_10_1_EJL.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_11_1_MFK.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_12_1_mEi.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_13_1_M5k.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_14_1_mrk.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_15_1_6iz.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_16_1_Okw.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_17_1_oMY.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_18_1_uRZ.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_1_1_Z5O.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_2_1_Fnp.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_3_1_wTC.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_4_1_Ii3.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_5_1_j9a.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_6_1_KU9.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_7_1_6Rd.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_8_1_c48.root',
    ## 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_9_1_34q.root',
        ),
        lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )
    )
else :
    histFileName = 'jetStudiesQCDFlat.root'
    ## Source
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_10_1_dly.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_11_1_gSw.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_12_1_t6v.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_13_1_joV.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_14_1_zg9.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_15_1_MRh.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_16_1_T04.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_17_1_ZD9.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_18_1_VnA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_19_1_EkI.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_1_1_qHQ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_20_1_PsD.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_21_1_dUt.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_22_1_uSw.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_23_1_LVV.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_24_1_lvT.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_25_1_xhC.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_26_1_vth.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_27_1_ymx.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_28_1_VbG.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_29_1_a7A.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_2_1_WRX.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_30_1_ssM.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_31_1_k2q.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_32_1_PDy.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_33_1_d7D.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_34_1_dpo.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_35_1_U7E.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_36_1_jM2.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_37_1_fNT.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_38_1_C7P.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_39_1_RQE.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_3_1_M7r.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_40_1_xH8.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_41_1_iPR.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_42_1_PJy.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_43_1_RBd.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_44_1_xx8.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_45_1_ifw.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_46_1_g21.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_47_1_UbV.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_48_1_SSZ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_49_1_9GE.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_4_1_dIa.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_50_1_yeS.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_51_1_35b.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_52_1_EHP.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_53_1_daE.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_54_1_uv2.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_55_1_EP4.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_56_1_5GY.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_57_1_lIR.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_58_1_QdU.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_59_1_z4c.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_5_1_7yL.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_60_1_irZ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_61_1_8vw.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_62_1_KfX.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_63_1_9WI.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_64_1_qK4.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_65_1_WBo.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_66_1_X7D.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_67_1_kvY.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_68_1_7Lj.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_69_1_lqf.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_6_1_yss.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_70_1_WaC.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_71_1_ZEU.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_72_1_niX.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_73_1_fmX.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_74_1_Avr.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_75_1_ZER.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_76_1_77o.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_77_1_efE.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_78_1_peI.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_79_1_e8z.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_7_1_vNk.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_80_1_Y1G.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_81_1_6Yl.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_82_1_9vK.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_83_1_jRd.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_84_1_PUr.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_85_1_phH.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_86_1_Hpn.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_87_1_0Rc.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_88_1_AyL.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_89_1_aNN.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_8_1_PkZ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_90_1_ziW.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_Flat_7TeV/ttbsm_v1_Spring11-START311_V1A-v1/6b2e8dd0fca338a27d42f8bebea49998/ttbsm_413_9_1_NYT.root'

        )
    )    
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.JetAnalysis.jetStudies2011_cfi import jetStudies2011 as jetStudies2011


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(histFileName)
                                   )


process.ak5Analyzer = cms.EDAnalyzer('EDJetStudies2011',
                                     jetStudies2011.clone()
                                     )

process.ca8Analyzer = cms.EDAnalyzer('EDJetStudies2011',
                                     jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PF'),
                                                           useCA8GenJets = cms.bool(True)
                                                           )
                                     )

process.ca8PrunedAnalyzer = cms.EDAnalyzer('EDJetStudies2011',
                                           jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                                 useCA8GenJets = cms.bool(True)
                                                                 )
                                           )

process.ca8PrunedAnalyzerBTagSearch = cms.EDAnalyzer('EDJetStudies2011',
                                                     jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                                           useCA8GenJets = cms.bool(True),
                                                                           useBTags = cms.bool(True),
                                                                           orderByMass =cms.bool(True),
                                                                           )
                                                     )

process.ca8PrunedAnalyzerBTagMuSearch = cms.EDAnalyzer('EDJetStudies2011',
                                                     jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                                           useCA8GenJets = cms.bool(True),
                                                                           useBTags = cms.bool(True),
                                                                           orderByMass = cms.bool(True),
                                                                           trigs = cms.vstring([
                                                                               'HLT_Mu24_v1'
                                                                               ])
                                                                           )
                                                     )


process.ca8TopTagAnalyzer = cms.EDAnalyzer('EDJetStudies2011',
                                           jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCATopTagPF'),
                                                                 useCA8GenJets = cms.bool(True)
                                                                 )
                                           )

process.p = cms.Path(
    process.ak5Analyzer*
    process.ca8Analyzer*
    process.ca8PrunedAnalyzer*
    process.ca8TopTagAnalyzer*
    process.ca8PrunedAnalyzerBTagSearch*
    process.ca8PrunedAnalyzerBTagMuSearch
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
