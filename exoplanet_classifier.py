# -*- coding: utf-8 -*-
"""Exoplanet-classifier

Automatically generated by Colab.

Importar Bibliotecas e Configurar Logging
"""

# Cell 1: Importar Bibliotecas e Configurar Logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import joblib

# Scikit-learn
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold, KFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Cell 1 executada com sucesso!")

"""Função de Carregamento de Dados


"""

# Cell 2: Função para Carregar Dados da API e carregar o dataset confirmado
def load_data(source):
    if source == "confirmed":
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars&format=csv"
    elif source == "candidates":
        url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=toi&format=csv"
    else:
        raise ValueError("Fonte inválida! Use 'confirmed' ou 'candidates'.")

    logger.info(f"Carregando dados ({source}) da API da NASA...")
    df = pd.read_csv(url)
    logger.info(f"Dados carregados com sucesso! Formato: {df.shape}")
    return df

# Carrega o dataset confirmado
df_confirmed = load_data("confirmed")
print("Shape do dataset confirmado:", df_confirmed.shape)
print("Colunas do dataset confirmado:", df_confirmed.columns.tolist())

# Observação:
# Caso queira testar os candidatos, você poderá executar:

df_candidates = load_data("candidates")
print(df_candidates.head())

# Mas, se a API dos candidatos estiver retornando erro, você poderá prosseguir apenas com os confirmados.

"""Função de Pré-processamento e Engenharia de Features:

Nesta célula vamos definir a função de pré-processamento. Para o dataset confirmado, vamos discretizar a coluna "pl_orbper" (período orbital) para transformar o problema em classificação.
"""

# Cell 3: Função de Pré-processamento e Engenharia de Features
def preprocess_data(df, target_col, discretize=False, bins=3, labels=None):
    # Verifica se a coluna alvo existe
    if target_col not in df.columns:
        raise KeyError(f"Coluna alvo '{target_col}' não encontrada. Colunas disponíveis: {df.columns.tolist()}")

    # Se discretizar, utiliza pd.qcut com duplicates='drop'
    if discretize:
        if labels is None:
            labels = ['curto', 'médio', 'longo']
        new_target = target_col + "_cat"
        try:
            df[new_target] = pd.qcut(df[target_col], q=bins, labels=labels, duplicates='drop')
        except ValueError as e:
            logger.error(f"Erro ao discretizar a variável '{target_col}': {e}")
            raise
        target_col = new_target
        logger.info(f"Coluna '{target_col}' discretizada em categorias.")

    # Remove linhas com valores ausentes na coluna alvo
    df = df.dropna(subset=[target_col])

    # Remove colunas indesejadas, por exemplo 'rowid', se existir
    if 'rowid' in df.columns:
        df = df.drop(columns=['rowid'])

    # Define as features e a variável alvo
    feature_cols = [col for col in df.columns if col != target_col]
    X = df[feature_cols]
    y = df[target_col]

    # Se o alvo for categórico (object ou categorical), aplica LabelEncoder
    if y.dtype == 'object' or isinstance(y.dtype, pd.CategoricalDtype):
        le = LabelEncoder()
        y = le.fit_transform(y)

    # Converte y para pd.Series (para facilitar o uso de value_counts depois)
    y = pd.Series(y, index=X.index)

    # Identifica colunas numéricas e categóricas
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    logger.info(f"Colunas numéricas: {numeric_cols}")
    logger.info(f"Colunas categóricas: {categorical_cols}")

    # Cria pipelines para pré-processamento
    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_pipeline, numeric_cols),
        ('cat', categorical_pipeline, categorical_cols)
    ], remainder='drop')

    return X, y, preprocessor

# Aplica o pré-processamento ao dataset confirmado, discretizando "pl_orbper"
X_confirmed, y_confirmed, preprocessor_confirmed = preprocess_data(
    df_confirmed, target_col="pl_orbper", discretize=True, bins=3, labels=['curto', 'médio', 'longo']
)

print("Shapes após pré-processamento:")
print("X_confirmed:", X_confirmed.shape)
print("y_confirmed distribuição:")
print(y_confirmed.value_counts())

"""Função de Treinamento e Avaliação dos Modelos
Nesta célula definiremos a função para treinar e avaliar os modelos. Note que, para verificar a distribuição das classes, convertemos y para uma Série (caso já não seja) e usamos o value_counts(). Se a classe com menos amostras tiver menos de 2 membros, removemos a estratificação.
"""

# Cell 4: Função de Treinamento e Avaliação dos Modelos
def train_and_evaluate(X, y, preprocessor, dataset_name):
    # Converte y para pd.Series, caso não seja
    y_series = pd.Series(y)
    min_count = y_series.value_counts().min()
    if min_count < 2:
        logger.warning("A menor classe possui apenas %d amostra(s). Removendo estratificação.", min_count)
        stratify_param = None
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
    else:
        stratify_param = y_series
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Divisão em treino e teste com embaralhamento
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify_param, shuffle=True
    )

    # Define os modelos e seus hiperparâmetros
    models = {
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'RandomForest': RandomForestClassifier(random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }

    param_grids = {
        'LogisticRegression': {'classifier__C': [0.1, 1.0, 10.0]},
        'RandomForest': {'classifier__n_estimators': [100, 200]},
        'XGBoost': {'classifier__n_estimators': [100, 200]}
    }

    best_model = None
    best_score = 0
    best_model_name = None

    for model_name, classifier in models.items():
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', classifier)
        ])
        search = RandomizedSearchCV(
            pipeline,
            param_distributions=param_grids[model_name],
            cv=cv,
            scoring='accuracy',
            random_state=42,
            n_jobs=-1
        )
        search.fit(X_train, y_train)
        logger.info(f"{dataset_name} - {model_name} melhores parâmetros: {search.best_params_}")
        logger.info(f"{dataset_name} - {model_name} acurácia (CV): {search.best_score_:.4f}")

        if search.best_score_ > best_score:
            best_score = search.best_score_
            best_model = search
            best_model_name = model_name

    # Avaliação no conjunto de teste
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"{dataset_name} - Melhor modelo: {best_model_name}")
    logger.info(f"{dataset_name} - Acurácia no teste: {test_accuracy:.4f}")
    print("Relatório de Classificação:")
    print(classification_report(y_test, y_pred))

    return best_model, best_model_name, best_score

# Treina e avalia os modelos utilizando o dataset confirmado
best_model_confirmed, name_confirmed, score_confirmed = train_and_evaluate(
    X_confirmed, y_confirmed, preprocessor_confirmed, "confirmed"
)

# Cell 5: Salvando o Melhor Modelo
joblib.dump(best_model_confirmed, "best_exoplanet_model.joblib")
print("Melhor modelo salvo como 'best_exoplanet_model.joblib'.")
