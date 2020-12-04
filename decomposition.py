import networkx as nx
import matplotlib.pyplot as plt
from fa2 import ForceAtlas2
import seaborn as sns


def decomposition_republican(GU, core=False, truss=False):
    # Republican Graph
    nodes = (
        node
        for node, data in GU.nodes(data=True)
        if data.get("Party") == "Republican"
    )

    largest_cc = max(nx.connected_components(nx.Graph(GU.subgraph(nodes))), key=len)
    GU_Republican = GU.subgraph(largest_cc)

    if core:
        nodes = nx.k_core(GU_Republican, k=9).nodes()
    elif truss:
        nodes = nx.k_truss(GU_Republican, k=5).nodes()

    node_color = []
    for node in GU_Republican.nodes():
        if node in nodes:
            node_color.append("yellow")
        else:
            node_color.append("red")

    d = nx.degree(GU_Republican)
    sizes = [(d[node] + 1) * 5 for node in GU_Republican.nodes()]

    # Specify the settings for the Force Atlas 2 algorithm
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        gravity=5.0,

        # Log
        verbose=True)

    positions = forceatlas2.forceatlas2_networkx_layout(GU, pos=None, iterations=2000)

    plt.figure(num=None, figsize=(15, 9), dpi=80, facecolor='w', edgecolor='k')

    sns.set_style('whitegrid')
    sns.set_context('talk')

    # create legend
    plt.scatter([], [], c='yellow', alpha=0.7, s=100, label='Most Influential Republicans')
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1)

    nx.draw_networkx_nodes(GU_Republican, positions, node_size=sizes, node_color=node_color, alpha=0.7)
    nx.draw_networkx_edges(GU_Republican, positions, edge_color="grey", alpha=0.08)
    ax = plt.gca()
    ax.collections[0].set_linewidth(0.1)
    ax.set_title('US House Republican Representatives of 2020 network', fontsize=16);
    plt.axis('off')

    if core:
        plt.savefig("./images/core_republican.png", format="PNG")
    elif truss:
        plt.savefig("./images/truss_republican.png", format="PNG")
        return nodes, GU_Republican




def decomposition_democrat(GU, core=False, truss=False):
    # Democrat Graph
    nodes = (
        node
        for node, data in GU.nodes(data=True)
        if data.get("Party") == "Democrat"
    )

    largest_cc = max(nx.connected_components(nx.Graph(GU.subgraph(nodes))), key=len)
    GU_Democrat = GU.subgraph(largest_cc)

    if core:
        nodes = nx.k_core(GU_Democrat, k=12).nodes()
    elif truss:
        nodes = nx.k_truss(GU_Democrat, k=4).nodes()

    node_color = []
    for node in GU_Democrat.nodes():
        if node in nodes:
            node_color.append("yellow")
        else:
            node_color.append("blue")

    d = nx.degree(GU_Democrat)
    sizes = [(d[node] + 1) * 5 for node in GU_Democrat.nodes()]

    # Specify the settings for the Force Atlas 2 algorithm
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        gravity=5.0,

        # Log
        verbose=True)

    positions = forceatlas2.forceatlas2_networkx_layout(GU, pos=None, iterations=2000)

    plt.figure(num=None, figsize=(15, 9), dpi=80, facecolor='w', edgecolor='k')

    sns.set_style('whitegrid')
    sns.set_context('talk')

    # create legend
    plt.scatter([], [], c='yellow', alpha=0.7, s=100, label='Most Influential Democrats')
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1)

    nx.draw_networkx_nodes(GU_Democrat, positions, node_size=sizes, node_color=node_color, alpha=0.7)
    nx.draw_networkx_edges(GU_Democrat, positions, edge_color="grey", alpha=0.08)
    ax = plt.gca()
    ax.collections[0].set_linewidth(0.1)
    ax.set_title('US House Democrat Representatives of 2020 network', fontsize=16);
    plt.axis('off')

    if core:
        plt.savefig("./images/core_democrat.png", format="PNG")
    elif truss:
        plt.savefig("./images/truss_democrat.png", format="PNG")
        return nodes, GU_Democrat





