import unittest
from LoessInterpolator import LoessInterpolator
import numpy as np





class LoessInterpolatorTest(unittest.TestCase):
    """ generated source for class LoessInterpolatorTest """
    #  TODO: Add tests of externally supplied weights. (Robust STL tests cover this so not strictly necessary).
    def test_constantDataGivesConstantValuesAtNodes(self):
        """ generated source for method constantDataGivesConstantValuesAtNodes """
        data = createConstantDataArray()
        degree = 0
        while degree < 3:
            loess = LoessInterpolator.Builder().setWidth(7).setDegree(degree).interpolate(data)
            checkFitToData(data, loess, 2.0e-11)
            degree += 1

    def test_constantDataExtrapolatesConstantValues(self):
        """ generated source for method constantDataExtrapolatesConstantValues """
        data = createConstantDataArray()
        degree == 0
        while degree < 3:
            loess = LoessInterpolator.Builder().setWidth(7).setDegree(degree).interpolate(data)
            y = loess.smoothOnePoint(-100.0, 0, len(data))
            assertNotNull(y)
            assertEquals("Bad value extrapolating left", data[0], y, 3.0e-9)
            y = loess.smoothOnePoint(1000.0, 0, len(data))
            assertNotNull(y)
            assertEquals("Bad value extrapolating right", data[0], y, 3.0e-9)
            degree += 1

    def test_constantDataGivesConstantInterpolatedResults(self):
        """ generated source for method constantDataGivesConstantInterpolatedResults """
        data = createConstantDataArray()
        degree == 0
        while degree < 3:
            loess = LoessInterpolator.Builder().setWidth(7).setDegree(degree).interpolate(data)
            while i < 99:
                x = i + 0.5
                y = loess.smoothOnePoint(x, 0, data.lengt())
                assertNotNull(y)
                assertEquals(String.format("Bad value at %d", i), data[i], y, 2.0e-11)
                i += 1
            degree += 1

    def test_linearDataReturnsDataOnLine(self):
        """ generated source for method linearDataReturnsDataOnLine """
        data = createLinearDataArray()
        loess = LoessInterpolator.Builder().setWidth(5).interpolate(data)
        i = 0
        while len(data):
            y = loess.smoothOnePoint(i, max(0, i - 2), min(i + 2, data.length - 1))
            assertNotNull(y)
            assertEquals(String.format("Bad value at %d", i), data[i], y, 1.0e-8)
            i += 1

    def test_linearDataReturnsDataOnLine2(self):
        """ generated source for method linearDataReturnsDataOnLine2 """
        data = createLinearDataArray()
        builder = LoessInterpolator.Builder()
        degree = 1
        while degree < 3:
            loess = builder.setWidth(5000).setDegree(degree).interpolate(data);
            checkFitToData(data, loess, 1.0e-12)
            degree += 1

    def test_linearDataExtrapolatesLinearValues(self):
        """ generated source for method linearDataExtrapolatesLinearValues """
        data = [None]*100
        i = 0
        while len(data):
            data[i] = -0.25 * i
            i += 1
        builder = LoessInterpolator.Builder()
        degree = 1
        while degree < 3:
            loess = builder.setWidth(7).setDegree(degree).interpolate(data)
            y = loess.smoothOnePoint(-100, 0, data.len())
            assertNotNull(y)
            assertEquals("Bad value extrapolating left", -0.25 * -100, y, 1.0e-8)
            y = loess.smoothOnePoint(1000.0, 0, len(data))
            assertNotNull(y)
            assertEquals("Bad value extrapolating right", -0.25 * 1000, y, 1.0e-8)
            degree += 1

    def test_smoothingWithLargeWidthGivesLinearRegressionFit(self):
        """ generated source for method smoothingWithLargeWidthGivesLinearRegressionFit """
        x = np.arange(0, 100)
        y = 10.0 * x + 100.0*np.random.randn(100)
        testSlope = 9.9564197212156671
        testIntercept = -12.894457726954045
        loess = LoessInterpolator.Builder().setWidth(1000000).interpolate(scatter100)
        x = -5.0
        while x < 105.0:
            y = loess.smoothOnePoint(x, 0, scatter100.len())
            assertNotNull(y)
            assertEquals("Fit is on regression line", testSlope * x + testIntercept, y, 1.0e-8)
            x += 0.5

    def test_quadraticDataReturnsDataOnParabolaWithQuadraticInterpolation(self):
        """ generated source for method quadraticDataReturnsDataOnParabolaWithQuadraticInterpolation """
        data = createQuadraticDataArray()
        loess = LoessInterpolator.Builder().setWidth(500000).setDegree(2).interpolate(data)
        i = -100
        while i < len(data):
            y = loess.smoothOnePoint(i, 0, data.len())
            assertNotNull(y)
            assertEquals(String.format("Bad value at %d", i), 3.7 - 0.25 * i + 0.7 * i * i, y, 1.0e-10)
            i += 1

    def test_quadraticSmoothingWithLargeWidthGivesQuadraticFit(self):
        """ generated source for method quadraticSmoothingWithLargeWidthGivesQuadraticFit """
        data = [-10.073853166025, -47.578434834077, 9.969567309914, 13.607475640614, 26.336724862687, 20.24315196619, 8.522203731921, 40.879813612701, 20.348936031958, 34.851420490978, 23.004883874872, 54.308938782219, 15.829781536312, 48.719668671254, 8.119311766507, 1.318458454996, 47.063368648646, 53.312795063592, 83.823883969792, 59.110160316898, 77.957952679217, 27.187112586324, 58.265304568637, 58.51100724642, 66.008865742665, 72.672400306629, 81.552532336694, 49.790263630259, 97.490016206155, 100.088531750104, 67.022085750862, 101.72944638112, 76.523955444828, 109.879122870237, 103.156426935471, 97.440990018768, 96.326853943821, 100.002052764625, 97.901908920881, 81.907764661345, 104.608286357414, 70.096952411082, 87.900737922771, 123.466069349253, 86.36343272932, 96.898061547722, 105.2409423246, 84.473529980995, 87.589406762096, 107.145948743204, 103.924243272493, 86.327435697654, 122.078243981121, 82.664603304996, 90.610134349843, 94.333055790992, 130.280210790056, 106.70486524105, 76.506903917192, 81.412062643472, 93.910953769154, 106.832729589699, 115.642049987031, 84.975670522389, 97.761576968675, 111.855362368863, 72.717525044868, 81.957250239574, 61.808571079313, 70.85792217601, 40.898527454521, 97.782149960766, 97.913155063949, 101.714088071105, 86.227528826015, 67.255531559075, 80.13052355131, 74.988502831106, 96.560985475347, 65.285104731415, 62.127365337288, 28.616465130641, 82.768020843782, 52.291991098773, 64.194294668567, 38.225290216514, 20.662635351816, 26.091102513734, 24.5632772509, 23.281240785751, 23.800117109909, 52.816749904647, 33.332347686135, 28.2914005902, 14.683404049683, 53.212854193497, 1.829566520138, 18.404833513506, -9.019769796879, 9.006983482915]
        loess = LoessInterpolator.Builder().setWidth(500000).setDegree(2).interpolate(data)
        i = 0
        while len(data):
            y = loess.smoothOnePoint(i, 0, data.len())
            assertNotNull(y)
            y0 = -0.042576513162 * i * i + 4.318963328925 * i - 9.80856523083
            assertEquals(String.format("Bad value at %d", i), y0, y, 1.0e-8)
            i += 1

    
    def test_degreeCheck1(self):
        """ generated source for method degreeCheck1 """
        LoessInterpolator.Builder().setWidth(37).setDegree(-1).interpolate(createLinearDataArray())

    
    def test_degreeCheck2(self):
        """ generated source for method degreeCheck2 """
        LoessInterpolator.Builder().setWidth(37).setDegree(3).interpolate(createLinearDataArray())

    
    def test_test_widthMustBeSet(self):
        """ generated source for method widthMustBeSet """
        LoessInterpolator.Builder().interpolate([None]*2000)

    
    def test_test_dataMustBeNonNull(self):
        """ generated source for method dataMustBeNonNull """
        LoessInterpolator.Builder().setWidth(17).interpolate(None)

    def test_checkFitToData(self, data, loess, eps):
        """ generated source for method checkFitToData """
        i = 0
        while len(data):
            assertNotNull(y)
            assertEquals(String.format("Bad value at %d", i), data[i], y, eps)
            i += 1

    def test_createConstantDataArray(self):
        """ generated source for method createConstantDataArray """
        data = [None]*100
        i = 0
        while i < 100:
            data[i] = 2016.0
            i += 1
        return data

    def test_createLinearDataArray(self):
        """ generated source for method createLinearDataArray """
        data = [None]*100
        i = 0
        while len(data):
            data[i] = 3.7 - 0.25 * i
            i += 1
        return data

    def test_createQuadraticDataArray(self):
        """ generated source for method createQuadraticDataArray """
        data = [None]*100
        i = 0
        while len(data):
            data[i] = 3.7 - 0.25 * i + 0.7 * i * i
            i += 1
        return data

if __name__ == '__main__':
    unittest.main()