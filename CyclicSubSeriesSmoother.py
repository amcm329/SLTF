import math
import numpy as np
from LoessSmoother import LoessSmoother

class CyclicSubSeriesSmoother:

    """
     Create a cyclic sub-series smoother with the specified properties.
                                                                            
     @param width                           width of the LOESS smoother
     @param degree                          degree of the LOESS smoother
     @param jump                            jump to use in LOESS smoothing
     @param dataLength                      length of the input data
     @param periodicity                     length of the cyclic period
     @param numPeriodsToExtrapolateBackward number of periods to extrapolate backward
     @param numPeriodsToExtrapolateForward  numbers of periods to extrapolate forward
	""" 
    def __init__(self, width, degree, jump, dataLength, periodicity, numPeriodsToExtrapolateBackward, numPeriodsToExtrapolateForward):
        self._fRawCyclicSubSeries = np.array(1)
        self._fSmoothedCyclicSubSeries = np.array(1)
        self._fSubSeriesWeights = np.array(1)

        self._fPeriodLength = 0
        self._fNumPeriods = 0
        self._fRemainder = 0
        self._fNumPeriodsToExtrapolateBackward = 0
        self._fNumPeriodsToExtrapolateForward = 0

        self._fWidth = 0
        self._fLoessSmootherFactory = None
		
        self._fWidth = width

        ######
        self._fLoessSmootherFactory =  LoessSmoother.Builder().setWidth(width).setJump(jump).setDegree(degree)
        self._fPeriodLength = periodicity
        self._fNumPeriods = dataLength / periodicity
        self._fRemainder = dataLength % periodicity
        self._fNumPeriodsToExtrapolateBackward = numPeriodsToExtrapolateBackward
        self._fNumPeriodsToExtrapolateForward = numPeriodsToExtrapolateForward

        #ver si se crea un [] o de una vez un [] con elementos de tamanho periodicity
<<<<<<< HEAD
        self._fRawCyclicSubSeries = np.array(int(periodicity))

        #ver si se crea un [] o de una vez un [] con elementos de tamanho periodicity
        self._fSmoothedCyclicSubSeries = np.array(int(periodicity)])

        #ver si se crea un [] o de una vez un [] con elementos de tamanho periodicity
        self._fSubSeriesWeights = np.array(int(periodicity))
=======
        self._fRawCyclicSubSeries = [[]]*periodicity

        #ver si se crea un [] o de una vez un [] con elementos de tamanho periodicity
        self._fSmoothedCyclicSubSeries = [[]]*periodicity

        #ver si se crea un [] o de una vez un [] con elementos de tamanho periodicity
        self._fSubSeriesWeights = [[]]*periodicity
