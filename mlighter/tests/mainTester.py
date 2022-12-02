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
import sched,time
import os

sys.path.append(os.environ["MLIGHTER_HOME"])
from MLighter import MLighter

s = sched.scheduler(time.time, time.sleep)
#import os
session = MLighter()
def do_something(sc,session):
    try:
        state=session.retrieveTestingState()
        if(not state is None):
            print(state)
    except:
        print("Waiting for the tester to be ready\n")
    sc.enter(1, 1, do_something, (sc,session))      
#sys.path.append(os.environ["EURY_HOME"])

session.uploadCodeTemplate(language="python",fileName="/home/hector/mlighter/test/example/sklearnLogRegTest.py")
session.uploadCodeInput(fileName="/home/hector/mltest/pythonTest/inputLogReg/inputLogReg.bin.npy")
session.runCodeTesting()
s.enter(1, 1, do_something, (s,session,))
s.run()

print("done")
