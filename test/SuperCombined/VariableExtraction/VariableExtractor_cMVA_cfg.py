import FWCore.ParameterSet.Config as cms

process = cms.Process("CSVTrainer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

#process.load("RecoBTau.JetTagComputer.jetTagRecord_cfi")


# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff") 
process.load("Configuration.StandardSequences.GeometryRecoDB_cff") 
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
#process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

process.GlobalTag.globaltag = cms.string("MCRUN2_74_V7::All") #contains latest-greatest CSVv2+IVF training

#To use the newest training!
#process.load("CondCore.DBCommon.CondDBSetup_cfi")
#process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
#       process.CondDBSetup,
#       timetype = cms.string('runnumber'),
#       toGet = cms.VPSet(cms.PSet(
#               record = cms.string('BTauGenericMVAJetTagComputerRcd'),
#               tag = cms.string('MVAJetTags')
#       )),
#       connect = cms.string("sqlite_file:MVAJetTags_CSVV2dev.db"), #use CSVv2 from GT!!!
#       #connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
#       BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
#)
#process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")

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

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
)

process.source = cms.Source("PoolSource",
	skipEvents=cms.untracked.uint32(0),
	fileNames = cms.untracked.vstring(
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/000470E0-3B75-E411-8B90-00266CFFA604.root'
	)
)

# to write out events
#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('outfile.root')
#)

# write out file
#process.output = cms.EndPath(
#  process.out
#)


process.superCombinedTrainer = cms.EDAnalyzer("JetTagMVAExtractor",
	variables = cms.untracked.VPSet( cms.untracked.PSet(
		label = cms.untracked.string("combinedMVA"),  
		variables=cms.untracked.vstring("jetPt","jetEta","algoDiscriminator")
	)),

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
             jetTagComputer = cms.string('softPFMuonComputer') #check
         ),
         cms.PSet(
             discriminator = cms.bool(True),
             variables = cms.bool(False),
             jetTagComputer = cms.string('softPFElectronComputer') #check
         )
 ),
	
  ipTagInfos = cms.InputTag("impactParameterTagInfos"),
  svTagInfos = cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
	smTagInfos = cms.InputTag("softPFMuonsTagInfos"),
	seTagInfos = cms.InputTag("softPFElectronsTagInfos"),
	useCategories = cms.bool(False),
  calibrationRecord = cms.string('combinedMVA'),
	minimumTransverseMomentum = cms.double(20.0),
	maximumTransverseMomentum = cms.double(9999999.),
	minimumPseudoRapidity = cms.double(0.0),
	maximumPseudoRapidity = cms.double(2.4),
	signalFlavours = cms.vint32(5, 7),
	jetTagComputer = cms.string('combinedMVAComputer'),
	jetFlavourMatching = cms.InputTag("jetFlavourInfosAK4PFJets"),
	matchedGenJets = cms.InputTag("ak4PFJetsGenJetMatchMCPUJetID"),
	ignoreFlavours = cms.vint32(0)
)


process.p = cms.Path(
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
process.superCombinedTrainer 
)


 
