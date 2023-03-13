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

from dataset.mlDataStructure import MLDataStructure
from dataset.mlDataImage import MLDataImage
from dataset.mlDataAudio import MLDataAudio
from model.mlModelSkLearn import MLModelSkLearn
from evasions.mlEvasionDiscreetNoise import MLEvasionDiscreteNoise
from evasions.mlEvasionContinousNoise import MLEvasionContinousNoise
from evasions.testGen import MLEvasionSearch
from codereader.codeInfo import CallCollector
from codereader.importInfo import ImportCollector
import ast
import datetime
import os
import subprocess
import multiprocessing


class MLighter:
    def __init__(self, parameters={}):
        self.currentFolder = ""
        self.inputsFolder = ""
        self.outputsFolder = ""
        self.proc = None
        if "name" in parameters:
            self.name = parameters["name"]
        else:
            self.name = "Unknown"

    def uploadDataset(
        self,
        dataType,
        datasetName=None,
        dataClass=None,
        dataFile=None,
        actualData=None,
        targetData=None,
    ):
        if datasetName is not None:
            self.dataName = datasetName
        if dataType == "structured":
            self.data = MLDataStructure(self.dataName)
        if dataType == "image":
            self.data = MLDataImage(self.dataName)
        if dataType == "audio":
            self.data = MLDataAudio(self.dataName)
        if (
            dataClass is not None
            or dataFile is not None
            or actualData is not None
            or targetData is not None
        ):
            self.data.loadData(
                className=dataClass,
                dataFile=dataFile,
                actualData=actualData,
                targetData=targetData,
            )

    def uploadModel(
        self, modelType, modelName, modelUrl=None, modelFile=None, actualModel=None
    ):
        self.modelName = modelName
        if modelType == "sklearn":
            self.model = MLModelSkLearn(self.modelName)
            if modelUrl is not None:
                self.model.loadModel(modelUrl)
            elif modelFile is not None:
                self.model.loadModelIO(modelFile)
            elif actualModel is not None:
                self.model.model = actualModel

    def prediction(self, sample):
        return self.model.predict(sample)

    def prediction_proba(self, sample):
        return self.model.predict_proba(sample)

    def chooseStrategy(self, strategyName):
        self.strategyName = strategyName

    def chooseTransformation(self, transformationName):
        if transformationName == "discreet":
            self.transformation = MLEvasionDiscreteNoise(self.strategyName)
        elif transformationName == "continous":
            self.transformation = MLEvasionContinousNoise(self.strategyName)
        elif transformationName == "genAlg":
            self.transformation = MLEvasionSearch(self.strategyName)

    def setupTransformation(self, config):
        self.transformation.transformationSetup(config)

    def uploadCodeReview(self, language="python", fileName=None, codeContent=None):
        if language != "python":
            print("language not supported")
            return

        if fileName is not None and codeContent is not None:
            # TODO talk to Hector
            print("we only require a filename, or code content, not both")
            return

        codeReviewData = ""
        if fileName is not None:
            with open(fileName, "r") as f:
                codeReviewData = f.read()
        elif codeContent is not None:
            codeReviewData = codeContent
        else:
            print("you need to provde the code")

        if not codeReviewData:
            exit(-1)
        else:
            try:
                self.codeReviewTree = ast.parse(codeReviewData)
            except SyntaxError as error:
                print(f"invalid syntax {error}")
                exit(-1)

    def setCurrentFolder(self, folderPath=None):
        if folderPath is None:
            self.currentFolder = os.getcwd()
        else:
            if os.path.isdir(folderPath):
                self.currentFolder = folderPath
            else:
                # TODO what is the sensible default behaviour?
                pass

    def uploadCodeTemplate(self, language="python", fileName=None, codeContent=None):
        if not self.currentFolder:
            self.setCurrentFolder()
        if not language == "python":
            print("language not supported")
            return
        if fileName is not None:
            self.codeTemplate = fileName
            self.setCurrentFolder(os.path.dirname(fileName))
        elif codeContent is not None:
            self.codeTemplate = (
                self.currentFolder
                + "template_"
                + str(datetime.datetime.timestamp(datetime.datetime.now()))
                + ".txt"
            )
            with open(self.codeTemplate, "w") as f:
                f.write(codeContent)
        else:
            print("You need to provide the template")

    def uploadCodeInput(self, fileName=None, codeContent=None):
        if not self.currentFolder:
            self.setCurrentFolder()

        if not self.inputsFolder:
            self.testExperimentName = "exp_" + str(
                datetime.datetime.timestamp(datetime.datetime.now())
            )
            self.inputsFolder = (
                self.currentFolder + "/inputs_" + self.testExperimentName
            )
            self.outputsFolder = (
                self.currentFolder + "/outputs_" + self.testExperimentName
            )

            try:
                os.mkdir(self.inputsFolder)
            except OSError as error:
                print(error)
                exit(-1)

        if fileName is not None:
            print(fileName)
            self.caseInput = os.system("cp " + fileName + " " + self.inputsFolder)
        elif codeContent is not None:
            self.caseInput = (
                "input_"
                + str(datetime.datetime.timestamp(datetime.datetime.now()))
                + ".txt"
            )
            with open(self.inputsFolder + "/" + self.caseInput, "wb") as f:
                f.write(codeContent)
        else:
            print("You need to provide the input")

    def runCodeTesting(self):
        if self.proc is None:
            # TODO figure out how to remove screen dependency
            self.proc = subprocess.Popen(
                [
                    "screen",
                    "-d",
                    "-m",
                    "-S",
                    "mlTest",
                    "py-afl-fuzz",
                    "-m",
                    "4000",
                    "-t10000",
                    "-i",
                    self.inputsFolder,
                    "-o",
                    self.outputsFolder,
                    "-- python3",
                    self.codeTemplate,
                    " @@",
                ],
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            self.lastUpdate = multiprocessing.Value("i", 0)
        else:
            print("There is a process running")

    def retrieveTestingState(self):
        if self.outputsFolder:
            with open(self.outputsFolder + "/fuzzer_stats", "r") as f:
                data = f.readlines()
                dictData = {}
                for elem in data:
                    for elem in data:
                        kv = elem.strip().split()
                        dictData[kv[0]] = kv[2]
                    with self.lastUpdate.get_lock():
                        # if self.lastUpdate.value != int(dictData["last_update"]):
                        self.lastUpdate.value = int(dictData["last_update"])
                    return {
                        "Current Time": dictData["last_update"],
                        "Execs": dictData["execs_done"],
                        "Paths": dictData["paths_total"],
                        "Crashes": dictData["unique_crashes"],
                        "Hangs": dictData["unique_hangs"],
                    }
        else:
            # TODO
            pass

    def evaluateCodeReview(self):
        cc = CallCollector()
        ic = ImportCollector()
        cc.visit(self.codeReviewTree)
        ic.get_imports(self.codeReviewTree)
        self.calls = cc.calls
        self.impo = ic.impCalls
        self.listdual = []
        for elem in self.impo:
            if elem[1] == []:
                name = elem[0][-1]
                if elem[2] is not None:
                    name = elem[2]
                candidates = list(filter(lambda x: name in x, self.calls))
                for case in candidates:
                    namesCalls = case.split(".")
                    elemdual = {
                        "module": elem[0],
                        "function": namesCalls[1],
                        "alias": elem[2],
                    }
                    self.listdual.append(elemdual)
            else:
                elemdual = {"module": elem[0], "function": elem[1], "alias": elem[2]}
                self.listdual.append(elemdual)
        return self.listdual
