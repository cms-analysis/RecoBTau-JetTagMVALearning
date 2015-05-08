#!/bin/sh
#Rootfiles merged using: merge_from_storage.sh
#

#path_to_rootfiles=VariableExtraction/gridjobs/cMVA_default_filterOn/

#echo "Filling the 2D pt/eta histograms and calculating the pt/eta weights" 

#g++ histoJetEtaPt.cpp `root-config --cflags --glibs` -o histos
#./histos $path_to_rootfiles

#echo "saving the relevant variables " 
#nohup cmsRun MVATrainer_B_cfg.py &
#nohup cmsRun MVATrainer_C_cfg.py &
#nohup cmsRun MVATrainer_DUSG_cfg.py &
#
#hadd train_save_all.root train_B_save.root train_C_save.root train_DUSG_save.root
#
##echo "Do the actual training"

##TRAINING_TAG1=SC_CSVSL
###mkdir $TRAINING_TAG1
##cd $TRAINING_TAG1
##nohup mvaTreeTrainer ../SuperCombined_CSVSL.xml SC_CSVSL.mva ../train_save_all.root &
##cd ..

##TRAINING_TAG2=SC_CSVJP
##mkdir $TRAINING_TAG2
##cd $TRAINING_TAG2
##nohup mvaTreeTrainer ../SuperCombined_CSVJP.xml SC_CSVJP.mva ../train_save_all.root &
##cd ..

#TRAINING_TAG3=SC_CSVJPSL
#mkdir $TRAINING_TAG3
#cd $TRAINING_TAG3
nohup mvaTreeTrainer ../SuperCombined_CSVJPSL.xml SC_CSVJPSL.mva ../train_save_all.root &
#cd ..

##TRAINING_TAG4=SC_CSVJPSM
##mkdir $TRAINING_TAG4
##cd $TRAINING_TAG4
##nohup mvaTreeTrainer ../SuperCombined_CSVJPSM.xml SC_CSVJPSM.mva ../train_save_all.root &
##cd ..
##
##TRAINING_TAG5=SC_CSVSM
##mkdir $TRAINING_TAG5
##cd $TRAINING_TAG5
##nohup mvaTreeTrainer ../SuperCombined_CSVSM.xml SC_CSVSM.mva ../train_save_all.root &
##cd ..

##echo "do now manually cmsRun ../copyMVAToSQLite_cfg.py to copy the mva training output to sqlite format"
