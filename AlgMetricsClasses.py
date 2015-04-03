"""
This script creates an Algorithm and Metric class to handle the plan
analysis.
"""

import math
import parser
import scipy
import scipy.interpolate as spi


# A dictionary to hold metadata info. It is empty for now, but will
# reference the metadata dictionary created in the PinnacleDVH script.
metadata = {}

# A dictionary to hold the DVHs and bins. It is empty for now, but will
# reference the metadata dictionary created in the PinnacleDVH script.
DVHs = {}



class Metric(object):
    """
    A class that represents a metric providing attibutes and methods to
    work with the metric.
    """

############################# Constructor ##############################
    def __init__(self, *args):
        if   len(args) == 0:
            # Handle the case of being given zero arguments.
            print "ERROR: An algorithm cannot be constructed from zero arguments."
        elif len(args) == 1:
            # Handle the case of being given one argument.
            if   type(args[0]) is str:
                # Handle the case of the single argument being a string,
                # presumably matching the format of a metric line of an
                # algorithm.
                dummy = args[0].split()
                self.roi = dummy[0]
                self.quantity = dummy[1]
                self.direction = dummy[2]
                self.method = dummy[3]
                self.scoring = dummy[4:]
            elif type(args[0]) is list:
                # Handle the case of the single argument being a list,
                # presumably this list is formatted as if a metric line
                # of an algorithm was split according to its whitespace.
                # It may have 4 or 5 arguments depending on whether the
                # metric is a pass/fail metric or not.
                if   len(args[0]) == 4:
                    # Handle the case of there being only 4 arguments
                    # presumably because it is a pass/fail metric.
                elif len(args[0]) == 5:
                    # Handle the case of there being all 5 arguments.
                    self.roi = args[0][0]
                    self.quantity = args[0][1]
                    self.direction= args[0][2]
                    self.method = args[0][3]
                    self.scoring= args[0][4]
                else:
                    # Handle the case that there are the wrong number of
                    # arguments given.
                    print "ERROR: An incorrect number of arguments were given."
            elif type(args[0]) is dict:
                # Handle the case of the single argument being a dict,
                # presumably giving information about the ROI, quantity
                # to be scored, direction of success/failure, method of
                # interpolating, and the scoring information.
                self.roi = args[0]["roi"]
                self.quantity = args[0]["quantity"]
                self.direction= args[0]["direction"]
                if args[0].has_key("method"):
                    self.method = args[0]["method"]
                self.scoring= args[0]["scoring"]
            else:
                # Handle the case of not being given the argument in any
                # of the above acceptable formats.
                print "ERROR: The arguments are of the wrong format."
        elif len(args) == 4:
            # Handle the case of being given the arguments as separate
            # key value pairs similar to being given a dict. Here, the
            # method of interpolating is not given and so is presumed to
            # be pass/fail.
                self.roi = args[0]
                self.quantity = args[1]
                self.direction = args[2]
                self.scoring = args[3]
        elif len(args) == 5:
            # Handle the case of being given the arguments as separate
            # key value pairs similar to being given a dict. Here, the
            # method of interpolating is given.
                self.roi = args[0]
                self.quantity = args[1]
                self.direction = args[2]
                self.method = args[3]
                self.scoring = args[4]
        else:
            # Handle the case of not being given the arguments in any of
            # the above acceptable formats.
            print "ERROR: The arguments are of the wrong format and/or quantity."

        # Create the scoring function.
        if self.method:
            # Handle the case of the interpolation method being given.
            if   self.method == "lamda":
                # Handle the case of the method being given a mathemat-
                # ical expression to determine the score.
                self.code = parser.expr(self.scoring).compile()
                self.ScoreFunction = lambda (value): x=value;return eval(self.code)
                # evaluate using: return self.ScoreFuntion(value)
            elif self.method == "linear":
                # Handle the case of the method being a table of values
                # with linear interpolation to fill in the intermediate
                # scores.
                self.MetricX, self.MetricY = zip(*self.scoring)
                self.ScoreFunction = spi.InterpolatedUnivariateSpline(x=MetricX, 
                                                                      y=MetricY, 
                                                                      k=1, 
                                                                      ext='const')
                # evaluate using: return self.ScoreFunction(value)
            elif self.method == "cubic":
                # Handle the case of the method being a table of values
                # with cubic interpolation to fill in the intermediate
                # scores.
                self.ScoreFunction = spi.InterpolatedUnivariateSpline(x=MetricX, 
                                                                      y=MetricY, 
                                                                      k=3, 
                                                                      ext='const')
                # evaluate using: return self.ScoreFuntion(value)
            elif self.method == "file":
                # Handle the case of the method being given a file to
                # pull the scoring method from.
                MetricFile = open(self.scoring)

                line = MetricFile.readline()
                line = MetricFile.readline()

                self.method = MetricFile.readline()
                
                line = MetricFile.readline()
                line = MetricFile.readline()

                self.scoring = ""
                while line:
                    self.scoring.append(MetricFile.readline() + " ")
                    line = MetricFile.readline()

                self.MetricX, self.MetricY = zip(*self.scoring)
                if   self.method == "lamda":
                    # Handle the case of the method being given a mathemat-
                    # ical expression to determine the score.
                    self.code = parser.expr(self.scoring).compile()
                    self.ScoreFunction = lambda (value): x=value;return eval(self.code)
                    # evaluate using: return self.ScoreFuntion(value)
                elif self.method == "linear":
                    # Handle the case of the method being a table of values
                    # with linear interpolation to fill in the intermediate
                    # scores.
                    self.MetricX, self.MetricY = zip(*self.scoring)
                    self.ScoreFunction = spi.InterpolatedUnivariateSpline(x=MetricX, 
                                                                          y=MetricY, 
                                                                          k=1, 
                                                                          ext='const')
                    # evaluate using: return self.ScoreFunction(value)
                elif self.method == "cubic":
                    # Handle the case of the method being a table of values
                    # with cubic interpolation to fill in the intermediate
                    # scores.
                    self.ScoreFunction = spi.InterpolatedUnivariateSpline(x=MetricX, 
                                                                          y=MetricY, 
                                                                          k=3, 
                                                                          ext='const')
                    # evaluate using: return self.ScoreFuntion(value)
            else:
                # Handle the case of some erroneous method being used.
                print "ERROR: An invalid method has been used."
        else:
            # Handle the case of the interpolation method not being
            # given, presumably due to it being a pass/fail metric.
            if value < self.scoring:
                # Handle the case of the value being less than the
                # scoring function; namely the pass/fail value.
                return True 
                # or return some other value or maybe find out the max
                # value from other metrics or something.
            else:
                # Handle the case of the value being greater than or
                # equal to the scoring function; namely the pass/fail
                # metric.
                return False
                # or return some other value or maybe find out the min
                # value from other metrics or something.

    def FromFile(self, filename):
        """
        Get the metric scoring information from a file. This method will
        NOT generate a Metric object from the information within the
        given file.
        """

    def Result(self, value):
        """
        Return the result of the metric, the metric score, given the
        required DVH information.
        """
        
        # Use self.quantity and interpolation to determine value from the DVH
        # Data.

        return self.ScoreFunction(value)

