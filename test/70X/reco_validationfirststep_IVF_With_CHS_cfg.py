import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = "POSTLS170_V6::All"

# DQM include
process.load("Configuration.EventContent.EventContent_cff")
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.MessageLogger.cerr.threshold = 'ERROR'

process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
	process.CondDBSetup,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
                tag = cms.string('MVAJetTags')
	)),
	connect = cms.string("sqlite_file:MVAJetTags.db"),
	#connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)
process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")

# write DQM file
process.DQMoutput = cms.OutputModule("PoolOutputModule",
  splitLevel = cms.untracked.int32(0),
  outputCommands = process.DQMEventContent.outputCommands,
  fileName = cms.untracked.string('DQMfile.root'),
  #fileName = cms.untracked.string('DQMfile.root'),
  dataset = cms.untracked.PSet(
    filterName = cms.untracked.string(''),
    dataTier = cms.untracked.string('')
  )
)


from PhysicsTools.JetMCAlgos.AK5PFJetsMCPUJetID_cff import *
process.selectedAK5PFGenJets = ak5GenJetsMCPUJetID.clone()
process.matchedAK5PFGenJets = ak5PFJetsGenJetMatchMCPUJetID.clone()
process.matchedAK5PFGenJets.matched = cms.InputTag("selectedAK5PFGenJets")
process.matchedAK5PFGenJets.src = cms.InputTag("ak5PFJetsCHS")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = cms.InputTag("ak5PFJetsCHS")
                                                  )

#select good primary vertex
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )


from RecoBTag.Configuration.RecoBTag_cff import *

#for Inclusive Vertex Finder
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')

#new input for impactParameterTagInfos, softleptons, IVF
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")
process.impactParameterTagInfos.primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")
process.secondaryVertexTagInfos.trackSelection.qualityClass = cms.string('any')
process.secondaryVertexTagInfosV2.trackSelection.qualityClass = cms.string('any')
process.inclusiveSecondaryVertexFinderTagInfos.trackSelection.qualityClass = cms.string('any')
process.inclusiveVertexFinder.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")
process.trackVertexArbitrator.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")
process.softPFMuonsTagInfos.jets = cms.InputTag("ak5PFJetsCHS")
process.softPFElectronsTagInfos.jets = cms.InputTag("ak5PFJetsCHS") 

# taginfos
process.taginfos = cms.Sequence(
process.impactParameterTagInfos *
process.secondaryVertexTagInfos * 
process.secondaryVertexTagInfosV2 * 
process.inclusiveVertexing * 
###process.inclusiveMergedVerticesFiltered *   
###process.bToCharmDecayVertexMerged *  
process.inclusiveSecondaryVertexFinderTagInfos * # IVF
#inclusiveSecondaryVertexFinderFilteredTagInfos * # IVF with B->D merging 
process.softPFMuonsTagInfos *
process.softPFElectronsTagInfos 
)

## IP-based taggers
#process.IPbtaggers = cms.Sequence(
#trackCountingHighEffBJetTags * trackCountingHighPurBJetTags * jetProbabilityBJetTags * jetBProbabilityBJetTags
#)
#
## SV-based taggers
#process.SVbtaggers = cms.Sequence(
#simpleSecondaryVertexHighEffBJetTags * simpleSecondaryVertexHighPurBJetTags
#)
#
#process.combinedSecondaryVertex.trackSelection.qualityClass = cms.string('any')
#process.combinedSecondaryVertex.trackPseudoSelection.qualityClass = cms.string('any')
#process.combinedSecondaryVertex.trackMultiplicityMin = cms.uint32(2)

# CSVV2: MLP-based
process.combinedSecondaryVertexV2.calibrationRecords = cms.vstring(
		'CombinedSVV2RecoVertex',   # To be replaced with dedicated CSVV2 training (including trackJetPt variable)
		'CombinedSVV2PseudoVertex',
		'CombinedSVV2NoVertex'
)
process.combinedSecondaryVertexV2.trackSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexV2.trackPseudoSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexV2.trackMultiplicityMin = cms.uint32(2)


