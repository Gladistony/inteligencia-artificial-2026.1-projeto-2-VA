# =============================================================================
# ADULT DATASET CLASSIFICATION PIPELINE
# - Local adult.zip
# - Holdout cache (20%)
# - GridSearchCV (10-fold)
# - Model cache (.joblib)
# - Reuse trained models on future runs
# =============================================================================

import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

from joblib import dump, load

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    GridSearchCV
)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
    OneHotEncoder
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier


# -----------------------------------------------------------------------------
# CONFIGURAÇÃO
# -----------------------------------------------------------------------------

FORCAR_RETREINO = False

ZIP_PATH = "adult.zip"

MODELOS_DIR = Path("modelos")
CACHE_DIR = Path("cache")
PREDICOES_DIR = Path("predicoes")
CONFUSOES_DIR = Path("confusoes")

for d in [MODELOS_DIR, CACHE_DIR, PREDICOES_DIR, CONFUSOES_DIR]:
    d.mkdir(exist_ok=True)

HOLDOUT_FILE = CACHE_DIR / "holdout.joblib"
CV_RESULTS_FILE = CACHE_DIR / "resultados_cv.csv"
RANKING_FILE = "ranking_holdout.csv"

RESULTADOS_DIR = Path("resultados")
RESULTADOS_DIR.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# CARREGAR DATASET
# -----------------------------------------------------------------------------

print("=" * 80)
print("CARREGANDO ADULT DATASET")
print("=" * 80)

COLUNAS = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education_num",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
    "native_country",
    "income"
]

with zipfile.ZipFile(ZIP_PATH) as z:

    with z.open("adult.data") as f:
        train_df = pd.read_csv(
            f,
            names=COLUNAS,
            header=None,
            skipinitialspace=True
        )

    with z.open("adult.test") as f:
        test_df = pd.read_csv(
            f,
            names=COLUNAS,
            header=None,
            skiprows=1,
            skipinitialspace=True
        )

df = pd.concat([train_df, test_df], ignore_index=True)

df["income"] = (
    df["income"]
    .astype(str)
    .str.replace(".", "", regex=False)
    .str.strip()
)

df.replace("?", np.nan, inplace=True)

print(f"Registros originais: {len(df):,}")

antes = len(df)
df = df.drop_duplicates()
print(f"Duplicatas removidas: {antes - len(df)}")
print(f"Registros finais: {len(df):,}")

X = df.drop(columns=["income"])
y = df["income"]

le = LabelEncoder()
y_encoded = le.fit_transform(y)


# -----------------------------------------------------------------------------
# HOLDOUT CACHE
# -----------------------------------------------------------------------------

if HOLDOUT_FILE.exists() and not FORCAR_RETREINO:

    print("\nUsando holdout salvo.")

    dados = load(HOLDOUT_FILE)

    X_dev = dados["X_dev"]
    y_dev = dados["y_dev"]

    X_holdout = dados["X_holdout"]
    y_holdout = dados["y_holdout"]

else:

    print("\nCriando novo holdout.")

    X_dev, X_holdout, y_dev, y_holdout = train_test_split(
        X,
        y_encoded,
        test_size=0.20,
        stratify=y_encoded,
        random_state=42
    )

    dump(
        {
            "X_dev": X_dev,
            "y_dev": y_dev,
            "X_holdout": X_holdout,
            "y_holdout": y_holdout
        },
        HOLDOUT_FILE
    )

print(f"Desenvolvimento: {len(X_dev):,}")
print(f"Holdout: {len(X_holdout):,}")


# -----------------------------------------------------------------------------
# PREPROCESSAMENTO
# -----------------------------------------------------------------------------

numeric_features = [
    "age",
    "fnlwgt",
    "education_num",
    "capital_gain",
    "capital_loss",
    "hours_per_week"
]

categorical_features = [
    c for c in X.columns
    if c not in numeric_features
]

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)


# -----------------------------------------------------------------------------
# MODELOS
# -----------------------------------------------------------------------------

