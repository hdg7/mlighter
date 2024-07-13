## @package MLigther
#    Copyright 2022 Aidan Dakhama
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

from .mlEvasion import MLEvasion
import numpy as np

class MLDescriptionTransformation(MLEvasion):
    def transformationSetup(self, config):
        self.config = config

    def genVariants(self, data, oriVariant=None):
        print("Generating variants")
        print(self.config)
        original = data.copy()
        # Creates an array where the ith element contains the index of the original input
        if self.config["Type"] == "None":
            # set origin_map to be the same as the input data
            data = pd.concat([data, original.add_prefix('original_')], axis=1)

        print("=========================")
        print(data)

        return data

    def get_config(self):
        return self.config

    def get_name(self):
        return "DescriptionTransformation"