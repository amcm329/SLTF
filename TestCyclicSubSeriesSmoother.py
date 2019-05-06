from CyclicSubSeriesSmoother import CyclicSubSeriesSmoother
import math
import unittest
import numpy as np

class CyclicSubSeriesSmootherTest(unittest.TestCase):

      #Smoothing the cyclic sub-series extends the data one period in each direction. Ensure that when the data is 
      #linear, that the extrapolations are linear.
      def test_TrendingSinusoidExtrapolationTest(self):
          period = 24
          data = np.array(2 * period)
          dx = 2 * math.pi / period
          for i in range (len(data)):
              amplitude = int(10 - i / period)
              data[i] = float(amplitude * math.sin(i * dx))

          extendedData = np.array(4 * period)
          builder = Builder().setWidth(7) #Sub-cycle data is linear so width shouldn't matter
          sssmoother = builder.setDataLength(data.length).setPeriodicity(period).extrapolateForwardAndBack(1).build()
          sssmoother.smoothSeasonal(data, extendedData, null)

          for i in range(len(extendedData)):
              amplitude = int(11 - i / period) #An extra for the extrapolation before.
              value = float(amplitude * math.sin(i * dx))
              self.assertAlmostEqual(value, extendedData[i], 1.0e-11, "test point {0}".format(i))


      def test_shouldExtrapolateFourPeriodsForwards(self):
          period = 24
          data = np.array(2 * period) 
          dx = 2 * math.pi / period
          for i in range (len(data)):
              amplitude = int(10 - i / period)
              data[i] = float(amplitude * math.sin(i * dx))

          extendedData = np.array(6 * period)
          builder = Builder()
          builder = builder.setWidth(7) #Sub-cycle data is linear so width shouldn't matter
          builder = builder.extrapolateForwardOnly(4)
          sssmoother = builder.setDataLength(data.length).setPeriodicity(period).build();

          sssmoother.smoothSeasonal(data, extendedData, null);

          for i in range(len(extendedData)):
              amplitude = int(10 - i / period)
              value = float(amplitude * math.sin(i * dx))
              self.assertEquals(value, extendedData[i], 1.0e-11,"test point {0}".format(i))


      def test_shouldExtrapolateTwoPeriodsBackwardAndTwoPeriodsForward(self):
          period = 24
          data = np.array([2 * period])
          dx = float(2 * math.pi / period)

          for i in range (len(data)):
              amplitude = int(10 - i / period)
              data[i] = float(amplitude * math.sin(i * dx))

          extendedData = np.array(6 * period)
          builder = Builder()
          builder = builder.setWidth(7) #Sub-cycle data is linear so width shouldn't matter
          builder = builder.setNumPeriodsForward(2).setNumPeriodsBackward(2)
             
          sssmoother = builder.setDataLength(data.length).setPeriodicity(period).build()
 
          sssmoother.smoothSeasonal(data, extendedData, null)

          for i in range(len(extendedData)):
              amplitude = int(12 - i / period) #Two extra for the extrapolation before.
              value = float(amplitude * math.sin(i * dx))
              self.assertEquals(value, extendedData[i], 1.0e-11,"test point {0}".format(i))


      def test_degreeMustBePositive(self):
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setDegree(-1)
	

      def test_degreeMustBeLessThanThree(self): 
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setDegree(3)
	

      def test_widthMustBeSet(self): 
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setDataLength(100).extrapolateForwardAndBack(1).setPeriodicity(12).build()

    
      def test_dataLengthMustBeSet(self):
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setWidth(3).extrapolateForwardAndBack(1).setPeriodicity(12).build()


      def test_periodMustBeSet(self):
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setDataLength(100).extrapolateForwardAndBack(1).setWidth(11).build()
	

      def test_backwardExtrapolationMustBeSet(self):
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setDataLength(100).setNumPeriodsForward(1).setWidth(11).setPeriodicity(12).build()


      def test_forwardExtrapolationMustBeSet(self):
          with self.assertRaises(ValueError):
               builder = Builder()
               builder.setDataLength(100).setNumPeriodsBackward(1).setWidth(11).setPeriodicity(12).build()


      #def test___str__Test(self):
      #    """ generated source for method toStringTest """
      #    settings = LoessSettings(23)
      #    str_ = settings.__str__()
      #    self.assertEqual("[width = 23, degree = 1, jump = 3]", str_)

if __name__ == '__main__':
    unittest.main()
