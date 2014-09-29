#!/bin/bash

echo "input parameters: cluster, process, run path, input path, output path, data?, leptype " $1 $2 $3 $4 $5 $6

CLUSTER=$1
PROCESS=$2
RUNPATH=$3
INPATH=$4
OUTPATH=$5 
DATA=$6
LEPTYPE=1

cd $RUNPATH
source /uscmst1/prod/sw/cms/shrc uaf
eval `scramv1 runtime -sh`

counter=0

for dir in `ls $INPATH`; do
    echo "going here: "$dir
    if test -d $INPATH/$dir/res; then
	echo "directory   $INPATH/$dir/res   exists"
	if test $DATA -eq 0; then
        if test $counter -eq $PROCESS; then
            echo "python shyft_fwlite.py --lepType 1 --files $INPATH/$dir/res/shyftDump_\*.root --pileupReweight nominal --addDirs --outname $OUTPATH/${dir}_nominal"
            python shyft_fwlite.py --lepType 1  --files $INPATH/$dir/res/shyftDump_\*.root --pileupReweight nominal --addDirs --outname $OUTPATH/${dir}_nominal
            echo "python shyft_fwlite.py --lepType 1 --noMET --files $INPATH/$dir/res/shyftDump_\*.root --pileupReweight nominal --addDirs --outname $OUTPATH/${dir}_noMETCut"
            python shyft_fwlite.py --lepType 1 --noMET --files $INPATH/$dir/res/shyftDump_\*.root --pileupReweight nominal --addDirs --outname $OUTPATH/${dir}_noMETCut
        fi
	    let "counter+=1"
	else
	    let "counter+=1"
	fi
	
    fi
done
