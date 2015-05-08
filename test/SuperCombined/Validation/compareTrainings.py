######################################################################
###                                                                ###
### Script for plotting comparisons of different performances      ###
###                                                                ###
### Main thing to be changed by YOU: list of paths.                ###
###                                                                ###
### Easily adjustable                                              ###
### - legend                                                       ###
### - color                                                        ### 
###                                                                ###
### Assumes you have your CSV performance files                    ###
### in different directories for different training settings       ###
###                                                                ###
### TODO: - make it usable for pT/eta comparisons too              ###
###       - let setting be specified 'outside' the script when running
###                                                                ###
######################################################################
###                                                                ###
### What the user needs to do:                                     ###
###                                                                ###
### 1) Adjust the list of training settings that you would like to compare
### 2) Update the maps of paths/colors/legends such that the maps are not empty for you new variable
### 3) Run as python -i compareTrainings.py                    ###
###                                                                ###
######################################################################

from ROOT import *
gROOT.SetStyle("Plain")

############################################################################################ 
### This is the list of training settings you would like to compare                      ###
### => Change it if you would like to compare more/different settings.                   ###
### => If you add new variables, update the maps of path/color/legend accordingly (once) ###
############################################################################################ 

plotPerfEtaPt = false
plotDiscriminator = false

settingList = [
								"CSV", #CSV
								"JP", 
#								"GT", 
								"CSVv2"#, #CSVv2
#								"CSVSL", #CSVSL
#								"cMVA"#, 
#								"cMVA_new"#, 
#								"JBP"#, 
]
#################################################
### here are just some maps of paths          ###
###  and legend names and colors for plotting ###
### - paths: adjust only once                 ### 
### - legend/color: adjust when you want      ###
#################################################

#path = "Validation_CSVIVFinput_notCSVv2IVF/DQM_V0001_R000000001__POG__BTAG__cMVA.root"
path = "DQM_V0001_R000000001__POG__BTAG__cMVA.root"
#path = "DQM_V0001_R000000001__POG__BTAG__cMVA_VBFHtoBB.root"
#path = "DQM_V0001_R000000001__POG__BTAG__cMVA_qcdHT100To250.root"

#pathList = {
#						"CSV": path,
#						"CSVv2": path,
#						} 

legend = {
				"CSV": "CSV",
				"JP": "JP",
				"GT": "GT",
				"CSVv2": "CSVv2",
				"CSVSL": "CSVSL",
				"cMVA": "cMVA",
				"cMVA_new": "cMVA 74X",
#				"JBP": "JBP",
       }

color = {
			"CSV": 1, #9
			"JP": 6,
			"GT": 7,
			"CSVv2": 2,
			"CSVSL": 8,
			"cMVA": 4,
			"cMVA_new": 1,
#			"JBP": 7,
         }

#####################################
### Retrieve global performance   ###
#####################################
   
plotList   = {}
plotList_C = {}
plotListeta1   = {}
plotListeta1_C = {}
plotListeta2   = {}
plotListeta2_C = {}
plotListeta3   = {}
plotListeta3_C = {}
plotListpt1   = {}
plotListpt1_C = {}
plotListpt2   = {}
plotListpt2_C = {}
plotListpt3   = {}
plotListpt3_C = {}

for setting in settingList:
    ### Get file and plot
