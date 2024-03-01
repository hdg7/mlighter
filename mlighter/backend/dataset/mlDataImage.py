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
import io

import pandas as pd

from .mlData import MLDataset
import joblib
from skimage.io import imread
from skimage.transform import resize

class MLDataImage(MLDataset):
    def loadData(self,className=None, dataFile=None, actualData=None, targetData=None):
        print("Loading Image")
        if(not dataFile is None):
            self.data=pd.read_csv(io.BytesIO(dataFile))
        else:
            self.data=pd.read_csv(self.name)    
        if(not className is None):
            self.target = self.data.pop(className)
        else:
            self.target = self.data.pop(self.data.columns[-1])

        print(self.data)
        print(self.target)

    def setTarget(self,className):
        self.target =self.data.pop(className)

    def getColumns(self):
        return self.data.columns
    
