import pandas as pd

from Social_Graphs import graph_generator
from Social_Graphs import wordclouds

if __name__ == "__main__":
    #load data from csv
    Data = pd.read_csv('./data/Data.csv')

    G = graph_generator.directed_graph(Data)

    GCC = graph_generator.giant_connected_component(G)

    #in and out degree
    in_deg, out_deg = graph_generator.in_out_deg(G)

    #in and out degree distribution
    graph_generator.distribution_graph(GCC, 'In')
    graph_generator.distribution_graph(GCC, 'Out')

    GU = graph_generator.forceatlas_graph(GCC)


    wordclouds.wordclouds(Data)