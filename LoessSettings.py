""" generated source for module LoessSettings """
# package: com.github.servicenow.ds.stats.stl
# 
#  * LoessSettings - immutable settings class for specifying the triple of width/jump/degree used to initialize the LOESS
#  * interpolators. Enforces that width be 3 or larger and that the degree is 0 or 1.
#  *
#  * Created by Jim Crotinger on 12-May-2016.
#  *
#  
class LoessSettings:

    fWidth = None
    fDegree = None
    fJump = None

    # 
    # 	 * Create specifying width, degree and jump.
    # 	 *
    # 	 * @param width
    # 	 *            int width of the LOESS smoother in data points.
    # 	 * @param degree
    # 	 *            int degree of polynomial used in LOESS.
    # 	 * @param jump
    # 	 *            int number of points to skip between LOESS smoothings.
    # 	 
    def __init__(self, width, degree=None, jump=None):
        """ generated source for method __init__ """
        width = max(3, width)
        if width % 2 == 0:
            width += 1
        self.fWidth = width
        if jump is None:
            self.fJump = max(1, int((0.1 * width + 0.9)))
        else:
            self.fJump = max(1, jump)
        if degree is None:
            self.fDegree = 1
        else:
            self.fDegree = max(0, min(2, degree))

    # 
    # 	 * Get the width of the LOESS smoother.
    # 	 *
    # 	 * @return int width of LOESS smoother.
    # 	 
    def getWidth(self):
        """ generated source for method getWidth """
        return self.fWidth

    # 
    # 	 * Get the degree of the LOESS smoother
    # 	 *
    # 	 * @return int degree of the LOESS smoother.
    # 	 
    def getDegree(self):
        """ generated source for method getDegree """
        return self.fDegree

    # 
    # 	 * Get the jump used between LOESS interpolations.
    # 	 *
    # 	 * @return int jump used between LOESS interpolations.
    # 	 
    def getJump(self):
        """ generated source for method getJump """
        return self.fJump

    def __str__(self):
        """ generated source for method toString """
        return String.format("[width = %d, degree = %d, jump = %d]", self.fWidth, self.fDegree, self.fJump)
