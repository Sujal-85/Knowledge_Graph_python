import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit as st

# Streamlit UI Title
st.title("Knowledge Graph: IMDB Movies")

# Load the Dataset
st.subheader("Dataset")
df = pd.read_csv('./imdb_top_1000.csv').head(10)
st.write(df)

# Preprocess the Dataset and Create Relationships
relationships = []

for _, row in df.iterrows():
    movie = row['Series_Title']
    director = row['Director']
    actors = row['Star1'].split(', ')
    genres = row['Genre'].split(', ')

    # Add relationships
    relationships.append((movie, 'Directed By', director))
    for actor in actors:
        relationships.append((movie, 'Stars', actor))
    for genre in genres:
        relationships.append((movie, 'Belongs To', genre))

# Convert relationships to a DataFrame
relationships_df = pd.DataFrame(relationships, columns=['Entity1', 'Relationship', 'Entity2'])

# Display Relationships
st.subheader("Relationships")
st.write(relationships_df)

# Build the Knowledge Graph Using NetworkX
G = nx.DiGraph()

for _, row in relationships_df.iterrows():
    G.add_edge(row['Entity1'], row['Entity2'], relation=row['Relationship'])

# Visualize the Knowledge Graph Using Pyvis
st.subheader("Knowledge Graph Visualization")

# Initialize Pyvis Network
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

# Add nodes and edges from the NetworkX graph
for node in G.nodes():
    net.add_node(node, label=node, title=node)

for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], title=edge[2]['relation'])

# Save and render the Pyvis graph
net.save_graph("imdb_knowledge_graph.html")

# Display the Pyvis graph in Streamlit
HtmlFile = open("imdb_knowledge_graph.html", "r", encoding="utf-8")
components = HtmlFile.read()
st.components.v1.html(components, height=750)
