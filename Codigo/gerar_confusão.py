from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

CONFUSOES_DIR = Path("confusoes")
SAIDA_DIR = Path("graficos_confusao")

SAIDA_DIR.mkdir(exist_ok=True)

for arquivo in CONFUSOES_DIR.glob("*.csv"):

    nome = arquivo.stem

    df = pd.read_csv(arquivo)

    # Remove possível coluna de índice criada pelo pandas
    if df.shape == (2, 3):
        df = df.iloc[:, 1:]

    cm = df.values

    print(nome, cm.shape)

    fig, ax = plt.subplots(figsize=(7, 6))

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["<=50K", ">50K"]
    )

    disp.plot(
        ax=ax,
        values_format="d",
        colorbar=True
    )

    plt.title(f"Matriz de Confusão - {nome}")

    plt.tight_layout()

    plt.savefig(
        SAIDA_DIR / f"{nome}.png",
        dpi=300
    )

    plt.close()

    print(f"Gerado: {nome}.png")