#    fileName = pathList[setting]
    fileName = path
    file     = TFile.Open(fileName)
    print setting
    if setting == "CSV" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/FlavEffVsBEff_DUSG_discr_CSV_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/FlavEffVsBEff_C_discr_CSV_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_CSV_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_0-1v2/FlavEffVsBEff_C_discr_CSV_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_CSV_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_1v2-2v1/FlavEffVsBEff_C_discr_CSV_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_CSV_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_2v1-2v4/FlavEffVsBEff_C_discr_CSV_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_PT_40-60/FlavEffVsBEff_DUSG_discr_CSV_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_PT_40-60/FlavEffVsBEff_C_discr_CSV_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_PT_90-150/FlavEffVsBEff_DUSG_discr_CSV_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_PT_90-150/FlavEffVsBEff_C_discr_CSV_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_PT_400-600/FlavEffVsBEff_DUSG_discr_CSV_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_PT_400-600/FlavEffVsBEff_C_discr_CSV_PT_400-600")
    elif setting == "CSVv2" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_GLOBAL/FlavEffVsBEff_DUSG_discr_CSVv2_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_GLOBAL/FlavEffVsBEff_C_discr_CSVv2_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_CSVv2_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_ETA_0-1v2/FlavEffVsBEff_C_discr_CSVv2_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_CSVv2_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_ETA_1v2-2v1/FlavEffVsBEff_C_discr_CSVv2_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_CSVv2_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_ETA_2v1-2v4/FlavEffVsBEff_C_discr_CSVv2_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_PT_40-60/FlavEffVsBEff_DUSG_discr_CSVv2_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_PT_40-60/FlavEffVsBEff_C_discr_CSVv2_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_PT_90-150/FlavEffVsBEff_DUSG_discr_CSVv2_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_PT_90-150/FlavEffVsBEff_C_discr_CSVv2_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_PT_400-600/FlavEffVsBEff_DUSG_discr_CSVv2_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVv2_PT_400-600/FlavEffVsBEff_C_discr_CSVv2_PT_400-600")
    elif setting == "CSVSL" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/FlavEffVsBEff_DUSG_discr_CSVSL_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/FlavEffVsBEff_C_discr_CSVSL_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_CSVSL_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_0-1v2/FlavEffVsBEff_C_discr_CSVSL_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_CSVSL_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_1v2-2v1/FlavEffVsBEff_C_discr_CSVSL_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_CSVSL_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_2v1-2v4/FlavEffVsBEff_C_discr_CSVSL_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_PT_40-60/FlavEffVsBEff_DUSG_discr_CSVSL_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_PT_40-60/FlavEffVsBEff_C_discr_CSVSL_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_PT_90-150/FlavEffVsBEff_DUSG_discr_CSVSL_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_PT_90-150/FlavEffVsBEff_C_discr_CSVSL_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_PT_400-600/FlavEffVsBEff_DUSG_discr_CSVSL_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_PT_400-600/FlavEffVsBEff_C_discr_CSVSL_PT_400-600")
    elif setting == "cMVA" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/FlavEffVsBEff_DUSG_discr_cMVA_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/FlavEffVsBEff_C_discr_cMVA_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_cMVA_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_ETA_0-1v2/FlavEffVsBEff_C_discr_cMVA_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_cMVA_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_ETA_1v2-2v1/FlavEffVsBEff_C_discr_cMVA_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_cMVA_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_ETA_2v1-2v4/FlavEffVsBEff_C_discr_cMVA_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_PT_40-60/FlavEffVsBEff_DUSG_discr_cMVA_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_PT_40-60/FlavEffVsBEff_C_discr_cMVA_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_PT_90-150/FlavEffVsBEff_DUSG_discr_cMVA_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_PT_90-150/FlavEffVsBEff_C_discr_cMVA_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_PT_400-600/FlavEffVsBEff_DUSG_discr_cMVA_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_PT_400-600/FlavEffVsBEff_C_discr_cMVA_PT_400-600")
    elif setting == "cMVA_new" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/FlavEffVsBEff_DUSG_discr_cMVA_new_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/FlavEffVsBEff_C_discr_cMVA_new_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_cMVA_new_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_ETA_0-1v2/FlavEffVsBEff_C_discr_cMVA_new_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_cMVA_new_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_ETA_1v2-2v1/FlavEffVsBEff_C_discr_cMVA_new_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_cMVA_new_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_ETA_2v1-2v4/FlavEffVsBEff_C_discr_cMVA_new_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_PT_40-60/FlavEffVsBEff_DUSG_discr_cMVA_new_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_PT_40-60/FlavEffVsBEff_C_discr_cMVA_new_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_PT_90-150/FlavEffVsBEff_DUSG_discr_cMVA_new_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_PT_90-150/FlavEffVsBEff_C_discr_cMVA_new_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_PT_400-600/FlavEffVsBEff_DUSG_discr_cMVA_new_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_PT_400-600/FlavEffVsBEff_C_discr_cMVA_new_PT_400-600")
    elif setting == "JP" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/JP_GLOBAL/FlavEffVsBEff_DUSG_discr_JP_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_GLOBAL/FlavEffVsBEff_C_discr_JP_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/JP_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_JP_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_ETA_0-1v2/FlavEffVsBEff_C_discr_JP_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/JP_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_JP_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_ETA_1v2-2v1/FlavEffVsBEff_C_discr_JP_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/JP_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_JP_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_ETA_2v1-2v4/FlavEffVsBEff_C_discr_JP_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/JP_PT_40-60/FlavEffVsBEff_DUSG_discr_JP_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_PT_40-60/FlavEffVsBEff_C_discr_JP_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/JP_PT_90-150/FlavEffVsBEff_DUSG_discr_JP_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_PT_90-150/FlavEffVsBEff_C_discr_JP_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/JP_PT_400-600/FlavEffVsBEff_DUSG_discr_JP_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/JP_PT_400-600/FlavEffVsBEff_C_discr_JP_PT_400-600")
    elif setting == "JBP" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_GLOBAL/FlavEffVsBEff_DUSG_discr_JBP_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_GLOBAL/FlavEffVsBEff_C_discr_JBP_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_JBP_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_ETA_0-1v2/FlavEffVsBEff_C_discr_JBP_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_JBP_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_ETA_1v2-2v1/FlavEffVsBEff_C_discr_JBP_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_JBP_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_ETA_2v1-2v4/FlavEffVsBEff_C_discr_JBP_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_PT_40-60/FlavEffVsBEff_DUSG_discr_JBP_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_PT_40-60/FlavEffVsBEff_C_discr_JBP_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_PT_90-150/FlavEffVsBEff_DUSG_discr_JBP_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_PT_90-150/FlavEffVsBEff_C_discr_JBP_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/JBP_PT_400-600/FlavEffVsBEff_DUSG_discr_JBP_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/JBP_PT_400-600/FlavEffVsBEff_C_discr_JBP_PT_400-600")
    elif setting == "GT" :
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/GT_GLOBAL/FlavEffVsBEff_DUSG_discr_GT_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_GLOBAL/FlavEffVsBEff_C_discr_GT_GLOBAL")
       ploteta1     = file.Get("DQMData/Run 1/Btag/Run summary/GT_ETA_0-1v2/FlavEffVsBEff_DUSG_discr_GT_ETA_0-1v2")
       ploteta1_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_ETA_0-1v2/FlavEffVsBEff_C_discr_GT_ETA_0-1v2")
       ploteta2     = file.Get("DQMData/Run 1/Btag/Run summary/GT_ETA_1v2-2v1/FlavEffVsBEff_DUSG_discr_GT_ETA_1v2-2v1")
       ploteta2_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_ETA_1v2-2v1/FlavEffVsBEff_C_discr_GT_ETA_1v2-2v1")
       ploteta3     = file.Get("DQMData/Run 1/Btag/Run summary/GT_ETA_2v1-2v4/FlavEffVsBEff_DUSG_discr_GT_ETA_2v1-2v4")
       ploteta3_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_ETA_2v1-2v4/FlavEffVsBEff_C_discr_GT_ETA_2v1-2v4")
       plotpt1     = file.Get("DQMData/Run 1/Btag/Run summary/GT_PT_40-60/FlavEffVsBEff_DUSG_discr_GT_PT_40-60")
       plotpt1_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_PT_40-60/FlavEffVsBEff_C_discr_GT_PT_40-60")
       plotpt2     = file.Get("DQMData/Run 1/Btag/Run summary/GT_PT_90-150/FlavEffVsBEff_DUSG_discr_GT_PT_90-150")
       plotpt2_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_PT_90-150/FlavEffVsBEff_C_discr_GT_PT_90-150")
       plotpt3     = file.Get("DQMData/Run 1/Btag/Run summary/GT_PT_400-600/FlavEffVsBEff_DUSG_discr_GT_PT_400-600")
       plotpt3_C   = file.Get("DQMData/Run 1/Btag/Run summary/GT_PT_400-600/FlavEffVsBEff_C_discr_GT_PT_400-600")
