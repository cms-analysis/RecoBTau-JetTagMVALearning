import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")

process.load('Configuration.Geometry.GeometryExtended2023_cff')
process.load('Configuration.Geometry.GeometryExtended2023Reco_cff')

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
#process.GlobalTag.globaltag = "START53_V26::All"
process.GlobalTag.globaltag = "DES19_62_V8::All"

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
                tag = cms.string('MVAJetTags_CMSSW_6_2_0_SLHC13')
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

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = cms.InputTag("ak5PFJets")
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
process.inclusiveSecondaryVertexFinderTagInfos.trackSelection.qualityClass = cms.string('any')
process.inclusiveVertexFinder.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")
process.trackVertexArbitrator.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")
process.softPFMuonsTagInfos.jets = cms.InputTag("ak5PFJets")
process.softPFElectronsTagInfos.jets = cms.InputTag("ak5PFJets")

# taginfos
process.taginfos = cms.Sequence(
process.impactParameterTagInfos *
process.secondaryVertexTagInfos *
process.inclusiveVertexing *
###process.inclusiveMergedVerticesFiltered *
###process.bToCharmDecayVertexMerged *
process.inclusiveSecondaryVertexFinderTagInfos * # IVF
#inclusiveSecondaryVertexFinderFilteredTagInfos * # IVF with B->D merging
process.softPFMuonsTagInfos *
process.softPFElectronsTagInfos
)

# IP-based taggers
process.IPbtaggers = cms.Sequence(
trackCountingHighEffBJetTags * trackCountingHighPurBJetTags * jetProbabilityBJetTags * jetBProbabilityBJetTags
)

# SV-based taggers
process.SVbtaggers = cms.Sequence(
simpleSecondaryVertexHighEffBJetTags * simpleSecondaryVertexHighPurBJetTags
)

process.combinedSecondaryVertex.trackSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertex.trackPseudoSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertex.trackMultiplicityMin = cms.uint32(2)

# CSVV2: MLP-based
process.combinedSecondaryVertexV2.calibrationRecords = cms.vstring(
'CombinedSVIVFV2RecoVertex', # To be replaced with dedicated CSVV2 training (including trackJetPt variable)
'CombinedSVIVFV2PseudoVertex',
'CombinedSVIVFV2NoVertex'
)
process.combinedSecondaryVertexV2.trackSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexV2.trackPseudoSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexV2.trackMultiplicityMin = cms.uint32(2)


# combined IP+SV or IP+SV+SL taggers
process.Combinedbtaggers = cms.Sequence(
process.combinedSecondaryVertexBJetTags * process.combinedSecondaryVertexV2BJetTags
)

# CSVIVF
process.combinedSecondaryVertexIVF=process.combinedSecondaryVertex.clone(
calibrationRecords = cms.vstring(
'CombinedSVRecoVertex', # no dedicated IVF training exists
'CombinedSVPseudoVertex',
'CombinedSVNoVertex'
)
)
process.combinedSecondaryVertexIVFBJetTags = process.combinedSecondaryVertexBJetTags.clone(
jetTagComputer = cms.string('combinedSecondaryVertexIVF'),
tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"),
cms.InputTag("inclusiveSecondaryVertexFinderTagInfos")) #inclusiveSecondaryVertexFinderFilteredTagInfos
)
process.combinedSecondaryVertexIVF.trackSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexIVF.trackPseudoSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexIVF.trackMultiplicityMin = cms.uint32(2)

# CSVIVFV2: MLP-based
process.combinedSecondaryVertexIVFV2=process.combinedSecondaryVertexV2.clone(
calibrationRecords = cms.vstring(
#'CombinedSVIVFV2RecoVertex',
#'CombinedSVIVFV2PseudoVertex',
#'CombinedSVIVFV2NoVertex'
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


# combined IP+IVF or IP+IVF+SL taggers
process.CombinedIVFbtaggers = cms.Sequence(
#process.combinedSecondaryVertexIVFBJetTags *
process.combinedSecondaryVertexIVFV2BJetTags
)

#do the matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
process.jetFlavourInfosAK5PFJets.jets = cms.InputTag("ak5PFJets")

#standard validation tools
from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")


from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
#process.bTagCommonBlock.ptRecJetMin = cms.double(600.0)
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4)
process.bTagValidation.jetMCSrc = 'jetFlavourInfosAK5PFJets'
process.bTagValidation.genJetsMatched = 'matchedAK5PFGenJets'
process.bTagValidation.doPUid = True
process.bTagValidation.allHistograms = True
#process.bTagValidation.fastMC = True

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

####
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
      finalizePlots = False,
      finalizeOnly = False
)



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
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
process.IPbtaggers *
process.SVbtaggers *
#process.Combinedbtaggers *
process.CombinedIVFbtaggers *
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
#'/store/mc/GEM2019Upg14DR/QCD_Pt_15to500_Tune4C_FlatPtEta_14TeV_pythia8/AODSIM/PU50bx25_DES19_62_V8-v1/00000/187ADA13-53DD-E311-951F-003048FFD7BE.root',
 # '/store/mc/GEM2019Upg14DR/QCD_BBbar_Pt_15to500_Tune4C_FlatPtEta_14TeV_pythia8/AODSIM/PU50bx25_DES19_62_V8-v1/00000/083D4CB9-57DC-E311-AB86-0025905A6094.root'
 'root://xrootd.unl.edu//store/mc/GEM2019Upg14DR/QCD_BBbar_Pt_15to500_Tune4C_FlatPtEta_14TeV_pythia8/AODSIM/PU50bx25_DES19_62_V8-v1/00000/083D4CB9-57DC-E311-AB86-0025905A6094.root'	]
