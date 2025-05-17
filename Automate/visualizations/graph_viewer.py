import matplotlib.pyplot as plt
import networkx as nx
from models.automate import Automate

def visualize_automate(automate: Automate):
    """Affiche un automate sous forme de graphe avec networkx et matplotlib."""
    G = nx.MultiDiGraph()

    # Ajout des nœuds (états)
    for etat in automate.etats:
        node_color = 'lightblue'
        if etat.est_initial and etat.est_final:
            node_color = 'lightgreen'
        elif etat.est_initial:
            node_color = 'yellow'
        elif etat.est_final:
            node_color = 'green'
        G.add_node(etat.nom, color=node_color)

    # Ajout des transitions (arcs)
    for t in automate.transitions:
        G.add_edge(t.etat_depart, t.etat_arrive, label=t.symbole)

    # Positions automatiques des nœuds
    pos = nx.spring_layout(G)

    # Récupération des couleurs des nœuds
    node_colors = [G.nodes[n]['color'] for n in G.nodes]

    # Dessin du graphe
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True, connectionstyle='arc3,rad=0.2')
    
    # Affichage des étiquettes des transitions
    #edge_labels = nx.get_edge_attributes(G, 'label')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    edge_labels = {(u, v, k): d['label'] for u, v, k, d in G.edges(keys=True, data=True)}
    
    print(edge_labels)
    # Draw each edge label
    for (u, v, k), label in edge_labels.items():
    # You can customize this to shift labels slightly to avoid overlap
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2 + 0.05 * (int(k))  # vertical shift based on key
        plt.text(x, y, label, fontsize=10, color='red', ha='center')


    # Affichage final
    plt.title(f"Automate : {automate.nom}")
    plt.axis('off')
    plt.show()

# Test rapide (exécutable uniquement si ce fichier est lancé directement)
if __name__ == "__main__":
    from utils.json_handler import load_automate, list_saved_automates

    automates = list_saved_automates()
    if not automates:
        print("❌ Aucun automate trouvé. Veuillez en créer un d'abord.")
    else:
        print("📚 Automates disponibles :", automates)
        name = input("Nom de l'automate à afficher : ")
        try:
            automate = load_automate(name)
            visualize_automate(automate)
        except FileNotFoundError:
            print("❌ Fichier non trouvé.")
