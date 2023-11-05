from math import sqrt
import random

# Genetic Algorithm Parameters
population_size = 100
num_generations = 2000
mutation_rate = 0.1

# Get polynomial degree and range of coefficients:
# n = int(input()) #TODO uncomment
n=4
print("Polynomial degree: ",n)
# lowerLimit, upperLimit = [int(x) for x in input().split()] #TODO uncomment
lowerLimit, upperLimit = -20 ,20
print("Range of coefficients: (%d, %d)"%(lowerLimit,upperLimit))

# Get dataset
samplePoints = [(0, 1), (1, 0), (2, -5), (-1, -8) , (5,16)]
# while True: #TODO uncomment
#     point = tuple(int(x) for x in input().split())
#     if len(point) < 2:
#         break
#     samplePoints.append(point)
print("Sample points: ", samplePoints)

def calcTarget(x: int, coefficients: tuple[int]):
    result = 0
    for i in range(len(coefficients)):
        result += coefficients[i] * (x ** i)
    return result

def fitnessFunction(coefficients: tuple[int]):
    result = 0
    for x,y in samplePoints:
        result += (y - calcTarget(x, coefficients))**2
    return result/ len(samplePoints)

def crossoverFunction(parent1: tuple[int], parent2: tuple[int]):
    return [random.choice([parent1[i], parent2[i]]) for i in range(n)]  # Crossover

def findBestSolution(chromosomes:list[list[int]]):
    _population_size=population_size
    for genNum in range(num_generations):
        fitness_scores = [fitnessFunction(coefficients) for coefficients in chromosomes]
        if 0 in fitness_scores:
            index= fitness_scores.index(0)
            print('',_,' ) index= ',index,', ch= ',chromosomes[index])
            return chromosomes[index]
        weights=[int(1+(100 / score)) for score in fitness_scores]
        # print('weight: ',weights)
        selected_parents = random.choices(chromosomes, weights=weights, k=_population_size)
        # print("fitness_scores: ",int(sum(fitness_scores)))
        offspring = []
        for _ in range(_population_size):
            parent1, parent2 = random.sample(selected_parents, 2)
            child = crossoverFunction(parent1,parent2)  # Crossover
            for chromosomeIndex in range(n):
                if random.random() < mutation_rate:
                    randomNumber = random.randint(lowerLimit, upperLimit)  # Mutation
                    # randomIndex=random.randint(0, len(child)-1)
                    child[chromosomeIndex]=randomNumber
            offspring.append(child)
        chromosomes = offspring
        
        # Increase population size:
        _population_size += int(0.2*_population_size)
        
        best_solution = min(chromosomes, key=lambda coefficients: fitnessFunction(coefficients))
        print(f"{genNum}) best solution is {best_solution}")
    return best_solution

chromosomes = [[random.randint(lowerLimit, upperLimit) for _ in range(n)] for _ in range(population_size)]
best_solution=findBestSolution(chromosomes=chromosomes)
print(fitnessFunction(best_solution))
print(f"Fitted Polynomial: y = {best_solution[0]} +",' + '.join([f'{best_solution[i]} x^{i}' for i in range(1,len(best_solution))]).replace('+ -','- '))
