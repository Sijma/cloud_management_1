import database
import networkx as nx
from datetime import datetime

import random  # For sampling
from pyvis.network import Network # For Demonstration

# Fetch all articles from the database
articles = database.fetch_all_articles()

# Create an empty graph
article_graph = nx.Graph()

# Add nodes to graph
for article in articles:
    article["_id"] = str(article["_id"])
    article["publishedAt"] = str(article["publishedAt"])
    article_graph.add_node(article["_id"], source=article["source"]["name"], author=article["author"], timestamp=article["publishedAt"])

# Add edges based on the criteria
for i, article1 in enumerate(articles):
    for article2 in articles[i+1:]:
        if article1["source"]["name"] == article2["source"]["name"] or article1["author"] == article2["author"]:
            article_graph.add_edge(article1["_id"], article2["_id"])

# Connect nodes with no connections using the closest timestamp
for node in article_graph.nodes():
    if article_graph.degree(node) == 0:
        closest_node = None
        closest_timestamp = None
        for other_node in article_graph.nodes():
            if node != other_node:
                if closest_node is None:
                    closest_node = other_node
                    closest_timestamp = abs(datetime.strptime(article_graph.nodes[node]["timestamp"], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(article_graph.nodes[other_node]["timestamp"], "%Y-%m-%dT%H:%M:%SZ"))
                else:
                    other_timestamp = abs(datetime.strptime(article_graph.nodes[node]["timestamp"], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(article_graph.nodes[other_node]["timestamp"], "%Y-%m-%dT%H:%M:%SZ"))
                    if other_timestamp < closest_timestamp:
                        closest_node = other_node
                        closest_timestamp = other_timestamp
        article_graph.add_edge(node, closest_node)

# Set the fraction of nodes to keep
fraction_to_keep = 0.1

# Get the number of nodes to keep
num_nodes_to_keep = int(fraction_to_keep * article_graph.number_of_nodes())

random_nodes = random.sample(article_graph.nodes(), num_nodes_to_keep)

subgraph = article_graph.subgraph(random_nodes)
n = Network(notebook=True)
n.repulsion()
n.from_nx(subgraph)
#n.show("graph.html")


def get_recommended(article_id):
    # Get the degree centrality of all nodes in the graph
    degree_centrality = nx.degree_centrality(article_graph)

    # Get the neighbors of the article
    neighbors = article_graph.neighbors(article_id)

    # Find the neighbor with the highest degree centrality
    highest_degree_centrality = -1
    highest_degree_centrality_neighbor = None
    for neighbor in neighbors:
        if degree_centrality[neighbor] > highest_degree_centrality:
            highest_degree_centrality = degree_centrality[neighbor]
            highest_degree_centrality_neighbor = neighbor

    # Return the neighbor with the highest degree centrality
    recommendation = database.get_article_by_id(highest_degree_centrality_neighbor)
    print(recommendation)
    if recommendation is None:
        return "No recommendations found."
    return recommendation
