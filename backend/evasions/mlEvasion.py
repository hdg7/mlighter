## @package MLigther
#  Documentation for this module.
#
#  More details.
#from exception import NotImplementedError

class MLEvasion:

    def __init__(self,name):
        self.name = name

    def transformationSetup(self,config):
        raise NotImplementedError("Please Implement this method")
    
    def genVariants(self,data):
        raise NotImplementedError("Please Implement this method")

    #Number of variants per input
    def setNumberVariants(self,numberVariants):
        self.numberVariants=numberVariants
