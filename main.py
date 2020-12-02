import pandas as pd

from Social_Graphs import graph_generator
from Social_Graphs import wordclouds
from Social_Graphs import core_decomposition

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
    core_decomposition.core_decomposition_republican(GU)
    core_decomposition.core_decomposition_democrat(GU)

    # word cloud generator
    wordclouds.wordclouds(Data)
