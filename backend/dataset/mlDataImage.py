from .mlData import MLDataset
import joblib
from skimage.io import imread
from skimage.transform import resize

class MLDataImage(MLDataset):
    def loadData (self,className=None,dataFile=None):
        if(not dataFile is None):
            self.data=pd.read_csv(io.BytesIO(dataFile))
        else:
            self.data=pd.read_csv(self.name)    
        if(not className is None):
            self.target = self.data.pop(className)

    def setTarget(self,className):
        self.target =self.data.pop(className)

    
