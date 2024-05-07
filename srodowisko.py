import math
import random
from osobnik import Osobnik

class Srodowisko:
    def __init__(self, params):
      self.populacja = self.zainicjuj_populację(params)
      self.optimum = self.zainicjuj_opt(params['num_genes'])
      self.max_pop = params['max_population']

    def get_optimum(self):
      return self.optimum

    def zainicjuj_populację(self, params):
      populacja = []
      for i in range(params['init_population']):
        populacja.append(Osobnik(params))
      return populacja

    def zainicjuj_opt(self, num_genes):
      return [random.uniform(0,1) for i in range(num_genes)]

    def zmiana_srodowiska(self, parametr_c):
        for i in range(len(self.optimum)):
            self.optimum[i] += parametr_c
        return self.optimum

    def oblicz_fitness(self, cechy_genotypu, sigma):
        norm = math.sqrt(sum((x - y)**2 for x, y in zip(cechy_genotypu, self.optimum)))
        return math.exp(-norm / (2 * sigma**2))
    
    def katastrofa(self, warm_scale):
      # zabij losowe 50% populacji + zmień optimum
      num_to_delete = int(len(self.populacja) * 0.5)
      indices_to_delete = random.sample(range(len(self.populacja)), num_to_delete)
      indices_to_delete.sort(reverse=True)
      for idx in indices_to_delete:
        del self.populacja[idx]

      new_opt = []
      for i in range(len(self.optimum)):
        new_opt.append(self.optimum[i] + random.uniform(-warm_scale*3, warm_scale*3))
        if new_opt[i]<0: new_opt[i] = 0

      self.optimum = new_opt
           