models = [
    (
        "DecisionTree",
        DecisionTreeClassifier(random_state=42),
        {
            "classifier__criterion": ["gini", "entropy"],
            "classifier__max_depth": [5, 10, 20, None],
            "classifier__min_samples_split": [2, 5, 10]
        }
    ),
    (
        "KNN",
        KNeighborsClassifier(),
        {
            "classifier__n_neighbors": [3, 5, 7, 11],
            "classifier__weights": ["uniform", "distance"]
        }
    ),
    (
        "GaussianNB",
        GaussianNB(),
        {}
    ),
    (
        "LogisticRegression",
        LogisticRegression(
            max_iter=3000,
            random_state=42
        ),
        {
            "classifier__C": [0.01, 0.1, 1, 10]
        }
    ),
    (
        "LinearSVM",
        LinearSVC(
            max_iter=10000,
            random_state=42
        ),
        {
            "classifier__C": [0.01, 0.1, 1, 10]
        }
    ),
    (
        "MLP",
        MLPClassifier(
            max_iter=1000,
            random_state=42
        ),
        {
            "classifier__hidden_layer_sizes": [
                (64,),
                (128,),
                (64, 32)
            ],
            "classifier__activation": [
                "relu",
                "tanh"
            ],
            "classifier__alpha": [
                0.0001,
                0.001
            ]
        }
    )
]


# -----------------------------------------------------------------------------
# CROSS VALIDATION
# -----------------------------------------------------------------------------

cv_strategy = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)

scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1"
}

resultados_cv = []
ranking_holdout = []


# -----------------------------------------------------------------------------
# TREINAR OU CARREGAR MODELOS
# -----------------------------------------------------------------------------

for nome, estimador, parametros in models:

    print("\n" + "=" * 80)
    print(nome)
    print("=" * 80)

    modelo_file = MODELOS_DIR / f"{nome}.joblib"

    if modelo_file.exists() and not FORCAR_RETREINO:

        print("Carregando modelo salvo...")

        modelo = load(modelo_file)

        resultados_cv.append({
            "Modelo": nome,
            "CV_F1": np.nan,
            "Origem": "cache"
        })

    else:

        print("Treinando modelo...")

        pipeline = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("classifier", estimador)
            ]
        )

        grid = GridSearchCV(
            estimator=pipeline,
            param_grid=parametros,
            scoring=scoring,
            cv=cv_strategy,
            refit="f1",
            n_jobs=-1
        )

        grid.fit(X_dev, y_dev)

        modelo = grid.best_estimator_

        dump(modelo, modelo_file)

        resultados_cv.append({
            "Modelo": nome,
            "CV_F1": grid.best_score_,
            "Origem": "treinado"
        })

        resultado_grid = pd.DataFrame(grid.cv_results_)

        resultado_grid.to_csv(
            f"resultados/{nome}_gridsearch.csv",
            index=False
        )

        print(f"Melhor F1 CV: {grid.best_score_:.4f}")
        print(grid.best_params_)

    # -----------------------------------------------------------------
    # TESTE HOLDOUT
    # -----------------------------------------------------------------

    y_pred = modelo.predict(X_holdout)

    acc = accuracy_score(y_holdout, y_pred)
    prec = precision_score(y_holdout, y_pred)
    rec = recall_score(y_holdout, y_pred)
    f1 = f1_score(y_holdout, y_pred)

    ranking_holdout.append({
        "Modelo": nome,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1": f1
    })

    # Predições

    pd.DataFrame({
        "real": y_holdout,
        "predito": y_pred
    }).to_csv(
        PREDICOES_DIR / f"{nome}.csv",
        index=False
    )

    # Confusão

    cm = confusion_matrix(y_holdout, y_pred)

    pd.DataFrame(cm).to_csv(
        CONFUSOES_DIR / f"{nome}.csv",
        index=False
    )

    print(f"Holdout F1: {f1:.4f}")


# -----------------------------------------------------------------------------
# EXPORTA RESULTADOS
# -----------------------------------------------------------------------------

cv_df = pd.DataFrame(resultados_cv)
cv_df.to_csv(CV_RESULTS_FILE, index=False)

ranking_df = pd.DataFrame(ranking_holdout)

ranking_df = ranking_df.sort_values(
    by="F1",
    ascending=False
)

ranking_df.to_csv(
    RANKING_FILE,
    index=False
)

print("\n")
print("=" * 80)
print("RANKING FINAL HOLDOUT")
print("=" * 80)
print(ranking_df)

print("\nArquivos gerados:")
print(" - cache/resultados_cv.csv")
print(" - ranking_holdout.csv")
print(" - modelos/*.joblib")
print(" - predicoes/*.csv")
print(" - confusoes/*.csv")
