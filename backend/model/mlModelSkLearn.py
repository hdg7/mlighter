## @package MLighter
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
        