#    else
#			print "check path to DQM file or histogram directory and name inside the DQM file"
		### Set name of plot
    plot.SetName("")
    plot_C.SetName("")
    ### Fill plot list
    plotList[setting]   = plot  
    plotList_C[setting] = plot_C
    plotListeta1[setting]   = ploteta1  
    plotListeta1_C[setting] = ploteta1_C
    plotListeta2[setting]   = ploteta2  
    plotListeta2_C[setting] = ploteta2_C
    plotListeta3[setting]   = ploteta3  
    plotListeta3_C[setting] = ploteta3_C
    plotListpt1[setting]   = plotpt1  
    plotListpt1_C[setting] = plotpt1_C
    plotListpt2[setting]   = plotpt2  
    plotListpt2_C[setting] = plotpt2_C
    plotListpt3[setting]   = plotpt3  
    plotListpt3_C[setting] = plotpt3_C


### Plot global performance ###

Plots2 = TCanvas("Plots2","",800,800)

Plots2.cd().SetLogy()
Plots2.cd().SetGridx()
Plots2.cd().SetGridy()
Plots2.SetLeftMargin(0.1683417)
Plots2.SetRightMargin(0.03140704)
Plots2.SetTopMargin(0.0620155)
Plots2.SetBottomMargin(0.1382429)

leg = TLegend(0.72,0.17,0.95,0.47)
leg.SetFillColor(0);

