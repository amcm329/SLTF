import math 
class LoessInterpolator(object):
    
    def __init__(self):
        self._fWidth = int()
        self._fExternalWeights = []
        self._fData = []
        self._fWeights = []

    class Builder(object):
        
        def __init__(self):
            self._fWidth = None
            self._fDegree = 1
            self._fExternalWeights = None

        # 
        #        * Set the width of the LOESS smoother.
        #        *
        #        * @param width
        #        * @return this
        #        
        def setWidth(self, width):
            """ generated source for method setWidth """
            self._fWidth = width
            return self

       
       
        def setDegree(self, degree):
            """ generated source for method setDegree """
            if degree < 0 or degree > 2:
                raise IllegalArgumentException("Degree must be 0, 1 or 2")
            self._fDegree = degree
            return self


       
        def setExternalWeights(self, weights):
            """ generated source for method setExternalWeights """
            self._fExternalWeights = weights
            return self


       
 
        def interpolate(self, data):
            """ generated source for method interpolate """
            if self._fWidth is None:
                raise IllegalStateException("LoessInterpolator.Builder: Width must be set")
            if data is None:
                raise IllegalStateException("LoessInterpolator.Builder: data must be non-null")
            if self._fDegree == 0:
                return FlatLoessInterpolator(self._fWidth, data, self._fExternalWeights)
            elif self._fDegree == 1:
                return LinearLoessInterpolator(self._fWidth, data, self._fExternalWeights)
            elif self._fDegree == 2:
                return QuadraticLoessInterpolator(self._fWidth, data, self._fExternalWeights)
            else:
                return None
            #  Can't actually get here but compiler didn't figure that out.

    #  -----------------------------------------------------------------------------------------------------------------
    #  Interface
    #  -----------------------------------------------------------------------------------------------------------------
    # 
    #    * Given a set of data on the regular grid {left, left+1, ..., right-1, right}, computed the LOESS-smoothed value at
    #    * the position x and return it. If the value can't be computed, return null.
    #    *
    #    * @param x
    #    *            double x-coordinate at which we want to compute an estimate of y
    #    * @param left
    #    *            int leftmost coordinate to use from the input data
    #    * @param right
    #    *            int rightmost coordinate to use from the input data
    #    * @return Double interpolated value, or null if interpolation could not be done
    #    
    def smoothOnePoint(self, x, left, right):
        """ generated source for method smoothOnePoint """
        #  Ordinarily, one doesn't do linear regression one x-value at a time, but LOESS does since
        #  each x-value will typically have a different window. As a result, the weighted linear regression
        #  is recast as a linear operation on the input data, weighted by this.fWeights.
        state = computeNeighborhoodWeights(x, left, right)
        if state == State._WEIGHTS_FAILED:
            return None
        if state == State._LINEAR_OK:
            updateWeights(x, left, right)
        ys = 0.0
        i = left
        while i <= right:
            ys += self._fWeights[i] * self._fData[i]
            i += 1
        return ys

    # 
    #    * Update the weights for the appropriate least-squares interpolation.
    #    *
    #    * @param x
    #    *            double x-coordinate at which we want to compute an estimate of y
    #    * @param left
    #    *            int leftmost coordinate to use from the input data
    #    * @param right
    #    *            int rightmost coordinate to use from the input data
    #    
    def updateWeights(self, x, left, right):
        """ generated source for method updateWeights """

    #  -----------------------------------------------------------------------------------------------------------------
    #  Implementation
    #  -----------------------------------------------------------------------------------------------------------------
    # 
    #    * Internal enum used to return the state of the weights calculation.
    #    
    class State:
        """ generated source for enum State """

        def __init__():
            self._WEIGHTS_FAILED = 'WEIGHTS_FAILED'
            self._LINEAR_FAILED = 'LINEAR_FAILED'
            self._LINEAR_OK = 'LINEAR_OK'

    # 
    #    * Computer the neighborhood weights.
    #    *
    #    * @param x
    #    *            double x-coordinate at which we want to compute an estimate of y
    #    * @param left
    #    *            int leftmost coordinate to use from the input data
    #    * @param right
    #    *            int rightmost coordinate to use from the input data
    #    * @return State indicating the whether we can do linear, moving average, or nothing
    #    
    def computeNeighborhoodWeights(self, x, left, right):
        """ generated source for method computeNeighborhoodWeights """
        lambda_ = max(x - left, right - x)
        #  Ordinarily, lambda ~ width / 2.
        # 
        #  If width > n, then we will only be computing with n points (i.e. left and right will always be in the
        #  domain of 1..n) and the above calculation will give lambda ~ n / 2. We want the shape of the neighborhood
        #  weight function to be driven by width, not by the size of the domain, so we adjust lambda to be ~ width / 2.
        #  (The paper does this by multiplying the above lambda by (width / n). Not sure why the code is different.)
        if _fWidth > _fData.len():
            lambda_ += _fWidth - _fData.len() / 2
        #  "Neighborhood" is computed somewhat fuzzily.
        l999 = 0.999 * lambda_
        l001 = 0.001 * lambda_
        #  Compute neighborhood weights, updating with external weights if supplied.
        totalWeight = 0.0
        j = left
        while j <= right:
            #  Compute the tri-cube neighborhood weight
            delta = x -j 
            if delta <= l999:
                if delta <= l001:
                    weight = 1.0
                else:
                    fraction = delta / _lambda
                    trix = 1.0 - fraction * fraction * fraction
                    weight = trix * trix * trix
                #  If external weights are provided, apply them.
                if self._fExternalWeights != None:
                    weight *= self._fExternalWeights[j]
                totalWeight += weight
            self._fWeights[j] = weight
            j += 1
        #  If the total weight is 0, we can't proceed, so signal failure.
        if totalWeight <= 0.0:
            return self.State._WEIGHTS_FAILED
        #  Normalize the weights
        j = left
        while j <= right:
            self._fWeights[j] /= totalWeight
            j += 1
        return self.State._LINEAR_OK if (lambda_ > 0) else self.State._LINEAR_FAILED

    # 
    #    * Create a LoessInterpolator interpolator for the given data set with the specified smoothing width and
    #    * optional external Weights.
    #    *
    #    * @param width
    #    *            - the width of the neighborhood weighting function
    #    * @param data
    #    *            - underlying data set that is being smoothed
    #    * @param externalWeights
    #    *            - additional weights to apply in the smoothing. Ignored if null.
    #    
    def __init__(self, width, data, externalWeights):
        """ generated source for method __init__ """
        self._fWidth = width
        self._fData = data
        self._fExternalWeights = externalWeights
        self._fWeights = [None]


