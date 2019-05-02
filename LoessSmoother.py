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
import math 

from LoessInterpolator import LoessInterpolator

class LoessSmoother:
    """ generated source for class LoessSmoother """
    fInterpolator = None
    fData = []
    fWidth = None
    fJump = None
    fSmoothed = []

    class Builder:
        #generated source for class Builder 
        fWidth = None
        fDegree = 1
        fJump = 1
        fExternalWeights = None
        fData = None

       

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
        #Set the width of the LOESS smoother.

        def setWidth(self, width):
            self.fWidth = width
            return self

        # Build the LoessSmoother.
     
        def build(self):
            if self.fWidth is None:
                raise ValueError("LoessSmoother.Builder: Width must be set before calling build")
            if self.fData is None:
                raise ValueError("LoessSmoother.Builder: Data must be set before calling build")
            
            return LoessSmoother(self.fWidth, self.fJump, self.fDegree, self.fData, self.fExternalWeights)

    #  -----------------------------------------------------------------------------------------------------------------
    #  Interface
    #  -----------------------------------------------------------------------------------------------------------------
    # 
    #    * Create a LoessSmoother for the given data set with the specified smoothing width and optional external
    #    * Weights.
    #    *
    #    * @param width           approximate width the width of the neighborhood weighting function
    #    * @param jump            smoothing jump - only ever jump points are smoothed by LOESS with linear interpolation in between.
    #    * @param degree          1 for linear regression, 0 for simple weighted average
    #    * @param data            underlying data set that is being smoothed
    #    * @param externalWeights additional weights to apply in the smoothing. Ignored if null.
    # 

    def __init__(self, width, jump, degree, data, externalWeights):
        self.fInterpolator = LoessInterpolator.Builder().setWidth(width).setDegree(degree).setExternalWeights(externalWeights).interpolate(data)
        self.fData = data
        self.fJump = min(jump, len(data))
        self.fWidth = width
        self.fSmoothed = [float(len(data))]

       

    def getInterpolator(self):
        return self.fInterpolator

    def smooth(self):
        """ generated source for method smooth """
        if len(self.fData) == 1:
            self.fSmoothed[0] = self.fData[0]
            return self.fSmoothed
        left = -1
        right = -1
        if self.fWidth >= len(self.fData):
            left = 0
            right = len(self.fData)
            for i in range(len(self.fData)):
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[i] = self.fData[i] if y == None else y

        elif self.fJump == 1:
            halfWidth = int((self.fWidth + 1) / 2)
            left = 0
            right = self.fWidth - 1
            for i in range(len(self.fData)):
                if i >= halfWidth and right != len(self.fData):
                    left += 1
                    right += 1
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[i] = self.fData[i] if y == None else y
                
        else:
            halfWidth = int((self.fWidth + 1) / 2)
            for i in range(len(self.fData)):
                if i < halfWidth - 1:
                    left = 0
                elif i >= (len(self.fData) - halfWidth):
                    left = len(self.fData) - self.fWidth
                else:
                    left = i - halfWidth + 1
                right = left + self.fWidth - 1
                y = LoessInterpolator.smoothOnePoint(i, left, right)
                self.fSmoothed[i] = self.fData[i] if y == None else y
        
        if self.fJump != 1:
            for i in range(len(self.fData - self.fJump)):
                slope = (fSmoothed[i + self.fJump] - fSmoothed[i]) / float(fJump)
                for j in range(i + self.fJump):
                    self.fSmoothed[j] = self.fSmoothed[i] + slope * (j - i)
            last = int(len(self.fData) - 1);
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

