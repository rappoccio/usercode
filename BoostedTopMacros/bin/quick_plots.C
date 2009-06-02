{   

  TChain * t = new TChain("Events");

    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_10.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_11.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_12.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_13.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_14.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_15.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_16.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_17.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_18.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_19.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_1.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_20.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_21.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_22.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_23.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_2.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_3.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_4.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_5.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_6.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_7.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_8.root");
    t->AddFile("/uscms_data/d2/rappocc/TopTaggingV2/ttbar_v5/ca_pat_slim_223_9.root");

    TChain * old = new TChain("Events");

    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_11.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_12.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_13.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_14.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_15.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_16.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_17.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_18.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_19.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_1.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_20.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_21.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_22.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_23.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_2.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_3.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_4.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_5.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_6.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_7.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_8.root");
    old->AddFile("/uscms_data/d2/rappocc/TopTagging/ttbar/ca_pat_slim_220_9.root");


    t->SetAlias("jets", "patJets_selectedLayer1Jets__CATopJets.obj");

    TCanvas * c1 = new TCanvas ("c1", "c1");

    c1->Print("simpleplots.ps[");
    t->Draw("jets.partonFlavour_ >> flavor(25,0,25)");
    c1->Print("simpleplots.ps");
    t->Draw("jets.pt() >> jets_pt(24, 0, 1200)");
    c1->Print("simpleplots.ps");
    t->Draw("jets.pt() >> jets_pt_top(24, 0, 1200)", "abs(jets.partonFlavour_) == 6");
    c1->Print("simpleplots.ps");
    t->Draw("jets.nConstituents() >> n_subjet(5,0,5)");
    c1->Print("simpleplots.ps");
    t->Draw("jets.nConstituents() >> n_subjet_top(5,0,5)", "abs(jets.partonFlavour_) == 6");
    c1->Print("simpleplots.ps");
    c1->Print("simpleplots.ps]");

}
