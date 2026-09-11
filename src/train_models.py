from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "processed" / "players_clean.csv"
MODEL_DIR = ROOT / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

target = "purchase_flag"

features = [
    "age",
    "gender",
    "location",
    "game_genre",
    "game_difficulty",
    "sessions_per_week",
    "avg_session_duration_minutes",
    "player_level",
    "achievements_unlocked",
    "total_events",
    "days_since_last_seen",
    "account_age_days"
]

X = df[features]
y = df[target]

numeric_features = [
    "age",
    "sessions_per_week",
    "avg_session_duration_minutes",
    "player_level",
    "achievements_unlocked",
    "total_events",
    "days_since_last_seen",
    "account_age_days"
]

categorical_features = [
    "gender",
    "location",
    "game_genre",
    "game_difficulty"
]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )
}

results = {}

for name, model in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    results[name] = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities)
    }

    print(f"\n{name}")
    print("-" * len(name))
    print(f"Accuracy : {results[name]['accuracy']:.4f}")
    print(f"Precision: {results[name]['precision']:.4f}")
    print(f"Recall   : {results[name]['recall']:.4f}")
    print(f"F1 Score : {results[name]['f1']:.4f}")
    print(f"ROC-AUC  : {results[name]['roc_auc']:.4f}")

best_model_name = max(
    results,
    key=lambda name: results[name]["roc_auc"]
)

best_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", models[best_model_name])
])

best_model.fit(X_train, y_train)

model_file = MODEL_DIR / "purchase_model.pkl"

joblib.dump(best_model, model_file)

print("\nBest Model:", best_model_name)
print("Saved:", model_file)