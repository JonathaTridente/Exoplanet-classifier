# Exoplanets Classification & Incremental Learning Pipeline

Este repositório contém um pipeline completo de Machine Learning para classificação de exoplanetas, desde a exploração dos dados até a geração de dashboards e treinamento incremental. O projeto demonstra boas práticas de pré-processamento, engenharia de features, otimização de hiperparâmetros, rastreamento com logging, exportação de modelos e predição para novos dados.

## Funcionalidades

- **Exploração de Dados (EDA):**
  - Carregamento e inspeção dos dados.
  - Visualizações: histogramas e contagem de classes.

- **Pré-processamento e Engenharia de Features:**
  - Separação de colunas numéricas e categóricas com `ColumnTransformer`.
  - Imputação, escalonamento e codificação one-hot.

- **Treinamento e Otimização de Modelos:**
  - Treinamento de múltiplos modelos (Logistic Regression, Random Forest e XGBoost).
  - Otimização de hiperparâmetros com `RandomizedSearchCV` e validação cruzada estratificada.
  - Seleção do melhor modelo com base em acurácia.

- **Dashboard de Resultados:**
  - Geração de relatório HTML contendo os principais resultados e a matriz de confusão.

- **Treinamento Incremental:**
  - Uso de `SGDClassifier` com `partial_fit` para atualização contínua do modelo.
  - Função para atualizar o modelo com novos dados.

- **Exportação e Predição:**
  - Exportação dos modelos treinados utilizando `joblib`.
  - Função para realizar predições em novos datasets e salvar os resultados em CSV.

## Estrutura do Repositório

. ├── README.md ├── main.py ├── requirements.txt └── data └── transits_0130135810_2025_30_01.csv


- **main.py:** Código principal do projeto.
- **requirements.txt:** Lista de dependências necessárias.
- **data:** Pasta para armazenar os arquivos CSV com os dados.

## Instalação

1. Clone o repositório:

   ```bash
   git clone <url-do-repositório>
   cd <nome-do-repositório>

Crie um ambiente virtual (opcional):
python -m venv venv
source venv/bin/activate   # Linux/MacOS
.\venv\Scripts\activate    # Windows

Instale as dependências:
pip install -r requirements.txt

Uso
Para executar o pipeline, basta rodar:
python main.py

O script realizará o seguinte:

Carregamento e exploração dos dados;
Pré-processamento e engenharia de features;
Treinamento, otimização e avaliação de modelos;
Geração de um dashboard HTML com os resultados;
Treinamento incremental e exportação dos modelos.
Contribuições
Contribuições são bem-vindas! Se você encontrar algum bug ou tiver sugestões de melhorias, por favor, abra uma issue ou envie um pull request.

Licença
Este projeto está licenciado sob a MIT License.


