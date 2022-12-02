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
from joblib import dump, load
from .mlModel import MLModel
from io import BytesIO
from tempfile import TemporaryFile

class MLModelSkLearn(MLModel):

    def loadModel(self,modelURL):
        self.model = load(modelURL)
        print("loaded",type(self.model))

    def loadModelIO(self,modelFile):
        fileTemp=TemporaryFile(mode="w+b")
        fileTemp.write(modelFile)
        fileTemp.seek(0)
        self.model=load(fileTemp)
        print("loaded",type(self.model))
        
