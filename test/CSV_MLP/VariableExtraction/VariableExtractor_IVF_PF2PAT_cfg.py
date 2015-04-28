
import FWCore.ParameterSet.Config as cms


process = cms.Process("CSVTrainer")


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10


process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("SimTracker.TrackAssociation.TrackAssociatorByChi2_cfi")
process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
process.load("SimTracker.TrackHistory.TrackHistory_cff")
process.load("SimTracker.TrackHistory.TrackClassifier_cff")
process.load("RecoBTag.Configuration.RecoBTag_cff")

#2023 geometry
process.load('Configuration.Geometry.GeometryExtended2023SHCalNoTaperReco_cff')
process.load('Configuration.Geometry.GeometryExtended2023SHCalNoTaper_cff')


process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.globaltag = cms.string("PH2_1K_FB_V6::All") 

process.options = cms.untracked.PSet(
allowUnscheduled = cms.untracked.bool(True),
#SkipEvent = cms.untracked.vstring('ProductNotFound')
)


process.maxEvents = cms.untracked.PSet(
input = cms.untracked.int32(100)
)

process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring(
#'root://xrootd.unl.edu//store/mc/Upg2023SHCAL14DR/PYTHIA6_Tauola_TTbar_TuneZ2star_14TeV/GEN-SIM-RECO/PU140bx25_PH2_1K_FB_V4-v1/00000/0039D9EB-343C-E411-8141-0025905A60A8.root'
 '/store/mc/TP2023SHCALDR/PYTHIA6_Tauola_TTbar_TuneZ2star_14TeV/GEN-SIM-RECO/SHCALJan23_PU140BX25_PH2_1K_FB_V6-v1/00000/003506C6-E2A3-E411-831B-0025905A6076.root',

 )
)



## Jet energy corrections
jetCorrectionsAK4 = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')
jetCorrectionsAK5 = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')
jetCorrectionsAK7 = ('AK7PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

#pvCollection = 'sortedGoodOfflinePrimaryVertices'
pvCollection = 'goodOfflinePrimaryVertices'

from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
jetAlgo="AK5"
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=True, postfix=postfix, jetCorrections=jetCorrectionsAK4, pvCollection=cms.InputTag(pvCollection))


## Produce a collection of good primary vertices
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')

## Filter for good primary vertex
process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
vertexCollection = cms.InputTag('offlinePrimaryVertices'),
minimumNDOF = cms.uint32(4) ,
maxAbsZ = cms.double(24),
maxd0 = cms.double(2)
)

## Load modules for primary vertex sorting
process.load("RecoVertex.PrimaryVertexSorter.sortedOfflinePrimaryVertices_cff")
process.sortedGoodOfflinePrimaryVertices = process.sortedOfflinePrimaryVertices.clone(
src = cms.InputTag('goodOfflinePrimaryVertices')
)


# top projections in PF2PAT:
getattr(process,"pfPileUpJME"+postfix).checkClosestZVertex = False
getattr(process,"pfNoPileUpJME"+postfix).enable = True
getattr(process,"pfNoMuonJME"+postfix).enable = False
getattr(process,"pfNoElectronJME"+postfix).enable = False
getattr(process,"pfNoTau"+postfix).enable = False
getattr(process,"pfNoJet"+postfix).enable = False


# Switch the default jet collection (done in order to use the above specified b-tag infos and discriminators)
switchJetCollection(
process,
jetSource = cms.InputTag('pfJets'+postfix),   
jetCorrections = jetCorrectionsAK4,
genJetCollection = cms.InputTag('ak5GenJetsNoNu'+postfix),
btagDiscriminators = 
["jetBProbabilityBJetTags","jetProbabilityBJetTags","trackCountingHighPurBJetTags",
"trackCountingHighEffBJetTags","simpleSecondaryVertexHighEffBJetTags",
"simpleSecondaryVertexHighPurBJetTags","combinedSecondaryVertexBJetTags"],
postfix = postfix
)


#process.patJetsPFlow.addJetCorrFactors = cms.bool(False) ## switch off the jet corrections, they are true by default


# Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag(pvCollection))
# Need to update impactParameterTagInfosForPVSorting to remove circular module dependency
getattr(process,'impactParameterTagInfosForPVSorting').primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")



