import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",

  CombinedSVRecoVertex = cms.string('GlobalTag_MCRUN2_74_V7/CombinedSVRecoVertex.mva'), 
	CombinedSVPseudoVertex = cms.string('GlobalTag_MCRUN2_74_V7/CombinedSVPseudoVertex.mva'), 
	CombinedSVNoVertex = cms.string('GlobalTag_MCRUN2_74_V7/CombinedSVNoVertex.mva'), 
	
	GhostTrackRecoVertex = cms.string('GlobalTag_MCRUN2_74_V7/GhostTrackRecoVertex.mva'),
  GhostTrackPseudoVertex = cms.string('GlobalTag_MCRUN2_74_V7/GhostTrackPseudoVertex.mva'),
  GhostTrackNoVertex = cms.string('GlobalTag_MCRUN2_74_V7/GhostTrackNoVertex.mva'),
	
	CombinedMVA = cms.string('GlobalTag_MCRUN2_74_V7/CombinedMVA.mva'),
	
	CombinedSVIVFV2RecoVertex = cms.string('GlobalTag_MCRUN2_74_V7/CombinedSVIVFV2RecoVertex.mva'), 
	CombinedSVIVFV2PseudoVertex = cms.string('GlobalTag_MCRUN2_74_V7/CombinedSVIVFV2PseudoVertex.mva'), 
	CombinedSVIVFV2NoVertex = cms.string('GlobalTag_MCRUN2_74_V7/CombinedSVIVFV2NoVertex.mva'),
	
	CombinedSVRecoVertexNoSoftLepton = cms.string('GlobalTag_MCRUN2_74_V7/CombinedRecoVertexNoSoftLepton.mva'), 
	CombinedSVPseudoVertexNoSoftLepton = cms.string('GlobalTag_MCRUN2_74_V7/CombinedPseudoVertexNoSoftLepton.mva'), 
	CombinedSVNoVertexNoSoftLepton = cms.string('GlobalTag_MCRUN2_74_V7/CombinedNoVertexNoSoftLepton.mva'),
	CombinedSVRecoVertexSoftMuon = cms.string('GlobalTag_MCRUN2_74_V7/CombinedRecoVertexSoftMuon.mva'),  
	CombinedSVPseudoVertexSoftMuon = cms.string('GlobalTag_MCRUN2_74_V7/CombinedPseudoVertexSoftMuon.mva'), 
	CombinedSVNoVertexSoftMuon = cms.string('GlobalTag_MCRUN2_74_V7/CombinedNoVertexSoftMuon.mva'),
	CombinedSVRecoVertexSoftElectron = cms.string('GlobalTag_MCRUN2_74_V7/CombinedRecoVertexSoftElectron.mva'), 
	CombinedSVPseudoVertexSoftElectron = cms.string('GlobalTag_MCRUN2_74_V7/CombinedPseudoVertexSoftElectron.mva'), 
	CombinedSVNoVertexSoftElectron = cms.string('GlobalTag_MCRUN2_74_V7/CombinedNoVertexSoftElectron.mva'), 

	CombinedMVAnew = cms.string('cMVA.mva'),
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:MVAJetTags_newCMVA.db'),
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
		
		'CombinedMVAnew'
	)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
