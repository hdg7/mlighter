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
import pandas as pd

from dataset.mlDataStructure import MLDataStructure
from dataset.mlDataImage import MLDataImage
from dataset.mlDataAudio import MLDataAudio
from model.hugging_face_model import HuggingFaceModel
from model.mlModelSkLearn import MLModelSkLearn
from evasions.mlEvasionDiscreetNoise import MLEvasionDiscreteNoise
from evasions.mlEvasionContinousNoise import MLEvasionContinousNoise
from evasions.mlDescriptionTransformation import MLDescriptionTransformation
from evasions.testGen import MLEvasionSearch
from codereader.codeInfo import CallCollector
from codereader.importInfo import ImportCollector
import ast
import datetime
import os
import subprocess
import multiprocessing


class MLighter:
<<<<<<< HEAD
    def __init__(self, parameters={}):
        self.currentFolder = ""
        self.inputsFolder = ""
        self.outputsFolder = ""
        self.proc = None
        if "name" in parameters:
            self.name = parameters["name"]
=======

  def __init__(self,parameters={}):
    self.currentFolder = None
    self.inputsFolder = None
    self.outputsFolder = None
    self.proc = None
    self.testName = str(datetime.datetime.timestamp(datetime.datetime.now()))
    self.test_folder = self.testName
    if("name" in parameters):
      self.name = parameters["name"]
    else:
      self.name = "Unknown"


  def uploadDataset(self,dataType,datasetName=None,dataClass=None,dataFile=None,actualData=None, targetData=None):
    print("Uploading dataset " + dataType)
    if not datasetName is None:
      self.dataName = datasetName

    if(dataType == "structured" or dataType == "description"):
      self.data = MLDataStructure(self.dataName)
    elif(dataType == "image"):
      print("Image")
      self.data = MLDataImage(self.dataName)
      print("Image ->")
    elif(dataType == "audio"):
      self.data = MLDataAudio(self.dataName)

    print("Uploading datafile " + str(dataFile))

    if (not dataClass is None) or (not dataFile is None) or (not actualData is None) or (not targetData is None):
      print("Loading data")
      self.data.loadData(className=dataClass,dataFile=dataFile,actualData=actualData,targetData=targetData)
    else:
      print("No data provided")

  def uploadModel(self,modelType, modelName,modelUrl=None,modelFile=None,actualModel=None):
    print("Uploading model " + modelName + " of type " + modelType)
    self.modelName = modelName
    if(modelType == "sklearn"):
      self.model = MLModelSkLearn(self.modelName)
      if (not modelUrl is None):
        self.model.loadModel(modelUrl)
      elif (not modelFile is None):
        self.model.loadModelIO(modelFile)
      elif (not actualModel is None):
        self.model.model=actualModel
    elif(modelType == "huggingface"):
      print("Hugging Face Model")
      self.model = HuggingFaceModel(self.modelName)

  def prediction(self,sample, original_text=None):
    p = self.model.predict(sample, original_text)
    print(p)
    return p

  def prediction_proba(self,sample):
    return self.model.predict_proba(sample)

  def chooseStrategy(self,strategyName):
    self.strategyName = strategyName

  def chooseTransformation(self, transformationName):
    if (transformationName == "discrete"):
      self.transformation = MLEvasionDiscreetNoise(self.strategyName)
    elif (transformationName == "continuous"):
      self.transformation = MLEvasionContinousNoise(self.strategyName)
    elif (transformationName == "genAlg"):
      self.transformation = MLEvasionSearch(self.strategyName)
    elif (transformationName == "descriptions"):
      self.transformation = MLDescriptionTransformation(self.strategyName)

  def setupTransformation(self, config):
    self.transformation.transformationSetup(config)
    
  def uploadCodeReview(self, language="python",fileName=None,codeContent=None):
    codeReviewData = None
    if (not (language == "python" or language=="R")):
      print("language not supported")
      return
    if (not fileName is None):
      with open(fileName, 'r') as f:
        codeReviewData = f.read()
    elif (not codeContent is None):
      codeReviewData = codeContent
    else:
      print("You need to provide the code")
    if (not codeReviewData is None):  
      self.codeReviewTree = ast.parse(codeReviewData)

  def setCurrentFolder(self,folderPath=None):
    if (folderPath is None):
      self.currentFolder = os.getenv('MLIGHTER_FOLDER')    
      if(self.currentFolder is None):
        self.currentFolder = os.popen('pwd').read()
        self.currentFolder=self.currentFolder.rstrip()
    else:
      self.currentFolder=folderPath


  def setTestName(self, testName=None):
    if (not testName is None):
      self.testName = testName + "_" + str(datetime.datetime.timestamp(datetime.datetime.now()))
    else:
        self.testName = str(datetime.datetime.timestamp(datetime.datetime.now()))

    self.test_folder = self.testName

    return self.testName


  def resetSession(self):
    self.currentFolder = None
    self.inputsFolder = None
    self.outputsFolder = None
    self.proc = None
    self.testName = str(datetime.datetime.timestamp(datetime.datetime.now()))
    self.test_folder = self.testName

  def upload_aux_files(self, aux_files):
    """
    Uploads auxiliary files to the current folder
    :param aux_files: list of dictionaries with the following structure
    {
        "name": "name of the file",
        "content": "content of the file"
    }
    """
    if (self.currentFolder is None):
      self.setCurrentFolder()

    if not os.path.exists(os.path.join(self.currentFolder, self.test_folder)):
      os.makedirs(os.path.join(self.currentFolder, self.test_folder))

    for aux_file in aux_files:
      aux_path = os.path.join(self.currentFolder, self.test_folder, aux_file["name"])

      f = open(aux_path, "w")
      f.write(aux_file["content"])
      f.close()

  def uploadCodeTemplate(self, language="python",fileName=None,codeContent=None):
    if(self.currentFolder is None):
      self.setCurrentFolder()
    if (not (language == "python" or language=="R")):
      print("language not supported")
      return
    if (not fileName is None):
      self.codeTemplate = fileName
      self.setCurrentFolder(os.path.dirname(fileName))
    elif (not codeContent is None):
      if not os.path.exists(os.path.join(self.currentFolder, self.test_folder)):
        os.makedirs(os.path.join(self.currentFolder, self.test_folder))
      if(language == "python"):
        self.codeTemplate = os.path.join(self.currentFolder, self.test_folder, "template_" + self.testName + ".py")
      elif(language == "R"):
        self.codeTemplate = os.path.join(self.currentFolder, self.test_folder, "template_" + self.testName + ".R")
      else:
        self.codeTemplate = os.path.join(self.currentFolder, self.test_folder, "template_" + self.testName + ".txt")
      f = open(self.codeTemplate, "w")
      f.write(codeContent)
      f.close()
    else:
      print("You need to provide the template")

  def uploadCodeInput(self, fileName=None,codeContent=None):
    if(self.currentFolder is None):
      self.setCurrentFolder()
    if(self.inputsFolder is None):
      self.testExperimentName="exp_" + self.testName
      self.inputsFolder=self.currentFolder + "/inputs_" + self.testExperimentName
      self.outputsFolder=self.currentFolder + "/outputs_" + self.testExperimentName
      os.system("mkdir " + self.inputsFolder)
      print("mkdir " + self.inputsFolder)
    if (not fileName is None):
      print(fileName)
      self.caseInput = os.system("cp " + fileName + " " + self.inputsFolder)
    elif (not codeContent is None):
      self.caseInput = "input_" + self.testName + ".txt"
      f = open(self.inputsFolder + "/" + self.caseInput, "wb")
      f.write(codeContent)
      f.close()
    else:
      print("You need to provide the input")


  def runCodeTesting(self, language="Python"):
    if(self.proc is None):
      #print("Preparing running process")
      screen_name = "mlTest_" + self.testName
      if(self.codeTemplate.lower().endswith(".py")):
        self.proc = subprocess.Popen('screen -d -m -S ' + screen_name + ' py-afl-fuzz -m 4000 -t10000 -i ' + self.inputsFolder + ' -o ' + self.outputsFolder + ' -- python3 ' + self.codeTemplate + ' @@', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
      elif (self.codeTemplate.lower().endswith(".r")):
        self.proc = subprocess.Popen('screen -d -m -S ' + screen_name + ' afl-fuzz -t10000 -i ' + self.inputsFolder + ' -o ' + self.outputsFolder + ' -- Rscript ' + self.codeTemplate + ' @@', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
      else:
        print("Language unknown, please check the file extension")
        return
      self.lastUpdate = multiprocessing.Value('i', 0)
      #print('screen -d -m -S mlTest py-afl-fuzz -m 4000 -t10000 -i ' + self.inputsFolder + ' -o ' + self.outputsFolder + ' -- python3 ' + self.codeTemplate + ' @@')
      #print("Process running")
#      for stdout_line in iter(self.proc.stderr.readline, ""):
#        yield stdout_line
    else:
      print("There is a process running")


  def getRunningTests(self):
    """Gets the names of the running screen sessions prepended with mlTest_"""
    screenSessions = os.popen('screen -ls | grep mlTest').read().split('\n')
    screenSessions = [x.split('\t')[1] for x in screenSessions if len(x) > 0]
    # strip the "mlTest_" from the screen session names but also anything preceeding it
    screenSessions = [x.split("mlTest_")[1] for x in screenSessions if len(x) > 0]

    return screenSessions


  def getAllTests(self, displayRunning=False):
    """reads what output folders are available from within the currentdir"""
    if (self.currentFolder is None):
      self.setCurrentFolder()

    testList = os.listdir(self.currentFolder)
    testList = [x for x in testList if x.startswith("outputs_")]
    testList = [x.replace("outputs_exp_", "") for x in testList]

    if (displayRunning):
      runningTests = self.getRunningTests()

      testList = list(map(lambda x: (x, x in runningTests), testList))

    return testList


  def reconnectToSession(self, sessionName):
    self.lastUpdate = multiprocessing.Value('i', 0)
    if (self.currentFolder is None):
      self.setCurrentFolder()

    self.testName = sessionName

    self.testExperimentName = "exp_" + sessionName

    self.inputsFolder=self.currentFolder + "/inputs_" + self.testExperimentName
    self.outputsFolder=self.currentFolder + "/outputs_" + self.testExperimentName


  def retrieveTestingState(self,AFLOri=None):
    if AFLOri is None:
      f = open(self.outputsFolder + "/default/fuzzer_stats", "r")
    else:
      f = open(self.outputsFolder + "/fuzzer_stats", "r")
    data=f.readlines()
    dictData={}
    for elem in data:
        dictData[elem.strip().split()[0]]=elem.strip().split()[2]
    if(self.lastUpdate.value != int(dictData["last_update"])):
        self.lastUpdate.value=int(dictData["last_update"])
        if not AFLOri is None:
          return {"Current Time" : dictData["last_update"],
                "Execs" : dictData["execs_done"],
                "Paths" : dictData["paths_total"],
                "Crashes" : dictData["unique_crashes"],
                "Hangs" : dictData["unique_hangs"]}
        else:
          return {"Current Time" : dictData["last_update"],
                "Execs" : dictData["execs_done"],
                "Paths" : dictData["pending_total"],
                "Crashes" : dictData["saved_crashes"],
                "Hangs" : dictData["saved_hangs"]}
  
  def evaluateCodeReview(self):
    cc = CallCollector()
    ic = ImportCollector()
    cc.visit(self.codeReviewTree)
    ic.get_imports(self.codeReviewTree)
    self.calls=cc.calls
    self.impo=ic.impCalls
    self.listdual=[]
    for elem in self.impo:
        if(elem[1]==[]):
          name=elem[0][-1]
          if(not elem[2] is None):
            name=elem[2]
          candidates=list(filter(lambda x:name in x, self.calls))
          for case in candidates:
            namesCalls=case.split('.')
            elemdual={"module":elem[0],"function":namesCalls[1],"alias":elem[2]}
            self.listdual.append(elemdual)
>>>>>>> main
        else:
            self.name = "Unknown"

<<<<<<< HEAD
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
=======
  @staticmethod
  def expected_vs_actual_hf(expected, actual):
    expected = expected.copy()
    actual = actual.copy()
    print(len(actual))
    try:
      # Check if actual contains an original_description and original_labels columns
      if 'original_description' in actual.columns and 'original_label' in actual.columns:
        print("Original columns found")

        print(expected)
        print("--------------------------------------------")
        print(actual)

        actual['expected_labels'] = expected[actual.index]

        actual['variant_expected'] = actual.apply(lambda row: row['label'] in row['expected_labels'], axis=1)
        actual['original_expected'] = actual.apply(lambda row: row['original_label'] in row['expected_labels'], axis=1)

        actual['expected_label'] = None
        actual.loc[actual['variant_expected'], 'expected_label'] = actual.loc[actual['variant_expected'], 'label']
        actual.loc[actual['original_expected'], 'expected_label'] = actual.loc[actual['original_expected'], 'original_label']

        actual.drop(columns=['expected_labels'], inplace=True)

        expected = expected.apply(ast.literal_eval)

        for idx, labels in expected.items():
          for label in labels:
            if label not in actual.loc[actual['idx'] == idx, 'label'].values:
              actual = pd.concat([actual, pd.DataFrame({'description': actual.loc[actual['idx'] == idx, 'description'].values[0],
                                                      'original_description': actual.loc[actual['idx'] == idx, 'original_description'].values[0],
                                                      'label': None,
                                                      'prediction': 0.0,
                                                      'original_label': None,
                                                      'original_prediction': 0.0,
                                                      'variant_expected': False,
                                                      'original_expected': False,
                                                      'expected_label': label,
                                                      }, index=[0])])

        return actual
      else:
        print("Original columns not found")
        actual['expected_labels'] = expected[actual.index]

        # We now have
        # | description | label | predicted | expected_labels |
        # | "something" | 1     | True      |[lab, lab]       |
        # we need to go through each row checking if the label is in the expected_labels, if so
        # we set the expected to True, otherwise False
        # we simultaneously set predicted to true on everything

        actual['expected'] = actual.apply(lambda row: row['label'] in row['expected_labels'], axis=1)
        actual['predicted'] = True

        actual.drop(columns=['expected_labels'], inplace=True)

        print(expected)
        expected = expected.apply(ast.literal_eval)

        # now we need to add any missing labels from expected to actual matching on index
        for idx, labels in expected.items():
          print(idx, labels)
          for label in labels:
            print(idx, label)
            if label not in actual.loc[actual['idx'] == idx, 'label'].values:
              actual = pd.concat([actual, pd.DataFrame({'description': actual.loc[actual['idx'] == idx, 'description'].values[0],
                                                      'label': label,
                                                      'predicted': False,
                                                      'expected': True,
                                                      'prediction': 0.0}, index=[0])])

        return actual

    except Exception as e:
        print(e)
        return pd.DataFrame(columns=['description', 'label', 'predicted', 'expected', 'probability'])
>>>>>>> main
