import random

CROSSOVER_PROBIBILITY = 0.3
CARRY_PERCENTAGE = 0.2
POPULATION_SIZE = 100
FOUND = 100

class EquationBuilder:
    
    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber

        # Create the earliest population at the begining
        self.population = self.makeFirstPopulation()
        
    def makeFirstPopulation(self):
        pass
        #TODO create random chromosomes to build the early population, and return it
    
    def findEquation(self):
        # Create a new generation of chromosomes, and make it better in every iteration
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            for i in range(POPULATION_SIZE):
                fitness = self.calcFitness(self.population[i])
                if fitness == FOUND:
                    return self.population[i]
                fitnesses.append(fitness)
                
                #TODO calculate the fitness of each chromosome
                #TODO return chromosome if a solution is found, else save the fitness in an array

            #TODO find the best chromosomes based on their fitnesses, and carry them directly to the next generation (optional)
            carriedChromosomes = []
            for i in range(0, int(POPULATION_SIZE*CARRY_PERCENTAGE)):
                carriedChromosomes.append(bestChromosome[i]) 

            # A pool consisting of potential candidates for mating (crossover and mutation)    
            matingPool = self.createMatingPool()

            # The pool consisting of chromosomes after crossover
            crossoverPool = self.createCrossoverPool(matingPool)

            # Delete the previous population
            self.population.clear()

            # Create the portion of population that is undergone crossover and mutation
            for i in range(POPULATION_SIZE - int(POPULATION_SIZE*CARRY_PERCENTAGE)):
                self.population.append(self.mutate(crossoverPool[i]))
                
            # Add the prominent chromosomes directly to next generation
            self.population.extend(carriedChromosomes)
    
    def createMatingPool(self):
        matingPool = 12
        #TODO make a brand new custom pool to accentuate prominent chromosomes (optional)
        #TODO create the matingPool using custom pool created in the last step and return it
        return matingPool
    
    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        for i in range(len(matingPool)):
            if random.random() > CROSSOVER_PROBIBILITY:
                pass
                #TODO don't perform crossover and add the chromosomes to the next generation directly to crossoverPool
            else:
                pass
                #TODO find 2 child chromosomes, crossover, and add the result to crossoverPool
        return crossoverPool
    
    def mutate(self, chromosome):
        #TODO mutate the input chromosome 
        return chromosome

    def calcFitness(self, chromosome):
        pass
        #TODO define the fitness measure here


operands = [1, 2, 3, 4, 5, 6, 7, 8]
operators = ['+', '-', '*']
equationLength = 21
goalNumber = 18019

equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)
equation = equationBuilder.findEquation()
print(equation)