
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Membaca dataset
df = pd.read_csv("toyota_clean.csv")

# 2. Menentukan input dan target
X = df[[
    "model", "year", "transmission", "mileage",
    "fuel_type", "tax", "mpg", "engine_size"
]]

y = df["price"]

# 3. Preprocessing
categorical = ["model", "transmission", "fuel_type"]
numerical = ["year", "mileage", "tax", "mpg", "engine_size"]

preprocessor = ColumnTransformer([
    ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("numerical", StandardScaler(), numerical)
])

# 4. Pembagian data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Algoritma machine learning
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=100, random_state=42, n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "K-Nearest Neighbors": KNeighborsRegressor(n_neighbors=5)
}

results = []
best_score = -np.inf
best_name = ""

# 6. Training dan evaluasi
for name, algorithm in models.items():

    print(f"Training {name}...", flush=True)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", algorithm)
    ])

    cv_score = cross_val_score(
        pipeline, X_train, y_train,
        cv=5, scoring="r2"
    ).mean()

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
        "CV_R2": cv_score
    })

    print(f"R2: {r2:.4f}")

    if cv_score > best_score:
        best_score = cv_score
        best_name = name
        joblib.dump(pipeline, "model_toyota.pkl")

# 7. Menyimpan hasil evaluasi
results_df = pd.DataFrame(results)
results_df.to_csv("model_scores.csv", index=False)

print("\nHASIL EVALUASI MODEL")
print(results_df.to_string(index=False))

print("\nModel terbaik:", best_name)
print("Training berhasil!")
