from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import  pickle
from sklearn.pipeline import make_pipeline
from   sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
model = make_pipeline(scaler, DecisionTreeClassifier(random_state=42))

# Charger le jeu de données Iris
data = pd.read_csv("data/iris.csv")

X = data.drop("species", axis=1)
y = data["species"]

# Entraîner le modèle
model.fit(X, y)

# Sauvegarder le modèle entraîné dans un fichier .pkl
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)