# END



class Algorithm(object):
    """
    A class that represents an algorithm providing attributes and
    methods to work with the algorithm.
    """

############################# Constructor ##############################
    def __init__(self, *args):
        if   len(args) == 0:
            # Handle the case of being given zero arguments.
            print "ERROR: An algorithm cannot be constructed from zero arguments."
        elif len(args) == 1:
            # Handle the case of being given one argument. That argument
            # could be a string, a list, or a dict.
            if   type(args[0]) is str:
                # Handle the case of the single argument being a string,
                # presumably the filename for the algorithm. This is the
                # prefered method.
                self.FromFile(filename)
            elif type(args[0]) is list:
                # Handle the case of the single argument being a list of
                # the various metadata info and metrics in the order
                # below.
                if   len(args[0]) == 9:
                    # Handle the case of there being only 9 pieces of
                    # information passed, namely with the filename
                    # missing. In this case, just assign it a filename
                    # matching the name of the algorithm.
                    self.filename = args[0][0] + ".algorithm"
                    self.name     = args[0][0]
                    self.date     = args[0][1]
                    self.clinic   = args[0][2]
                    self.radonc   = args[0][3]
                    self.site     = args[0][4]
                    self.modality = args[0][5]
                    self.delivery = args[0][6]
                    self.tps      = args[0][7]
                    self.metadata = {"filename":filename,
                                     "name":name,
                                     "date":date,
                                     "clinic":clinic,
                                     "radonc":radonc,
                                     "site":site,
                                     "modality":modality,
                                     "delivery":delivery,
                                     "energy":tps}
                    self.metrics  = args[0][7]
                elif len(args[0]) == 10:
                    # Handle the case of all 10 pieces of information
                    # being passed.
                    self.filename = args[0][0]
                    self.name     = args[0][1]
                    self.date     = args[0][2]
                    self.clinic   = args[0][3]
                    self.radonc   = args[0][4]
                    self.site     = args[0][5]
                    self.modality = args[0][6]
                    self.delivery = args[0][7]
                    self.tps      = args[0][8]
                    self.metadata = {"filename":filename,
                                     "name":name,
                                     "date":date,
                                     "clinic":clinic,
                                     "radonc":radonc,
                                     "site":site,
                                     "modality":modality,
                                     "delivery":delivery,
                                     "energy":tps}
                    self.metrics  = args[0][9]
                else:
                    # Handle the case of not being given the arguments 
                    # in any of the above acceptable formats.
                    print "ERROR: An incorrect number of arguments were given."
            elif type(args[0]) is dict:
                # Handle the case of the single argument being a dict of
                # all the pieces of metadata information and metrics.
                if args[0].has_key("filename"):
                    # If the filename is given then go ahead and use it.
                    self.filename = args[0]["filename"]
                else:
                    # If not, then go ahead and assign it a filename
                    # matching the name of the algorithm.
                    self.filename = args[0]["name"] + ".algorithm"
                self.name     = args[0]["name"]
                self.date     = args[0]["date"]
                self.clinic   = args[0]["clinic"]
                self.radonc   = args[0]["radonc"]
                self.site     = args[0]["site"]
                self.modality = args[0]["modality"]
                self.delivery = args[0]["delivery"]
                self.energy   = args[0]["energy"]
                self.tps      = args[0]["tps"]
                self.metadata = {"filename":filename,
                                 "name":name,
                                 "date":date,
                                 "clinic":clinic,
                                 "radonc":radonc,
                                 "site":site,
                                 "modality":modality,
                                 "delivery":delivery,
                                 "energy":tps}
                self.metrics  = args[0]["metrics"]
            else:
                # Handle the case of not being given the arguments in 
                # any of the above acceptable formats.
                print "ERROR: The arguments are of the wrong format."
        elif len(args) == 9:
            # Handle the case of there being only 9 pieces of
            # information passed, namely with the filename
            # missing. In this case, just assign it a filename
            # matching the name of the algorithm.
            self.filename = args[0] + ".algorithm"
            self.name     = args[0]
            self.date     = args[1]
            self.clinic   = args[2]
            self.radonc   = args[3]
            self.site     = args[4]
            self.modality = args[5]
            self.delivery = args[6]
            self.energy   = args[7]
            self.tps      = args[8]
            self.metadata = {"filename":filename,
                             "name":name,
                             "date":date,
                             "clinic":clinic,
                             "radonc":radonc,
                             "site":site,
                             "modality":modality,
                             "delivery":delivery,
                             "energy":tps}
            self.metrics  = args[9]
        elif len(args) == 10:
            # Handle the case of all 10 pieces of information
            # being passed.
            self.filename = args[0]
            self.name     = args[1]
            self.date     = args[2]
            self.clinic   = args[3]
            self.radonc   = args[4]
            self.site     = args[5]
            self.modality = args[6]
            self.delivery = args[7]
            self.energy   = args[8]
            self.tps      = args[9]
            self.metadata = {"filename":filename,
                             "name":name,
                             "date":date,
                             "clinic":clinic,
                             "radonc":radonc,
                             "site":site,
                             "modality":modality,
                             "delivery":delivery,
                             "energy":tps}
            self.metrics  = args[10]
        else:
            # Handle the case of not being given the arguments in any of
            # the above acceptable formats.
            print "ERROR: The arguments are of the wrong format and/or quantity."

    def FromFile(self, filename):
        """
        Fill in all the metadata and metrics information from a file.
        This is the prefered method.
        """
        AlgFile = open(filename)
        self.filename = filename
        self.name     = AlgFile.readline()
        self.date     = AlgFile.readline()
        self.clinic   = AlgFile.readline()
        self.radonc   = Algfile.readline()
        self.site     = Algfile.readline()
        self.modality = AlgFile.readline()
        self.delivery = Algfile.readline()
        self.energy   = Algfile.readline()
        self.tps      = Algfile.readline()
        self.metadata = {"filename":filename,
                         "name":self.name,
                         "date":self.date,
                         "clinic":self.clinic,
                         "radonc":self.radonc,
                         "site":self.site,
                         "modality":self.modality,
                         "delivery":self.delivery,
                         "energy":self.tps}
        dummy = Algfile.readline()
        dummy = Algfile.readline()
        self.metrics  = {"standard":[], "custom":[]}
        line = Alfgile.readline()
        while line:
            self.metrics["standard"] = Metric(line)
            line = AlgFile.readline()
        line = Alfgile.readline()
        line = Alfgile.readline()
        while line:
            self.metrics["custom"] = Metric(line)
            line = AlgFile.readline()
        AlgFile.close()

    def Results(self, DVHs, algorithm):
        """
        Determine the results of analyzing the provided DVH data against
        the algorithm.

        Consider moving this method to being part of the main program.
        """

# END