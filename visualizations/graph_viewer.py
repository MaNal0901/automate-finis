import itertools as it
import matplotlib.pyplot as plt
import networkx as nx
from models.automate import Automate

def visualize_automate(automate: Automate, return_fig=False):
    """
    Visualize an automaton with improved layout and clarity.
    
    Parameters:
    - automate: Automate object containing states and transitions
    """
    G = nx.MultiDiGraph()
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]

    # Add nodes with color attributes
    for etat in automate.etats:
        if etat.est_initial and etat.est_final:
            node_color = 'orange'
        elif etat.est_initial:
            node_color = 'yellow'
        elif etat.est_final:
            node_color = 'green'
        else:
            node_color = 'lightblue'
        G.add_node(etat.nom, color=node_color)

    # Add edges with transition labels
    for t in automate.transitions:
        G.add_edge(t.etat_depart, t.etat_arrive, w=t.symbole)

    # Improved spring layout for better spacing
    pos = nx.spring_layout(G, k=0.7, iterations=200, seed=42)

    # Node color list
    node_colors = [G.nodes[n]['color'] for n in G.nodes]

    # Drawing
    plt.figure(figsize=(10, 8))  # Larger figure for clarity
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, arrows=True,arrowstyle='-|>', arrowsize=20,node_size=800, edge_color="grey", connectionstyle=connectionstyle)
    
    # Add edge labels in the style of draw_labeled_multigraph
    labels = {
        tuple(edge): f"{attrs['w']}"
        for *edge, attrs in G.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        G,
        pos,
        labels,
        connectionstyle=connectionstyle,
        label_pos=0.5,
        font_color='k',
        bbox={"alpha": 0},
    )
    
    if return_fig:
        fig = plt.gcf()
        plt.close()
        return fig
    else:
        plt.show()
        plt.close()

