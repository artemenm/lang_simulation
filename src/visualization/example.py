import sys
sys.path.append('.')

from src.model.Simulation import Simulation
from src.model.Lang import Lang
from src.model.Community import Community
from src.model.Agent import Agent

from itertools import chain
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm


df_langs = pd.read_excel('src/visualization/languages.xlsx')
df_communities = pd.read_excel('src/visualization/communities.xlsx')
df_adj_communities = pd.read_excel('src/visualization/adj_communities.xlsx')

s = Simulation(agent_mobility=0.1, official_lang_pressure=0.5)
langs = {
    Lang(name, bool(is_official)): 0
    for i, (name, is_official) in df_langs.iterrows()
}

communities = {}
for i, (name, appeal, official_lang, x, y, pop, a_prob, b_prob) in df_communities.iterrows():
    communities[name] = Community(s, name, appeal, [], langs, official_lang)
for i, (c_from, c_to) in df_adj_communities.iterrows():
    communities[c_from].adj_list.append(communities[c_to])
    communities[c_to].adj_list.append(communities[c_from])
s.communities = list(communities.values())

for i, (name, appeal, official_lang, x, y, pop, a_prob, b_prob) in df_communities.iterrows():
    for _ in range(pop):
        agent_langs = []
        if np.random.random() < a_prob:
            agent_langs.append(list(langs.keys())[0])
        if np.random.random() < b_prob:
            agent_langs.append(list(langs.keys())[1])
        if agent_langs == []:
            agent_langs.append(np.random.choice(list(langs.keys())))

        c_i = [c.name for c in s.communities].index(name)
        s.communities[c_i].add_agent(Agent(s, s.communities[c_i], agent_langs))

##############

columns = ['age', 'community', 'turn'] + [l.name for l in langs]

dfs = []
for turn_n in tqdm(range(200)):
    agents = {c.name: [a.id for a in c.agents] for c in s.communities}
    agent_ids = list(chain(*agents.values()))
    turn_df = pd.DataFrame(index=agent_ids, columns=columns)
    turn_df.index.name = 'agent_id'
    for c in s.communities:
        for a in c.agents:
            agent_dict = {
                'age': a.age,
                'community': c.name,
                'turn': turn_n
            }
            for l in langs:
                #print(a.langs)
                agent_dict[l.name] = int(l in a.langs or l.name in a.langs)
            turn_df.loc[a.id] = agent_dict
    dfs.append(turn_df)
    s.make_turn()

df = pd.concat(dfs).reset_index()
df.to_csv('src/visualization/result.csv')

##############

turns = sorted(df.turn.unique())
a_counts, b_counts = [], []
for turn in turns:
    a_counts.append(df[df.turn == turn]['a'].sum())
    b_counts.append(df[df.turn == turn]['b'].sum())

plt.plot(turns[5:], a_counts[5:])
plt.plot(turns[5:], b_counts[5:])
plt.show()