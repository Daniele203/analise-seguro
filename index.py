import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Passo 1: Criar base de dados fictícia
# Dados fictícios para 15 clientes
dados = {
    'id_cliente': range(1, 16),
    'idade': [35, 42, 29, 50, 46, 38, 33, 40, 28, 45, 60, 27, 34, 48, 31],
    'genero': ['Feminino', 'Masculino', 'Feminino', 'Masculino', 'Masculino', 'Feminino', 'Feminino', 'Masculino', 'Feminino', 'Masculino', 'Feminino', 'Feminino', 'Masculino', 'Masculino', 'Feminino'],
    'estado_civil': ['Casado', 'Solteiro', 'Solteiro', 'Casado', 'Divorciado', 'Casado', 'Solteiro', 'Casado', 'Solteiro', 'Divorciado', 'Casado', 'Solteiro', 'Casado', 'Casado', 'Solteiro'],
    'renda': [5000, 7000, 3200, 10000, 8500, 6200, 4500, 7800, 3100, 9200, 11000, 3000, 5200, 8700, 4100],
    'tipo_imovel': ['Casa', 'Apartamento', 'Casa', 'Casa', 'Apartamento', 'Casa', 'Casa', 'Apartamento', 'Casa', 'Apartamento', 'Casa', 'Apartamento', 'Casa', 'Casa', 'Apartamento'],
    'valor_imovel': [300000, 400000, 200000, 500000, 450000, 320000, 250000, 420000, 210000, 480000, 600000, 190000, 310000, 460000, 230000],
    'localizacao': ['Centro', 'Bairro', 'Centro', 'Centro', 'Suburbio', 'Centro', 'Suburbio', 'Bairro', 'Centro', 'Bairro', 'Centro', 'Suburbio', 'Centro', 'Centro', 'Bairro'],
    'tempo_segurado': [2, 3, 1, 5, 4, 2, 1, 3, 1, 4, 6, 1, 2, 5, 1],
    'sinistros': [1, 0, 1, 2, 1, 0, 0, 1, 1, 0, 3, 0, 1, 2, 0],
    'valor_indenizado': [5000, 0, 3000, 20000, 10000, 0, 0, 8000, 4000, 0, 35000, 0, 7000, 15000, 0],
    'premio_anual': [1200, 1500, 800, 2500, 2000, 1300, 900, 1800, 750, 2200, 3000, 700, 1250, 2400, 950],
    'desconto': [0.05, 0.1, 0.02, 0.15, 0.1, 0.05, 0.03, 0.08, 0.02, 0.12, 0.2, 0.01, 0.04, 0.18, 0.03],
    'renovou': [1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0]
}

df = pd.DataFrame(dados)

# Preparação dos dados
variaveis_numericas = df.select_dtypes(include=['float64', 'int64']).columns
variaveis_categoricas = df.select_dtypes(include=['object']).columns

def preencher_nulos(df):
    for col in variaveis_numericas:
        df[col].fillna(df[col].median(), inplace=True)
    for col in variaveis_categoricas:
        df[col].fillna("Desconhecido", inplace=True)

preencher_nulos(df)

# Codificação de variáveis categóricas
df = pd.get_dummies(df, columns=variaveis_categoricas, drop_first=True)

# Separar X (variáveis explicativas) e y (alvo)
X = df.drop('renovou', axis=1)
y = df['renovou']

# Divisão entre treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Treinamento do modelo
modelo = RandomForestClassifier(random_state=42, n_estimators=100)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
y_prob = modelo.predict_proba(X_test)[:, 1]

# Adicionando os scores ao conjunto de teste
X_test['score_renovacao'] = y_prob
clientes_prioritarios = X_test[X_test['score_renovacao'] > 0.6]

# Função do Streamlit para criar o dashboard
st.title("Dashboard de Predição de Renovação de Seguro")

st.header("Base de Dados Fictícia")
st.dataframe(df)

st.header("Resultados do Modelo")
st.write(f"AUC-ROC do modelo: {roc_auc_score(y_test, y_prob):.2f}")

st.header("Clientes Prioritários")
st.write(f"Total de clientes prioritários: {len(clientes_prioritarios)}")
st.dataframe(clientes_prioritarios)

# Visualização: Matriz de Confusão
st.header("Matriz de Confusão")
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Não', 'Sim'], yticklabels=['Não', 'Sim'])
plt.title('Matriz de Confusão')
plt.xlabel('Predição')
plt.ylabel('Real')
st.pyplot(fig)