class FlatLoessInterpolator(LoessInterpolator):
    """ generated source for class FlatLoessInterpolator """
    # 
    #    * Create a LoessInterpolator interpolator for the given data set with the specified smoothing width and
    #    * optional external Weights.
    #    *
    #    * @param width           - the width of the neighborhood weighting function
    #    * @param data            - underlying data set that is being smoothed
    #    * @param externalWeights
    #    
    def __init__(self, width, data, externalWeights):
        """ generated source for method __init__ """
        super(FlatLoessInterpolator, self).__init__(externalWeights)

    # 
    #    * Weight update for FlatLinearInterpolator is a no-op.
    #    
    def updateWeights(self, x, left, right):
        """ generated source for method updateWeights """


class LinearLoessInterpolator(LoessInterpolator):
    """ generated source for class LinearLoessInterpolator """
    # 
    #    * Create a LoessInterpolator interpolator for the given data set with the specified smoothing width and
    #    * optional external Weights.
    #    *
    #    * @param width           - the width of the neighborhood weighting function
    #    * @param data            - underlying data set that is being smoothed
    #    * @param externalWeights
    #    
    def __init__(self, width, data, externalWeights):
        """ generated source for method __init__ """
        super(LinearLoessInterpolator, self).__init__(externalWeights,data,width)     

    # 
    #    * Compute weighted least squares fit to the data points and adjust the weights with the results.
    #    *
    #    * @param x
    #    *            double x-coordinate at which we want to compute an estimate of y
    #    * @param left
    #    *            int leftmost coordinate to use from the input data
    #    * @param right
    #    *            int rightmost coordinate to use from the input data
    #    
    def updateWeights(self, x, left, right):
        """ generated source for method updateWeights """
        xMean = 0.0

        i = left
        while i <= right:
            xMean += i * _fWeights[i]
            i += 1
        x2Mean = 0.0
        i = left
        while i <= right:
            x2Mean += _fWeights[i] * delta * delta
            i += 1
        #  Finding y(x) from the least-squares fit can be cast as a linear operation on the input data.
        #  This is implemented by updating the weights to include the least-squares weighting of the points.
        #  Note that this is only done if the points are spread out enough (variance > (0.001 * range)^2)
        #  to compute a slope. If not, we leave the weights alone and essentially fall back to a moving
        #  average of the data based on the neighborhood and external weights.
        range = len(fData)
        if x2Mean > 0.000001 * range * range:
            while i <= right:
                _fWeights[i] *= (1.0 + beta * (i - xMean))
                i += 1