## combined IP+SV or IP+SV+SL taggers
#process.Combinedbtaggers = cms.Sequence(
#process.combinedSecondaryVertexBJetTags * process.combinedSecondaryVertexV2BJetTags 
#)
#
## CSVIVF
#process.combinedSecondaryVertexIVF=process.combinedSecondaryVertex.clone(
#	calibrationRecords = cms.vstring(
#		'CombinedSVRecoVertex', # no dedicated IVF training exists
#		'CombinedSVPseudoVertex',
#		'CombinedSVNoVertex'
#	)
#)
#process.combinedSecondaryVertexIVFBJetTags = process.combinedSecondaryVertexBJetTags.clone(
#	jetTagComputer = cms.string('combinedSecondaryVertexIVF'),
#	tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"),
#	                         cms.InputTag("inclusiveSecondaryVertexFinderTagInfos")) #inclusiveSecondaryVertexFinderFilteredTagInfos
#)
#process.combinedSecondaryVertexIVF.trackSelection.qualityClass = cms.string('any')
#process.combinedSecondaryVertexIVF.trackPseudoSelection.qualityClass = cms.string('any')
#process.combinedSecondaryVertexIVF.trackMultiplicityMin = cms.uint32(2)

# CSVIVFV2: MLP-based
process.combinedSecondaryVertexIVFV2=process.combinedSecondaryVertexV2.clone(
	calibrationRecords = cms.vstring(
		'CombinedSVV2RecoVertex', 
		'CombinedSVV2PseudoVertex',
		'CombinedSVV2NoVertex'
	)
)
process.combinedSecondaryVertexIVFV2BJetTags = process.combinedSecondaryVertexV2BJetTags.clone(
	jetTagComputer = cms.string('combinedSecondaryVertexIVFV2'),
	tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"),
	                         cms.InputTag("inclusiveSecondaryVertexFinderTagInfos")) #inclusiveSecondaryVertexFinderFilteredTagInfos
)
process.combinedSecondaryVertexIVFV2.trackSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexIVFV2.trackPseudoSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexIVFV2.trackMultiplicityMin = cms.uint32(2)

#
## combined IP+IVF or IP+IVF+SL taggers
#process.CombinedIVFbtaggers = cms.Sequence(
#process.combinedSecondaryVertexIVFBJetTags * process.combinedSecondaryVertexIVFV2BJetTags 
#)

#do the matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
process.jetFlavourInfosAK5PFJets.jets = cms.InputTag("ak5PFJetsCHS")

#standard validation tools
from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")
#process.bTagCommonBlock.ptRecJetMin = cms.double(600.0)

from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
process.bTagValidation.jetMCSrc = 'jetFlavourInfosAK5PFJets'
process.bTagValidation.genJetsMatched = 'matchedAK5PFGenJets'
process.bTagValidation.allHistograms = True 
#process.bTagValidation.fastMC = True
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4)
process.bTagValidation.doPUid = cms.bool(True)
process.bTagValidation.flavPlots = cms.string("alldusg")

process.CustombTagValidation = process.bTagValidation.clone(
    tagConfig = cms.VPSet(
#				cms.PSet(
#            bTagTrackCountingAnalysisBlock,
#            label = cms.InputTag("trackCountingHighEffBJetTags"),
#            folder = cms.string("TCHE")
#        ), 
#        cms.PSet(
#            bTagTrackCountingAnalysisBlock,
#            label = cms.InputTag("trackCountingHighPurBJetTags"),
#            folder = cms.string("TCHP")
#        ), 
#        cms.PSet(
#            bTagProbabilityAnalysisBlock,
#            label = cms.InputTag("jetProbabilityBJetTags"),
#            folder = cms.string("JP")
#        ), 
#        cms.PSet(
#            bTagBProbabilityAnalysisBlock,
#            label = cms.InputTag("jetBProbabilityBJetTags"),
#            folder = cms.string("JBP")
#        ), 
#        cms.PSet(
#            bTagSimpleSVAnalysisBlock,
#            label = cms.InputTag("simpleSecondaryVertexHighEffBJetTags"),
#            folder = cms.string("SSVHE")
#        ), 
#        cms.PSet(
#            bTagSimpleSVAnalysisBlock,
#            label = cms.InputTag("simpleSecondaryVertexHighPurBJetTags"),
#            folder = cms.string("SSVHP")
#        ), 
#        cms.PSet(
#				    parameters = cms.PSet(
#        			discriminatorStart = cms.double(-0.1),
#        			discriminatorEnd = cms.double(1.05),
#        			nBinEffPur = cms.int32(200),
#        			# the constant b-efficiency for the differential plots versus pt and eta
#        			effBConst = cms.double(0.5),
#        			endEffPur = cms.double(1.005),
#        			startEffPur = cms.double(-0.005)
#    				),
#            label = cms.InputTag("combinedSecondaryVertexBJetTags"),
#            folder = cms.string("oldCSV") # standard CSV for 7 TeV data taking
#        ), 
#        cms.PSet(
#				    parameters = cms.PSet(
#        			discriminatorStart = cms.double(-0.1),
#        			discriminatorEnd = cms.double(1.05),
#        			nBinEffPur = cms.int32(200),
#        			# the constant b-efficiency for the differential plots versus pt and eta
#        			effBConst = cms.double(0.5),
#        			endEffPur = cms.double(1.005),
#        			startEffPur = cms.double(-0.005)
#    				),
#            label = cms.InputTag("combinedSecondaryVertexV2BJetTags"),
#            folder = cms.string("CSVV2") # MLP-based CSV
#        ),
#        cms.PSet(
#				    parameters = cms.PSet(
#        			discriminatorStart = cms.double(-0.1),
#        			discriminatorEnd = cms.double(1.05),
#        			nBinEffPur = cms.int32(200),
#        			# the constant b-efficiency for the differential plots versus pt and eta
#        			effBConst = cms.double(0.5),
#        			endEffPur = cms.double(1.005),
#        			startEffPur = cms.double(-0.005)
#    				),
#            label = cms.InputTag("combinedSecondaryVertexIVFBJetTags"),
#            folder = cms.string("oldCSVIVF") # standard CSV+IVF for 7 TeV data taking
#        ), 
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
            			bTagCombinedSVAnalysisBlock,
            			type = cms.string('GenericMVA'),
            			ipTagInfos = cms.InputTag("impactParameterTagInfos"),
            			svTagInfos = cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
            label = cms.InputTag("combinedSecondaryVertexIVFV2"),
            folder = cms.string("CSVIVFV2Tag")
       ),
			),
      finalizePlots = False,
      finalizeOnly = False
)



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(101)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)


