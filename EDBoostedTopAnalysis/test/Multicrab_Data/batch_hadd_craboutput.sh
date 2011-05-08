#!/bin/bash
ARG1=$1

YEAR=`date +%Y`
MONTH=`date +%m`
DAY=`date +%d`
DATE=`echo ${YEAR}_${MONTH}_${DAY}`

for STRING in Results*
do
	FOLDER=`echo ${STRING}`
	DIR=`echo ${FOLDER}/res/`
	COMBINE_FILE=`echo combine_${STRING}.root`
	echo
	echo $STRING
	echo $DIR
	echo $COMBINE_FILE
	hadd -f $COMBINE_FILE $DIR/*.root
done

hadd -f combine_Results_data_${DATE}_${ARG1}.root combine*.root
