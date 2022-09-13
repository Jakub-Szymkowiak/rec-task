from src.components import *
from src.utils      import *

from numpy.random import uniform

class RepMethods:
    def RandRep(replication_pr: float):
        assert(0 <= replication_pr <= 1)

        def replicate(P: Pairing, death_pr: float):
            offspring = None
            if uniform(0,1) < replication_pr:
                offspring_color = ColorUtils.get_random_color()
                offspring = Agent(offspring_color, death_pr)
            return offspring
            
        return replicate

    def RandRepSameColor(replication_pr: float):
        assert(0 <= replication_pr <= 1)

        def replicate(P: Pairing, death_pr: float):
            offspring = None
            if uniform(0,1) < replication_pr and P.compare_colors():
                offspring_color = ColorUtils.get_random_color()
                offspring = Agent(offspring_color, death_pr)
            return offspring

        return replicate

    def AvgColorRep(similarity_th: float, mutant_app_pr: float):
        assert(0 <= similarity_th <= 1)
        assert(0 <= mutant_app_pr <= 1)

        def replicate(P: Pairing, death_pr: float):
            offspring = None
            if P.get_similarity_score() < similarity_th:
                if uniform(0,1) < mutant_app_pr:
                    offspring_color = ColorUtils.get_random_color()
                    is_mutant = True
                else:
                    offspring_color = P.get_color_avg()
                    is_mutant = False
                offspring = Agent(offspring_color, death_pr, is_mutant)
            return offspring

        return replicate
