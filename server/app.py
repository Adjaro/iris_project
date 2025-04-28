import pickle
from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Charger le modèle au démarrage de l'application
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    # Test du modèle
    X_test = [[5.1, 3.5, 1.4, 0.2]]
    test_prediction = model.predict(X_test)
    print(f"Test prediction: {test_prediction}")
except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    model = None


class InputData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.post("/predict")
def predict(data: InputData):
    if model is None:
        return {"error": "Le modèle n'est pas chargé"}

    # Conversion des données d'entrée en array
    input_data = np.array(
        [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    )

    try:
        prediction = model.predict(input_data)
        # probabilities = model.predict_proba(input_data)
        probabilities = model.predict_proba(input_data)
        probabilities = probabilities[:, 1]  # Probabilité de la classe positive
        return {
            "prediction": prediction.tolist()[0],
            "probabilities": probabilities.tolist()[0],
        }
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction: {str(e)}"}
