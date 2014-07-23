import FWCore.ParameterSet.Config as cms

process = cms.Process("CSVTrainer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("RecoBTau.JetTagComputer.jetTagRecord_cfi")
process.load("RecoBTag.SecondaryVertex.combinedSecondaryVertexES_cfi")
#process.combinedSecondaryVertex.trackMultiplicityMin = cms.uint32(2)

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.Geometry_cff") #old one, to use for old releases
process.load("Configuration.Geometry.GeometryIdeal_cff") #new one
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("POSTLS170_V6::All")

##To use the newest training!
#process.load("CondCore.DBCommon.CondDBSetup_cfi")
#process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
#       process.CondDBSetup,
#       timetype = cms.string('runnumber'),
#       toGet = cms.VPSet(cms.PSet(
#               record = cms.string('BTauGenericMVAJetTagComputerRcd'),
#               tag = cms.string('MVAJetTags_CMSSW_5_3_4')
#       )),
#       connect = cms.string("sqlite_file:MVAJetTags_withPFnoPU_Adding2HighPtBins.db"),
#       #connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
#       BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
#)
#process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")

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

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(101)
)

process.source = cms.Source("PoolSource",
#	fileNames = cms.untracked.vstring('file:testTagInfos.root')
	fileNames = cms.untracked.vstring(
#'/store/mc/Fall11/QCD_Pt-50to80_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00225C27-4744-E111-8583-003048C692E4.root',
#'/store/mc/Fall11/QCD_Pt-80to120_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00D668C4-5244-E111-A8F6-0025901D4936.root',
#'/store/mc/Fall11/QCD_Pt-120to170_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/023CE3AD-CF46-E111-90CB-003048C690A0.root',
#'/store/mc/Fall11/QCD_Pt-170to300_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0433579C-7644-E111-9D93-00215AD4D6C8.root',
#'/store/mc/Fall11/QCD_Pt-300to470_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00C128DE-923F-E111-AA76-003048C69312.root',
#'/store/mc/Fall11/QCD_Pt-470to600_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00CC4BA4-FC45-E111-A993-003048F0E80C.root',
#'/store/mc/Fall11/QCD_Pt-600to800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/000548D5-0A40-E111-A327-002481E0DA4E.root',
#'/store/mc/Fall11/QCD_Pt-800to1000_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0469BF65-8343-E111-8E43-003048F0E3B2.root',
#'/store/mc/Fall11/QCD_Pt-1000to1400_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/14151191-9043-E111-BA90-003048C690A0.root',
#'/store/mc/Fall11/QCD_Pt-1400to1800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0E10C938-1146-E111-95AC-0025901D4A58.root',
#'/store/mc/Fall11/QCD_Pt-1800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0C4D9605-2544-E111-B39F-003048D4DF80.root',
#'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FED775BD-B8E1-E111-8ED5-003048C69036.root'
'root://xrootd.unl.edu//store/mc/Spring14dr/QCD_Pt-470to600_Tune4C_13TeV_pythia8/AODSIM/castor_PU_S14_POSTLS170_V6-v1/00000/00435352-A3ED-E311-ACA8-0025905A607A.root'

	)
)


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

 
