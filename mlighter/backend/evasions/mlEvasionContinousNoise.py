## @package MLigther
#    Copyright 2022 Hector D. Menendez
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#  
#  Documentation for this module.
#
#  More details.
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
        # Creates an array where the ith element contains the index of the original input
        self.origin_map = np.tile(np.arange(len(data)), self.numberVariants)
        variableInput = data
        inputVal=np.asmatrix(variableInput)

        total=[]
        for i in range(self.numberVariants):
            total.append([inputVal])

        inputVal = np.block(total)

        transformations = (self.noise)*np.random.random(size=(len(inputVal),len(self.featureSelection)))+self.shift

        transformations = transformations * np.asarray(self.featureSelection)
        variants = inputVal + transformations
        return variants

    def get_config(self):
        return {
            "number_variants": self.numberVariants,
            "noise": self.noise,
            "features": self.featureSelection,
            "shift": self.shift
        }

    def get_name(self):
        return "Continous Noise"

    def get_variant_original(self, index):
        return self.origin_map[index]
