# =============================================================================
# RESUMO DOS RESULTADOS DO GRIDSEARCH
# =============================================================================

from pathlib import Path
import pandas as pd

RESULTADOS_DIR = Path("resultados")
SAIDA_DIR = Path("tabelas")

SAIDA_DIR.mkdir(exist_ok=True)

arquivos = sorted(RESULTADOS_DIR.glob("*gridsearch*.csv"))

if not arquivos:
    print("Nenhum arquivo encontrado.")
    exit()

todos_resultados = []
melhores_resultados = []

for arquivo in arquivos:

    nome_modelo = (
        arquivo.stem
        .replace("_gridsearch_completo", "")
        .replace("_gridsearch", "")
    )

    print(f"Lendo {nome_modelo}")

    df = pd.read_csv(arquivo)

    # procura a coluna de parâmetros
    if "params" not in df.columns:
        print(f"Arquivo ignorado: {arquivo.name}")
        continue

    resumo = pd.DataFrame()

    resumo["Modelo"] = [nome_modelo] * len(df)
    resumo["Parâmetros"] = df["params"]

    resumo["Accuracy"] = (
        df["mean_test_accuracy"].round(4).astype(str)
        + " ± "
        + df["std_test_accuracy"].round(4).astype(str)
    )

    resumo["Precision"] = (
        df["mean_test_precision"].round(4).astype(str)
        + " ± "
        + df["std_test_precision"].round(4).astype(str)
    )

    resumo["Recall"] = (
        df["mean_test_recall"].round(4).astype(str)
        + " ± "
        + df["std_test_recall"].round(4).astype(str)
    )

    resumo["F1"] = (
        df["mean_test_f1"].round(4).astype(str)
        + " ± "
        + df["std_test_f1"].round(4).astype(str)
    )

    todos_resultados.append(resumo)

    # melhor combinação por F1
    melhor_idx = df["mean_test_f1"].idxmax()

    melhores_resultados.append({
        "Modelo": nome_modelo,
        "Parâmetros": df.loc[melhor_idx, "params"],
        "Accuracy": f"{df.loc[melhor_idx,'mean_test_accuracy']:.4f} ± {df.loc[melhor_idx,'std_test_accuracy']:.4f}",
        "Precision": f"{df.loc[melhor_idx,'mean_test_precision']:.4f} ± {df.loc[melhor_idx,'std_test_precision']:.4f}",
        "Recall": f"{df.loc[melhor_idx,'mean_test_recall']:.4f} ± {df.loc[melhor_idx,'std_test_recall']:.4f}",
        "F1": f"{df.loc[melhor_idx,'mean_test_f1']:.4f} ± {df.loc[melhor_idx,'std_test_f1']:.4f}",
        "F1_medio": df.loc[melhor_idx, "mean_test_f1"]
    })

# =============================================================================
# TODAS AS COMBINAÇÕES
# =============================================================================

tabela_completa = pd.concat(
    todos_resultados,
    ignore_index=True
)

arquivo_completo = SAIDA_DIR / "todas_combinacoes.csv"

tabela_completa.to_csv(
    arquivo_completo,
    index=False
)

print(f"\nSalvo: {arquivo_completo}")

# =============================================================================
# MELHOR CONFIGURAÇÃO DE CADA ALGORITMO
# =============================================================================

melhores = pd.DataFrame(melhores_resultados)

melhores = melhores.sort_values(
    by="F1_medio",
    ascending=False
)

arquivo_melhores = SAIDA_DIR / "melhores_modelos.csv"

melhores.to_csv(
    arquivo_melhores,
    index=False
)

print(f"Salvo: {arquivo_melhores}")

# =============================================================================
# LATEX
# =============================================================================

latex_df = melhores.drop(columns=["F1_medio"])

latex = latex_df.to_latex(
    index=False,
    escape=True,
    longtable=False
)

arquivo_latex = SAIDA_DIR / "melhores_modelos.tex"

with open(arquivo_latex, "w", encoding="utf-8") as f:
    f.write(latex)

print(f"Salvo: {arquivo_latex}")

print("\nRanking final:")

print(
    melhores[
        [
            "Modelo",
            "Accuracy",
            "Precision",
            "Recall",
            "F1"
        ]
    ]
)