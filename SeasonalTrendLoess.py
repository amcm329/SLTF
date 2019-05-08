""" generated source for module SeasonalTrendLoess """
import numpy as np
from LoessSettings import LoessSettings
from LoessInterpolator import LoessInterpolator
from LoessSmoother import LoessSmoother
from CyclicSubSeriesSmoother import CyclicSubSeriesSmoother  
from TimeSeriesUtilities import TimeSeriesUtilities

# 
#  * Python implementation of the Seasonal-Trend-Loess algorithm for evenly spaced data. This is basically a direct port of
#  * the RATFOR from the netlib stl package.
#  * Inspired by the code created by Jim Crotinger on 18-Apr-2016.
#  
class SeasonalTrendLoess:

    fData = []

    fDecomposition = None

    fPeriodLength = None
    fSeasonalSettings = None
    fTrendSettings = None
    fLowpassSettings = None
    fInnerIterations = None
    fRobustIterations = None

    fDetrend = []
    fExtendedSeasonal = []

    fDeSeasonalized = []

    fCyclicSubSeriesSmoother = None
    fLoessSmootherFactory = None
    fLowpassLoessFactory = None

    # 
    #Builder class for SeasonalTrendLoess decomposition
    # 	 
    class Builder:
        fPeriodLength = None

        fSeasonalWidth = None
        fSeasonalJump = None
        fSeasonalDegree = None

        fTrendWidth = None
        fTrendJump = None
        fTrendDegree = None

        fLowpassWidth = None
        fLowpassJump = None
        fLowpassDegree = 1

        #  Following the R interface, we default to "non-robust"
        fInnerIterations = 2
        fRobustIterations = 0

        #  Following the R interface, we implement a "periodic" flag that defaults to false.
        fPeriodic = False
        fFlatTrend = False
        fLinearTrend = False

        # 
        # 		 * Set the period length for the STL seasonal decomposition.
        # 		 * Required - no default.
        # 		 *
        # 		 * @param period period length (number of data points in each season or period)
        # 		 * @return self
        # 		 
        def setPeriodLength(self, period):
            """ generated source for method setPeriodLength """
            if period < 2:
                raise ValueError("periodicity must be at least 2")

            self.fPeriodLength = period
            return self

        # 
        # 		 * Set the LOESS width (in data points) used to smooth the seasonal sub-series.
        # 		 * Required unless setPeriodic is called.
        # 		 *
        # 		 * @param width LOESS width for the seasonal sub-series
        # 		 * @return self
        # 		 
        def setSeasonalWidth(self, width):
            """ generated source for method setSeasonalWidth """
            self.fSeasonalWidth = width
            return self

        # 
        # 		 * Set the LOESS degree used to smooth the seasonal sub-series.
        # 		 * Defaults to 1.
        # 		 *
        # 		 * @param degree LOESS degree for the seasonal sub-series
        # 		 * @return self
        # 		 
        def setSeasonalDegree(self, degree):
            """ generated source for method setSeasonalDegree """
            self.fSeasonalDegree = degree
            return self

        # 
        # 		 * Set the jump (number of points to skip) between LOESS interpolations when smoothing the seasonal sub-series.
        # 		 * Defaults to 10% of the smoother width.
        # 		 *
        # 		 * @param jump LOESS jump (number of points to skip) for the seasonal sub-series
        # 		 * @return self
        # 		 
        def setSeasonalJump(self, jump):
            """ generated source for method setSeasonalJump """
            self.fSeasonalJump = jump
            return self

        # 
        # 		 * Set the LOESS width (in data points) used to smooth the trend.
        # 		 * Defaults to (1.5 * periodLength / (1 - 1.5 / seasonalWidth) + 0.5)
        # 		 *
        # 		 * @param width LOESS with for the trend component
        # 		 * @return self
        # 		 
        def setTrendWidth(self, width):
            """ generated source for method setTrendWidth """
            self.fTrendWidth = width
            return self

        # 
        # 		 * Set the LOESS degree used to smooth the trend.
        # 		 * Defaults to 1.
        # 		 *
        # 		 * @param degree LOESS degree for the trend component
        # 		 * @return self
        # 		 
        def setTrendDegree(self, degree):
            """ generated source for method setTrendDegree """
            self.fTrendDegree = degree
            return self

        # 
        # 		 * Set the jump (number of points to skip) between LOESS interpolations used when smoothing the trend.
        # 		 * Defaults to 10% of the smoother width.
        # 		 *
        # 		 * @param jump LOESS jump (number of points to skip) for the trend component
        # 		 * @return self
        # 		 
        def setTrendJump(self, jump):
            """ generated source for method setTrendJump """
            self.fTrendJump = jump
            return self

        # 
        # 		 * Set the LOESS width (in data points) used by the low-pass filter step.
        # 		 * Defaults to the period length.
        # 		 *
        # 		 * @param width LOESS width for the low-pass step
        # 		 * @return self
        # 		 
        def setLowpassWidth(self, width):
            """ generated source for method setLowpassWidth """
            self.fLowpassWidth = width
            return self

        # 
        # 		 * Set the LOESS degree used by the low-pass filter step.
        # 		 * Defaults to 1.
        # 		 *
        # 		 * @param degree LOESS degree for the low-pass step
        # 		 * @return self
        # 		 
        def setLowpassDegree(self, degree):
            """ generated source for method setLowpassDegree """
            self.fLowpassDegree = degree
            return self

        # 
        # 		 * Set the jump (number of points to skip) between LOESS interpolations used by the low-pass filter step.
        # 		 * Defaults to 10% of the smoother width.
        # 		 *
        # 		 * @param jump LOESS jump (number of points to skip) for the low-pass step
        # 		 * @return self
        # 		 
        def setLowpassJump(self, jump):
            """ generated source for method setLowpassJump """
            self.fLowpassJump = jump
            return self

        # 
        # 		 * Set the number of STL inner iterations.
        # 		 * Required, but also set by setRobust, setNonRobust, setRobustFlag.
        # 		 *
        # 		 * @param ni number of inner iterations
        # 		 * @return self
        # 		 
        def setInnerIterations(self, ni):
            """ generated source for method setInnerIterations """
            self.fInnerIterations = ni
            return self

        # 
        # 		 * Set the number of STL robustness (outer) iterations.
        # 		 * Required, but also set by setRobust, setNonRobust, setRobustFlag.
        # 		 *
        # 		 * @param no number of outer iterations
        # 		 * @return self
        # 		 
        def setRobustnessIterations(self, no):
            """ generated source for method setRobustnessIterations """
            self.fRobustIterations = no
            return self

        # 
        # 		 * Set the default robust STL iteration counts (15 robustness iterations, 1 inner iteration).
        # 		 *
        # 		 * @return self
        # 		 
        def setRobust(self):
            """ generated source for method setRobust """
            self.fInnerIterations = 1
            self.fRobustIterations = 15
            return self

        # 
        # 		 * Set the default non-robust STL iteration counts (0 robustness iterations, 2 inner iterations).
        # 		 *
        # 		 * @return self
        # 		 
        def setNonRobust(self):
            """ generated source for method setNonRobust """
            self.fInnerIterations = 2
            self.fRobustIterations = 0
            return self

        # 
        # 		 * Set the robustness according to a flag; e.g. setRobust if true, setNonRobust if false.
        # 		 *
        # 		 * @param robust true to be robust
        # 		 * @return self
        # 		 
        def setRobustFlag(self, robust):
            """ generated source for method setRobustFlag """
            return self.setRobust() if robust else self.setNonRobust()

        # 
        # 		 * Constrain the seasonal component to be exactly periodic.
        # 		 *
        # 		 * @return self
        # 		 
        def setPeriodic(self):
            """ generated source for method setPeriodic """
            self.fPeriodic = True
            return self

        # 
        # 		 * Set the trend smoother force a flat trend. (Degree == 0, Large Loess Width)
        # 		 *
        # 		 * @return self
        # 		 
        def setFlatTrend(self):
            """ generated source for method setFlatTrend """
            self.fLinearTrend = False
            self.fFlatTrend = True
            return self

        # 
        # 		 * Set the trend smoother force a linear trend. (Degree == 1, Large Loess Width)
        # 		 *
        # 		 * @return this
        # 		 
        def setLinearTrend(self):
            """ generated source for method setLinearTrend """
            self.fLinearTrend = True
            self.fFlatTrend = False
            return self

        # 
        # 		 * Construct the smoother.
        # 		 *
        # 		 * @param data the data to be smoothed
        # 		 * @return a new SeasonalTrendLoess object
        # 		 
        def buildSmoother(self, data):
            self.sanityCheck(data)

            if self.fPeriodic:
                self.fSeasonalWidth = 100 * len(data)
                self.fSeasonalDegree = 0
            elif self.fSeasonalDegree is None:
                self.fSeasonalDegree = 1

            seasonalSettings = LoessSettings(self.fSeasonalWidth, self.fSeasonalDegree, self.fSeasonalJump)

            if self.fFlatTrend:
                self.fTrendWidth = 100 * self.fPeriodLength *len(data)
                self.fTrendDegree = 0
            elif self.fLinearTrend:
                self.fTrendWidth = 100 * self.fPeriodLength *len(data)
                self.fTrendDegree = 1
            elif self.fTrendDegree is None:
                self.fTrendDegree = 1

            if self.fTrendWidth is None:
                self.fTrendWidth = self.calcDefaultTrendWidth(self.fPeriodLength, self.fSeasonalWidth)

            trendSettings = LoessSettings(self.fTrendWidth, self.fTrendDegree, self.fTrendJump)

            if self.fLowpassWidth is None:
                self.fLowpassWidth = self.fPeriodLength

            lowpassSettings = LoessSettings(self.fLowpassWidth, self.fLowpassDegree, self.fLowpassJump)

            return SeasonalTrendLoess(data, self.fPeriodLength, self.fInnerIterations, self.fRobustIterations, seasonalSettings, trendSettings, lowpassSettings)

        def calcDefaultTrendWidth(self, periodicity, seasonalWidth):
            #  This formula is based on a numerical stability analysis in the original paper.
            return int((1.5 * periodicity / (1 - 1.5 / seasonalWidth) + 0.5))

        def sanityCheck(self, data):
            if data is None:
                raise ValueError("SeasonalTrendLoess.Builder: Data array must be non-null")
            if self.fPeriodLength is None:
                raise NameError("SeasonalTrendLoess.Builder: Period Length must be specified")
            if len(data) < 2 * self.fPeriodLength:
                raise ValueError("SeasonalTrendLoess.Builder: Data series must be at least 2 * periodicity in length")
            if self.fPeriodic:
                massiveWidth = 100 * len(data)
                periodicConsistent = self.fSeasonalDegree is not None and self.fSeasonalWidth is not None and self.fSeasonalWidth == massiveWidth and self.fSeasonalDegree == 0
                if self.fSeasonalWidth is not None and not periodicConsistent:
                    raise NameError("SeasonalTrendLoess.Builder: setSeasonalWidth and setPeriodic cannot both be called.")
                if self.fSeasonalDegree is not None and not periodicConsistent:
                    raise NameError("SeasonalTrendLoess.Builder: setSeasonalDegree and setPeriodic cannot both be called.")
                if self.fSeasonalJump is not None:
                    raise ValueError("SeasonalTrendLoess.Builder: setSeasonalJump and setPeriodic cannot both be called.")
            else:
                if self.fSeasonalWidth is None:
                    raise ValueError("SeasonalTrendLoess.Builder: setSeasonalWidth or setPeriodic must be called.")
            if self.fFlatTrend:
                massiveWidth = 100 * self.fPeriodLength * len(data)
                flatTrendConsistent = self.fTrendWidth is not None and self.fTrendDegree is not None and self.fTrendWidth == massiveWidth and self.fTrendDegree == 0
                if self.fTrendWidth is not None and not flatTrendConsistent:
                    raise NameError("SeasonalTrendLoess.Builder: setTrendWidth incompatible with flat trend.")
                if self.fTrendDegree is not None and not flatTrendConsistent:
                    raise NameError("SeasonalTrendLoess.Builder: setTrendDegree incompatible with flat trend.")
                if self.fTrendJump is not None:
                    raise ValueError("SeasonalTrendLoess.Builder: setTrendJump incompatible with flat trend.")
            if self.fLinearTrend:
                massiveWidth = 100 * self.fPeriodLength * len(data)
                linearTrendConsistent = self.fTrendWidth is not None and self.fTrendDegree is not None and self.fTrendWidth == massiveWidth and self.fTrendDegree == 1
                if self.fTrendWidth is not None and not linearTrendConsistent:
                    raise NameError("SeasonalTrendLoess.Builder: setTrendWidth incompatible with linear trend.")
                if self.fTrendDegree is not None and not linearTrendConsistent:
                    raise NameError("SeasonalTrendLoess.Builder: setTrendDegree incompatible with linear trend.")
                if self.fTrendJump is not None:
                    raise ValueError("SeasonalTrendLoess.Builder: setTrendJump incompatible with linear trend.")

    # 
    # 	 * Construct STL specifying full details of the LOESS smoothers via LoessSettings objects.
    # 	 *
    # 	 * @param data             the data to be decomposed
    # 	 * @param periodicity      the periodicity of the data
    # 	 * @param ni               the number of inner iterations
    # 	 * @param no               the number of outer "robustness" iterations
    # 	 * @param seasonalSettings the settings for the LOESS smoother for the cyclic sub-series
    # 	 * @param trendSettings    the settings for the LOESS smoother for the trend component
    # 	 * @param lowpassSettings  the settings for the LOESS smoother used in de-seasonalizing
    # 	 
    #  Could be private but causes a hidden class to be generated in order for the Builder to have access.
    def __init__(self, data, periodicity, ni, no, seasonalSettings, trendSettings, lowpassSettings):

        self.fData = data

        size = len(data)

        self.fPeriodLength = periodicity
        self.fSeasonalSettings = seasonalSettings
        self.fTrendSettings = trendSettings
        self.fLowpassSettings = lowpassSettings
        self.fInnerIterations = ni
        self.fRobustIterations = no

        self.fLoessSmootherFactory = LoessSmoother.Builder()\
                                                  .setWidth(self.fTrendSettings.getWidth())\
                                                  .setDegree(self.fTrendSettings.getDegree())\
                                                  .setJump(self.fTrendSettings.getJump())

        self.fLowpassLoessFactory = LoessSmoother.Builder()\
                                                 .setWidth(self.fLowpassSettings.getWidth())\
                                                 .setDegree(self.fLowpassSettings.getDegree())\
                                                 .setJump(self.fLowpassSettings.getJump())

        self.fCyclicSubSeriesSmoother = CyclicSubSeriesSmoother.Builder()\
                                                               .setWidth(self.fSeasonalSettings.getWidth())\
                                                               .setDegree(self.fSeasonalSettings.getDegree())\
                                                               .setJump(self.fSeasonalSettings.getJump())\
                                                               .setDataLength(size)\
                                                               .extrapolateForwardAndBack(1)\
                                                               .setPeriodicity(periodicity)\
                                                               .build()
        self.fDetrend = np.zeros(size)
        self.fExtendedSeasonal = np.zeros(size + 2 * self.fPeriodLength)

	#
	# Factory method to perform a non-robust STL decomposition enforcing strict periodicity.
	# Meant for diagnostic purposes only.
	#
	# @param data        the data to analyze
	# @param periodicity the (suspected) periodicity of the data
	# @return SeasonalTrendLoess object with the decomposition already performed.
	#
    def performPeriodicDecomposition(self, data, periodicity):
		# The LOESS interpolator with degree 0 and a very long window (arbitrarily chosen to be 100 times the length of
		# the array) will interpolate all points as the average value of the series. This particular setting is used
		# for smoothing the seasonal sub-cycles, so the end result is that the seasonal component of the decomposition
		# is exactly periodic.

		# This fit is for diagnostic purposes, so we just do a single inner iteration.
        stl = SeasonalTrendLoess.Builder()\
                                .setPeriodLength(periodicity)\
                                .setSeasonalWidth(100 * len(data))\
                                .setSeasonalDegree(0)\
                                .setInnerIterations(1)\
                                .setRobustnessIterations(0)\
                                .buildSmoother(data)

        return stl.decompose()

	#
	# Factory method to perform a (somewhat) robust STL decomposition enforcing strict periodicity.
	# Meant for diagnostic purposes only.
	#
	# @param data        the data to analyze
	# @param periodicity the (suspected) periodicity of the data
	# @return SeasonalTrendLoess object with the decomposition already performed.
	#
    def performRobustPeriodicDecomposition(self, data, periodicity):
		# The LOESS interpolator with degree 0 and a very long window (arbitrarily chosen to be 100 times the length of
		# the array) will interpolate all points as the average value of the series. This particular setting is used
		# for smoothing the seasonal sub-cycles, so the end result is that the seasonal component of the decomposition
		# is exactly periodic.

		# This fit is for diagnostic purposes, so we just do a single inner and outer iteration.
        stl = SeasonalTrendLoess.Builder()\
                                .setPeriodLength(periodicity)\
                                .setSeasonalWidth(100 * len(data))\
                                .setSeasonalDegree(0)\
                                .setInnerIterations(1)\
                                .setRobustnessIterations(1)\
                                .buildSmoother(data)

        return stl.decompose()

	#
	# Simple class to hold the results of the STL decomposition.
	#
    class Decomposition:

        fData = []
        fTrend = []
        fSeasonal = []
        fResiduals = []
        fWeights = []

		#
		# Initialize Decomposition object from the original data.
		# Allocates space for the decomposition and initializes the weights to 1.
		#
		# @param data input data
		#
        def __init__(self, data):
            self.fData = data

            size = len(data)
            self.fTrend = np.zeros(size)
            self.fSeasonal = np.zeros(size)
            self.fResiduals = np.zeros(size)
            self.fWeights = np.ones(size)

        def getData(self):
            return self.fData

        def getTrend(self):
            return self.fTrend

        def getSeasonal(self):
            return self.fSeasonal

        def getResidual(self):
            return self.fResiduals

		#
		# Get the robustness weights used in the calculation. Places where the weights are near zero indicate outliers that
		# were effectively ignored during the decomposition. (Only applicable if robustness iterations are performed.)
		#
		# @return double the robustness weights
		#
        def getWeights(self):
            return self.fWeights

        def updateResiduals(self):
            self.fResiduals = self.fData - self.fSeasonal - self.fTrend


        # This method contains some changes in comparison with the java code
        def computeResidualWeights(self):

			# The residual-based weights are a "bisquare" weight based on the residual deviation compared to 6 times the
			# median absolute deviation (MAD). First compute 6 * MAD. (The sort could be a selection but this is
			# not critical as the rest of the algorithm is higher complexity.)

            # We use the power of numpy to make the first calculation of the weights, avoiding a loop
            self.fWeights = np.sort(np.absolute(self.fData - self.fSeasonal - self.fTrend))
            sixMad = 6.0 * np.median(self.fWeights)
            c999 = 0.999 * sixMad
            c001 = 0.001 * sixMad

            # For the second calculation of the weights, we aren't able to avoid the loop, because each weight depends on the r value
            for i in range(len(self.fData)):
                r = abs(self.fData[i] - self.fSeasonal[i] - self.fTrend[i])
                if r <= c001:
                    self.fWeights[i] = 1.0
                elif r <= c999:
                    h = r / sixMad
                    w = 1.0 - h ** 2
                    self.fWeights[i] = w ** 2
                else:
                    self.fWeights[i] = 0.0


        def smoothSeasonal(self, width, restoreEndPoints=True):
            width = max(3, width)
            if width % 2 == 0:
                width += 1

			# Quadratic smoothing of the seasonal component.
			# Do NOT perform linear interpolation between smoothed points - the quadratic spline can accommodate
			# sharp changes and linear interpolation would cut off peaks/valleys.
            seasonalSmoother = LoessSmoother.Builder()\
                                            .setWidth(width)\
                                            .setDegree(2)\
                                            .setJump(1)\
                                            .setData(self.fSeasonal)\
                                            .build()

            smoothedSeasonal = seasonalSmoother.smooth()

			# Update the seasonal with the smoothed values.
			# We only do the smoothing part in the middle of the seasonal vector. We avoid the extremes in a different way than it's do in the java code
            self.fSeasonal[1:-1] = smoothedSeasonal[1:-1]

            # We avoid the loop thanks to the power of numpy
            self.fResiduals = self.fData - self.fTrend - self.fSeasonal

    def decompose(self):

        self.fDecomposition = self.Decomposition(self.fData)

        outerIteration = 0

        while True:

            useResidualWeights = outerIteration > 0

            for iteration in range(self.fInnerIterations):
                self.smoothSeasonalSubCycles(useResidualWeights)
                self.removeSeasonality()
                self.updateSeasonalAndTrend(useResidualWeights)

            outerIteration += 1
            if outerIteration > self.fRobustIterations:
                break

            self.fDecomposition.computeResidualWeights()

        self.fDecomposition.updateResiduals()

        result = self.fDecomposition

        self.fDecomposition = None

        return result

    #
	# The seasonal component is computed by doing smoothing on the cyclic sub-series after removing the trend. The
	# current estimate of the trend is removed, then the detrended data is separated into sub-series (e.g. all the
	# Januaries, all the Februaries, etc., for yearly data), and these sub-series are smoothed and extrapolated into
	# fExtendedSeasonal.
	#
    def smoothSeasonalSubCycles(self, useResidualWeights):

        data = self.fDecomposition.fData
        trend = self.fDecomposition.fTrend
        weights = self.fDecomposition.fWeights

        self.fDetrend = data - trend

        residualWeights = weights if useResidualWeights else None

        self.fCyclicSubSeriesSmoother.smoothSeasonal(self.fDetrend, self.fExtendedSeasonal, residualWeights)

	#
	# The lowpass calculation takes the extended seasonal results and smooths them with three moving averages and a
	# LOESS smoother to remove the seasonality.
	#
    def removeSeasonality(self):

        pass1 = TimeSeriesUtilities.simpleMovingAverage(self.fExtendedSeasonal, self.fPeriodLength)
        pass2 = TimeSeriesUtilities.simpleMovingAverage(pass1, self.fPeriodLength)
        pass3 = TimeSeriesUtilities.simpleMovingAverage(pass2, 3)

        lowPassLoess = self.fLowpassLoessFactory.setData(pass3).build()
        self.fDeSeasonalized = lowPassLoess.smooth()

	#
	# The new seasonal component is computed by removing the low-pass smoothed seasonality from the extended
	# seasonality, and the trend is recalculated by subtracting this new seasonality from the data.
	#
    def updateSeasonalAndTrend(self, useResidualWeights):

        data = self.fDecomposition.fData
        trend = self.fDecomposition.fTrend
        weights = self.fDecomposition.fWeights
        seasonal = self.fDecomposition.fSeasonal

        for i in range(len(data)):
            seasonal[i] = self.fExtendedSeasonal[self.fPeriodLength + i] - self.fDeSeasonalized[i]

        trend = data - seasonal

        residualWeights = weights if useResidualWeights else None

        trendSmoother = self.fLoessSmootherFactory.setData(trend).setExternalWeights(residualWeights).build()

        self.fDecomposition.fTrend = trendSmoother.smooth()

    def __str__(self):
        return ("SeasonalTrendLoess: [\n" +
                                     "inner iterations     = {}\n" +
                                     "outer iterations     = {}\n" + 
                                     "periodicity          = {}\n" + 
                                     "seasonality settings = {}\n" + 
                                     "trend settings       = {}\n" + 
                                     "lowpass settings     = {}\n]").format(self.fInnerIterations, 
                                                                           self.fRobustIterations, 
                                                                           self.fPeriodLength, 
                                                                           self.fSeasonalSettings, 
                                                                           self.fTrendSettings, 
                                                                           self.fLowpassSettings)

