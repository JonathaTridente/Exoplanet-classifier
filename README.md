# Exoplanets Classification & Incremental Learning Pipeline

Este repositório contém um pipeline completo de Machine Learning para a classificação de exoplanetas, abrangendo desde a exploração dos dados até a geração de dashboards e treinamento incremental. O projeto demonstra boas práticas em pré-processamento, engenharia de features, otimização de hiperparâmetros, rastreamento com logging, exportação de modelos e predição para novos dados.

---

## Funcionalidades

### Exploração de Dados (EDA)
- **Carregamento e Inspeção dos Dados:**  
  Importa os dados diretamente da API da NASA e realiza a inspeção inicial.
- **Visualizações:**  
  Geração de histogramas, contagem de classes e outras visualizações para melhor entendimento dos dados.

### Pré-processamento e Engenharia de Features
- **Transformações Avançadas:**  
  Separação de colunas numéricas e categóricas utilizando `ColumnTransformer`.
- **Tratamento de Dados Faltantes:**  
  Imputação de valores ausentes e escalonamento dos dados.
- **Codificação:**  
  Utilização de One-Hot Encoding para variáveis categóricas e Label Encoding para o alvo.
- **Discretização:**  
  Conversão de variáveis contínuas (ex.: período orbital) em categorias para facilitar a classificação.

### Treinamento e Otimização de Modelos
- **Modelos Implementados:**  
  - Logistic Regression  
  - Random Forest  
  - XGBoost  
- **Otimização de Hiperparâmetros:**  
  Uso de `RandomizedSearchCV` com validação cruzada (estratificada ou KFold, conforme a distribuição dos dados).
- **Seleção do Melhor Modelo:**  
  Comparação de modelos com base na acurácia e outras métricas de performance.

### Dashboard de Resultados
- **Relatórios e Visualizações:**  
  Geração de relatórios em HTML com os principais resultados, métricas e matrizes de confusão.

### Treinamento Incremental
- **Atualização Contínua do Modelo:**  
  Implementação de treinamento incremental utilizando `SGDClassifier` com `partial_fit`, permitindo que o modelo seja atualizado à medida que novos dados chegam.

### Exportação e Predição
- **Exportação dos Modelos:**  
  Salvamento dos modelos treinados utilizando `joblib`.
- **Predição para Novos Dados:**  
  Função para realizar predições em novos datasets e salvar os resultados em CSV.

---

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

## Estrutura do Repositório

```plaintext
.
├── README.md              # Este arquivo de documentação
├── main.py                # Código principal do pipeline
├── requirements.txt       # Lista de dependências do projeto
└── data
    └── transits_0130135810_2025_30_01.csv   # Arquivo CSV de exemplo para os dados

