#Evolutionary Strategy

import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

IND_SIZE = 30
MIN_VALUE = 4
MAX_VALUE = 5
MIN_STRATEGY = 0.5
MAX_STRATEGY = 3

class EVStrategy:

    def __init__(self,fitness,options={}):
        #EvStra Parameters 
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
        self.minFloat= float(options['minFloat'])
        self.maxFloat= float(options['maxFloat'])
        self.fitness=fitness
        #The rest of the parameters
        random.seed()
        self.hof = tools.HallOfFame(1)
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

    def evalFitness(self,individual):
        return self.fitness(individual)
    
    # Individual generator
    def generateES(self,icls, scls, size, imin, imax, smin, smax):
        ind = icls(random.uniform(imin, imax) for _ in range(size))
        ind.strategy = scls(random.uniform(smin, smax) for _ in range(size))
        return ind

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
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode="d", fitness=creator.FitnessMin, strategy=None)
        creator.create("Strategy", array.array, typecode="d")
        toolbox = base.Toolbox()
        toolbox.register("individual", self.generateES, creator.Individual, creator.Strategy, IND_SIZE, MIN_VALUE, MAX_VALUE, MIN_STRATEGY, MAX_STRATEGY)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxESBlend, alpha=0.1)
        toolbox.register("mutate", tools.mutESLogNormal, c=1.0, indpb=0.03)
        toolbox.register("select", tools.selTournament, tournsize=self.tournamentSel)
        toolbox.register("evaluate", self.evalFitness)
        toolbox.decorate("mate", self.checkStrategy(MIN_STRATEGY))
        toolbox.decorate("mutate", self.checkStrategy(MIN_STRATEGY))
        self.pop = toolbox.population(n=self.muSel)
        pop, logbook = algorithms.eaMuCommaLambda(self.pop, toolbox, mu=self.muSel, lambda_=self.lambdaSel, cxpb=self.crossProb, mutpb=self.mutProb, ngen=self.numGen, stats=self.stats, halloffame=self.hof)
        return pop, logbook, self.hof

def ga_config():
    config = {
        # GA parameters
        'numgen': 120,
        'mut_prob': 0.1,
        'cross_prob': 0.8,
        'num_sel': 10,
        'mu_sel': 300,
        'lambda_sel': 300,
        'inner_mut_prob': 0.05,
        'population_size': 300,
        'tournament_sel': 7,
        'minInt' : -100000,
        'maxInt' : 100000,
        'minFloat': -100000.0,
        'maxFloat' : 100000.0,
        'numtuples': 1,
    }
    config['sizetuples']=1
    config['type'+"0"]=["int"]
    return config


def main():
    fitness= benchmarks.sphere
    gen= EVStrategy(fitness,ga_config())
    gen.optimize()

main()
