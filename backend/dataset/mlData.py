## @package MLigther
#  Documentation for this module.
#
#  More details.

class MLDataset:

    def __init__(self,name):
        self.name = name

    #Transformation is an MLEvasion type
    def transform(self, transformation, oriVariant=None):
        if(oriVariant is None):
            self.variants = transformation.genVariants(self.data)
        else:
           self.variants = transformation.genVariants(self.data,oriVariant)
 
    def getVariants(self):
        return self.variants
