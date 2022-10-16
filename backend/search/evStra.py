## @package Eurystheus
#  Documentation for this module.
#
#  More details.
import random
import math
import sys
import hashlib
import numpy as np
from deap import creator, base, tools, algorithms

class EvStOptimizer:

    def __init__(self,fitness,options={}):
        #GA parameters
        self.numGen = int(options['numgen'])
        self.mutProb= float(options['mut_prob'])
        self.crossProb=float(options['cross_prob'])
        self.numSel=int(options['num_sel'])
        self.muSel=int(options['mu_sel'])
        self.lambdaSel=int(options['lambda_sel'])
        self.innerMutProb=float(options['inner_mut_prob'])
        self.populationSize=int(options['population_size'])
        self.tournamentSel=int(options['tournament_sel'])
        #Individual Initialization parameters
        self.tsize = int(options['sizetuples'])
        self.isize = int(options['numtuples'])
        self.types = list(options["type"+str(i)] for i in range(self.tsize))
        self.minInt = int(options['minInt'])
        self.maxInt = int(options['maxInt'])
        self.minFloat= float(0)
        self.maxFloat= float(options['noise'])
        self.fitness=fitness
        self.weights=options["weights"]
        ## Documentation for randomInit
        # @param icls individual composed by tuples
        # @param low vector for minimum values for each element of a tuple
        # @param top vector for maximum values of the tuples
        # @param size individual size
        # @brief this function initializes an individual
    def generateES(self,icls, scls):
        ind = icls(random.random() if self.types[index%self.tsize]=='float' else random.randint(self.minInt,self.maxInt) for index in range(self.isize*self.tsize))
        ind.strategy = scls(random.random() if self.types[index%self.tsize]=='float' else random.randint(self.minInt,self.maxInt) for index in range(self.isize*self.tsize))
        #ind.strategy = scls(random.uniform(smin, smax) for _ in range(size))
        return ind


    ## Documentation for evalFitness
    # @param individual individual composed by tuples
    # @brief this function fakes an individual fitness
    def evalFitness(self,individual):
        #inputs=[individual[x:x+self.tsize] for x in range(0,len(individual),self.tsize)]
        return self.fitness(individual)

#    def fitness(self,inputs):
#        return 1
    def checkStrategy(self,minstrategy):
        def decorator(func):
            def wrappper(*args, **kargs):
                children = func(*args, **kargs)
                for child in children:
                    for i, s in enumerate(child.strategy):
                        if s < minstrategy:
                            child.strategy[i] = minstrategy
                return children
            return wrappper
        return decorator
    
    def optimize(self):
#        creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0,-1.0))
#        creator.create("FitnessMin", base.Fitness, weights=self.weights)
#        creator.create("Individual", list, fitness=creator.FitnessMin)
#        toolbox = base.Toolbox()
#        toolbox.register("individual", self.randomInit, creator.Individual)
#        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#        toolbox.register("evaluate", self.evalFitness)
#        toolbox.register("mate", tools.cxTwoPoint)
#        toolbox.register("mutate", self.mutUniform)
#        toolbox.register("select", tools.selTournament,tournsize=self.tournamentSel)
        #toolbox.register("elitism", tools.selBest, k=numSel)
#        population = toolbox.population(n=self.populationSize)
        # The genetic algorithm, this implementation ia mu+lambda
        # it is feeded with a population of individuals, a mutation
        # and crossover probabilities and a number of generations
#        offspring = algorithms.eaMuCommaLambda(population, toolbox,mu=self.muSel,lambda_=self.lambdaSel,cxpb=self.crossProb, mutpb=self.mutProb,ngen=self.numGen)
        # the top ten individuals are printed
        #topTen = tools.selBest(population, k=10)
        #print(topTen)
#        best = tools.selBest(population, k=1)
#        return best[0],offspring

    
        creator.create("FitnessMin", base.Fitness, weights=self.weights)
        creator.create("Individual", list, fitness=creator.FitnessMin)
        creator.create("Strategy", list)
        toolbox = base.Toolbox()
        toolbox.register("individual", self.generateES, creator.Individual,creator.Strategy)
#        ,                 IND_SIZE, MIN_VALUE, MAX_VALUE, MIN_STRATEGY, MAX_STRATEGY)
#        toolbox.register("mate", tools.cxESBlend, alpha=0.1)
        toolbox.register("mutate", tools.mutESLogNormal, c=1.0, indpb=0.03)
        toolbox.register("evaluate", self.evalFitness)
#        toolbox.decorate("mate", checkStrategy(MIN_STRATEGY))
        toolbox.decorate("mutate", self.checkStrategy(self.minFloat))
        
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("select", tools.selBest)
        population = toolbox.population(n=self.populationSize)
        # The genetic algorithm, this implementation ia mu+lambda
        # it is feeded with a population of individuals, a mutation
        # and crossover probabilities and a number of generations
        offspring,logbook = algorithms.eaMuCommaLambda(population, toolbox,mu=self.muSel,lambda_=self.lambdaSel,cxpb=0, mutpb=self.mutProb,ngen=self.numGen)



def fitness(nothing):
    return (1,1,1,)

def config():
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
        'minStra' : 0,
        'maxStra' : 1,
    }
    #        config['sizetuples']=len(varNames)
    #        for i,type in enumerate(varTypes):
    #            config['type'+str(i)]=varTypes[i]
    config['sizetuples']=1
    config['type0']="float"
    #Remove
    config["numtuples"]=4
    config["noise"]=1
    config["features"]=[1,1,1,1]
    #config["predictor"]=session.prediction_proba
    config["oriVariant"]=1
    config["weights"]=(-1.0,1.0,1.0)
    return config

def main():
    
    evStrategy=EvStOptimizer(fitness,options=config())
#    MU, LAMBDA = 10, 100
#    pop = toolbox.population(n=MU)
#    stats = tools.Statistics(lambda ind: ind.fitness.values)
#    stats.register("avg", numpy.mean)
#    stats.register("std", numpy.std)
#    stats.register("min", numpy.min)
#    stats.register("max", numpy.max)
    evStrategy.optimize()
#    pop, logbook = algorithms.eaMuCommaLambda(pop, toolbox, mu=MU, lambda_=LAMBDA,  mutpb=0.3, ngen=500, stats=stats)
#    print(pop)
    #return pop, logbook

main()
