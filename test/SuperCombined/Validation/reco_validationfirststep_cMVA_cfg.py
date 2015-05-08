import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.threshold = 'ERROR'

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff") 
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("MCRUN2_74_V7::All") #contains latest-greatest CSVv2+IVF training

#DB FILE WITH ALL RECORDS +  NEW cMVA RECORD!!!
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
	process.CondDBSetup,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
                tag = cms.string('MVAJetTags')
	)),
	connect = cms.string("sqlite_file:MVAJetTags_newCMVA.db"), 
	#connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)
process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")


# DQM include
process.load("Configuration.EventContent.EventContent_cff")
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')



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

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak4JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = cms.InputTag("ak4PFJetsCHS") 
                                                  )
#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak4JetTracksAssociatorAtVertex")

#select good primary vertex
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

#for Inclusive Vertex Finder
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
process.load('RecoBTag/SecondaryVertex/inclusiveSecondaryVertexFinderTagInfos_cfi')
process.inclusiveVertexFinder.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")
process.trackVertexArbitrator.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")


#input for softLeptonTagInfos
from RecoBTag.SoftLepton.softPFElectronTagInfos_cfi import *
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag('goodOfflinePrimaryVertices')
process.softPFElectronsTagInfos.jets = cms.InputTag("ak4PFJetsCHS")
process.softPFElectronsTagInfos.useMCpromptElectronFilter = cms.bool(True) ###to implement
from RecoBTag.SoftLepton.softPFMuonTagInfos_cfi import *
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag('goodOfflinePrimaryVertices')
process.softPFMuonsTagInfos.jets = cms.InputTag("ak4PFJetsCHS")
process.softPFMuonsTagInfos.useMCpromptMuonFilter = cms.bool(True) ###to implement


# for the PU ID
# Select GenJets with Pt>8 GeV
process.ak4GenJetsMCPUJetID = cms.EDFilter("GenJetSelector",
    src    = cms.InputTag("ak4GenJets"),
    cut    = cms.string('pt > 8.0'),
    filter = cms.bool(False)             # in case no GenJets pass the selection, do not filter events, just produce an empty GenJet collection
)

# Match selected GenJets to RecoJets
process.ak4PFJetsGenJetMatchMCPUJetID = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR
    src                   = cms.InputTag("ak4PFJetsCHS"),           # RECO jets (any View<Jet> is ok)
    matched               = cms.InputTag("ak4GenJetsMCPUJetID"), # GEN jets  (must be GenJetCollection)
    mcPdgId               = cms.vint32(),                        # N/A
    mcStatus              = cms.vint32(),                        # N/A
    checkCharge           = cms.bool(False),                     # N/A
    maxDeltaR             = cms.double(0.25),                    # Minimum deltaR for the match
    resolveAmbiguities    = cms.bool(True),                      # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(False),
)

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK4PFJetsMCFlavourInfos_cfi import ak4JetFlavourInfos
process.jetFlavourInfosAK4PFJets = ak4JetFlavourInfos.clone()
process.jetFlavourInfosAK4PFJets.jets = cms.InputTag("ak4PFJetsCHS")

from RecoBTag.Configuration.RecoBTag_cff import *

process.combinedMVAComputer.jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('jetProbabilityComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('combinedSecondaryVertexV2Computer') #default is combinedSecondaryVertexComputer
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuonComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectronComputer')
		)
)
process.candidateCombinedMVAComputer.jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('candidateJetProbabilityComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('candidateCombinedSecondaryVertexV2Computer') #default is candidateCombinedSecondaryVertexComputer
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuonComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectronComputer')
		)
)

process.combinedMVAComputerNEW = combinedMVAComputer.clone(
	calibrationRecord = cms.string('CombinedMVAnew'), 
	jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('jetProbabilityComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('combinedSecondaryVertexV2Computer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuonComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectronComputer')
		)
	)
)
process.combinedMVABJetTagsNEW = combinedMVABJetTags.clone(
	jetTagComputer = cms.string('combinedMVAComputerNEW')
)
process.candidateCombinedMVAComputerNEW = candidateCombinedMVAComputer.clone(
	calibrationRecord = cms.string('CombinedMVAnew'), 
	jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('candidateJetProbabilityComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('candidateCombinedSecondaryVertexV2Computer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuonComputer')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectronComputer')
		)
	)
)
process.pfCombinedMVABJetTagsNEW =pfCombinedMVABJetTags.clone(
	jetTagComputer = cms.string('candidateCombinedMVAComputerNEW')
)

#standard validation tools
from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")

from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
process.bTagValidation.jetMCSrc = 'jetFlavourInfosAK4PFJets'
process.bTagValidation.genJetsMatched = 'ak4PFJetsGenJetMatchMCPUJetID'
#process.bTagValidation.allHistograms = True 
#process.bTagValidation.fastMC = True
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4)
process.bTagValidation.doPUid = cms.bool(True)
#process.bTagValidation.doJEC = cms.bool(False)
process.bTagValidation.flavPlots = cms.string("alldusg")

process.bTagValidation.tagConfig += cms.VPSet(
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("combinedInclusiveSecondaryVertexV2BJetTags"),
            folder = cms.string("CSVv2_tkOnly")
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("pfCombinedSecondaryVertexSoftLeptonBJetTags"),
            folder = cms.string("CSVSL")
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("ghostTrackBJetTags"), #no PF version available at the moment
            folder = cms.string("GT")
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("combinedMVABJetTags"),
            folder = cms.string("cMVA_tkOnly")
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("pfCombinedMVABJetTags"),
            folder = cms.string("cMVA")
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("combinedMVABJetTagsNEW"),
            folder = cms.string("cMVA_new_tkOnly")
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("pfCombinedMVABJetTagsNEW"),
            folder = cms.string("cMVA_new")
		),
	)
	
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)


process.btagDQM = cms.Path(
process.ak4GenJetsMCPUJetID *
process.ak4PFJetsGenJetMatchMCPUJetID *
process.goodOfflinePrimaryVertices * 
process.inclusiveVertexing * 
#process.inclusiveMergedVerticesFiltered * 
#process.bToCharmDecayVertexMerged * 
process.myak4JetTracksAssociatorAtVertex * 
process.impactParameterTagInfos * 
process.inclusiveSecondaryVertexFinderTagInfos *
process.softPFMuonsTagInfos *
process.softPFElectronsTagInfos *
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK4PFJets *
btagging * 											#rerun all taggers (legacy and pf-based)
process.combinedMVABJetTagsNEW * 				
process.pfCombinedMVABJetTagsNEW *
process.bTagValidation
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
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/000470E0-3B75-E411-8B90-00266CFFA604.root'
]
