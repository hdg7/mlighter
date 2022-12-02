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
import math
import sys
import hashlib
from .genAlg import GAOptimizer
from deap import creator, base, tools, algorithms

#Optimizer parameters
#numTuples = int(ConfigSectionMap("Optimizer")['numtuples'])

class GAOptimizerMul(GAOptimizer):
        
    def evalFitness(self,individual):
        return self.fitness(individual)

    #    def fitness(self,inputs):
    #        return 1
    def spea2(self,pop,toolbox,num_gens=100,sel_factor_pop=80,sel_factor_arch=40,mut_prob=0.06):
        archive = []
        curr_gen = 1

        while curr_gen <= num_gens:
            print(curr_gen)
            # Step 2 Fitness assignement
            for ind in pop:
                ind.fitness.values = toolbox.evaluate(ind)

#            for ind in archive:
#                ind.fitness.values = toolbox.evaluate(ind)

            # Step 3 Environmental selection
            archive  = toolbox.select(pop + archive, k=sel_factor_arch)

            # Step 4 Termination
            if curr_gen >= num_gens:
                return archive

            # Step 5 Mating Selection
            mating_pool = toolbox.selectTournament(archive, k=sel_factor_pop)
            offspring_pool = list(map(toolbox.clone, mating_pool))

            # Step 6 Variation
            # crossover 100% and mutation 6%
            for child1, child2 in zip(offspring_pool[::2], offspring_pool[1::2]):
                toolbox.mate(child1, child2)
            for mutant in offspring_pool:
                if random.random() < mut_prob:
                    toolbox.mutate(mutant)
            pop = offspring_pool
            curr_gen += 1

    def spea2Rand(self,pop,toolbox,num_gens=100,sel_factor_pop=80,sel_factor_arch=40,mut_prob=0.06):
        archive = []
        curr_gen = 1

        while curr_gen <= num_gens:
            print(curr_gen)
            # Step 2 Fitness assignement
            for ind in pop:
                ind.fitness.values = toolbox.evaluate(ind)
            for ind in archive:
                ind.fitness.values = toolbox.evaluate(ind)
            # Step 3 Environmental selection
            archive  = toolbox.select(pop + archive, k=sel_factor_arch)
            # Step 4 Termination
            if curr_gen >= num_gens:
                return archive
            population = toolbox.population(n=self.populationSize)
            curr_gen += 1

            
    def optimize(self):
        self.objectives=2
        weights=tuple(1.0 for i in range(self.objectives))
        creator.create("FitnessMax", base.Fitness, weights=weights)
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("individual", self.randomInit, creator.Individual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evalFitness)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", self.mutUniform)
        toolbox.register("select", tools.selSPEA2)
        toolbox.register("selectTournament", tools.selTournament,tournsize=self.tournamentSel)
        #toolbox.register("elitism", tools.selBest, k=numSel)
        population = toolbox.population(n=self.populationSize)
        # The genetic algorithm, this implementation ia mu+lambda
        # it is feeded with a population of individuals, a mutation
        # and crossover probabilities and a number of generations
        final_set = self.spea2(pop=population,toolbox=toolbox,num_gens=self.numGen,sel_factor_pop=80,sel_factor_arch=40,mut_prob=self.mutProb)
        # the top ten individuals are printed
        #topTen = tools.selBest(population, k=10)
        #print(topTen)
        with open('pareto', 'w') as f:
            for ind in final_set:
                f.write("%s %s\n" % (str(ind.fitness.values[0]), str(ind.fitness.values[1])))
        return(final_set)

    def greedy(self):
        self.objectives=2
        weights=tuple(1.0 for i in range(self.objectives))
        creator.create("FitnessMax", base.Fitness, weights=weights)
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("individual", self.randomInit, creator.Individual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evalFitness)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", self.mutUniform)
        toolbox.register("select", tools.selSPEA2)
        toolbox.register("selectTournament", tools.selTournament,tournsize=self.tournamentSel)
        #toolbox.register("elitism", tools.selBest, k=numSel)
        population = toolbox.population(n=self.populationSize)

        final_set = self.spea2Rand(pop=population,toolbox=toolbox,num_gens=self.numGen,sel_factor_pop=80,sel_factor_arch=40,mut_prob=self.mutProb)
        # the top ten individuals are printed
        #topTen = tools.selBest(population, k=10)
        #print(topTen)
        with open('paretoGreedy', 'w') as f:
            for ind in final_set:
                print(ind)
                f.write("%s %s\n" % (str(ind.fitness.values[0]), str(ind.fitness.values[1])))
        return(final_set)
        
