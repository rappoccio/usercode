import FWCore.ParameterSet.Config as cms

# from 

def RecoInput() : 
 return cms.Source("PoolSource",
                   debugVerbosity = cms.untracked.uint32(200),
                   debugFlag = cms.untracked.bool(True),
                   
                   fileNames = cms.untracked.vstring(
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/063B4FB8-30E3-DD11-BF44-00161725E4DD.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/26EA0EB0-46E7-DD11-AA96-0013D3541F6E.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/2E474FC7-43E7-DD11-B211-00E0817917AB.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/3003F9D0-30E3-DD11-A9E1-0013D3228229.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/50EEEBCF-43E7-DD11-A9E3-001A64789D54.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/5A127E01-43E7-DD11-B0E3-0015170AE344.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/627228B6-3AE7-DD11-9314-00E0812D72E2.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/72D6DAC2-43E7-DD11-BF2B-0015170AC6B4.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/8E537F9D-3AE7-DD11-9809-0015170AD178.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/8ECA8B7A-43E7-DD11-9452-0015170AE398.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/8EE3C27A-43E7-DD11-BC2A-0015170AC780.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/9061117D-30E3-DD11-98DF-001A64789DE0.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/96DB58B4-46E7-DD11-B187-0013D32281CF.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/982D32C6-43E7-DD11-AA95-001A64789D9C.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/9E5CD6DF-46E7-DD11-9B3B-00E0812D7D1A.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/A6EF81C9-43E7-DD11-947A-003048673E8A.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/B05FA3B5-38E3-DD11-9967-003048326974.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/B6052DC6-38E3-DD11-AE38-00304832691A.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/B643411A-56E3-DD11-9F81-003048635E32.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/BCA912CD-43E7-DD11-88E3-003048673FFC.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/BE15F9BF-47E7-DD11-8A68-001A64789490.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/BE76E416-45E7-DD11-8C90-00E08178C039.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/C67E18CF-43E7-DD11-9BF3-003048673E7A.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/C86CC6C3-47E7-DD11-B71A-001A64789D44.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/D6C2911A-3AE7-DD11-97F8-00161720D8B7.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/EC0661CE-43E7-DD11-87DF-001A64789D94.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/EE3938C7-39E7-DD11-801B-0015170AC464.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/F0BC5084-43E7-DD11-9105-0030486361BC.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/F460753E-3AE7-DD11-B6F3-00E0812D8C00.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/FA12CFC8-39E7-DD11-BAE6-0015170AE680.root',
        '/store/mc/Summer08/VQQ-madgraph/USER/IDEAL_V9_PAT_v3/0000/FE5D20C4-43E7-DD11-98E5-003048670ADA.root'           )
                   )
