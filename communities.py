import string
import networkx as nx
import nltk
import math
from community import community_louvain
import matplotlib.pyplot as plt
from fa2 import ForceAtlas2
from nltk import WordNetLemmatizer
import seaborn as sns

lemmatizer = WordNetLemmatizer()  # assign the lemmatization function to a variable
pun = string.punctuation  # assign to a string all sets of punctuation
stops = nltk.corpus.stopwords.words('english')  # assign the list of english stop words (commonly used words)


def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos


def _position_communities(g, partition, **kwargs):
    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos


def _find_between_community_edges(g, partition):
    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges


def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos


def communities(GU, Data, truss_nodes, p):
    largest_cc = max(nx.connected_components(GU), key=len)
    GU_party = GU.subgraph(largest_cc)

    partition = community_louvain.best_partition(GU_party)

    nodes = []
    for node in GU_party.nodes():
        if node not in truss_nodes:
            nodes.append(node)

    node_color = []
    for key, value in partition.items():
        if key not in truss_nodes:
            node_color.append(value)

    pos = community_layout(GU_party, partition)

    node_pos = {}
    truss_pos = {}
    for key, value in pos.items():
        if key in truss_nodes:
            truss_pos[key] = value
        else:
            node_pos[key] = value

    plt.figure(num=None, figsize=(15, 9), dpi=80, facecolor='w', edgecolor='k')
    nx.draw_networkx_nodes(GU_party, node_pos, node_size=400, node_shape="o", cmap=plt.cm.RdYlBu, nodelist=nodes, node_color=node_color, alpha=0.8)
    nx.draw_networkx_nodes(GU_party, truss_pos, node_size=800, node_shape="*", node_color="black", nodelist=truss_nodes, alpha=0.8)
    nx.draw_networkx_edges(GU_party, pos, alpha=0.2, edge_color="grey")
    plt.axis('off')
    if p == "d":
        plt.savefig("./images/communities_democrat.png", format="PNG")
    elif p == "r":
        plt.savefig("./images/communities_republican.png", format="PNG")