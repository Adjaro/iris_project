import requests
import streamlit as st
import json
import pandas as pd
import time
from requests.exceptions import ConnectionError, Timeout
import os

# URL de l'API
# API_URL = "http://localhost:8000/predict"
API_URL = "http://server:8000/predict"
# API_URL = "http://mlops-server:8000/predict"

# Configuration de la page
st.set_page_config(
    page_title="🌸 Classification d'Iris", 
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #9146FF;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        text-align: center;
    }
    .result-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #9146FF;
        color: white;
        font-size: 1.2rem;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">🌸 Classification d\'Iris</h1>', unsafe_allow_html=True)

# Description de l'application
st.markdown("""
Cette application prédit l'espèce d'une fleur Iris en fonction des dimensions de ses sépales et pétales.
Ajustez les mesures ci-dessous et cliquez sur "Prédire" pour voir le résultat.
""")

# Interface principale avec deux colonnes
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📏 Caractéristiques de la fleur")
    
    # Formulaire d'entrée
    with st.form("prediction_form"):
        # Entrées utilisateur
        sepal_length = st.slider("Longueur du sépale (cm)", 
                               min_value=4.0, max_value=8.0, value=5.4, step=0.1,
                               help="Valeur typique entre 4.3 et 7.9 cm")
        
        sepal_width = st.slider("Largeur du sépale (cm)", 
                              min_value=2.0, max_value=4.5, value=3.2, step=0.1,
                              help="Valeur typique entre 2.0 et 4.4 cm")
        
        petal_length = st.slider("Longueur du pétale (cm)", 
                               min_value=1.0, max_value=7.0, value=1.5, step=0.1,
                               help="Valeur typique entre 1.0 et 6.9 cm")
        
        petal_width = st.slider("Largeur du pétale (cm)", 
                              min_value=0.1, max_value=2.5, value=0.2, step=0.1,
                              help="Valeur typique entre 0.1 et 2.5 cm")
        
        # Bouton de soumission
        submit_button = st.form_submit_button(label="🔍 PRÉDIRE L'ESPÈCE", use_container_width=True)

# Définition du mapping des espèces pour les images et informations
species_mapping = {
    "Iris-setosa": {
        "nom_fr": "Iris Setosa",
        "image": "./assets/iris_setosa.jpg",
        "description": "L'Iris setosa est reconnaissable par ses pétales courts et ses sépales larges. Cette espèce se distingue facilement des deux autres."
    },
    "Iris-versicolor": {
        "nom_fr": "Iris Versicolor",
        "image": "./assets/iris_versicolor.jpg",
        "description": "L'Iris versicolor présente des dimensions intermédiaires entre les deux autres espèces. Ses pétales sont de taille moyenne."
    },
    "Iris-virginica": {
        "nom_fr": "Iris Virginica",
        "image": "./assets/iris_virginica.jpg",
        "description": "L'Iris virginica se distingue par ses grands pétales et sépales. C'est généralement la plus grande des trois espèces."
    },
    # Ajout pour gérer les cas où l'API retourne sans préfixe "Iris-"
    "setosa": {
        "nom_fr": "Iris Setosa",
        "image": "./assets/iris_setosa.jpg",
        "description": "L'Iris setosa est reconnaissable par ses pétales courts et ses sépales larges. Cette espèce se distingue facilement des deux autres."
    },
    "versicolor": {
        "nom_fr": "Iris Versicolor",
        "image": "./assets/iris_versicolor.jpg",
        "description": "L'Iris versicolor présente des dimensions intermédiaires entre les deux autres espèces. Ses pétales sont de taille moyenne."
    },
    "virginica": {
        "nom_fr": "Iris Virginica",
        "image": "./assets/iris_virginica.jpg",
        "description": "L'Iris virginica se distingue par ses grands pétales et sépales. C'est généralement la plus grande des trois espèces."
    }
}

# Mapping des chemins d'images pour chaque espèce
image_paths = {
    "Iris-setosa": ["./assets/iris_setosa.jpg", "./assets/iris-setosa.jpg", "./assets/setosa.jpg"],
    "Iris-versicolor": ["./assets/iris_versicolor.jpg", "./assets/iris-versicolor.jpg", "./assets/versicolor.jpg"],
    "Iris-virginica": ["./assets/iris_virginica.jpg", "./assets/iris-virginica.jpg", "./assets/virginica.jpg"],
    "setosa": ["./assets/iris_setosa.jpg", "./assets/iris-setosa.jpg", "./assets/setosa.jpg"],
    "versicolor": ["./assets/iris_versicolor.jpg", "./assets/iris-versicolor.jpg", "./assets/versicolor.jpg"],
    "virginica": ["./assets/iris_virginica.jpg", "./assets/iris-virginica.jpg", "./assets/virginica.jpg"]
}