class QuadraticLoessInterpolator(LoessInterpolator):
    """ generated source for class QuadraticLoessInterpolator """
    # 
    #    * Create a QuadraticLoessInterpolator interpolator for the given data set with the specified smoothing width and
    #    * optional external Weights.
    #    *
    #    * @param width           - the width of the neighborhood weighting function
    #    * @param data            - underlying data set that is being smoothed
    #    * @param externalWeights
    #    
    def __init__(self, width, data, externalWeights):
        """ generated source for method __init__ """
        super(QuadraticLoessInterpolator, self).__init__(externalWeights)

    # 
    #    * Compute weighted least squares quadratic fit to the data points and adjust the weights with the results.
    #    *
    #    * @param x
    #    *            double x-coordinate at which we want to compute an estimate of y
    #    * @param left
    #    *            int leftmost coordinate to use from the input data
    #    * @param right
    #    *            int rightmost coordinate to use from the input data
    #    
    def updateWeights(self, x, left, right):
        """ generated source for method updateWeights """
        self._x1Mean = 0.0
        self._x2Mean = 0.0
        self._x3Mean = 0.0
        self._x4Mean = 0.0
        i = left
        while i <= right:
            w = _fWeights[i]
            x1w = i * w
            x2w = i * x1w
            x3w = i * x2w
            x4w = i * x3w
        
            x1Mean += x1w;
            x2Mean += x2w;
            x3Mean += x3w;
            x4Mean += x4w;
            i += 1

        m2 = _x2Mean - _x1Mean * _x1Mean
        m3 = _x3Mean - _x2Mean * _x1Mean
        m4 = _x4Mean - _x2Mean * _x2Mean

        denominator = m2 * m4 - m3 * m3
        range = _fData.len()

        if denominator > 0.000001 * range * range:
            #  TODO: Are there cases where denominator is too small but m2 is not too small?
            #  In that case, it would make sense to fall back to linear regression instead of falling back to just the
            #  weighted average.
            beta2 = m4 / denominator
            beta3 = m3 / denominator
            beta4 = m2 / denominator
            x1 = x - x1Mean
            x2 = x*x - x2Mean

            a1 = beta2 * x1 - beta3 * x2
            a2 = beta4 * x2 - beta3 * x1


            i = left
            while i <= right:
                _fWeights[i] *= (1 + a1 * (i - _x1Mean) + a2 * (i * i - _x2Mean))
                i += 1

LoessInterpolator #      * class LoessInterpolator.Builder - Factory for LoessInterpolator objects

