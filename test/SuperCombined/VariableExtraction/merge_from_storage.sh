#!/bin/bash

maindirec=/pnfs/iihe/cms/store/user/pvmulder/Trees_cMVA_740pre8/cMVA_default_filterOn_fix/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Phys14DR-PU20bx25_PHYS14_25_V1-v1_AODSIM/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/cMVA_default_filterOn/150317_131746/

dirs_to_merge=(0000)

homedirec=/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/cMVA_development/CMSSW_7_4_0_pre8/src/RecoBTau/JetTagMVALearning/test/SuperCombined/cMVA_test1/VariableExtraction/gridjobs/cMVA_default_filterOn/

CAT=(combinedMVA)
FLAV=(B C DUSG)

cd $homedirec

for l in ${dirs_to_merge[@]} ;
do
	for k in ${CAT[@]} ;
	do
		for j in $( ls $maindirec/$l/${k}_B*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Bfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_C*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Cfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_D*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_U*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_S*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_G*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done			
	done
done	

for k in ${CAT[@]} ;
do
	for i in ${FLAV[@]} ;
	do
#		echo cat ${k}${i}files.txt
		rootfiles=`cat ${k}${i}files.txt`
		hadd tmp.root $rootfiles
		mv tmp.root ${k}_${i}.root
	done
done

cd -
