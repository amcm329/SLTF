#!/usr/bin/env python
""" generated source for module LoessSettingsTest """
# package: com.github.servicenow.ds.stats.stl
import unittest
from LoessSettings import LoessSettings

# 
#  * While this class has no behavior, per se, the constructors are robust and fix bad args. Make sure they're doing it
#  * right and doing it consistently.
#  
class TestLoessSettings(unittest.TestCase):
    """ generated source for class LoessSettingsTest """
    def test_evenWidthBecomesNextOdd(self):
        """ generated source for method evenWidthBecomesNextOdd """
        settings = LoessSettings(20)
        self.assertEqual(21, settings.getWidth())
        self.assertEqual(1, settings.getDegree())
        self.assertEqual(3, settings.getJump())

    # 
    # 	 * Test that all constructors work consistently
    # 	 
    def test_evenWidthBecomesNextOdd2(self):
        """ generated source for method evenWidthBecomesNextOdd2 """
        settings = LoessSettings(20, 0)
        self.assertEqual(21, settings.getWidth())
        self.assertEqual(0, settings.getDegree())
        self.assertEqual(3, settings.getJump())

    # 
    # 	 * Test that all constructors work consistently
    # 	 
    def test_evenWidthBecomesNextOdd3(self):
        """ generated source for method evenWidthBecomesNextOdd3 """
        settings = LoessSettings(20, 0, 4)
        self.assertEqual(21, settings.getWidth())
        self.assertEqual(0, settings.getDegree())
        self.assertEqual(4, settings.getJump())

    def test_defaultJumpCalculationIsConsistentForOddWidth(self):
        """ generated source for method defaultJumpCalculationIsConsistentForOddWidth """
        settings1 = LoessSettings(51, 0)
        settings2 = LoessSettings(51)
        self.assertEqual(6, settings1.getJump())
        self.assertEqual(6, settings2.getJump())

    # 
    # 	 * Test for bug where jump was calculated before width was made odd.
    # 	 
    def test_defaultJumpCalculationIsConsistentForEvenWidth(self):
        """ generated source for method defaultJumpCalculationIsConsistentForEvenWidth """
        settings1 = LoessSettings(50, 0)
        settings2 = LoessSettings(50)
        self.assertEqual(6, settings1.getJump())
        self.assertEqual(6, settings2.getJump())

    def test_minWidthIsThree(self):
        """ generated source for method minWidthIsThree """
        settings = LoessSettings(0)
        self.assertEqual(3, settings.getWidth())
        self.assertEqual(1, settings.getDegree())
        self.assertEqual(1, settings.getJump())

    def test_jumpIsCorrect(self):
        """ generated source for method jumpIsCorrect """
        settings = LoessSettings(100)
        self.assertEqual(11, settings.getJump())
        self.assertEqual(1, settings.getDegree())
        self.assertEqual(101, settings.getWidth())

    # 
    # 	 * Test that cap was fixed after LOESS was extended to quadratic - this was broken for some time.
    # 	 
    def test_quadraticWorks(self):
        """ generated source for method quadraticWorks """
        settings = LoessSettings(13, 2, 1)
        self.assertEqual(2, settings.getDegree())
        self.assertEqual(13, settings.getWidth())
        self.assertEqual(1, settings.getJump())

    def test_jumpIsFlooredAtOne(self):
        """ generated source for method jumpIsFlooredAtOne """
        settings = LoessSettings(13, 2, -1)
        self.assertEqual(2, settings.getDegree())
        self.assertEqual(13, settings.getWidth())
        self.assertEqual(1, settings.getJump())

    def test_degreeIsFlooredAtZero(self):
        """ generated source for method degreeIsFlooredAtZero """
        settings = LoessSettings(13, -2)
        self.assertEqual(13, settings.getWidth())
        self.assertEqual(0, settings.getDegree())
        self.assertEqual(2, settings.getJump())

    def test_degreeIsCappedAt2(self):
        """ generated source for method degreeIsCappedAt2 """
        settings = LoessSettings(13, 10)
        self.assertEqual(13, settings.getWidth())
        self.assertEqual(2, settings.getDegree())
        self.assertEqual(2, settings.getJump())

    def test___str__Test(self):
        """ generated source for method toStringTest """
        settings = LoessSettings(23)
        str_ = settings.__str__()
        self.assertEqual("[width = 23, degree = 1, jump = 3]", str_)

if __name__ == '__main__':
    unittest.main()