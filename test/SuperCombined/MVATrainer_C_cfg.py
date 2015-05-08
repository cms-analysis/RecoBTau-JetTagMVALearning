import FWCore.ParameterSet.Config as cms

process = cms.Process("IPTrainer")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.combinedMVATrainer = cms.EDAnalyzer("JetTagMVATreeTrainer",
	useCategories		= cms.bool(False),
	calibrationRecord	= cms.string("combinedMVA"),
	ignoreFlavours		= cms.vint32(0),#### since input is only C, this is correct
	signalFlavours		= cms.vint32(5, 7),#### this is used to flag jets of flavour B as signal and other flavours as background
	minimumTransverseMomentum = cms.double(20.0),
	minimumPseudoRapidity	= cms.double(0),
	maximumPseudoRapidity	= cms.double(2.4),
	fileNames = cms.vstring(
		"VariableExtraction/gridjobs/cMVA_default_filterOn/combinedMVA_C.root",
	)
)

process.looper = cms.Looper("JetTagMVATrainerLooper",
	trainers = cms.VPSet(
		cms.PSet(
			calibrationRecord = cms.string("combinedMVA"),
			trainDescription = cms.untracked.string("Save_C.xml"),
			loadState = cms.untracked.bool(False),
			saveState = cms.untracked.bool(False)
		)
	)
)

process.p = cms.Path(process.combinedMVATrainer)
