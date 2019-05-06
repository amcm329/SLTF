import unittest
from LoessInterpolator import LoessInterpolator
import numpy as np


class LoessInterpolatorTest(unittest.TestCase):
    """ generated source for class LoessInterpolatorTest """
    #  TODO: Add tests of externally supplied weights. (Robust STL tests cover this so not strictly necessary).
    def test_constantDataGivesConstantValuesAtNodes(self):
        """ generated source for method constantDataGivesConstantValuesAtNodes """
        data = self.createConstantDataArray()
        degree = 0
        while degree < 3:
            loess = LoessInterpolator.Builder().setWidth(7).setDegree(degree).interpolate(data)
            self.test_checkFitToData(data, loess, 2.0e-11)
            degree += 1

    def test_constantDataExtrapolatesConstantValues(self):
        """ generated source for method constantDataExtrapolatesConstantValues """
        data = self.createConstantDataArray()
        degree = 0
        while degree < 3:
            loess = LoessInterpolator.Builder().setWidth(7).setDegree(degree).interpolate(data)
            y = loess.smoothOnePoint(-100.0, 0, len(data)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(data[0], y, msg="Bad value extrapolating left", delta=3.0e-9)
            y = loess.smoothOnePoint(1000.0, 0, len(data)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(data[0], y, msg="Bad value extrapolating right", delta=3.0e-9)
            degree += 1

    def test_constantDataGivesConstantInterpolatedResults(self):
        """ generated source for method constantDataGivesConstantInterpolatedResults """
        data = self.createConstantDataArray()
        degree = 0
        while degree < 3:
            loess = LoessInterpolator.Builder().setWidth(7).setDegree(degree).interpolate(data)
            i = 0
            while i < 99:
                x = i + 0.5
                y = loess.smoothOnePoint(x, 0, len(data)-1)
                self.assertIsNotNone(y)
                self.assertAlmostEqual(data[i], y, msg="Bad value at {}".format(i), delta=2.0e-11)
                i += 1
            degree += 1

    def test_linearDataReturnsDataOnLine(self):
        """ generated source for method linearDataReturnsDataOnLine """
        data = self.createLinearDataArray()
        loess = LoessInterpolator.Builder().setWidth(5).interpolate(data)
        i = 0
        while len(data):
            y = loess.smoothOnePoint(i, max(0, i - 2), min(i + 2, len(data) - 1))
            self.assertIsNotNone(y)
            self.assertAlmostEqual(data[i], y, msg="Bad value at {}".format(i), delta=1.0e-8)
            i += 1

    def test_linearDataReturnsDataOnLine2(self):
        """ generated source for method linearDataReturnsDataOnLine2 """
        data = self.createLinearDataArray()
        builder = LoessInterpolator.Builder()
        degree = 1
        while degree < 3:
            loess = builder.setWidth(5000).setDegree(degree).interpolate(data);
            self.test_checkFitToData(data, loess, 1.0e-12)
            degree += 1

    def test_linearDataExtrapolatesLinearValues(self):
        """ generated source for method linearDataExtrapolatesLinearValues """
        data = np.zeros(100)
        i = 0
        while i<len(data):
            data[i] = -0.25 * i
            i += 1
        builder = LoessInterpolator.Builder()
        degree = 1
        while degree < 3:
            loess = builder.setWidth(7).setDegree(degree).interpolate(data)
            y = loess.smoothOnePoint(-100, 0, len(data)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(-0.25 * -100, y, msg="Bad value extrapolating left", delta=1.0e-8)
            y = loess.smoothOnePoint(1000.0, 0, len(data)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(-0.25 * 1000, y, msg="Bad value extrapolating right", delta=1.0e-8)
            degree += 1

    def test_smoothingWithLargeWidthGivesLinearRegressionFit(self):
        """ generated source for method smoothingWithLargeWidthGivesLinearRegressionFit """
        scatter100 = [45.0641826945, 69.6998783993, 9.81903951235, -75.4079441854,
                53.7430205615, 12.1359388898, 84.972441255, 194.467452805, 182.276035711, 128.161856616, 147.021732433,
                -40.6773185264, 41.1575417261, 111.04115761, 75.0179056538, 278.946359666, 93.3453251262,
                103.779785975, 252.750915429, 252.636103208, 457.859165335, 143.021758047, 79.343240193, 280.969547174,
                35.650257308, 157.656673765, 29.6984404613, 141.980264706, 263.465758806, 346.309482972, 330.044915761,
                135.019120067, 211.801092316, 198.186646037, 206.088498967, 510.89412974, 332.076915483, 530.524264511,
                298.21175481, 234.317252809, 573.836352739, 382.708235416, 340.090947574, 452.475239395, 576.134135134,
                536.703405146, 545.033194307, 479.525083559, 368.551750848, 588.429801268, 528.672000843,
                507.301073925, 432.749370682, 600.239380863, 567.328853536, 481.544306962, 510.42118889, 456.519971302,
                565.839651322, 510.505759788, 503.2514057, 491.279917041, 642.319449309, 573.019058995, 574.709858012,
                597.316826688, 602.361341448, 622.312708681, 506.669245531, 640.120714982, 699.793133288,
                672.969830555, 656.645808774, 901.375994679, 573.903581507, 906.472771298, 719.604429516,
                759.262994619, 786.970584025, 717.422383977, 899.007418786, 745.516032607, 748.049043698, 876.99080793,
                810.985707949, 888.762045358, 947.030030816, 1007.48402395, 830.251382179, 921.078927761,
                810.212273661, 926.740829016, 787.965498372, 944.230542154, 808.215987256, 1044.74526488,
                866.568085766, 1068.6479395, 776.566771785, 1190.32090194]

        testSlope = 9.9564197212156671
        testIntercept = -12.894457726954045
        loess = LoessInterpolator.Builder().setWidth(1000000).interpolate(scatter100)
        x = -5.0
        while x < 105.0:
            y = loess.smoothOnePoint(x, 0, len(scatter100)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(testSlope * x + testIntercept, y, msg="Fit is on regression line", delta=1.0e-8)
            x += 0.5

    def test_quadraticDataReturnsDataOnParabolaWithQuadraticInterpolation(self):
        """ generated source for method quadraticDataReturnsDataOnParabolaWithQuadraticInterpolation """
        data = self.createQuadraticDataArray()
        loess = LoessInterpolator.Builder().setWidth(500000).setDegree(2).interpolate(data)
        i = -100
        while i < len(data):
            y = loess.smoothOnePoint(i, 0, len(data)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(3.7 - 0.25 * i + 0.7 * i * i, y, msg="Bad value at {}".format(i), delta=1.0e-10)
            i += 1

    def test_quadraticSmoothingWithLargeWidthGivesQuadraticFit(self):
        """ generated source for method quadraticSmoothingWithLargeWidthGivesQuadraticFit """
        data = [-10.073853166025, -47.578434834077, 9.969567309914, 13.607475640614, 26.336724862687, 20.24315196619, 
        8.522203731921, 40.879813612701, 20.348936031958, 34.851420490978, 23.004883874872, 54.308938782219, 15.829781536312, 
        48.719668671254, 8.119311766507, 1.318458454996, 47.063368648646, 53.312795063592, 83.823883969792, 59.110160316898, 
        77.957952679217, 27.187112586324, 58.265304568637, 58.51100724642, 66.008865742665, 72.672400306629, 81.552532336694, 
        49.790263630259, 97.490016206155, 100.088531750104, 67.022085750862, 101.72944638112, 76.523955444828, 109.879122870237, 
        103.156426935471, 97.440990018768, 96.326853943821, 100.002052764625, 97.901908920881, 81.907764661345, 104.608286357414, 
        70.096952411082, 87.900737922771, 123.466069349253, 86.36343272932, 96.898061547722, 105.2409423246, 84.473529980995, 
        87.589406762096, 107.145948743204, 103.924243272493, 86.327435697654, 122.078243981121, 82.664603304996, 90.610134349843, 
        94.333055790992, 130.280210790056, 106.70486524105, 76.506903917192, 81.412062643472, 93.910953769154, 106.832729589699, 
        115.642049987031, 84.975670522389, 97.761576968675, 111.855362368863, 72.717525044868, 81.957250239574, 61.808571079313, 
        70.85792217601, 40.898527454521, 97.782149960766, 97.913155063949, 101.714088071105, 86.227528826015, 67.255531559075, 
        80.13052355131, 74.988502831106, 96.560985475347, 65.285104731415, 62.127365337288, 28.616465130641, 82.768020843782, 
        52.291991098773, 64.194294668567, 38.225290216514, 20.662635351816, 26.091102513734, 24.5632772509, 23.281240785751, 
        23.800117109909, 52.816749904647, 33.332347686135, 28.2914005902, 14.683404049683, 53.212854193497, 1.829566520138, 
        18.404833513506, -9.019769796879, 9.006983482915]
        loess = LoessInterpolator.Builder().setWidth(500000).setDegree(2).interpolate(data)
        i = 0
        while len(data):
            y = loess.smoothOnePoint(i, 0, len(data)-1)
            self.assertIsNotNone(y)
            y0 = -0.042576513162 * i * i + 4.318963328925 * i - 9.80856523083
            self.assertAlmostEqual(y0, y, msg="Bad value at {}".format(i), delta=1.0e-8)
            i += 1

    
    def test_degreeCheck1(self):
        """ generated source for method degreeCheck1 """
        with self.assertRaises(ValueError):
            LoessInterpolator.Builder().setWidth(37).setDegree(-1).interpolate(createLinearDataArray())

    
    def test_degreeCheck2(self):
        """ generated source for method degreeCheck2 """
        with self.assertRaises(ValueError):
            LoessInterpolator.Builder().setWidth(37).setDegree(3).interpolate(createLinearDataArray())

    
    def test_test_widthMustBeSet(self):
        """ generated source for method widthMustBeSet """
        with self.assertRaises(ValueError):
            LoessInterpolator.Builder().interpolate([None]*2000)

    
    def test_test_dataMustBeNonNull(self):
        """ generated source for method dataMustBeNonNull """
        with self.assertRaises(ValueError):
            LoessInterpolator.Builder().setWidth(17).interpolate(None)

    def test_checkFitToData(self, data, loess, eps):
        """ generated source for method checkFitToData """
        i = 0
        while i<len(data):
            y = loess.smoothOnePoint(i, 0, len(data)-1)
            self.assertIsNotNone(y)
            self.assertAlmostEqual(data[i], y, msg="Bad value at {}".format(i), delta=eps)
            i += 1

    def createConstantDataArray(self):
        """ generated source for method createConstantDataArray """
        data = np.empty(100)
        i = 0
        while i < 100:
            data[i] = 2016.0
            i += 1
        return data

    def createLinearDataArray(self):
        """ generated source for method createLinearDataArray """
        data = np.empty(100)
        i = 0
        while i<len(data):
            data[i] = 3.7 - 0.25 * i
            i += 1
        return data

    def createQuadraticDataArray(self):
        """ generated source for method createQuadraticDataArray """
        data = np.empty(100)
        i = 0
        while i<len(data):
            data[i] = 3.7 - 0.25 * i + 0.7 * i * i
            i += 1
        return data

if __name__ == '__main__':
    unittest.main()