>>>>>>> c0a0b23c28ebc102983e8c9bdda358fabcc0322d

        """
         Bookkeeping: Write the data length as
            
         n = m * periodicity + r

         where r < periodicity. The first r sub-series will have length m + 1 and the remaining will have length m.
         Another way to look at this is that the cycle length is:

         cycleLength = (n - p - 1) / periodicity + 1

         where p is the index of the cycle that we're currently in.
        """
            
        for period in range(periodicity):
            #importante con el ++period

            seriesLength = self._fNumPeriods + 1 if period < self._fRemainder else self._fNumPeriods

            #Lo mismo, hacer esa verificacion aqui para poder hacer la "matriz" que se pide en Java 
            self._fRawCyclicSubSeries[period] = np.zeros(int(seriesLength))
            self._fSmoothedCyclicSubSeries[period] = np.empty(int(self._fNumPeriodsToExtrapolateBackward + seriesLength +     self._fNumPeriodsToExtrapolateForward))
            self._fSubSeriesWeights[period] = np.empty(int(seriesLength))
			  
			  
    """
     Run the cyclic sub-series smoother on the specified data, with the specified weights (ignored if null). The
     sub-series are reconstructed into a single series in smoothedData.

     @param rawData      input data
     @param smoothedData output data
     @param weights      weights to use in the underlying interpolator; ignored if null.
    """
    def smoothSeasonal(self, rawData, smoothedData, weights):
        self.extractRawSubSeriesAndWeights(rawData, weights)
        self.computeSmoothedSubSeries(weights != None)
        self.reconstructExtendedDataFromSubSeries(smoothedData)


    def computeSmoothedSubSeries(self, useResidualWeights):
        
        #importante lo del ++period
        for period in range(self._fPeriodLength):
            weights = self._fSubSeriesWeights[period] if useResidualWeights else None
            rawData = self._fRawCyclicSubSeries[period]
            smoothedData = self._fSmoothedCyclicSubSeries[period]
            self.smoothOneSubSeries(weights, rawData, smoothedData)


    def extractRawSubSeriesAndWeights(self, data, weights):
          
        #++period
        for period in range(self._fPeriodLength:
              period += 1
              cycleLength =  (self._fNumPeriods + 1) if period < self._fRemainder else self._fNumPeriods
              i = 0

              #period ++
              while i < cycleLength:
                    i += 1 
                    self._fRawCyclicSubSeries[period][i] = data[i * self._fPeriodLength + period]
                    if weights != None: 
                       self._fSubSeriesWeights[period][i] = weights[i * self._fPeriodLength + period]


    def reconstructExtendedDataFromSubSeries(self, data):
        period = 0 
        #Copy this smoothed cyclic sub-series to the extendedSeasonal work array.
        while period < self._fPeriodLength:
              #++period
              period += 1
              cycleLength = (self._fNumPeriods + 1) if period < self._fRemainder else self._fNumPeriods
              i = 0
              while i < self._fNumPeriodsToExtrapolateBackward + cycleLength + self._fNumPeriodsToExtrapolateForward:
                    #++i
                    i += 1 
                    data[i * self._fPeriodLength + period] = self._fSmoothedCyclicSubSeries[period][i]
			

    """
     Use LOESS interpolation on each of the cyclic sub-series (e.g. in monthly data, smooth the Januaries, Februaries, etc.).

     @param weights      external weights for interpolation
     @param rawData      input data to be smoothed
     @param smoothedData output smoothed data
    """
    def smoothOneSubSeries(self, weights, rawData, smoothedData): 
        cycleLength = len(rawData)
 
        #Smooth the cyclic sub-series with LOESS and then extrapolate one place beyond each end.
        smoother = self._fLoessSmootherFactory.setData(rawData).setExternalWeights(weights).build()

        """
         public static void arraycopy(Object source_arr, int sourcePos,
                        Object dest_arr, int destPos, int len)
         Parameters : 
          source_arr : array to be copied from
          sourcePos : starting position in source array from where to copy
          dest_arr : array to be copied in
          destPos : starting position in destination array, where to copy in
          len : total no. of components to be copied.
        """
        #Copy, shifting by 1 to leave room for the extrapolated point at the beginning.
        #System.arraycopy(smoother.smooth(), 0, smoothedData, self._fNumPeriodsToExtrapolateBackward, cycleLength)

        smoothedData[destPos:destPos + cycleLength] = smoother.smooth()[self._fNumPeriodsToExtrapolateBackward:self._fNumPeriodsToExtrapolateBackward + cycleLength]
          
        interpolator = smoother.getInterpolator()

        #Extrapolate from the leftmost "width" points to the "-1" position
        left = 0;
        right = left + self._fWidth - 1;
        right = math.min(right, cycleLength - 1)
        leftValue = self._fNumPeriodsToExtrapolateBackward

        #es menor e igual
        for i in range(1, self._fNumPeriodsToExtrapolateBackward + 1):
            ys = interpolator.smoothOnePoint(-i, left, right)
            smoothedData[leftValue - i] = smoothedData[leftValue] if ys == None else ys

            #Extrapolate from the rightmost "width" points to the "length" position (one past the array end).
            right = cycleLength - 1
            left = right - sel._fWidth + 1
            left = math.max(0, left)
            rightValue = sel._fNumPeriodsToExtrapolateBackward + right

            #es menor e igual
            for i in range(1,self._fNumPeriodsToExtrapolateForward + 1):
                ys = interpolator.smoothOnePoint(right + i, left, right)
                smoothedData[rightValue + i] = smoothedData[rightValue] if ys == None else ys
				

    """
    Use Builder to simplify complex construction patterns.
    """
    class Builder: 

        def __init__(self):
            self._fWidth = None
            self._fDataLength = None
            self._fPeriodicity = None
            self._fNumPeriodsBackward = None
            self._fNumPeriodsForward = None
            self._fDegree = 1;
            self._fJump = 1;

        """
         Set the width of the LOESS smoother used to smooth each seasonal sub-series.
	
         @param width width of the LOESS smoother
         @return this
	    """
        def setWidth(self, width):
            self._fWidth = width
            return self


        """
         Set the degree of the LOESS smoother used to smooth each seasonal sub-series.
         
         @param degree degree of the LOESS smoother
         @return this
	    """
        def setDegree(self, degree):
            if degree < 0 or degree > 2:
               raise ValueError("Degree must be 0, 1 or 2")

            self._fDegree = degree
            return self


        """
         Set the jump (number of points to skip) between LOESS interpolations when smoothing the seasonal sub-series.
         <p>
         Defaults to 1 (computes LOESS interpolation at each point).

         @param jump jump (number of points to skip) in the LOESS smoother
         @return this
        """
        def setJump(self, jump):
            self._fJump = jump
            return self


        """
         Set the total length of the data that will be deconstructed into cyclic sub-series.

         @param dataLength total length of the data
         @return this
        """	
        def setDataLength(self, dataLength):
            self._fDataLength = dataLength
            return self
		

        """
         Set the period of the data's seasonality.

         @param periodicity number of data points in each season or period
         @return this
        """
        def setPeriodicity(self, periodicity):
            self._fPeriodicity = periodicity
            return self


        """
         Construct a smoother that will extrapolate forward only by the specified number of periods.
	
         @param periods number of periods to extrapolate
         @return this
        """
        def extrapolateForwardOnly(self, periods):
            self._fNumPeriodsForward = periods
            self._fNumPeriodsBackward = 0
            return self
	
	
        """
         Construct a smoother that extrapolates forward and backward by the specified number of periods.
       
         @param periods number of periods to extrapolate
         @return this
        """
        def extrapolateForwardAndBack(self, periods): 
            self._fNumPeriodsForward = periods
            self._fNumPeriodsBackward = periods
            return self
		

        """
         Set the number of periods to extrapolate forward.
         <p>
         Defaults to 1.

         @param periods number of periods to extrapolate
         @return this
     	"""
        def setNumPeriodsForward(self, periods): 
            self._fNumPeriodsForward = periods
            return self
		

        """
         Set the number of periods to extrapolate backward.
         <p>
         Defaults to 1.

         @param periods number of periods to extrapolate
         @return this
        """
        def setNumPeriodsBackward(self, periods):
            self._fNumPeriodsBackward = periods
            return self
	
	
        """
         Build the sub-series smoother.
           
         @return new CyclicSubSeriesSmoother

        """
        def build(self):
            self._checkSanity()
            return CyclicSubSeriesSmoother(
                                           self._fWidth, 
                                           self._fDegree, 
                                           self._fJump, 
                                           self._fDataLength, 
                                           self._fPeriodicity,
					   self._fNumPeriodsBackward, 
                                           self._fNumPeriodsForward
                                           )
		

        def _checkSanity(self):
            if self._fWidth == None:
                raise ValueError("CyclicSubSeriesSmoother.Builder: setWidth must be called before building the smoother.")

            if self._fPeriodicity == None:
                raise ValueError("CyclicSubSeriesSmoother.Builder: setPeriodicity must be called before building the smoother.")

            if self._fDataLength == None:
                raise ValueError("CyclicSubSeriesSmoother.Builder: setDataLength must be called before building the smoother.")

            if self._fNumPeriodsBackward == None or self._fNumPeriodsForward == None:
                raise ValueError("CyclicSubSeriesSmoother.Builder: Extrapolation settings must be provided.")
