from src.components import *
from src.utils      import *

class Simulation:
    def __init__(self, sim_len: int, init_agents: list, agent_death_pr: float, replicate: callable):
        assert(len(init_agents) % 2 == 0) 

        self.sim_len = sim_len
        self.all_agents = init_agents
        self.agent_death_pr = agent_death_pr

        self.replicate = lambda P: replicate(P, self.agent_death_pr)

        self.no_agents = len(self.all_agents)

    def __init_pairings(self):
        pairing_indeces = get_random_subsets(self.no_agents) # default subset size is 2
        self.cur_pairings = []
        for idx in pairing_indeces:
            pair_list = [self.all_agents[idx[0]], self.all_agents[idx[1]]]
            pairing = Pairing(pair_list, self.replicate)
            self.cur_pairings.append(pairing)

    def __init_replication(self):
        for p in self.cur_pairings:
            offspring = p.get_offspring()
            if offspring != None:
                self.all_agents.append(offspring)

    def __init_survival_stage(self):
        for agent in self.all_agents:
            agent.live_one_day()
            if not agent.alive:
                self.all_agents.remove(agent)
        self.no_agents = len(self.all_agents)

    def __advance_sim(self):
        self.__init_pairings()
        self.__init_replication()
        self.__init_survival_stage()

    def run(self):
        for _ in range(self.sim_len):
            # print(self.no_agents)
            self.__advance_sim()