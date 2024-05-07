import random
import numpy as np

class Osobnik:
    def __init__(self, params, wiek = 1, repr='płciowe'):
      self.wiek = wiek
      self.cechy_genotypu = self.losuj_genotyp(params['num_genes'])
      # płeć 0 albo 1
      self.płeć = self.losuj_płeć()
      self.repr = repr

    def losuj_genotyp(self, num_genes):
      return [random.uniform(0, 1) for i in range(num_genes)]

    def mutacja(self, mi, num_genes, efekt_mutacji):
      x = np.random.uniform(0,1)
      if x < mi:
        miejsce = random.randint(0, num_genes-1)
        efekt = random.normalvariate(0, efekt_mutacji)
        self.cechy_genotypu[miejsce] += efekt


    def reprodukuj(self, osobnik_1, params):
      dziecko = Osobnik(params)

      od_1 = random.sample(range(params['num_genes']), int(params['num_genes']/2))
      od_0 = [ele for ele in range(params['num_genes']) if ele not in od_1]
      for i in od_1:
        dziecko.cechy_genotypu[i] = osobnik_1.cechy_genotypu[i]
      for j in od_0:
        dziecko.cechy_genotypu[j] = self.cechy_genotypu[j]
      return dziecko

    def losuj_płeć(self):
      return random.randint(0,1)