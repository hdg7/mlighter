from .mlData import MLDataset
import pandas as pd
import io

class MLDataStructure(MLDataset):

    def loadData (self,className=None,dataFile=None,actualData=None, targetData=None):
        if(not dataFile is None):
            self.data=pd.read_csv(io.BytesIO(dataFile))
        elif(actualData is None):
            self.data=pd.read_csv(self.name)    
        if(not className is None):
            self.target = self.data.pop(className)
        if(not actualData is None):
            self.data = actualData
        if(not targetData is None):
            self.target = targetData
    

    def setTarget(self,className):
        self.target =self.data.pop(className)
        self.targetName=className
        
    def getColumns(self):
        return self.data.columns
        
    def cleanColumn(self,columnName):
        self.data.pop(columnName)

        
