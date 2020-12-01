import networkx as nx
import pandas as pd
import regex as re
import matplotlib.pyplot as plt


# Create Undirected Graph and save to image
def undirected_graph(Data):
    G = nx.DiGraph()

    for i in range(len(Data)):
        name = Data["TwitterUsernames"][i]
        G.add_node(name, Party=Data["Party"][i], Tweets=Data["Tweets"][i])  # new entry of representative in the graph
        usernames_before = re.findall(regex_mentions_retweets, Data["Tweets"][i])

        for username in usernames_before:
            username = username.strip().split('@')[1]

        if username in Data["TwitterUsernames"]:  # usernames / candidates
            G.add_edge(name, username)

    nx.draw(G, node_size=10)
    plt.savefig("./images/Undirected_Graph.png", format="PNG")

    return G

# Create Giant Connected Component - GCC
def giant_connected_component(G):
    largest_cc = max(nx.weakly_connected_components(G), key=len)
    GCC = G.subgraph(largest_cc)

    return GCC

if __name__ == "__main__":
    # regex for mentions/ retweets
    regex_mentions_retweets = "\s([@][\w_-]+)"

    #load data from csv
    Data = pd.read_csv('./data/Data.csv')

    G = undirected_graph(Data)

    GCC = giant_connected_component(G)

    print("There are {} links in the GCC network.".format(GCC.number_of_edges()))
    print("There are {} nodes in the GCC network.".format(GCC.number_of_nodes()))


