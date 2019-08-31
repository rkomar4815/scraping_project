import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools


def gen_viz(filename):

    df = pd.read_csv(filename)

    key_value_tuples = []

    for index, row in df.iterrows():
        combos = itertools.combinations([row['TITLE'],
                                         row['Commercial Registered Agent'],
                                         row['Owner Name'],
                                         row['Registered Agent']], 2)

        for x in combos:

            pair = list(x)

            if str(pair[0]) != 'nan' and str(pair[-1]) != 'nan':
                key_value_tuples.append(tuple(pair))

    graph = nx.from_edgelist(key_value_tuples)

    nx.draw_networkx(graph, with_labels=False, node_size=25)
    plt.show()


if __name__ == "__main__":

    gen_viz('result.csv')
