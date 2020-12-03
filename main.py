import pandas as pd

from Social_Graphs import graph_generator
from Social_Graphs import wordclouds
from Social_Graphs import decomposition

if __name__ == "__main__":
    # load data from csv
    Data = pd.read_csv('./data/Data.csv')

    G = graph_generator.directed_graph(Data)

    GCC = graph_generator.giant_connected_component(G)

    # in and out degree
    in_deg, out_deg = graph_generator.in_out_deg(G)

    # in and out degree distribution
    graph_generator.distribution_graph(GCC, 'In')
    graph_generator.distribution_graph(GCC, 'Out')

    # Convert to undirected graph
    GU = GCC.to_undirected()

    # force atlas
    graph_generator.forceatlas_graph(GU)

    # core decomposition
    decomposition.decomposition_republican(GU, core=True)
    decomposition.decomposition_democrat(GU, core=True)

    # truss decomposition
    decomposition.decomposition_republican(GU, truss=True)
    decomposition.decomposition_democrat(GU, truss=True)

    # word cloud generator
    wordclouds.wordclouds(Data)
