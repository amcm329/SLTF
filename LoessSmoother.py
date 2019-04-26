#!/usr/bin/env python
""" generated source for module smoot """
# package: com.github.servicenow.ds.stats.stl
# 
#  * LoessSmoother uses LOESS interpolation to compute a smoothed data set from a regularly-spaced set of input
#  * data. If a jump is specified, then LOESS interpolation is only done on every jump points and linear interpolation is
#  * done to fill in the gaps.
#  * <p>
#  * Author: Jim Crotinger, ported from the original RATFOR source from netlib
#  
#import LoessInterpolator.py

#import smoot.py as LoessSmoother

#@SuppressWarnings("WeakerAccess")
from LoessInterpolator import LoessInterpolator

class LoessSmoother(object):
    """ generated source for class LoessSmoother """
    def __init__(self, width, jump, degree, data, externalWeights):
        b = LoessInterpolator.self.Builder()
        self.fInterpolator = b.setWidth(width).setDegree(degree).setExternalWeights(externalWeights).interpolate(data)
        self.fData = []
        self.fJump = min(jump, len(data))
        self.fWidth = 0
        self.fSmoothed = [float(len(data))]

    class Builder(object):
        #generated source for class Builder 
        fWidth = None
        fDegree = 1
        fJump = 1
        fExternalWeights = None
        fData = None

        #Set the width of the LOESS smoother.

        def setWidth(self, width):
            self.fWidth = width
            return self

        # Set the degree of the LOESS smoother.	 
        def setDegree(self, degree):
            if (degree < 0) or (degree > 2):
                raise ValueError("Degree must be 0, 1 or 2")
            self.fDegree = degree
            return self


        #Set the jump (number of points to skip) between LOESS interpolations.

        def setJump(self, jump):
            self.fJump = jump
            return self

        # Set the external weights for interpolation.

        def setExternalWeights(self, weights):
            self.fExternalWeights = weights
            return self

        #Set the data to be smoothed.

        def setData(self, data):
            self.fData = data
            return self

        # Build the LoessSmoother.
	 
        def build(self):
            if self.fWidth == None:
                raise ValueError("LoessSmoother.Builder: Width must be set before calling build")
            if self.fData == None:
                raise ValueError("LoessSmoother.Builder: Data must be set before calling build")
            
            return LoessSmoother(self.fWidth, self.fJump, self.fDegree, self.fData, self.fExternalWeights)

    #  -----------------------------------------------------------------------------------------------------------------
    #  Interface
    #  -----------------------------------------------------------------------------------------------------------------
    # 
    # 	 * Create a LoessSmoother for the given data set with the specified smoothing width and optional external
    # 	 * Weights.
    # 	 *
    # 	 * @param width           approximate width the width of the neighborhood weighting function
    # 	 * @param jump            smoothing jump - only ever jump points are smoothed by LOESS with linear interpolation in between.
    # 	 * @param degree          1 for linear regression, 0 for simple weighted average
    # 	 * @param data            underlying data set that is being smoothed
    # 	 * @param externalWeights additional weights to apply in the smoothing. Ignored if null.
    # 

   

    def getInterpolator(self):
        return self.fInterpolator

    def smooth(self):
        """ generated source for method smooth """
        if len(fData):
            self.fSmoothed[0] = self.fData[0]
            return self.fSmoothed
        left = -1
        right = -1
        if fWidth >= len(fData):
            left = 0
            right = len(fData)
            while i < len(fData):
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[i] = self.fData[i] if y == None else y
                i = i + self.fJump   

        elif self.fJump == 1:
            halfWidth = int((fWidth + 1) / 2)
            left = 0
            right = self.fWidth - 1
            while i < len(fData):
                if i >= halfWidth and right != len(fData):
                    left += 1
                    right += 1
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[i] = self.fData[i] if y == None else y
                i = i + 1
        else:
            halfWidth = int((fWidth + 1) / 2)
            while i < len(fData):
                if i < halfWidth - 1:
                    left = 0
                elif i >= (len(fData) - halfWidth):
                    left = len(fData) - fWidth
                else:
                    left = i - halfWidth + 1
                right = left + self.fWidth - 1
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[i] = self.fData[i] if y == None else y
                i =  i + self.fJump
        
        if self.fJump != 1:
            while i < len(fData - self.fJump):
                slope = (fSmoothed[i + self.fJump] - fSmoothed[i]) / float(fJump);
                while j < i + self.fJump:
                    self.fSmoothed[j] = self.fSmoothed[i] + slope * (j - i)
                    j = j + 1
                i = i + self.fJump
            last = int(len(fData) - 1);
            lastSmoothedPos = int((last / fJump) * fJump);
            if lastSmoothedPos != last:
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[last] = self.fData[last] if y == None else y
                if lastSmoothedPos != last - 1:
                    slope = (fSmoothed[last] - fSmoothed[lastSmoothedPos]) / (last - lastSmoothedPos);
                    j = lastSmoothedPos + 1
                    while j < last:            
                        self.fSmoothed[j] = self.fSmoothed[lastSmoothedPos] + slope * (j - lastSmoothedPos)
                        j = j +1
        return self.fSmoothed