leg2 = TLegend(0.2,0.78,0.3,0.88)
leg2.SetFillColor(0);

### and draw ###

first=true
for setting in settingList:
    plotList[setting].SetMarkerColor(color[setting])
    plotList[setting].SetMarkerStyle(20)
    plotList_C[setting].SetMarkerColor(color[setting])
    plotList_C[setting].SetMarkerStyle(21)
    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
			plotList[setting].SetMarkerStyle(20)
			plotList_C[setting].SetMarkerStyle(21)
    if first:
        plotList[setting].GetXaxis().SetTitle("b eff.")
        plotList[setting].GetYaxis().SetTitle("mistag eff.")
        plotList[setting].GetYaxis().SetTitleOffset(1.2)
        plotList[setting].GetYaxis().SetRangeUser(0.0004,1)
        plotList[setting].GetXaxis().SetRangeUser(0.1,1)
        plotList[setting].SetTitle("")
        plotList[setting].Draw("")
        plotList_C[setting].Draw("same")  
        leg2.AddEntry(plotList_C[setting],"c","p")
        leg2.AddEntry(plotList[setting],"dusg","p")
        first=false
    else         :
        plotList[setting].Draw("same")  
        plotList_C[setting].Draw("same")  
    leg.AddEntry(plotList[setting],legend[setting],"p")
  
leg.Draw()
leg2.Draw()

