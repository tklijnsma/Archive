import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
    lepIsoLoose = cms.untracked.double(0.2),
    pathToCP = cms.string('./root/ControlPlotsTEST.root'),
    speedup = cms.untracked.int32(0),
    doJECdown = cms.untracked.int32(0),
    btag_prob_cut_5jets = cms.untracked.double(0.98225),
    integralOption2 = cms.untracked.int32(1),
    integralOption0 = cms.untracked.int32(0),
    integralOption1 = cms.untracked.int32(0),
    pathTo_f_Vtype3_id = cms.string('root/EleRecoId.ScaleFactor.wp80.2012ABCD.root'),
    nMaxJetsSLw1jType3 = cms.untracked.int32(4),
    integralOption2_stage = cms.untracked.int32(1),
    doJERup = cms.untracked.int32(0),
    pathTo_f_Vtype1_id = cms.string('root/EleRecoId.ScaleFactor.wp95.2012ABCD.root'),
    samples = cms.VPSet(cms.PSet(
        perJob = cms.uint32(100000),
        name = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        color = cms.int32(1),
        skip = cms.bool(False),
        xSec = cms.double(508.5),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        fullFilename = cms.string('dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/s1_eb733a1/ttjets_13tev_madgraph_pu20bx25_phys14/block_512.root')
    )),
    doJECup = cms.untracked.int32(0),
    MwH = cms.untracked.double(100),
    norm = cms.untracked.int32(0),
    MwL = cms.untracked.double(60),
    lumi = cms.untracked.double(19.04),
    useAnalyticalFormula = cms.untracked.int32(1),
    MhL = cms.untracked.double(110),
    csv_WP_M = cms.untracked.double(0.679),
    csv_WP_L = cms.untracked.double(0.244),
    MhH = cms.untracked.double(140),
    doJERdown = cms.untracked.int32(0),
    hypo = cms.untracked.int32(0),
    useCMVA = cms.untracked.int32(0),
    debug = cms.untracked.int32(0),
    csv_WP_T = cms.untracked.double(0.898),
    integralOption2_nevalfact = cms.untracked.double(1.0),
    muEtaTight = cms.untracked.double(2.1),
    doCSVup = cms.untracked.int32(0),
    printout = cms.untracked.int32(0),
    pathTo_f_Vtype3_tr = cms.string('root/SingleEle.TrigEff.wp80.2012ABCD.root'),
    evLimits = cms.vint32(0, 10000),
    cutWMass = cms.untracked.bool(False),
    cutLeptons = cms.untracked.bool(False),
    pathTo_f_Vtype2_tr = cms.string('root/SingleMu24OR40.TrigEff.2012ABCD.root'),
    smearJets = cms.untracked.int32(0),
    useCSVcalibration = cms.untracked.int32(1),
    doType6ByBTagShape = cms.untracked.int32(1),
    useMET = cms.untracked.int32(1),
    jetPtThreshold = cms.untracked.double(30.0),
    lepIsoTight = cms.untracked.double(0.12),
    muEtaLoose = cms.untracked.double(2.4),
    doType3ByBTagShape = cms.untracked.int32(1),
    maxChi2 = cms.untracked.double(2.5),
    doType6 = cms.untracked.int32(0),
    doType7 = cms.untracked.int32(0),
    doType4 = cms.untracked.int32(0),
    doType2 = cms.untracked.int32(0),
    doType3 = cms.untracked.int32(0),
    doType0 = cms.untracked.int32(0),
    doType1 = cms.untracked.int32(0),
    lepPtLoose = cms.untracked.double(20),
    reject_pixel_misalign_evts = cms.untracked.int32(0),
    MH = cms.untracked.double(125.0),
    jetPtLoose = cms.untracked.double(40.0),
    MT = cms.untracked.double(174.3),
    MW = cms.untracked.double(80.19),
    pathToFile = cms.string('dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/s1_eb733a1/'),
    pathTo_f_Vtype1L2_tr = cms.string('root/DoubleEle8.TrigEff.wp95.2012ABCD.root'),
    doType2ByBTagShape = cms.untracked.int32(1),
    verbose = cms.bool(False),
    useME = cms.untracked.int32(1),
    useRegression = cms.untracked.int32(0),
    recoverTopBTagBin = cms.untracked.int32(1),
    lepPtTight = cms.untracked.double(30),
    doGenLevelAnalysis = cms.untracked.int32(0),
    ordering = cms.string('TTHbb_s1_eb733a1_'),
    useJac = cms.untracked.int32(1),
    pathToTF = cms.string('./root/transferFunctionsTEST.root'),
    selectByBTagShape = cms.untracked.int32(1),
    testSLw1jType3 = cms.untracked.int32(1),
    ntuplizeAll = cms.untracked.int32(1),
    switchoffOL = cms.untracked.int32(0),
    triggerErrors = cms.untracked.int32(1),
    useTF = cms.untracked.int32(1),
    systematics = cms.vint32(0),
    doJERbias = cms.untracked.int32(0),
    MwLType3 = cms.untracked.double(72.0),
    fixNumEvJob = cms.untracked.int32(0),
    doType0ByBTagShape = cms.untracked.int32(1),
    SoB = cms.untracked.int32(1),
    elEta = cms.untracked.double(2.5),
    usePDF = cms.untracked.int32(1),
    cutJets = cms.untracked.bool(False),
    doCSVdown = cms.untracked.int32(0),
    btag_prob_cut_4jets = cms.untracked.double(0.95295),
    functions = cms.vstring('8.95351e+18*TMath::Landau(x, 5.67600e+01,1.01258e+01)',
        '2.95547e+17*TMath::Landau(x,7.61581e+01 ,1.89245e+01)',
        '2.98474e+17*TMath::Landau(x,7.40196e+01 ,1.80142e+01)',
        '6.28300e+16*TMath::Landau(x,8.03060e+01 ,1.81679e+01)',
        'x>150?2.44515e+27*x^(-5.35628e+00):1.24208e+18*exp((-3.63162e-02)*x)',
        'x>=12 ? x^(-2.010e-01)*exp((-1.5785e-02)*x) : 4.184e-02*x'),
    MwHType3 = cms.untracked.double(92.0),
    outFileName = cms.string('/scratch/tmpdir-6294569.1.all.q/277_0/174892/output.root'),
    enhanceMC = cms.untracked.int32(0),
    pathTo_f_Vtype1L1_tr = cms.string('root/DoubleEle17.TrigEff.wp95.2012ABCD.root'),
    jetMultLoose = cms.untracked.int32(0),
    pathToCP_smear = cms.string('./root/ControlPlotsTEST_std_gen.root'),
    massesH = cms.vdouble(125.0),
    useBtag = cms.untracked.int32(1),
    doType1ByBTagShape = cms.untracked.int32(1),
    doTypeBTag4 = cms.untracked.int32(0),
    doTypeBTag5 = cms.untracked.int32(0),
    doTypeBTag6 = cms.untracked.int32(0),
    massesT = cms.vdouble(174.3),
    integralOption2_niter = cms.untracked.int32(1),
    doubleGaussianB = cms.untracked.int32(1),
    pathTo_f_Vtype2_id = cms.string('root/MuRecoId.ScaleFactor.2012ABCD.root'),
    max_n_trials = cms.untracked.int32(50000),
    btag_prob_cut_6jets = cms.untracked.double(0.96),
    isMC = cms.bool(True),
    useDynamicalScale = cms.untracked.int32(1),
    cutBTagShape = cms.untracked.bool(False)
)
