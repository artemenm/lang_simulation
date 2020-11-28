from src.model.Lang import Lang

from collections import Counter, defaultdict
from typing import List, Dict


class Community:
    def __init__(self,
                 name: str,
                 appeal: int,
                 agents,
                 langs: Dict[Lang, int],
                 official_lang: Lang):
        self.name: str = name
        self.appeal: int = appeal

        from src.model.Agent import Agent
        self.agents: List[Agent] = []

        self.langs: Dict[Lang, int] = defaultdict(int)
        self.langs.update(langs)

        self.official_lang: Lang = official_lang
        self.most_common_lang: Lang = None

        self.adj_list: List = []

    def __hash__(self):
        return hash(self.name)

    def add_agent(self, agent):
        self.agents.append(agent)
        for lang in agent.langs:
            self.langs[lang] += 1

    def remove_agent(self, agent):
        self.agents.remove(agent)
        for lang in agent.langs:
            self.langs[lang] -= 1
            if self.langs[lang] == 0:
                del self.langs[lang]

    def update(self) -> None:
        langs: List[Lang] = []
        for agent in self.agents:
            langs.extend(agent.langs)

        if len(langs):
            self.most_common_lang = Counter(langs).most_common(1)[0][0]
        else:
            self.most_common_lang = None
