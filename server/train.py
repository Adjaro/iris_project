from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import  pickle
from sklearn.pipeline import make_pipeline
from   sklearn.preprocessing import StandardScaler
import os


scaler = StandardScaler()
model = make_pipeline(scaler, DecisionTreeClassifier(random_state=42))

# Charger le jeu de données Iris
data = pd.read_csv("server/data/iris.csv")

X = data.drop("label", axis=1)
y = data["label"]

# Entraîner le modèle
model.fit(X, y)

#creer le  dossier model si il n'existe pas
if not os.path.exists("model"):
    os.makedirs("model")
# Sauvegarder le modèle entraîné dans un fichier .pkl
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)