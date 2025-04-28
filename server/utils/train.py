from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import  pickle
from sklearn.pipeline import make_pipeline
from   sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
model = make_pipeline(scaler, DecisionTreeClassifier(random_state=42))

data = pd.read_csv("./server/utlis/iris.csv")

X = data.drop("label", axis=1)
y = data["label"]


model.fit(X, y)

with open("./server/model.pkl", "wb") as f:
    pickle.dump(model, f)