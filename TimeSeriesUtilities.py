"""TimeSeriesUtilities is a collection of static functions implementing common time-series utilities."""

import numpy as np

class TimeSeriesUtilities:
     
    @staticmethod
    def simpleMovingAverage(data, window):
        ret = np.cumsum(data, dtype=float)
        ret[window:] = ret[window:] - ret[:-window]
        average = ret[window - 1:] / window
        return average
