README - Entrega Integrante 3

Este arquivo descreve a organização e a finalidade dos artefatos gerados no notebook.

1. Arquivos de descrição estatística do dataset

- resumo_dataset.csv
  Apresenta um resumo geral do conjunto de dados, incluindo quantidade de registros, quantidade de atributos e informações gerais utilizadas na caracterização do Adult Income Dataset.

- descricao_estatistica_numericas.csv
  Contém as estatísticas descritivas das variáveis numéricas do dataset, como média, desvio padrão, valores mínimo e máximo e quartis.

- distribuicao_classes.csv
  Apresenta a distribuição quantitativa das classes da variável-alvo, permitindo verificar o desbalanceamento entre as classes <=50K e >50K.

- distribuicao_classes.png
  Gráfico da distribuição das classes do dataset. Este arquivo serve como apoio visual para a análise do desbalanceamento da variável-alvo.

- valores_ausentes.csv
  Indica a quantidade de valores ausentes identificados em cada coluna do dataset, auxiliando na verificação da qualidade dos dados antes do treinamento dos modelos.

2. Arquivos da Árvore de Decisão

- cv_results_DecisionTree.csv
  Registra os resultados completos da validação cruzada realizada pelo GridSearchCV para a Árvore de Decisão, incluindo as combinações de hiperparâmetros testadas, médias e desvios padrão das métricas.

- classification_report_DecisionTree.csv
  Contém o relatório de classificação da Árvore de Decisão, com métricas como precisão, recall e F1-score por classe.

- matriz_confusao_DecisionTree.csv
  Matriz de confusão da Árvore de Decisão em formato tabular, indicando os acertos e erros do modelo nas classes avaliadas.

- matriz_confusao_DecisionTree.png
  Representação gráfica da matriz de confusão da Árvore de Decisão.

- GridSearch_DecisionTree.joblib
  Objeto do GridSearchCV da Árvore de Decisão salvo em formato joblib, permitindo consultar os parâmetros avaliados e o melhor modelo encontrado.

- Modelo_Final_DecisionTree.joblib
  Modelo final da Árvore de Decisão treinado com os melhores hiperparâmetros encontrados.

3. Arquivos do KNN

- cv_results_KNN.csv
  Registra os resultados completos da validação cruzada realizada pelo GridSearchCV para o KNN, incluindo as combinações de hiperparâmetros testadas, médias e desvios padrão das métricas.

- classification_report_KNN.csv
  Contém o relatório de classificação do KNN, com métricas como precisão, recall e F1-score por classe.

- matriz_confusao_KNN.csv
  Matriz de confusão do KNN em formato tabular, indicando os acertos e erros do modelo nas classes avaliadas.

- matriz_confusao_KNN.png
  Representação gráfica da matriz de confusão do KNN.

- GridSearch_KNN.joblib
  Objeto do GridSearchCV do KNN salvo em formato joblib, permitindo consultar os parâmetros avaliados e o melhor modelo encontrado.

- Modelo_Final_KNN.joblib
  Modelo final do KNN treinado com os melhores hiperparâmetros encontrados.

4. Arquivos de comparação e consolidação dos resultados

- resumo_gridsearch_modelos.csv
  Resume os principais resultados obtidos pelos modelos Árvore de Decisão e KNN após a otimização por GridSearchCV.

- tabela_artigo_gridsearch.csv
  Tabela organizada com os resultados finais de Árvore de Decisão e KNN, contendo médias e desvios padrão das métricas para possível uso no artigo.

- comparacao_metricas_gridsearch.png
  Gráfico comparativo das métricas da Árvore de Decisão e do KNN após a otimização por GridSearchCV.

- metricas_modelos_csv.csv
  Consolida as métricas calculadas a partir dos arquivos CSV de predição dos modelos da equipe, permitindo comparar os classificadores em uma mesma estrutura.

- comparacao_modelos_csv.png
  Gráfico comparativo dos modelos avaliados a partir dos arquivos CSV de predição, incluindo métricas como acurácia, precisão, recall, F1-score e balanced accuracy.

5. Arquivo de verificação

- checklist_arquivos_gerados.csv
  Lista de conferência dos arquivos gerados, usada para verificar se os artefatos essenciais da entrega foram produzidos corretamente.