# Switching from AK5 to AK4 jets
print 'Switching from AK5 to AK4 jets'
print '******************************'
## Change cone sizes (note that only the cose sizes are changed, but not the collection names)
process.ak5GenJetsNoNuPFlow.rParam = cms.double(0.4)
process.pfJetsPFlow.rParam = cms.double(0.4)
process.jetTracksAssociatorAtVertexPFlow.coneSize = cms.double(0.4)

## Select JEC version
#jec = 'DES19_V1'
#jec = 'AGE1K_V1'
jec = 'PhaseII_Shashlik140PU_V2'
## Get AK4PFchs JECs from a sqlite file
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.jec = cms.ESSource("PoolDBESSource",
DBParameters = cms.PSet(
messageLevel = cms.untracked.int32(0)
),
timetype = cms.string('runnumber'),
toGet = cms.VPSet(
cms.PSet(
record = cms.string('JetCorrectionsRecord'),
tag = cms.string('JetCorrectorParametersCollection_' + jec + '_AK4PFchs'),
label = cms.untracked.string('AK4PFchs')
),
## here you add as many jet types as you need
## note that the tag name is specific for the particular sqlite file
),
connect = cms.string('sqlite_fip:RecoBTau/JetTagMVALearning/data/' + jec + '.db')
)
## add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

#better PV sorting
from CommonTools.RecoAlgos.sortedPFPrimaryVertices_cfi import *
process.betterOfflinePrimaryVertices=sortedPFPrimaryVertices.clone(jets = "ak5PFJets")
process.vertSeq = cms.Sequence(
process.betterOfflinePrimaryVertices
)
process.primaryVertexFilter.vertexCollection= cms.InputTag('betterOfflinePrimaryVertices')
process.goodOfflinePrimaryVertices.src = cms.InputTag('betterOfflinePrimaryVertices')



from PhysicsTools.JetMCAlgos.AK5PFJetsMCPUJetID_cff import *
process.selectedAK5PFGenJets = ak5GenJetsMCPUJetID.clone()
process.selectedAK5PFGenJets.src = cms.InputTag('ak5GenJetsNoNu'+postfix) 
process.matchedAK5PFGenJets = ak5PFJetsGenJetMatchMCPUJetID.clone()
process.matchedAK5PFGenJets.src=cms.InputTag('patJets' +postfix) 
process.matchedAK5PFGenJets.matched = cms.InputTag("selectedAK5PFGenJets")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = cms.InputTag('patJets' +postfix),
						#  coneSize = cms.double(0.4)
                                                  )

#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")
#process.impactParameterTagInfos.minimumNumberOfHits = cms.int32(6) #default is 8 , changed for phase1 aged sample
process.combinedSecondaryVertexV2.trackMultiplicityMin = cms.uint32(2)

#for Inclusive Vertex Finder
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
process.load('RecoBTag/SecondaryVertex/inclusiveSecondaryVertexFinderTagInfos_cfi')

process.impactParameterTagInfos.primaryVertex = cms.InputTag("betterOfflinePrimaryVertices")
process.inclusiveSecondaryVertexFinderTagInfos.trackSelection.qualityClass = cms.string('any')
process.inclusiveVertexFinder.primaryVertices = cms.InputTag("betterOfflinePrimaryVertices")
process.trackVertexArbitrator.primaryVertices = cms.InputTag("betterOfflinePrimaryVertices") 

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
process.jetFlavourInfosAK5PFJets.jets = cms.InputTag("patJets"+postfix)
process.jetFlavourInfosAK5PFJets.rParam = cms.double(0.4)  



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
	maximumPseudoRapidity = cms.double(4.2),  
	signalFlavours = cms.vint32(5, 7),
	minimumPseudoRapidity = cms.double(0.0),
	jetTagComputer = cms.string('combinedSecondaryVertexV2'),
	jetFlavourMatching = cms.InputTag("jetFlavourInfosAK5PFJets"),
	matchedGenJets = cms.InputTag("matchedAK5PFGenJets"),
	ignoreFlavours = cms.vint32(0)
)




process.p = cms.Path(
process.vertSeq*
process.goodOfflinePrimaryVertices*
process.combinedSVMVATrainer

)

