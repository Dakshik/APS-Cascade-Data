import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON file containing cascades
json_file_path = "aps_cascades.json"

with open(json_file_path, "r", encoding="utf-8") as file:
    cascades = json.load(file)

# Sort cascades by the number of participants (filtering out empty ones)
valid_cascades = [c for c in cascades if c["number_of_participants"] > 0]
valid_cascades = sorted(valid_cascades, key=lambda x: x["number_of_participants"])

# Select cascades based on participation count
smallest_cascade = valid_cascades[0]  # Smallest with at least one participant
largest_cascade = valid_cascades[-1]  # Largest with the most participants

# Compute the average size between smallest and largest
average_size = (smallest_cascade["number_of_participants"] + largest_cascade["number_of_participants"]) // 2

# Find the cascade closest to the average size
medium_cascade = min(valid_cascades, key=lambda x: abs(x["number_of_participants"] - average_size))

# Function to create and visualize a cascade graph
def plot_cascade_graph(cascade, title):
    G = nx.DiGraph()
    
    # Add edges based on citation paths
    for participant in cascade["participants"]:
        path_nodes = participant["path"].split("/")
        for i in range(len(path_nodes) - 1):
            G.add_edge(path_nodes[i], path_nodes[i + 1], time=participant["time"])

    # Draw the graph
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)  # Consistent layout for better visualization
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", edge_color="black", linewidths=1, font_size=10, font_weight="bold")

    # Draw edge labels with time delays
    edge_labels = {(u, v): f"{d['time']}s" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red")

    # Display the graph
    plt.title(title)
    plt.show()

# Plot smallest, medium, and largest cascades
plot_cascade_graph(smallest_cascade, "Smallest Cascade Graph")
plot_cascade_graph(medium_cascade, "Medium Cascade Graph")
plot_cascade_graph(largest_cascade, "Largest Cascade Graph")
