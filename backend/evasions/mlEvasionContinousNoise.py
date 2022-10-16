from .mlEvasion import MLEvasion
import numpy as np

class MLEvasionContinousNoise(MLEvasion):

    def setNoise(self,noise):
        self.noise=noise

    def setShift(self,shift):
        self.shift=shift
        
    def transformationSetup(self,config):
        self.numberVariants=config["numberVariants"]
        self.noise=config["noise"]
        self.featureSelection=config["features"]
        self.shift=config["shift"]
        
    def genVariants(self,data):
        variableInput = data
        inputVal=np.asmatrix(variableInput)
#        print("Inputs before block")
#        print(inputVal)
        total=[]
        for i in range(self.numberVariants): total.append([inputVal])
        inputVal = np.block(total)
#        print("Inputs after block")
#        print(inputVal)
        transformations = (self.noise)*np.random.random(size=(len(inputVal),len(self.featureSelection)))+self.shift
#        print(transformations)
#        print("size")
#        print(self.numberVariants*len(inputVal),len(self.featureSelection))
#        print(np.asarray(self.featureSelection))
        transformations = transformations * np.asarray(self.featureSelection)
        variants = inputVal + transformations
        return variants

