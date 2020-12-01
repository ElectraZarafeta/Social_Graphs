import networkx as nx
import pandas as pd
import regex as re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from fa2 import ForceAtlas2


# Create Directed Graph and save to image
def directed_graph(Data):
    G = nx.DiGraph()

    for i in range(len(Data)):
        name = Data["TwitterUsernames"][i]
        G.add_node(name, Party=Data["Party"][i], Tweets=Data["Tweets"][i])  # new entry of representative in the graph
        usernames_before = re.findall(regex_mentions_retweets, Data["Tweets"][i])

        for username in usernames_before:
            username = username.strip().split('@')[1]

            if username in Data["TwitterUsernames"].values:  # usernames / candidates
                G.add_edge(name, username)

    nx.draw(G, node_size=10)
    plt.savefig("./images/Undirected_Graph.png", format="PNG")

    return G



# Create Giant Connected Component - GCC
def giant_connected_component(G):
    largest_cc = max(nx.weakly_connected_components(G), key=len)
    GCC = G.subgraph(largest_cc)

    print("There are {} links in the GCC network.".format(GCC.number_of_edges()))
    print("There are {} nodes in the GCC network.".format(GCC.number_of_nodes()))

    between_representatives = 0

    for edge in GCC.edges:
        if GCC.nodes[edge[0]]['Party'] != GCC.nodes[edge[1]]['Party']:
            between_representatives += 1

    print(f'Number of links between the representatives (from GCC): {between_representatives}')
    print(f'Percentage of links between the representatives (from GCC): {round(between_representatives / GCC.number_of_edges() * 100, 1)} %')

    return GCC



def in_out_deg(G):
    in_deg = []
    for i in G.nodes:
        in_deg.append(G.in_degree(i))

    index_max_in = sorted(range(len(in_deg)), reverse=True, key=lambda k: in_deg[k])

    node_names = []
    for i in G.nodes:
        node_names.append(i)

    index_max_in = index_max_in[0:5]

    print('The 5 most connected in-degree representatives are:\n')

    for i in range(len(index_max_in)):
        index = index_max_in[i]
        print(node_names[index])

    out_deg = []
    for i in G.nodes:
        out_deg.append(G.out_degree(i))

    index_max_out = sorted(range(len(out_deg)), reverse=True, key=lambda k: out_deg[k])

    index_max_out = index_max_out[0:5]

    print('The 5 most connected out-degree representatives are:\n')

    for i in range(len(index_max_out)):
        index = index_max_out[i]
        print(node_names[index])

    return in_deg, out_deg



def distribution_graph(GCC, mode):
    # find in or out degrees of network
    if mode.lower() == 'in':
        degree_sequence = [d for n, d in G.in_degree()]
    else:
        degree_sequence = [d for n, d in G.out_degree()]
    # find min and max of degrees
    dmax = max(degree_sequence)
    dmin = min(degree_sequence)

    # compute frequencies of degrees distribution
    counts, bins = np.histogram(degree_sequence, bins=np.arange(dmin - 0.5, dmax + 1.5, 1))

    sns.set()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=[15, 5])
    fig.suptitle(mode + '-degree distribution')

    ax1.bar(np.arange(dmin, dmax + 1, 1), counts, color='midnightblue')
    ax1.set_xlim(-1, 60)
    ax1.set_ylim(0, 200)
    ax1.set_xlabel('node degree')
    ax1.set_ylabel('count')

    ax2.loglog(np.arange(dmin, dmax + 1, 1), counts, 'o', color='midnightblue')
    ax2.set_xlim(0.5, 10 ** 3)
    ax2.set_ylim(0.5, 10 ** 3)
    ax2.set_xlabel('log(node degree)')
    ax2.set_ylabel('log(count)')
    plt.show()

    plt.savefig("./images/Degree_Distribution.png", format="PNG")


def forceatlas_graph(GCC):
    # Convert to undirected graph
    GU = GCC.to_undirected()

    # Color nodes according to party
    colors = []
    for n in list(GU.nodes(data="Party")):
        if 'Republican' in n:
            colors.append('red')
        else:
            colors.append('blue')

            # Scale node-size according to degree
    d = nx.degree(GU)
    sizes = [(d[node] + 1) * 5 for node in GU.nodes()]

    # Color edges according to between-party or not
    edge_colors = []
    for edge in GU.edges:
        if GU.nodes[edge[0]]['Party'] != GU.nodes[edge[1]]['Party']:
            edge_colors.append('grey')
        else:
            if GU.nodes[edge[0]]['Party'] == 'Republican':
                edge_colors.append('red')
            else:
                edge_colors.append('blue')

    # Specify the settings for the Force Atlas 2 algorithm
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=7.0,

        # Performance
        jitterTolerance=0.5,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=40,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=0.5,
        strongGravityMode=False,
        gravity=0,

        # Log
        verbose=True)

    positions = forceatlas2.forceatlas2_networkx_layout(GU, pos=None, iterations=4000)

    plt.figure(num=None, figsize=(18, 9), dpi=85, facecolor='w', edgecolor='k')

    sns.set_style('whitegrid')
    sns.set_context('talk')

    # create legend
    plt.scatter([], [], c='red', alpha=0.7, s=100, label='Republican party')
    plt.scatter([], [], c='blue', alpha=0.7, s=100, label='Democrat party')
    plt.legend(scatterpoints=1, frameon=False, labelspacing=1)

    nx.draw_networkx_nodes(GU, positions, node_size=sizes, node_color=colors, alpha=0.5)
    nx.draw_networkx_edges(GU, positions, edge_color=edge_colors, alpha=0.08)
    ax = plt.gca()
    ax.collections[0].set_linewidth(0.1)
    ax.set_title('US House Representatives of 2020 network', fontsize=16);
    plt.axis('off')
    plt.show()

    plt.savefig("./images/ForceAtlas_Graph.png", format="PNG")

    return GU



if __name__ == "__main__":
    # regex for mentions/ retweets
    regex_mentions_retweets = "\s([@][\w_-]+)"

    #load data from csv
    Data = pd.read_csv('./data/Data.csv')

    G = directed_graph(Data)

    GCC = giant_connected_component(G)

    #in and out degree
    in_deg, out_deg = in_out_deg(G)

    #in and out degree distribution
    distribution_graph(GCC, 'In')
    distribution_graph(GCC, 'Out')

    GU = forceatlas_graph(GCC)












