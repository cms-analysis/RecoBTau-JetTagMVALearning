import FWCore.ParameterSet.Config as cms

process = cms.Process("harvesting")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
#process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EDMtoMEAtRunEnd_cff')
process.load('Configuration.StandardSequences.Harvesting_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.Geometry.GeometryExtended2023_cff')
process.load('Configuration.Geometry.GeometryExtended2023Reco_cff')

process.MessageLogger.cerr.threshold = 'ERROR'

# for the conditions
from Configuration.AlCa.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.GlobalTag.globaltag = "DES19_62_V8::All"

# Open and read list file
#filename = open('RootFiles/list.list', 'r')
#filelist = cms.untracked.vstring( filename.readlines() )

# Input source
process.source = cms.Source("PoolSource",
  #fileNames = filelist,
  fileNames = cms.untracked.vstring(),
  secondaryFileNames = cms.untracked.vstring(),
  processingMode = cms.untracked.string('RunsAndLumis')
)


process.options = cms.untracked.PSet(
  Rethrow = cms.untracked.vstring('ProductNotFound'),
  fileMode = cms.untracked.string('FULLMERGE')
)

from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")


###############################################################################################

from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4)

process.CustombTagValidation = process.bTagValidation.clone(
    tagConfig = cms.VPSet(
cms.PSet(
            bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("trackCountingHighEffBJetTags"),
            folder = cms.string("TCHE")
        ),
        cms.PSet(
            bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("trackCountingHighPurBJetTags"),
            folder = cms.string("TCHP")
        ),
        cms.PSet(
            bTagProbabilityAnalysisBlock,
            label = cms.InputTag("jetProbabilityBJetTags"),
            folder = cms.string("JP")
        ),
        cms.PSet(
            bTagBProbabilityAnalysisBlock,
            label = cms.InputTag("jetBProbabilityBJetTags"),
            folder = cms.string("JBP")
        ),
        cms.PSet(
            bTagSimpleSVAnalysisBlock,
            label = cms.InputTag("simpleSecondaryVertexHighEffBJetTags"),
            folder = cms.string("SSVHE")
        ),
        cms.PSet(
            bTagSimpleSVAnalysisBlock,
            label = cms.InputTag("simpleSecondaryVertexHighPurBJetTags"),
            folder = cms.string("SSVHP")
        ),
# cms.PSet(
# parameters = cms.PSet(
# discriminatorStart = cms.double(-0.1),
# discriminatorEnd = cms.double(1.05),
# nBinEffPur = cms.int32(200),
# # the constant b-efficiency for the differential plots versus pt and eta
# effBConst = cms.double(0.5),
# endEffPur = cms.double(1.005),
# startEffPur = cms.double(-0.005)
# ),
# label = cms.InputTag("combinedSecondaryVertexBJetTags"),
# folder = cms.string("oldCSV") # standard CSV for 7 TeV data taking
# ),
# cms.PSet(
# parameters = cms.PSet(
# discriminatorStart = cms.double(-0.1),
# discriminatorEnd = cms.double(1.05),
# nBinEffPur = cms.int32(200),
# # the constant b-efficiency for the differential plots versus pt and eta
# effBConst = cms.double(0.5),
# endEffPur = cms.double(1.005),
# startEffPur = cms.double(-0.005)
# ),
# label = cms.InputTag("combinedSecondaryVertexV2BJetTags"),
# folder = cms.string("CSVV2") # MLP-based CSV
# ),
# cms.PSet(
# parameters = cms.PSet(
# discriminatorStart = cms.double(-0.1),
# discriminatorEnd = cms.double(1.05),
# nBinEffPur = cms.int32(200),
# # the constant b-efficiency for the differential plots versus pt and eta
# effBConst = cms.double(0.5),
# endEffPur = cms.double(1.005),
# startEffPur = cms.double(-0.005)
# ),
# label = cms.InputTag("combinedSecondaryVertexIVFBJetTags"),
# folder = cms.string("oldCSVIVF") # standard CSV+IVF for 7 TeV data taking
# ),

##############
        cms.PSet(
parameters = cms.PSet(
         discriminatorStart = cms.double(-0.1),
         discriminatorEnd = cms.double(1.05),
         nBinEffPur = cms.int32(200),
         # the constant b-efficiency for the differential plots versus pt and eta
         effBConst = cms.double(0.5),
         endEffPur = cms.double(1.005),
         startEffPur = cms.double(-0.005)
     ),
            label = cms.InputTag("combinedSecondaryVertexIVFV2BJetTags"),
            folder = cms.string("CSVIVFV2") # MLP+IVF-based CSV

        ),
	
    ),
       finalizePlots = True,
        finalizeOnly = True
)

