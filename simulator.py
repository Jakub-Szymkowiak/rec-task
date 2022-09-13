from src.simulation  import *
from src.components  import *
from src.replication import *
from src.utils       import *

import numpy as np

class Experiment:
    def __get_init_agents(death_pr: float, red: int=5, blue: int=5):
        red_agents = [Agent(ColorUtils.RED, death_pr) for _ in range(red)]
        blue_agents = [Agent(ColorUtils.BLUE, death_pr) for _ in range(blue)]
        return red_agents + blue_agents

    def __run_sim(death_pr: float, simulation_len: int, no_iters: int, replicate: callable):
        results = []
        for _ in range(no_iters):
            init_agents = Experiment.__get_init_agents(death_pr)
            sim = Simulation(simulation_len, init_agents, death_pr, replicate)
            sim.run()
            results.append(sim.all_agents)

        return results

    def RunA(replication_pr: float, death_pr: float=.1, simulation_len: int=100, no_iters: int=1):
        replicate = RepMethods.RandRep(replication_pr)
        return Experiment.__run_sim(death_pr, simulation_len, no_iters, replicate)

    def RunB(replication_pr: float, death_pr: float=.1, simulation_len: int=100, no_iters: int=1):
        replicate = RepMethods.RandRepSameColor(replication_pr)
        return Experiment.__run_sim(death_pr, simulation_len, no_iters, replicate)

    def RunC(similarity_th: float, death_pr: float=.1, mutat_app_pr: float=.15, simulation_len: int=100, no_iters: int=1):
        replicate = RepMethods.AvgColorRep(similarity_th, mutat_app_pr)
        return Experiment.__run_sim(death_pr, simulation_len, no_iters, replicate)

class GridExpMean:
    def __GridRun(exp: callable, par_a: np.ndarray, par_b: np.ndarray):
        shape = [len(par_a), len(par_b)]
        res_grid = np.empty(shape)

        for i, p_a in enumerate(par_a):
            for j, p_b in enumerate(par_b):
                result = exp(p_a, p_b)
                pop_size = [len(pop) for pop in result]
                res_grid[i][j] = np.mean(pop_size)

        return res_grid

    def RunA(replication_pr: np.ndarray, death_pr: np.ndarray, no_iters: int):
        exp = lambda rpr, dpr: Experiment.RunA(rpr, dpr, no_iters=no_iters)
        return GridExpMean.__GridRun(exp, replication_pr, death_pr)

    def RunB(replication_pr: np.ndarray, death_pr: np.ndarray, no_iters: int):
        exp = lambda rpr, dpr: Experiment.RunB(rpr, dpr, no_iters=no_iters)
        return GridExpMean.__GridRun(exp, replication_pr, death_pr)

    def RunC(similarity_th: np.ndarray, death_pr: np.ndarray, no_iters: int):
        exp = lambda sth, dpr: Experiment.RunC(sth, dpr, no_iters=no_iters)
        return GridExpMean.__GridRun(exp, similarity_th, death_pr)