## @package MLigther
#    Copyright 2022 Hector D. Menendez, Aidan Dakhama
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
from evasions.mlEvasionDiscreetNoise import MLEvasionDiscreetNoise
from evasions.mlEvasionContinousNoise import MLEvasionContinousNoise
from evasions.testGen import MLEvasionSearch
from codereader.codeInfo import CallCollector
from codereader.importInfo import ImportCollector
import ast
import datetime
import os
import subprocess
import multiprocessing
import logging
import shutil

def init_global_logger():
    print("Initializing global logger")
    # Prepare logging
    logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      handlers=[
                          logging.FileHandler("MLighter.log"),
                          logging.StreamHandler()
                      ])
    logging.basicConfig(level=logging.NOTSET)


class MLighter:

    def __init__(self, parameters=None):
        # Logger
        init_global_logger()
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initializing MLighter session with parameters: {}".format(parameters))

        # Parameter parsing
        if (not parameters is None) and "name" in parameters:
            self.name = parameters["name"]
        else:
            self.name = "Unknown"

        # Code Testing

        # Filesystem setup
        self.currentFolder = None   # Current folder where the session is running
        self.inputsFolder = None    # Folder for afl inputs
        self.outputsFolder = None   # Folder for afl outputs

        # Test setup
        self.testName = str(datetime.datetime.timestamp(datetime.datetime.now()))  # Name of the test, defaults to timestamp
        self.test_folder = self.testName    # Folder where the test is running

        self.logger.debug("Current test name: {}".format(self.testName))
        self.logger.debug("Current test folder: {}".format(self.test_folder))

        # Test process
        self.proc = None

        self.codeTemplate = None
        self.codeReviewTree = None
        self.testExperimentName = None
        self.lastUpdate = None
        self.calls = None
        self.imports = None
        self.list_dual = None

        # ML setup
        self.dataName = ""
        self.data = None
        self.modelName = ""
        self.model = None

        self.strategyName = ""
        self.transformation = None

        self.logger.info("MLighter session created")

    def upload_dataset(self, data_type, dataset_name=None, data_class=None, data_file=None, actual_data=None,
                      target_data=None):
        self.logger.debug("Uploading dataset with parameters: data_type={}, dataset_name={}, data_class={}, data_file={}, actual_data={}, target_data={}".format(
            data_type, dataset_name, data_class, data_file, actual_data, target_data
        ))
        if not dataset_name is None:
            self.dataName = dataset_name
        if data_type == "structured":
            self.data = MLDataStructure(self.dataName)
        if data_type == "image":
            self.data = MLDataImage(self.dataName)
        if data_type == "audio":
            self.data = MLDataAudio(self.dataName)
        if ((not data_class is None) or (not data_file is None)
                or (not actual_data is None) or (not target_data is None)):
            self.data.loadData(className=data_class, dataFile=data_file, actualData=actual_data, targetData=target_data)

    def upload_model(self, model_type, model_name, model_url=None, model_file=None, actual_model=None):
        self.logger.debug("Uploading model with parameters: model_type={}, model_name={}, model_url={}, model_file={}, actual_model={}".format(
            model_type, model_name, model_url, model_file, actual_model
        ))
        self.modelName = model_name
        if model_type == "sklearn":
            self.model = MLModelSkLearn(self.modelName)
            if not model_url is None:
                self.model.loadModel(model_url)
            elif not model_file is None:
                self.model.loadModelIO(model_file)
            elif not actual_model is None:
                self.model.model = actual_model

    def prediction(self, sample):
        self.logger.debug("Making prediction with sample: {}".format(sample))
        return self.model.predict(sample)

    def prediction_probability(self, sample):
        self.logger.debug("Making prediction probability with sample: {}".format(sample))
        return self.model.predict_proba(sample)

    def choose_strategy(self, strategy_name):
        self.logger.debug("Updating strategy to name: {}".format(strategy_name))
        self.strategyName = strategy_name

    def choose_transformation(self, transformation_name):
        self.logger.debug("Updating transformation to name: {}".format(transformation_name))
        if transformation_name == "discrete":
            self.transformation = MLEvasionDiscreetNoise(self.strategyName)
        elif transformation_name == "continuous":
            self.transformation = MLEvasionContinousNoise(self.strategyName)
        elif transformation_name == "genAlg":
            self.transformation = MLEvasionSearch(self.strategyName)

    def setup_transformation(self, config):
        self.logger.debug("Setting up transformation with config: {}".format(config))
        self.transformation.transformationSetup(config)

    def upload_code_review(self, language="python", file_name=None, code_content=None):
        code_review_data = None
        if not (language == "python" or language == "R"):
            self.logger.error("Language not supported")
            return
        if not file_name is None:
            with open(file_name, 'r') as f:
                code_review_data = f.read()
        elif not code_content is None:
            code_review_data = code_content
        else:
            self.logger.error("You need to provide the code")
        if not code_review_data is None:
            self.codeReviewTree = ast.parse(code_review_data)

    def set_current_folder(self, folder_path=None):
        if folder_path is None:
            self.currentFolder = os.getenv('MLIGHTER_FOLDER')
            if self.currentFolder is None:
                self.currentFolder = os.popen('pwd').read()
                self.currentFolder = self.currentFolder.rstrip()
        else:
            self.currentFolder = folder_path

    def set_test_name(self, test_name=None):
        old_test_name = self.testName

        if not test_name is None:
            self.testName = test_name + "_" + str(datetime.datetime.timestamp(datetime.datetime.now()))
        else:
            self.testName = str(datetime.datetime.timestamp(datetime.datetime.now()))

        self.test_folder = self.testName

        self.logger.debug("Updating test name from {} to {}".format(old_test_name, self.testName))

        return self.testName

    def reset_session(self):
        self.logger.debug("Resetting session with name: {}".format(self.testName))
        self.currentFolder = None
        self.inputsFolder = None
        self.outputsFolder = None
        self.proc = None
        self.testName = str(datetime.datetime.timestamp(datetime.datetime.now()))
        self.test_folder = self.testName
        self.logger.debug("Reset session to name: {}".format(self.testName))

    def upload_aux_files(self, aux_files):
        """
        Uploads auxiliary files to the current folder
        :param aux_files: list of dictionaries with the following structure
        {
            "name": "name of the file",
            "content": "content of the file"
        }
        """
        self.logger.debug("Uploading auxiliary files: {}".format(aux_files))
        if self.currentFolder is None:
            self.set_current_folder()

        if not os.path.exists(os.path.join(self.currentFolder, self.test_folder)):
            os.makedirs(os.path.join(self.currentFolder, self.test_folder))

        for (i, aux_file) in enumerate(aux_files):
            self.logger.debug("Uploading auxiliary file ({} of {}): {}".format(i + 1, len(aux_files) + 1, aux_file))
            aux_path = os.path.join(self.currentFolder, self.test_folder, aux_file["name"])
            try:
                f = open(aux_path, "w")
                f.write(aux_file["content"])
                f.close()
            except Exception as e:
                self.logger.error("Error uploading auxiliary file: {}".format(e))

    def upload_code_template(self, language="python", file_name=None, code_content=None):
        self.logger.debug("Uploading code template with parameters: language={}, file_name={}, code_content={}".format(
            language, file_name, code_content
        ))
        if self.currentFolder is None:
            self.set_current_folder()
        if not (language == "python" or language == "R"):
            self.logger.error("Language not supported")
            return
        if not file_name is None:
            self.codeTemplate = file_name
            self.set_current_folder(os.path.dirname(file_name))
        elif not code_content is None:
            if not os.path.exists(os.path.join(self.currentFolder, self.test_folder)):
                os.makedirs(os.path.join(self.currentFolder, self.test_folder))
            if language == "python":
                self.codeTemplate = os.path.join(self.currentFolder, self.test_folder,
                                                 "template_" + self.testName + ".py")
            elif language == "R":
                self.codeTemplate = os.path.join(self.currentFolder, self.test_folder,
                                                 "template_" + self.testName + ".R")
            else:
                self.codeTemplate = os.path.join(self.currentFolder, self.test_folder,
                                                 "template_" + self.testName + ".txt")
            try:
                f = open(self.codeTemplate, "w")
                f.write(code_content)
                f.close()
            except Exception as e:
                self.logger.error("Error uploading code template: {}".format(e))
        else:
            self.logger.error("You need to provide the code")

    def upload_code_input(self, file_name=None, code_content=None):
        self.logger.debug("Uploading code input with parameters: file_name={}, code_content={}".format(
            file_name, code_content
        ))
        if self.currentFolder is None:
            self.set_current_folder()
        if self.inputsFolder is None:
            self.testExperimentName = "exp_" + self.testName
            self.inputsFolder = self.currentFolder + "/inputs_" + self.testExperimentName
            self.outputsFolder = self.currentFolder + "/outputs_" + self.testExperimentName
            os.makedirs(self.inputsFolder, exist_ok=True)
            self.logger.debug("Created inputs folder: {}".format(self.inputsFolder))
        if (not file_name is None):
            print(file_name)
            #self.caseInput = os.system("cp " + file_name + " " + self.inputsFolder)
            shutil.copy(file_name, self.inputsFolder)
            self.caseInput = os.path.basename(file_name)
            self.logger.debug("Copied input file: {} to {}".format(file_name, self.inputsFolder))
            self.logger.debug("Input file name: {}".format(self.caseInput))
        elif not code_content is None:
            self.caseInput = "input_" + self.testName + ".txt"
            try:
                f = open(self.inputsFolder + "/" + self.caseInput, "wb")
                f.write(code_content)
                f.close()
            except Exception as e:
                self.logger.error("Error uploading code input: {}".format(e))
        else:
            self.logger.error("You need to provide the input")

    def run_code_testing(self, language="Python"):
        self.logger.debug("Running code testing with language: {}".format(language))
        if self.proc is None:
            screen_name = "mlTest_" + self.testName
            self.logger.debug("Screen name: {}".format(screen_name))
            if self.codeTemplate.lower().endswith(".py"):
                command = 'screen -d -m -S ' + screen_name + ' py-afl-fuzz -m 4000 -t10000 -i ' + self.inputsFolder + ' -o ' + self.outputsFolder + ' -- python3 ' + self.codeTemplate + ' @@'
                self.proc = subprocess.Popen(
                    command,
                    shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE
                )
                self.logger.debug("Process {} running with command: {}".format(
                    self.proc.pid, command
                ))
            elif self.codeTemplate.lower().endswith(".r"):
                command = 'screen -d -m -S ' + screen_name + ' afl-fuzz -t10000 -i ' + self.inputsFolder + ' -o ' + self.outputsFolder + ' -- Rscript ' + self.codeTemplate + ' @@'
                self.proc = subprocess.Popen(
                    command,
                    shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE
                )
                self.logger.debug("Process {} running with command: {}".format(
                    self.proc.pid, command
                ))
            else:
                self.logger.error("Language not recognised")
                return
            self.lastUpdate = multiprocessing.Value('i', 0)
            # print('screen -d -m -S mlTest py-afl-fuzz -m 4000 -t10000 -i ' + self.inputsFolder + ' -o ' + self.outputsFolder + ' -- python3 ' + self.codeTemplate + ' @@')
            # print("Process running")
            # for stdout_line in iter(self.proc.stderr.readline, ""):
            #    yield stdout_line
        else:
            self.logger.error("Process already running")

    def get_running_tests(self):
        """Gets the names of the running screen sessions prepended with mlTest_"""
        self.logger.debug("Getting running tests")
        screen_sessions = os.popen('screen -ls | grep mlTest').read().split('\n')
        screen_sessions = [x.split('\t')[1] for x in screen_sessions if len(x) > 0]
        # strip the "mlTest_" from the screen session names but also anything preceding it
        screen_sessions = [x.split("mlTest_")[1] for x in screen_sessions if len(x) > 0]

        return screen_sessions

    def get_all_tests(self, display_running=False):
        """reads what output folders are available from within the currentdir"""
        if self.currentFolder is None:
            self.set_current_folder()

        test_list = os.listdir(self.currentFolder)
        test_list = [x for x in test_list if x.startswith("outputs_")]
        test_list = [x.replace("outputs_exp_", "") for x in test_list]

        if display_running:
            running_tests = self.get_running_tests()

            test_list = list(map(lambda x: (x, x in running_tests), test_list))

        self.logger.debug("Getting all tests: {}".format(test_list))

        return test_list

    def reconnect_to_session(self, session_name):
        self.logger.debug("Reconnecting to session with name: {}".format(session_name))
        self.lastUpdate = multiprocessing.Value('i', 0)
        if self.currentFolder is None:
            self.set_current_folder()

        self.testName = session_name

        self.testExperimentName = "exp_" + session_name

        self.inputsFolder = self.currentFolder + "/inputs_" + self.testExperimentName
        self.outputsFolder = self.currentFolder + "/outputs_" + self.testExperimentName
        # TODO: Check if the session exists

    def retrieve_testing_state(self, afl_ori=None):
        self.logger.debug("Retrieving testing state with afl_ori: {}".format(afl_ori))
        if afl_ori is None:
            f = open(self.outputsFolder + "/default/fuzzer_stats", "r")
        else:
            f = open(self.outputsFolder + "/fuzzer_stats", "r")
        data = f.readlines()
        dict_data = {}
        for elem in data:
            dict_data[elem.strip().split()[0]] = elem.strip().split()[2]
        if self.lastUpdate.value != int(dict_data["last_update"]):
            self.logger.debug("Updating last update value from {} to {}".format(
                self.lastUpdate.value, int(dict_data["last_update"])
            ))
            self.lastUpdate.value = int(dict_data["last_update"])
            if not afl_ori is None:
                return {
                    "Current Time": dict_data["last_update"],
                    "Execs": dict_data["execs_done"],
                    "Paths": dict_data["paths_total"],
                    "Crashes": dict_data["unique_crashes"],
                    "Hangs": dict_data["unique_hangs"]
                }
            else:
                return {
                    "Current Time": dict_data["last_update"],
                    "Execs": dict_data["execs_done"],
                    "Paths": dict_data["pending_total"],
                    "Crashes": dict_data["saved_crashes"],
                    "Hangs": dict_data["saved_hangs"]
                }

    def evaluate_code_review(self):
        self.logger.debug("Evaluating code review")
        cc = CallCollector()
        ic = ImportCollector()

        cc.visit(self.codeReviewTree)
        ic.get_imports(self.codeReviewTree)

        self.calls = cc.calls
        self.imports = ic.impCalls
        self.list_dual = []

        for (i, elem) in enumerate(self.imports):
            self.logger.debug("Evaluating import ({} of {}): {}".format(i + 1, len(self.imports) + 1, elem))
            if elem[1] == []:
                name = elem[0][-1]

                if not elem[2] is None:
                    name = elem[2]

                candidates = list(filter(lambda x: name in x, self.calls))

                for case in candidates:
                    names_calls = case.split('.')
                    elem_dual = {
                        "module": elem[0],
                        "function": names_calls[1],
                        "alias": elem[2]
                    }

                    self.list_dual.append(elem_dual)
            else:
                elem_dual = {
                    "module": elem[0],
                    "function": elem[1],
                    "alias": elem[2]
                }

                self.list_dual.append(elem_dual)

        self.logger.debug("Code review evaluation result: {}".format(self.list_dual))

        return self.list_dual