if plotPerfEtaPt:

	### Plot etabin 1 performance ###

	Plotseta1 = TCanvas("Plotseta1","",800,800)

	Plotseta1.cd().SetLogy()
	Plotseta1.cd().SetGridx()
	Plotseta1.cd().SetGridy()
	Plotseta1.SetLeftMargin(0.1683417)
	Plotseta1.SetRightMargin(0.03140704)
	Plotseta1.SetTopMargin(0.0620155)
	Plotseta1.SetBottomMargin(0.1382429)

	legeta1 = TLegend(0.72,0.17,0.95,0.27)
	legeta1.SetFillColor(0);

	leg2eta1 = TLegend(0.2,0.73,0.35,0.88)
	leg2eta1.SetFillColor(0);
	leg2eta1.SetHeader("0<|#eta|<1.2")

	### and draw ###

	first=true
	for setting in settingList:
	    plotListeta1[setting].SetMarkerColor(color[setting])
	    plotListeta1[setting].SetMarkerStyle(24)
	    plotListeta1_C[setting].SetMarkerColor(color[setting])
	    plotListeta1_C[setting].SetMarkerStyle(25)
	    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
				plotListeta1[setting].SetMarkerStyle(20)
				plotListeta1_C[setting].SetMarkerStyle(21)
	    if first:
	        plotListeta1[setting].GetXaxis().SetTitle("b eff.")
	        plotListeta1[setting].GetYaxis().SetTitle("mistag eff.")
	        plotListeta1[setting].GetYaxis().SetTitleOffset(1.2)
	        plotListeta1[setting].GetYaxis().SetRangeUser(0.0004,1)
	        plotListeta1[setting].GetXaxis().SetRangeUser(0.1,1)
	        plotListeta1[setting].SetTitle("")
	        plotListeta1[setting].Draw("")
	        plotListeta1_C[setting].Draw("same")  
	        leg2eta1.AddEntry(plotListeta1_C[setting],"c","p")
	        leg2eta1.AddEntry(plotListeta1[setting],"dusg","p")
	        first=false
	    else         :
	        plotListeta1[setting].Draw("same")  
	        plotListeta1_C[setting].Draw("same")  
	    legeta1.AddEntry(plotListeta1[setting],legend[setting],"p")
  
	legeta1.Draw()
	leg2eta1.Draw()
	
	Plotseta1.SaveAs("CSVv2_CSVSL_cMVA_taggers_etabin1.png")
	
	### Plot etabin 2 performance ###

	Plotseta2 = TCanvas("Plotseta2","",800,800)

	Plotseta2.cd().SetLogy()
	Plotseta2.cd().SetGridx()
	Plotseta2.cd().SetGridy()
	Plotseta2.SetLeftMargin(0.1683417)
	Plotseta2.SetRightMargin(0.03140704)
	Plotseta2.SetTopMargin(0.0620155)
	Plotseta2.SetBottomMargin(0.1382429)

	legeta2 = TLegend(0.72,0.17,0.95,0.27)
	legeta2.SetFillColor(0);

	leg2eta2 = TLegend(0.2,0.73,0.35,0.88)
	leg2eta2.SetFillColor(0);
	leg2eta2.SetHeader("1.2<|#eta|<2.1")

	### and draw ###

	first=true
	for setting in settingList:
	    plotListeta2[setting].SetMarkerColor(color[setting])
	    plotListeta2[setting].SetMarkerStyle(24)
	    plotListeta2_C[setting].SetMarkerColor(color[setting])
	    plotListeta2_C[setting].SetMarkerStyle(25)
	    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
				plotListeta2[setting].SetMarkerStyle(20)
				plotListeta2_C[setting].SetMarkerStyle(21)
	    if first:
	        plotListeta2[setting].GetXaxis().SetTitle("b eff.")
	        plotListeta2[setting].GetYaxis().SetTitle("mistag eff.")
	        plotListeta2[setting].GetYaxis().SetTitleOffset(1.2)
	        plotListeta2[setting].GetYaxis().SetRangeUser(0.0004,1)
	        plotListeta2[setting].GetXaxis().SetRangeUser(0.1,1)
	        plotListeta2[setting].SetTitle("")
	        plotListeta2[setting].Draw("")
	        plotListeta2_C[setting].Draw("same")  
	        leg2eta2.AddEntry(plotListeta2_C[setting],"c","p")
	        leg2eta2.AddEntry(plotListeta2[setting],"dusg","p")
	        first=false
	    else         :
	        plotListeta2[setting].Draw("same")  
	        plotListeta2_C[setting].Draw("same")  
	    legeta2.AddEntry(plotListeta2[setting],legend[setting],"p")
  
	legeta2.Draw()
	leg2eta2.Draw()

	Plotseta2.SaveAs("CSVv2_CSVSL_cMVA_taggers_etabin2.png")

	### Plot etabin 3 performance ###

	Plotseta3 = TCanvas("Plotseta3","",800,800)

	Plotseta3.cd().SetLogy()
	Plotseta3.cd().SetGridx()
	Plotseta3.cd().SetGridy()
	Plotseta3.SetLeftMargin(0.1683417)
	Plotseta3.SetRightMargin(0.03140704)
	Plotseta3.SetTopMargin(0.0620155)
	Plotseta3.SetBottomMargin(0.1382429)

	legeta3 = TLegend(0.72,0.17,0.95,0.27)
	legeta3.SetFillColor(0);

	leg2eta3 = TLegend(0.2,0.73,0.35,0.88)
	leg2eta3.SetFillColor(0);
	leg2eta3.SetHeader("2.1<|#eta|<2.4")

	### and draw ###

	first=true
	for setting in settingList:
	    plotListeta3[setting].SetMarkerColor(color[setting])
	    plotListeta3[setting].SetMarkerStyle(24)
	    plotListeta3_C[setting].SetMarkerColor(color[setting])
	    plotListeta3_C[setting].SetMarkerStyle(25)
	    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
				plotListeta3[setting].SetMarkerStyle(20)
				plotListeta3_C[setting].SetMarkerStyle(21)
	    if first:
	        plotListeta3[setting].GetXaxis().SetTitle("b eff.")
	        plotListeta3[setting].GetYaxis().SetTitle("mistag eff.")
	        plotListeta3[setting].GetYaxis().SetTitleOffset(1.2)
	        plotListeta3[setting].GetYaxis().SetRangeUser(0.0004,1)
	        plotListeta3[setting].GetXaxis().SetRangeUser(0.1,1)
	        plotListeta3[setting].SetTitle("")
	        plotListeta3[setting].Draw("")
	        plotListeta3_C[setting].Draw("same")  
	        leg2eta3.AddEntry(plotListeta3_C[setting],"c","p")
	        leg2eta3.AddEntry(plotListeta3[setting],"dusg","p")
	        first=false
	    else         :
	        plotListeta3[setting].Draw("same")  
	        plotListeta3_C[setting].Draw("same")  
	    legeta3.AddEntry(plotListeta3[setting],legend[setting],"p")
  
	legeta3.Draw()
	leg2eta3.Draw()

	Plotseta3.SaveAs("CSVv2_CSVSL_cMVA_taggers_etabin3.png")

	### Plot ptbin 1 performance ###

	Plotspt1 = TCanvas("Plotspt1","",800,800)

	Plotspt1.cd().SetLogy()
	Plotspt1.cd().SetGridx()
	Plotspt1.cd().SetGridy()
	Plotspt1.SetLeftMargin(0.1683417)
	Plotspt1.SetRightMargin(0.03140704)
	Plotspt1.SetTopMargin(0.0620155)
	Plotspt1.SetBottomMargin(0.1382429)

	legpt1 = TLegend(0.72,0.17,0.95,0.27)
	legpt1.SetFillColor(0);

	leg2pt1 = TLegend(0.2,0.73,0.4,0.88)
	leg2pt1.SetFillColor(0);
	leg2pt1.SetHeader("40<p_{T}<60 GeV")

	### and draw ###

	first=true
	for setting in settingList:
	    plotListpt1[setting].SetMarkerColor(color[setting])
	    plotListpt1[setting].SetMarkerStyle(24)
	    plotListpt1_C[setting].SetMarkerColor(color[setting])
	    plotListpt1_C[setting].SetMarkerStyle(25)
	    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
				plotListpt1[setting].SetMarkerStyle(20)
				plotListpt1_C[setting].SetMarkerStyle(21)
	    if first:
	        plotListpt1[setting].GetXaxis().SetTitle("b eff.")
	        plotListpt1[setting].GetYaxis().SetTitle("mistag eff.")
	        plotListpt1[setting].GetYaxis().SetTitleOffset(1.2)
	        plotListpt1[setting].GetYaxis().SetRangeUser(0.0004,1)
	        plotListpt1[setting].GetXaxis().SetRangeUser(0.1,1)
	        plotListpt1[setting].SetTitle("")
	        plotListpt1[setting].Draw("")
	        plotListpt1_C[setting].Draw("same")  
	        leg2pt1.AddEntry(plotListpt1_C[setting],"c","p")
	        leg2pt1.AddEntry(plotListpt1[setting],"dusg","p")
	        first=false
	    else         :
	        plotListpt1[setting].Draw("same")  
	        plotListpt1_C[setting].Draw("same")  
	    legpt1.AddEntry(plotListpt1[setting],legend[setting],"p")
  
	legpt1.Draw()
	leg2pt1.Draw()

	Plotspt1.SaveAs("CSVv2_CSVSL_cMVA_taggers_ptbin1.png")

	### Plot ptbin 2 performance ###

	Plotspt2 = TCanvas("Plotspt2","",800,800)

	Plotspt2.cd().SetLogy()
	Plotspt2.cd().SetGridx()
	Plotspt2.cd().SetGridy()
	Plotspt2.SetLeftMargin(0.1683417)
	Plotspt2.SetRightMargin(0.03140704)
	Plotspt2.SetTopMargin(0.0620155)
	Plotspt2.SetBottomMargin(0.1382429)

	legpt2 = TLegend(0.72,0.17,0.95,0.27)
	legpt2.SetFillColor(0);

	leg2pt2 = TLegend(0.2,0.73,0.4,0.88)
	leg2pt2.SetFillColor(0);
	leg2pt2.SetHeader("90<p_{T}<150 GeV")

	### and draw ###

	first=true
	for setting in settingList:
	    plotListpt2[setting].SetMarkerColor(color[setting])
	    plotListpt2[setting].SetMarkerStyle(24)
	    plotListpt2_C[setting].SetMarkerColor(color[setting])
	    plotListpt2_C[setting].SetMarkerStyle(25)
	    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
				plotListpt2[setting].SetMarkerStyle(20)
				plotListpt2_C[setting].SetMarkerStyle(21)
	    if first:
	        plotListpt2[setting].GetXaxis().SetTitle("b eff.")
	        plotListpt2[setting].GetYaxis().SetTitle("mistag eff.")
	        plotListpt2[setting].GetYaxis().SetTitleOffset(1.2)
	        plotListpt2[setting].GetYaxis().SetRangeUser(0.0004,1)
	        plotListpt2[setting].GetXaxis().SetRangeUser(0.1,1)
	        plotListpt2[setting].SetTitle("")
	        plotListpt2[setting].Draw("")
	        plotListpt2_C[setting].Draw("same")  
	        leg2pt2.AddEntry(plotListpt2_C[setting],"c","p")
	        leg2pt2.AddEntry(plotListpt2[setting],"dusg","p")
	        first=false
	    else         :
	        plotListpt2[setting].Draw("same")  
	        plotListpt2_C[setting].Draw("same")  
	    legpt2.AddEntry(plotListpt2[setting],legend[setting],"p")
  
	legpt2.Draw()
	leg2pt2.Draw()

	Plotspt2.SaveAs("CSVv2_CSVSL_cMVA_taggers_ptbin2.png")

	### Plot ptbin 3 performance ###

	Plotspt3 = TCanvas("Plotspt3","",800,800)

	Plotspt3.cd().SetLogy()
	Plotspt3.cd().SetGridx()
	Plotspt3.cd().SetGridy()
	Plotspt3.SetLeftMargin(0.1683417)
	Plotspt3.SetRightMargin(0.03140704)
	Plotspt3.SetTopMargin(0.0620155)
	Plotspt3.SetBottomMargin(0.1382429)

	legpt3 = TLegend(0.72,0.17,0.95,0.27)
	legpt3.SetFillColor(0);

	leg2pt3 = TLegend(0.2,0.73,0.4,0.88)
	leg2pt3.SetFillColor(0);
	leg2pt3.SetHeader("400<p_{T}<600 GeV")

	### and draw ###

	first=true
	for setting in settingList:
	    plotListpt3[setting].SetMarkerColor(color[setting])
	    plotListpt3[setting].SetMarkerStyle(24)
	    plotListpt3_C[setting].SetMarkerColor(color[setting])
	    plotListpt3_C[setting].SetMarkerStyle(25)
	    if setting == "cMVA" or setting == "cMVA_new" or setting == "CSVSL":
				plotListpt3[setting].SetMarkerStyle(20)
				plotListpt3_C[setting].SetMarkerStyle(21)
	    if first:
	        plotListpt3[setting].GetXaxis().SetTitle("b eff.")
	        plotListpt3[setting].GetYaxis().SetTitle("mistag eff.")
	        plotListpt3[setting].GetYaxis().SetTitleOffset(1.2)
	        plotListpt3[setting].GetYaxis().SetRangeUser(0.0004,1)
	        plotListpt3[setting].GetXaxis().SetRangeUser(0.1,1)
	        plotListpt3[setting].SetTitle("")
	        plotListpt3[setting].Draw("")
	        plotListpt3_C[setting].Draw("same")  
	        leg2pt3.AddEntry(plotListpt3_C[setting],"c","p")
	        leg2pt3.AddEntry(plotListpt3[setting],"dusg","p")
	        first=false
	    else         :
	        plotListpt3[setting].Draw("same")  
	        plotListpt3_C[setting].Draw("same")  
	    legpt3.AddEntry(plotListpt3[setting],legend[setting],"p")
  
	legpt3.Draw()
	leg2pt3.Draw()

	Plotspt3.SaveAs("CSVv2_CSVSL_cMVA_taggers_ptbin3.png")





