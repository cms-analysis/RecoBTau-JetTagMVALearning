import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")
#process.load("DQMServices.Components.DQMEnvironment_cfi")
#process.load("DQMServices.Core.DQM_cfg")


#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000


process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
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

# DQM include
process.load("Configuration.EventContent.EventContent_cff")
process.load('DQMOffline.Configuration.DQMOffline_cff')  #file had to be modified
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.MessageLogger.cerr.threshold = 'ERROR'

process.options = cms.untracked.PSet(
allowUnscheduled = cms.untracked.bool(True),
#SkipEvent = cms.untracked.vstring('ProductNotFound')
)


process.maxEvents = cms.untracked.PSet(
input = cms.untracked.int32(10)
)

process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring(
#'root://xrootd.unl.edu//store/mc/Upg2023SHCAL14DR/PYTHIA6_Tauola_TTbar_TuneZ2star_14TeV/GEN-SIM-RECO/PU140bx25_PH2_1K_FB_V4-v1/00000/0039D9EB-343C-E411-8141-0025905A60A8.root'
  '/store/mc/TP2023SHCALDR/PYTHIA6_Tauola_TTbar_TuneZ2star_14TeV/GEN-SIM-RECO/SHCALJan23_PU140BX25_PH2_1K_FB_V6-v1/00000/003506C6-E2A3-E411-831B-0025905A6076.root',

  )
)


process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
process.CondDBSetup,
timetype = cms.string('runnumber'),
toGet = cms.VPSet(cms.PSet(
record = cms.string('BTauGenericMVAJetTagComputerRcd'),
                tag = cms.string('MVAJetTags_620SLHCX')
)),
connect = cms.string("sqlite_file:MVAJetTags_620SLHCX_Phase1And2Upgrade_v10.db"),
#connect = cms.string("sqlite_file:MVAJetTags_test.db"),
#connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)
process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")




## Jet energy corrections
jetCorrectionsAK4 = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')
jetCorrectionsAK5 = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')
jetCorrectionsAK7 = ('AK7PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

#pvCollection = 'sortedGoodOfflinePrimaryVertices'
pvCollection = 'goodOfflinePrimaryVertices'

from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
jetAlgo="AK5"
jetcorr= jetCorrectionsAK4
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=True, postfix=postfix, jetCorrections=jetcorr, pvCollection=cms.InputTag(pvCollection))


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
jetCorrections = jetcorr, #jetCorrectionsAK4,
genJetCollection = cms.InputTag('ak5GenJetsNoNu'+postfix),
## b-tag infos
btagInfos = ['impactParameterTagInfos','secondaryVertexTagInfos','secondaryVertexNegativeTagInfos','softMuonTagInfos','inclusiveSecondaryVertexFinderTagInfos'],
btagDiscriminators = 
["jetBProbabilityBJetTags","jetProbabilityBJetTags","trackCountingHighPurBJetTags",
"trackCountingHighEffBJetTags","simpleSecondaryVertexHighEffBJetTags",
"simpleSecondaryVertexHighPurBJetTags"] , #"combinedSecondaryVertexBJetTags"],
postfix = postfix
)



# Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag(pvCollection))
# Need to update impactParameterTagInfosForPVSorting to remove circular module dependency
getattr(process,'impactParameterTagInfosForPVSorting').primaryVertex = cms.InputTag("goodOfflinePrimaryVertices")


#
# Switching from AK5 to AK4 jets
print 'Switching from AK5 to AK4 jets'
print '******************************'
## Change cone sizes (note that only the cose sizes are changed, but not the collection names)
process.ak5GenJetsNoNuPFlow.rParam = cms.double(0.4)
process.pfJetsPFlow.rParam = cms.double(0.4)
process.jetTracksAssociatorAtVertexPFlow.coneSize = cms.double(0.4)

