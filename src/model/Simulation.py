from src.model.Agent import Agent
from src.model.Community import Community

from typing import List


class Simulation:
    def __init__(self,
                 agent_mobility: float,
                 official_lang_pressure: float):
        self.agent_mobility: float = agent_mobility
        self.official_lang_pressure: float = official_lang_pressure

        self.communities: List[Community] = []
        self.agents: List[Agent] = []
        self.n_agents: int = 0

    def make_turn(self) -> None:
        for community in self.communities:
            for agent in community.agents:
                agent.make_turn()

        for community in self.communities:
            community.update()
