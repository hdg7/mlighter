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

    def get_config(self):
        raise NotImplementedError("Please Implement this method")

    def get_name(self):
        raise NotImplementedError("Please Implement this method")

    def get_variant_original(self, index):
        raise NotImplementedError("Please Implement this method")