if plotDiscriminator :
	#################################
	### Retrieve discriminator    ###
	#################################

	#flavourList = ["b", "c", "dusg", "pu", "dus", "g", "ni"]
	flavourList = ["b", "c", "dusg", "pu"]
#	flavourList = ["b", "c", "dusg"]

	colorfl = {
				"b": 2,
				"c": 8,
				"dusg": 4,
				"pu": 6,
				"dus": 9,
				"g": 7,
				"ni": 1,
	}

	legend2 = {
				"b": "b",
				"c": "c",
				"dusg": "dusg",
				"pu": "PU",
				"dus": "dus",
				"g": "g",
				"ni": "NI",
	}

	plotListDiscr   = {}
	plotListDiscr2   = {}
	plotListDiscr3   = {}

	for flavour in flavourList:
	    fileName = path
	    file     = TFile.Open(fileName)
	    print flavour
	    if flavour == "b" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALB")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALB")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALB")
	    elif flavour == "c" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALC")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALC")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALC")
	    elif flavour == "dusg" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALDUSG")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALDUSG")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALDUSG")
	    elif flavour == "pu" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALPU")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALPU")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALPU")
	    elif flavour == "dus" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALDUS")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALDUS")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALDUS")
	    elif flavour == "g" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALG")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALG")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALG")
	    elif flavour == "ni" :
	       plotdiscr     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_new_GLOBAL/discr_cMVA_new_GLOBALNI")
	       plotdiscr2     = file.Get("DQMData/Run 1/Btag/Run summary/cMVA_GLOBAL/discr_cMVA_GLOBALNI")
	       plotdiscr3     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALNI")
	    plotdiscr.SetName("")
	    plotListDiscr[flavour] = plotdiscr
	    plotdiscr2.SetName("")
	    plotListDiscr2[flavour] = plotdiscr2
	    plotdiscr3.SetName("")
	    plotListDiscr3[flavour] = plotdiscr3


	### Plot discriminator ###
	Plots_discr = TCanvas("Plots_discr","",800,800)
	Plots_discr.SetLeftMargin(0.1683417)
	Plots_discr.SetRightMargin(0.03140704)
	Plots_discr.SetTopMargin(0.0620155)
	Plots_discr.SetBottomMargin(0.1382429)

	leg3 = TLegend(0.6,0.70,0.75,0.88)
	leg3.SetFillColor(0);

	first=true
	for flavour in flavourList:
	    plotListDiscr[flavour].SetLineColor(colorfl[flavour])
	    plotListDiscr[flavour].SetLineWidth(2)
	    if first:
	        plotListDiscr[flavour].GetXaxis().SetTitle("cMVA 74X discriminator")
	        plotListDiscr[flavour].GetYaxis().SetTitle("a.u.")
	        plotListDiscr[flavour].GetYaxis().SetTitleOffset(1.2)
	        plotListDiscr[flavour].SetTitle("")
	        plott=plotListDiscr[flavour].DrawNormalized("") ## this and the following 4 lines are used to make sure that the range of the y-axis can be set (did not work in any other way)
	        plott.GetYaxis().SetRangeUser(0,0.25)
	        plott.SetLineColor(colorfl[flavour])
	        plott.SetLineWidth(2)
	        plott.Draw("HIST")
	        first=false
	    else         :
	        plotListDiscr[flavour].DrawNormalized("same")  
	    leg3.AddEntry(plotListDiscr[flavour],legend2[flavour],"l")

	leg3.Draw()
	Plots_discr.SaveAs("cMVA_74X_discriminator.png")

