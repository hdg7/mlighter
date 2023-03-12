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
import random

# import math
# import sys
# import hashlib
import numpy as np
from deap import creator, base, tools, algorithms

# Optimizer parameters
# numTuples = int(ConfigSectionMap("Optimizer")['numtuples'])


class GAOptimizer:
    def __init__(self, fitness, options={}):
        # GA parameters
        self.numGen = int(options["numgen"])
        self.mutProb = float(options["mut_prob"])
        self.crossProb = float(options["cross_prob"])
        self.numSel = int(options["num_sel"])
        self.muSel = int(options["mu_sel"])
        self.lambdaSel = int(options["lambda_sel"])
        self.innerMutProb = float(options["inner_mut_prob"])
        self.populationSize = int(options["population_size"])
        self.tournamentSel = int(options["tournament_sel"])
        # Individual Initialization parameters
        self.tsize = int(options["sizetuples"])
        self.isize = int(options["numtuples"])
        self.types = list(options["type" + str(i)] for i in range(self.tsize))
        self.minInt = int(options["minInt"])
        self.maxInt = int(options["maxInt"])
        self.minFloat = float(0)
        self.maxFloat = float(options["noise"])
        self.fitness = fitness
        self.weights = options["weights"]
        ## Documentation for randomInit
        # @param icls individual composed by tuples
        # @param low vector for minimum values for each element of a tuple
        # @param top vector for maximum values of the tuples
        # @param size individual size
        # @brief this function initializes an individual

    def randomInit(self, icls):
        # TODO: Arreglar random del float random
        ind = icls(
            random.random()
            if self.types[index % self.tsize] == "float"
            else random.randint(self.minInt, self.maxInt)
            for index in range(self.isize * self.tsize)
        )
        #        ind[0]=0
        return ind

    ## Documentation for randomInit
    # @param icls individual composed by tuples
    # @param low vector for minimum values for each element of a tuple
    # @param top vector for maximum values of the tuples
    # @param size individual size
    # @brief this function initializes an individual
    def mutUniform(self, individual):
        ind2 = individual
        for index, elem in enumerate(individual):
            if random.random() < self.innerMutProb:
                # TODO:Rango para los float
                ind2[index] = (
                    random.random()
                    if self.types[index % self.tsize] == "float"
                    else random.randint(self.minInt, self.maxInt)
                )
        return (ind2,)

    ## Documentation for evalFitness
    # @param individual individual composed by tuples
    # @brief this function fakes an individual fitness
    def evalFitness(self, individual):
        # inputs=[individual[x:x+self.tsize] for x in range(0,len(individual),self.tsize)]
        return self.fitness(individual)

    #    def fitness(self,inputs):
    #        return 1

    def optimize(self):
        #        creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0,-1.0))
        creator.create("FitnessMin", base.Fitness, weights=self.weights)
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()
        toolbox.register("individual", self.randomInit, creator.Individual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evalFitness)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", self.mutUniform)
        toolbox.register("select", tools.selTournament, tournsize=self.tournamentSel)
        # The statistics for the logbook
        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)
        # toolbox.register("elitism", tools.selBest, k=numSel)
        population = toolbox.population(n=self.populationSize)
        # The genetic algorithm, this implementation ia mu+lambda
        # it is feeded with a population of individuals, a mutation
        # and crossover probabilities and a number of generations
        offspring, logbook = algorithms.eaMuCommaLambda(
            population,
            toolbox,
            mu=self.muSel,
            lambda_=self.lambdaSel,
            cxpb=self.crossProb,
            mutpb=self.mutProb,
            ngen=self.numGen,
            stats=stats,
        )
        # the top ten individuals are printed
        # topTen = tools.selBest(population, k=10)
        # print(topTen)
        best = tools.selBest(population, k=1)
        return best[0], offspring, logbook