# Traitement de la prédiction
with col2:
    st.subheader("🌸 Résultat de la prédiction")
    
    # Par défaut, afficher l'image générique des iris
    if not submit_button:
        # Correction de l'erreur: suppression de use_container_width
        st.image("./assets/image_iris.png", caption="Les trois espèces d'Iris", width=700)
        st.info("Ajustez les paramètres et cliquez sur 'Prédire' pour voir le résultat.")
    
    # Si le formulaire est soumis
    if submit_button:
        # Préparation des données pour l'API
        payload = {
            "sepal_length": float(sepal_length),
            "sepal_width": float(sepal_width),
            "petal_length": float(petal_length),
            "petal_width": float(petal_width)
        }
        
        # Animation de chargement
        with st.spinner("Analyse en cours..."):
            # Simuler un petit délai pour l'expérience utilisateur
            time.sleep(1.5)
            
            try:
                # Appel à l'API
                response = requests.post(API_URL, json=payload, timeout=10)
                
                # Traitement de la réponse
                if response.status_code == 200:
                    try:
                        result = response.json()
                        # st.write(result)  # Debug: afficher la réponse brute
                        prediction = result.get("prediction")
                        confidence = result.get("probabilities", 0) * 100
                        
                        # Récupérer les informations de l'espèce prédite
                        species_info = species_mapping.get(prediction, {
                            "nom_fr": prediction,
                            "image": "./assets/image_iris.png",
                            "description": "Information non disponible pour cette espèce."
                        })
                        
                        # Afficher la carte de résultat
                        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                        st.markdown(f'<p class="result-header">Espèce prédite: {species_info["nom_fr"]}</p>', unsafe_allow_html=True)
                        
                        # Trouver le premier chemin d'image valide pour l'espèce prédite
                        image_found = False
                        image_path = None
                        
                        # Chercher dans la liste des chemins possibles pour cette espèce
                        if prediction in image_paths:
                            for path in image_paths[prediction]:
                                if os.path.exists(path):
                                    image_path = path
                                    image_found = True
                                    break
                        
                        # Si aucune image n'a été trouvée, utiliser l'image par défaut
                        if not image_found:
                            image_path = "./assets/image_iris.png"
                            if not os.path.exists(image_path):
                                image_path = None
                        
                        # Afficher l'image si trouvée
                        if image_path:
                            try:
                                st.image(image_path, caption=f"{species_info['nom_fr']}", width=300)
                            except Exception as img_error:
                                st.warning(f"🖼️ Erreur lors de l'affichage de l'image: {image_path}")
                                st.exception(img_error)
                        else:
                            st.warning("🖼️ Aucune image disponible pour cette espèce.")
                            st.info(f"Vérifiez que les images des espèces d'iris sont présentes dans le dossier 'assets/'.")
                            
                            # Afficher les chemins recherchés
                            if prediction in image_paths:
                                st.text("Chemins recherchés:")
                                for path in image_paths[prediction]:
                                    st.code(path)
                        
                        # Afficher le niveau de confiance
                        if "confidence" in result:
                            st.markdown("### Niveau de confiance")
                            st.progress(confidence/100)
                            st.metric("Confiance", f"{confidence:.1f}%")
                        
                        # Description de l'espèce
                        st.markdown("### Description")
                        st.markdown(species_info["description"])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    except json.JSONDecodeError:
                        st.error("❌ La réponse du serveur n'est pas dans un format JSON valide.")
                        with st.expander("Détails de l'erreur"):
                            st.code(response.text)
                
                else:
                    st.error(f"❌ Erreur {response.status_code}: {response.reason}")
                    with st.expander("Détails de l'erreur"):
                        st.code(response.text)

            except ConnectionError:
                st.error("❌ Impossible de se connecter au serveur API.")
                st.info(f"Vérifiez que le serveur est en cours d'exécution à l'adresse: {API_URL}")
                
            except Timeout:
                st.error("❌ Le serveur API a mis trop de temps à répondre.")
                
            except Exception as e:
                st.error(f"❌ Une erreur inattendue est survenue: {str(e)}")

