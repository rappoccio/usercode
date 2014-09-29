{

  TChain * t = new TChain("Events");

t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_10.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_1.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_2.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_3.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_4.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_5.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_6.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_7.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_8.root");
t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/zprime_m3000_w30_testing/ca_pat_fat_223_9.root");

 t->SetAlias("jets", "patJets_selectedLayer1Jets__CATopJets.obj");

 t->SetAlias("recojets", "recoBasicJets_caTopJetsProducer__CATopJets.obj");
 t->SetAlias("subjets",  "recoCaloJets_caTopJetsProducer_caTopSubJets_CATopJets.obj");
 t->SetAlias("taginfos", "recoCATopJetTagInfos_CATopJetTagger__CATopJets.obj.properties_");

}
