import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() : 
 return cms.Source("PoolSource",
                   debugVerbosity = cms.untracked.uint32(200),
                   debugFlag = cms.untracked.bool(True),
                   
                   fileNames = cms.untracked.vstring(
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0001/4C7B8ABC-68E0-DD11-A831-003048673FC0.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0001/52C10BA0-08E0-DD11-A41F-00E0817917BB.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0001/80FA8508-40E1-DD11-9F3A-001A64789D6C.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0001/D834A532-56E0-DD11-AABA-0015170AE7AC.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0002/8A0B44B9-6BE0-DD11-BE71-00E08178C053.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0002/F01590C5-42E1-DD11-A7A5-0013D3228147.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/0091BE0D-6BE4-DD11-801F-001A6478705C.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/A4282023-4DE6-DD11-92EB-00E08178C199.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/A6295281-8CE1-DD11-9F75-00E08178C039.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/B2CDC887-8CE1-DD11-AD81-0013D3DE2633.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/C250E452-C2E1-DD11-94A5-00E081791773.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/C8218C49-72E4-DD11-923F-001A64789D14.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/D40478D7-68E4-DD11-BFF8-00E0817917E3.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/D8B164BA-8BE1-DD11-AAD8-00E08178C14D.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0004/F8828CF8-C0E1-DD11-B986-001A64789CE4.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0005/8CB1D564-DFE1-DD11-BE71-003048673E7A.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0005/ECDA4194-F6E1-DD11-B3AF-003048635E12.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/16057F96-43E3-DD11-83B6-0015170AD23C.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/2E567260-36E3-DD11-9B62-00E0817918B3.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/40B284E4-D2E2-DD11-A32F-003048670B36.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/60FCAC35-C1E3-DD11-A5BC-003048635E0E.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/76970F8F-F6E1-DD11-8C24-001A64789360.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/AE795DAF-3AE3-DD11-9720-003048674048.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/DADF567E-4EE3-DD11-BFE7-001A64789D20.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/EE5245D7-3EE3-DD11-B2A7-003048673EA8.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0006/F2760C3F-0CE7-DD11-9540-0013D3DE26AF.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/02248717-4DE6-DD11-8913-001A647894DC.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/046D8F88-E7E6-DD11-876E-00151715BB94.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/0A5981BC-B8E4-DD11-B9BD-00E08178C0DB.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/0CD198F5-F4E7-DD11-B7E0-00E0812D7DAA.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/0CDF69AD-F4E7-DD11-850E-0015170AE55C.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/18DF0A8D-F4E7-DD11-A330-0015170AE29C.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/1CC1439F-F5E7-DD11-9BD5-00161725E4F3.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/1EC2B911-86E4-DD11-9AC2-001A64789504.root',
        '/store/mc/Summer08/VQQ-madgraph/GEN-SIM-RECO/IDEAL_V11_redigi_v1/0007/2239A726-F6E7-DD11-98AB-00E081791867.root'            )
                   )
