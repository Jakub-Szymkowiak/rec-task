from src.utils import *

from numpy.random import uniform

class Agent:
    def __init__(self, color: Color, death_pr: float, is_mutant: bool=None):
        assert(0 <= death_pr <= 1) # 0 <= Pr(X) <= 1

        self.alive = True
        self.color = color
        self.death_pr = death_pr
        self.days_alive = 0
        self.offspring_count = 0
        self.is_mutant = is_mutant

    def live_one_day(self):
        if uniform(0,1) < self.death_pr:
            self.alive = False
        else:
            self.days_alive = self.days_alive + 1

    def increment_offspring_count(self):
        self.offspring_count = self.offspring_count + 1

class Pairing:
    def __init__(self, agents: list, replicate: callable):
        assert(len(agents) == 2)

        self.agents = agents
        self.replicate = replicate

    def compare_colors(self):
        c1 = self.agents[0].color
        c2 = self.agents[1].color
        return ColorUtils.compare_colors(c1, c2)

    def get_similarity_score(self):
        c1 = self.agents[0].color
        c2 = self.agents[1].color
        return ColorUtils.normalized_sRGB(c1, c2)

    def get_color_avg(self):
        c1 = self.agents[0].color
        c2 = self.agents[1].color
        return ColorUtils.get_color_avg(c1, c2)

    def get_offspring(self):
        offspring = self.replicate(self)
        if offspring != None:
            self.agents[0].increment_offspring_count()
            self.agents[1].increment_offspring_count()
        return offspring