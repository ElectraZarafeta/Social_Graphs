import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

from Social_Graphs import graph_generator
from Social_Graphs import wordclouds
from Social_Graphs import decomposition
from Social_Graphs import communities
from Social_Graphs import hashtag_correlations
from Social_Graphs import StateSentiment

if __name__ == "__main__":
    # load data from csv
    Data = pd.read_csv('./data/Data.csv')

    G = graph_generator.directed_graph(Data)

    GCC = graph_generator.giant_connected_component(G)

    # in and out degree
    in_deg, out_deg = graph_generator.in_out_deg(G)

    # in and out degree distribution
    graph_generator.distribution(GCC, 'In')
    graph_generator.distribution(GCC, 'Out')

    # Convert to undirected graph
    GU = GCC.to_undirected()

    # force atlas
    graph_generator.forceatlas_graph(GU)

    # core decomposition
    decomposition.decomposition_republican(GU, core=True)
    decomposition.decomposition_democrat(GU, core=True)

    # truss decomposition
    truss_nodes_r, GU_Republican = decomposition.decomposition_republican(GU, truss=True)
    truss_nodes_d, GU_Democrat = decomposition.decomposition_democrat(GU, truss=True)

    # word cloud generator
    wordclouds.wordclouds(Data)

    # community generator
    communities.communities(GU_Republican, Data, truss_nodes_r, p="r")
    communities.communities(GU_Democrat, Data, truss_nodes_d, p="d")

    # hashtag correlation
    hashtag_correlations.hashtag_correlations(Data, republican=True)
    hashtag_correlations.hashtag_correlations(Data, democrat=True)
    
    #Sentiment by State
    StateSentiment.initialization(Data)

