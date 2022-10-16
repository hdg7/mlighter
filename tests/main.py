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

sys.path.append(os.environ["MLIGHTER_HOME"])

from MLighter import MLighter
parameters = {"name":"iris.csv"}
session = MLighter(parameters)
session.uploadDataset("structured","example/iris.csv","target")
print(session.data.getColumns())
session.uploadModel("sklearn","iris",modelUrl="example/iris.joblib")
session.data.cleanColumn("Unnamed: 0")
session.prediction(session.data.data)
session.chooseStrategy("noise")
session.chooseTransformation("discreet")
config={"numberVariants":2,"shift":0,"noise":1,"features":[0,0,1,1]}
session.setupTransformation(config)
session.data.transform(session.transformation)

variants = session.data.getVariants()
print(session.prediction(variants))
