#!/bin/bash

for LABEL in ScaleUp ScaleDown PtSmearUp PtSmearDown EtaSmearUp EtaSmearDown
do
	for DIR in Zprime_M1000GeV_W100GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M1000GeV_W10GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M1500GeV_W150GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M1500GeV_W15GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M2000GeV_W200GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M2000GeV_W20GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M3000GeV_W300GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M3000GeV_W30GeV_ttbsm_v8_ttbsmTuples_v4 Zprime_M750GeV_W7500MeV_ttbsm_v8_ttbsmTuples_v4
	do
		echo $LABEL $DIR 
		python TTHadronicAnalyzerCombined.py --dirs=/uscms_data/d2/jdolen/BoostedTop424Ntuple/CMSSW_4_2_4/src/Analysis/TTBSMPatTuples/test/${DIR}/res/ --outfile=TTHadronicAnalyzerCombined_${DIR} --analyzer=Type11Analyzer --mistagFile=MISTAG_RATE_TYPE1 --useMC --collectionLabelSuffix=$LABEL
	done
done	
