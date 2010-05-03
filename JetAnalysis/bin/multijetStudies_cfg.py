import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")

process.load('Analysis.JetAnalysis.multijetStudies_cfi')

process.load('PhysicsTools.SelectorUtils.pfJetIDSelector_cfi')
process.load('PhysicsTools.SelectorUtils.jetIDSelector_cfi')

process.plotParameters = cms.PSet (
    doTracks = cms.bool(False),
    useMC = cms.bool(False)
)


process.inputs = cms.PSet (
    fileNames = cms.vstring(
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_100_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_101_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_102_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_103_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_104_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_105_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_106_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_107_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_108_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_109_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_10_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_110_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_111_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_112_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_113_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_114_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_115_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_116_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_117_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_118_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_119_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_11_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_120_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_121_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_122_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_123_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_124_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_125_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_126_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_127_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_128_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_129_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_12_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_130_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_131_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_132_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_133_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_134_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_135_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_136_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_137_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_138_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_139_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_13_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_140_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_141_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_142_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_143_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_144_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_145_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_146_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_147_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_148_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_149_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_14_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_150_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_151_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_152_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_153_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_154_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_155_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_156_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_157_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_158_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_159_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_15_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_160_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_161_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_162_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_163_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_164_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_165_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_166_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_167_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_168_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_169_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_16_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_170_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_171_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_172_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_173_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_174_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_175_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_176_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_177_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_178_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_179_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_17_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_180_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_181_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_182_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_183_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_184_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_186_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_187_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_188_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_189_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_18_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_190_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_191_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_192_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_193_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_194_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_195_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_196_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_197_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_198_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_199_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_19_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_1_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_200_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_201_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_202_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_203_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_204_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_205_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_206_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_207_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_208_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_209_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_20_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_210_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_211_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_212_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_213_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_214_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_215_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_216_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_217_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_218_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_219_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_21_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_220_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_221_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_222_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_223_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_224_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_225_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_226_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_227_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_228_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_229_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_22_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_230_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_231_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_232_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_233_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_234_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_235_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_236_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_237_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_238_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_239_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_23_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_240_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_241_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_242_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_243_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_244_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_245_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_246_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_247_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_248_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_249_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_24_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_250_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_251_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_252_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_253_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_25_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_26_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_27_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_28_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_29_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_2_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_30_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_31_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_32_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_33_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_34_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_35_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_36_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_37_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_38_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_39_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_3_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_40_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_41_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_42_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_43_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_44_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_45_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_46_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_47_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_48_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_49_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_4_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_50_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_51_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_52_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_53_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_54_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_55_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_56_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_57_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_58_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_59_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_5_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_60_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_61_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_62_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_63_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_64_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_65_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_66_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_67_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_68_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_69_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_6_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_70_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_71_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_72_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_73_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_74_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_75_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_76_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_77_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_78_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_79_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_7_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_80_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_81_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_82_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_83_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_84_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_85_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_86_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_87_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_88_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_89_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_8_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_90_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_91_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_92_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_93_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_94_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_95_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_96_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_97_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_98_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_99_1.root',
'/Volumes/MyBook/Data/shyft_7TeV_firstdata_357_pat/shyft_7TeV_firstdata_357_pat_9_1.root'


        ),

    lumisToProcess = cms.untracked.VLuminosityBlockRange(
	'132440:157-132440:401',
	'132596:382-132596:383',
	'132596:447-132596:453',
	'132598:80-132598:82',
	'132598:174-132598:188',
	'132599:1-132599:379',
	'132599:381-132599:538',
	'132601:1-132601:207',
	'132601:209-132601:259',
	'132601:261-132601:1131',
	'132602:1-132602:83',
	'132605:1-132605:444',
	'132605:446-132605:622',
	'132605:624-132605:829',
	'132605:831-132605:968',
	'132606:1-132606:37',
	'132656:1-132656:140',
	'132658:1-132658:177',
	'132659:1-132659:84',
	'132661:1-132661:130',
	'132662:1-132662:130',
	'132662:132-132662:165',
	'132716:220-132716:591',
	'132716:593-132716:640',
	'132959:1-132959:276',
	'132959:278-132959:417',
	'132960:1-132960:190',
	'132961:1-132961:427',
	'132965:1-132965:107',
	'132968:1-132968:173',
	'133029:101-133029:115',
	'133029:129-133029:350',
	'133031:1-133031:18',
	'133034:131-133034:325',
	'133035:1-133035:306',
	'133036:1-133036:225',
	'133046:1-133046:43',
	'133046:45-133046:323',
	'133158:65-133158:786',
	'133321:1-133321:383',
        )
)

process.outputs = cms.PSet (
    outputName = cms.string('multijetPlots_4jets.root')
)
 
