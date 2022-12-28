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

import sys
import os
from sklearn import datasets


try:
    home = os.environ["MLIGHTER_HOME"]
except KeyError:
    home = os.environ["HOME"]
    homeTool = home + "/mlighter/mlighter"
homeLib = homeTool + "/backend"
sys.path.append(homeLib)

from MLighter import MLighter
iris = datasets.load_iris()
session = MLighter()
session.uploadDataset("structured",datasetName="iris",actualData=iris.data,
                      targetData=iris.target)
#print(session.data.getColumns())
session.uploadModel("sklearn","iris",modelUrl=homeTool + "/tests/example/irisProb.joblib")
#session.data.cleanColumn("Unnamed: 0")
session.prediction(session.data.data)
session.chooseStrategy("search")
session.chooseTransformation("genAlg")
config=session.transformation.ga_config()
config["numtuples"]=4
config["noise"]=1
config["features"]=[1,1,1,1]
config["predictor"]=session.prediction_proba
config["oriVariant"]=1
config["weights"]=(-1.0,1.0,1.0)
config["numberVariants"]=1
config["shift"]=0
config["numgen"]=50
config["population_size"]=100
config["lambda_sel"]=50
config["mu_sel"]=50
config["class"]=1

session.setupTransformation(config)
#print(session.prediction_proba([session.data.data.iloc[config["oriVariant"]]]))
#print("\n")
#print(session.data.data.head(1)+session.data.data.iloc[config["oriVariant"]])
#print("\n")
#print(session.data.data.iloc[config["oriVariant"]])
#print(session.prediction_proba(session.data.data[config["oriVariant"]:config["oriVariant"]+1]))
#print(session.data.data[config["oriVariant"]:config["oriVariant"]+1])
#The number is for the original variant position
session.data.transform(session.transformation)
variants = session.data.getVariants()
print(variants)
print(session.prediction(session.data.data))
print(session.prediction(session.data.data)[config["oriVariant"]])
print(session.prediction(variants))
#print(session.prediction_proba(variants))