#	### Plot discriminator ###
#	Plots_discr2 = TCanvas("Plots_discr2","",800,800)
#	Plots_discr2.SetLeftMargin(0.1683417)
#	Plots_discr2.SetRightMargin(0.03140704)
#	Plots_discr2.SetTopMargin(0.0620155)
#	Plots_discr2.SetBottomMargin(0.1382429)
#
#	leg3b = TLegend(0.6,0.70,0.75,0.88)
#	leg3b.SetFillColor(0);
#
#	first=true
#	for flavour in flavourList:
#	    plotListDiscr2[flavour].SetLineColor(colorfl[flavour])
#	    plotListDiscr2[flavour].SetLineWidth(2)
#	    if first:
#	        plotListDiscr2[flavour].GetXaxis().SetTitle("cMVA discriminator")
#	        plotListDiscr2[flavour].GetYaxis().SetTitle("a.u.")
#	        plotListDiscr2[flavour].GetYaxis().SetTitleOffset(1.2)
#	        plotListDiscr2[flavour].SetTitle("")
#	        plott2=plotListDiscr2[flavour].DrawNormalized("") ## this and the following 4 lines are used to make sure that the range of the y-axis can be set (did not work in any other way)
#	        plott2.GetYaxis().SetRangeUser(0,0.25)
#	        plott2.SetLineColor(colorfl[flavour])
#	        plott2.SetLineWidth(2)
#	        plott2.Draw("HIST")
#	        first=false
#	    else         :
#	        plotListDiscr2[flavour].DrawNormalized("same")  
#	    leg3b.AddEntry(plotListDiscr2[flavour],legend2[flavour],"l")
#
#	leg3b.Draw()
#	Plots_discr2.SaveAs("cMVA_discriminator.png")
#
#	### Plot discriminator ###
#	Plots_discr3 = TCanvas("Plots_discr3","",800,800)
#	Plots_discr3.SetLeftMargin(0.1683417)
#	Plots_discr3.SetRightMargin(0.03140704)
#	Plots_discr3.SetTopMargin(0.0620155)
#	Plots_discr3.SetBottomMargin(0.1382429)
#
#	leg3c = TLegend(0.6,0.70,0.75,0.88)
#	leg3c.SetFillColor(0);
#
#	first=true
#	for flavour in flavourList:
#	    plotListDiscr3[flavour].SetLineColor(colorfl[flavour])
#	    plotListDiscr3[flavour].SetLineWidth(2)
#	    if first:
#	        plotListDiscr3[flavour].GetXaxis().SetTitle("CSVSL discriminator")
#	        plotListDiscr3[flavour].GetYaxis().SetTitle("a.u.")
#	        plotListDiscr3[flavour].GetYaxis().SetTitleOffset(1.2)
#	        plotListDiscr3[flavour].SetTitle("")
#	        plott3=plotListDiscr3[flavour].DrawNormalized("") ## this and the following 4 lines are used to make sure that the range of the y-axis can be set (did not work in any other way)
#	        plott3.GetYaxis().SetRangeUser(0,0.25)
#	        plott3.SetLineColor(colorfl[flavour])
#	        plott3.SetLineWidth(2)
#	        plott3.Draw("HIST")
#	        first=false
#	    else         :
#	        plotListDiscr3[flavour].DrawNormalized("same")  
#	    leg3c.AddEntry(plotListDiscr3[flavour],legend2[flavour],"l")
#
#	leg3c.Draw()
#	Plots_discr3.SaveAs("CSVSL_discriminator.png")
 


