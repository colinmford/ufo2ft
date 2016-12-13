from fontTools.ttLib import TTFont
from defcon import Font
from ufo2ft.kernFeatureWriter import KernFeatureWriter
from ufo2ft.makeotfParts import FeatureOTFCompiler
from ufo2ft.markFeatureWriter import MarkFeatureWriter
import unittest
import os


def makeCompiler(filename):
    dirname = os.path.dirname(__file__)
    ufo = Font(os.path.join(dirname, "data", filename))
    featureCompiler = FeatureOTFCompiler(
        ufo, TTFont(), KernFeatureWriter, MarkFeatureWriter)
    featureCompiler.precompile()
    featureCompiler.setupFile_features()
    return featureCompiler


class FeatureOTFCompilerTest(unittest.TestCase):
    def test_GDEF_withCarets(self):
        compiler = makeCompiler("LigatureTestFont.ufo")
        self.assertEqual(compiler.getLigatureCaretPositions(),
                         {'f_f_i': (306, 613)})
        self.assertEqual(compiler.features.split("\n"), [
            "table GDEF {",
            "  LigatureCaretByPos f_f_i 306 613;",
            "} GDEF;",
        ])

    def test_GDEF_noCarets(self):
        compiler = makeCompiler("TestFont.ufo")
        self.assertEqual(compiler.getLigatureCaretPositions(), {})
        self.assertEqual(compiler.features, "")


if __name__ == "__main__":
    unittest.main()