### Select JEC version
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
connect = cms.string('sqlite_fip:RecoBTau/JetTagMVALearning/test/62XSLHC/' + jec + '.db')
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
#process.selectedAK5PFGenJets.cut = cms.string('pt>8.0')
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
process.secondaryVertexTagInfos.trackSelection.qualityClass = cms.string('any')
process.inclusiveSecondaryVertexFinderTagInfos.trackSelection.qualityClass = cms.string('any')
process.inclusiveVertexFinder.primaryVertices = cms.InputTag("betterOfflinePrimaryVertices")
process.trackVertexArbitrator.primaryVertices = cms.InputTag("betterOfflinePrimaryVertices")
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag("betterOfflinePrimaryVertices")
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag("betterOfflinePrimaryVertices")
process.softPFMuonsTagInfos.jets = cms.InputTag('patJets'+postfix)
process.softPFElectronsTagInfos.jets = cms.InputTag('patJets'+postfix)

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
process.jetFlavourInfosAK5PFJets.jets = cms.InputTag("patJets"+postfix)
process.jetFlavourInfosAK5PFJets.rParam = cms.double(0.4)  



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


# CSVIVFV2: MLP-based --> "standard CSVv2 from 53x"
process.combinedSecondaryVertexIVFV2=process.combinedSecondaryVertexV2.clone(
calibrationRecords = cms.vstring(
'CombinedSVIVFV2RecoVertex_53x',
'CombinedSVIVFV2PseudoVertex_53x',
'CombinedSVIVFV2NoVertex_53x'
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


###retrained CSVv2 Phase2 140PU, ak4PFCHS+ new Phase2JEC eta<3.0
process.combinedSecondaryVertexIVFV2Phase2JECHighPU=process.combinedSecondaryVertexV2.clone(
calibrationRecords = cms.vstring(
'CombinedSVIVFV2Phase2JEC_140PU_RecoVertex',
'CombinedSVIVFV2Phase2JEC_140PU_PseudoVertex',
'CombinedSVIVFV2Phase2JEC_140PU_NoVertex'
)
)
process.combinedSecondaryVertexIVFV2Phase2JECHighPUBJetTags = process.combinedSecondaryVertexV2BJetTags.clone(
jetTagComputer = cms.string('combinedSecondaryVertexIVFV2Phase2JECHighPU'),
tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"),
cms.InputTag("inclusiveSecondaryVertexFinderTagInfos")) #inclusiveSecondaryVertexFinderFilteredTagInfos
)
process.combinedSecondaryVertexIVFV2Phase2JECHighPU.trackSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexIVFV2Phase2JECHighPU.trackPseudoSelection.qualityClass = cms.string('any')
process.combinedSecondaryVertexIVFV2Phase2JECHighPU.trackMultiplicityMin = cms.uint32(2)


# combined IP+IVF or IP+IVF+SL taggers
process.CombinedIVFbtaggers = cms.Sequence(
process.combinedSecondaryVertexIVFV2BJetTags*
process.combinedSecondaryVertexIVFV2Phase2JECHighPUBJetTags
)





#standard validation tools
from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")


from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
#process.bTagCommonBlock.ptRecJetMin = cms.double(600.0)
process.bTagValidation.etaMax = cms.double(3.0)# 2.4 by default
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4, 3.0, 4.0)
process.bTagValidation.jetMCSrc = 'jetFlavourInfosAK5PFJets'
process.bTagValidation.genJetsMatched = 'matchedAK5PFGenJets'
process.bTagValidation.doPUid = True
process.bTagValidation.allHistograms = True
process.bTagValidation.flavPlots= 'allbcdusg'
#process.bTagValidation.fastMC = True
process.bTagValidation.doJetID = cms.bool(False) #check jet pass loose jet ID, only for PFjets 
process.bTagValidation.doJEC = False  #patJets are already corrected--> switch JEC off!

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
      finalizePlots = False,
      finalizeOnly = False
)


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
process.load('Configuration.StandardSequences.EndOfProcess_cff')


process.filtSeq =cms.Sequence(

process.primaryVertexFilter
*process.goodOfflinePrimaryVertices

)

process.btagDQM = cms.Path(
process.vertSeq*
process.filtSeq*
#process.selectedAK5PFGenJets *
#process.matchedAK5PFGenJets *
#process.goodOfflinePrimaryVertices *
#process.selectedHadronsAndPartons *
#process.jetFlavourInfosAK5PFJets *
#process.myak5JetTracksAssociatorAtVertex *
#process.taginfos *
#process.IPbtaggers *
#process.SVbtaggers *
#process.CombinedIVFbtaggers *
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

