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
from search.genAlg import GAOptimizer
from evasions.mlEvasion import MLEvasion
import numpy as np

class MLEvasionSearch(MLEvasion):
    def ga_config(self):
        config = {
            # GA parameters
            'numgen': 200,
            'mut_prob': 0.1,
            'cross_prob': 0.8,
            'num_sel': 10,
            'mu_sel': 100,
            'lambda_sel': 100,
            'inner_mut_prob': 0.05,
            'population_size': 200,
            'tournament_sel': 7,
            'minInt' : -100000,
            'maxInt' : 100000,
            'minFloat': 0,
            'maxFloat' : 2,
            'numtuples': 1,
        }
#        config['sizetuples']=len(varNames)
#        for i,type in enumerate(varTypes):
#            config['type'+str(i)]=varTypes[i]
        config['sizetuples']=1
        config['type0']="float"
        return config


#    varNames=['x','y','z']
#    varTypes=["int","int","int"]

    def setFeatures(self,features):
        self.features=features

    #This will identify whether a feature is int, float or categorical
    def identifyFeatureType(self):
        pass

    #This attacks directly to the classifier, but does not target a
    #specific class
    def setModel(self,model):
        self.model=model


    def transformationSetup(self,config):
        if config is None:
            self.config=self.ga_config()
        else:
            self.config=config
        self.predictor=config["predictor"]
        self.setFeatures(config["features"])
        self.oriVariant=config["oriVariant"]
    #The fitness is a direct prediction of the classifier, if this is
    #totally binary, it is better to train it with some probability
    #output.
    def fitness(self,individual):
#        print(self.data.iloc[0])
#        print(len(self.data.iloc[0]))
        #print(self.data)
        compIndividual=np.zeros(len(self.data[self.oriVariant]))
#        print(individual)
#        print(compIndividual)
        self.features=np.array(self.features)
#        print(self.features)
        compIndividual[self.features==1]+=individual
#        print(compIndividual)
        compIndividual+=self.data[self.oriVariant]
#        print(self.oriVariant)
#        print(self.data.iloc[self.oriVariant])
#        print(compIndividual)
#        print(self.data)
#        print(self.predictor(self.data.head(1)+compIndividual))
#        pred=self.predictor([self.data.iloc[self.oriVariant]])
#        print(pred[0])
        pred=self.predictor([compIndividual])
        print(pred[0])
        return pred[0]

    #The populations are the variants, but we keep the best solution.
    #Data initializes the fitness.
    def genVariants(self,data):
        self.data=data
        gen= GAOptimizer(self.fitness,self.config)
        self.sol,self.pop,self.logbook=gen.optimize()
        bestIndividual=np.zeros(len(self.data[self.oriVariant]))
#        print(self.features)
#        print(self.sol[0])
        bestIndividual[self.features==1]+=self.sol[0]
        bestIndividual+=self.data[self.oriVariant]
#        print(compIndividual)
        variants=[]
        print(self.pop)
        for elem in self.pop:
            compIndividual=np.zeros(len(self.data[self.oriVariant]))
#            print(elem)
            compIndividual[self.features==1]+=elem
#            compIndividual+=self.data.iloc[self.oriVariant]
#            print(compIndividual)
            variants.append(compIndividual)
        print(variants)
#        print(self.data.iloc[self.oriVariant])
        variants=[variant+self.data[self.oriVariant] for variant in variants]
        pred=self.predictor(variants)
        print(pred)
        pred=self.predictor([self.data[self.oriVariant]])
        print(pred)
        print(variants)
        return variants

