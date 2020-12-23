import numpy as np

from src.model.Community import Community
from src.model.Lang import Lang

from typing import List, Dict


class Agent:
    def __init__(self,
                 simulation,
                 community: Community,
                 languages: List[Lang] = []):
        self.simulation = simulation
        self.community: Community = community
        self.langs: List[Lang] = languages
        self.age: int = 0

        self.id = simulation.n_agents
        simulation.n_agents += 1

    def study(self) -> None:
        if np.random.random() < self.simulation.official_lang_pressure:
            self.langs.append(self.community.official_lang)

        if self.community.most_common_lang is not None and \
            self.community.most_common_lang not in self.langs:
            self.langs.append(self.community.most_common_lang)

    def get_migration_probs(self) -> Dict[Community, float]:
        langs = {
            community: list(community.langs.keys())
            for community in self.community.adj_list
        }
        langs[self.community] = list(self.community.langs.keys())

        appeals = {
            community: community.appeal
            for community in self.community.adj_list
        }
        appeals[self.community] = self.community.appeal

        common_lang_fractions: Dict[Community, float] = {
            community: len([l for l in community_langs if l in self.langs]) / len(community_langs)
            for community, community_langs in langs.items()
        }

        migration_probs = {
            community: common_lang_fraction *
            (1 if community == self.community else self.simulation.agent_mobility ** 2)
            for community, common_lang_fraction in common_lang_fractions.items()
        }

        sum_exp = np.sum(np.exp(list(migration_probs.values())))
        migration_probs = {
            community: np.exp(prob) / sum_exp
            for community, prob in migration_probs.items()
        }

        return migration_probs

    def migrate(self) -> None:
        migration_probs = self.get_migration_probs()
        communities, probs = zip(*migration_probs.items())

        self.community.remove_agent(self)
        self.community = np.random.choice(communities, p=probs)
        self.community.add_agent(self)

        lang = self.community.most_common_lang
        if lang is not None and lang not in self.langs:
            self.langs.append(lang)

    def give_birth(self) -> None:
        lang = np.random.choice(self.langs)

        self.community.agents.append(Agent(self.simulation,
                                           self.community,
                                           [lang]))

    def die(self):
        self.community.agents.remove(self)
        del self

    def make_turn(self):
        self.age += 1

        actions = {
            1: self.study,
            2: self.migrate,
            3: self.give_birth,
            4: self.die
        }

        actions[self.age]()
