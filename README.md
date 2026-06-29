# Predição de Renda (Adult Dataset): Pipeline de Classificação e Artigo Científico

Este repositório reúne todo o pipeline de aprendizado de máquina (Machine Learning) utilizado para a classificação preditiva do **Adult Income Dataset**, incluindo os scripts de análise estatística e a estrutura completa em LaTeX necessária para a compilação do artigo científico correspondente.

## 👥 Autores e Contribuidores

* **Victor Rodrigues de Lima**
* **Gladistony Silva Lins**
* **Erick Jonathan Macedo dos Santos**
* **Isaac Adler Alves de Oliveira**
* **Instituição**: Universidade Federal Rural de Pernambuco (UFRPE) / Unidade Acadêmica de Belo Jardim

---

## 📖 Sobre o Projeto

O objetivo principal deste estudo é prever se a renda anual de um indivíduo ultrapassa a marca de 50 mil dólares com base em dados censitários (demográficos e socioeconômicos). 

Devido à forte presença de dados heterogêneos e ao desbalanceamento de classes, o projeto implementa um fluxo rigoroso de pré-processamento para evitar o vazamento de dados (*data leakage*). O treinamento e a otimização foram conduzidos com validação cruzada estratificada em 10 partições (*10-fold Cross-Validation*), avaliando seis algoritmos distintos:
* Árvore de Decisão (*Decision Tree*)
* Regressão Logística (*Logistic Regression*)
* K-Vizinhos Mais Próximos (*KNN*)
* Support Vector Machine Linear (*LinearSVC*)
* Rede Neural Artificial (*MLP*)
* Naive Bayes Gaussiano (*GaussianNB*)

---

## 📁 Estrutura do Repositório

* **`Codigo/`**: Contém o pipeline principal em Python, englobando o pré-processamento (imputação, *Z-score*, *One-Hot Encoding*), o *GridSearchCV*, scripts de cálculo de desvio padrão, geração de matrizes de confusão e arquivos exportados (modelos em `.joblib`, predições em CSV e gráficos).
* **`Artigo Latex/`**: Código-fonte completo do artigo científico formatado rigorosamente nos padrões da Sociedade Brasileira de Computação (SBC).
* **`Resultados/`**: Relatórios quantitativos, compilações estatísticas e tabelas comparativas geradas ao final da execução dos modelos.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo no seu terminal para configurar o ambiente isolado, instalar as dependências, rodar os experimentos preditivos e compilar o artigo em PDF.

### 1. Configurar o Ambiente Virtual e Instalar Dependências

Navegue até a raiz do projeto, crie o ambiente virtual `.venv`, ative-o e instale as bibliotecas necessárias listadas no `requirements.txt`:

```bash
# Criar o ambiente virtual
python3 -m venv .venv

# Ativar o ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Ativar o ambiente virtual (Windows)
# .venv\Scripts\activate

# Instalar os requerimentos
pip install -r Codigo/requirements.txt

```

### 2. Executar o Pipeline de Código

Os scripts localizados no diretório `Codigo/` devem ser executados estritamente na sequência estruturada abaixo. Isso garante que os dados de treino e os arquivos de cache sejam gerados e alimentados corretamente para as próximas etapas:

```bash
# Navegar até a pasta do código fonte
cd Codigo

# Passo 1: Executar o pré-processamento, pipeline principal e otimização dos modelos
python3 Main.py

# Passo 2: Calcular as métricas consolidadas e o desvio padrão (K-Fold)
python3 desvio_padrao.py

# Passo 3: Gerar as matrizes de confusão e gráficos de avaliação
python3 gerar_confusao.py

```

### 3. Compilar o Artigo LaTeX

Para gerar o documento final em PDF contendo todas as referências cruzadas, citações bibliográficas (BibTeX) e as imagens atualizadas pelo código, utilize o utilitário `latexmk`:

```bash
# Retornar à raiz e entrar na pasta do artigo
cd "../Artigo Latex"

# Compilar o documento automaticamente
latexmk -pdf main.tex

```

O arquivo final com a pesquisa completa, nomeado como **`main.pdf`**, será gerado automaticamente dentro da pasta do artigo.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem**: Python 3
* **Machine Learning**: Scikit-Learn
* **Processamento e Manipulação de Dados**: Pandas, NumPy
* **Persistência de Modelos**: Joblib
* **Visualização de Dados**: Matplotlib, Seaborn
* **Documentação Científica**: TeX Live / LaTeX (`latexmk`)
