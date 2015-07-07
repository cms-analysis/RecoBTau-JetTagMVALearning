import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
  CombinedSVRecoVertex = cms.string('ExtractedRecords/CombinedSVRecoVertex.mva'), 
	CombinedSVPseudoVertex = cms.string('ExtractedRecords/CombinedSVPseudoVertex.mva'), 
	CombinedSVNoVertex = cms.string('ExtractedRecords/CombinedSVNoVertex.mva'), 
	
	GhostTrackRecoVertex = cms.string('ExtractedRecords/GhostTrackRecoVertex.mva'),
  GhostTrackPseudoVertex = cms.string('ExtractedRecords/GhostTrackPseudoVertex.mva'),
  GhostTrackNoVertex = cms.string('ExtractedRecords/GhostTrackNoVertex.mva'),
	
	CombinedMVA = cms.string('Kevin_cMVA/cMVA.mva'),
	
	CombinedSVIVFV2RecoVertex = cms.string('ExtractedRecords/CombinedSVIVFV2RecoVertex.mva'), 
	CombinedSVIVFV2PseudoVertex = cms.string('ExtractedRecords/CombinedSVIVFV2PseudoVertex.mva'), 
	CombinedSVIVFV2NoVertex = cms.string('ExtractedRecords/CombinedSVIVFV2NoVertex.mva'),
	
	CombinedSVRecoVertexNoSoftLepton = cms.string('ExtractedRecords/CombinedRecoVertexNoSoftLepton.mva'), 
	CombinedSVPseudoVertexNoSoftLepton = cms.string('ExtractedRecords/CombinedPseudoVertexNoSoftLepton.mva'), 
	CombinedSVNoVertexNoSoftLepton = cms.string('ExtractedRecords/CombinedNoVertexNoSoftLepton.mva'),
	CombinedSVRecoVertexSoftMuon = cms.string('ExtractedRecords/CombinedRecoVertexSoftMuon.mva'),  
	CombinedSVPseudoVertexSoftMuon = cms.string('ExtractedRecords/CombinedPseudoVertexSoftMuon.mva'), 
	CombinedSVNoVertexSoftMuon = cms.string('ExtractedRecords/CombinedNoVertexSoftMuon.mva'),
	CombinedSVRecoVertexSoftElectron = cms.string('ExtractedRecords/CombinedRecoVertexSoftElectron.mva'), 
	CombinedSVPseudoVertexSoftElectron = cms.string('ExtractedRecords/CombinedPseudoVertexSoftElectron.mva'), 
	CombinedSVNoVertexSoftElectron = cms.string('ExtractedRecords/CombinedNoVertexSoftElectron.mva'), 
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:MVAJetTags.db'),
	toPut = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags')
	))
)

process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerSave",
	toPut = cms.vstring(),
	toCopy = cms.vstring(
	  'CombinedSVRecoVertex', 
	  'CombinedSVPseudoVertex', 
	  'CombinedSVNoVertex', 
		
	  'GhostTrackRecoVertex',
		'GhostTrackPseudoVertex',
		'GhostTrackNoVertex',
		
		'CombinedMVA',
		
		'CombinedSVIVFV2RecoVertex',
		'CombinedSVIVFV2PseudoVertex',
		'CombinedSVIVFV2NoVertex',
		
		'CombinedSVRecoVertexNoSoftLepton',
		'CombinedSVPseudoVertexNoSoftLepton',
		'CombinedSVNoVertexNoSoftLepton',
		'CombinedSVRecoVertexSoftMuon',
		'CombinedSVPseudoVertexSoftMuon',
		'CombinedSVNoVertexSoftMuon',
		'CombinedSVRecoVertexSoftElectron',
		'CombinedSVPseudoVertexSoftElectron',
		'CombinedSVNoVertexSoftElectron',
		
		)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
