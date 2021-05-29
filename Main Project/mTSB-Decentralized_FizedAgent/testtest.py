import numpy as np
"""
import ray
ray.init()

@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0
    def increment(self):
        self.n += 1
    def read(self):
        return self.n

counters = [Counter.remote() for i in range(4)]
[c.increment.remote() for c in counters]
futures = [c.read.remote() for c in counters]
print(ray.get(futures))
"""


list1 = [20]

print(int(list1))

if any(isinstance(l, list) for l in pop):

    rankedFitness = [rankRoutes(pops, home_city) for pops in pop]
    print(rankedFitness)

    best_pop_id = [rankedFitness[pop_id][0][1] for pop_id, _ in enumerate(rankedFitness)]
    best_pop_id = np.argmax(best_pop_id)
    print(best_pop_id)

    rankedFitness = rankedFitness[best_pop_id]
    pop = pop[best_pop_id]

else:
    rankedFitness = rankRoutes(pop, home_city)