# Tableau récapitulatif des mesures
st.subheader("📊 Résumé des mesures")
input_data = pd.DataFrame({
    "Caractéristique": ["Longueur sépale", "Largeur sépale", "Longueur pétale", "Largeur pétale"],
    "Valeur (cm)": [sepal_length, sepal_width, petal_length, petal_width]
})
# Correction de l'erreur: pour les versions plus anciennes de Streamlit, ne pas utiliser use_container_width
st.dataframe(input_data, hide_index=True)

# Section d'informations
with st.expander("ℹ️ À propos des espèces d'Iris"):
    st.markdown("""
    ### Les trois espèces d'Iris du dataset
    
    Le dataset Iris contient des échantillons de trois espèces d'Iris:
    
    1. **Iris setosa** - Se caractérise par des pétales courts et des sépales larges
    2. **Iris versicolor** - Présente des caractéristiques intermédiaires
    3. **Iris virginica** - Possède de grands pétales et sépales
    
    Ces trois espèces peuvent être différenciées par les dimensions de leurs pétales et sépales,
    ce qui en fait un excellent exemple pour la classification en machine learning.
    """)
    
    # Afficher une comparaison des espèces
    col_a, col_b, col_c = st.columns(3)
    
    try:
        with col_a:
            st.markdown("#### Iris Setosa")
            # Vérifier quelle image existe réellement
            setosa_images = ["./assets/iris_setosa.jpg", "./assets/iris-setosa.jpg", "./assets/setosa.jpg"]
            image_found = False
            for img_path in setosa_images:
                if os.path.exists(img_path):
                    st.image(img_path, width=220)
                    image_found = True
                    break
            if not image_found:
                st.warning("Image non disponible")
            
        with col_b:
            st.markdown("#### Iris Versicolor")
            versicolor_images = ["./assets/iris_versicolor.jpg", "./assets/iris-versicolor.jpg", "./assets/versicolor.jpg"]
            image_found = False
            for img_path in versicolor_images:
                if os.path.exists(img_path):
                    st.image(img_path, width=220)
                    image_found = True
                    break
            if not image_found:
                st.warning("Image non disponible")
            
        with col_c:
            st.markdown("#### Iris Virginica")
            virginica_images = ["./assets/iris_virginica.jpg", "./assets/iris-virginica.jpg", "./assets/virginica.jpg"]
            image_found = False
            for img_path in virginica_images:
                if os.path.exists(img_path):
                    st.image(img_path, width=220)
                    image_found = True
                    break
            if not image_found:
                st.warning("Image non disponible")
    except Exception as img_comp_error:
        st.warning("Certaines images d'illustration n'ont pas pu être chargées.")
        st.exception(img_comp_error)

# Ajout d'une gestion de vérification des fichiers
if not submit_button:
    with st.expander("🛠️ Vérification des ressources"):
        st.markdown("### Vérification des ressources nécessaires")
        # Vérification de la connexion API
        try:
            requests.get(API_URL.replace('/predict', '/health'), timeout=2)
            st.success("✅ API accessible")
        except Exception as api_error:
            st.error("❌ API non accessible à l'adresse: " + API_URL)
            st.info("Assurez-vous que le serveur FastAPI est démarré.")
            
        # Vérification des images
        st.markdown("### Vérification des images")
        
        images_to_check = [
            ("Image générique", "./assets/image_iris.png"),
            ("Iris Setosa", ["./assets/iris_setosa.jpg", "./assets/iris-setosa.jpg"]),
            ("Iris Versicolor", ["./assets/iris_versicolor.jpg", "./assets/iris-versicolor.jpg"]),
            ("Iris Virginica", ["./assets/iris_virginica.jpg", "./assets/iris-virginica.jpg"])
        ]
        
        for name, paths in images_to_check:
            if isinstance(paths, list):
                found = False
                for path in paths:
                    if os.path.exists(path):
                        st.success(f"✅ {name}: {path}")
                        found = True
                        break
                if not found:
                    st.error(f"❌ {name}: aucun des chemins suivants n'existe")
                    for path in paths:
                        st.text(f"   - {path}")
            else:
                if os.path.exists(paths):
                    st.success(f"✅ {name}: {paths}")
                else:
                    st.error(f"❌ {name}: {paths} n'existe pas")

# Pied de page
st.markdown("---")
st.markdown("Application de prédiction d'Iris © 2025 | Réalisée avec Streamlit et FastAPI")