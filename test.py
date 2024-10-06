import matplotlib.pyplot as plt
import networkx as nx

def create_mind_map():
    # Initialize the directed graph
    mind_map = nx.DiGraph()

    # Define the nodes and their hierarchical relationships
    mind_map.add_edges_from([
        ("Main Idea", "Sub Idea 1"),
        ("Main Idea", "Sub Idea 2"),
        ("Main Idea", "Sub Idea 3"),
        ("Sub Idea 1", "Detail 1.1"),
        ("Sub Idea 1", "Detail 1.2"),
        ("Sub Idea 2", "Detail 2.1"),
        ("Sub Idea 2", "Detail 2.2"),
        ("Sub Idea 3", "Detail 3.1"),
        ("Sub Idea 3", "Detail 3.2"),
        ("Detail 1.1", "Note 1"),
        ("Detail 2.1", "Note 2"),
        ("Detail 3.1", "Note 3"),
    ])

    # Set up plot
    plt.figure(figsize=(8, 8))

    # Create the layout for the nodes (spring layout makes it look like a mind map)
    pos = nx.spring_layout(mind_map, k=0.8, seed=42)

    # Draw nodes
    nx.draw_networkx_nodes(mind_map, pos, node_size=2000, node_color='lightblue', node_shape='o', alpha=0.9)

    # Draw edges
    nx.draw_networkx_edges(mind_map, pos, edge_color='gray', width=2, alpha=0.5)

    # Draw labels
    nx.draw_networkx_labels(mind_map, pos, font_size=10, font_color='black', font_family='sans-serif')

    # Set the title
    plt.title("Professional Mind Map", fontsize=16)
    
    # Remove axis
    plt.axis('off')
    
    # Show the mind map
    plt.show()

create_mind_map()