process.dqmEnv.subSystemFolder = 'BTAG'
process.dqmSaver.producer = 'DQM'
process.dqmSaver.workflow = '/POG/BTAG/CSVV2'
process.dqmSaver.convention = 'Offline'
process.dqmSaver.saveByRun = cms.untracked.int32(-1)
process.dqmSaver.saveAtJobEnd =cms.untracked.bool(True)
process.dqmSaver.forceRunNumber = cms.untracked.int32(1)

# Path and EndPath definitions
process.edmtome_step = cms.Path(process.EDMtoME)
process.bTagValidation_step = cms.Path(process.CustombTagValidation)
process.dqmsave_step = cms.Path(process.DQMSaver)

# Schedule definition
process.schedule = cms.Schedule(
  process.edmtome_step,
  process.bTagValidation_step,
  process.dqmsave_step
)

process.PoolSource.fileNames = [
#'/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_100_1_DLU.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_100_1_nEk.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_101_1_TMv.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_10_1_5Vn.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_102_1_2wg.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_103_1_FvJ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_104_1_rGm.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_105_1_Z43.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_106_1_LBv.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_107_1_H1h.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_108_1_r1J.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_109_1_tUY.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_110_1_ocV.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_111_1_DeK.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_111_1_Z45.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_11_1_y9b.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_112_1_aip.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_113_1_tSJ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_114_1_eng.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_115_1_ncf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_116_1_Mbm.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_117_1_ZeS.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_118_1_PSp.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_119_1_h9A.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_1_1_QLL.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_120_1_QNB.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_121_1_0NO.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_12_1_C45.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_122_1_MIy.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_123_1_7S4.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_124_1_Tjm.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_125_1_0hg.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_126_1_y2s.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_127_1_AsM.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_128_1_kip.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_129_1_7nr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_130_1_0yF.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_131_1_Szi.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_13_1_8uI.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_132_1_bMW.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_133_1_U8W.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_134_1_XUi.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_135_1_e5T.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_136_1_MHH.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_137_1_B2W.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_138_1_gh0.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_139_1_F46.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_140_1_0hK.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_141_1_f1z.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_14_1_C8a.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_142_1_9mg.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_143_1_Pad.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_144_1_YvR.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_145_1_uvu.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_146_1_LT2.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_147_1_ICb.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_148_1_8SO.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_149_1_rMW.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_150_1_CMZ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_151_1_Un9.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_15_1_XBr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_152_1_74p.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_153_1_abx.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_154_1_Y0X.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_155_1_LWT.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_156_1_bID.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_157_1_W7b.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_158_1_Ymp.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_159_1_oSc.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_160_1_WgC.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_161_1_vuw.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_16_1_8WE.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_162_1_L55.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_163_1_eDi.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_164_1_p1y.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_165_1_0gG.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_166_1_f50.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_167_1_J6t.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_168_1_mUr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_169_1_VK6.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_170_1_5kI.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_171_1_ZKE.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_17_1_SfE.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_172_1_vYf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_173_1_tnu.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_174_1_d3T.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_175_1_knz.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_176_1_ce3.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_177_1_MoN.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_178_1_E8b.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_179_1_Unn.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_180_1_6qb.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_181_1_R47.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_18_1_nrX.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_182_1_g38.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_183_1_Bsd.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_184_1_2Dm.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_185_1_QaP.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_186_1_FqW.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_187_1_uFh.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_188_1_tu9.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_189_1_ad1.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_190_1_HNa.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_191_1_oMc.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_19_1_Kb4.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_192_1_uLH.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_193_1_P75.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_194_1_ib0.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_195_1_hfl.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_196_1_4ow.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_197_1_LlL.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_198_1_A7a.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_199_1_p43.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_200_1_FQF.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_201_1_NjX.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_20_1_num.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_202_1_iKl.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_203_1_jew.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_204_1_kQr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_205_1_13s.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_206_1_Ppa.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_207_1_RUl.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_208_1_oTl.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_209_1_gWe.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_210_1_yBg.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_211_1_4si.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_21_1_k9n.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_212_1_UTw.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_213_1_ZTb.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_214_1_2iZ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_215_1_xaM.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_216_1_gVK.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_217_1_Xot.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_218_1_J0F.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_219_1_cUo.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_2_1_BZV.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_220_1_6Om.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_221_1_3U3.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_22_1_IWU.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_222_1_AQI.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_223_1_Rvv.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_224_1_XjM.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_225_1_g9w.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_226_1_Vki.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_227_1_OBc.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_228_1_iWr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_229_1_3g6.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_230_1_wkS.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_231_1_1tJ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_23_1_ogR.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_232_1_DPl.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_233_1_HLQ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_234_1_iDI.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_235_1_vza.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_236_1_VxF.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_237_1_fto.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_238_1_RY3.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_239_1_kWR.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_240_1_LrT.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_241_1_rm5.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_24_1_89i.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_242_1_j2v.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_243_1_Fam.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_244_1_VtU.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_245_1_BFx.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_246_1_hCH.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_247_1_N6b.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_248_1_1tN.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_249_1_Phs.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_250_1_QRr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_25_1_KHh.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_26_1_O6m.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_27_1_cXq.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_28_1_JZY.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_29_1_ua1.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_30_1_0u6.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_31_1_CtR.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_3_1_iAG.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_32_1_yjV.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_33_1_3AS.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_34_1_bzC.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_35_1_Wu9.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_36_1_3kC.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_37_1_DE4.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_38_1_N7h.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_39_1_xsd.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_40_1_9C4.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_41_1_0EB.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_4_1_uMM.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_42_1_N0A.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_43_1_YMV.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_44_1_mtr.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_45_1_ZUP.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_46_1_fAq.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_47_1_FvF.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_48_1_BRh.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_49_1_pTt.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_50_1_zk6.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_51_1_Nt9.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_5_1_7lT.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_52_1_s8p.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_53_1_GFg.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_54_1_9lA.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_55_1_de6.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_56_1_nkf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_57_1_nml.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_58_1_26M.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_59_1_pVh.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_60_1_GUe.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_61_1_a9v.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_6_1_zmT.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_62_1_8f8.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_63_1_Fkj.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_64_1_lBV.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_65_1_1wH.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_66_1_ApM.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_67_1_dmf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_68_1_MU2.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_69_1_sdU.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_70_1_ghb.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_71_1_M82.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_7_1_Ix3.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_72_1_gUQ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_73_1_HQL.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_74_1_2b9.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_75_1_46J.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_76_1_O2N.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_77_1_8OZ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_78_1_fTs.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_79_1_dj0.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_80_1_S0B.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_81_1_8Se.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_8_1_uxv.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_82_1_RZ7.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_82_1_vq4.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_83_1_jFO.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_83_1_u91.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_84_1_B2H.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_84_1_Eyf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_85_1_MW0.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_86_1_5xS.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_87_1_M3E.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_88_1_sdB.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_89_1_uUP.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_90_1_CJf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_90_1_NqA.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_91_1_vHn.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_9_1_fEJ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_92_1_USp.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_93_1_WfQ.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_94_1_dGC.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_95_1_XE2.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_96_1_3in.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_97_1_yYY.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_98_1_Gdf.root', '/store/user/pvmulder/BtagValidation_53X/CSVLR_pregitrecipe//DQMfile_99_1_TQc.root'
 'file:DQMfile.root']
