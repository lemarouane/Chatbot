import mysql.connector
import streamlit as st

# Établir une connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot"
)
cursor = conn.cursor()

# Créer une requête SQL pour extraire les données
query = "SELECT * FROM conversations"

# Exécuter la requête et récupérer les données
cursor.execute(query)
data = cursor.fetchall()

# Afficher les données dans Streamlit
st.write("Données de la base de données :")
st.dataframe(data)

# Fermer la connexion à la base de données
cursor.close()
conn.close()
