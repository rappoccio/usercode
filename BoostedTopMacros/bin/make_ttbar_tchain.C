#include "TChain.h"


TChain * make_ttbar_ttchain(const char * name = "Events")
{

  TChain * c = new TChain(name);


  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_11.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_12.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_13.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_14.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_15.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_16.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_17.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_18.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_19.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_1.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_20.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_21.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_22.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_23.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_2.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_3.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_4.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_5.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_6.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_7.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_8.root");
  c->AddFile("/uscms_data/d1/rappocc/TopTagging/ttbar/ca_pat_slim_220_9.root");

  return c;

}
