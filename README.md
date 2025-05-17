# 🔄 Gestion des Automates Finis

Une application web interactive pour la manipulation et l'analyse des automates finis, développée avec Streamlit.

## 📋 Contexte du Projet

Dans le cadre du module "Mathématiques pour Ingénieurs", nous avons réalisé ce projet qui a été encadré par :
- Pr. LAZAIZ
- Pr. KAMOUSS

## 🙏 Remerciements

Nous tenons à exprimer notre profonde gratitude envers nos professeurs encadrants :

### Pr. LAZAIZ
Pour son expertise précieuse dans le domaine des mathématiques pour l'ingénieur et ses conseils avisés qui ont grandement contribué à la réussite de ce projet. Sa passion pour l'enseignement et sa capacité à transmettre des concepts complexes de manière claire ont été une source d'inspiration constante.

### Pr. KAMOUSS
Pour son encadrement rigoureux et son soutien continu tout au long du projet. Ses retours constructifs et son expertise technique ont été déterminants dans l'amélioration de notre travail.

## 🎯 Importance du Projet

Ce projet revêt une importance particulière pour plusieurs raisons :

1. **Application Pratique des Connaissances Théoriques**
   - Mise en pratique concrète des concepts mathématiques
   - Développement d'une solution logicielle complète
   - Expérience hands-on avec les automates finis

2. **Développement de Compétences Professionnelles**
   - Travail en équipe et gestion de projet
   - Résolution de problèmes complexes
   - Documentation et présentation technique

3. **Innovation et Créativité**
   - Conception d'une interface utilisateur intuitive
   - Implémentation d'algorithmes sophistiqués
   - Développement de fonctionnalités avancées

4. **Préparation au Monde Professionnel**
   - Exposition aux méthodologies de développement
   - Utilisation d'outils et technologies modernes
   - Gestion de la complexité des systèmes informatiques

## 📋 Description

Cette application permet de créer, visualiser, modifier et analyser des automates finis. Elle offre une interface graphique intuitive pour effectuer diverses opérations sur les automates, telles que la déterminisation, la minimisation, et la vérification de propriétés.

## 🌟 Fonctionnalités

### 1. 📝 Création d'Automates
- Définition des états (initiaux et finaux)
- Spécification de l'alphabet
- Création des transitions
- Visualisation en temps réel

### 2. 📂 Chargement et Sauvegarde
- Sauvegarde automatique des automates
- Chargement des automates existants
- Visualisation des informations détaillées

### 3. ✏️ Modification
- Ajout/suppression d'états
- Modification de l'alphabet
- Gestion des transitions
- Mise à jour en temps réel

### 4. 🔍 Analyse
- Vérification du déterminisme
- Test de complétude
- Complétion d'automate
- Minimisation

### 5. 🔄 Opérations
- Union d'automates
- Intersection
- Complément
- Déterminisation
- Test d'équivalence

### 6. ▶️ Simulation
- Test de mots
- Génération de mots acceptés/rejetés
- Visualisation du parcours

## 🎨 Interface

L'interface utilise un système d'onglets pour organiser les différentes fonctionnalités :
- Les états sont représentés par des cercles colorés
- Les transitions sont affichées avec des flèches
- Code couleur intuitif :
  - État initial : Cercle  jaune
  - État final : Cercle vert
  - État initial et final :Cercle orange
  - État normal : Cercle  bleu clair

## 🏗️ Structure du Projet

```
automate_projet/
├── interface/
│   ├── app.py          # Point d'entrée de l'application
│   ├── markdown.py     # Styles CSS
│   └── __init__.py
├── pages/
│   ├── create_page.py  # Création d'automates
│   ├── load_page.py    # Chargement d'automates
│   ├── edit_page.py    # Modification d'automates
│   ├── analyze_page.py # Analyse d'automates
│   ├── operations_page.py # Opérations sur les automates
│   ├── simulate_page.py   # Simulation d'automates
│   └── __init__.py
├── models/             # Classes de modèles
│   ├── etat.py
│   ├── alphabet.py
│   ├── transition.py
│   └── automate.py
├── services/          # Services métier
│   ├── analysis_tools.py
│   └── simulation_tools.py
├── utils/            # Utilitaires
│   └── json_handler.py
└── visualizations/   # Outils de visualisation
    └── graph_viewer.py
```

## 🚀 Installation

1. Cloner le dépôt :
```bash
git clone [url-du-depot]
cd automate-projet
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer l'application :
```bash
streamlit run interface/app.py
```

## 📦 Dépendances Principales

- Python >= 3.7
- streamlit >= 1.28.0
- networkx >= 3.1
- matplotlib >= 3.7.1

## 💡 Utilisation

1. **Créer un Automate**
   - Accéder à l'onglet "Créer"
   - Définir les états et l'alphabet
   - Ajouter les transitions
   - Visualiser l'automate en temps réel

2. **Analyser un Automate**
   - Charger un automate existant
   - Utiliser les outils d'analyse
   - Visualiser les résultats

3. **Effectuer des Opérations**
   - Sélectionner deux automates pour les opérations binaires
   - Choisir l'opération désirée
   - Observer le résultat

4. **Simuler un Automate**
   - Entrer un mot à tester
   - Voir le résultat de l'acceptation
   - Générer des exemples de mots

## 🔧 Maintenance

Pour ajouter de nouvelles fonctionnalités :
1. Créer les services nécessaires dans `/services`
2. Ajouter les modèles requis dans `/models`
3. Créer une nouvelle page dans `/pages` si nécessaire
4. Mettre à jour l'interface utilisateur


## 👥 Réalisé par
- REDOUNE HAKIM
- ECHALH MANAL
- MOUHIBI ASSIA
- CHIGUER OTHMANE