process.btagDQM = cms.Path(
process.selectedAK5PFGenJets *
process.matchedAK5PFGenJets *
process.goodOfflinePrimaryVertices * 
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK5PFJets *
process.myak5JetTracksAssociatorAtVertex *
process.taginfos *
#process.IPbtaggers *
#process.SVbtaggers *
#process.Combinedbtaggers * 
#process.CombinedIVFbtaggers *
process.combinedSecondaryVertexV2BJetTags *
process.combinedSecondaryVertexIVFV2BJetTags *
process.CustombTagValidation
)

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(
  process.btagDQM,
  process.endjob_step,
  process.DQMoutput_step
)

process.PoolSource.fileNames = [
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FED775BD-B8E1-E111-8ED5-003048C69036.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/001C868B-B2E1-E111-9BE3-003048D4DCD8.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/56EA7074-7EE1-E111-9540-003048D436FE.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/ACCEC445-28E2-E111-8950-003048C692CA.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0046E17E-BCE1-E111-A1D1-003048F02CB2.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/56F8C2F9-DEE1-E111-9A0D-0030487D5E4B.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/ACD1193E-D8E1-E111-B834-0030487F1797.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0076C8E3-9AE1-E111-917C-003048D439AA.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/581BEC0C-92E1-E111-8C02-003048C692C0.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AE17F607-CCE1-E111-B2BB-002481E0D2EA.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0244AEA1-7CE1-E111-956B-0025901D4C3C.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/583CFC88-2FE2-E111-B04A-0030487F1BD5.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AE3D8060-E6E1-E111-BE25-003048F0E18E.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/024A37B1-C9E1-E111-9CDF-0025901D4B04.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/588C32FF-0AE2-E111-A849-0030487D5E49.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AE455D86-8BE1-E111-A27C-003048D438FE.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/027E3BA0-F2E1-E111-AAD3-003048D3CA06.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/58968F79-EDE1-E111-B9B5-003048D4363C.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AE559E1D-94E1-E111-8A5C-003048F0E5A4.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02963472-F6E1-E111-B0F9-0030487D814D.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/5898B1DB-6CE1-E111-86F5-00266CFB8D74.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AE572CE9-96E2-E111-9487-002481E0E912.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02A13705-B0E1-E111-8248-0030487E4EB5.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/58E89052-E9E1-E111-928E-003048D439AC.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AE73FA02-99E1-E111-B3EE-003048C68A98.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02A9D360-C9E1-E111-B4AE-003048D3CA06.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/5AF14FE2-F8E1-E111-8EC9-003048C6903E.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AEBB6623-65E1-E111-9F35-0025904B12FC.root',
#       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02F5A838-8FE1-E111-B0C8-00266CFFA654.root',
'root://xrootd.unl.edu//store/mc/Spring14dr/QCD_Pt-470to600_Tune4C_13TeV_pythia8/AODSIM/castor_PU_S14_POSTLS170_V6-v1/00000/00435352-A3ED-E311-ACA8-0025905A607A.root'
			 ]
