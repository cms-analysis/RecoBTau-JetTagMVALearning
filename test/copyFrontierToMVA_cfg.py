import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'MCRUN2_74_V9::All'

#process.prefer("BTauMVAJetTagComputerRecord")

process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerFileSave",
	trained = cms.untracked.bool(False),
	CombinedMVA = cms.string('CombinedMVA.mva'), 

	CombinedSVRecoVertex = cms.string('CombinedSVRecoVertex.mva'), 
	CombinedSVPseudoVertex = cms.string('CombinedSVPseudoVertex.mva'), 
	CombinedSVNoVertex = cms.string('CombinedSVNoVertex.mva'), 

	GhostTrackRecoVertex = cms.string('GhostTrackRecoVertex.mva'),
  GhostTrackPseudoVertex = cms.string('GhostTrackPseudoVertex.mva'),
  GhostTrackNoVertex = cms.string('GhostTrackNoVertex.mva'),

	CombinedSVIVFV2RecoVertex = cms.string('CombinedSVIVFV2RecoVertex.mva'), 
	CombinedSVIVFV2PseudoVertex = cms.string('CombinedSVIVFV2PseudoVertex.mva'), 
	CombinedSVIVFV2NoVertex = cms.string('CombinedSVIVFV2NoVertex.mva'),
	
	CombinedSVRecoVertexNoSoftLepton = cms.string('CombinedRecoVertexNoSoftLepton.mva'), 
	CombinedSVPseudoVertexNoSoftLepton = cms.string('CombinedPseudoVertexNoSoftLepton.mva'), 
	CombinedSVNoVertexNoSoftLepton = cms.string('CombinedNoVertexNoSoftLepton.mva'),
	CombinedSVRecoVertexSoftMuon = cms.string('CombinedRecoVertexSoftMuon.mva'),  
	CombinedSVPseudoVertexSoftMuon = cms.string('CombinedPseudoVertexSoftMuon.mva'), 
	CombinedSVNoVertexSoftMuon = cms.string('CombinedNoVertexSoftMuon.mva'),
	CombinedSVRecoVertexSoftElectron = cms.string('CombinedRecoVertexSoftElectron.mva'), 
	CombinedSVPseudoVertexSoftElectron = cms.string('CombinedPseudoVertexSoftElectron.mva'), 
	CombinedSVNoVertexSoftElectron = cms.string('CombinedNoVertexSoftElectron.mva'), 
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
