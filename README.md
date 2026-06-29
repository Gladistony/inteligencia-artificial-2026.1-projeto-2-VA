# Pipeline de Classificação (Adult Dataset) e Artigo LaTeX

Este repositório contém o pipeline completo de machine learning para classificação do *Adult Dataset*, além dos códigos de análise e a estrutura para compilação do artigo científico associado.

---

## 📁 Estrutura do Projeto

*   **`Codigo/`**: Contém o pipeline em Python, scripts de desvio padrão, matrizes de confusão e arquivos gerados (modelos salvos em `.joblib`, predições e tabelas).
*   **`Artigo Latex/`**: Código-fonte do artigo formatado nos padrões da SBC.
*   **`Resultados/`**: Relatórios estatísticos, gráficos e comparativos finais gerados pelos modelos.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo no terminal para configurar o ambiente, instalar as dependências, rodar os experimentos e compilar o artigo.

### 1. Configurar o Ambiente Virtual e Instalar Dependências

Entre na raiz do projeto, crie o ambiente virtual `.venv`, ative-o e instale as bibliotecas necessárias listadas no `requirements.txt`:

```bash
# Criar o ambiente virtual
python3 -m venv .venv

# Ativar o ambiente virtual
source .venv/bin/activate

# Instalar os requerimentos
pip install -r Codigo/requirements.txt
```

### 2. Executar o Pipeline de Código

Os scripts do diretório `Codigo/` devem ser executados estritamente na sequência abaixo para que os dados e arquivos de cache sejam alimentados corretamente:

```bash
# Navegar até a pasta do código
cd Codigo

# 1º Passo: Executar o pipeline principal e treinamento dos modelos
python3 Main.py

# 2º Passo: Calcular as métricas e o desvio padrão
python3 desvio_padrao.py

# 3º Passo: Gerar as matrizes e gráficos de confusão
python3 gerar_confusão.py

```

### 3. Compilar o Artigo LaTeX

Para gerar o PDF final do artigo contendo todas as referências cruzadas, citações bibliográficas (BibTeX) e imagens atualizadas, utilize o `latexmk`:

```bash
# Entrar na pasta do artigo
cd "Artigo Latex"

# Compilar o documento automaticamente
latexmk -pdf main.tex
```

O arquivo final **`main.pdf`** será gerado automaticamente na mesma pasta.

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem**: Python 3
*   **Machine Learning**: Scikit-Learn (Decision Tree, KNN, Naive Bayes, Logistic Regression, SVM, MLP)
*   **Processamento de Dados**: Pandas, NumPy
*   **Persistência de Modelos**: Joblib
*   **Texto/Documentação**: TeX Live / LaTeX (`latexmk`)
