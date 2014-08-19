# The following comments couldn't be translated into the new config version:

#! /bin/env cmsRun

import FWCore.ParameterSet.Config as cms

process = cms.Process("rereco2")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

#process.options = cms.untracked.PSet(multiProcesses=cms.untracked.PSet(
#        maxChildProcesses=cms.untracked.int32(15),
#        maxSequentialEventsPerChild=cms.untracked.uint32(10)))



# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

#parallel processing

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(101)
)
process.source = cms.Source("PoolSource",
#     skipEvents = cms.untracked.uint32(281),	
    fileNames = cms.untracked.vstring(),
    secondaryFileNames = cms.untracked.vstring()
)

process.GlobalTag.globaltag = 'POSTLS170_V6::All'

#process.reco = cms.Sequence(process.siPixelRecHits+process.siStripMatchedRecHits+process.ckftracks_wodEdX+process.offlinePrimaryVertices+process.ak5JetTracksAssociatorAtVertex*process.btagging)

process.siPixelClusters = cms.EDProducer("JetCoreClusterSplitter",
    pixelClusters         = cms.InputTag("siPixelClusters","","RECO"),
    vertices              = cms.InputTag('offlinePrimaryVertices',"","RECO"),
    pixelCPE = cms.string( "PixelCPEGeneric" ),
    verbose     = cms.bool(True),

    )

process.IdealsiPixelClusters = cms.EDProducer(
    "TrackClusterSplitter",
    stripClusters         = cms.InputTag("siStripClusters","","RECO"),
    pixelClusters         = cms.InputTag("siPixelClusters","","RECO"),
    useTrajectories       = cms.bool(False),
    trajTrackAssociations = cms.InputTag('generalTracks'),
    tracks                = cms.InputTag('pixelTracks'),
    propagator            = cms.string('AnalyticalPropagator'),
    vertices              = cms.InputTag('pixelVertices'),
    simSplitPixel         = cms.bool(True), # ideal pixel splitting turned OFF
    simSplitStrip         = cms.bool(False), # ideal strip splitting turned OFF
    tmpSplitPixel         = cms.bool(False), # template pixel spliting
    tmpSplitStrip         = cms.bool(False), # template strip splitting
    useStraightTracks     = cms.bool(True),
    test     = cms.bool(True)
    )

#this is needed if we run off RECO, comment it if you run RECO in this job
process.caloTowerForTrk = process.calotowermaker.clone(hbheInput=cms.InputTag('hbhereco'))

#process.retrack = cms.Sequence(process.IdealsiPixelClusters*process.siPixelClusters*process.MeasurementTrackerEvent+process.siPixelRecHits+process.siStripMatchedRecHits+process.ckftracks_wodEdX+process.offlinePrimaryVertices+process.ak5JetTracksAssociatorAtVertexPF*process.btagging)
process.retrack = cms.Sequence(process.IdealsiPixelClusters*process.siPixelClusters*process.MeasurementTrackerEvent+process.siPixelRecHits+process.siStripMatchedRecHits+process.ckftracks_wodEdX+process.offlinePrimaryVertices)

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

#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")
process.combinedSecondaryVertexV2.trackMultiplicityMin = cms.uint32(2)


#for Inclusive Vertex Finder
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
process.load('RecoBTag/SecondaryVertex/inclusiveSecondaryVertexFinderTagInfos_cfi')

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
process.jetFlavourInfosAK5PFJets.jets = cms.InputTag("ak5PFJets")


process.combinedSVMVATrainer = cms.EDAnalyzer("JetTagMVAExtractor",
	variables = cms.untracked.VPSet(
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVV2RecoVertex"),  variables=cms.untracked.vstring(
"jetPt","trackJetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","flightDistance2dSig","flightDistance3dSig","flightDistance2dVal","flightDistance3dVal","trackSumJetEtRatio","jetNSecondaryVertices","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","vertexFitProb","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVV2PseudoVertex"),  variables=cms.untracked.vstring(
"jetPt","trackJetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),

		cms.untracked.PSet( label = cms.untracked.string("CombinedSVV2NoVertex"),  variables=cms.untracked.vstring(
"jetPt","trackJetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity"
)) # no trackEtaRel!!!???!!!

	),
	ipTagInfos = cms.InputTag("impactParameterTagInfos"),
	#svTagInfos =cms.InputTag("secondaryVertexTagInfos"),
	svTagInfos =cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
	
	minimumTransverseMomentum = cms.double(15.0),
	maximumTransverseMomentum = cms.double(9999999.),
	useCategories = cms.bool(True),
        calibrationRecords = cms.vstring(
                'CombinedSVV2RecoVertex',
                'CombinedSVV2PseudoVertex',
                'CombinedSVV2NoVertex'),
	categoryVariableName = cms.string('vertexCategory'), # vertexCategory = Reco,Pseudo,No
	maximumPseudoRapidity = cms.double(2.5),
	signalFlavours = cms.vint32(5, 7),
	minimumPseudoRapidity = cms.double(0.0),
	jetTagComputer = cms.string('combinedSecondaryVertexV2'),
	jetFlavourMatching = cms.InputTag("jetFlavourInfosAK5PFJets"),
	matchedGenJets = cms.InputTag("matchedAK5PFGenJets"),
	ignoreFlavours = cms.vint32(0)
)

process.p = cms.Path(
process.retrack *
process.selectedAK5PFGenJets*
process.matchedAK5PFGenJets *
process.inclusiveVertexing * 
#process.inclusiveMergedVerticesFiltered * 
#process.bToCharmDecayVertexMerged * 
process.myak5JetTracksAssociatorAtVertex * 
process.impactParameterTagInfos * 
process.inclusiveSecondaryVertexFinderTagInfos *
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK5PFJets *
process.combinedSVMVATrainer 
)


process.PoolSource.fileNames = [
#"root://xrootd-redic.pi.infn.it:1194//store/relval/CMSSW_7_0_6/RelValQCD_Pt_600_800_13/GEN-SIM-RECO/PLS170_V7AN1-v1/00000/BAE49338-32FA-E311-9609-00261894394B.root"
#"root://xrootd-redic.pi.infn.it:1194//store/mc/Spring14dr/QCD_Pt-1800_Tune4C_13TeV_pythia8/GEN-SIM-RECODEBUG/castor_PU_S14_POSTLS170_V6-v1/00000/00ECBDAF-960B-E411-8441-02163E00F114.root"
"root://xrootd-redic.pi.infn.it:1194//store/mc/Spring14dr/QCD_Pt-1400to1800_Tune4C_13TeV_pythia8/GEN-SIM-RECODEBUG/castor_PU_S14_POSTLS170_V6-v1/00000/02B69E5F-7309-E411-A895-003048D15E40.root"
]

