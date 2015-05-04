# Auto generated configuration file
# using: 
# Revision: 1.118 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/PYTHIA6_QCD_Pthat_80_10TeV_cff.py --customise Configuration/GenProduction/PYTHIA_custom.py -s GEN:ProductionFilterSequence --mc --eventcontent RAWSIM --datatier GEN --conditions FrontierConditions_GlobalTag,IDEAL_31X::All --no_exec -n 1000000
import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/MixingNoPileUp_cff')
process.load('Configuration/StandardSequences/GeometryExtended_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/Generator_cff')
process.load('Configuration/StandardSequences/VtxSmearedEarly10TeVCollision_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.7 $'),
    annotation = cms.untracked.string('Summer09: Pythia6 generation of QCD events, 10TeV, D6T tune, pthat > __PTHAT__ GeV'),
    name = cms.untracked.string('$Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/GenProduction/python/PYTHIA6_QCD_Pthat.sh,v $')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(__MAX_EVENTS__)
)
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)
# Input source
process.source = cms.Source("EmptySource")

# Output definition
#process.output = cms.OutputModule("SewerModule", shouldPass = cms.int32(__MAX_EVENTS__), name = cms.string("sewer"),
process.output = cms.OutputModule("PoolOutputModule",
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('__SE_OUTPUT_FILES__'),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.GlobalTag.globaltag = 'MC_31X_V3::All'
process.generator = cms.EDFilter("Pythia6GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(10000.0),
    crossSection = cms.untracked.double(__XSEC__),
    maxEventsToPrint = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        pythiaUESettings = cms.vstring(
            'MSTJ(11)=3      ! Choice of the fragmentation function', 
            'MSTJ(22)=2      ! Decay those unstable particles', 
            'PARJ(71)=10     ! for which ctau  10 mm', 
            'MSTP(2)=1       ! which order running alphaS', 
            'MSTP(33)=0      ! no K factors in hard cross sections', 
            'MSTP(51)=10042  ! CTEQ6L1 structure function chosen', 
            'MSTP(52)=2      ! work with LHAPDF', 
            'MSTP(81)=1      ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4      ! Defines the multi-parton model', 
            'MSTU(21)=1      ! Check on possible errors during program execution', 
            'PARP(82)=1.8387 ! pt cutoff for multiparton interactions', 
            'PARP(89)=1960   ! sqrts for which PARP82 is set', 
            'PARP(83)=0.5    ! Multiple interactions: matter distrbn parameter', 
            'PARP(84)=0.4    ! Multiple interactions: matter distribution parameter', 
            'PARP(90)=0.16   ! Multiple interactions: rescaling power', 
            'PARP(67)=2.5    ! amount of initial-state radiation', 
            'PARP(85)=1.0    ! gluon prod. mechanism in MI', 
            'PARP(86)=1.0    ! gluon prod. mechanism in MI', 
            'PARP(62)=1.25   ! ', 
            'PARP(64)=0.2    ! ', 
            'MSTP(91)=1      ! ', 
            'PARP(91)=2.1    ! kt distribution', 
            'PARP(93)=15.0   ! '),
        processParameters = cms.vstring(
            'MSEL=1          ! QCD hight pT processes', 
            'CKIN(3)= __PTHAT__    ! minimum pt hat for hard interactions'),
        parameterSets = cms.vstring(
            'pythiaUESettings', 
            'processParameters')
    )
)
process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.endjob_step = cms.Path(process.endOfProcess)
process.out_step = cms.EndPath(process.output)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step, process.endjob_step, process.out_step)

# special treatment in case of production filter sequence  
for path in process.paths: 
    getattr(process, path)._seq = process.ProductionFilterSequence*getattr(process, path)._seq


# Automatic addition of the customisation function

def customise(process):
	process.genParticles.abortOnUnknownPDGCode = False
#	process.xsec = cms.EDAnalyzer('XSEC')
#	process.generation_step += process.xsec
	process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(__RANDOM__)

	return(process)


# End of customisation function definition

process = customise(process)
