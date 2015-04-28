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

process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
#2023 geometry
process.load('Configuration.Geometry.GeometryExtended2023SHCalNoTaperReco_cff')
process.load('Configuration.Geometry.GeometryExtended2023SHCalNoTaper_cff')

process.MessageLogger.cerr.threshold = 'ERROR'
# for the conditions
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = cms.string("PH2_1K_FB_V6::All")
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
process.bTagValidation.etaMax = cms.double(3.0)
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4, 3.0, 4.0)
process.bTagValidation.flavPlots= 'allbcdusg'

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
	cms.PSet(
             bTagCombinedSVAnalysisBlock,
             type = cms.string('GenericMVA'),
             ipTagInfos = cms.InputTag("impactParameterTagInfos"),
             svTagInfos = cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
            label = cms.InputTag("combinedSecondaryVertexIVFV2"),
            folder = cms.string("CSVIVFV2Tag")
    ),
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
            label = cms.InputTag("combinedSecondaryVertexIVFV2Phase2JECHighPUBJetTags"),
            folder = cms.string("CSVIVFV2Phase2JECHighPU") # Retrained MLP+IVF-based CSV
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
'file:DQMfile.root'
]


