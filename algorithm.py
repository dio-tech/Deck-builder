import numpy as np
import itertools
import math

sizes = [940, 1240, 1550, 1820, 2150]
length = 5000
rows = 4

c = []
for i in range(math.ceil(length/sizes[-1]), math.ceil(length/sizes[0])):
  lst = list(itertools.combinations_with_replacement(sizes, i))
  for l in lst:
    if sum(l) > length and (sum(l) - length) < length*0.08:
      c.append(l)

from copy import copy

def generate_number():
  return np.random.randint(0, len(c))

def evaluate_waste(combination):
  total = 0
  for row in combination:
    total += (sum(row) - length)
  return total

def evaluate_waste_population(combinations):
  total = []
  for combination in combinations:
    total.append(evaluate_waste(combination))
  return total

def evaluate_population(population):
  return sum(evaluate_waste(individual) for individual in population) / len(population)
  

def select_fittest(population, n_best):
  population=sorted(population, key=evaluate_waste)
  return population[:n_best]

def generate_individuals():
  individual = []
  for i in range(rows):
    t = c[generate_number()]
    if t not in individual:
      individual.append(t)

  return individual

def generate_population(n):
  population = []
  for i in range(n):
    ind = generate_individuals()
    if ind not in population:
      population.append(ind)
  
  return population

def mutate_change(individual):
  p=len(individual)
  i1=np.random.randint(p)
  i2=(i1+np.random.randint(p-1)) % p
  individual = copy(individual)
  individual[i1], individual[i2] = individual[i2], individual[i1]
  return individual

def mutate_invert(individual):
  p=len(individual)
  i1=np.random.randint(p-2)
  i2=(np.random.randint(i1,p)) % p
  individual = copy(individual)
  gene=individual[i1:i2+1]
  individual[i1:i2]=gene[::-1]
  #print(i1,i2,gene)
  return individual

def pmx_crossover(individual1, individual2):
  size = len(individual1)

  i = np.random.randint(size - 1)
  j = np.random.randint(i + 1, size)
  
  already=set(individual1[i:j])
  remaining=[gene for gene in individual2 if gene not in already]
  final = []
  #return np.concatenate([remaining[:i], individual1[i:j], remaining[i:]])
  for k in remaining[:i]:
    final.append(k)
  for k in individual1[i:j]:
    final.append(k)
  for k in remaining[i:]:
    final.append(k)
  
  return final


def next_gen(population, n):
  size = len(population)
  best_individuals = select_fittest(population, int(size*.20) )
  mutated = [ mutate_change(individual) for individual in best_individuals ]
  
  child = []
  for i in range(size-len(best_individuals)-len(mutated)):
    i1, i2 = np.random.randint(len(best_individuals), size=2)
    child.append(pmx_crossover(best_individuals[i1],best_individuals[i2]))
  generated = generate_population(n)

  final = []
  for k in best_individuals:
    if len(k) == rows:
      final.append(k)
  for k in mutated:
    if len(k) == rows:
      final.append(k)
  for k in child:
    if len(k) == rows:
      final.append(k)
  for k in generated:
    if len(k) == rows:
      final.append(k)
  
  return final

from tqdm import tqdm

it = 50
n = 1000

population = generate_population(n)

scores = []
best = []
less_waste = []

for i in tqdm(range(it)):
  population = next_gen(population, n)
  scores.append(evaluate_population(population))
  if sorted(population, key=evaluate_waste)[0] not in sorted(best):
    best.append(sorted(population, key=evaluate_waste)[0])
    less_waste.append(sorted(evaluate_waste_population(population))[0])

print(best[0])
print(less_waste)
print(min(less_waste))
print(sum(scores)/len(scores))