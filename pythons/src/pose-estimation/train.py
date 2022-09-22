import pickle
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

df = pd.read_csv("coords.csv")
df = df.dropna(axis=1)
X = df.drop("label", axis=1)
y = df["label"]
X = X.values
y = y.values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=777
)

pipelines = {
    "lr": make_pipeline(StandardScaler(), LogisticRegression()),
    "rc": make_pipeline(StandardScaler(), RidgeClassifier()),
    "rf": make_pipeline(StandardScaler(), RandomForestClassifier()),
    "gb": make_pipeline(StandardScaler(), GradientBoostingClassifier()),
}

fit_models = {}
for algo, pipeline in pipelines.items():
    model = pipeline.fit(X_train, y_train)
    fit_models[algo] = model


for algo, model in fit_models.items():
    result = model.predict(X_test)
    print(algo, accuracy_score(y_test, result))

with open("face.pkl", "wb") as f:
    pickle.dump(fit_models["rf"], f)
